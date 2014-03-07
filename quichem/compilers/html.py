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


class HtmlCompiler(DisplayCompiler):

    def __init__(self):
        DisplayCompiler.__init__(self)
        self.fragments['separator'].literals['='] = '&nbsp;+&nbsp;'
        self.fragments['separator'].literals['-'] = '&nbsp;&#x27f6;&nbsp;'
        self.fragments['separator'].literals['/'] = '&#x2022;'
        self.fragments['coefficient'].wrap = (
            '{}&#x2006;', '<sup>{}</sup>&frasl;<sub>{}</sub>&#x2006;')
        self.fragments['charge'].literals['='] = '+'
        self.fragments['charge'].literals['-'] = '&#x2212;'
        for numeral in xrange(10):
            self.fragments['charge'].literals[str(numeral)] = str(numeral)
        self.fragments['charge'].wrap = ('<sup>{}</sup>',)
        self.fragments['state'].literals['l'] = '&#x2113;'
        self.fragments['state'].wrap = ('<sub>({})</sub>',)
        for numeral in xrange(10):
            self.fragments['counter'].literals[str(numeral)] = str(numeral)
        self.fragments['counter'].wrap = ('<sub>{}</sub>',)
        self.fragments['open group'].literals["'"] = '('
        self.fragments['close group'].literals["'"] = ')'

    def compile(self, ast):
        # Merge adjacent subscripts and superscripts.
        return re.sub(r'<(sup|sub)>(.+?)</\1><\1>(.+?)</\1>', r'<\1>\2\3</\1>',
                      DisplayCompiler.compile(self, ast))
