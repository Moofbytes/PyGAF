class WellGrid:
    """
    Rectangular well grid with well at the center.

    Arguments:
    ---------
    gr : float
        Radius defining the extent of the solution grid (default 100)
    gd : float
        Grid density defining the number of rows/columns - minimum and maximum
        constraints enforced (default 20)
    csv : str
        Filepath of csv file for results export (default '' - no export)
    """
    from .wells import SteadyWell
    def __init__(self, well=SteadyWell(), gr=100, gd=20, plot=True, csv=''):
        self.well = well
        self.gr = gr
        self.gd = gd
        self.max_gd = 40
        self.min_gd = 10

    @property
    def gr(self):
        return self._gr
    @gr.setter
    def gr(self, v):
        if not (v > 0):
            raise Exception('Grid radius must be greater than 0.')
        self._gr = v

    @property
    def grdim(self):
        """Number of grid rows and columns."""
        if self.gd < self.min_gd:
            return self.min_gd
        elif self.gd > self.max_gd:
            return self.max_gd
        else:
            return int(self.gd)

    @property
    def npts(self):
        """Number of grid points."""
        return self.grdim**2

    @property
    def locx(self):
        """Local x coordinates of the grid."""
        from numpy import linspace
        row = list(linspace(-self.gr, self.gr, self.grdim))
        return [row for _ in range(self.grdim)]

    @property
    def locy(self):
        """Local y coordinates of the grid."""
        from numpy import linspace
        col = list(linspace(-self.gr, self.gr, self.grdim))
        return [col for _ in range(self.grdim)]

    @property
    def worldx(self):
        """World x coordinates of the grid"""
        wx = [
        [x + self.well.x for x in self.locx[r]]
        for r in range(self.grdim)
        ]
        return wx

    @property
    def worldy(self):
        """World y coordinates of the grid"""
        wy = [
        [y + self.well.y for y in self.locy[r]]
        for r in range(self.grdim)
        ]
        return wy

    @property
    def rad_pts(self):
        """Radii of grid points from well."""
        from numpy import sqrt
        r = [
        [sqrt(self.locx[i][j]**2 + self.locy[j][i]**2)
        for i in range(self.grdim)]
        for j in range(self.grdim)
        ]
        return r

    def info(self):
        """Print the well grid information."""
        print('WELL GRID INFORMATION')
        print('---------------------')
        if self.npts == self.min_gd**2:
            print('Notice! grid spacing may have been increased to enforce the',
            'minimum grid density of', self.min_gd**2, 'points.')
        if self.npts == self.max_gd**2:
            print('Notice! grid spacing may have been decreased to enforce the',
            'maximum grid density of', self.max_gd**2, 'points.')
        print('Grid radius:', round(self.gr, 1))
        print('Number of grid points:', self.npts)
        print('Number of grid rows:', self.grdim)
        return

    def draw(self, world=False):
        """
        Draw the grid points.

        Arguments:
        ---------
        world : bool
            Display the grid plot in 'local' or 'world' coordinates (Default
            'local' with well at 0, 0)
        """
        from matplotlib import pyplot as plt
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))
        if not world:
            for i in range(self.grdim):
                for j in range(self.grdim):
                    ax.plot(
                    self.locx[i][j], self.locy[j][i], '.', markersize=1,
                    c='black'
                    )
            ax.plot(0, 0, 'o', c='red')
            ax.set_title('Well Grid in Local Coordinates')
            ax.axis('equal')
        else:
            for i in range(self.grdim):
                for j in range(self.grdim):
                    ax.plot(
                    self.worldx[i][j], self.worldy[j][i], '.', markersize=1,
                    c='black'
                    )
            ax.plot(self.well.x, self.well.y, 'o', c='red')
            ax.set_title('Well Grid in World Coordinates')
            ax.axis('equal')
        plt.show()
        return
