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

    """LaTeX math mode compiler."""

    def __init__(self):
        DisplayCompiler.__init__(self)
        # We can use \underset or \overset{text}{arrow} to make text above
        # or below separators without using packages other than AMS.
        self.fragments['separator'].literals['='] = '+'
        self.fragments['separator'].literals['-'] = r'\longrightarrow'
        self.fragments['separator'].literals['/'] = r'\cdot{}'
        self.fragments['separator'].literals['=,'] = '='
        self.fragments['separator'].literals['-/'] = r'\rightleftarrows'
        self.fragments['separator'].literals['=/'] = r'\rightleftharpoons'
        self.fragments['coefficient'].wrap = (r'{}\,', r'\frac{{{}}}{{{}}}\,')
        self.fragments['charge'].literals['='] = '+'
        self.fragments['charge'].literals['-'] = '-'
        for numeral in range(10):
            self.fragments['charge'].literals[str(numeral)] = str(numeral)
        self.fragments['charge'].wrap = ('^{{{}}}{{}}',)
        self.fragments['state'].literals['l'] = r'\ell'
        self.fragments['state'].wrap = (r'_{{\mathrm{{({})}}}}{{}}',)
        self.fragments['element'].wrap = (r'\mathrm{{{}}}',)
        for numeral in range(10):
            self.fragments['counter'].literals[str(numeral)] = str(numeral)
        self.fragments['counter'].wrap = ('_{{{}}}{{}}',)
        self.fragments['open group'].literals["'"] = r'\left('
        self.fragments['close group'].literals["'"] = r'\right)'

    def _replace(self, match):
        """Take a regex match containing adjacent, identical LaTeX
        commands and combine them into a single command.

        """
        command = match.group(1)
        return ''.join(
            [command, '{',
             re.sub('\\' + command + r'\{(.*?)\}', r'\1', match.group(0)),
             '}'])

    def compile(self, ast):
        # Merge adjacent subscripts, superscripts and \mathrms.
        return r'\({}\)'.format(re.sub(
            r'(_|\^|\\mathrm)\{([^{}]+?)\}(?:\{\})?(?:\1\{([^{}]+?)\})+',
            self._replace, DisplayCompiler.compile(self, ast)))


class LatexMhchemV3Compiler(DisplayCompiler):

    """LaTeX compiler for ``mchem`` package."""

    def __init__(self):
        DisplayCompiler.__init__(self)
        self.fragments['separator'].literals['='] = ' + '
        self.fragments['separator'].literals['-'] = ' -> '
        self.fragments['separator'].literals['/'] = '*'
        self.fragments['separator'].literals['=,'] = ' = '
        self.fragments['separator'].literals['-/'] = ' <--> '
        self.fragments['separator'].literals['=/'] = ' <=> '
        self.fragments['coefficient'].wrap = ('{}', '{}/{}')
        self.fragments['charge'].literals['='] = '+'
        self.fragments['charge'].literals['-'] = '-'
        for numeral in range(10):
            self.fragments['charge'].literals[str(numeral)] = str(numeral)
        self.fragments['charge'].wrap = ('^{}',)
        self.fragments['state'].literals['l'] = r'$\ell$'
        self.fragments['state'].wrap = (' _{{({})}}',)
        for numeral in range(10):
            self.fragments['counter'].literals[str(numeral)] = str(numeral)
        self.fragments['open group'].literals["'"] = '('
        self.fragments['close group'].literals["'"] = ')'

    def compile(self, ast):
        return r'\ce{{{}}}'.format(DisplayCompiler.compile(self, ast))
