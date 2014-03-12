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

"""Plain text compiler resources for `quichem`."""

from __future__ import unicode_literals

from quichem.compilers.display import DisplayCompiler


class PlainCompiler(DisplayCompiler):

    """Plain text compiler."""

    def __init__(self):
        DisplayCompiler.__init__(self)
        self.fragments['separator'].literals['='] = ' + '
        self.fragments['separator'].literals['-'] = ' \u27f6 '
        self.fragments['separator'].literals['/'] = '\xb7'
        self.fragments['coefficient'].wrap = ('{}\u2006', '{}\u2044{}\u2006')
        self.fragments['charge'].literals['='] = '\u207a'
        self.fragments['charge'].literals['-'] = '\u207b'
        for numeral in range(10):
            self.fragments['charge'].literals[str(numeral)] = (
                '\u2070\xb9\xb2\xb3\u2074\u2075\u2076\u2077\u2078'
                '\u2079'[numeral])
        self.fragments['state'].literals['l'] = '\u2113'
        self.fragments['state'].wrap = ('({})',)
        for numeral in range(10):
            self.fragments['counter'].literals[str(numeral)] = (
                '\u2080\u2081\u2082\u2083\u2084\u2085\u2086\u2087\u2088'
                '\u2089'[numeral])
        self.fragments['open group'].literals["'"] = '('
        self.fragments['close group'].literals["'"] = ')'


# FIXME: ascii plain text compiler needed
