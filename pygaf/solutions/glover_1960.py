class GloverRectBasinSteady:
    """Glover (1960) solution class.

    The default GloverRectBasinSteady object uses the default Aq2dConf and
    BasinGrid classes. It's methods include impress at a point .impress and
    grid-contoured impress at specified time .impress_grid.

    Attributes:
        aq (obj) : Confined aquifer object.
        basin (obj) : Basin object.

    """
    from pygaf.aquifers import Aq2dConf
    from pygaf.grids import BasinGrid
    def __init__(self, aq=Aq2dConf(), basin=BasinGrid()):
        self.aq = aq
        self.basin = basin
        return

    def info(self):
        """Print the solution information.

        Returns:
            Screen printout of solution information.

        """
        print('METHOD REFERENCE')
        print('----------------')
        print(
        'Glover R. E. (1960) - Mathematical derivations as pertain to' +
        '\ngroundwater recharge.'
        )
        print('\nConceptual Model:')
        print('- Infinite, unconfined and homogeneous aquifer.')
        print('- Rectangular recharge basin with steady state infiltration.')
        print('- Spatially uniform infiltration rate.')
        print('- Instant transfer of infiltration to water table.')
        print()

    def u1(self, x, xL, T, S, t, tau):
        """Glover u1 solution term; tau is an integration variable."""
        from numpy import sqrt
        value = (x - xL/2) / sqrt(4*T*(t-tau)/S)
        return value

    def u2(self, x, xL, T, S, t, tau):
        """Glover u2 solution term; tau is an integration variable."""
        from numpy import sqrt
        value = (x + xL/2) / sqrt(4*T*(t-tau)/S)
        return value

    def u3(self, y, yL, T, S, t, tau):
        """Glover u3 solution term; tau is an integration variable."""
        from numpy import sqrt
        value = (y - yL/2) / sqrt(4*T*(t-tau)/S)
        return value

    def u4(self, y, yL, T, S, t, tau):
        """Glover u4 solution term; tau is an integration variable."""
        from numpy import sqrt
        value = (y + yL/2) / sqrt(4*T*(t-tau)/S)
        return value

    def h(self, x, y, xL, yL, T, S, t, q):
        """Glover impress solution."""
        from scipy.special import erfc
        import scipy.integrate as integrate
        P = integrate.quad(lambda z: (erfc(self.u2(x, xL, T, S, t, z))-\
        erfc(self.u1(x, xL, T, S, t, z))) * (erfc(self.u4(y, yL, T, S, t, z))-\
        erfc(self.u3(y, yL, T, S, t, z))), 0, t)
        value = (q/4/S) * P[0]
        return value

    def impress(self, t=[1], locs=[(0, 0)], q=0.0, plot=True, csv='', xlsx=''):
        """Calculate impress at specified locations and times.

        Args:
            t (float) : List of times to evaluate impress (default [1.0]).
            locs (float tupple) : List of (dx, dy) location tupples to
                evaluate impress; dx is distance from basin center in x
                direction; dy is distance from basin center in y direction
                (default [(0.0, 0.0)]).
            q (float) : Basin infiltration rate (default 0.0).
            plot (bool) : Display a plot of the results (default True).
            csv (str) : Filepath for export of results to csv file; results
                are exported if the string is not empty (default '').
            xlsx (str) : Filepath for export of result to xlsx file; results
                are exported if the string is not empty (default '').

        Returns:
            Pandas dataframe containing results, hydraulic loading.

        """
        import pandas
        # Checks
        if min(t) <= 0:
            print('Error! All times must be greater than 0.')
            return
        # Hydraulic loading
        Q = self.basin.area * q
        # Impress
        d = {'Time':t}
        df = pandas.DataFrame(data=d)
        df.set_index('Time', inplace=True)
        for loc in locs:
            impress = []
            for tim in t:
                impress.append(
                    self.h(
                        loc[0], loc[1], self.basin.lx, self.basin.ly,
                        self.aq.T, self.aq.S, tim, q
                        )
                )
            df[str(loc)] = impress
        # Plot results
        if plot:
            import matplotlib.pyplot as plt
            df.plot(
                grid=True, marker='.', lw=3, alpha=0.5, ylabel='Displacement'
                )
            plt.title('Impress\n' +
                'T = ' + str(self.aq.T) +
                ', S = ' + str(self.aq.S) +
                ', q = ' + str(q)
                )
            plt.legend(
                locs, ncol=5, mode='expand', loc='upper left',
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
            df.to_excel(xlsx, sheet_name='impress')
            print('Results exported to:', xlsx)
        return df, Q

    def impress_grid(self, t=1, q=0.0, gr=100, gd=20, plot=True, local=False,
        csv='', xlsx=''):
        """Calculate impress on a regular grid.

        Args:
            t (float) : Time to evaluate impress (default [1.0]).
            q (float) : Basin infiltration rate (default 0.0).
            gr (float) : Radius defining the extent of the solution grid
                (default 100.0).
            gd (int) : Grid density defining the number of gird rows and
                columns; minimum and maximum constraints are enforced
                (default 21).
            plot (bool) : Display a plot of the results (default True).
            local (bool) : Display the drawdown plot in 'local' coordinates
                with the well at 0, 0 (Default False).
            csv (str) : Filepath for export of results to csv file; results
                are exported if the string is not empty (default '').
            xlsx (str) : Filepath for export of result to xlsx file; results
                are exported if the string is not empty (default '').

        Returns:
            Pandas dataframe containing results, hydraulic loading.

        """
        from pygaf.grids import BasinGrid
        import matplotlib.pyplot as plt
        import numpy
        import pandas
        self.gr = gr
        self.gd = gd
        self.grid = BasinGrid(basin=self.basin, gr=self.gr, gd=self.gd)
        # Set coordinates
        if local:
            x, y = list(self.grid.pts.locx), list(self.grid.pts.locy)
            bx, by = 0, 0
            plot_title = 'Impress at r < ' + str(self.grid.gr) +\
            ' and t = ' + str(t) + '\n(local coordinates)'
        else:
            x, y = list(self.grid.pts.worldx), list(self.grid.pts.worldy)
            bx, by = self.grid.basin.cx, self.grid.basin.cy
            plot_title = 'Impress at r < ' + str(self.grid.gr) +\
            ' and t = ' + str(t) + '\n(world coordinates)'
        # Hydraulic loading
        Q = self.basin.area * q
        # Impress
        impress = []
        for i in range(self.grid.npts):
            impress.append(
                self.h(
                    self.grid.pts.dx[i],
                    self.grid.pts.dy[i],
                    self.basin.lx,
                    self.basin.ly,
                    self.aq.T,
                    self.aq.S, t, q
                )
            )
        # Plot results
        mid_row = int(self.grid.grdim/2)
        if plot:
            cm = plt.cm.get_cmap('Blues')
            fig, (ax1, ax2, ax3) = plt.subplots(
                3, 1, gridspec_kw={'height_ratios': [4, 1, 1]},
                figsize=(6, 10)
            )
            fig.suptitle(plot_title, fontsize=14)
            ax1.tricontourf(x, y, impress, cmap=cm)
            cs = ax1.tricontour(
                x, y, impress, linewidths=0.25, colors=['black']
            )
            ax1.clabel(cs, inline=1, fontsize=10)
            ax1.plot(bx, by, '.', c='red')
            ax1.set_title('Impress Contours')
            ax1.grid(True)
            ax1.axis('equal')
            ax2.plot(
                x[self.grid.grdim*(mid_row-1):self.grid.grdim*mid_row],
                impress[self.grid.grdim*(mid_row-1):self.grid.grdim*mid_row],
                '.-', lw=3, alpha=0.5
            )
            ax2.set_title('Distance Impress')
            ax2.set_xlabel('dx')
            ax2.grid(True)
            ax3.plot(
                [y[i] for i in range(mid_row, self.grid.npts, self.grid.grdim)],
                [impress[i] for i in range(mid_row, self.grid.npts, self.grid.grdim)],
                '.-', lw=3, alpha=0.5
            )
            ax3.set_xlabel('dy')
            ax3.grid(True)
            plt.tight_layout()
            plt.show()
            plt.close()
        # Export result
        df = pandas.DataFrame()
        df['x'] = x
        df['y'] = y
        df['impress'] = impress
        if csv != '':
            if csv.split('.') != 'csv':
                csv = csv + '.csv'
            df.to_csv(csv, index=False)
            print('Results exported to:', csv)
        if xlsx != '':
            if xlsx.split('.') != 'xlsx':
                xlsx = xlsx + '.xlsx'
            df.to_excel(xlsx, sheet_name='impress', index=False)
            print('Results exported to:', xlsx)
        return df, Q
