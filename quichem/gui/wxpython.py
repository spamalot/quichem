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

import wx
import wx.html
import wx.lib.expando

from quichem.gui import generic


class WxpythonGui(generic.GenericGui):

    def __init__(self):
        generic.GenericGui.__init__(self)
        self.window = wx.Frame(None, -1, 'quichem-wxpython')
        self.window.SetBackgroundColour(wx.NullColour)
        self.scroll_area = wx.ScrolledWindow(self.window)
        self.scroll_area.SetScrollbars(1, 1, 1, 1)
        self.scroll_area.SetScrollRate(16, 16)
        self.layout = wx.BoxSizer(wx.VERTICAL)
        self.grid_layout = wx.FlexGridSizer(len(generic.COMPILERS), 3, 8, 12)
        self.grid_layout.AddGrowableCol(1)
        self.scroll_area.SetSizer(self.layout)
        edit = wx.TextCtrl(self.scroll_area)
        edit.Bind(wx.EVT_TEXT, self.change_value_from_event)
        self.view = wx.html.HtmlWindow(self.scroll_area)
        self.view.SetFonts('times new roman', '')
        self.view.SetMinSize((1, self.view.GetCharHeight() * 4))
        button = wx.Button(self.scroll_area, label='Copy Formatted Text')
        button.Disable()  # Until we can add HTML data to clipboard
        button.Bind(wx.EVT_BUTTON, self.set_clipboard_html)
        self.layout.Add(edit, flag=wx.EXPAND | wx.ALL, border=8)
        self.layout.Add(self.view, 1, flag=wx.EXPAND | wx.ALL, border=8)
        self.layout.Add(button, flag=wx.ALIGN_RIGHT | wx.RIGHT, border=8)
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

    def set_html(self, html):
        self.view.SetPage(html)

    def set_source(self, widget, source):
        widget.SetValue(source)

    def set_clipboard_html(self, event):
        # FIXME: This only works on Windows ANSI builds of wxPython.
        # Ideally we want support on all wxPython builds on all OSs.
        data = wx.DataObjectSimple(wx.DataFormat(wx.DF_HTML))
        data.SetData(bytes(self.view.GetParser().GetSource()))
        wx.TheClipboard.Open()
        wx.TheClipboard.SetData(data)
        wx.TheClipboard.Close()

    def set_clipboard(self, source, event):
        data = wx.TextDataObject()
        data.SetText(source.GetValue())
        wx.TheClipboard.Open()
        wx.TheClipboard.SetData(data)
        wx.TheClipboard.Close()


app = wx.App(redirect=False)
gui = WxpythonGui()
gui.run()
app.MainLoop()
