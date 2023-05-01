import numpy

from svg import path


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
