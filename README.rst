Android Bluetooth Low Energy
============================

.. start-badges
.. image:: https://img.shields.io/pypi/v/able_recipe.svg
    :target: https://pypi.python.org/pypi/able_recipe
    :alt: Latest version on PyPi
.. end-badges

`Python <https://github.com/kivy/python-for-android>`_ interface to Android Bluetooth Low Energy API.

Generated documentation: http://able.readthedocs.org


Build
-----

The following instructions are for building app with `buildozer <https://github.com/kivy/buildozer/>`_ tool.

Download the `able` recipes directory: https://github.com/b3b/able/tree/master/recipes .

Path to recipes directory should be set in buildozer.spec::

   p4a.local_recipes = /path/to/downloaded/recipes


`able` recipe should be added to buildozer.spec requirements::

   requirements = python3,kivy,android,able


Bluetooth permissions should be requested in buildozer.spec::

    android.permissions = BLUETOOTH, BLUETOOTH_ADMIN, ACCESS_COARSE_LOCATION


App configuration example: `buildozer.spec <https://github.com/b3b/able/tree/master/examples/alert/buildozer.spec>`_
