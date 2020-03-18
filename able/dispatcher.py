from kivy.event import EventDispatcher
from kivy.logger import Logger

from able.queue import BLEQueue, ble_task, ble_task_done
from able.utils import force_convertible_to_java_array


class BLEError(object):
    """raise Exception on attribute access
    """

    def __init__(self, msg):
        self.msg = msg

    def __getattr__(self, name):
        raise Exception(self.msg)


class BluetoothDispatcherBase(EventDispatcher):
    __events__ = (
        'on_device', 'on_scan_started', 'on_scan_completed', 'on_services',
        'on_connection_state_change', 'on_characteristic_changed',
        'on_characteristic_read', 'on_characteristic_write',
        'on_descriptor_read', 'on_descriptor_write',
        'on_gatt_release', 'on_error',
    )
    queue_class = BLEQueue

    def __init__(self, queue_timeout=0.5, enable_ble_code=0xab1e):
        super(BluetoothDispatcherBase, self).__init__()
        self.queue_timeout = queue_timeout
        self._set_ble_interface()
        self._set_queue()
        self.enable_ble_code = enable_ble_code

    def _set_ble_interface(self):
        self._ble = BLEError('BLE is not implemented for platform')

    def _set_queue(self):
        self.queue = self.queue_class(timeout=self.queue_timeout)

    def _check_runtime_permissions(self):
        return True

    def _request_runtime_permissions(self):
        pass

    @property
    def gatt(self):
        """GATT profile of the connected device

        :type: BluetoothGatt Java object
        """
        return self._ble.getGatt()

    def set_queue_timeout(self, timeout):
        """Change the BLE operations queue timeout
        """
        self.queue_timeout = timeout
        self.queue.set_timeout(timeout)

    def start_scan(self):
        """Start a scan for devices.
        Ask for runtime permission to access location.
        Start a system activity that allows the user to turn on Bluetooth,
        if Bluetooth is not enabled.
        The status of the scan start are reported with
        :func:`scan_started <on_scan_started>` event.
        """
        if self._check_runtime_permissions():
            self._ble.startScan(self.enable_ble_code)
        else:
            self._request_runtime_permissions()

    def stop_scan(self):
        """Stop the ongoing scan for devices.
        """
        self._ble.stopScan()

    def connect_gatt(self, device):
        """Connect to GATT Server hosted by device
        """
        self._ble.connectGatt(device)

    def close_gatt(self):
        """Close current GATT client
        """
        self._ble.closeGatt()

    def discover_services(self):
        """Discovers services offered by a remote device.
        The status of the discovery reported with
        :func:`services <on_services>` event.

        :return: true, if the remote services discovery has been started
        """
        return self.gatt.discoverServices()

    def enable_notifications(self, characteristic, enable=True, indication=False):
        """Enable/disable notifications or indications for a given characteristic

        :param characteristic: BluetoothGattCharacteristic Java object
        :param enable: enable notifications if True, else disable notifications
        :param indication: handle indications instead of notifications
        :return: True, if the operation was initiated successfully
        """
        return True

    @ble_task
    def write_descriptor(self, descriptor, value):
        """Set and write the value of a given descriptor to the associated
        remote device

        :param descriptor: BluetoothGattDescriptor Java object
        :param value: value to write
        """
        if not descriptor.setValue(force_convertible_to_java_array(value)):
            Logger.error("Error on set descriptor value")
            return
        if not self.gatt.writeDescriptor(descriptor):
            Logger.error("Error on descriptor write")

    @ble_task
    def write_characteristic(self, characteristic, value):
        """Write a given characteristic value to the associated remote device

        :param characteristic: BluetoothGattCharacteristic Java object
        :param value: value to write
        """
        self._ble.writeCharacteristic(characteristic,
                                      force_convertible_to_java_array(value))

    @ble_task
    def read_characteristic(self, characteristic):
        """Read a given characteristic from the associated remote device

        :param characteristic: BluetoothGattCharacteristic Java object
        """
        self._ble.readCharacteristic(characteristic)

    def on_error(self, msg):
        """Error handler

        :param msg: error message
        """
        self._ble = BLEError(msg)  # Exception for calls from another threads
        raise Exception(msg)

    @ble_task_done
    def on_gatt_release(self):
        """`gatt_release` event handler.
        Event is dispatched at every read/write completed operation
        """
        pass

    def on_scan_started(self, success):
        """`scan_started` event handler

        :param success: true, if scan was started successfully
        """
        pass

    def on_scan_completed(self):
        """`scan_completed` event handler
        """
        pass

    def on_device(self, device, rssi, advertisement):
        """`device` event handler.
        Event is dispatched when device is found during a scan.

        :param device: BluetoothDevice Java object
        :param rssi: the RSSI value for the remote device
        :param advertisement: :class:`Advertisement` data record
        """
        pass

    def on_connection_state_change(self, status, state):
        """`connection_state_change` event handler

        :param status: status of the operation,
                       `GATT_SUCCESS` if the operation succeeds
        :param state: STATE_CONNECTED or STATE_DISCONNECTED
        """
        pass

    def on_services(self, services, status):
        """`services` event handler

        :param services: :class:`Services` dict filled with discovered
                         characteristics
                         (BluetoothGattCharacteristic Java objects)
        :param status: status of the operation,
                       `GATT_SUCCESS` if the operation succeeds
        """
        pass

    def on_characteristic_changed(self, characteristic):
        """`characteristic_changed` event handler

        :param characteristic: BluetoothGattCharacteristic Java object
        """
        pass

    def on_characteristic_read(self, characteristic, status):
        """`characteristic_read` event handler

        :param characteristic: BluetoothGattCharacteristic Java object
        :param status: status of the operation,
                       `GATT_SUCCESS` if the operation succeeds
        """
        pass

    def on_characteristic_write(self, characteristic, status):
        """`characteristic_write` event handler

        :param characteristic: BluetoothGattCharacteristic Java object
        :param status: status of the operation,
                       `GATT_SUCCESS` if the operation succeeds
        """
        pass

    def on_descriptor_read(self, descriptor, status):
        """`descriptor_read` event handler

        :param descriptor: BluetoothGattDescriptor Java object
        :param status: status of the operation,
                       `GATT_SUCCESS` if the operation succeeds
        """
        pass

    def on_descriptor_write(self, descriptor, status):
        """`descriptor_write` event handler

        :param descriptor: BluetoothGattDescriptor Java object
        :param status: status of the operation,
                       `GATT_SUCCESS` if the operation succeeds
        """
        pass
