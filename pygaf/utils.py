def rot_point_clockwise(self, x0, y0, x1, y1, phi):
    """
    Rotate a point clockwise about a point.

    Arguments:
    ---------
    x0 : float
        x coordinate of ceter of rotation [L]
    y0 : float
        y coordinate of center of rotation [L]
    x1 : float
        x coordinate of point to be rotated [L]
    y1 : float
        y coordinate of point to be rotated [L]
    phi : float
        Angle of clockwise rotation [radians]
    """
    from numpy import cos, sin
    x1_rot = x0 + (x1-x0)*cos(-phi) - (y1-y0)*sin(-phi)
    y1_rot = y0 + (y1-y0)*cos(-phi) + (x1-x0)*sin(-phi)
    return (x1_rot, y1_rot)
