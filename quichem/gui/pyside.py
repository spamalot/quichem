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

from pyparsing import ParseException

import quichem.parser
import quichem.compilers.html
import quichem.compilers.plain
import quichem.compilers.latex
import quichem.compilers.rst


parser = quichem.parser.parser_factory()
html_compiler = quichem.compilers.html.HtmlCompiler()
plain_compiler = quichem.compilers.plain.PlainCompiler()
latex_compiler = quichem.compilers.latex.LatexCompiler()
rst_compiler = quichem.compilers.rst.RstCompiler()


def on_value_change(val):
    try:
        ast = parser.parseString(val)
    except ParseException as e:
        view.setHtml(str(e))
        for source in (html_source, plain_source, latex_source, rst_source):
            source.setPlainText('')
    else:
        html = html_compiler.compile(ast)
        view.setHtml(html)
        html_source.setPlainText(html)
        plain_source.setPlainText(plain_compiler.compile(ast))
        latex_source.setPlainText(latex_compiler.compile(ast))
        rst_source.setPlainText(rst_compiler.compile(ast))


from PySide.QtGui import (QWidget, QVBoxLayout, QLineEdit, QApplication,
                          QPlainTextEdit, QSizePolicy)
from PySide.QtWebKit import QWebView
app = QApplication(())
w = QWidget()
l = QVBoxLayout()
w.setLayout(l)
edit = QLineEdit()
view = QWebView()
view.setHtml('')
html_source = QPlainTextEdit()
plain_source = QPlainTextEdit()
latex_source = QPlainTextEdit()
rst_source = QPlainTextEdit()
l.addWidget(edit)
l.addWidget(view)
l.addWidget(html_source)
l.addWidget(plain_source)
l.addWidget(latex_source)
l.addWidget(rst_source)
edit.textChanged.connect(on_value_change)
w.resize(500, 436)
w.show()
app.exec_()
