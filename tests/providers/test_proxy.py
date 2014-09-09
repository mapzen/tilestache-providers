import unittest

class TestProxy(unittest.TestCase):

    srs = '+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext +no_defs +over'

    def _instance(self, *args, **kwargs):
        from mapzen.providers import Proxy
        return Proxy(*args, **kwargs)

    def _makeone(self):
        return self._instance(None, url='http://127.0.0.1/')

    def test_no_url(self):
        try:
            self._instance(None)
        except AssertionError:
            pass
        else:
            self.fail('Expected an AssertionError to be thrown')

    def test_creation(self):
        proxy = self._makeone()

    def test_known_extension_json(self):
        proxy = self._makeone()
        mime_type = proxy.getTypeByExtension('json')
        self.assertEqual('application/json', mime_type[0])
        self.assertEqual('JSON', mime_type[1])

    def test_known_extension_vtm(self):
        proxy = self._makeone()
        mime_type = proxy.getTypeByExtension('vtm')
        self.assertEqual('image/png', mime_type[0])
        self.assertEqual('OpenScienceMap', mime_type[1])

    def test_render(self):
        from ModestMaps.Core import Coordinate
        proxy = self._makeone()
        tile = proxy.renderTile(256, 256, self.srs, Coordinate(1, 1, 1))
        self.assertIsNotNone(tile)
        self.failUnless(hasattr(tile, 'save'))
