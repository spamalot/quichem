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
import os
import sys

from PySide.QtCore import Qt, QMimeData, QBuffer, QIODevice, QSize
from PySide.QtGui import (QWidget, QFormLayout, QHBoxLayout, QLineEdit, QImage,
                          QApplication, QTextEdit, QSizePolicy, QVBoxLayout,
                          QPushButton, QTabWidget, QFont, QStyle, QPainter,
                          QListWidget, QStackedWidget, QFrame)
from PySide.QtWebKit import QWebView, QWebPage

from quichem.gui import generic

# Load MathJax and other web files from Qt resource system.
from quichem.gui import web


class AutoSizingListWidget(QListWidget):

    """QListWidget that is as wide as the widest item it contains."""

    def sizeHint(self):
        size = QSize()
        size.setHeight(QListWidget.sizeHint(self).height())
        size.setWidth(self.sizeHintForColumn(0))
        return size


class PysideGui(generic.GenericGui):

    def __init__(self):
        generic.GenericGui.__init__(self)
        window = QWidget()
        window.setWindowTitle('quichem-pyside')

        self.compiler_view = QListWidget()
        self.compiler_view.currentRowChanged.connect(self.show_source)
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        self.edit = QLineEdit()
        self.edit.setPlaceholderText('Type quichem input...')
        self.edit.textChanged.connect(self.change_value)
        self.view = QWebView()
        self.view.page().mainFrame().setScrollBarPolicy(Qt.Vertical,
                                                        Qt.ScrollBarAlwaysOff)
        self.view.page().action(QWebPage.Reload).setVisible(False)
        self.view.setMaximumHeight(0)
        self.view.setUrl('qrc:/web/page.html')
        self.view.setZoomFactor(2)
        self.view.page().mainFrame().contentsSizeChanged.connect(
            self._resize_view)
        # For debugging JS:
        ## from PySide.QtWebKit import QWebSettings
        ## QWebSettings.globalSettings().setAttribute(
        ##     QWebSettings.DeveloperExtrasEnabled, True)

        button_image = QPushButton('Copy as Image')
        button_image.clicked.connect(self.set_clipboard_image)
        button_image.setToolTip('Then paste into any graphics program')
        button_word = QPushButton('Copy as MS Word Equation')
        button_word.clicked.connect(self.set_clipboard_word)
        button_html = QPushButton('Copy as Formatted Text')
        button_html.clicked.connect(self.set_clipboard_html)
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(button_image)
        button_layout.addWidget(button_word)
        button_layout.addWidget(button_html)
        source_layout = QHBoxLayout()
        source_layout.addWidget(self.compiler_view)
        source_layout.addWidget(self.stacked_widget, 1)
        QVBoxLayout(window)
        window.layout().addWidget(self.edit)
        window.layout().addWidget(self.view)
        window.layout().addLayout(button_layout)
        window.layout().addWidget(line)
        window.layout().addLayout(source_layout, 1)

        window.show()
        window.resize(window.minimumWidth(), window.height())
        # To prevent garbage collection of internal Qt object.
        self._window = window

    def show_source(self, index):
        if not self.sources:
            return
        self.stacked_widget.setCurrentIndex(index)
        self.change_value(self.edit.text())

    def _resize_view(self):
        """Set the QWebView's minimum height based on its current
        contents.

        """
        div = self.view.page().mainFrame().findFirstElement('.output')
        scrollbar_width = QApplication.style().pixelMetric(
            QStyle.PM_ScrollBarExtent)
        self.view.setMaximumHeight(
            div.geometry().height() + scrollbar_width + 16)

    def make_source(self, name):
        self.compiler_view.addItem(name)
        self.compiler_view.setCurrentRow(0)
        scrollbar_width = QApplication.style().pixelMetric(
            QStyle.PM_ScrollBarExtent)
        self.compiler_view.setMaximumWidth(
            self.compiler_view.sizeHintForColumn(0) + scrollbar_width + 16)
        page = QWidget()
        QHBoxLayout(page)
        page.layout().setContentsMargins(*(0,) * 4)
        source = QTextEdit()
        source.setStyleSheet('min-width: 0; min-height: 0')
        source.setReadOnly(True)
        QVBoxLayout(source)
        button = QPushButton('Copy')
        button.clicked.connect(functools.partial(self.set_clipboard, source))
        page.layout().addWidget(source)
        source.layout().addWidget(button, 0, Qt.AlignRight | Qt.AlignBottom)
        self.stacked_widget.addWidget(page)
        return source

    def run_script(self, js):
        self.view.page().mainFrame().evaluateJavaScript(js)

    def set_source(self, widget, source_factory):
        if widget.isVisible():
            widget.setPlainText(source_factory())

    def set_clipboard_image(self):
        """Export the formatted output to an image and store it in the
        clipboard.

        The image stored in the clipboard is a PNG file with alpha
        transparency.

        """
        div = self.view.page().mainFrame().findFirstElement('.output')
        images = {}
        for background in (Qt.transparent, Qt.white):
            image = QImage(div.geometry().size(),
                           QImage.Format_ARGB32_Premultiplied)
            image.fill(background)
            painter = QPainter(image)
            div.render(painter)
            painter.end()
            images[background] = image

        # Windows needs this buffer hack to get alpha transparency in
        # the copied PNG.
        buffer_ = QBuffer()
        buffer_.open(QIODevice.WriteOnly)
        images[Qt.transparent].save(buffer_, 'PNG')
        buffer_.close()
        data = QMimeData()
        data.setData('PNG', buffer_.data())
        data.setImageData(images[Qt.white])
        QApplication.clipboard().setMimeData(data)

    def set_clipboard_word(self):
        """Store the formatted output in the clipboard in a Microsoft
        Word friendly format.

        Microsoft Word interprets the clipboard contents as an
        equation. Other programs will see it as plain text containing
        XML.

        """
        QApplication.clipboard().setText(generic.word_equation_from_mathml(
            self.view.page().mainFrame().evaluateJavaScript(generic.MML_JS)))

    def set_clipboard_html(self):
        """Place the HTML displayed in the HTML view widget into the
        system clipboard.

        """
        data = QMimeData()
        data.setText(self.plain)
        data.setHtml(self.html)
        QApplication.clipboard().setMimeData(data)

    def set_clipboard(self, source):
        """Place the text displayed in the given source widget into the
        system clipboard.

        """
        QApplication.clipboard().setText(source.toPlainText())


def main():
    app = QApplication(())
    gui = PysideGui()
    gui.run()
    app.exec_()


if __name__ == '__main__':
    main()
