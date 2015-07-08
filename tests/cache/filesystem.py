import unittest


class TestFilesysteCache(unittest.TestCase):

    def _makeone(self, basepath):
        from mapzen.cache import Filesystem
        return Filesystem(basepath)

    def _tmppath(self):
        import tempfile
        tmppath = tempfile.mkdtemp()
        return tmppath

    def _removepath(self, path):
        import shutil
        shutil.rmtree(path)

    def test_save(self):
        from ModestMaps.Core import Coordinate
        import os
        tmppath = self._tmppath()
        fs_cache = self._makeone(tmppath)
        coord = Coordinate(1, 1, 1)
        ext = 'json'
        data = 'foo'
        layer = 'unused'
        fs_cache.save(data, layer, coord, ext)
        exp_path = os.path.join(
            tmppath, str(coord.zoom), str(coord.column),
            '%s.%s' % (coord.row, ext))
        self.failUnless(os.path.exists(exp_path))
        with open(exp_path) as fp:
            cache_data = fp.read()
        self.assertEqual(data, cache_data)
        self._removepath(tmppath)

    def test_read_exists(self):
        from ModestMaps.Core import Coordinate
        import os
        tmppath = self._tmppath()
        fs_cache = self._makeone(tmppath)
        coord = Coordinate(1, 1, 1)
        ext = 'json'
        data = 'foo'
        layer = 'unused'
        os.makedirs(os.path.join(tmppath, str(coord.zoom), str(coord.column)))
        exp_path = os.path.join(
            tmppath, str(coord.zoom), str(coord.column),
            '%s.%s' % (coord.row, ext))
        with open(exp_path, 'w') as fp:
            fp.write(data)
        cache_data = fs_cache.read(layer, coord, ext)
        self.assertEqual(data, cache_data)
        self._removepath(tmppath)

    def test_read_not_exists(self):
        from ModestMaps.Core import Coordinate
        tmppath = self._tmppath()
        fs_cache = self._makeone(tmppath)
        coord = Coordinate(1, 1, 1)
        ext = 'json'
        layer = 'unused'
        cache_data = fs_cache.read(layer, coord, ext)
        self.failUnless(cache_data is None)
        self._removepath(tmppath)

    def test_remove_exists(self):
        from ModestMaps.Core import Coordinate
        import os
        tmppath = self._tmppath()
        fs_cache = self._makeone(tmppath)
        coord = Coordinate(1, 1, 1)
        ext = 'json'
        data = 'foo'
        layer = 'unused'
        os.makedirs(os.path.join(tmppath, str(coord.zoom), str(coord.column)))
        exp_path = os.path.join(
            tmppath, str(coord.zoom), str(coord.column),
            '%s.%s' % (coord.row, ext))
        with open(exp_path, 'w') as fp:
            fp.write(data)
        fs_cache.remove(layer, coord, ext)
        self.failIf(os.path.exists(exp_path))
        self._removepath(tmppath)

    def test_remove_not_exists(self):
        from ModestMaps.Core import Coordinate
        import os
        tmppath = self._tmppath()
        fs_cache = self._makeone(tmppath)
        coord = Coordinate(1, 1, 1)
        ext = 'json'
        layer = 'unused'
        exp_path = os.path.join(
            tmppath, str(coord.zoom), str(coord.column),
            '%s.%s' % (coord.row, ext))
        fs_cache.remove(layer, coord, ext)
        self.failIf(os.path.exists(exp_path))
        self._removepath(tmppath)
