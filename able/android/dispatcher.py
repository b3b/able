from functools import partial, wraps
from typing import Optional

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
from able.scan_settings import ScanSettingsBuilder

ArrayList = autoclass('java.util.ArrayList')

Activity = autoclass('android.app.Activity')
BLE = autoclass('org.able.BLE')

BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
BluetoothGattDescriptor = autoclass('android.bluetooth.BluetoothGattDescriptor')

ENABLE_NOTIFICATION_VALUE = BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE
ENABLE_INDICATION_VALUE = BluetoothGattDescriptor.ENABLE_INDICATION_VALUE
DISABLE_NOTIFICATION_VALUE = BluetoothGattDescriptor.DISABLE_NOTIFICATION_VALUE


def require_bluetooth_enabled(method):

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._run_on_bluetooth_enabled = partial(method, self, *args, **kwargs)
        if self.adapter:
            self._run_on_bluetooth_enabled()
            self._run_on_bluetooth_enabled = None
        else:
            Logger.debug("BLE adapter is not ready")

    return wrapper


def require_runtime_permissions(method):

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._run_on_runtime_permissions = partial(method, self, *args, **kwargs)
        if self._is_service_context or self._check_runtime_permissions():
            self._run_on_runtime_permissions()
            self._run_on_runtime_permissions = None
        else:
            Logger.debug("Request runtime permissions")
            self._request_runtime_permissions()

    return wrapper


class BluetoothDispatcher(BluetoothDispatcherBase):

    @property
    def adapter(self) -> Optional['android.bluetooth.BluetoothAdapter']:
        return self._ble and self._ble.getAdapter(self.enable_ble_code)

    @property
    def bonded_devices(self):
        ble_types = (BluetoothDevice.DEVICE_TYPE_LE, BluetoothDevice.DEVICE_TYPE_DUAL)
        return [
            dev for dev in self._ble.mBluetoothAdapter.getBondedDevices().toArray()
            if dev.getType() in ble_types
        ]

    @property
    def _is_service_context(self):
        return not activity._activity

    def _set_ble_interface(self):
        self._events_interface = PythonBluetooth(self)
        self._ble = BLE(self._events_interface)
        if not self._is_service_context:
            activity.bind(on_activity_result=self.on_activity_result)

    def _check_runtime_permissions(self):
        # ACCESS_FINE_LOCATION permission is needed to obtain BLE scan results
        return check_permission(Permission.ACCESS_FINE_LOCATION)

    def _request_runtime_permissions(self):
        request_permission(Permission.ACCESS_FINE_LOCATION,
                           self.on_runtime_permissions)

    @require_bluetooth_enabled
    @require_runtime_permissions
    def start_scan(self, filters=None, settings=None):
        filters_array = ArrayList()
        for f in filters or []:
            filters_array.add(f.build())
        if not settings:
            settings = ScanSettingsBuilder()
        try:
            settings = settings.build()
        except AttributeError:
            pass
        self._ble.startScan(self.enable_ble_code, filters_array, settings)

    def stop_scan(self):
        self._ble.stopScan()

    @require_bluetooth_enabled
    def connect_by_device_address(self, address: str):
        address = address.upper()
        if not BluetoothAdapter.checkBluetoothAddress(address):
            raise ValueError(f"{address} is not a valid Bluetooth address")
        adapter = self.adapter
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

    @require_bluetooth_enabled
    def _start_advertising(self, advertiser):
        advertiser._start()

    @require_bluetooth_enabled
    def _set_name(self, value):
        self.adapter.setName(value)

    def on_activity_result(self, requestCode, resultCode, intent):
        if requestCode == self.enable_ble_code:
            self.on_bluetooth_enabled(resultCode == Activity.RESULT_OK)

    def on_bluetooth_enabled(self, enabled):
        callback = self._run_on_bluetooth_enabled
        self._run_on_bluetooth_enabled = None
        if enabled:
            if callback:
                callback()
        elif callback:
            if callback.func == self.start_scan:
                self.dispatch('on_scan_started', False)

    def on_runtime_permissions(self, permissions, grant_results):
        callback = self._run_on_runtime_permissions
        self._run_on_runtime_permissions = None
        if permissions and all(grant_results):
            if callback:
                callback()
        else:
            Logger.error(
                'Permissions necessary to obtain scan results are not granted'
            )
            if callback.func == self.start_scan:
                self.dispatch('on_scan_started', False)
