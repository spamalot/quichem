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

The ``quichem`` parser does **not** (yet) handle:

    - isotopes
    - radioactive particles


Recent Changes
--------------
- **[2014-03-12]** Error messages are now significantly more helpful.
- **[2014-03-12]** Groups of elements that needed backtracking to disambiguate
  are now automatically handled by the change to ``modgrammar``.
- **[2014-02-15]** States only need semicolons in ambiguous situations (e.g.
  ``heg`` is now equivalent to ``he;g``, and will render as He\ :sub:`(g)`\ )
- **[2014-02-15]** Support for fractional and decimal coefficients.
- **[2013-08-26]** Invalid elements are no longer ignored. They are now syntax
  errors.


General Notes
-------------
The only symbols that the parser needs to recognize are:

    + ``=`` : either a `positive charge`_ or sum_ of two elements_/compounds_
    + ``-`` : either a `negative charge`_ or an `arrow`_ in a
      `chemical equation`_
    + ``/`` : dot used in hydrates_ or a fraction slash for fractional
      coefficients_
    + ``'`` : represents either an open or close parenthesis_
    + ``.``: decimal point in decimal coefficients or a separator used in
      ambiguous cases pertaining to elements, subscripts, and charges
    + ``;`` : separator used in ambiguous cases pertaining to state
    + numbers & lower-case letters

This means that one does not have to press shift while typing text to be
processed by the parser [*]_.

.. [*] When using a QWERTY keyboard.


Elements
--------
Elements are expected by the parser to be lower case. If only one element
is entered, its identity is unambiguous, so the parser can automatically
capitalize the first letter when necessary.

Invalid elements result in a syntax error.

========  ===============================================
Examples
---------------------------------------------------------
Input     Output
========  ===============================================
``o``     O
``pb``    Pb
``uuo``   Uuo
``x``     *[line 1, column 1] Expected item: Found 'x'*
========  ===============================================


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
To clarify ambiguous cases, put a dot (``.``) at any ambiguous
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
``cmg.ali``  CMgAlI
===========  ======

.. _parenthesis:

Sometimes elements require parentheses. Parentheses are inserted into
compounds by surrounding a segment of a compound with single-quotes (``'``).
Parentheses can be nested if necessary.

``quichem`` relies on close parentheses ending with a number. If a close
parenthesis without a subscript is needed, use 1 as the subscript and it will
be ignored

==================  =======================================================
Examples
---------------------------------------------------------------------------
Input               Output
==================  =======================================================
``ge'oh'4``         Ge(OH)\ :sub:`4`
``b'nh4'3'p.o4'2``  B(NH\ :sub:`4`\ )\ :sub:`3`\ (PO\ :sub:`4`\ )\ :sub:`2`
``ge''nh4'2o'4``    Ge((NH\ :sub:`4`\ )\ :sub:`2`\ O)\ :sub:`4`
``'cl2'1``          (Cl\ :sub:`2`\ )
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
``br-``   Br\ :sup:`⁻`
========  ============

If the charge has a numeric value, a dot (``.``) must be used to distinguish
it from a subscript_. A dot placed before a superscript without a numeric value
is ignored.

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

``quichem`` supports nearly all of the states of aggregation listed in
*Quantities, Units and Symbols in Physical Chemistry* [IUPAC2011]_.
Some common states are: 

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
``naq``      N\ :sub:`(aq)`
===========  =================

If the state could be misinterpreted as an element (e.g. ``hg`` could be
interpreted as mercury or as gaseous hydrogen), a semicolon (``;``) must be
placed before the state to avoid ambiguity. Semicolons can be used in
unambiguous cases, in which case they will be ignored.

=========  =========================
Examples
------------------------------------
Input      Output
=========  =========================
``he;g``   He\ :sub:`(g)`
``heg``    He\ :sub:`(g)`
``h;g``    H\ :sub:`(g)`
``hg``     Hg
``li2s``   Li\ :sub:`2`\ S
``li2;s``  Li\ :sub:`2(s)`
``li=s``   Li\ :sup:`+`\ :sub:`(s)`
``li=;s``  Li\ :sup:`+`\ :sub:`(s)`
``li;=s``  Li + S
``li=s2``  Li + S\ :sub:`2`
=========  =========================


Coefficients
------------
Coefficients can be added to elements or compounds by including the value of
the coefficient before the element or compound. Integer, fractional, and
decimal coefficients are supported. Fractional coefficients can be entered in
the format ``numerator/denominator``.

==========  ========================================
Examples
----------------------------------------------------
Input       Output
==========  ========================================
``2h2o``    2 H\ :sub:`2`\ O
``10he``    10 He
``1/2h2o``  \ :sup:`1`\ ⁄\ :sub:`2`\  H\ :sub:`2`\ O
``0.5h2o``  0.5 H\ :sub:`2`\ O
==========  ========================================


Hydrates
--------
Slash (``/``) is converted into the hydrate dot ("·"), so hydrates can be
made.

==============  ===========================================
Examples
-----------------------------------------------------------
Input           Output
==============  ===========================================
``cocl2/6h2o``  CoCl\ :sub:`2`·6 H\ :sub:`2`\ O
``li3=/6h2o``   Li\ :sub:`3`\ :sup:`+`·6 H\ :sub:`2`\ O
==============  ===========================================


.. _sum:
.. _arrow:
.. _`chemical equation`:

Chemical Equations and Fragments
--------------------------------
Elements and compounds can be added together to form fragments of or full
chemical equations. Equals (``=``) is used to add elements together, while
minus (``-``) creates an equation arrow ("⟶"). |plus_note|

=========================  ===================================================================================
Examples
--------------------------------------------------------------------------------------------------------------
Input                      Output
=========================  ===================================================================================
``mgo=h2o-mg'oh'2``        MgO + H\ :sub:`2`\ O ⟶ Mg(OH)\ :sub:`2`
``2cl-aq=2ag=aq-2agcl;s``  2 Cl\ :sup:`⁻`\ :sub:`(aq)`\  + 2 Ag\ :sup:`+`\ :sub:`(aq)`\  ⟶ 2 AgCl\ :sub:`(s)`
=========================  ===================================================================================

.. |plus_note| replace::

    Note that plus (``+``) is typed as equals (``=``) because both are on the
    same key on most standard keyboards and equals does not require the shift
    key to be pressed.



References
----------

.. [IUPAC2011] *Quantities, Units and Symbols in Physical Chemistry* (Green Book)

    http://www.iupac.org/home/projects/project-db/project-details.html?tx_wfqbe_pi1[project_nr]=110-2-81
