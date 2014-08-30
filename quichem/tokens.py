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

"""Contains classes representing various syntax tokens."""


from __future__ import unicode_literals

from quichem.modgrammar_fixes import Token, default, string


__all__ = ['Element', 'Group', 'Counter', 'Compound', 'State', 'Coefficient',
           'Charge', 'Item', 'Separator']


class Element(Token):

    """Represents an individual element.

    Attributes
    ----------
    symbol : string
        An element symbol in lowercase letters.

    """

    def grammar_init(self):
        self.symbol = string(self)

    def __repr__(self):
        return 'Element[{}]'.format(self.symbol)


class Group(Token):

    """Represents a bracketed group of elements in a compound.

    Attributes
    ----------
    list_ : list
        Contains `Counter`\ s storing other elements or groups.

    See Also
    --------
    Compound

    """

    def grammar_init(self):
        self.list_ = self.get_all('compound_segment', 'counter')

    def __repr__(self):
        return 'Group[{!r}]'.format(self.list_)


class Counter(Token):

    """Associates a count (subscript) with an item.

    Attributes
    ----------
    item : Element, Group
        An item to associate the counter with.
    count : string
        The count associated with the item.

    """

    def grammar_init(self):
        self.item = self.get('element') or self.get('group')
        self.count = default(string(self.get('number')), '1')

    def __repr__(self):
        return 'Counter[{!r}, {}]'.format(self.item, self.count)


class Compound(Token):

    """Represents a chemical compound.

    Attributes
    ----------
    list_ : list
        Contains `Counter`\ s storing elements or groups.

    See Also
    --------
    Group

    """

    def grammar_init(self):
        self.list_ = self.get_all('compound_segment', 'counter')

    def __repr__(self):
        return 'Compound[{!r}]'.format(self.list_)


class State(Token):

    """Represents a state of aggregation.

    Attributes
    ----------
    state : string
        An abbreviated state of aggregation.

    """

    def grammar_init(self):
        self.state = string(self.find('state_word'))

    def __repr__(self):
        return 'State[{}]'.format(self.state)


class Coefficient(Token):

    """Represents a coefficient of an item in a chemical equation.

    Attributes
    ----------
    numerator : string
        The numerator of the coefficient.
    denominator: string
        The denominator of the coefficient, or '1' if the numerator
        is a decimal.

    """

    def grammar_init(self):
        self.numerator, self.denominator = string(self.find('decimal')), '1'
        if self.numerator is None:
            self.numerator, self.denominator = (
                list(map(string, self.find_all('number'))) + ['1'])[:2]

    def __repr__(self):
        return 'Coefficient[{}, {}]'.format(self.numerator, self.denominator)


class Charge(Token):

    """Represents the charge of an ion or charged compound.

    Attributes
    ----------
    value : string
        The numerical value of the charge (0 means no charge).
    sign : string
        Either "=" (positive) or "-" (negative), representing whether
        the value of the charge is applied positively or negatively.
        This value is ignored if the charge is 0.

    """

    def grammar_init(self):
        self.value = default(string(self.find('number')), '1')
        self.sign = string(self.find('sign'))

    def __repr__(self):
        return 'Charge[{}, {}]'.format(self.value, self.sign)


class Item(Token):

    """Represents an compound in a chemical equation with a coefficient,
    charge, and state.

    Attributes
    ----------
    coefficient : Coefficient
    compound : Compound
    charge : Charge
    state : State

    """

    def grammar_init(self):
        self.coefficient = default(
            self.find('coefficient'),
            Coefficient.from_attributes(numerator='1', denominator='1'))
        self.compound = self.find('compound')
        self.charge = default(self.find('charge'),
                              Charge.from_attributes(value='0', sign=''))
        self.state = default(self.find('state'),
                             State.from_attributes(state=''))

    def __repr__(self):
        return 'Item[{!r}, {!r}, {!r}, {!r}]'.format(
            self.coefficient, self.compound, self.charge, self.state)


class Separator(Token):

    """Represents a separator in a chemical equation, such as a plus
    sign or arrow.

    Attributes
    ----------
    type_ : string
        The type of separator ("=", "-", "/", "=,", "-/", or "=/").

    """

    def grammar_init(self):
        self.type_ = string(self.find('separator_word'))
        if self.type_ == ',=':
            self.type_ = '=,'

    def __repr__(self):
        return 'Separator[{}]'.format(self.type_)
