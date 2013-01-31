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


class Compiler(object):

    """Abstract compiler for `quichem` ASTs.

    `handle_*` methods handle the corresponding tokens in
    `quichem.tokens`.

    """

    def __init__(self):
        self.result = None

    def compile(self, ast):
        """Compiles a `quichem` AST into the desirable output type."""
        self.result = []
        for token in ast:
            if isinstance(token, Separator):
                self.result.append(self.handle_separator(token))
            elif isinstance(token, Item):
                self.result.append(self.handle_coefficient(token.coefficient))
                for counter in token.compound.list_:
                    self.compile_counter(counter)
                self.result.append(self.handle_charge(token.charge))
                self.result.append(self.handle_state(token.state))
            else:
                raise Exception('Invalid token in AST.')
        return ''.join(self.result)

    def compile_counter(self, counter):
        """Recursively compile a counter."""
        if isinstance(counter, Element):
            self.result.append(self.handle_element(counter))
        elif isinstance(counter, Group):
            self.result.append(self.handle_open_group())
            for element in counter.list_:
                self.compile_counter(element)
            self.result.append(self.handle_close_group())
        elif isinstance(counter, Counter):
            self.compile_counter(counter.item)
            self.result.append(self.handle_counter(counter))

    def handle_separator(self, separator):
        raise NotImplementedError

    def handle_coefficient(self, coefficient):
        raise NotImplementedError

    def handle_charge(self, charge):
        raise NotImplementedError

    def handle_state(self, state):
        raise NotImplementedError

    def handle_element(self, element):
        raise NotImplementedError

    def handle_counter(self, counter):
        raise NotImplementedError

    def handle_open_group(self):
        raise NotImplementedError

    def handle_close_group(self):
        raise NotImplementedError
