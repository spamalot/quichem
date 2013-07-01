.. _SourceForge page: http://sourceforge.net/projects/quichem

===========
``quichem``
===========

``quichem`` (pronounced *[kwi-kehm]*) is a utility written in pure Python
allowing for fast input and parsing of chemical formulae and equations.
Entering data does not require any modifier keys or keystrokes to be pressed.

``quichem`` is distributed under the GNU LGPL v3.0.

Looking for the Windows application? Download it from ``quichem``'s
`SourceForge page`_.


Examples
--------

=========================  ===============================================================================
Input                      reStructuredText Output
=========================  ===============================================================================
``o2aq``                   O\ :sub:`2(aq)`
``li=``                    Li\ :sup:`+`
``'nh4'2s``                (NH\ :sub:`4`\ )\ :sub:`2`\ S
``b'nh4'3'p.o4'2``         B(NH\ :sub:`4`\ )\ :sub:`3`\ (PO\ :sub:`4`\ )\ :sub:`2`
``2cl-aq=2ag=aq-2agcl;s``  2Cl\ :sup:`-`\ :sub:`(aq)`\  + 2Ag\ :sup:`+`\ :sub:`(aq)`\  → 2AgCl\ :sub:`(s)`
=========================  ===============================================================================

For more examples and a detailed description, see `SYNTAX.rst <SYNTAX.rst>`_.


Current Output Format Support
-----------------------------

- plain text
- reStructuredText
- HTML
- LaTeX


Installation
-----------

Dependencies
++++++++++++

- Python 2.7 or Python >= 3.0
- ``pyparsing``
- ``PySide`` (optional; for GUI front-end)
- ``cx_Freeze`` (optional; for building ``PySide`` GUI front-end)
- ``wxPython`` (optional; for GUI front-end)


Binaries
++++++++
Windows binaries for the ``PySide`` ``quichem`` front-end can be downloaded
from  ``quichem``'s `SourceForge page`_. The binaries are created with
``cx_Freeze``, so Python does not have to be installed for them to run.

There are currently no pre-built binaries for the ``wxPython`` front-end, nor a
``setup.py`` file for installing ``quichem`` as a Python package.


Running from Source
+++++++++++++++++++

Locate to the ``quichem`` directory and run::

    $ python -m quichem.gui.pyside

for the ``PySide`` front-end, or::

    $ python -m quichem.gui.wxpython

for the ``wxPython`` front-end.

This will create a small ``Qt`` or ``wxWidgets`` window demonstrating how the
various output formats render your input.


Building from Source
++++++++++++++++++++

PySide Front-end
~~~~~~~~~~~~~~~~

Locate to the ``build/cx_Freeze-pyside/`` subdirectory of the ``quichem``
directory. Run::

    $ python setup.py build

The Windows binary will be located in ``build/``.


Screenshots
-----------

.. figure:: http://c.fsdn.com/con/app/proj/quichem/screenshots/screenshot.png

    ``quichem-pyside`` *running on Windows 7.*


Roadmap
-------

Below are some features which may be implemented in ``quichem`` in the future.

- full wxPython clipboard support
- Windows binaries for wxPython front-end
- ``setup.py`` files for installing ``quichem`` as a Python package
- isotopes (through indication of atomic mass)
- a PyGTK front-end
- a Win32 GUI front-end
