class DupuitThiemWell:
    """Dupuit-Thiem radial flow solution for uniform recharge.

    The default DupuitThiemWell object adopts the Aq2dUnconf, SteadyWellGrid
    and SteadyWell classes. Methods include drawdown at a point (.dd) and
    drawdown on a regular grid of points (.dd_grid).

    Attributes:
        aq (obj) : Aq2dUnconf aquifer object.
        grd (obj) : SteadyWellGrid object.
        well (obj) : SteadyWell object.
    """
    from pygaf.aquifers import Aq2dUnconf
    from pygaf.grids import SteadyWellGrid
    def __init__(self):
        self.aq = self.Aq2dUnconf()
        self.grid = self.SteadyWellGrid()
        self.well = self.grid.well
        self.well.q = -1000
        self.R = 1.0e-4
        return
    
    @property
    def R(self):
        """float : Groundwater recharge rate (units L/T, default 1.0e-4).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._R

    @R.setter
    def R(self, v):
        if not (v > 0):
            raise Exception('Recharge rate (R) must be positive.')
        self._R = v
    
    def info(self):
        """Print the solution information."""
        print('METHOD REFERENCE')
        print('----------------')
        print('Conceptual Model:')
        print('- Infinite, uniform and homogeneous aquifer.')
        print('- Dupuit–Forchheimer assumption (relatively flat water table.')
        print('- Steady state radial groundwater flow.')
        print('- Steady state and fully penetrating well.')
        print('- Uniform groundwater recharge.')
        print()
    
    def draw(self, dw=8):
        """Display the definition diagram.

        Args:
            dw (float) : Width of figure (default 8.0).

        """
        from pygaf.utils import display_image
        display_image('DupuitThiemWell.png', dw=dw)
        return
        
    def ri(self):
        """Radius of influence."""
        from numpy import absolute, pi, sqrt
        Q = absolute(self.well.q)
        R = self.R
        return sqrt(Q/(pi*R))
    
    def disp(self, r, T, Q):
        """Drawdown displacement."""
        from numpy import log, pi
        RI = self.ri()
        return Q * log(RI/r) / (2.0 * pi * T)
    
    
    def dd(self, r=[1], plot=True, csv='', xlsx=''):
        """Drawdown at radial distance."""
        import pandas
        # Checks
        if self.well.q >= 0:
            print('Error! Pumping must be negative (extract).')
            return
        if min(r) <= 0:
            print('Error! All radius values must be greater than zero.')
            return
        r.sort()
        d = {'Radius':r}
        df = pandas.DataFrame(data=d)
        df.set_index('Radius', inplace=True)
        DD = []
        for i, rad in enumerate(r):
            DD.append(self.disp(rad, self.aq.T, self.well.q))
        df['displacement'] = DD
        print('Aquifer transmissivity:', self.aq.T)
        print('Pumping rate:', self.well.q)
        print('Radius of influence:', round(self.ri(),0))
        # Plot results
        if plot:
            import matplotlib.pyplot as plt
            df.plot(grid=True, marker='.', lw=3, alpha=0.5, ylabel='Displacement')
            plt.title('Drawdown\n' + 'T = ' + str(self.aq.T) + ', q = ' + str(self.well.q))
            plt.show()
        # Export results
        if csv != '':
            if csv.split('.') != 'csv':
                csv = csv + '.csv'
            df.to_csv(csv)
            print('Results exported to:', csv)
        if xlsx != '':
            if xlsx.split('.') != 'xlsx':
                xlsx = xlsx + '.xlsx'
            df.to_excel(xlsx, sheet_name='ri')
            print('Results exported to:', xlsx)
        return df
    
    def dd_grid(self, plot=True, local=False, csv='', xlsx=''):
        """Evaluate drawdown on a regular grid of points.

        Unless otherwise specified, a default WellGrid object is used and
        is accessed and adjusted via the .grid.gr (grid radius) and .grid.gd
        (grid density) attributes.

        Results are returned in a Pandas dataframe with columns x-coord,
        y-coord and drawdown value. A drawdown graph is displayed as default
        and can be suppressed by setting plot=False.

        Args:
            plot (bool) : Display a plot of results (default True).
            local (bool) : Display the results in 'local' coordinates with the
                well at coordinates 0.0, 0.0 (Default False).
            csv (str) : Full filepath for export of results to csv file;
                results are exported if the string is not empty (default '').
            xlsx (str) : Full filepath for export of result to xlsx file;
                results are exported if the string is not empty (default '').

        Returns:
            Results in a pandas dataframe.

        """
        import matplotlib.pyplot as plt
        import pandas
        # Set well grid radius to radius of influence
        self.grid.gr = self.ri()
        # Set coordinates
        if local:
            x, y = list(self.grid.pts.locx), list(self.grid.pts.locy)
            wx, wy = 0, 0
        else:
            x, y = list(self.grid.pts.worldx), list(self.grid.pts.worldy)
            wx, wy = self.well.x, self.well.y
        # Calculate drawdown
        radius, drawdown = [], []
        for i in range(self.grid.npts):
            r = self.grid.pts.rad[i]
            if r <= self.well.r:
                r = self.grid.pts.rad[i-1]
            dd = self.disp(r, self.aq.T, self.well.q)
            radius.append(r)
            drawdown.append(dd)
        # Plot results
        mid_row = int(self.grid.grdim/2)
        plot_title = 'Drawdown for R = ' + str(self.R) +\
        '\nT = ' + str(self.aq.T) + ', S = ' + str(self.aq.S) + ', q = ' +\
        str(self.well.q) + ', ri = ' + str(round(self.ri(),0))
        if plot:
            cm = plt.cm.get_cmap('Blues').reversed()
            fig, (ax1, ax2) = plt.subplots(
            2, 1, gridspec_kw={'height_ratios': [4, 1]}, figsize=(6, 7.6)
            )
            fig.suptitle(plot_title, fontsize=14)
            ax1.tricontourf(x, y, drawdown, cmap=cm)
            cs = ax1.tricontour(
                x, y, drawdown, linewidths=0.25, colors=['black']
            )
            ax1.clabel(cs, inline=1, fontsize=10)
            ax1.plot(wx, wy, '.', c='red')
            if local:
                ax1.set_title('Displacement Contours (local)')
            else:
                ax1.set_title('Displacement Contours')
            ax1.grid(True)
            ax1.axis('equal')
            ax2.plot(
                x[self.grid.grdim*(mid_row-1):self.grid.grdim*mid_row],
                drawdown[self.grid.grdim*(mid_row-1):self.grid.grdim*mid_row],
                '.-', lw=3, alpha=0.5
            )
            if local:
                ax2.set_title('Radial Displacement (local)')
            else:
                ax2.set_title('Radial Displacement')
            ax2.grid(True)
            plt.show()
            plt.close()
        # Export result
        df = pandas.DataFrame()
        df['x'] = x
        df['y'] = y
        df['radius'] = radius
        df['drawdown'] = drawdown
        if csv != '':
            if csv.split('.') != 'csv':
                csv = csv + '.csv'
            df.to_csv(csv, index=False)
            print('Results exported to:', csv)
        if xlsx != '':
            if xlsx.split('.') != 'xlsx':
                xlsx = xlsx + '.xlsx'
            df.to_excel(xlsx, sheet_name='drawdown', index=False)
            print('Results exported to:', xlsx)
        return df