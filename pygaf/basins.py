class Basin:
    """Parent basin class."""
    def __init__(self, cx, cy, name):
        self.cx = cx
        self.cy = cy
        self.name = name
        return

class RectBasin(Basin):
    """
    Rectangular basin.

    Arguments:
    ---------
    cx : float
        Basin center x coordinate (default 0.0)
    cy : float
        Basin center y coordinate (default 0.0)
    lx : float
        Basin length in x direction (default 10)
    ly : float
        Basin length in y direction (default 10)
    name : str
        Basin name (default '')
    """
    is_rectangular = True
    is_circular = False
    def __init__(self, cx=0.0, cy=0.0, lx=10, ly=10, name='unnamed'):
        super().__init__(cx, cy, name)
        self.lx = lx
        self.ly = ly
        self.type = 'Rectangular basin'
        self.title = self.type
        return

    @property
    def lx(self):
        return self._lx
    @lx.setter
    def lx(self, v):
        if not (v > 0):
            raise Exception('Basin x length must be greater than 0.')
        self._lx = v

    @property
    def ly(self):
        return self._ly
    @ly.setter
    def ly(self, v):
        if not (v > 0):
            raise Exception('Basin y length must be greater than 0.')
        self._ly = v

    @property
    def area(self):
        """Basin area."""
        return self.lx * self.ly

    def info(self):
        """Print the basin information."""
        print('BASIN INFORMATION')
        print('-----------------')
        print('Type:', self.type)
        print('Name:', self.name)
        print('Basin center:', round(self.cx, 1), ',', round(self.cy, 1))
        print('Basin x length:', self.lx, '[L]')
        print('Basin y length:', self.ly, '[L]')
        print('Basin area:', self.area, '[L2]')
        return

    def draw(self, dw=5):
        """
        Display the basin as a picture.

        Arguments:
        ---------
        dw : float
            Width of aquifer drawing (default 5)
        """
        import matplotlib.pyplot as plt
        w = self.lx
        h = self.ly
        cx=self.cx
        cy=self.cy
        dl = max([w, h])/50
        plt.figure(figsize=(dw, dw))
        ax = plt.gca()
        ax.add_patch(plt.Rectangle((-w/2, -h/2), width=w, height=h, facecolor='silver', edgecolor='black', linewidth=2)) # basin
        ax.add_line(plt.Line2D(((-w/2)-dl, (w/2)+dl), (0, 0), color='grey', linestyle='-.', linewidth=1)) # x axis
        ax.add_line(plt.Line2D((0, 0), ((-h/2)-dl, (h/2)+dl), color='grey', linestyle='-.', linewidth=1)) # y axis
        ax.arrow(0, (h/2)+(2*dl), (w/2)-dl, 0, overhang=1, head_width=dl, color='black', linewidth=0.5, fill=False)
        ax.arrow(0, (h/2)+(2*dl), -(w/2)+dl, 0, overhang=1, head_width=dl, color='black', linewidth=0.5, fill=False)
        ax.arrow(-(w/2)-(2*dl), 0, 0, (h/2)-dl, overhang=1, head_width=dl, color='black', linewidth=0.5, fill=False)
        ax.arrow(-(w/2)-(2*dl), 0, 0, -(h/2)+dl, overhang=1, head_width=dl, color='black', linewidth=0.5, fill=False)
        ax.text(0, (-h/2)-dl, self.title, fontsize=12, horizontalalignment='center', verticalalignment='top')
        ax.text(0, 0, '('+str(cx)+', '+str(cy)+')', fontsize=12, horizontalalignment='center', verticalalignment='bottom')
        ax.text(0, (h/2)+(2*dl), w, fontsize=12, horizontalalignment='center', verticalalignment='bottom')
        ax.text(-(w/2)-(2*dl), 0, h, fontsize=12, horizontalalignment='right', verticalalignment='center', rotation=90)
        plt.axis('scaled')
        plt.axis('off')
        plt.show()
        return

class CircBasin(Basin):
    """
    Circular basin.

    Arguments:
    ---------
    cx : float
        Basin center x coordinate (default 0.0)
    cy : float
        Basin center y coordinate (default 0.0)
    diam : float
        Basin diameter (default 10)
    name : str
        Basin name (default '')
    """
    is_rectangular = False
    is_circular = True
    def __init__(self, cx=0.0, cy=0.0, diam=10, name='unnamed'):
        super().__init__(cx, cy, name)
        self.diam = diam
        self.type = 'Circular basin'
        self.title = self.type
        return

    @property
    def diam(self):
        return self._diam
    @diam.setter
    def diam(self, v):
        if not (v > 0):
            raise Exception('Basin diameter must be greater than 0.')
        self._diam = v

    @property
    def rad(self):
        """Basin radius."""
        return self.diam / 2

    @property
    def area(self):
        """Basin area."""
        from numpy import pi
        return pi * self.rad**2

    def info(self):
        """Print the basin information."""
        print('BASIN INFORMATION')
        print('-----------------')
        print('Type:', self.type)
        print('Name:', self.name)
        print('Basin center:', round(self.cx, 1), ',', round(self.cy, 1))
        print('Basin diameter:', self.diam, '[L]')
        print('Basin radius:', self.rad, '[L]')
        print('Basin area:', round(self.area, 1), '[L2]')
        return

    def draw(self, dw=3.5):
        """
        Display the basin as a picture.

        Arguments:
        ---------
        dw : float
            Width of aquifer drawing (default 5)
        """
        import matplotlib.pyplot as plt
        r = self.rad
        dr = r/25
        cx=self.cx
        cy=self.cy
        plt.figure(figsize=(dw, dw))
        ax = plt.gca()
        ax.add_patch(plt.Circle((0, 0), radius=self.rad, facecolor='silver', edgecolor='black', linewidth=2)) # basin
        ax.add_line(plt.Line2D((-r-dr, r+dr), (0, 0), color='grey', linestyle='-.', linewidth=1)) # x axis
        ax.add_line(plt.Line2D((0, 0), (-r-dr, r+dr), color='grey', linestyle='-.', linewidth=1)) # y axis
        ax.arrow(0, 0, 0.65*r, 0.65*r, overhang=1, head_width=1.5*dr, color='black', linewidth=0.5, fill=False)
        ax.text(0.5*r, 0.5*r, round(r, 1), fontsize=12, horizontalalignment='center', verticalalignment='top', rotation=45)
        ax.text(0, -r-(2*dr), self.title, fontsize=12, horizontalalignment='center', verticalalignment='top')
        ax.text(0, 0, '('+str(cx)+', '+str(cy)+')', fontsize=12, horizontalalignment='center', verticalalignment='top')
        plt.axis('scaled')
        plt.axis('off')
        plt.show()
        return
