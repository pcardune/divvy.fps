import unittest
from divvy.fps import util

class UtilTestCase(unittest.TestCase):
    def test_query_string(self):
        self.assertEquals(util.query_string(dict(foo="bar", one=1, two=None)),
                          '?foo=bar&one=1')

    def test_signature(self):
        self.assertEquals(util.get_signature("secret_key", dict(foo="bar", one=1)),
                          'XtaSKfYnpyaQqfjL6mqX2Gow+Y0=')


#?signature=cfWBevnG0GSKzwHgZsixvDUy8cw%3D&expiry=03%2F2015&tokenID=DSLR1R6I9BB6H1C9PI3L7BKINICYDJW4J3LHTBEK7831QF5M1T77ML5ABCEVLAFI&status=SC&callerReference=foo
