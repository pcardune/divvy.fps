import os
import sys
import urlparse
import cgi

def get_stub_file(fn):
    return os.path.join(os.path.dirname(__file__),"tests","stubs",fn)

class MockUrllib2(object):
    """Mock interface to urllib2 library."""
    stub_action_map = {
        'Pay':get_stub_file("PayResponse.xml")
        }

    mocked = None

    old_urlopen = None
    @classmethod
    def mock_urlopen(cls, url):
        parsed = urlparse.urlparse(url)
        qs = cgi.parse_qs(parsed.query)
        action = qs['Action'][0]
        return open(cls.stub_action_map[action])

    @classmethod
    def get_mocks(cls):
        return [(fname[5:], getattr(cls, fname)) for fname in dir(cls)
                if fname.startswith('mock_')]

    @staticmethod
    def install():
        if MockUrllib2.mocked is not None:
            return
        import urllib2
        MockUrllib2.mocked = MockUrllib2()

        for fname, f in MockUrllib2.get_mocks():
            setattr(MockUrllib2.mocked, "old_"+fname, getattr(urllib2, fname))
            setattr(urllib2, fname, f)

    @staticmethod
    def uninstall():
        if MockUrllib2.mocked is None:
            return
        import urllib2
        for fname, f in MockUrllib2.get_mocks():
            setattr(urllib2, fname, getattr(MockUrllib2.mocked, "old_"+fname))
            setattr(MockUrllib2.mocked, "old_"+fname, None)

        MockUrllib2.mocked = None
