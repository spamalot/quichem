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

"""Parsing utilities for ``quichem``."""

from __future__ import unicode_literals

import modgrammar
from modgrammar import (L, WORD, OPTIONAL, ZERO_OR_MORE, ONE_OR_MORE, OR,
                        LIST_OF, GRAMMAR, NOT_FOLLOWED_BY)
from modgrammar.extras import RE

from quichem import tokens
from quichem import modgrammar_fixes as fixes


modgrammar.grammar_whitespace_mode = 'explicit'

ELEMENTS = (
    'uut uup uus uuo he li be ne na mg al si cl ar ca sc ti cr mn fe co ni cu '
    'zn ga ge as se br kr rb sr zr nb mo tc ru rh pd ag cd in sn sb te xe cs '
    'ba la ce pr nd pm sm eu gd tb dy ho er tm yb lu hf ta re os ir pt au hg '
    'tl pb bi po at rn fr ra ac th pa np pu am cm bk cf es fm md no lr rf db '
    'sg bh hs mt ds rg cn fl lv h b c n o f p s k v y i w u')

# FIXME: Still missing "aq, inf".
STATES = 'mon pol sln vit ads cd cr am aq lc s f l g n a'


def make_parser():
    """Create a parser for the ``quichem`` syntax.

    The parser handles coefficients, compounds, compounds, ions,
    subscripts, and states. Below a several examples and what they
    translate to in plain text (ASCII).

    ``3h2o;l`` -> 3H2O(l)
    ``mg2=`` -> Mg 2+
    ``cmgali`` -> CmGaLi
    ``c.mgali`` -> CMgAlI

    For a full syntax description, see SYNTAX.rst, included with the
    library.

    Returns
    -------
    The `quichem` parser.

    """

    # Note: Support for isotopes can be added by requiring brackets around
    # the value. E.g. 3'14'c -> 3^{14}C, '12''nh4'2s -> ^{12}(NH_3)_2S.
    # The proton value can be automatically provided based on the following
    # element, and can be overridden by manually specifying a value (e.g.
    # '14;4'c -> ^{14}_4C ). These quotes can be distinguished from brackets,
    # because brackets must always end in a number, but these quotes cannot
    # end in a number.

    element_word = OR(*ELEMENTS.split())
    dot = L('.')
    semicolon = L(';')
    dash = L('-', tags=('sign', 'separator'))
    equals = L('=', tags=('sign', 'separator'))
    slash = L('/', tags=('separator',))
    state_word = GRAMMAR(
        OR(*(L(state, tags=('state_word',)) for state in STATES.split())),
        collapse=True, desc='state')
    number = RE(r'\d+', tags=('number',))
    decimal = RE(r'\d+\.\d*|\.\d+', tags=('decimal',))
    parenthesis = L("'")

    element = fixes.g([element_word], 'element', tokens.Element)
    compound_segment_ref = fixes.ref(lambda: compound_segment)
    group = fixes.g(
        [parenthesis, compound_segment_ref, parenthesis, RE(r'(?=\d)')],
        'group', tokens.Group)
    counter = fixes.g(
        [(element | group), OPTIONAL(number, collapse=True), OPTIONAL(dot)],
        'counter', tokens.Counter)
    compound_segment = fixes.g(
        [ONE_OR_MORE(counter, collapse=True)], 'compound_segment',
        desc='element')
    compound = fixes.g([compound_segment], 'compound', tokens.Compound)
    state = fixes.g([OPTIONAL(semicolon), state_word], 'state', tokens.State)
    coefficient = fixes.g([decimal | (number, OPTIONAL(slash, number))],
                          'coefficient', tokens.Coefficient)
    charge = fixes.g([OPTIONAL(number), (equals | dash)],
                     'charge', tokens.Charge)
    # We need to have both a stateless item and a item with a state
    # to ensure that a stateless item have higher precedence (e.g. to
    # ensure that "clina" render as "ClINa" and not "ClIN(a)").
    #
    # The NOT_FOLLOWED_BY(charge) ensures we take the item with a
    # state. This ensures that the charge is distinguished from a
    # separator.
    stateless_item = [OPTIONAL(coefficient), compound,
                      OPTIONAL(OPTIONAL(dot), charge)]
    item = fixes.g(
        [GRAMMAR(stateless_item + [NOT_FOLLOWED_BY(charge)], collapse=True) |
         (stateless_item + [OPTIONAL(state)])],
        'item', tokens.Item)
    # We have an optional semicolon here to allow for distinction
    # between a sign + state and a separator + element (e.g.
    # positively charged solid vs. plus sulphur).
    separator = fixes.g([OPTIONAL(semicolon), (equals | dash | slash)],
                        'separator', tokens.Separator)

    class Grammar(modgrammar.Grammar):
        grammar = LIST_OF(item, sep=separator, collapse=True)

    Grammar.grammar_resolve_refs()
    return Grammar.parser()


def parse(string, parser):
    """Parse a string using the given parser.

    Returns
    -------
    A list of tokens storing the parsed data.

    """
    result = parser.parse_string(string)
    return [] if result is None else list(result.elements)
