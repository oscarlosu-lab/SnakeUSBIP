package com.snakeusbip

import android.app.UiModeManager
import android.content.Context
import android.content.res.Configuration
import android.os.Bundle
import android.util.Log
import android.view.KeyEvent
import android.view.MotionEvent
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.ui.Modifier
import com.snakeusbip.catalog.UsbDeviceCatalog
import com.snakeusbip.gamepad.GamepadInputManager
import com.snakeusbip.gaming.sunshine.SunshineHandoffManager
import com.snakeusbip.theme.SnakeUSBIPTheme
import com.snakeusbip.ui.AppNavHost

class MainActivity : ComponentActivity() {

    companion object {
        private const val TAG = "MainActivity"
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        com.snakeusbip.data.AppPreferences.syncComponentState(applicationContext)
        UsbDeviceCatalog.initialize(applicationContext)
        SunshineHandoffManager.initialize(applicationContext)

        val isTv = isAndroidTv()
        Log.i(TAG, "SnakeUSBIP initialized. Running on Android TV / 10-foot mode: $isTv")

        setContent {
            SnakeUSBIPTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    AppNavHost(isTvMode = isTv)
                }
            }
        }
    }

    override fun dispatchGenericMotionEvent(event: MotionEvent): Boolean {
        GamepadInputManager.handleMotionEvent(event)
        return super.dispatchGenericMotionEvent(event)
    }

    override fun dispatchKeyEvent(event: KeyEvent): Boolean {
        if (SunshineHandoffManager.processKeyEvent(event)) {
            return true
        }
        GamepadInputManager.handleKeyEvent(event)
        return super.dispatchKeyEvent(event)
    }

    override fun onDestroy() {
        super.onDestroy()
        SunshineHandoffManager.shutdown()
    }

    private fun isAndroidTv(): Boolean {
        val uiModeManager = getSystemService(Context.UI_MODE_SERVICE) as? UiModeManager
        return uiModeManager?.currentModeType == Configuration.UI_MODE_TYPE_TELEVISION
    }
}
