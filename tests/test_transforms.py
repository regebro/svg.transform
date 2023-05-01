import numpy

from svg import transform


def test_make_matrix():
    # Default is a non-transformation
    m1 = transform.make_matrix()
    assert m1.tolist() == [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

    # Translate
    m1 = transform.make_matrix(tx=8.6, ty=7)
    assert m1.tolist() == [[1, 0, 8.6], [0, 1, 7], [0, 0, 1]]

    # Scale
    m2 = transform.make_matrix(sx=5, sy=2.1)
    assert m2.tolist() == [[5, 0, 0], [0, 2.1, 0], [0, 0, 1]]

    # Skew
    m3 = transform.make_matrix(ax=2, ay=5)
    numpy.testing.assert_array_almost_equal(
        m3,
        [
            [1, -2.185039863261519, 0],
            [-3.380515006246586, 1, 0],
            [0, 0, 1],
        ],
    )

    # Translate + Scale
    m4 = transform.make_matrix(tx=8.6, ty=7, sx=5, sy=2.1)
    assert m4.tolist() == [[5, 0, 8.6], [0, 2.1, 7], [0, 0, 1]]

    # Translate and scale should be the same as translate @ scale
    numpy.testing.assert_array_almost_equal(m4, (m1 @ m2))

    # Translate + Skew
    m4 = transform.make_matrix(tx=8.6, ty=7, ax=2, ay=5)
    numpy.testing.assert_array_almost_equal(
        m4.tolist(),
        [
            [1, -2.185039863261519, 8.6],
            [-3.380515006246586, 1, 7],
            [0, 0, 1],
        ],
    )

    # Translate and skew should be the same as translate @ skew
    assert m4.tolist() == (m1 @ m3).tolist()

    # Scale + Skew
    m4 = transform.make_matrix(sx=5, sy=2.1, ax=2, ay=5)
    numpy.testing.assert_array_almost_equal(
        m4,
        [
            [5, -10.925199316307594, 0],
            [-7.099081513117831, 2.1, 0],
            [0, 0, 1],
        ],
    )

    # Scale and skew should be the same as scale @ skew
    numpy.testing.assert_array_almost_equal(m4, (m2 @ m3))

    # Translate + Scale + Skew
    m4 = transform.make_matrix(tx=8.6, ty=7, sx=5, sy=2.1, ax=2, ay=5)
    numpy.testing.assert_array_almost_equal(
        m4,
        [
            [5, -10.925199316307594, 8.6],
            [-7.099081513117831, 2.1, 7],
            [0, 0, 1],
        ],
    )

    # Translate and Scale and skew should be the same as translate @ scale @ skew
    numpy.testing.assert_array_almost_equal(m4, (m1 @ m2 @ m3))

    # Rotate
    m4 = transform.make_matrix(r=1)
    # cos(1) == 0.5403023058681398
    # sin(1) == 0.8414709848078965
    numpy.testing.assert_array_almost_equal(
        m4,
        [
            [0.5403023058681398, -0.8414709848078965, 0],
            [0.8414709848078965, 0.5403023058681398, 0],
            [0, 0, 1],
        ],
    )

    # Rotate with offset
    m4 = transform.make_matrix(r=1, cx=10, cy=4)
    # cos(1) == 0.5403023058681398
    # sin(1) == 0.8414709848078965
    numpy.testing.assert_array_almost_equal(
        m4,
        [
            [0.5403023058681398, -0.8414709848078965, 7.962860880550188],
            [0.8414709848078965, 0.5403023058681398, -6.5759190715515246],
            [0, 0, 1],
        ],
    )

    # And that's the same as applying a translate, rotating and deducting the translation:
    m5 = transform.make_matrix(tx=10, ty=4)
    m5 = m5 @ transform.make_matrix(r=1)
    m5 = m5 @ transform.make_matrix(tx=-10, ty=-4)
    assert m4.tolist() == m5.tolist()

    # Do them all!
    m5 = transform.make_matrix(tx=8.6, ty=7, sx=5, sy=2.1, ax=2, ay=5, r=1, cx=10, cy=4)
    numpy.testing.assert_array_almost_equal(
        m5,
        [
            [-6.49172669857521, -10.1102653067095, 120.25753094735971],
            [-2.0685610429868637, 7.108305954397887, -63.33842851890122],
            [0, 0, 1],
        ],
    )
    numpy.testing.assert_array_almost_equal(m5, m1 @ m2 @ m3 @ m4)


def test_coordinate_transform():
    def xy_transform(matrix, x, y):
        """Takes an x and a y coordinate and transforms it"""
        x, y, _ = matrix @ numpy.array([x, y, 1])
        return x, y

    # Translate
    matrix = transform.make_matrix(tx=20, ty=30)
    assert xy_transform(matrix, 100, 100) == (120, 130)

    # Scale
    matrix = transform.make_matrix(sx=2, sy=3)
    assert xy_transform(matrix, 100, 100) == (200, 300)

    # Skew in 45 degree angles, one reversed
    matrix = transform.make_matrix(ax=numpy.pi / 4, ay=-numpy.pi / 4)
    x, y = xy_transform(matrix, 100, 100)
    # So the x is now 200
    assert x == 200
    # And the y is now (nearly) 0
    numpy.testing.assert_almost_equal(y, 0)

    # Rotate 180 degrees
    matrix = transform.make_matrix(r=numpy.pi)
    x, y = xy_transform(matrix, 100, 100)
    # They are approximately -100, -100 but not the last few decimals
    numpy.testing.assert_almost_equal(x, -100)
    numpy.testing.assert_almost_equal(y, -100)

    # Rotate 90 degrees with non-zero center
    matrix = transform.make_matrix(r=numpy.pi / 2, cx=50, cy=30)
    x, y = xy_transform(matrix, 100, 100)
    # They are approximately -100, -100 but not the last few decimals
    numpy.testing.assert_almost_equal(x, -20)
    numpy.testing.assert_almost_equal(y, 80)


def test_parsing():
    m = transform.parse("translate(-10,-20)")
    assert m.tolist() == [[1, 0, -10], [0, 1, -20], [0, 0, 1]]

    m = transform.parse("scale(2)")
    assert m.tolist() == [[2, 0, 0], [0, 2, 0], [0, 0, 1]]

    m = transform.parse("rotate(45)")
    numpy.testing.assert_array_almost_equal(
        m,
        [
            [0.5253219888177297, -0.8509035245341184, 0],
            [0.8509035245341184, 0.5253219888177297, 0],
            [0, 0, 1],
        ],
    )

    m = transform.parse("skewX(5)")
    numpy.testing.assert_array_almost_equal(
        m, [[1, -3.380515006246586, 0], [0, 1, 0], [0, 0, 1]]
    )

    m = transform.parse("skewY(5)")
    numpy.testing.assert_array_almost_equal(
        m, [[1, 0, 0], [-3.380515006246586, 1, 0], [0, 0, 1]]
    )

    m = transform.parse("translate(-10 -20) scale(2) rotate(45)translate(5,10)")
    numpy.testing.assert_array_almost_equal(
        m,
        [
            [1.0506439776354595, -1.7018070490682369, -21.76485060250507],
            [1.7018070490682369, 1.0506439776354595, -0.984524978304222],
            [0, 0, 1],
        ],
    )
