class WellGrid:
    """
    Rectangular well grid with well at the center.

    Arguments:
    ---------
    gr : float
        Radius defining the extent of the solution grid (default 100)
    gs : float
        Grid spacing (default 10)
    csv : str
        Filepath of csv file for results export (default '' - no export)
    """
    from .wells import SteadyWell
    def __init__(self, well=SteadyWell(), gr=100, gs=10, plot=True, csv=''):
        self.well = well
        self.gr = gr
        self.gs = gs
        self.max_pts = 2500
        self.min_pts = 25

    @property
    def gr(self):
        return self._gr
    @gr.setter
    def gr(self, v):
        if not (v > 0):
            raise Exception('Grid radius must be greater than 0..')
        self._gr = v

    @property
    def gs(self):
        return self._gs
    @gs.setter
    def gs(self, v):
        if not (v > 0):
            raise Exception('Grid spacing must be greater than 0.')
        self._gs = v

    @property
    def npts(self):
        """Number of grid points."""
        from numpy import sqrt
        np = round((1 + 2*self.gr/self.gs)**2)
        if np > self.max_pts:
            self.gs = 2*self.gr/(sqrt(self.max_pts)-1)
            return round((1 + 2*self.gr/self.gs)**2)
        elif np < self.min_pts:
            self.gs = self.gr/2
            return round((1 + 2*self.gr/self.gs)**2)
        else:
            return np

    @property
    def grdim(self):
        """Number of grid rows and columns."""
        from numpy import sqrt
        nrow = round(sqrt(self.npts))
        return nrow

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
        if self.npts == self.min_pts:
            print('Notice! grid spacing was increased to achieve minimum',
            self.min_pts, 'grid points.')
        if self.npts == self.max_pts:
            print('Notice! grid spacing was decresed to achieve maximum',
            self.max_pts, 'grid points.')
        print('Grid radius:', round(self.gr, 1))
        print('Grid spacing:', round(self.gs, 2))
        print('Number of rows:', self.grdim)
        print('Number of cols:', self.grdim)

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
        if not world:
            for i in range(self.grdim):
                for j in range(self.grdim):
                    plt.plot(self.locx[i][j], self.locy[j][i], '.', c='grey')
            plt.plot(0, 0, 'o', c='red')
            plt.title('Well Grid in Local Coordinates')
            plt.axis('equal')
            plt.show()
        else:
            for i in range(self.grdim):
                for j in range(self.grdim):
                    plt.plot(self.worldx[i][j], self.worldy[j][i], '.', c='grey')
            plt.plot(self.well.x, self.well.y, 'o', c='red')
            plt.title('Well Grid in World Coordinates')
            plt.axis('equal')
            plt.show()
        return
