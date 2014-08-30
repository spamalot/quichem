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

import sys
from cx_Freeze import setup, Executable

sys.path.insert(0, '../..')

build_exe_options = {
    'packages': ['quichem'],
     'includes': ['modgrammar', 'PySide', 'PySide.QtCore', 'PySide.QtGui'],
     'excludes': ['tkinter', 'ttk', 'wx', 'socket', 'doctest', 'pdb',
                  'unittest', 'difflib', 'inspect', '_bz2',
                  '_hashlib', '_lzma', '_socket', '_ssl'],
     'optimize': True,
     'compressed': True,
     }

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

setup(name='quichem-pyside',
      version='2013-02-18',
      description='quichem',
      options={'build_exe': build_exe_options},
      executables=[Executable('../../quichem/gui/pyside.py',
                              targetName='quichem-pyside.exe',
                              base=base)])
