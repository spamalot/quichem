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
                       ParseException, Regex, NoMatch)

import quichem.tokens


ELEMENTS = (
    'uut uup uus uuo he li be ne na mg al si cl ar ca sc ti cr mn fe co ni cu '
    'zn ga ge as se br kr rb sr zr nb mo tc ru rh pd ag cd in sn sb te xe cs '
    'ba la ce pr nd pm sm eu gd tb dy ho er tm yb lu hf ta re os ir pt au hg '
    'tl pb bi po at rn fr ra ac th pa np pu am cm bk cf es fm md no lr rf db '
    'sg bh hs mt ds rg cn fl lv h b c n o f p s k v y i w u')

DEFAULT_DENOMINATOR = '1'
DEFAULT_COUNT_NUMBER = '1'
DEFAULT_CHARGE_NUMBER = '1'
DEFAULT_COEFFICIENT_NUMBER = '1'
DEFAULT_COEFFICIENT = quichem.tokens.Coefficient(('1', '1'))
DEFAULT_CHARGE = quichem.tokens.Charge(('0', ''))
DEFAULT_STATE = quichem.tokens.State(('',))


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

    number = Word(nums).setName('number')
    decimal = Regex(r'\d+(\.\d*)?|\.\d+')

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
    # Optional(NoMatch(), ...) allows us to insert text to match the
    # parse action's arguments. Ideally, there is a better solution than
    # this.
    coefficient = ((decimal +
                   Optional(NoMatch(), DEFAULT_COEFFICIENT_NUMBER)) ^
                   (number + Optional(Suppress(slash) + number,
                    DEFAULT_DENOMINATOR)))
    element = oneOf(ELEMENTS)

    compound = Forward()
    compound_segment = Forward()
    group = Suppress(lbracket) + compound_segment + Suppress(rbracket)
    counter = ((element | group) + Optional(number |
               (Suppress(dot) + Optional(NoMatch(), DEFAULT_COUNT_NUMBER)),
               DEFAULT_COUNT_NUMBER))
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
    element.setParseAction(quichem.tokens.Element).setName('element')
    group.setParseAction(quichem.tokens.Group).setName('group')
    counter.setParseAction(quichem.tokens.Counter).setName('counter')
    compound.setParseAction(quichem.tokens.Compound).setName('compound')
    item.setParseAction(quichem.tokens.Item).setName('item')
    separator.setParseAction(quichem.tokens.Separator).setName('separator')

    return expression
