Usage Examples
==============

Alert
-----

.. literalinclude:: ./examples/alert.py
   :language: python


Change MTU
----------
.. literalinclude:: ./examples/mtu.py
   :language: python


Advertising
-----------

Advertise with data and additional (scannable) data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: python

  from able import BluetoothDispatcher
  from able.advertising import (
      Advertiser,
      AdvertiseData,
      ManufacturerData,
      Interval,
      ServiceUUID,
      ServiceData,
      TXPower,
  )

  advertiser = Advertiser(
      ble=BluetoothDispatcher(),
      data=AdvertiseData(ServiceUUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")),
      scan_data=AdvertiseData(ManufacturerData(id=0xAABB, data=b"some data")),
      interval=Interval.MEDIUM,
      tx_power=TXPower.MEDIUM,
  )

  advertiser.start()


Set and advertise device name
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

  from able import BluetoothDispatcher
  from able.advertising import Advertiser, AdvertiseData

  ble = BluetoothDispatcher()
  ble.name = "New test device name"

  # There must be a wait and check, it takes time for new name to take effect
  print(f"New device name is set: {ble.name}")

  Advertiser(
      ble=ble,
      data=AdvertiseData(DeviceName())
  )


Battery service data
^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ./examples/advertising_battery.py
   :language: python


Use iBeacon advertising format
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

  import uuid
  from able import BluetoothDispatcher
  from able.advertising import Advertiser, AdvertiseData, ManufacturerData


  data = AdvertiseData(
      ManufacturerData(
          0x4C,  # Apple Manufacturer ID
          bytes([
              0x2, # SubType: Custom Manufacturer Data
              0x15 # Subtype lenth
          ]) +
          uuid.uuid4().bytes +  # UUID of beacon
          bytes([
              0, 15,  # Major value
              0, 1,  # Minor value
              10  # RSSI, dBm at 1m
          ]))
  )

  Advertiser(BluetoothDispatcher(), data).start()


Android Services
----------------

BLE devices scanning service
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**main.py**

.. literalinclude:: ./examples/service_scan_main.py
   :language: python

**service.py**

.. literalinclude:: ./examples/service_scan_service.py
   :language: python

Full example code: `service_scan <https://github.com/b3b/able/blob/master/examples/service_scan/>`_


Advertising service
^^^^^^^^^^^^^^^^^^^

**main.py**

.. literalinclude:: ./examples/service_advertise_main.py
   :language: python

**service.py**

.. literalinclude:: ./examples/service_advertise_service.py
   :language: python

Full example code: `service_advertice <https://github.com/b3b/able/blob/master/examples/service_advertise/>`_
