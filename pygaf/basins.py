class CircBasin:
    """Circular recharge basin class.

    Attributes:
        cx (float) : Basin center x coordinate (units L, default 0.0).
        cy (float) : Basin center y coordinate (units L, default 0.0).
        diam (float) : Basin diameter (default 10.0).
        rot (float) : Basin rotation angle in radians (default 0.0).
        name (str) : Basin name (default 'Unnamed').

    """
    is_rectangular = False
    is_circular = True
    def __init__(self, cx=0.0, cy=0.0, diam=10, name='Circle basin'):
        self.cx = cx
        self.cy = cy
        self.diam = diam
        self.name = name
        self.type = 'Circular Basin'
        return

    @property
    def diam(self):
        """float : Basin diameter.

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.

        """
        return self._diam
    @diam.setter
    def diam(self, v):
        if not (v > 0):
            raise Exception('Basin diameter must be greater than 0.')
        self._diam = v

    @property
    def rad(self):
        """float : Basin radius."""
        return self.diam / 2

    @property
    def area(self):
        """float : basin area."""
        from numpy import pi
        return pi * self.rad**2

    def info(self):
        """Print the basin information."""
        print('BASIN INFORMATION')
        print('-----------------')
        print('Type:', self.type)
        print('Name:', self.name)
        print('Basin center: (' + str(round(self.cx, 1)) + ', ' +\
            str(round(self.cy, 1)) + ') [L]')
        print('Basin diameter:', self.diam, '[L]')
        print('Basin radius:', self.rad, '[L]')
        print('Basin area:', round(self.area, 1), '[L2]')
        print()
        return

    def draw(self, dw=4):
        """Display a drawing of the basin.

        Args:
            dw (float) : Width of basin drawing (default 4.0).

        """
        import matplotlib.pyplot as plt
        from matplotlib.patches import Circle
        dr = self.rad/25
        fig = plt.figure(figsize=(dw, dw))
        fig.suptitle(self.name, fontsize=14, fontweight=530)
        ax = plt.gca()
        ax.add_patch(
            Circle((self.cx, self.cy), radius=self.rad, facecolor='silver',
            edgecolor='black', linewidth=2)
        ) # basin
        plt.plot(self.cx, self.cy, '.', color='black')
        ax.arrow(
            self.cx, self.cy, 0, self.rad-2*dr, overhang=1, head_width=1.5*dr,
            color='black', linewidth=0.5, fill=False
        )
        ax.text(
            self.cx-2*dr, self.cy+0.33*self.rad, round(self.rad, 1),
            fontsize=12, horizontalalignment='center',
            verticalalignment='bottom', rotation=90
        )
        ax.text(
            self.cx, self.cy, '('+str(self.cx)+', '+str(self.cy)+')',
            fontsize=12, horizontalalignment='center', verticalalignment='top'
        )
        plt.axis('scaled')
        plt.axis('off')
        plt.tight_layout()
        plt.show()
        return

