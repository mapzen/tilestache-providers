[![Circle CI](https://circleci.com/gh/mapzen/tilestache-providers/tree/master.png?style=badge)](https://circleci.com/gh/mapzen/tilestache-providers/tree/master)

# Tilestache Providers

This will hold Mapzen specific Tilestache providers. Hopefully this will
eventually obviate the need for a fork of Tilestache.

## Providers

### Proxy

Although Tilestache contains a proxy provider, it expects to receive an image
response. This proxy provider expects that the response is already formatted,
and simply writes that back out directly.

#### Sample Configuration

    "all": {
      "allowed origin": "*",
      "provider": {
        "class": "mapzen.providers:Proxy",
        "kwargs": {
          "url": "http://127.0.0.1:8080/all/{Z}/{X}/{Y}.${format}"
        }
      }
    }
