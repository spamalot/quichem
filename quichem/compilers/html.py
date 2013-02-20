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

    def compile(self, ast):
        return re.sub(r'<(sup|sub)>(.+?)</\1><\1>(.+?)</\1>', r'<\1>\2\3</\1>',
                      DisplayCompiler.compile(self, ast))

    def handle_separator(self, separator):
        if separator.type_ == '=':
            return '&nbsp;+&nbsp;'
        if separator.type_ == '-':
            return '&nbsp;&#x2192;&nbsp;'
        if separator.type_ == '/':
            return '&nbsp;&#x2022;&nbsp;'
        raise Exception('Separator not supported.')

    def handle_charge(self, charge):
        charge = DisplayCompiler.handle_charge(self, charge)
        if charge:
            return '<sup>{}</sup>'.format(charge)
        return ''

    def handle_state(self, state):
        display_state = DisplayCompiler.handle_state(self, state)
        if state.state == 'l':
            display_state = '(&#x2113;)'
        if display_state:
            return '<sub>{}</sub>'.format(display_state)
        return ''

    def handle_counter(self, counter):
        counter = DisplayCompiler.handle_counter(self, counter)
        if counter:
            return '<sub>{}</sub>'.format(counter)
        return ''
