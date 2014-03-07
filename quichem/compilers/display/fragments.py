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

"""Generic display compilers for individual tokens."""


from __future__ import unicode_literals


class DisplayFragment(object):

    """Base display compiler for individual tokens (fragments).

    Subclass to provide behavior for a specific token.

    Attributes
    ----------
    wrap : tuple
        Contains formatting strings for different renderings of the
        fragment (using new-style Python string formatting). Should
        be in the order from lowest number of format substitutions to
        highest number of format substitutions.
    literals : dict
        Contains rendered outputs for individual symbols within the
        token.

    """

    def __init__(self):
        self.wrap = ()
        self.literals = {}

    def render(self, token):
        parts = self.compile_parts(token)
        if not parts:
            return ''
        if not self.wrap:
            return ('{}' * len(parts)).format(*parts)
        a = self.wrap[len(parts) - 1].format(*parts)
        return a

    def compile_parts(self, token):
        raise NotImplementedError


class Separator(DisplayFragment):

    """Requires a literal for "=" (plus), "-" (arrow), and "/"
    (hydrate).

    See Also
    --------
    quichem.tokens.Separator

    """

    def compile_parts(self, token):
        if token.type_ == '=':
            return (self.literals['='],)
        if token.type_ == '-':
            return (self.literals['-'],)
        if token.type_ == '/':
            return (self.literals['/'],)
        raise Exception('Separator not supported.')


class Coefficient(DisplayFragment):

    """Requires no literals. ``wrap`` should add proper spacing and
    also a fraction slash if there are two parameters.

    See Also
    --------
    quichem.tokens.Separator

    """

    def compile_parts(self, token):
        if token.denominator == '1':
            if token.numerator == '1':
                return ()
            return (token.numerator,)
        return (token.numerator, token.denominator)


class Charge(DisplayFragment):

    """Requires a literal for "-" (negative charge), "=" (positive
    charge) and for each of "0".."9" (superscripts).

    See Also
    --------
    quichem.tokens.Separator

    """

    def compile_parts(self, token):
        if token.value == '0':
            return ()
        value = ('' if token.value == '1' else
                 ''.join(self.literals[number] for number in token.value))
        sign = self.literals[token.sign]
        return (value + sign,)


class State(DisplayFragment):

    """Requires a literal for "l" (liquid). ``wrap`` should add
    parentheses.

    See Also
    --------
    quichem.tokens.Separator

    """

    def compile_parts(self, token):
        if token.state == '':
            return ()
        if token.state == 'l':
            return (self.literals['l'],)
        return (token.state,)


class Element(DisplayFragment):

    """Requires no literals.

    Capitalization is done automatically.

    See Also
    --------
    quichem.tokens.Separator

    """

    def compile_parts(self, token):
        return (token.symbol.title(),)


class Counter(DisplayFragment):

    """Requires a literal for "1".."9" (subscript).

    See Also
    --------
    quichem.tokens.Separator

    """

    def compile_parts(self, token):
        if token.count == '1':
            return ()
        return (''.join(self.literals[number] for number in token.count),)


class OpenCloseGroup(DisplayFragment):

    """Requires a literal for "'" (parenthesis).

    Can be used to represent either an open or a close group.

    See Also
    --------
    quichem.tokens.Separator

    """

    def compile_parts(self, token):
        return (self.literals["'"],)
