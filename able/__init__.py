from enum import IntEnum

from able.structures import Advertisement, Services
from able.version import __version__  # noqa
from kivy.utils import platform

__all__ = ('Advertisement',
           'BluetoothDispatcher',
           'Services',)

# constants
GATT_SUCCESS = 0  #: GATT operation completed successfully
STATE_CONNECTED = 2  #: The profile is in connected state
STATE_DISCONNECTED = 0  #: The profile is in disconnected state


class WriteType(IntEnum):
    """GATT characteristic write types constants.
    """
    DEFAULT = 2  #: Write characteristic, requesting acknoledgement by the remote device
    NO_RESPONSE = 1  #: Write characteristic without requiring a response by the remote device
    SIGNED = 4  #: Write characteristic including authentication signature


if platform == 'android':
    from able.android.dispatcher import BluetoothDispatcher
else:
    from able.dispatcher import BluetoothDispatcherBase

    class BluetoothDispatcher(BluetoothDispatcherBase):
        """Bluetooth Low Energy interface

        :param queue_timeout: BLE operations queue timeout
        :param enable_ble_code: request code to identify activity that alows
               user to turn on :func:`Bluetooth <start_scan>`
        """
