# FIXME:: license here

import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    'packages': ['quichem'],
     'includes': ['pyparsing', 'PySide', 'PySide.QtCore', 'PySide.QtGui'],
     'excludes': ['tkinter', 'ttk', 'socket', 'doctest', 'pdb',
                  'unittest', 'difflib', 'inspect', '_bz2',
                  '_hashlib', '_lzma', '_socket', '_ssl'],
     'optimize': True,
     'compressed': True,
     }

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

setup(name = 'quichem-pyside',
      version = '2013-02-18',
      description = 'quichem',
      options = {'build_exe': build_exe_options},
      executables = [Executable('quichem/gui/pyside.py',
                                targetName='quichem-pyside.exe',
                                base=base)])
