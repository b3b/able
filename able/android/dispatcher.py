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

BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
BluetoothGattDescriptor = autoclass('android.bluetooth.BluetoothGattDescriptor')

ENABLE_NOTIFICATION_VALUE = BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE
ENABLE_INDICATION_VALUE = BluetoothGattDescriptor.ENABLE_INDICATION_VALUE
DISABLE_NOTIFICATION_VALUE = BluetoothGattDescriptor.DISABLE_NOTIFICATION_VALUE


class BluetoothDispatcher(BluetoothDispatcherBase):

    @property
    def bonded_devices(self):
        ble_types = (BluetoothDevice.DEVICE_TYPE_LE, BluetoothDevice.DEVICE_TYPE_DUAL)
        return [
            dev for dev in self._ble.mBluetoothAdapter.getBondedDevices().toArray()
            if dev.getType() in ble_types
        ]


    def _set_ble_interface(self):
        self._events_interface = PythonBluetooth(self)
        self._ble = BLE(self._events_interface)
        activity.bind(on_activity_result=self.on_activity_result)

    def _check_runtime_permissions(self):
        # ACCESS_FINE_LOCATION permission is needed to obtain BLE scan results
        return check_permission(Permission.ACCESS_FINE_LOCATION)

    def _request_runtime_permissions(self):
        request_permission(Permission.ACCESS_FINE_LOCATION,
                           self.on_runtime_permissions)

    def connect_by_device_address(self, address: str):
        address = address.upper()
        if not BluetoothAdapter.checkBluetoothAddress(address):
            raise ValueError(f"{address} is not a valid Bluetooth address")
        # remember address to retry connection request when adapter becomes ready
        self._remote_device_address = address
        adapter = self._ble.getAdapter(self.enable_ble_code)
        if adapter:
            self.connect_gatt(adapter.getRemoteDevice(address))

    def enable_notifications(self, characteristic, enable=True, indication=False):
        if not self.gatt.setCharacteristicNotification(characteristic, enable):
            return False

        if not enable:
            # DISABLE_NOTIFICAITON_VALUE is for disabling
            # both notifications and indications
            descriptor_value = DISABLE_NOTIFICATION_VALUE
        elif indication:
            descriptor_value = ENABLE_INDICATION_VALUE
        else:
            descriptor_value = ENABLE_NOTIFICATION_VALUE

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
            if self._remote_device_address:  # connection by MAC address was requested, without scanning
                self.connect_by_device_address(self._remote_device_address)
            else:
                self.start_scan()
        elif not self._remote_device_address:
            self.dispatch('on_scan_started', False)
