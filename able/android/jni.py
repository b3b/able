from able import GATT_SUCCESS
from able.structures import Advertisement, Services
from jnius import PythonJavaClass, java_method
from kivy.logger import Logger


class PythonBluetooth(PythonJavaClass):
    __javainterfaces__ = ['org.able.PythonBluetooth']
    __javacontext__ = 'app'

    def __init__(self, dispatcher):
        super(PythonBluetooth, self).__init__()
        self.dispatcher = dispatcher

    @java_method('(Ljava/lang/String;)V')
    def on_error(self, msg):
        Logger.debug("on_error")
        self.dispatcher.dispatch('on_error', msg)

    @java_method('(Landroid/bluetooth/BluetoothDevice;I[B)V')
    def on_device(self, device, rssi, record):
        self.dispatcher.dispatch('on_device', device, rssi,
                                 Advertisement(record))

    @java_method('(Z)V')
    def on_scan_started(self, success):
        Logger.debug("on_scan_started")
        self.dispatcher.dispatch('on_scan_started', success)

    @java_method('()V')
    def on_scan_completed(self):
        Logger.debug("on_scan_completed")
        self.dispatcher.dispatch('on_scan_completed')

    @java_method('(II)V')
    def on_connection_state_change(self, status, state):
        Logger.debug("on_connection_state_change status={} state: {}".format(
            status, state))
        self.dispatcher.dispatch('on_connection_state_change', status, state)

    @java_method('(ILjava/util/List;)V')
    def on_services(self, status, services):
        services_dict = Services()
        if status == GATT_SUCCESS:
            for service in services.toArray():
                service_uuid = service.getUuid().toString()
                Logger.debug("Service discovered: {}".format(service_uuid))
                services_dict[service_uuid] = {}
                for c in service.getCharacteristics().toArray():
                    characteristic_uuid = c.getUuid().toString()
                    Logger.debug("Characteristic discovered: {}".format(
                        characteristic_uuid))
                    services_dict[service_uuid][characteristic_uuid] = c
        self.dispatcher.dispatch('on_services', status, services_dict)

    @java_method('(Landroid/bluetooth/BluetoothGattCharacteristic;)V')
    def on_characteristic_changed(self, characteristic):
        # uuid = characteristic.getUuid().toString()
        self.dispatcher.dispatch('on_characteristic_changed', characteristic)

    @java_method('(Landroid/bluetooth/BluetoothGattCharacteristic;I)V')
    def on_characteristic_read(self, characteristic, status):
        self.dispatcher.dispatch('on_gatt_release')
        # uuid = characteristic.getUuid().toString()
        self.dispatcher.dispatch('on_characteristic_read',
                                 characteristic,
                                 status)

    @java_method('(Landroid/bluetooth/BluetoothGattCharacteristic;I)V')
    def on_characteristic_write(self, characteristic, status):
        self.dispatcher.dispatch('on_gatt_release')
        # uuid = characteristic.getUuid().toString()
        self.dispatcher.dispatch('on_characteristic_write',
                                 characteristic,
                                 status)

    @java_method('(Landroid/bluetooth/BluetoothGattDescriptor;I)V')
    def on_descriptor_read(self, descriptor, status):
        self.dispatcher.dispatch('on_gatt_release')
        # characteristic = descriptor.getCharacteristic()
        # uuid = characteristic.getUuid().toString()
        self.dispatcher.dispatch('on_descriptor_read', descriptor, status)

    @java_method('(Landroid/bluetooth/BluetoothGattDescriptor;I)V')
    def on_descriptor_write(self, descriptor, status):
        self.dispatcher.dispatch('on_gatt_release')
        # characteristic = descriptor.getCharacteristic()
        # uuid = characteristic.getUuid().toString()
        self.dispatcher.dispatch('on_descriptor_write', descriptor, status)

    @java_method('(II)V')
    def on_rssi_updated(self, rssi, status):
        self.dispatcher.dispatch('on_gatt_release')
        self.dispatcher.dispatch('on_rssi_updated', rssi, status)

    @java_method('(II)V')
    def on_mtu_changed(self, mtu, status):
        self.dispatcher.dispatch('on_gatt_release')
        self.dispatcher.dispatch('on_mtu_changed', mtu, status)
