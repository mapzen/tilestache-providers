from mapzen.mimetypes import lookup_extension
from string import Template
import urllib2

class ProxyTile(object):

    def __init__(self, url, timeout):
        self.url = url
        self.timeout = timeout
        self.bufsize = 8192

    def save(self, out, format):
        extension = lookup_extension(format)
        if extension is None:
            raise Exception('You can\'t fool me twice!')
        url = Template(self.url).substitute(dict(format=extension))

        url_opener = urllib2.build_opener(urllib2.ProxyHandler({}))
        url_fp = url_opener.open(url, timeout=self.timeout)

        while True:
            data = url_fp.read(self.bufsize)
            if not data:
                break
            out.write(data)
