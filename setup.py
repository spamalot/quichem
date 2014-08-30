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

import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages


setup(
    name = 'quichem',
    version = '2014-03-28',
    packages = find_packages(exclude=['tests']),
    description = ('Parser and utilities for extremely fast input of chemical '
                   'formulae and equations.'),
    license = 'LGPLv3',
    keywords = 'chemistry chemical formula equation input parse',
    classifiers = [
        'Topic :: Scientific/Engineering :: Chemistry',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Development Status :: 5 - Production/Stable',
    ],
    url = 'http://github.com/spamalot/quichem',
    test_suite = 'tests',
    ## install_requires = ['modgrammar>=0.10'],
    extras_require = {
        'pyside':  [],  ## 'PySide>=1.1.1'
        ## 'wxpython': [...],
    },
    entry_points = {
        'console_scripts': [
            'quichem-latex-tool = quichem.tools.latex:main',
        ],
        'gui_scripts': [
            'quichem-pyside = quichem.gui.pyside:main [pyside]',
            ## 'quichem-wxpython = quichem.gui.wxpython:main [wxpython]',
        ],
    },
)
