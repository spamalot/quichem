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

import re

from quichem.compilers.display import DisplayCompiler


class RstCompiler(DisplayCompiler):

    """reStructuredText compiler."""

    def __init__(self):
        DisplayCompiler.__init__(self)
        self.fragments['separator'].literals['='] = ' + '
        self.fragments['separator'].literals['-'] = ' \u27f6 '
        self.fragments['separator'].literals['/'] = '\xb7'
        self.fragments['separator'].literals['=,'] = ' = '
        self.fragments['separator'].literals['-/'] = ' \u21c4 '
        self.fragments['separator'].literals['=/'] = ' \u21cc '
        self.fragments['coefficient'].wrap = (
            '{}\u2006', r'\ :sup:`{}`\ ' '\u2044\ ' r':sub:`{}`\ ' '\u2006')
        self.fragments['charge'].literals['='] = '+'
        self.fragments['charge'].literals['-'] = '\u2212'
        for numeral in range(10):
            self.fragments['charge'].literals[str(numeral)] = str(numeral)
        self.fragments['charge'].wrap = (r'\ :sup:`{}`\ ',)
        self.fragments['state'].literals['l'] = '\u2113'
        self.fragments['state'].wrap = (r'\ :sub:`({})`\ ',)
        for numeral in range(10):
            self.fragments['counter'].literals[str(numeral)] = str(numeral)
        self.fragments['counter'].wrap = (r'\ :sub:`{}`\ ',)
        self.fragments['open group'].literals["'"] = '('
        self.fragments['close group'].literals["'"] = ')'

    def compile(self, ast):
        return re.sub(r'(\\ :(?:sub|sup):`)([^`]+?)`\\ \1([^`]+?)`\\ ',
                      r'\1\2\3`\\ ',
                      DisplayCompiler.compile(self, ast)
                      ).replace(r'\ \ ', r'\ ').rstrip(r'\ ')
