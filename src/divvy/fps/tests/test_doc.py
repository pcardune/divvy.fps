########################################################################
# Copyright (c) 2009 Paul Carduner and Contributors
# All Rights Reserved
# This file is part of divvy.fps.
#
# divvy.fps is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# divvy.fps is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with divvy.fps.  If not, see
# <http://www.gnu.org/licenses/>.
#########################################################################

import doctest
import os
import unittest
from doctest import NORMALIZE_WHITESPACE, ELLIPSIS
from divvy.fps import testing, conf

def get_stub_file(fn):
    return os.path.join(os.path.dirname(__file__),"stubs",fn)

def setup_readme(test):
    testing.MockUrllib2.install()
    conf.DEFAULT_COBRANDING_URL = None

def teardown_readme(test):
    testing.MockUrllib2.uninstall()

def test_suite():
    return unittest.TestSuite([
            doctest.DocFileSuite("../README.txt",
                                 optionflags=NORMALIZE_WHITESPACE | ELLIPSIS,
                                 setUp=setup_readme,
                                 tearDown=teardown_readme),
            ])

