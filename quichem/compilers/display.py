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

from quichem.compilers.compiler import Compiler


class DisplayCompiler(Compiler):

    """Generic compiler for rendering to displayable text formats.

    Output from this compiler and its subclasses is in UTF-8.

    """

    def handle_separator(self, separator):
        if separator.type_ == '=':
            return ' + '
        if separator.type_ == '-':
            return ' \u2192 '
        if separator.type_ == '/':
            return ' \u2022 '
        raise Exception('Separator not supported.')

    def handle_coefficient(self, coefficient):
        if coefficient.denominator == '1':
            if coefficient.numerator == '1':
                return ''
            return '{}\u2006'.format(coefficient.numerator)
        return '{}\u2044{}\u2006'.format(coefficient.numerator,
                                         coefficient.denominator)

    def handle_charge(self, charge):
        if charge.value == '0':
            return ''
        value = '' if charge.value == '1' else charge.value
        sign = '+' if charge.sign == '=' else '-'
        return value + sign

    def handle_state(self, state):
        if state.state == '':
            return ''
        if state.state == 'l':
            return '(\u2113)'
        return '({})'.format(state.state)

    def handle_element(self, element):
        return element.symbol.title()

    def handle_counter(self, counter):
        if counter.count == '1':
            return ''
        return counter.count

    def handle_open_group(self):
        return '('

    def handle_close_group(self):
        return ')'
