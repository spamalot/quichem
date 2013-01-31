===========
``quichem``
===========

``quichem`` is a Python utility allowing for fast input and parsing of
chemical formulae and equations. Entering data does not require any
modifier keys or keystrokes to be pressed.


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
- ``PySide`` (for GUI frontend)

At the moment, you will just have to download the source and try it out. I
will create a ``setup.py`` file and a ``py2exe`` compiled exe as soon as I
can.

To run``quichem`` from source, make sure you have the above dependencies.
Locate to the ``quichem`` folder and run::

    $ python -m quichem.gui.pyside

This will create a little ``Qt`` window demonstrating how the various output
formats render your input.


Screenshots
-----------

Coming soon.
