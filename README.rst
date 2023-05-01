svg.transform
=============

It's a library to do svg.transforms.

It's been on a list of things to do for years, and I haven't implemented it,
because I don't need it, and making a library you don't use is silly.
But since nobody else is implementing this, even though it's perfectly simple,
well, I did it anyway. Anger-Driven Development is a thing. :-D

You are welcome.

I'm already looking for someone to take over this, and I haven't even started
writing code. You can take over svg.path too, I don't use it anymore either.

Usage
-----

You make transformation matrices with the following commands::


    * svg.transform.translate_matrix(tx, ty=0): Returns a matrix that will translate in x and y

    * svg.transform.scale_matrix(sx, sy=None): Returns a matrix that will scale in x and y

    * svg.transform.rotate_matrix(r, cx=0, cy=0): Returns a matrix that will rotate, with optional offset

    * svg.transform.skewx_matrix(ax): Returns a matrix that will skew in the x axis

    * svg.transform.skewy_matrix(ay): Returns a matrix that will skew in the y axis

    * svg.transform.matrix_matrix(a, b, c, d, e, f): Returns a free form translation matrix

For example like this::

    >>> from svg import transform
    >>>
    >>> transform.translate_matrix(5, 8)
    array([[ 1,  0,  5],
          [ 0,  1, 10],
          [ 0,  0,  1]])

You use this matrix by applying a matrix multiplication::

    >>> from array import array
    >>>
    >>> old_x = 10
    >>> old_y = 10
    >>>
    >>> res = transform.translate_matrix(5, 8) @ array("f", [old_x, old_y, 1])
    >>> new_x = res[0]
    >>> new_y = res[1]
    >>> new_x, new_y
    15.0, 18.0

You can also create transformation matrices directly from the SVG transform attributes::

    >>> transform.parse("translate(-10 -20) scale(2) rotate(45) translate(5 10)")
    array([[  1.05064398,  -1.70180705, -21.7648506 ],
           [  1.70180705,   1.05064398,  -0.98452498],
           [  0.        ,   0.        ,   1.        ]])
