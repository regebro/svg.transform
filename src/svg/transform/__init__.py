import numpy
import re


def make_matrix(tx=0, ty=0, sx=1, sy=1, ax=0, ay=0, r=0, cx=0, cy=0):
    """Make a transformation matrix, with the following parameters:

    tx: Translation (ie move) in the x direction
    ty: Translation (ie move) in the y direction
    sx: Scaling in the x direction
    sy: Scaling in the y direction
    ax: Skewing of x coordinates
    ay: Skewing of y coordinates
    r:  Rotatation
    cx: Rotation center x coordinate
    cy: Rotation center y coordinate
    """

    matrix = numpy.array([[sx, 0, tx], [0, sy, ty], [0, 0, 1]])

    if ax or ay:
        matrix = matrix @ numpy.array(
            [[1, numpy.tan(ax), 0], [numpy.tan(ay), 1, 0], [0, 0, 1]]
        )

    if r:
        if cx or cy:
            matrix = matrix @ numpy.array(
                [
                    [1, 0, cx],
                    [0, 1, cy],
                    [0, 0, 1],
                ]
            )

        matrix = matrix @ numpy.array(
            [
                [numpy.cos(r), numpy.sin(-r), 0],
                [numpy.sin(r), numpy.cos(r), 0],
                [0, 0, 1],
            ]
        )

        if cx or cy:
            matrix = matrix @ numpy.array(
                [
                    [1, 0, -cx],
                    [0, 1, -cy],
                    [0, 0, 1],
                ]
            )

    return matrix


def translate_matrix(tx, ty=0):
    """Returns a matrix that will translate in x and y"""
    return make_matrix(tx=tx, ty=ty)


def scale_matrix(sx, sy=None):
    """Returns a matrix that will scale in x and y"""
    if sy is None:
        sy = sx
    return make_matrix(sx=sx, sy=sy)


def rotate_matrix(r, cx=0, cy=0):
    """Returns a matrix that will rotate, with optional offset"""
    return make_matrix(r=r, cx=cx, cy=cy)


def skewx_matrix(ax):
    """Returns a matrix that will skew in the x axis"""
    return make_matrix(ax=ax)


def skewy_matrix(ay):
    """Returns a matrix that will skew in the y axis"""
    return make_matrix(ay=ay)


def matrix_matrix(a, b, c, d, e, f):
    """Returns a free form translation matrix"""
    return numpy.array([[a, c, e], [b, d, f], [0, 0, 1]])


TRANSFORM_RE = re.compile(r"[a-zA-Z]+?\([0-9\.\,\-\s]+?\)")
ARGUMENT_RE = re.compile(r"[0-9\.\-]+")
TRANSFORMS = {
    "translate": translate_matrix,
    "scale": scale_matrix,
    "rotate": rotate_matrix,
    "skewx": skewx_matrix,
    "skewy": skewy_matrix,
    "matrix": matrix_matrix,
}


def parse(transform):
    """Parse a svg transform attribute"""
    transformlist = TRANSFORM_RE.findall(transform)
    matrix = make_matrix()

    for xform in transformlist:
        action, params = xform.split("(")
        params = [float(x) for x in ARGUMENT_RE.findall(params)]
        matrix = matrix @ TRANSFORMS[action.lower()](*params)

    return matrix
