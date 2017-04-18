.. automodule:: able

API
---

Classes
~~~~~~~

.. autoclass:: BluetoothDispatcher
   :members: gatt,
             set_queue_timeout,
             start_scan,
             stop_scan,
             connect_gatt,
             close_gatt,
             discover_services,
             enable_notifications,
             write_descriptor,
             write_characteristic,
             read_characteristic,
             on_gatt_release,
             on_scan_started,
             on_scan_completed,
             on_device,
             on_connection_state_change,
             on_services,
             on_characteristic_changed,
             on_characteristic_read,
             on_characteristic_write,
             on_descriptor_read,
             on_descriptor_write,

.. autoclass:: Advertisement

   .. autoclass:: able::Advertisement.ad_types

.. autoclass:: Services
   :members:

Constants
~~~~~~~~~

.. autodata:: GATT_SUCCESS
.. autodata:: STATE_CONNECTED
.. autodata:: STATE_DISCONNECTED

