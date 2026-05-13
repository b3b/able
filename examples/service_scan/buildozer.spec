[app]
title = BLE scan dev service
version = 1.1
package.name = scanservice
package.domain = test.able
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

requirements =
             python3==3.14.2,
             hostpython3==3.14.2,
             filetype==1.2.0,
             kivy==2.3.1,
             android,
             able_recipe
services = Able:service.py:foreground

p4a.branch = v2026.05.09

android.api = 36
android.minapi = 22
android.ndk = 28c
android.accept_sdk_license = True
android.permissions =
                    FOREGROUND_SERVICE,
                    (name=android.permission.BLUETOOTH;maxSdkVersion=30),
                    (name=android.permission.BLUETOOTH_ADMIN;maxSdkVersion=30),
                    android.permission.BLUETOOTH_SCAN,
                    android.permission.BLUETOOTH_CONNECT,
                    android.permission.BLUETOOTH_ADVERTISE,
                    android.permission.ACCESS_FINE_LOCATION

[buildozer]
warn_on_root = 1
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2
