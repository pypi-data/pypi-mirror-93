# author: Drew Botwinick, Botwinick Innovations
# license: 3-clause BSD

from math import floor, pi, radians
from os import path as osp

import numpy as np
import shapefile as shp
from botwinick_math.geo.transforms_2d import TransformTSR2D, rotate_2d
from pyproj import CRS, Proj, Transformer
from pyproj.enums import TransformDirection, WktVersion


def dms2dd(degrees, minutes, seconds):
    """
    Utility function to convert DMS (degrees, minutes, seconds) to decimal value

    :param degrees: degrees value
    :param minutes: minutes value
    :param seconds: seconds value
    :return: decimal (float) value
    """
    if degrees >= 0.0:
        return degrees + (minutes / 60.0) + (seconds / 3600.0)
    else:
        return degrees - (minutes / 60.0) - (seconds / 3600.0)


def get_utm_zone(lat, lon):
    """
    Return the UTM zone, hemisphere indication, and latitude letter designation for the associated
    decimal latitude and longitude inputs. You can use `dms2dd` to convert DMS (decimal, minutes, seconds)
    to decimal values.

    :param lat: latitude value (float)
    :param lon: longitude value (float)
    :return: zone (int), hemisphere string ('north'|'south'), latitude letter (str)
    """
    zone = int(floor((lon + 180) / 6) % 60) + 1

    # exceptions for Svalbard and Norway
    if 56.0 <= lat < 64.0 and 3.0 <= lon < 12.0:
        zone = 32
    elif 72.0 <= lat < 84.0 and 0.0 <= lon < 9.0:
        zone = 31
    elif 72.0 <= lat < 84.0 and 9.0 <= lon < 21.0:
        zone = 33
    elif 72.0 <= lat < 84.0 and 21.0 <= lon < 33.0:
        zone = 35
    elif 72.0 <= lat < 84.0 and 33.0 <= lon < 42.0:
        zone = 37

    hemisphere = 'north' if lat >= 0 else 'south'
    # noinspection SpellCheckingInspection
    letter = 'CDEFGHJKLMNPQRSTUVWXX'[int((lat + 80) / 8)] if -80.0 <= lat <= 84.0 else None

    return zone, hemisphere, letter


def ll2utm(lat, lon):
    """
    Convert lat/long to UTM coordinates (m)

    :param lat: latitude (decimal)
    :param lon: longitude (decimal)
    :return: x, y, ((utm_zone, north/south, latitude_letter), projection_instance)
    """
    utm_z = get_utm_zone(lat, lon)
    p = Proj(CRS.from_epsg(get_wgs84_utm_epsg_code(*utm_z)))
    x, y = p(lon, lat)
    return x, y, (utm_z, p)


def utm2ll(x, y, utm_zone, south=False):
    """
    Convert UTM (m) to lat/long (decimal)

    :param x: x/easting UTM (m)
    :param y: y/northing UTM (m)
    :param utm_zone: utm zone number (or a pyproj CRS)
    :param south: boolean, true if south, false for north [default] [unused if pyproj CRS provided for utm_zone]
    :return: lat, lon, projection_instance
    """
    if isinstance(utm_zone, CRS):
        crs = utm_zone
    else:
        crs = CRS.from_epsg(get_wgs84_utm_epsg_code(utm_zone, south))

    p = Proj(crs)
    lon, lat = p(x, y, inverse=True)
    return lat, lon, p


def get_wgs84_utm_epsg_code(*utm_zone):
    """
    Convert utm zone information to an EPSG code to make projection definition easier. Can take parameters output
    from `get_utm_zone` as arguments for `utm_zone`.

    :param utm_zone: iterable with at least two parameters (zone number[int], hemisphere[str:'north'|'south']
    :return: the appropriately zoned WGS84 UTM EPSG code
    """
    utm_band = '%02d' % utm_zone[0]

    hemisphere = utm_zone[1]
    if hemisphere == 'north' or hemisphere is False:
        epsg_code = '326' + utm_band
    else:
        epsg_code = '327' + utm_band

    return int(epsg_code)


