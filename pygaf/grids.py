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
        from numpy import sqrt
        self.well = well
        self.gr = gr
        self.gs = gs
        self.max_points = 2500
        self.min_points = 25
        # Checks
        if self.gr <= 0 or self.gs <= 0:
            print('Error! Grid radius and spacing must be greater than 0.')
            return
        if self.gs >= self.gr:
            print('Error! Grid spacing must be less than grid radius.')
            return
        # Grid setup
        num_points = (1 + 2*self.gr/self.gs)**2
        if num_points > self.max_points:
            self.gs = 2*self.gr/(sqrt(self.max_points)-1)
            num_points = (1 + 2*self.gr/self.gs)**2
            print('Notice! the number of grid points exceeds', self.max_points)
            print('The grid spacing is re-set to', round(self.gs, 3))
        elif num_points < self.min_points:
            self.gs = self.gr/2
            num_points = (1 + 2*self.gr/self.gs)**2
            print('Notice! the number of grid points subceeds', self.min_points)
            print('The grid spacing is re-set to', round(self.gs, 3))
        #self.nrow = int(sqrt(num_points))
        #self.ncol = int(sqrt(num_points))
        print('Number of grid points is', round(num_points, 0))
        #self.local_x = list(linspace(-self.gr, self.gr, num_grid_lines))
        #self.local_y = list(linspace(-self.gr, self.gr, num_grid_lines))
        #self.world_x = [x + self.well.x for x in self.local_x]
        #self.world_y = [y + self.well.y for y in grid_local_y]
        #grid_r = [
            #[sqrt(x**2 + y**2) for x in self.local_x]
            #for y in grid_local_y
            #]
        #print(self.local_x)
        #print(grid_world_x)
    @property
    def num_points(self):
        if self.gr <= 0 or self.gs <= 0:
            print('Error! Grid radius and spacing must be greater than 0.')
            return
        elif self.gs >= self.gr:
            print('Error! Grid spacing must be less than grid radius.')
            return


    @property
    def local_x(self):
        """Local x coordinates of the grid."""
        return list(linspace(-self.gr, self.gr, self.ncol))


        return
