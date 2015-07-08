import os


def tile_parentdir(base, coord):
    location = os.path.join(base, str(coord.zoom), str(coord.column))
    return location


def tile_location(base, coord, extension):
    parent = tile_parentdir(base, coord)
    location = os.path.join(parent, '%s.%s' % (coord.row, extension))
    return location


class Filesystem(object):

    def __init__(self, basepath):
        assert basepath is not None
        assert os.path.isdir(basepath)
        self.basepath = basepath

    def lock(self, layer, coord, format):
        pass

    def unlock(self, layer, coord, format):
        pass

    def remove(self, layer, coord, format):
        loc = tile_location(self.basepath, coord, format)
        try:
            os.remove(loc)
        except OSError:
            pass

    def read(self, layer, coord, format):
        loc = tile_location(self.basepath, coord, format)
        try:
            with open(loc, 'rb') as fp:
                data = fp.read()
                return data
        except Exception:
            return None

    def save(self, body, layer, coord, format):
        parent = tile_parentdir(self.basepath, coord)
        loc = tile_location(self.basepath, coord, format)
        try:
            os.makedirs(parent)
        except OSError:
            pass
        with open(loc, 'wb') as fp:
            fp.write(body)