def rad2arcs(theta):
    """
    Utility function to convert angle in radians to arc seconds.

    :param theta: angle in radians
    :return: angle in arc seconds
    """
    return theta * (3600.0 * 180.0) / pi


def make_model_tsr_crs(m, w, raw_world=False, return_raw_params=False, return_pyproj=False, **kwargs):
    """
    Generate a CRS for a model that will be convertible to UTM via GIS software

    :param m: Model Coordinates (list of tuples of x,y) or numpy array [model, m] [corresponding to w]
    :param w: World Coordinates (list of tuples of lat,long) or numpy array [wgs84 lat/long decimal] [corresponding to m]
    :param raw_world: whether to use the given world coordinates as raw (x,y) coordinates and perform no transformations on them
    :param return_raw_params: whether to return ((tx, ty), (sx, sy), theta/rz) as 3rd output
    :param return_pyproj: whether the resulting transformer should be a pyproj transformer or our own.
    :return: transformer, target_crs, (and optionally) ((tx, ty), (sx, sy), theta/rz)
    :rtype: (Transformer, CRS)|(Transformer, CRS, tuple[tuple[float, float], tuple[float, float], float])
    """
    w = np.asarray(w)
    if not raw_world:  # convert lat/lon to UTM coordinates
        zone, hemisphere, letter = get_utm_zone(*np.average(w, axis=0))  # zone from average of given coordinates
        target_crs = CRS.from_epsg(get_wgs84_utm_epsg_code(zone, hemisphere))  # target CRS
        target_prj = Proj(target_crs)
        w_utm = np.stack(target_prj(w[:, 1], w[:, 0]), axis=-1)  # convert lat/long to UTM
    else:
        target_crs = None
        w_utm = w

    if 'sx' in kwargs and 'sy' in kwargs and 'theta' in kwargs:
        m = np.asarray(m)
        sx = kwargs['sx']
        sy = kwargs['sy']
        rz = kwargs['theta']
        # calculate transformation for model coordinates to UTM coordinates
        xfm_2d = TransformTSR2D.from_point_tsr(m, w_utm, sx, sy, rz)
    else:
        # calculate transformation for model coordinates to UTM coordinates
        xfm_2d = TransformTSR2D.from_points(m, w_utm)

    # support for 'nudging' translation by kwargs
    xfm_2d.nudge(tx=kwargs.pop('nx', 0.0), ty=kwargs.pop('ny', 0.0))

    # get final forward transformation details from Transform2D [partially done for backwards compatibility...]
    (tx, ty), (sx, sy), rz = xfm_2d.tsr

    if return_pyproj:
        # TODO: ideally we could make a proj definition that would perform the transformation and appropriate projection in 1 definition...?
        # TODO: this projection should actually be a 2D Helmert projection?? Affine *should* work fine thought, right??
        pipeline_str = """
            +proj=pipeline
            +step +proj=affine +xoff=%.6f +yoff=%.6f +s11=%.6f +s12=%.6f +s21=%.6f +s22=%.6f
            """ % (tx, ty,
                   sx * np.cos(rz), -np.sin(rz),
                   np.sin(rz), sy * np.cos(rz))
        target_xfm = Transformer.from_pipeline(pipeline_str)
    else:
        target_xfm = xfm_2d

    if return_raw_params:
        return target_xfm, target_crs, ((tx, ty), (sx, sy), rz)
    return target_xfm, target_crs


