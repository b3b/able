Changelog
=========

1.0.8
-----

* Added support to use `able` in Android services
* Added decorators:

  - `able.require_bluetooth_enabled`: to call `BluetoothDispatcher` method when bluetooth adapter becomes ready
  - `able.require_runtime_permissions`:  to call `BluetoothDispatcher` method when location runtime permission is granted


1.0.7
-----

* Added `able.advertising`: module to perform BLE advertise operations
* Added property to get and set Bluetoth adapter name


1.0.6
-----

* Fixed `TypeError` exception on `BluetoothDispatcher.enable_notifications`


1.0.5
-----

* Added `BluetoothDispatcher.bonded_devices` property: list of paired BLE devices

1.0.4
-----

* Fixed sending string data with `write_characteristic` function

1.0.3
-----

* Changed package version generation:

  - Version is set during the build, from the git tag
  - Development (git master) version is always "0.0.0"
* Added ATT MTU changing method and callback
* Added MTU changing example
* Fixed:

  - set `BluetoothDispatcher.gatt` attribute in GATT connection handler,
    to avoid possible `on_connection_state_change()` call before  the `gatt` attribute is set
