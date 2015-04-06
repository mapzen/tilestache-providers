from mapzen.util import is_valid


class Notifier(object):

    def __init__(self, cache, on_save):
        self.cache = cache
        self.on_save = on_save

    def lock(self, layer, coord, format):
        return self.cache.lock(layer, coord, format)

    def unlock(self, layer, coord, format):
        return self.cache.unlock(layer, coord, format)

    def remove(self, layer, coord, format):
        return self.cache.remove(layer, coord, format)

    def read(self, layer, coord, format):
        return self.cache.read(layer, coord, format)

    def save(self, body, layer, coord, format):
        # if we received a request for an invalid coordinate, don't
        # cache or notify it
        if not is_valid(coord):
            return None
        result = self.cache.save(body, layer, coord, format)
        data = dict(
            body=body,
            layer=layer,
            coord=coord,
            format=format,
            )
        self.on_save(data)
        return result
