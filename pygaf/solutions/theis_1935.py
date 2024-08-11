class TheisWell:
    """Theis (1935) radial flow solution.

    The default TheisWell object uses the Aq2dConf, SteadyWellGrid and
    SteadyWell classes. Methods include radius of influence .ri, transient
    drawdown at a point .dd and grid-contoured drawdown at specified time
    .dd_grid.

    Attributes:
        aq (obj) : Aq2dConf aquifer object.
        grd (obj) : SteadyWellGrid object.
        well (obj) : SteadyWell object.
        qf (float) : Fraction of pumped volume used for calculating radius of
            influence (default 0.99).

    """
    from pygaf.aquifers import Aq2dConf
    from pygaf.grids import SteadyWellGrid
    def __init__(self):
        self.aq = self.Aq2dConf()
        self.grid = self.SteadyWellGrid()
        self.well = self.grid.well
        self.well.q = -1000
        self.qf = 0.99
        return

    @property
    def qfp(self):
        """float : Fraction of pumped volume."""
        return self.qf

    def info(self):
        """Print the solution information."""
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
        print('- Steady state and fully penetrating well.')
        print('- No groundwater recharge.')
        print()

    def rinf(self, T, S, t, qf):
        """Radius of influence."""
        from numpy import sqrt, log
        return sqrt(-4.0 * T * t * log(1-qf) / S)

    def disp(self, r, S, T, t, Q):
        """Drawdown displacement."""
        from numpy import pi
        from scipy.special import expn
        u = (r**2) * S / (4.0 * T * t)
        W = expn(1, u) # Well Function
        return Q * W / (4.0 * pi * T)


    def ri(self, t=[1.0], plot=True, csv='', xlsx=''):
        """Calculate radius of influence at specified times.

        Radius of influence is defined as the radius from within which a
        specified faction qf of the pumped volume has been drawn. The default
        value for qf is 0.99, corresponding to the radius from which 99% of the
        pumped volume has been drawn.

        Time for calculating ri are provided in a list. A results graph is
        displayed as default and can be suppressed by setting plot=False. A
        pandas dataframe is returned with time as the row index and ri as
        a column.

        Results can be exported to csv and Excel files by setting non-blank
        filename strings for the .csv and .xlsx attributes. Filenames can be
        supplied with or without file extentions, which are added if ommitted.

        Args:
            t (float) : List of times to evaluate radius of influence
                (default [1.0]).
            plot (bool) : Display a plot of results (default True).
            csv (str) : Full filepath for export of results to csv file;
                results are exported if the string is not empty (default '').
            xlsx (str) : Full filepath for export of result to xlsx file;
                results are exported if the string is not empty (default '').

        Returns:
            Results in pandas dataframe.

        """
        import pandas
        # Checks
        if self.qfp < 0 or self.qfp > 1:
            print('Error! The value of qf must be between 0 and 1.')
            return
        if min(t) <= 0:
            print('Error! All times must be greater than 0.')
            return
        # Radius of influence
        t.sort()
        ri = []
        for tim in t:
            ri.append(self.rinf(self.aq.T, self.aq.S, tim, self.qfp))
        d = {'Time':t, 'ri':ri}
        df = pandas.DataFrame(data=d)
        df.set_index('Time', inplace=True)
        # Results plot
        if plot:
            import matplotlib.pyplot as plt
            df.plot(grid=True, marker='.', lw=3, alpha=0.5, ylabel='Radius')
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
        """Evaluate drawdown at specified radii and times.

        Evaluate drawdown at each radius and time specified in the lists t
        and r and for well rate q. Defaults are t=[1.0], r=[1.0] and
        q=-1000.0. A drawdown graph is displayed as default and can be
        suppressed by setting plot=False.

        A pandas dataframe of drawdown values is returned with time as the row
        index and radius values as the column headers. Results can be exported
        to csv and Excel files by setting non-blank filename strings for the
        .csv and .xlsx attributes. Filenames can be supplied with or without
        file extentions, which are added if ommitted.

        Args:
            t (float) : List of times to evaluate drawdown (default [1.0]).
            r (float) : List of radii to evaluate drawdown (default [1.0]).
            plot (bool) : Display a plot of results (default True).
            csv (str) : Full filepath for export of results to csv file;
                results are exported if the string is not empty (default '').
            xlsx (str) : Full filepath for export of result to xlsx file;
                results are exported if the string is not empty (default '').

        Returns:
            Results in a pandas dataframe.

        """
        import pandas
        # Checks
        if min(t) <= 0 or min(r) <= 0:
            print('Error! All times and radii must be greater than 0.')
            return
        # Calculate drawdown
        t.sort()
        d = {'Time':t}
        df = pandas.DataFrame(data=d)
        df.set_index('Time', inplace=True)
        for rad in r:
            drawdown = []
            for tim in t:
                dd = self.disp(rad, self.aq.S, self.aq.T, tim, self.well.q)
                drawdown.append(dd)
            df['r' + str(rad)] = drawdown
        # Plot results
        if plot:
            import matplotlib.pyplot as plt
            df.plot(
                grid=True, marker='.', lw=3, alpha=0.5, ylabel='Displacement'
                )
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

    def dd_grid(self, t=1.0, plot=True, local=False, csv='', xlsx=''):
        """Evaluate drawdown on a regular grid.

        Evaluate drawdown on a grid of points at specified time and well rate.
        Default values are t=1.0 and q=-1000. Unless otherwise specified, a
        default WellGrid object is used; it can be accessed and adjusted via
        the .grid.gr (grid radius) and .grid.gd (grid density) attributes.

        Results are returned in a Pandas dataframe with column x-coord, y-coord
        and drawdown value. A drawdown graph is displayed as default and can
        be suppressed by setting plot=False.

        Args:
            t (float) : Time of drawdown (default 1.0).
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
        # Checks
        if t <= 0:
            print('Error! Time must be greater than 0.')
            return
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
            dd = self.disp(r, self.aq.S, self.aq.T, t, self.well.q)
            radius.append(r)
            drawdown.append(dd)
        # Plot results
        mid_row = int(self.grid.grdim/2)
        plot_title = 'Drawdown at radius < ' + str(self.grid.gr) + ' and t = ' + str(t) +\
        '\nT = ' + str(self.aq.T) + ', S = ' + str(self.aq.S) + ', q = ' + str(self.well.q) +\
        ', ri99 = ' + str(round(self.rinf(self.aq.T, self.aq.S, t, qf=0.99),0))
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
