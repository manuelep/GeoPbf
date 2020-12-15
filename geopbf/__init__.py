# -*- coding: utf-8 -*-

from py4web.core import Fixture, HTTP
from py4web import request, response
from mapbox_vector_tile import encode as mvt_encode
import datetime

from .geom import geom2tile


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


def prototize(func):
    """
    Warning: func must return a dictionary with at least a 'features' key.
    """
    def wrapper(x, y, z, **kwargs):
        """ """
        feat2feat = FeatToFeat(x, y, z)
        return mvt_encode(feat2feat.loop(**func(x, y, z, **kwargs)))

    return wrapper


class Protobuf(Fixture):
    """docstring for ."""

    def on_success(self, status):

        response.headers["Content-Type"]="application/x-protobuf"

        time_expire=3600
        cache_control = f'max-age={time_expire}, s-maxage={time_expire}'

        cache_control += ', public'

        expires = (datetime.datetime.utcnow() + datetime.timedelta(seconds=time_expire)).strftime('%a, %d %b %Y %H:%M:%S GMT')
        headers = {
            'Pragma': None,
            'Expires': expires,
            'Cache-Control': cache_control
        }
        response.headers.update(headers)

    # def transform(self, output, shared_data=None):
    #     """ """
    #     return mvt_encode(output)
