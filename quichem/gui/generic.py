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

from modgrammar import ParseError

import quichem.parser
import quichem.compilers.html
import quichem.compilers.plain
import quichem.compilers.latex
import quichem.compilers.rst


parser = quichem.parser.make_parser()
COMPILERS = collections.OrderedDict((
    ('HTML', quichem.compilers.html.HtmlCompiler()),
    ('plain', quichem.compilers.plain.PlainCompiler()),
    ('LaTeX', quichem.compilers.latex.LatexCompiler()),
    ('LaTeX_mhchem_V3', quichem.compilers.latex.LatexMhchemV3Compiler()),
    ('reStructuredText', quichem.compilers.rst.RstCompiler()),
))


class GenericGui(object):

    """Generic GUI for parsing and displaying output.

    Automatically handles parsing input text and updating widgets with
    parsed text.

    """

    def __init__(self):
        self.compilers = self.sources = None

    def change_value(self, value):
        """Update all displays and source widgets with the given
        unparsed text.

        """
        try:
            ast = quichem.parser.parse(value, parser)
        except ParseError as e:
            self.set_html(str(e))
            for source in self.sources:
                self.set_source(source, '')
        else:
            html = COMPILERS['HTML'].compile(ast)
            self.set_html(html)
            for compiler, source in zip(self.compilers.values(), self.sources):
                self.set_source(source, compiler.compile(ast))

    def run(self):
        """Create the compiler objects and source widgets."""
        self.compilers = collections.OrderedDict(
            (name, COMPILERS[name]) for name in parse_args().compilers)
        self.sources = [self.make_source(name) for name in self.compilers]

    def make_source(self, name):
        """Create and return a widget for displaying the source with the
        given name.

        Must be implemented in subclasses.

        """
        raise NotImplementedError

    def set_html(self, html):
        """Display the given HTML in the HTML view widget.

        Must be implemented in subclasses.

        """
        raise NotImplementedError

    def set_source(self, widget, source):
        """Display the given source in the given widget.

        Must be implemented in subclasses.

        """
        raise NotImplementedError


def parse_args():
    """Allow users to choose which parsers to load and display in the
    GUI.

    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--compilers', nargs='+', dest='compilers',
                        choices=COMPILERS.keys(), default=COMPILERS.keys(),
                        help='which compilers to enable; default is all')
    return parser.parse_args()
