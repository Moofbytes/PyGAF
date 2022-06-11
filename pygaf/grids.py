class WellGrid:
    """Square grid class with regular spacing and well at grid center.

    The default WellGrid object has radius gr=100 defining the square's
    extent and grid density gd=21. An exception occurs if the grid radius is
    not positive. Grid density defines the numbers of rows and columns
    comprising the grid; thus, the default grid has 21 rows x 21 cols = 441
    grid points. Minimum grid density is constrained to 11 (121 grid points)
    and maximum grid density is constrained to 41 (1681 grid points). Values
    for gd outside of these contraints are re-set to the minimum or maximum
    values as appropriate.

    The .pts property returns the grid points attriubutes including local
    x-y coordinates, world x-y coordinates and radius values relative to the
    well location. The .info method displays grid information and the .draw
    method displays a plot of the grid in either local or world coordinates.

    Attributes:
        gr (float) : Radius defining the extent of the solution grid (units L,
            default 100.0).
        gd (int) : Grid density defining the number of rows and columns;
            minimum and maximum constraints are enforced (default 21).

    """
    from .wells import SteadyWell
    def __init__(self, well=SteadyWell(), gr=100, gd=21):
        self.well = well
        self.gr = gr
        self.gd = gd
        self.max_gd = 41
        self.min_gd = 11

    @property
    def gr(self):
        """float : Grid radius.

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._gr

    @gr.setter
    def gr(self, v):
        if not (v > 0):
            raise Exception('Grid radius must be greater than 0.')
        self._gr = v

    @property
    def grdim(self):
        """int : Number of grid rows and columns."""
        if self.gd < self.min_gd:
            return self.min_gd
        elif self.gd > self.max_gd:
            return self.max_gd
        else:
            return int(self.gd)

    @property
    def npts(self):
        """int : Number of grid points."""
        return self.grdim**2

    @property
    def pts(self):
        """pandas dataframe : grid point attriubutes including local grid
        point coordinates, world grid point coordinates and radius values of
        grid points relative to the well center.
        """
        import pandas
        import numpy
        from pygaf.utils import add_constant_to_list
        df = pandas.DataFrame()
        row = list(numpy.linspace(-self.gr, self.gr, self.grdim))
        rows = [row for _ in range(self.grdim)]
        cols = [[row[i] for _ in range(self.grdim)] for i in range(self.grdim)]
        df['locx'] = list(numpy.array(rows).flat)
        df['locy'] = list(numpy.array(cols).flat)
        df['worldx'] = add_constant_to_list(list(df.locx), self.well.x)
        df['worldy'] = add_constant_to_list(list(df.locy), self.well.y)
        df['rad'] = numpy.sqrt(df.locx**2 + df.locy**2)
        return df

    def info(self):
        """Print the well grid information."""
        print('WELL GRID INFORMATION')
        print('---------------------')
        if self.npts == self.min_gd**2:
            print('Notice! grid spacing has been increased to enforce the',
            'minimum grid density of', self.min_gd**2, 'points.')
        if self.npts == self.max_gd**2:
            print('Notice! grid spacing has been decreased to enforce the',
            'maximum grid density of', self.max_gd**2, 'points.')
        print('Grid radius:', round(self.gr, 1))
        print('Number of grid points:', self.npts)
        print('Grid density:', self.grdim)
        print()
        return

    def draw(self, local=False):
        """Draw the grid points.

        Args:
            local (bool) : Display the grid plot in local coordinates with
                the well at 0, 0 (default False ).

        """
        from matplotlib import pyplot as plt
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))
        if local:
            x, y = list(self.pts.locx), list(self.pts.locy)
            cx, cy = 0, 0
            title = 'Well Grid in Local Coordinates'
        else:
            x, y = list(self.pts.worldx), list(self.pts.worldy)
            cx, cy = self.well.x, self.well.y
            title = 'Well Grid'
        ax.plot(x, y, '.', markersize=1, c='black')
        ax.plot(cx, cy, '.', c='red')
        ax.set_title(title)
        ax.axis('equal')
        plt.show()
        return

class BasinGrid:
    """ Square grid class with basin center at grid center.

    The default BasinGrid object has radius gr=100 defining the square's extent
    and grid density gd=21. An exception occurs if the grid radius is not
    positive. Grid density defines the numbers of rows and columns comprising
    the grid; thus, the default grid has 21 rows x 21 cols = 441 grid points.
    Minimum grid density is constrained to 11 (121 grid points) and maximum
    grid density is constrained to 41 (1681 grid points). Values for gd outside
    of these contraints are re-set to the minimum or maximum values as
    appropriate.

    The .pts property returns the grid points attriubutes including local
    x-y coordinates and world x-y coordinates. The .info method displays grid
    information and the .draw method displays a plot of the grid in either
    local or world coordinates.

    Attributes:
        gr (float) : Radius defining the extent of the solution grid (units L,
            default 100.0).
        gd (int) : Grid density defining the number of rows and columns;
            minimum and maximum constraints are enforced (default 21).

    """
    from .basins import Basin
    def __init__(self, basin=Basin(), gr=100, gd=21):
        self.basin = basin
        self.gr = gr
        self.gd = gd
        self.max_gd = 41
        self.min_gd = 11

    @property
    def gr(self):
        """float : Grid radius.

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._gr

    @gr.setter
    def gr(self, v):
        if not (v > 0):
            raise Exception('Grid radius must be greater than 0.')
        self._gr = v

    @property
    def grdim(self):
        """int : Number of grid rows and columns."""
        if self.gd < self.min_gd:
            return self.min_gd
        elif self.gd > self.max_gd:
            return self.max_gd
        else:
            return int(self.gd)

    @property
    def npts(self):
        """int : Number of grid points."""
        return self.grdim**2

    @property
    def pts(self):
        """pandas dataframe : grid point attriubutes including local grid
        point coordinates and world grid point coordinates.
        """
        import pandas
        import numpy
        from pygaf.utils import add_constant_to_list
        from pygaf.utils import rotate_grid
        df = pandas.DataFrame()
        row = list(numpy.linspace(-self.gr, self.gr, self.grdim))
        rows = [row for _ in range(self.grdim)]
        cols = [[row[i] for _ in range(self.grdim)] for i in range(self.grdim)]
        df['locx'] = list(numpy.array(rows).flat)
        df['locy'] = list(numpy.array(cols).flat)
        df['rotx'], df['roty'] = rotate_grid(
            0, 0, list(df.locx), list(df.locy), self.basin.rot_rad
        )
        df['worldx'] = add_constant_to_list(list(df.rotx), self.basin.cx)
        df['worldy'] = add_constant_to_list(list(df.roty), self.basin.cy)
        df['dx'] = list(df.locx)
        df['dy'] = list(df.locy)
        return df

    def info(self):
        """Print the basin grid information."""
        print('BASIN GRID INFORMATION')
        print('----------------------')
        if self.npts == self.min_gd**2:
            print('Notice! grid spacing has been increased to enforce the',
            'minimum grid density of', self.min_gd**2, 'points.')
        if self.npts == self.max_gd**2:
            print('Notice! grid spacing has been decreased to enforce the',
            'maximum grid density of', self.max_gd**2, 'points.')
        print('Grid radius:', round(self.gr, 1))
        print('Number of grid points:', self.npts)
        print('Grid density:', self.grdim)
        print()
        return

    def draw(self, local=False):
        """Draw the grid points.

        Args:
            local (bool) : Display the grid plot in local coordinates with
                the well at 0, 0 (default False).

        """
        from matplotlib import pyplot as plt
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))
        if local:
            x, y = list(self.pts.locx), list(self.pts.locy)
            cx, cy = 0, 0
            title = 'Basin Grid in Local Coordinates'
        else:
            x, y = list(self.pts.worldx), list(self.pts.worldy)
            cx, cy = self.basin.cx, self.basin.cy
            title = 'Basin Grid'
        ax.plot(x, y, '.', markersize=1, c='black')
        ax.plot(cx, cy, '.', c='red')
        ax.set_title(title)
        ax.axis('equal')
        plt.show()
        return
