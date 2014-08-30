## This file is part of quichem.
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

import wx
import wx.html2
import wx.lib.expando
import wx.lib.scrolledpanel

from quichem.gui import generic


class _TextDataObject(wx.DataObjectSimple):

    """Hack around Phoenix's currently broken implementation of
    wx.TextDataObject.

    """

    def __init__(self, text=''):
        wx.DataObjectSimple.__init__(self, wx.DataFormat(wx.DF_TEXT))
        self.value = (text + '\0').encode('utf8')

    def GetDataSize(self):
        return len(self.value)

    def GetDataHere(self, buffer_):
        buffer_[:] = self.value
        return True


class ScrolledPanel(wx.lib.scrolledpanel.ScrolledPanel):

    """A wxPython ScrolledPanel that repaints whenever it is resized.

    This prevents tearing from occurring.

    """

    def __init__(self, *args, **kw):
        wx.lib.scrolledpanel.ScrolledPanel.__init__(self, *args, **kw)
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def OnSize(self, event):
        self.Refresh()
        event.Skip()


class WxpythonGui(generic.GenericGui):

    def __init__(self):
        generic.GenericGui.__init__(self)
        self.window = wx.Frame(None, -1, 'quichem-wxpython')
        # self.window.SetBackgroundColour(wx.NullColour)
        self.scroll_area = ScrolledPanel(self.window)
        self.scroll_area.SetScrollbars(1, 1, 1, 1)
        self.scroll_area.SetScrollRate(16, 16)
        self.layout = wx.BoxSizer(wx.VERTICAL)
        self.grid_layout = wx.FlexGridSizer(len(generic.COMPILERS), 3, 8, 12)
        self.grid_layout.AddGrowableCol(1)
        self.scroll_area.SetSizer(self.layout)
        edit = wx.TextCtrl(self.scroll_area)
        edit.Bind(wx.EVT_TEXT, self.change_value_from_event)
        self.view = wx.html2.WebView.New(self.scroll_area)
        self.view.LoadURL('file://' + generic.data_file('web/page.html'))
        self.view.SetMinSize((1, self.view.GetCharHeight() * 4))
        # Currently no simple way to export div as image.
        ## button_image = wx.Button(self.scroll_area, label='Copy as Image')
        button_word = wx.Button(self.scroll_area,
                                label='Copy as MS Word Equation')
        # Currently no way to export rich text to clipboard with wx.
        ## button_html = wx.Button(self.scroll_area,
        ##                         label='Copy as Formatted Text')
        button_word.Bind(wx.EVT_BUTTON, self.set_clipboard_word)
        self.layout.Add(edit, flag=wx.EXPAND | wx.ALL, border=8)
        self.layout.Add(self.view, 1, flag=wx.EXPAND | wx.ALL, border=8)
        self.layout.Add(button_word, flag=wx.ALIGN_RIGHT | wx.RIGHT, border=8)
        self.layout.Add(self.grid_layout, 0, flag=wx.EXPAND | wx.ALL, border=8)
        self.window.Show(True)

    def change_value_from_event(self, event):
        self.change_value(event.GetString())
        self.scroll_area.FitInside()

    def make_source(self, name):
        label = wx.StaticText(self.scroll_area, label=name)
        source = wx.lib.expando.ExpandoTextCtrl(
            self.scroll_area, style=wx.TE_READONLY | wx.TE_MULTILINE)
        button = wx.Button(self.scroll_area, label='Copy')
        button.Bind(wx.EVT_BUTTON, functools.partial(self.set_clipboard,
                                                     source))
        self.grid_layout.AddMany([(label,), (source, 1, wx.EXPAND),
                                  (button, 1, wx.EXPAND)])
        self.scroll_area.Layout()
        return source

    def run_script(self, js):
        self.view.RunScript(js)

    def set_source(self, widget, source_factory):
        widget.SetValue(source_factory())

    def set_clipboard_word(self, event):
        """Store the formatted output in the clipboard in a Microsoft
        Word friendly format.

        Microsoft Word interprets the clipboard contents as an
        equation. Other programs will see it as plain text containing
        XML.

        Note
        ----
        Currently, wx has no way of obtaining returned results from
        JavaScript functions. In order to do this, any data that needs
        to be read from the page is stored in the page title, which
        is accessible from wx. This is a hack that will be changed
        when wx implements the required functionality.

        """
        self.view.RunScript("document.title = {}".format(generic.MML_JS))
        mml = generic.word_equation_from_mathml(self.view.GetCurrentTitle())
        print(mml.encode('utf-8'))
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(_TextDataObject(mml))
            wx.TheClipboard.Close()

    def set_clipboard(self, source, event):
        """Place the text displayed in the given source widget into the
        system clipboard.

        """
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(_TextDataObject(source.GetValue()))
            wx.TheClipboard.Close()


def main():
    app = wx.App(redirect=False)
    gui = WxpythonGui()
    gui.run()
    app.MainLoop()


if __name__ == '__main__':
    main()
