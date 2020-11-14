[app]
title = Alert Mi
version = 1.0
package.name = alert_mi
package.domain = org.kivy
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
android.permissions = BLUETOOTH, BLUETOOTH_ADMIN, ACCESS_COARSE_LOCATION
requirements = python3,kivy,android,able_recipe

[buildozer]
warn_on_root = 1
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2
