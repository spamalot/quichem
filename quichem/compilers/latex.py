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


class LatexCompiler(DisplayCompiler):

    def compile(self, ast):
        return re.sub(
            r'(_|\^){([^{}]+?)}(?:{})?\1{([^{}]+?)}',
            r'\1{\2\3}',
            '$\mathrm{{{}}}$'.format(DisplayCompiler.compile(self, ast)))

    def handle_separator(self, separator):
        if separator.type_ == '=':
            return '+'
        if separator.type_ == '-':
            return r'\to '
        if separator.type_ == '/':
            return r'\bullet '
        raise Exception('Separator not supported.')

    def handle_charge(self, charge):
        charge = DisplayCompiler.handle_charge(self, charge)
        if charge:
            return '^{{{}}}'.format(charge)
        return ''

    def handle_state(self, state):
        state = DisplayCompiler.handle_state(self, state)
        if state:
            return '_{{{}}}'.format(state)
        return ''

    def handle_counter(self, counter):
        counter = DisplayCompiler.handle_counter(self, counter)
        if counter:
            return '_{{{}}}{{}}'.format(counter)
        return ''
