from android import activity
from android.permissions import (
    Permission,
    check_permission,
    request_permission,
)
from jnius import autoclass
from kivy.logger import Logger

from able.android.jni import PythonBluetooth
from able.dispatcher import BluetoothDispatcherBase


Activity = autoclass('android.app.Activity')
BLE = autoclass('org.able.BLE')

BluetoothGattDescriptor = autoclass(
    'android.bluetooth.BluetoothGattDescriptor')
ENABLE_NOTIFICATION_VALUE = BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE
DISABLE_NOTIFICATION_VALUE = BluetoothGattDescriptor.DISABLE_NOTIFICATION_VALUE


class BluetoothDispatcher(BluetoothDispatcherBase):

    def _set_ble_interface(self):
        self._events_interface = PythonBluetooth(self)
        self._ble = BLE(self._events_interface)
        activity.bind(on_activity_result=self.on_activity_result)

    def _check_runtime_permissions(self):
        # Either ACCESS_COARSE_LOCATION or ACCESS_FINE_LOCATION permission
        # is needed to obtain BLE scan results
        return check_permission(Permission.ACCESS_COARSE_LOCATION) or \
            check_permission(Permission.ACCESS_FINE_LOCATION)

    def _request_runtime_permissions(self):
        request_permission(Permission.ACCESS_COARSE_LOCATION,
                           self.on_runtime_permissions)

    def enable_notifications(self, characteristic, enable=True):
        if not self.gatt.setCharacteristicNotification(characteristic, enable):
            return False
        descriptor_value = (ENABLE_NOTIFICATION_VALUE if enable
                            else DISABLE_NOTIFICATION_VALUE)
        for descriptor in characteristic.getDescriptors().toArray():
            self.write_descriptor(descriptor, descriptor_value)
        return True

    def on_runtime_permissions(self, permissions, grant_results):
        if permissions and all(grant_results):
            self.start_scan()
        else:
            Logger.error(
                'Permissions necessary to obtain scan results are not granted'
            )
            self.dispatch('on_scan_started', False)

    def on_activity_result(self, requestCode, resultCode, intent):
        if requestCode == self.enable_ble_code:
            self.on_bluetooth_enabled(resultCode == Activity.RESULT_OK)

    def on_bluetooth_enabled(self, enabled):
        if enabled:
            self.start_scan()
        else:
            self.dispatch('on_scan_started', False)
