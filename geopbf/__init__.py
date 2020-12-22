# -*- coding: utf-8 -*-

from py4web.core import Fixture, HTTP
from py4web import request, response
from mapbox_vector_tile import encode as mvt_encode
import datetime

from kilimanjaro.frameworks.py4web.controller import WebWrapper

from .geom import geom2tile
from .hashit import hashit

class FeatToFeat(object):
    """ """

    type = 3

    def __init__(self, x, y, z):
        super(FeatToFeat, self).__init__()
        self.x = x
        self.y = y
        self.z = z

    def __call__(self, id, geometry, properties, type):
        assert type=='Feature'
        return dict(
            id=id, properties=properties, type=self.type,
            geometry = geom2tile(self.x, self.y, self.z, geometry)
        )

    def loop(self, features, name='mytiles'):
        return dict(
            name = name,
            features = list(map(lambda feat: self(**feat), features))
        )

def f2f(func):
    def wrapper(x, y, z, *args, **kwargs):
        feat2feat = FeatToFeat(x, y, z)
        return feat2feat.loop(**func(x, y, z, *args, **kwargs))
    return wrapper


class Prototizer(WebWrapper):
    """docstring for Prototizer."""

    EXT = '.pbf'

    def _hash(self, func, *args, **kwargs):
        return "{}.{}".format(*map(hashit, [
            (func.__module__, func.__name__,)+args,
            kwargs
        ]))

    # def on_request(self):
    #     """ called when a request arrives """
    #
    #     self.params = {}
    #     # self.now = now()
    #     # self.public = (db.fcache.file.uploadfolder == settings.STATIC_UPLOAD_FOLDER)

    def on_success(self, status):
        """ """
        response.headers["Content-Type"]="application/x-protobuf"
        response.headers["Content-Disposition"] = f'inline; filename="{self.filename}"'

    def __call__(self, func, **defaults):
        """
        func @callable : A function that returns a dictionary with a mandatory 'features' key
            and an optional 'name' key
        Returns a wrapper function, it's intended as a decorator.
        """
        kwargs = self.parse_request(func, **defaults)
        name = self._hash(func, **kwargs)
        self.filename = f"{name}{self.EXT}"
        wrapper = lambda : mvt_encode(WebWrapper.__call__(self, f2f(func), **defaults)())
        return wrapper

    # def transform(self, output, shared_data=None):
    #     """ """
    #     return mvt_encode(output)
