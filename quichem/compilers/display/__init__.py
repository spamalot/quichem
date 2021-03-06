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


from __future__ import unicode_literals

from quichem.compilers.compiler import Compiler, tokened_strings
from quichem.compilers.display import fragments


class DisplayCompiler(Compiler):

    """Generic compiler for rendering to displayable text formats.

    Attributes
    ----------
    fragments : dict
        Maps between token names and display fragments.
    token_fragments : dict
        Maps between token class objects and display fragments. The
        display fragment objects are the same objects as those stored
        in ``fragments``.

    """

    def __init__(self):
        Compiler.__init__(self)
        self.fragments = {
            'separator': fragments.Separator(),
            'element': fragments.Element(),
            'coefficient': fragments.Coefficient(),
            'charge': fragments.Charge(),
            'state': fragments.State(),
            'counter': fragments.Counter(),
            'open group': fragments.OpenCloseGroup(),
            'close group': fragments.OpenCloseGroup()}
        self.token_fragments = {tokened_strings[string]: fragment for
                                string, fragment in self.fragments.items()}

    def compile(self, ast):
        """Compile a `quichem` AST into a string of the compiled
        tokens.

        """
        return ''.join(Compiler.compile(self, ast))

    def handle(self, token):
        return self.token_fragments[next(x for x in self.token_fragments if isinstance(token, x))].render(token)
