[app]
title = BLE functions test
version = 1.0
package.name = kivy_ble_test
package.domain = org.kivy
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
requirements =
             python3==3.14.2,
             hostpython3==3.14.2,
             filetype==1.2.0,
             kivy==2.3.1,
             android,
             able_recipe

p4a.branch = v2026.05.09

android.api = 36
android.minapi = 22
android.ndk = 28c
android.accept_sdk_license = True
android.permissions =
                    (name=android.permission.BLUETOOTH;maxSdkVersion=30),
                    (name=android.permission.BLUETOOTH_ADMIN;maxSdkVersion=30),
                    android.permission.BLUETOOTH_SCAN,
                    android.permission.BLUETOOTH_CONNECT,
                    android.permission.BLUETOOTH_ADVERTISE,
                    android.permission.ACCESS_FINE_LOCATION

# Build all app ABIs here so CI can package device APKs and run emulator smoke tests
android.archs = arm64-v8a, armeabi-v7a, x86_64

# (str) Android's logcat filters to use
android.logcat_filters = *:S python:D

[buildozer]
warn_on_root = 1
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2
