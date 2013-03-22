==============================
``quichem`` Syntax Description
==============================

The ``quichem`` parser handles:

    - `elements`_
    - `subscripts`_
    - `compounds`_
    - `charges`_
    - `states of matter`_
    - `coefficients`_
    - hydrates_
    - `chemical equations and fragments`_

The ``quichem`` parser does **not** handle:

    - isotopes
    - radioactive particles

General Notes
-------------
The only symbols that the parser needs to recognize are:

    + ``=`` : either a `positive charge`_ or sum_ of two elements_/compounds_
    + ``-`` : either a `negative charge`_ or an `arrow`_ in a `chemical equation`_
    + ``/`` : dot used in hydrates_
    + ``'`` : represents either an open or close parenthesis_
    + ``.``/``;`` : separators used in ambiguous cases
    + lower-case letters & numbers

This means that one does not have to press shift while typing text to be
processed by the parser.


Elements
--------
Elements are expected by the parser to be lower case. If only one element
is entered, its identity is unambiguous, so the parser can automatically
capitalize the first letter when necessary.

========  ======
Examples
----------------
Input     Output
========  ======
``o``     O
``pb``    Pb
``uuo``   Uuo
========  ======


.. _subscript:

Subscripts
----------
Subscripts can be added to elements by including the value of the subscript
after the element.

========  ============
Examples
----------------------
Input     Output
========  ============
``o2``    O\ :sub:`2`
``c60``   C\ :sub:`60`
========  ============


Compounds
---------
Compounds are made by putting elements together.

===========  ======================================
Examples
---------------------------------------------------
Input        Output
===========  ======================================
``h2o``      H\ :sub:`2`\ O
``c6h12o6``  C\ :sub:`6`\ H\ :sub:`12`\ O\ :sub:`6`
``lioh``     LiOH
===========  ======================================

Since element names are not capitalized, there are several ambiguous cases.
To clarify ambiguous cases, put a dot (``.``) at the *first* ambiguous
position in the compound.

Some common ambiguous cases to remember are PO and HS. A dot must be used to
separate the elements in these cases, or else Po and Hs are received as
output, respectively.

===========  ======
Examples
-------------------
Input        Output
===========  ======
``cmgali``   CmGaLi
``c.mgali``  CMgAlI
===========  ======

.. _parenthesis:

Sometimes, elements require parentheses. Parenthesis are inserted into
compounds by surrounding a segment of a compound with single-quotes (``'``).
Parentheses can be nested if necessary.

==================  =======================================================
Examples
---------------------------------------------------------------------------
Input               Output
==================  =======================================================
``ge'oh'4``         Ge(OH)\ :sub:`4`
``b'nh4'3'p.o4'2``  B(NH\ :sub:`4`\ )\ :sub:`3`\ (PO\ :sub:`4`\ )\ :sub:`2`
==================  =======================================================


.. _`positive charge`:
.. _`negative charge`:

Charges
-------
Charges can be added to elements or compounds by including the value and sign
of the charge after the element or compound. |plus_note|

========  ============
Examples
----------------------
Input     Output
========  ============
``h=``    H\ :sup:`+`
``br-``   Br\ :sup:`-`
========  ============

If the charge has a numeric value, a dot (``.``) must be used to distinguish
it from a subscript_. A dot can be placed before a subscript even if there
is no preceding subscript, in which case it will be ignored.

==========  =======================
Examples
-----------------------------------
Input       Output
==========  =======================
``o2=``     O\ :sub:`2`\ :sup:`+`
``o2.=``    O\ :sub:`2`\ :sup:`+`
``o.2=``    O\ :sup:`2+`
``so4.2=``  SO\ :sub:`4`\ :sup:`2+`
==========  =======================


States of Matter
----------------
States can be added to elements or compounds by including the abbreviation of
the state after the element or compound.

Valid states are:

    - ``aq`` : aqueous
    - ``g`` : gas
    - ``l`` : liquid
    - ``s`` : solid

===========  =================
Examples
------------------------------
Input        Output
===========  =================
``h2g``      H\ :sub:`2(g)`
``hp.o4aq``  HPO\ :sub:`4(aq)`
===========  =================

If the compound does not end with a charge or subscript, a semicolon (``;``)
must be placed before the state's abbreviation to avoid ambiguity.
Additionally, solids require a semicolon after subscripts, otherwise the
``s`` would be interpreted as sulphur. Semicolons can be used in unambiguous
cases, in which they will be ignored.

=========  =========================  =====================
Examples
-----------------------------------------------------------
Input      Output                     Notes
=========  =========================  =====================
``heg``    He                         *(extra "g" ignored)*
``he;g``   He\ :sub:`(g)`
``li2s``   Li\ :sub:`2`\ S
``li2;s``  Li\ :sub:`2(s)`
``li=s``   Li\ :sup:`+`\ :sub:`(s)`
``li=;s``  Li\ :sup:`+`\ :sub:`(s)`
``li;=s``  Li + S
``li=s2``  Li + S\ :sub:`2`
=========  =========================  =====================


Coefficients
------------
Coefficients can be added to elements or compounds by including the value of
the coefficient before the element or compound.

========  ===============
Examples
-------------------------
Input     Output
========  ===============
``2h2o``  2H\ :sub:`2`\ O
``10he``  10He
========  ===============


Hydrates
--------
Slash (``/``) is converted into the hydrate dot ("•"), so hydrates can be
made.

==============  ===========================================
Examples
-----------------------------------------------------------
Input           Output
==============  ===========================================
``cocl2/6h2o``  CoCl\ :sub:`2`\  • 6H\ :sub:`2`\ O
``li3=/6h2o``   Li\ :sub:`3`\ :sup:`+`\  • 6H\ :sub:`2`\ O
==============  ===========================================


.. _sum:
.. _arrow:
.. _`chemical equation`:

Chemical Equations and Fragments
--------------------------------
Elements and compounds can be added together to form fragments of or full
chemical equations. Equals (``=``) is used to add elements together, while
minus (``-``) creates an equation arrow ("→"). |plus_note|

=========================  ===============================================================================
Examples
----------------------------------------------------------------------------------------------------------
Input                      Output
=========================  ===============================================================================
``mgo=h2o-mg'oh'2``        MgO + H\ :sub:`2`\ O → Mg(OH)\ :sub:`2`
``2cl-aq=2ag=aq-2agcl;s``  2Cl\ :sup:`-`\ :sub:`(aq)`\  + 2Ag\ :sup:`+`\ :sub:`(aq)`\  → 2AgCl\ :sub:`(s)`
=========================  ===============================================================================

.. |plus_note| replace::

    Note that plus (``+``) is typed as equals (``=``) because both are on the
    same key on most standard keyboards and equals does not require the shift
    key to be pressed.
