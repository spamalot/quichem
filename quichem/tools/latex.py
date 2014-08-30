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

"""Used by the LaTeX ``quichem`` package to generate LaTeX code to
render chemical equations.

Takes one argument from the command line and outputs the LaTeX
``mhchem`` code to stdout.

    $ python -m quichem.tools.latex h==oh-
    \ce{H^+ + OH^-}

"""

from __future__ import absolute_import, print_function

import os
import sys

from modgrammar import ParseError

import quichem.parser
import quichem.compilers.latex


def main():
    if len(sys.argv) == 1:
        print('Congratulations! Your quichem installation is set up with '
              'LaTeX support.')
        return
    compiler = quichem.compilers.latex.LatexMhchemV3Compiler()
    parser = quichem.parser.make_parser()
    try:
        print(compiler.compile(quichem.parser.parse(sys.argv[1], parser)))
    except ParseError as e:
        print((r"\PackageError{{quichem}}{{ \protect {} }}{{"
               r"I don't know what to do with \protect {}}}").format(
                   e, sys.argv[1]))


if __name__ == '__main__':
    main()
