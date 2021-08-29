[app]
title = BLE service
version = 1.0
package.name = service
package.domain = test.able
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
android.permissions = BLUETOOTH,BLUETOOTH_ADMIN,ACCESS_FINE_LOCATION,FOREGROUND_SERVICE
requirements = kivy==2.0.0,plyer==2.0.0,python3,able_recipe
services = Able:service.py:foreground

android.api = 27
android.minapi = 22
android.ndk = 20b

[buildozer]
warn_on_root = 1
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2
