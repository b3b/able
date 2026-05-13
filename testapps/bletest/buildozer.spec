[app]
title = BLE functions test
version = 1.0
package.name = kivy_ble_test
package.domain = org.kivy
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
android.permissions = BLUETOOTH, BLUETOOTH_ADMIN, ACCESS_FINE_LOCATION
requirements = python3,kivy,android,able_recipe
android.accept_sdk_license = True

# Build all app ABIs here so CI can package device APKs and run emulator smoke tests
android.archs = arm64-v8a, armeabi-v7a, x86_64


# (str) Android's logcat filters to use
android.logcat_filters = *:S python:D

[buildozer]
warn_on_root = 1
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2
