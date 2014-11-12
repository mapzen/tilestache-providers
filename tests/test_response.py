from StringIO import StringIO
import unittest


class StubOpener(object):

    def __init__(self, input):
        self.input = input

    def open(self, url, timeout=None):
        self.url = url
        self.timeout = timeout
        return StringIO(self.input)


def make_stub_opener(stub):
    return lambda: stub


class TestProxyTile(unittest.TestCase):

    def _instance(self, *args, **kwargs):
        from mapzen.provider.proxy import ProxyTile
        return ProxyTile(*args, **kwargs)

    def _makeone(self, url=None, timeout=None, stub_opener=None):
        if url is None:
            url = 'http://127.0.0.1/'
        proxy_tile = self._instance(url, timeout)
        if stub_opener is None:
            stub_opener = StubOpener('tile data')
        proxy_tile.make_url_opener = make_stub_opener(stub_opener)
        return proxy_tile

    def test_create(self):
        proxy_tile = self._makeone()
        self.failUnless(proxy_tile is not None)

    def test_save_invalid_format(self):
        proxy_tile = self._makeone()
        try:
            proxy_tile.save(None, 'unknown-format')
        except Exception:
            pass
        else:
            self.fail('Expected an exception to be thrown')

    def test_save(self):
        input_data = 'tile data'
        url = 'http://127.0.0.1/foo.${format}'
        timeout = 2
        stub = StubOpener(input_data)
        proxy_tile = self._makeone(url, timeout, stub)

        buf = StringIO()
        proxy_tile.save(buf, 'JSON')

        self.assertEqual(input_data, buf.getvalue())
        # stub saves arguments when called
        self.assertEqual('http://127.0.0.1/foo.json', stub.url)
        self.assertEqual(timeout, stub.timeout)
