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

import argparse
import collections

from pyparsing import ParseException

import quichem.parser
import quichem.compilers.html
import quichem.compilers.plain
import quichem.compilers.latex
import quichem.compilers.rst


parser = quichem.parser.parser_factory()
COMPILERS = collections.OrderedDict(
    HTML=quichem.compilers.html.HtmlCompiler(),
    plain=quichem.compilers.plain.PlainCompiler(),
    LaTeX=quichem.compilers.latex.LatexCompiler(),
    reStructuredText=quichem.compilers.rst.RstCompiler(),
)


class GenericGui(object):

    def __init__(self):
        self.compilers = self.sources = None

    def change_value(self, val):
        try:
            ast = parser.parseString(val, parseAll=True)
        except ParseException as e:
            self.set_html(str(e))
            for source in self.sources:
                self.set_source(source, '')
        else:
            html = COMPILERS['HTML'].compile(ast)
            self.set_html(html)
            for compiler, source in zip(self.compilers.values(), self.sources):
                self.set_source(source, compiler.compile(ast))

    def run(self):
        self.compilers = collections.OrderedDict(
            (name, COMPILERS[name]) for name in parse_args().compilers)
        self.sources = [self.make_source(name) for name in self.compilers]

    def make_source(self, name):
        raise NotImplementedError

    def set_html(self, html):
        raise NotImplementedError

    def set_source(self, widget, source):
        raise NotImplementedError


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--compilers', nargs='+', dest='compilers',
                        choices=COMPILERS.keys(), default=COMPILERS.keys(),
                        help='which compilers to enable; default is all')
    return parser.parse_args()
