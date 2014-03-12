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

"""Contains the abstract compiler for `quichem` ASTs."""


from __future__ import unicode_literals

from quichem.tokens import Counter, Element, Group, Item, Separator
import quichem.tokens
from quichem.compilers.compiler import flat_tokens


class Compiler(object):

    """Abstract compiler for `quichem` ASTs."""

    def __init__(self):
        self.result = None

    def compile(self, ast):
        """Compile a `quichem` AST into the desirable output type.

        By default, return a list of compiled tokens.

        """
        self.result = []
        for token in ast:
            if isinstance(token, Separator):
                self.result.append(self.handle(token))
            elif isinstance(token, Item):
                self.result.append(self.handle(token.coefficient))
                for counter in token.compound.list_:
                    self.compile_counter(counter)
                self.result.append(self.handle(token.charge))
                self.result.append(self.handle(token.state))
            else:
                raise Exception('Invalid token in AST.')
        return self.result

    def compile_counter(self, counter):
        """Recursively compile a counter."""
        if isinstance(counter, Element):
            self.result.append(self.handle(counter))
        elif isinstance(counter, Group):
            self.result.append(self.handle(tokened_strings['open group']()))
            for element in counter.list_:
                self.compile_counter(element)
            self.result.append(self.handle(tokened_strings['close group']()))
        elif isinstance(counter, Counter):
            self.compile_counter(counter.item)
            self.result.append(self.handle(counter))

    def handle(self, token):
        """Return the desirable output for a given individual token.

        Must be implemented in subclasses.

        """
        raise NotImplementedError


tokened_strings = {
    'separator': quichem.tokens.Separator,
    'coefficient': quichem.tokens.Coefficient,
    'charge': quichem.tokens.Charge,
    'state': quichem.tokens.State,
    'element': quichem.tokens.Element,
    'counter': quichem.tokens.Counter,
    'open group': flat_tokens.OpenGroup,
    'close group': flat_tokens.CloseGroup,
}
