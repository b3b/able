from android import activity
from able.android.jni import PythonBluetooth
from able.dispatcher import BluetoothDispatcherBase
from jnius import autoclass


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

    def enable_notifications(self, characteristic, enable=True):
        if not self.gatt.setCharacteristicNotification(characteristic, enable):
            return False
        descriptor_value = (ENABLE_NOTIFICATION_VALUE if enable
                            else DISABLE_NOTIFICATION_VALUE)
        for descriptor in characteristic.getDescriptors().toArray():
            self.write_descriptor(descriptor, descriptor_value)
        return True

    def on_activity_result(self, requestCode, resultCode, intent):
        if requestCode == self.enable_ble_code:
            self.on_bluetooth_enabled(resultCode == Activity.RESULT_OK)

    def on_bluetooth_enabled(self, enabled):
        if enabled:
            self.start_scan()
        else:
            self.dispatch('on_scan_started', False)
