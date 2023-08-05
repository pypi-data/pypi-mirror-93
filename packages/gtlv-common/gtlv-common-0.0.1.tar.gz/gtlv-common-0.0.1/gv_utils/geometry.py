#!/usr/bin/env python3

import math
from typing import Generator, Iterable, List, Tuple, Union

import shapely.geometry
import shapely.geos
import shapely.ops
import shapely.wkb

LONLAT_CENTER = (5.74626, 45.17475)
LONLAT_EXTEND = ((5.60268, 45.0821), (5.88934, 45.2674))
EXTEND_BBOX_XY = None
SRID = 4326
R = 6371000  # earth radius in meters

GeomType = Union[shapely.geometry.Point, shapely.geometry.LineString, shapely.geometry.Polygon,
                 shapely.geometry.MultiPolygon]


def geom_to_xy(geom: GeomType, lonlatcenter: Tuple[float, float] = None, rounding: int = 2) -> GeomType:
    if lonlatcenter is None:
        lonlatcenter = LONLAT_CENTER

    return shapely.ops.transform(lambda lon, lat, z=None: _to_xy(lon, lat, lonlatcenter, rounding), geom)


def lonlat_to_xy(lonlat: Tuple[float, float], lonlatcenter: Tuple[float, float] = None,
                 rounding: int = 2) -> Tuple[float, float]:
    if lonlatcenter is None:
        lonlatcenter = LONLAT_CENTER

    return _to_xy(*lonlat, lonlatcenter=lonlatcenter, rounding=rounding)


def coords_to_xy(coords: Iterable[Tuple[float, float]], lonlatcenter: Tuple[float, float] = None,
                 rounding: int = 2) -> Generator[Tuple[float, float], None, None]:
    if lonlatcenter is None:
        lonlatcenter = LONLAT_CENTER

    for lonlat in coords:
        yield _to_xy(*lonlat, lonlatcenter=lonlatcenter, rounding=rounding)


def _to_xy(lon: float, lat: float, lonlatcenter: Tuple[float, float], rounding: int) -> Tuple[float, float]:
    if rounding is not None:
        _f = lambda u: round(u, rounding)
    else:
        _f = lambda u: u

    lon = lon * math.pi / 180
    lat = lat * math.pi / 180
    loncenter = lonlatcenter[0] * math.pi / 180
    latcenter = lonlatcenter[1] * math.pi / 180

    x = R * math.cos(lat) * math.sin(lon - loncenter)
    y = R * (math.cos(latcenter) * math.sin(lat) - math.sin(latcenter) * math.cos(lat) * math.cos(lon - loncenter))
    return _f(x), _f(y)


def geom_to_lonlat(geom: GeomType, lonlatcenter: Tuple[float, float] = None, rounding: int = 5) -> GeomType:
    if lonlatcenter is None:
        lonlatcenter = LONLAT_CENTER

    return shapely.ops.transform(lambda x, y, z=None: _to_lonlat(x, y, lonlatcenter, rounding), geom)


def xy_to_lonlat(x: float, y: float, lonlatcenter: Tuple[float, float] = None,
                 rounding: int = 5) -> Tuple[float, float]:
    if lonlatcenter is None:
        lonlatcenter = LONLAT_CENTER

    return _to_lonlat(x, y, lonlatcenter, rounding)


def coords_to_lonlat(coords: List[Tuple[float, float]], lonlatcenter: Tuple[float, float] = None,
                     rounding: int = 5) -> Generator[Tuple[float, float], None, None]:
    if lonlatcenter is None:
        lonlatcenter = LONLAT_CENTER

    for xy in coords:
        yield _to_lonlat(*xy, lonlatcenter=lonlatcenter, rounding=rounding)


def _to_lonlat(x: float, y: float, lonlatcenter: Tuple[float, float], rounding: int) -> Tuple[float, float]:
    if rounding is not None:
        _f = lambda u: round(u, rounding)
    else:
        _f = lambda u: u

    loncenter = lonlatcenter[0] * math.pi / 180
    latcenter = lonlatcenter[1] * math.pi / 180

    p = math.pow(x ** 2 + y ** 2, .5)
    c = math.asin(p / R)

    lon = loncenter + math.atan2(x * math.sin(c),
                                 p * math.cos(c) * math.cos(latcenter) - y * math.sin(c) * math.sin(latcenter))
    lat = math.asin(math.cos(c) * math.sin(latcenter) + y * math.sin(c) * math.cos(latcenter) / p)
    lon = lon / math.pi * 180
    lat = lat / math.pi * 180
    return _f(lon), _f(lat)


def round_lonlat(lonlat: Tuple[float, float]) -> Tuple[int, int]:
    return round(lonlat[0] * 1000), round(lonlat[1] * 1000)


def is_inside_extend(geomxy: GeomType) -> bool:
    global EXTEND_BBOX_XY
    if EXTEND_BBOX_XY is None:
        coords = []
        for coord in coords_to_xy(LONLAT_EXTEND):
            coords.extend(coord)
        EXTEND_BBOX_XY = shapely.geometry.box(*coords)

    return EXTEND_BBOX_XY.intersects(geomxy)


def close_elems_it(lonlatrounded: Tuple[int, int], lonlatmatrix: dict,
                   radius: int = 1) -> Generator[GeomType, None, None]:
    if radius >= 1:
        lat, lon = lonlatrounded
        for i in _get_range(lat, radius):
            if i in lonlatmatrix:
                for j in _get_range(lon, radius):
                    if j in lonlatmatrix[i]:
                        for elem in lonlatmatrix[i][j]:
                            yield elem


def _get_range(i: int, radius: int) -> List[int]:
    return sorted(range(i - radius, i + radius + 1), key=lambda x: abs(x - i))


def encode_geometry(geometry: GeomType) -> bytes:
    if not hasattr(geometry, '__geo_interface__'):
        raise TypeError('{g} does not conform to '
                        'the geo interface'.format(g=geometry))
    shape = shapely.geometry.asShape(geometry)
    shapely.geos.lgeos.GEOSSetSRID(shape._geom, SRID)
    return shapely.wkb.dumps(shape, include_srid=True)


def decode_geometry(wkb: bytes) -> GeomType:
    return shapely.wkb.loads(wkb)
