Android Bluetooth Low Energy
============================

`Python <https://github.com/kivy/python-for-android>`_ interface to Android Bluetooth Low Energy API.

Generated documentation: http://able.readthedocs.org


Build
-----

The following instructions are for building app with `buildozer <https://github.com/kivy/buildozer/>`_ tool (buildozer android_new).

Download the `able` recipes directory: https://github.com/b3b/able/tree/master/recipes .

Path to recipes directory should be set in buildozer.spec::

   p4a.local_recipes = /path/to/downloaded/recipes


`able` recipe should be added to buildozer.spec requirements::

   requirements = hostpython2,kivy,android,able


Bluetooth permissions should be requested in buildozer.spec::

    android.permissions = BLUETOOTH, BLUETOOTH_ADMIN, ACCESS_COARSE_LOCATION

