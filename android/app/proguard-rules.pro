# ==============================================================================
# SnakeUSBIP Android — Production ProGuard & R8 Hardening Rules
# ==============================================================================

# Line numbers and source files for clean crash traces
-keepattributes SourceFile,LineNumberTable
-renamesourcefileattribute SourceFile

# Preserve standard annotations and generic signatures
-keepattributes *Annotation*,Signature,InnerClasses,EnclosingMethod

# ------------------------------------------------------------------------------
# Kotlin Coroutines & Flow
# ------------------------------------------------------------------------------
-keepnames class kotlinx.coroutines.internal.MainDispatcherFactory {}
-keepnames class kotlinx.coroutines.CoroutineExceptionHandler {}
-dontwarn kotlinx.coroutines.**

# ------------------------------------------------------------------------------
# Kotlinx Serialization
# ------------------------------------------------------------------------------
-keepclassmembers class * {
    @kotlinx.serialization.SerialName <fields>;
}
-keepclassmembers class * {
    *** Companion;
}
-keepclasseswithmembers class * {
    kotlinx.serialization.KSerializer serializer(...);
}

# ------------------------------------------------------------------------------
# USB/IP Binary Protocol, DTOs & Descriptors
# (Must preserve binary field layout for Big-Endian network serialization)
# ------------------------------------------------------------------------------
-keep class com.snakeusbip.protocol.** { *; }
-keep class com.snakeusbip.data.** { *; }
-keep class com.snakeusbip.catalog.** { *; }
-keep class com.snakeusbip.net.wan.** { *; }
-keep class com.snakeusbip.audio.** { *; }
-keep class com.snakeusbip.gamepad.** { *; }
-keep class com.snakeusbip.gaming.** { *; }

# ------------------------------------------------------------------------------
# Android System Components & Reflection Boundaries
# ------------------------------------------------------------------------------
-keep public class * extends android.app.Activity
-keep public class * extends android.app.Application
-keep public class * extends android.app.Service
-keep public class * extends android.content.BroadcastReceiver

# Ensure Foreground Service and Broadcast Receivers remain intact
-keep class com.snakeusbip.server.UsbIpServerService { *; }
-keep class com.snakeusbip.receiver.BootCompletedReceiver { *; }
-keep class com.snakeusbip.receiver.UsbAttachedReceiver { *; }

# ------------------------------------------------------------------------------
# Compose & Material 3
# ------------------------------------------------------------------------------
-dontwarn androidx.compose.**
-keep class androidx.compose.ui.platform.** { *; }
