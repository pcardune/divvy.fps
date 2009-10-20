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