class RectBasin:
    """Rectangular recharge basin class.

    Attributes:
        cx (float) : Basin center x coordinate (units L, default 0.0).
        cy (float) : Basin center y coordinate (units L, default 0.0).
        lx (float) : Basin length in x direction (default 10.0)
        ly (float) : Basin length in y direction (default 10.0)
        rot (float) : Basin rotation angle in radians (default 0.0).
        name (str) : Basin name (default 'Unnamed').

    """
    is_rectangular = True
    is_circular = False
    def __init__(self, cx=0.0, cy=0.0, lx=10, ly=10, rot=0, name='Rectangle basin'):
        self.cx = cx
        self.cy = cy
        self.lx = lx
        self.ly = ly
        self.rot = rot
        self.name = name
        self.type = 'Rectangular Basin'
        return

    @property
    def lx(self):
        """float : Basin length in x direction.

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._lx
    @lx.setter
    def lx(self, v):
        if not (v > 0):
            raise Exception('Basin x length must be greater than 0.')
        self._lx = v

    @property
    def ly(self):
        """float : Basin length in y direction.

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._ly
    @ly.setter
    def ly(self, v):
        if not (v > 0):
            raise Exception('Basin y length must be greater than 0.')
        self._ly = v

    @property
    def rot(self):
        """float : Basin rotation angle in degrees.

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._rot
    @rot.setter
    def rot(self, v):
        if v <= -90 or v >= 90:
            raise Exception('Rotation angle must be between -90 and 90 deg.')
        self._rot = v

    @property
    def rot_rad(self):
        """float : Basin rotation angle in radians."""
        from pygaf.utils import deg2rad
        rad = deg2rad(self.rot)
        return rad

    @property
    def area(self):
        """float : Basin area."""
        return self.lx * self.ly

    @property
    def verts(self):
        """dict : x and y coordinates of basin verticies.

        Vertex keys: ll - lower left, ul - upper left, lr - lower right and
        ur - upper right.
        """
        values = {
            'll' : (self.cx-self.lx/2, self.cy-self.ly/2),
            'ul' : (self.cx-self.lx/2, self.cy+self.ly/2),
            'lr' : (self.cx+self.lx/2, self.cy-self.ly/2),
            'ur' : (self.cx+self.lx/2, self.cy+self.ly/2)
            }
        return values

    @property
    def verts_rot(self):
        """dict : x and y rotated coordinates of basin verticies.

        Vertex keys: ll - lower left, ul - upper left, lr - lower right and
        ur - upper right.
        """
        from pygaf.utils import rotate_point
        values = {
            'll' : rotate_point(
                self.cx, self.cy,
                self.verts['ll'][0], self.verts['ll'][1],
                self.rot_rad
                ),
            'ul' : rotate_point(
                self.cx, self.cy,
                self.verts['ul'][0], self.verts['ul'][1],
                self.rot_rad
                ),
            'lr' : rotate_point(
                self.cx, self.cy,
                self.verts['lr'][0], self.verts['lr'][1],
                self.rot_rad
                ),
            'ur' : rotate_point(
                self.cx, self.cy,
                self.verts['ur'][0], self.verts['ur'][1],
                self.rot_rad
                )
        }
        return values

    def info(self):
        """Print the basin information."""
        print('BASIN INFORMATION')
        print('-----------------')
        print('Type:', self.type)
        print('Name:', self.name)
        print('Basin center: (' + str(round(self.cx, 1)) + ', ' +\
            str(round(self.cy, 1)) + ') [L]')
        print('Basin x length:', self.lx, '[L]')
        print('Basin y length:', self.ly, '[L]')
        print('Basin area:', self.area, '[L2]')
        print('Clockwise rotation angle:', self.rot, '[deg]')
        print()
        return

    def draw(self, dw=4):
        """Display a drawing of the basin.

        Args:
            dw (float) : Width of basin drawing (default 4.0).

        """
        import matplotlib.pyplot as plt
        from matplotlib.patches import Polygon, Circle
        from pygaf.utils import rotate_point
        dl = max([self.lx, self.ly])/25
        fig = plt.figure(figsize=(dw, dw))
        fig.suptitle(self.name, fontsize=14, fontweight=530)
        ax = plt.gca()
        ax.add_patch(
            Polygon((self.verts_rot['ll'], self.verts_rot['lr'],
            self.verts_rot['ur'], self.verts_rot['ul']), fill=True,
            facecolor='silver', edgecolor='black', linewidth=2)
        )
        plt.plot(self.cx, self.cy, '.', color='black')
        ax.text(
            self.cx, self.cy-dl, '('+str(self.cx)+', '+str(self.cy)+')',
            fontsize=12, horizontalalignment='center',
            verticalalignment='center'
        )
        loc = rotate_point(
            self.cx, self.cy, self.cx, self.cy+dl+self.ly/2, self.rot_rad
        )
        ax.text(
            loc[0], loc[1], str(self.lx), fontsize=12,
            horizontalalignment='center', verticalalignment='center',
            rotation=-self.rot
        )
        loc = rotate_point(
            self.cx, self.cy, self.cx-dl-self.lx/2, self.cy, self.rot_rad
        )
        ax.text(
            loc[0], loc[1], str(self.ly), fontsize=12,
            horizontalalignment='center', verticalalignment='center',
            rotation=-self.rot+90
        )
        plt.axis('scaled')
        plt.axis('off')
        plt.tight_layout()
        plt.show()
        return
