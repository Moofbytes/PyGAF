def add_constant_to_list(list, const):
    """Add a constant value to each item of a list.

    Args:
        list (float) : 2d list of numeric values.
        const (float) : Constant value to add to each list item.

    Returns:
        2d list.

    """
    import numpy
    arr = numpy.add(list, const)
    return arr.tolist()

def deg2rad(deg):
    """Convert degrees to radians for an angle between -90 and 90 deg.

    Args:
        deg (float) : Angle in degrees.

    Returns:
        Angle in radians.

    """
    from numpy import pi
    return deg*2*pi/360

def rotate_point(x0, y0, x1, y1, phi):
    """Rotate the coordinates of a point.

    Args:
        x0 (float) : X coordinate of ceter of rotation.
        y0 (float) : Y coordinate of center of rotation.
        x1 (float) : X coordinate of point to be rotated.
        y1 (float) : Y coordinate of point to be rotated.
        phi (float) : Angle of clockwise rotation in radians.

    Returns:
        Tupple of rotated x and y coordinates.

    """
    from numpy import cos, sin
    x1r = x0 + (x1-x0)*cos(-phi) - (y1-y0)*sin(-phi)
    y1r = y0 + (y1-y0)*cos(-phi) + (x1-x0)*sin(-phi)
    return (x1r, y1r)

def rotate_grid(x0, y0, x, y, phi):
    """Rotate the coordinates of a grid.

    Args:
        x0 (float) : X coordinate of ceter of rotation.
        y0 (float) : Y coordinate of center of rotation.
        x (float) : 1d list of grid x coordinates.
        y (float) : 1d list of grid y coordinates.
        phi (float) : Angle of clockwise rotation in radians.

    Returns:
        Rotated x as 1d lsit, rotated y as 1d list.

    """
    from pygaf.utils import rotate_point
    npts = len(x)
    rotx, roty = [], []
    for i in range(npts):
        coord = rotate_point(x0, y0, x[i], y[i], phi)
        rotx.append(coord[0])
        roty.append(coord[1])
    return rotx, roty

def rotate_grid_2d(x0, y0, x, y, phi):
    """
    Rotate the coordinates of a grid in 2d format.

    Args:
        x0 (float) : X coordinate of ceter of rotation.
        y0 (float) : Y coordinate of center of rotation.
        x (float) : 2d list of grid x coordinates.
        y (float) : 2d list of grid y coordinates.
        phi (float) : Angle of clockwise rotation in radians.

    Returns:
        Rotated x as 2d list, rotated y as 2d list.

    """
    from pygaf.utils import rotate_point
    nrow = len(x)
    ncol = len(x[0])
    rotx, roty = [], []
    for r in range(nrow):
        rowx, rowy = [], []
        for c in range(ncol):
            coord = rotate_point(x0, y0, x[r][c], y[c][r], phi)
            rowx.append(coord[0])
            rowy.append(coord[1])
        rotx.append(rowx)
        roty.append(rowy)
    return rotx, roty
