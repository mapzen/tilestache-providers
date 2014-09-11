from cStringIO import StringIO
from gzip import GzipFile
from mapzen.mimetypes import lookup_mimetype_from_format_name
from TileStache.Core import TheTileLeftANote
from TileStache.S3 import Cache as TilestacheS3Cache
from TileStache.S3 import tile_key
from wsgiref.headers import Headers

class S3(object):

    def __init__(self, bucket=None, access=None, secret=None, use_locks=True, path='', reduced_redundancy=False, gzip_formats=None):
        assert bucket is not None
        assert access is not None
        assert secret is not None

        self.tilestache_s3_cache = TilestacheS3Cache(bucket, access, secret, use_locks, path, reduced_redundancy)
        if gzip_formats is None:
            gzip_formats = ()
        self.gzip_formats = set(gzip_formats)

    def lock(self, layer, coord, format):
        if not self.tilestache_s3_cache.use_locks:
            return
        return self.tilestache_s3_cache.lock(layer, coord, format)

    def unlock(self, layer, coord, format):
        if not self.tilestache_s3_cache.use_locks:
            return
        return self.tilestache_s3_cache.unlock(layer, coord, format)

    def remove(self, layer, coord, format):
        return self.tilestache_s3_cache.remove(layer, coord, format)

    def read(self, layer, coord, format):
        key_name = tile_key(layer, coord, format, self.tilestache_s3_cache.path)
        key = self.tilestache_s3_cache.bucket.get_key(key_name)

        if key is None:
            return None

        out = StringIO()
        key.get_file(out)

        if format.lower() in self.gzip_formats:
            out.seek(0)
            with GzipFile(mode='rb', fileobj=out) as gz_stream:
                content = gz_stream.read()
        else:
            content = out.getvalue()

        mimetype = lookup_mimetype_from_format_name(format) or \
                'application/octet-stream'
        headers = Headers([
            ('Content-Type', mimetype),
            ('Last-Modified', key.last_modified),
            ('Etag', key.etag),
            ])

        raise TheTileLeftANote(headers=headers, content=content)

    def save(self, body, layer, coord, format):
        key_name = tile_key(layer, coord, format, self.tilestache_s3_cache.path)
        key = self.tilestache_s3_cache.bucket.new_key(key_name)

        out = StringIO()
        if format.lower() in self.gzip_formats:
            mimetype = 'application/x-gzip'
            with GzipFile(mode='wb', fileobj=out, compresslevel=9) as gzip_out:
                gzip_out.write(body)
        else:
            mimetype = lookup_mimetype_from_format_name(format) or \
                    'application/octet-stream'
            out.write(body)

        headers = {'Content-Type': mimetype}
        out.seek(0)

        key.set_contents_from_file(
                out,
                headers=headers,
                policy='public-read',
                reduced_redundancy=self.tilestache_s3_cache.reduced_redundancy,
                )