def write_points_file(path, m, w, sx=None, sy=None, theta=None, nx=0.0, ny=0.0):
    """
    Write a points CSV/TSV file that can be used for importing/exporting TSR and projection definitions

    # TODO: add translation/scaling for elevation/z

    :param path: path of file to write
    :param m: Model Coordinates (list of tuples of x,y) or numpy array [model, m] [corresponding to w]
    :param w: World Coordinates (list of tuples of lat,long) or numpy array [wgs84 lat/long decimal] [corresponding to m]
    :param sx: x-scale factor (None if using points)
    :param sy: y-scale factor (None if using points)
    :param theta: rotation theta (None if using points)
    :param nx: x-translation nudge scalar (default: 0.0); value to shift translation in the model x-direction
    :param ny: y-translation nudge scalar (default: 0.0); value to shift translation in the model y-direction
    """
    m = np.array(m, ndmin=2)
    w = np.array(w, ndmin=2)
    assert m.shape == w.shape and len(m.shape) == 2 and m.shape[1] == 2
    if m.shape[0] >= 2:
        points = True
    elif m.shape[0] == 1 and sx is not None and sy is not None and theta is not None:
        points = False
    else:
        raise ValueError('must either provide model and world points or anchor position with scale and rotation inputs')

    with open(path, 'w') as f:
        f.write('\t'.join(['x', 'y', 'lon', 'lat', 'sx', 'sy', 'theta']) + '\n')
        f.write('# either list multiple (x,y) and (lon, lat) pairs or a SINGLE entry of anchor point x/y/lon/lat, scale, and rotation\n')
        f.write('# nudge: tx=%.6f\n' % nx)
        f.write('# nudge: ty=%.6f\n' % ny)
        if points:
            for i in range(len(m)):
                f.write('\t'.join([
                    '%.6f' % m[i][0],
                    '%.6f' % m[i][1],
                    '%.6f' % w[i][1],  # 2nd column of w is lon
                    '%.6f' % w[i][0],  # 1st column of w is lat
                ]) + '\n')
        else:
            f.write('\t'.join([
                '%.6f' % m[0][0],
                '%.6f' % m[0][1],
                '%.6f' % w[0][1],  # 2nd column of w is lon
                '%.6f' % w[0][0],  # 1st column of w is lat
                '%.6f' % sx,
                '%.6f' % sy,
                '%.6f' % theta,
            ]) + '\n')


def interpret_points_file(path, return_raw_params=False):
    """
    Read a points CSV/TSV file and compute the TSR and projection definition

    # TODO: add translation/scaling for elevation/z

    :param path: path of file to read
    :param return_raw_params: whether or not to return the raw translation/scale/rotation parameters of the transformation
    :return: transform, target_crs
    """
    mw = np.array(np.genfromtxt(path, skip_header=1, comments='#'), copy=False, ndmin=2)
    # inefficient to do 2nd pass, but find nudges if defined
    nx = 0.0
    ny = 0.0
    try:
        with open(path, 'r') as f:
            for line in f:
                line = line.lower().strip()
                if line.startswith('#') and 'nudge' in line and 'x' in line:
                    nx = float(line.split('=', 2)[1].strip())
                if line.startswith('#') and 'nudge' in line and 'y' in line:
                    ny = float(line.split('=', 2)[1].strip())
                pass
    except ValueError:
        print('WARNING: unable to parse nudge(s)')
    # if we have a single entry file with additional data columns -- then we'll interpret that!
    if len(mw.shape) == 2 and mw.shape[0] == 1 and mw.shape[1] == 7:
        transform, target_crs, params = make_model_tsr_crs(mw[:, [0, 1]], mw[:, [3, 2]],
                                                           sx=mw[0, 4], sy=mw[0, 5], theta=mw[0, 6], nx=nx, ny=ny,
                                                           return_raw_params=True)
    # otherwise read points and compute 2D TSR
    elif len(mw.shape) > 1 and mw.shape[0] > 1 and mw.shape[1] > 3:
        transform, target_crs, params = make_model_tsr_crs(mw[:, [0, 1]], mw[:, [3, 2]], nx=nx, ny=ny,
                                                           return_raw_params=True)
    # or raise an error because we don't know what to do...
    else:
        raise IOError('points file did not conform to expected possible formats')
    if return_raw_params:
        return transform, target_crs, params
    return transform, target_crs


