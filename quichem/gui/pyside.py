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

import functools

from PySide.QtCore import Qt, QMimeData
from PySide.QtGui import (QWidget, QFormLayout, QHBoxLayout, QLineEdit,
                          QApplication, QTextEdit, QSizePolicy, QVBoxLayout,
                          QPushButton, QScrollArea)
from PySide.QtWebKit import QWebView

from quichem.gui import generic


class ExpandingTextEdit(QTextEdit):

    def __init__(self, *args, **kw):
        QTextEdit.__init__(self, *args, **kw)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textChanged.connect(self.change_size)

    def change_size(self):
        self.setMinimumHeight(self.document().size().height())

    def resizeEvent(self, event):
        QTextEdit.resizeEvent(self, event)
        self.change_size()


class PysideGui(generic.GenericGui):

    def __init__(self):
        generic.GenericGui.__init__(self)
        self.window = QScrollArea()
        self.window.setWindowTitle('quichem-pyside')
        self.window.setWidgetResizable(True)
        self.widget = QWidget()
        QFormLayout(self.widget)
        self.widget.layout().setContentsMargins(*(8,) * 4)
        edit = QLineEdit()
        view_layout = QVBoxLayout()
        self.view = QWebView()
        self.view.setMinimumHeight(self.view.fontMetrics().height() * 3)
        self.view.setHtml('')
        button = QPushButton('Copy Formatted Text')
        button.setSizePolicy(*(QSizePolicy.Minimum,) * 2)
        button.clicked.connect(self.set_clipboard_html)
        view_layout.addWidget(self.view)
        view_layout.addWidget(button, alignment=Qt.AlignRight)
        self.widget.layout().addRow(edit)
        self.widget.layout().addRow(view_layout)
        edit.textChanged.connect(self.change_value)
        self.window.setWidget(self.widget)
        self.window.show()

    def make_source(self, name):
        layout = QHBoxLayout()
        layout.setContentsMargins(*(0,) * 4)
        source = ExpandingTextEdit()
        source.setStyleSheet('min-width: 0; min-height: 0')
        source.setReadOnly(True)
        button = QPushButton('Copy')
        button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
        button.clicked.connect(functools.partial(self.set_clipboard, source))
        layout.addWidget(source)
        layout.addWidget(button)
        self.widget.layout().addRow(name, layout)
        return source

    def set_html(self, html):
        self.view.setHtml(html)

    def set_source(self, widget, source):
        widget.setPlainText(source)

    def set_clipboard_html(self):
        data = QMimeData()
        data.setHtml(self.view.page().mainFrame().toHtml())
        QApplication.clipboard().setMimeData(data)

    def set_clipboard(self, source):
        QApplication.clipboard().setText(source.toPlainText())


app = QApplication(())
gui = PysideGui()
gui.run()
app.exec_()
