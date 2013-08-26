# This file is part of quichem.
#
# quichem is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# quichem is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with quichem.  If not, see <http://www.gnu.org/licenses/>.

"""Parsing utilities for `quichem`."""


from __future__ import unicode_literals

import re
import string

from pyparsing import (FollowedBy, Forward, Literal, OneOrMore, Optional,
                       StringEnd, Suppress, Word, ZeroOrMore, nums, oneOf,
                       ParseException)

import quichem.tokens


ELEMENTS = '|'.join(sorted((
    'H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V '
    'Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc '
    'Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La Ce Pr Nd Pm Sm Eu '
    'Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi '
    'Po At Rn Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr '
    'Rf Db Sg Bh Hs Mt Ds Rg Cn Uut Fl Uup Lv Uus Uuo'
).lower().split(), key=len, reverse=True))

DEFAULT_COUNT_NUMBER = '1'
DEFAULT_CHARGE_NUMBER = '1'
DEFAULT_COEFFICIENT = quichem.tokens.Coefficient(('1',))
DEFAULT_CHARGE = quichem.tokens.Charge(('0', ''))
DEFAULT_STATE = quichem.tokens.State(('',))


# Token Factories
def number_factory():
    """Create a new `pyparsing` integer."""
    return Word(nums).setName('number')


def alpha_factory():
    """Create a new `pyparsing` word matching lower case ascii letters.

    """
    return Word(string.ascii_lowercase).setName('string')


# Parse Actions
def element_factory(args):
    """Parse action to create a list of element symbols.

    Parameters
    ----------
    args : Iterable
        Contains a mixture of `quichem.tokens.CompoundSegment`\ s and
        strings of chained element symbols. Strings will be split before
        being added to the list. This function splits by taking the
        longest element symbol first, meaning ambiguous cases can always
        be clarified through manual splitting of symbols.

    Returns
    -------
    list of `quichem.tokens.CompoundSegment`\ s

    """
    compound_segments = []
    for item in args:
        if isinstance(item, quichem.tokens.CompoundSegment):
            compound_segments.append(item)
        else:
            element_strings = re.findall(ELEMENTS, item)
            if item != ''.join(element_strings):
                raise ParseException('Unknown element')
            compound_segments.extend(quichem.tokens.Element([element])
                                     for element in element_strings)
    return compound_segments


def counter_factory(args):
    """Parse action to create a counter for every item in a list.

    Parameters
    ----------
    args : Iterable
        Must be in the format [item_0, item_1, item_2, ..., item_n,
        count_n] (only the last item is a counter).

    Returns
    -------
    list of `quichem.tokens.Counter`\ s

    """
    counters = []
    for item in args[:-2]:
        counters.append(quichem.tokens.Counter([item, '1']))
    # PyParsing handles IndexErrors for us, so we use the following
    # instead of args[-2:].
    counters.append(quichem.tokens.Counter([args[-2], args[-1]]))
    return counters


# Syntax
def parser_factory():
    """Create the parser for the `quichem` library.

    The parser handles coefficients, compounds, compounds, ions,
    subscripts, and states. Below a several examples and what they
    translate to in plain text.

    ``3h2o;l`` -> 3H2O(l)
    ``mg2=`` -> Mg2+
    ``cmgali`` -> CmGaLi
    ``c.mgali`` -> CMgAlI

    For a full syntax description, see SYNTAX.rst, included with the
    library.

    Returns
    -------
    The `quichem` parser.

    """
    # Basic
    dot = Literal('.').setName('dot')
    semicolon = Literal(';').setName('semicolon')
    dash = Literal('-').setName('dash')
    equals = Literal('=').setName('equals')
    slash = Literal('/').setName('slash')
    number = number_factory()
    lbracket = (Literal("'") + ~FollowedBy(number)).setName('left bracket')
    rbracket = (Literal("'") + FollowedBy(number)).setName('right bracket')

    # Note: Support for isotopes can be added by requiring brackets around
    # the value. E.g. 3'14'c -> 3^{14}C, '12''nh4'2s -> ^{12}(NH_3)_2S.
    # The proton value can be automatically provided based on the following
    # element, and can be overridden by manually specifying a value (e.g.
    # '14;4'c -> ^{14}_4C ). These quotes can be distinguished from brackets,
    # because brackets must always end in a number, but these quotes cannot
    # end in a number.

    separator = (Suppress(Optional(semicolon)) + (equals | dash | slash) +
                 ~FollowedBy(semicolon))
    state = (Suppress(Optional(semicolon)) + oneOf('s l g aq') +
             FollowedBy(separator | StringEnd()))
    state_lookahead = state | separator | StringEnd()

    charge = Optional(number, DEFAULT_CHARGE_NUMBER) + (equals | dash)
    coefficient = number_factory()
    element_chain = alpha_factory()
    element = element_chain + ZeroOrMore(Suppress(dot) + element_chain)

    compound = Forward()
    compound_segment = Forward()
    group = Suppress(lbracket) + compound_segment + Suppress(rbracket)
    counter = (element | group) + Optional(number, DEFAULT_COUNT_NUMBER)
    compound_segment << OneOrMore(counter)
    compound << (counter + ZeroOrMore(compound_segment))
    item = (Optional(coefficient, DEFAULT_COEFFICIENT) + compound +
            Optional(Suppress(Optional(dot)) + charge +
                     FollowedBy(state_lookahead), DEFAULT_CHARGE) +
            Optional(state, DEFAULT_STATE))

    expression = item + ZeroOrMore(separator + item)

    state.setParseAction(quichem.tokens.State).setName('state')
    charge.setParseAction(quichem.tokens.Charge).setName('charge')
    coefficient.setParseAction(
        quichem.tokens.Coefficient).setName('coefficient')
    element_chain.setParseAction(element_factory).setName('element')
    element.setParseAction(element_factory)
    group.setParseAction(quichem.tokens.Group).setName('group')
    counter.setParseAction(counter_factory).setName('counter')
    compound.setParseAction(quichem.tokens.Compound).setName('compound')
    item.setParseAction(quichem.tokens.Item).setName('item')
    separator.setParseAction(quichem.tokens.Separator).setName('separator')

    return expression
