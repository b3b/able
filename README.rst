Android Bluetooth Low Energy
============================

.. start-badges
.. image:: https://img.shields.io/pypi/v/able_recipe.svg
    :target: https://pypi.python.org/pypi/able_recipe
    :alt: Latest version on PyPi
.. end-badges

`Python <https://github.com/kivy/python-for-android>`_ interface to Android Bluetooth Low Energy API.

:Code repository: https://github.com/b3b/able
:Documentation: https://herethere.me/able
:Changelog: https://github.com/b3b/able/blob/master/CHANGELOG.rst

Quick start development environment
-----------------------------------

*able* is included in `PythonHere <https://herethere.me/pythonhere>`_ app, together with the `Jupyter Notebook <https://jupyter.org/>`_ it could be used as a development environment.

Usage example: https://herethere.me/pythonhere/examples/ble.html


Build
-----

The following instructions are for building app with `buildozer <https://github.com/kivy/buildozer/>`_ tool.

*able_recipe* recipe should be added to buildozer.spec requirements::

   requirements = python3,kivy,android,able_recipe


Bluetooth permissions should be requested in buildozer.spec::

    android.permissions = BLUETOOTH, BLUETOOTH_ADMIN, BLUETOOTH_SCAN, BLUETOOTH_CONNECT, BLUETOOTH_ADVERTISE, ACCESS_FINE_LOCATION


App configuration example: `buildozer.spec <https://github.com/b3b/able/tree/master/examples/alert/buildozer.spec>`_


Build with a local version
--------------------------

To build app with a local (modified) version of *able*,

path to *able* recipes directory should be set in buildozer.spec::

    p4a.local_recipes = /path/to/cloned/repo/recipes


Contributors
------------

Thanks to everyone who helped improve *able*:

.. csv-table::

    `331319341 <https://github.com/331319341>`_
    `andmart <https://github.com/andmart>`_
    `andreamerello <https://github.com/andreamerello>`_
    `datmaniac95 <https://github.com/datmaniac95>`_
    `dgatf <https://github.com/dgatf>`_
    `dwmoffatt <https://github.com/dwmoffatt>`_
    `Enkumicahel <https://github.com/Enkumicahel>`_
    `hailesir <https://github.com/hailesir>`_
    `HelaFaye <https://github.com/HelaFaye>`_
    `ilw <https://github.com/ilw>`_
    `jacklinquan <https://github.com/jacklinquan>`_
    `juasiepo <https://github.com/juasiepo>`_
    `MininDMhvh <https://github.com/MininDMhvh>`_
    `PapoKarlo <https://github.com/PapoKarlo>`_
    `quasarsuport-del <https://github.com/quasarsuport-del>`_
    `RoberWare <https://github.com/RoberWare>`_
    `Rowataro <https://github.com/Rowataro>`_
    `robgar2001 <https://github.com/robgar2001>`_
    `sodef <https://github.com/sodef>`_
    `sooko <https://github.com/sooko>`_
    `ujur007 <https://github.com/ujur007>`_
    `woutersj <https://github.com/woutersj>`_
