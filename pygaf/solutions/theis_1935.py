class TheisWell:
    """Theis (1935) well solution class.

    The aquifer and well objects of the solution object have PyGAF default
    values.

    Attributes:
        aq (obj) : Confined aquifer object with default attributes.
        w (obj) : Steady state well object with default attributes.
        qf (float) : Fraction of pumped volume used for calculating radius of
            influence (default 0.99).

    """
    from pygaf.aquifers import Aq2dConf
    from pygaf.wells import SteadyWell
    def __init__(self, aq=Aq2dConf(), w=SteadyWell()):
        self.aq = aq
        self.well = w
        self.qf = 0.99
        return

    @property
    def qfp(self):
        """float : Fraction of pumped volume."""
        return self.qf

    def info(self):
        """Print the solution information.

        Returns:
            Screen printout of solution information.

        """
        print('METHOD REFERENCE')
        print('----------------')
        print(
        'Theis C. V. (1935) - The relation between the lowering of the' +
        '\npiezometric surface and the rate and duration of discharge of a' +
        '\nwell using ground-water storage.'
        )
        print('\nConceptual Model:')
        print('- Infinite, confined, uniform and homogeneous aquifer.')
        print('- Radial groundwater flow.')
        print('- Groundwater recharge neglected.')
        print('- Steady state and fully penetrating well.')
        print()

    def ri(self, t=[1], plot=True, csv='', xlsx=''):
        """Calculate radius of influence at specified times.

        Radius of influence is defined as the radius from within which a
        specified faction qf of the pumped volume has been drawn. The default
        value for qf is 0.99, defining the radius from which 99% of the pumped
        volume has been drawn.

        The method evaluates the radius of influence for each time supplied in
        a list of times t and displays a plot of the results as default. The
        results plot can be suppressed by setting the method attribute
        plot=False. The method returns a pandas dataframe with time as the row
        index and radius of influence as a single column.

        Results can be exported to csv and Excel files if non-blank strings are
        set for the .csv and/or .xlsx attributes. File names can be supplied
        with or without file extentions, which are added if ommitted.

        Args:
            t (float) : List of times to evaluate radius of influence
                (default [1.0]).
            plot (bool) : Display a plot of results (default True).
            csv (str) : Filepath for export of results to csv file; results
                are exported if the string is not empty (default '').
            xlsx (str) : Filepath for export of result to xlsx file; results
                are exported if the string is not empty (default '').

        Returns:
            Pandas dataframe containing results.

        """
        from numpy import sqrt, log
        import pandas
        # Checks
        if self.qfp < 0 or self.qfp > 1:
            print('Error! The value of qf must be between 0 and 1.')
            return
        if min(t) <= 0:
            print('Error! All times must be greater than 0.')
            return
        # Radius of influence
        ri = []
        for tim in t:
            ri.append(sqrt(-4.0 * self.aq.T * tim * log(1-self.qfp) / self.aq.S))
        d = {'Time':t, 'ri':ri}
        df = pandas.DataFrame(data=d)
        df.set_index('Time', inplace=True)
        # Results plot
        if plot:
            import matplotlib.pyplot as plt
            df.plot(grid=True, marker='.', ylabel='Radius')
            plt.xlim(0, None)
            plt.ylim(0, None)
            plt.title('Radius of Influence\n' +
                'T = ' + str(self.aq.T) +
                ', S = ' + str(self.aq.S) +
                ', q =' + str(self.well.q) +
                ', qf = ' + str(self.qfp)
                )
            plt.show()
        # Export result to csv
        if csv != '':
            if csv.split('.') != 'csv':
                csv = csv + '.csv'
            df.to_csv(csv)
            print('Results exported to:', csv)
        # Export result to Excel
        if xlsx != '':
            if xlsx.split('.') != 'xlsx':
                xlsx = xlsx + '.xlsx'
            df.to_excel(xlsx, sheet_name='ri')
            print('Results exported to:', xlsx)
        return df

    def dd(self, t=[1], r=[1], plot=True, csv='', xlsx=''):
        """Calculate drawdown at specified radii and times.

        This method calculates drawdown at each radius and each time supplied.
        Radius and time are both supplied in lists.  A results plot is displayed
        as default and can be suppressed by setting plot=False.

        The method returns a pandas dataframe with time as the row index and
        radius values as the columns.

        Results can be exported to csv and Excel files if non-blank strings are
        set for the .csv and/or .xlsx attributes. File names can be supplied
        with or without file extentions, which are added if ommitted.

        Args:
            t (float) : List of times to evaluate drawdown (default [1.0]).
            r (float) : List of radii to evaluate drawdown (default [1])
            plot (bool) : Display a plot of results (default True).
            csv (str) : Filepath for export of results to csv file; results
                are exported if the string is not empty (default '').
            xlsx (str) : Filepath for export of result to xlsx file; results
                are exported if the string is not empty (default '').

        Returns:
            Pandas dataframe containing results.

        """
        from numpy import pi
        from scipy.special import expn
        import pandas
        # Checks
        if min(t) <= 0 or min(r) <= 0:
            print('Error! All times and radii must be greater than 0.')
            return
        # Calculate drawdown
        d = {'Time':t}
        df = pandas.DataFrame(data=d)
        df.set_index('Time', inplace=True)
        for rad in r:
            drawdown = []
            for tim in t:
                u = (rad**2) * self.aq.S / (4.0 * self.aq.T * tim)
                W = expn(1, u) # Well Function
                dd = self.well.q * W / (4.0 * pi * self.aq.T)
                drawdown.append(dd)
            df['r' + str(rad)] = drawdown
        # Plot results
        if plot:
            import matplotlib.pyplot as plt
            df.plot(grid=True, marker='.', ylabel='Displacement')
            plt.title('Drawdown\n' +
                'T = ' + str(self.aq.T) +
                ', S = ' + str(self.aq.S) +
                ', q = ' + str(self.well.q)
                )
            plt.legend(
                r, ncol=5, mode='expand', loc='upper left',
                bbox_to_anchor=(0,-0.1, 1, -0.1)
            )
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

    def dd_grid(self, t=1, gr=100, gd=21, plot=True, local=False, csv='',
    xlsx=''):
        """Calculate drawdown values on a regular grid.

        The method evaluates drawdown on a grid of points for the specified
        well pumping rate q and time t.

        Results are returned in a Pandas dataframe with columns x-coordinate,
        y-coordinate and drawdown values. A results plot is displayed as default
        and can be suppressed by setting plot=False.

        Unless otherwise specified, the solution uses a default well grid object
        with radius 100 and grid density 21 (441 grid points). Other values can
        be specified using the methods grid radius .gr and grid density .gd
        attributes.

        Args:
            t (float) : Time to evaluate drawdown (default 1.0).
            gr (float) : Radius defining the extent of the solution grid
                (default 100.0).
            gd (int) : Grid density defining the number of gird rows and
                columns; minimum and maximum constraints are enforced
                (default 21).
            plot (bool) : Display a plot of results (default True).
            local (bool) : Display the drawdown plot in 'local' coordinates
                with the well at 0, 0 (Default False).
            csv (str) : Filepath for export of results to csv file; results
                are exported if the string is not empty (default '').
            xlsx (str) : Filepath for export of result to xlsx file; results
                are exported if the string is not empty (default '').

        Returns:
            Pandas dataframe containing results.

        """
        from pygaf.grids import WellGrid
        from numpy import pi
        from scipy.special import expn
        import matplotlib.pyplot as plt
        #from matplotlib import ticker
        import pandas
        self.gr = gr
        self.gd = gd
        self.grid = WellGrid(well=self.well, gr=self.gr, gd=self.gd)
        # Set coordinates
        if local:
            x, y = list(self.grid.pts.locx), list(self.grid.pts.locy)
            wx, wy = 0, 0
            plot_title = 'Drawdown at radius < ' + str(self.grid.gr) +\
            ' and t = ' + str(t) + '\n(local coordinates)'
        else:
            x, y = list(self.grid.pts.worldx), list(self.grid.pts.worldy)
            wx, wy = self.grid.well.x, self.grid.well.y
            plot_title = 'Drawdown at radius < ' + str(self.grid.gr) +\
            ' and t = ' + str(t) + '\n(world coordinates)'
        # Calculate drawdown
        radius, drawdown = [], []
        for i in range(self.grid.npts):
            r = self.grid.pts.rad[i]
            if r <= self.grid.well.r:
                r = self.grid.pts.rad[i-1]
            u = (r**2) * self.aq.S / (4.0 * self.aq.T * t)
            W = expn(1, u)
            dd = self.grid.well.q * W / (4.0 * pi * self.aq.T)
            radius.append(r)
            drawdown.append(dd)
        # Plot results
        mid_row = int(self.grid.grdim/2)
        if plot:
            cm = plt.cm.get_cmap('Blues').reversed()
            fig, (ax1, ax2) = plt.subplots(
            2, 1, gridspec_kw={'height_ratios': [4, 1]}, figsize=(6, 7.6)
            )
            fig.suptitle(plot_title, fontsize=14)
            fig.suptitle(plot_title, fontsize=14)
            ax1.tricontourf(x, y, drawdown, cmap=cm)
            cs = ax1.tricontour(
                x, y, drawdown, linewidths=0.25, colors=['black']
            )
            ax1.clabel(cs, inline=1, fontsize=10)
            ax1.plot(wx, wy, '.', c='red')
            ax1.set_title('Displacement Contours')
            ax1.grid(True)
            ax1.axis('equal')
            ax2.plot(
                x[self.grid.grdim*(mid_row-1):self.grid.grdim*mid_row],
                drawdown[self.grid.grdim*(mid_row-1):self.grid.grdim*mid_row],
                lw=2
            )
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
