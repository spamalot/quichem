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


class CompoundSegment(object):

    """Represents a segment of a chemical compound."""


class Element(CompoundSegment):

    """Represents an individual element.

    Parameters
    ----------
    args : iterable
        The first item should be an element symbol in small-caps.

    """

    def __init__(self, args):
        self.symbol, = args

    def __repr__(self):
        return 'Element[{}]'.format(self.symbol)


class Group(CompoundSegment):

    """Represents a bracketed group of elements in a compound.

    Parameters
    ----------
    args : iterable
        Should contain `Counter`\ s storing other elements or groups.

    See Also
    --------
    Compound

    """

    def __init__(self, args):
        self.list_ = args

    def __repr__(self):
        return 'Group[{}]'.format(self.list_)


class Counter(object):

    """Associates a count with an item.

    Parameters
    ----------
    args : iterable
        The first item should be an item to associate the counter with.
        The second item should be the count associated with the item.

    """

    def __init__(self, args):
        self.item, self.count = args

    def __repr__(self):
        return 'Counter[{}, {}]'.format(self.item, self.count)


class Compound(object):

    """Represents a chemical compound.

    Parameters
    ----------
    args : iterable
        Should contain `Counter`\ s storing elements or groups.

    See Also
    --------
    Group

    """

    def __init__(self, args):
        self.list_ = args

    def __repr__(self):
        return 'Compound[{}]'.format(self.list_)


class State(object):

    """Represents a state of matter.

    Parameters
    ----------
    args : iterable
        The first item should be a state of matter.

    """

    def __init__(self, args):
        self.state, = args

    def __repr__(self):
        return 'State[{}]'.format(self.state)


class Coefficient(object):

    """Represents a coefficient of an item in a chemical equation.

    Parameters
    ----------
    args : iterable
        The first item should be the numerator of the coefficient. The
        second item should be the denominator, or '1' if the numerator
        is a decimal.

    """

    def __init__(self, args):
        self.numerator, self.denominator = args

    def __repr__(self):
        return 'Coefficient[{}, {}]'.format(self.numerator, self.denominator)


class Charge(object):

    """Represents the charge of an ion or charged compound.

    Parameters
    ----------
    args : iterable
        The first item should contain the numerical value of the charge
        (0 means no charge). The second item should contain whether the
        value of the charge should be applied positively or negatively.
        This value is ignored if the charge is 0.

    """

    def __init__(self, args):
        self.value, self.sign = args

    def __repr__(self):
        return 'Charge[{}, {}]'.format(self.value, self.sign)


class Item(object):

    """Represents an compound in a chemical equation with a coefficient,
    charge, and state.

    Parameters
    ----------
    args : iterable
        The first four items should be the (coefficient, compound,
        charge, and state) of the item.

    """

    def __init__(self, args):
        self.coefficient, self.compound, self.charge, self.state = args

    def __repr__(self):
        return 'Item[{}, {}, {}, {}]'.format(self.coefficient, self.compound,
                                             self.charge, self.state)


class Separator(object):

    """Represents a separator in a chemical equation, such as a plus
    sign or arrow.

    Parameters
    ----------
    args : iterable
        The first item should be the type of separator.

    """

    def __init__(self, args):
        self.type_, = args

    def __repr__(self):
        return 'Separator[{}]'.format(self.type_)
