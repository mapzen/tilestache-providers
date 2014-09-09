from mapzen.mimetypes import lookup_mimetype
from mapzen.response import ProxyTile
from ModestMaps.Providers import TemplatedMercatorProvider
import urllib2

class Proxy(object):

    def __init__(self, layer, url=None, timeout=None):
        assert url is not None, 'Proxy url configuration required'
        self.layer = layer
        self.provider = TemplatedMercatorProvider(url)
        self.timeout = timeout

    def getTypeByExtension(self, extension):
        mime_type = lookup_mimetype(extension.lower())
        if mime_type is None:
            raise ValueError('Cannot find mime type for extension: ' +
                             extension)
        return mime_type

    def renderTile(self, width, height, srs, coord):
        urls = self.provider.getTileUrls(coord)
        assert len(urls) == 1, 'Unexpected number of urls'
        url = urls[0]
        return ProxyTile(url, self.timeout)
