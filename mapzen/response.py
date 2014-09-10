from mapzen.mimetypes import lookup_extension
from string import Template
import urllib2

def make_url_opener(cls):
    return urllib2.build_opener(urllib2.ProxyHandler({}))

class ProxyTile(object):

    bufsize = 8192

    # for tests
    make_url_opener = make_url_opener

    def __init__(self, url, timeout=None):
        self.url = url
        self.timeout = timeout

    def save(self, out, format):
        extension = lookup_extension(format)
        if extension is None:
            raise Exception('You can\'t fool me twice!')
        url = Template(self.url).substitute(dict(format=extension))

        # we want a separate instance of the url opener every time
        url_opener = self.make_url_opener()
        url_fp = url_opener.open(url, timeout=self.timeout)

        while True:
            data = url_fp.read(self.bufsize)
            if not data:
                break
            out.write(data)
