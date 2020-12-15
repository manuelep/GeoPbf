# -*- coding: utf-8 -*-

from pyproj import Transformer
from shapely.geometry import shape, mapping
from shapely.ops import transform
from shapely.affinity import translate, scale, rotate
from shapely import wkt # , wkb
import mercantile
transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)

def merc2xy(x, y, z, sgeom):
    """ Apply some affine transformations to input shapely geometry for coordinates
    transformation from Mercatore to local tile pixels.

    sgeom @shapely.geom : Input polygon

    Returns a brand new shapely polygon in the new coordinates.
    """

    MVT_EXTENT = 4096

    X_min, Y_max = mercantile.xy(*mercantile.ul(x, y, z))
    X_max, Y_min = mercantile.xy(*mercantile.ul(x+1, y-1, z))

    geom_3857 = transform(transformer.transform, sgeom)
    tx, ty = -X_min, -2*Y_max+Y_min
    geom_XY = translate(geom_3857, tx, ty)
    x_scale_factor = MVT_EXTENT/(X_max-X_min)
    y_scale_factor = -MVT_EXTENT/(Y_max-Y_min)
    geom_xy = scale(geom_XY, x_scale_factor, y_scale_factor, origin=(0,0,0))
    return geom_xy

def geom2tile(x, y, z, geom):
    """ """
    geom_xy = merc2xy(x, y, z, shape(geom))
    # Courtesy of: https://gis.stackexchange.com/a/276512
    as_json = mapping(wkt.loads(wkt.dumps(geom_xy, rounding_precision=0)).simplify(0))
    return as_json
