package com.snakeusbip.client

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class DynamicInventoryParserTest {
    @Test
    fun parsesObjectInventory() {
        val device = DynamicInventoryParser.createDevices(
            listOf(
                DynamicInventoryParser.parseObject(
                    busId = "1-2",
                    vendorId = "046d",
                    productId = "c52b",
                    productName = "USB Receiver",
                    isShared = true
                )!!
            )
        )

        assertEquals(1, device.size)
        assertEquals("1-2", device.single().busId)
        assertEquals(0x046d, device.single().vendorId)
        assertEquals(0xc52b, device.single().productId)
        assertTrue(device.single().isShared)
    }

    @Test
    fun parsesWindowsInventoryAndExportState() {
        val devices = DynamicInventoryParser.createDevices(
            listOf(
                "1-1 : Local mouse [Not shared] (046d:c077)",
                "2-1 : Exported drive [Shared (forced)] (0781:5581)",
                "3-1 : Attached device [Attached to client] (abcd:1234)"
            ).mapNotNull(DynamicInventoryParser::parseLine)
        )

        assertEquals(3, devices.size)
        assertEquals("Local mouse", devices[0].productName)
        assertFalse(devices[0].isShared)
        assertTrue(devices[1].isShared)
        assertTrue(devices[2].isShared)
    }

    @Test
    fun parsesMacAndLinuxInventoryLinesAsUnshared() {
        val devices = DynamicInventoryParser.createDevices(
            listOf(
                "  1-4    : Logitech Controller [HID/Gamepad] (28de:1304)",
                "2-3 : USB Storage [Storage] (0781:5581)"
            ).mapNotNull(DynamicInventoryParser::parseLine)
        )

        assertEquals(2, devices.size)
        assertEquals(0x28de, devices[0].vendorId)
        assertEquals("Logitech Controller [HID/Gamepad]", devices[0].productName)
        assertFalse(devices[0].isShared)
        assertFalse(devices[1].isShared)
    }

    @Test
    fun ignoresInvalidEntriesAndDuplicateBusIds() {
        val devices = DynamicInventoryParser.createDevices(
            listOf(
                "invalid row",
                "1-1 : First (046d:c52b)",
                "1-1 : Duplicate (1234:5678)"
            ).mapNotNull(DynamicInventoryParser::parseLine) +
                listOfNotNull(
                    DynamicInventoryParser.parseObject("not-a-busid", "046d", "c52b", "Invalid", false)
                )
        )

        assertEquals(1, devices.size)
        assertEquals("First", devices.single().productName)
    }
}
