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
import re
import sys
import os
import html

from modgrammar import ParseError

import quichem.parser
import quichem.compilers.html
import quichem.compilers.plain
import quichem.compilers.latex
import quichem.compilers.rst


parser = quichem.parser.make_parser()
COMPILERS = collections.OrderedDict((
    ('plain', quichem.compilers.plain.PlainCompiler()),
    ('LaTeX_mhchem_V3', quichem.compilers.latex.LatexMhchemV3Compiler()),
    ('HTML', quichem.compilers.html.HtmlCompiler()),
    ('plain_ASCII', quichem.compilers.plain.PlainAsciiCompiler()),
    ('LaTeX', quichem.compilers.latex.LatexCompiler()),
    ('reStructuredText', quichem.compilers.rst.RstCompiler()),
))
MML_JS = 'MathJax.Hub.getAllJax("output")[0].root.toMathML("")'


class GenericGui(object):

    """GUI base for parsing and displaying output.

    Not tied to any particular GUI toolkit. Automatically handles
    parsing input text and updating widgets with parsed text.

    """

    def __init__(self):
        self.compilers = {}
        self.sources = []
        self._ast = None

    def _set_latex(self, latex):
        """Set the LaTeX code for MathJax to display in the formatted
        output view.

        `latex` should not contain the open or close delimiters.

        """
        # Chop out open & close delimiters; format for passing to
        # JavaScript.
        self.run_script('update("{}")'.format(
            re.escape(re.sub(r'^\\\(|\\\)$', '', latex))))

    @property
    def html(self):
        if self._ast is None:
            return html.escape(str(e))
        return COMPILERS['HTML'].compile(self._ast)

    @property
    def plain(self):
        if self._ast is None:
            return e
        return COMPILERS['plain'].compile(self._ast)

    def change_value(self, value):
        """Update all displays and source widgets with the given
        unparsed text.

        """
        try:
            self._ast = quichem.parser.parse(value, parser)
        except ParseError as e:
            self._ast = None
            self._set_latex(r'\text{{{}}}'.format(e))
            for source in self.sources:
                self.set_source(source, lambda: '')
        else:
            self._set_latex(COMPILERS['LaTeX'].compile(self._ast))
            for compiler, source in zip(self.compilers.values(), self.sources):
                self.set_source(source, lambda: compiler.compile(self._ast))

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

    def run_script(self, js):
        """Run the given JavaScript code using the JavaScript console
        of the embedded web view.

        Must be implemented in subclasses.

        """
        raise NotImplementedError

    def set_source(self, widget, source):
        """Display the given source in the given widget.

        Must be implemented in subclasses.

        """
        raise NotImplementedError


def word_equation_from_mathml(mathml):
    # Replace empty boxes with zero-width spaces.
    # Confuse Word into thinking this is an equation.
    return ('<?xml version="1.0"?>\n' +
            re.sub(r'(?<=<mrow class="MJX-TeXAtom-ORD">)\s*(?=</mrow>)',
                   '<mo>&#x180e;</mo>', mathml))


def data_file(filename):
    # Taken from:
    #     http://cx-freeze.readthedocs.org/en/latest/faq.html#using-data-files
    if getattr(sys, 'frozen', False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        datadir = os.getcwd()
    return os.path.abspath(os.path.join(datadir, filename))


def parse_args():
    """Allow users to choose which parsers to load and display in the
    GUI.

    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--compilers', nargs='+', dest='compilers',
                        choices=COMPILERS.keys(), default=COMPILERS.keys(),
                        help='which compilers to enable; default is all')
    return parser.parse_args()
