====================
aqtinstall changeLog
====================

All notable changes to this project will be documented in this file.

***************
Current changes
***************

`Unreleased`_
=============

Added
-----

Changed
-------

Fixed
-----

Deprecated
----------

Removed
-------

Security
--------

`v1.0.0b2`_ (28, Jan. 2021)
===========================

Added
-----

* Patch pkgconfig configurations(#199)
* Patch libQt5Core and libQt6Core for linux(#201)

Fixed
-----

* Catch exception on qmake -query execution(#201)


`v1.0.0b1`_ (27, Jan. 2021)
===========================

Fixed
-----

* Fix Qt6/Android installation handling.(#193, #200)


`v0.11.1`_ (21, Jan. 2021)
==========================

Added
-----

* Add --timeout option to specify connection timeout (default 5.0 sec) (#197)


`v0.11.0`_ (21, Jan. 2021)
==========================

Added
-----

* Automatically fallback to mirror site when main https://download.qt.io down.(#194, #196)


`v0.10.1`_ (11, Dec. 2020)
==========================

Added
-----

* Add LTS versions as known one.(#188)

Changed
-------

* Tool: Version comparison by startswith.
  When specified 4.0 but download server hold 4.0.1, it catch 4.0.1.(related #187)
* README: explicitly show python version requirements.



`v0.10.0`_ (25, Nov. 2020)
==========================

Added
-----

* Add v5.12.2, v6.0.0 as known versions.(#176, #177)
* Support --archives option on src installation.

Changed
-------

* Use multiprocessing.Pool instead of concurrent.futures(#178)
* Refactoring whole modules. (#179)
* Split old changelogs to CHNAGELOG_prerelease.rst
* Drop an upper limitation (<0.11) for py7zr.(#183)

Fixed
-----

* When we used "-m all" to download doc or examples, Qt sources are also downloaded(@Gamso)(#182)


v0.9.8 (4, Nov. 2020)
=====================

Added
-----

* Added new combinations for tools_ifw

Fixed
-----

* When we start an installation, all packages are downloaded whatever the specified platform.(#159)


.. _Unreleased: https://github.com/miurahr/aqtinstall/compare/v1.0.0b2...HEAD
.. _v1.0.0b2: https://github.com/miurahr/aqtinstall/compare/v1.0.0b1...v1.0.0b2
.. _v1.0.0b1: https://github.com/miurahr/aqtinstall/compare/v0.11.1...v1.0.0b1
.. _v0.11.1: https://github.com/miurahr/aqtinstall/compare/v0.11.0...v0.11.1
.. _v0.11.0: https://github.com/miurahr/aqtinstall/compare/v0.10.1...v0.11.0
.. _v0.10.1: https://github.com/miurahr/aqtinstall/compare/v0.10.0...v0.10.1
.. _v0.10.0: https://github.com/miurahr/aqtinstall/compare/v0.9.8...v0.10.0