def write_crs_wkt(path, crs, wkt_version=WktVersion.WKT1_ESRI):
    """
    Write a projection / coordinates system prj file using WKT format.

    :param path: path of file to write
    :param crs: coordinate reference system instance
    :param wkt_version: wkt version string (default is V1 ESRI)
    """
    with open(path, 'w') as f:
        f.write(crs.to_wkt(wkt_version, pretty=True))


def read_crs_wkt(path):
    """
    Read a projection / coordinates system WKT prj file.

    :param path: path of file to read
    :return: CRS from WKT
    :rtype: CRS
    """
    with open(path, 'r') as f:
        crs = CRS.from_wkt(f.read())
    return crs


def shp2model(model, shape_file, return_m2u=False):
    """
    Convert data from the given shape file to GeoJSON with the coordinates transformed to be consistent
    with the model based on the given points file.

    :param model: either model or points file that defines known points in the model as longitude and latitude [effective rosetta stone]
    :param shape_file: shapefile that contains GIS features to translate to the model coordinates system
    :param return_m2u: whether or not to return the model2utm transform object
    :return: list of geojson features (and optionally a model2utm transform object)
    """
    model = interpret_points_file(model) if not isinstance(model, tuple) else model
    model2utm_xfm, utm_crs = model

    shp_crs = read_crs_wkt(shape_file.replace('.shp', '.prj'))
    shp2utm_xfm = Transformer.from_crs(shp_crs, utm_crs)  # type: Transformer
    results = []
    with shp.Reader(shape_file) as r:
        for record in r.iterShapeRecords():
            data = record.__geo_interface__
            coordinates = np.asarray(data['geometry']['coordinates'])
            utm = np.stack(shp2utm_xfm.transform(coordinates[:, 0], coordinates[:, 1]), axis=-1)
            new_coords = np.stack(model2utm_xfm.transform(utm[:, 0], utm[:, 1], direction=TransformDirection.INVERSE), axis=-1)
            data['geometry']['coordinates'] = [[float(x), float(y)] for (x, y) in new_coords]
            results.append(data)
    if not return_m2u:
        return results
    return results, (model2utm_xfm, utm_crs)


# _world_file_extension_map = _CiDict({
#     'gif': 'gfw',
#     'jpg': 'jgw',
#     'jp2': 'j2w',
#     'png': 'pgw',
#     'tif': 'tfw',
#     'tiff': 'tfw',
# })


def write_image_world_file(image_file, a, d, b, e, c, f):
    """
    Write world file for given image file using given input parameters

    https://en.wikipedia.org/wiki/World_file

    :param image_file: path to image file
    :param a: parameter a [x-component of the pixel width (x-scale)]
    :param d: parameter d [y-component of the pixel width (y-skew)]
    :param b: parameter b [x-component of the pixel height (x-skew)]
    :param e: parameter e [y-component of the pixel height (y-scale), typically negative]
    :param c: parameter c [x-coordinate of the center of the original image's upper left pixel transformed to the map]
    :param f: parameter f [y-coordinate of the center of the original image's upper left pixel transformed to the map]
    :return:
    """
    target = osp.abspath(image_file) + 'w'  # simply just append w on end of whatever extension the file has... (easiest reliable method)
    with open(target, 'w') as t:
        t.write('%.8f\n%.8f\n%.8f\n%.8f\n%.8f\n%.8f\n' % (a, d, b, e, c, f))


