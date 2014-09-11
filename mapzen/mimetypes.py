extension_to_mime = dict(
    json = ('application/json', 'JSON'),
    vtm = ('image/png', 'OpenScienceMap'),
    topojson = ('application/json', 'TopoJSON'),
    mapbox = ('image/png', 'Mapbox'),
    )

def lookup_mimetype(extension):
    return extension_to_mime.get(extension)

def lookup_mimetype_from_format_name(format_name):
    for extension, (mime, format) in extension_to_mime.items():
        if format == format_name:
            return mime
    return None

def lookup_extension(format_name):
    for extension, (mime, format) in extension_to_mime.items():
        if format == format_name:
            return extension
    return None
