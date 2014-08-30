.. _SourceForge page: http://sourceforge.net/projects/quichem
.. _user guide: https://cdn.rawgit.com/spamalot/quichem/263b840dbba5892106650a6fb93efed1749a900c/userguide/USERGUIDE.html

===========
``quichem``
===========

``quichem`` (pronounced *[kwi-kehm]*) is a utility written in pure Python
allowing for fast input and parsing of chemical formulae and equations.
Entering data does not require any modifier keys or keystrokes to be pressed.
``quichem`` also now has a LaTeX package which will dynamically take
``quichem`` input in the LaTeX source and typeset it in the final document.

``quichem`` is distributed under the GNU LGPL v3.0. The ``quichem`` LaTeX
package (comprised of ``quichem.dtx`` and ``quichem.ins``) is distributed
under the LPPL v1.3 or newer.

Quick Links
-----------
+ *Looking for the Windows application?* Download it from ``quichem``'s
  `SourceForge page`_.
+ *Don't know where to get started?* Have a look at the
  `user guide`_.
+ *Want to use* ``quichem`` *as a LaTeX package?* Have a look at its
  `README <latex/README.txt>`_ and `documentation <latex/quichem.pdf>`_.


Examples
--------

=========================  ======================================================================================
Input                      reStructuredText Output
=========================  ======================================================================================
``o2aq``                   O\ :sub:`2(aq)`
``li=``                    Li\ :sup:`+`
``'nh4'2s``                (NH\ :sub:`4`\ )\ :sub:`2`\ S
``b'nh4'3'p.o4'2``         B(NH\ :sub:`4`\ )\ :sub:`3`\ (PO\ :sub:`4`\ )\ :sub:`2`
``2cl-aq=2ag=aq-2agcl;s``  2 Cl\ :sup:`⁻`\ :sub:`(aq)`\  + 2 Ag\ :sup:`+`\ :sub:`(aq)`\  ⟶ 2 AgCl\ :sub:`(s)`
=========================  ======================================================================================

For more examples and a detailed description, see `SYNTAX.rst <SYNTAX.rst>`_.


Current Output Format Support
-----------------------------

- plain text
- plain text (ASCII only) **(NEW)**
- reStructuredText
- HTML
- LaTeX
- LaTeX for the ``mchem`` package
- Microsoft Word (with ``quichem-pyside``, the Qt GUI front-end) **(NEW)**
- PNG image (with ``quichem-pyside``, the Qt GUI front-end) **(NEW)**


Installation
------------

Dependencies
++++++++++++

- Python >= 3.2
- ``modgrammar`` >= 0.10
- ``PySide`` (optional; for Qt GUI front-end)
- ``cx_Freeze`` (optional; for building ``PySide`` GUI front-end)
- ``wxPython`` *[Phoenix only]* (optional; for wxWidgets GUI front-end)
- ``MathJax`` (optional; if not using ``MathJax`` included with ``quichem`` in
  ``web.tar``/``quichem/gui/web.py``)

+----------------------------------------------------------------------------+
| **Python 2.7 Support**                                                     |
|                                                                            |
| Efforts have been taken to retain compatibility with Python 2.7.           |
| However, ``modgrammar-py2`` is at version 0.9.2, and therefore ``quichem`` |
| will only regain support for Python 2.7 once ``modgrammar-py2`` has been   |
| updated to match the ``modgrammar`` 0.10 API.                              |
+----------------------------------------------------------------------------+

+----------------------------------------------------------------------------+
| **Customized MathJax Inclusion**                                           |
|                                                                            |
| ``quichem`` uses ``MathJax`` to render chemical equations and formulae.    |
| The included ``MathJax`` has had many of its resources removed to          |
| reduce its size. It is stored in ``web.tar``. The PySide GUI frontend uses |
| Qt's resource system to store ``MathJax`` inside a Python file             |
| (``quichem/gui/web.py``). The included ``MathJax`` can be replaced with    |
| another version if desired. The ``MathJax`` files necessary for            |
| ``quichem`` to operate are listed in the Qt resource file ``web.qrc``.     |
+----------------------------------------------------------------------------+

Binaries
++++++++
Windows binaries for the ``PySide`` ``quichem`` front-end can be downloaded
from  ``quichem``'s `SourceForge page`_. The binaries are created with
``cx_Freeze``, so Python does not have to be installed for them to run.

There are currently no pre-built binaries for the ``wxPython`` front-end.


Installing as a Python Package
++++++++++++++++++++++++++++++

To install ``quichem`` as a Python package, locate to the ``quichem`` directory
and run::

	$ python setup.py install

``quichem`` should now be importable.

+------------------------------------------------------------------------+
| **Package Size**                                                       |
|                                                                        |
| If GUI front-ends are not needed, the package size can be              |
| reduced by removing the ``gui`` directory from the ``quichem/``        |
| directory. ``web.tar``, located in the root of the package, is only    |
| needed for the wxPython GUI and can be removed after it is extracted   |
| or if only the PySide GUI is to be used.                               |
+------------------------------------------------------------------------+


Running GUI from Source
+++++++++++++++++++++++

Locate to the ``quichem`` directory and run::

    $ python -m quichem.gui.pyside

for the ``PySide`` front-end, or::

    $ python -m quichem.gui.wxpython

for the ``wxPython`` front-end [*]_.

This will create a small ``Qt`` or ``wxWidgets`` window demonstrating how the
various output formats render your input.

.. [*] Because wxWidgets does not have a resource subsystem like Qt, external
   web files are needed for the wxPython front-end to operate. Extract
   ``web.tar`` located in the ``quichem`` directory into a folder named
   ``web/`` in the working directory before using the wxPython front-end.


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

.. figure:: http://c.fsdn.com/con/app/proj/quichem/screenshots/screenshot2.png

    ``quichem-pyside`` *running on Windows 7.*


Roadmap
-------

Below are some features which may be implemented in ``quichem`` in the future.

- full wxPython clipboard support
- Windows binaries for wxPython front-end
- multiple ``setup.py`` files for installing the ``quichem`` front-ends
  as separate packages (using namespace packages)
- isotopes (through indication of atomic mass)
- plain text in equations, such as "energy"
- subatomic particles
- OpenOffice/LibreOffice math output format
- different notation standards (e.g. *IUPAC*, *ACS*, etc.)
- automatic parsing and compiling of ``quichem`` markup in supported text
  documents (HTML, reStructuredText)
- a PyGTK front-end & Win32 GUI front-end