def model2model(model1, model2, x, y, numpy=True):
    """
    Convert from model 1 coordinate system (via model1) to model 2 coordinate system (via model2). Will use world/UTM
    system as an intermediary.

    Note: technically this could be somewhat lossy because of using UTM as an intermediary (and would be more straightforward
    if we just used known anchor points or similar common to both models; however, this approach was adopted to make it
    easier to convert between models while having a consistent model reference file format). That is, each model has a definition
    file to convert between that model and the real-world. Plus, if they're all referenced to the real world--that creates the
    easiest way to convert between models even if their anchor points aren't matched to each other.

    :param model1: definition of model 1 system (if filename is provided, will interpret points file)
    :param model2: definition of model 2 system (if filename is provided, will interpret points file)
    :param x: x values to convert [single float value, 1D numpy array, or list]
    :param y: y values to convert [single float value, 1D numpy array, or list]
    :param numpy: True to allow numpy result; False to return non-numpy structure; non-np useful for serialization sometimes
    :return: x', y'
    :rtype: tuple[list[float], list[float]]|tuple[array, array]
    """
    x1, y1 = model2utm(model1, x, y, inverse=False, numpy=True)
    x2, y2 = model2utm(model2, x1, y1, inverse=True, numpy=numpy)
    return x2, y2


def model2utm(model, x, y, inverse=False, numpy=True):
    """
    Convert from model coordinates to UTM coordinates using provided model definition.

    :param model: definition of model system (if filename is provided, will interpret points file)
    :param x: x values to convert [single float value, 1D numpy array, or list]
    :param y: y values to convert [single float value, 1D numpy array, or list]
    :param inverse: if True, this function will convert UTM to model coordinates
    :param numpy: True to allow numpy result; False to return non-numpy structure; non-np useful for serialization sometimes
    :return: x', y'
    :rtype: tuple[list[float], list[float]]|tuple[array, array]
    """
    if not isinstance(model, tuple):  # assume it's a path if not a tuple
        model = interpret_points_file(model)

    m2u_xfm = model[0]
    x, y = np.asarray(x), np.asarray(y)
    direction = TransformDirection.FORWARD if not inverse else TransformDirection.INVERSE
    x_, y_ = m2u_xfm.transform(x, y, direction=direction)

    if not numpy:
        return [float(x) for x in x_], [float(y) for y in y_]

    return x_, y_


def utm2model(model, x, y, numpy=True):
    """
    Convert from UTM coordinates to model coordinates using provided model definition. Note that
    this is a just a wrapper calling `model2utm` with inverse=True. Technically that means there is
    extra overhead in calling this function over using `model2utm` with inverse=True. It's provided
    just for convenience.

    :param model: definition of model system (if filename is provided, will interpret points file)
    :param x: x values to convert [single float value, 1D numpy array, or list]
    :param y: y values to convert [single float value, 1D numpy array, or list]
    :param numpy: True to allow numpy result; False to return non-numpy structure; non-np useful for serialization sometimes
    :return: x', y'
    :rtype: tuple[list[float], list[float]]|tuple[array, array]
    """
    return model2utm(model, x, y, inverse=True, numpy=numpy)


def gis_ellipse_polygon(origin, a, b, orientation=0.0, complexity=128):
    """
    Generate a polygon of an ellipse suitable for GIS applications.

    :param origin: the center of the ellipse (expected to be UTM, m)
    :param a: the a/semi-major axis length (expected to be UTM, m)
    :param b: the b/semi-minor axis length (expected to be UTM, m)
    :param orientation: the rotation/orientation (in degrees) of the ellipse [0.0 means no rotation applied] [rotated about origin]
    :param complexity: number of data points that make up the polygon [note that result will have length complexity + 1] with
    the last entry equal to the first entry to ensure compatibility for GIS applications.
    :return: numpy array containing (complexity+1) points representing the selected ellipse

    """
    x = origin[0]
    y = origin[1]
    result = np.zeros((complexity + 1, 2), dtype=np.float32)
    angles = np.linspace(0.0, 2.0 * pi, complexity + 1, endpoint=True)
    result[:, 0] = x + a * np.cos(angles)
    result[:, 1] = y + b * np.sin(angles)
    if orientation != 0.0:  # handle rotation
        result[:, 0], result[:, 1] = rotate_2d(result[:, 0], result[:, 1], orientation, x, y)
    result[-1] = result[0]  # this should be true anyway, but we make sure they're identical before returning...
    return result
