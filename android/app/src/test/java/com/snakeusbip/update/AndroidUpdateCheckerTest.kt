package com.snakeusbip.update

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertTrue
import org.junit.Test
import java.io.File
import java.nio.file.Files

class AndroidUpdateCheckerTest {

    @Test
    fun semverComparisonWorksCorrectly() {
        assertTrue(AndroidUpdateChecker.isNewerVersion("1.3.0", "v1.4.0"))
        assertTrue(AndroidUpdateChecker.isNewerVersion("1.9.9", "1.10.0"))
        assertFalse(AndroidUpdateChecker.isNewerVersion("1.3.0", "v1.3.0"))
        assertFalse(AndroidUpdateChecker.isNewerVersion("1.4.0", "1.3.0"))
    }

    @Test
    fun parseReleaseJsonExtractsApkAndSha256Sums() {
        val json = """
        {
          "tag_name": "v1.4.0",
          "body": "Release notes",
          "assets": [
            {
              "name": "SnakeUSBIP-v1.4.0-universal.apk",
              "browser_download_url": "https://github.com/oscarlosu-lab/SnakeUSBIP/releases/download/v1.4.0/SnakeUSBIP-v1.4.0-universal.apk"
            },
            {
              "name": "SHA256SUMS.txt",
              "browser_download_url": "https://github.com/oscarlosu-lab/SnakeUSBIP/releases/download/v1.4.0/SHA256SUMS.txt"
            }
          ]
        }
        """.trimIndent()
        val res = AndroidUpdateChecker.parseReleaseJson(json, "1.3.0")
        assertTrue(res.updateAvailable)
        assertEquals("1.4.0", res.latestVersion)
        assertEquals("SnakeUSBIP-v1.4.0-universal.apk", res.apkName)
        assertNotNull(res.checksumUrl)
    }

    @Test
    fun extractAndVerifySha256DeletesTamperedFile() {
        val tmpDir = Files.createTempDirectory("snake_upd_test").toFile()
        try {
            val apk = File(tmpDir, "app.apk").apply { writeBytes("hello-apk".toByteArray()) }
            val validHash = AndroidUpdateChecker.computeSha256Hex(apk)
            val sums = "$validHash  app.apk\n0000000000000000000000000000000000000000000000000000000000000000  other.apk"

            assertEquals(validHash, AndroidUpdateChecker.extractExpectedSha256(sums, "app.apk"))
            assertTrue(AndroidUpdateChecker.verifyDownloadedApk(apk, validHash))
            assertTrue(apk.exists())

            apk.writeBytes("tampered-apk".toByteArray())
            assertFalse(AndroidUpdateChecker.verifyDownloadedApk(apk, validHash))
            assertFalse("Tampered APK must be deleted", apk.exists())
        } finally {
            tmpDir.deleteRecursively()
        }
    }
}
