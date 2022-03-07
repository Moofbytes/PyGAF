class TheisWell:
    """Theis (1935) well solution."""
    is_infinite = True
    is_finite = False
    is_homogeneous = True
    is_heterogeneous = False
    is_radial = True
    is_1d = False
    is_2d = False
    is_confined = True
    is_unconfined = False

    def __init__(self, aq, w):
        # Checks
        if not aq.is_radial:
            print('Error! The solution assumes a radial aquifer.')
            return
        if not aq.is_infinite:
            print('Warning! The solution assumes an infinite aquifer.')
            return
        if not aq.is_homogeneous:
            print('Warning! The solution assumes a homogeneous aquifer.')
            return
        if not aq.is_confined:
            print('Warning! The solution assumes a confined aquifer.')
            return
        if not w.is_steady:
            print('Error! The solution assumes a steady state well.')
            return
        self.aq = aq
        self.well = w
        self.qf = 0.99
        self.title = 'Theis (1935) well flow solution'
        return

    @property
    def qfp(self):
        """Fraction of pumped volume."""
        return self.qf

    def info(self):
        """Print the solution information."""
        print('METHOD REFERENCE')
        print('----------------')
        print(
        'Theis (1935) - The relation between the lowering of the piezometric' +
        '\nsurface and the rate and duration of discharge of a well using' +
        '\nground-water storage.'
        )

    def ri(self, t=[1], plot=True, csv='', xlsx=''):
        """
        Compute radius of influence from which qf fraction of the pumped volume
        has been drawn (0 < qf < 1.0).

        Arguments:
        ---------
        t : float
            List of times to evaluate radius of influence (default [1])
        plot : bool
            Display a graph of radius of influence (default True)
        csv : str
            Filepath of csv file for results export (default '' - no export)
        xlsx : str
            Filepath of xlsx file for results export (default '' - no export)

        Returns:
        -------
        Pandas dataframe.
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
        # Plot result
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
        """
        Compute drawdown at radii and times.

        Arguments:
        ---------
        t : float
            List of times to evaluate drawdown (default [1])
        r : float
            List of radii to evaluate drawdown (default [1])
        csv : str
            Filepath of csv file for results export (default '' - no export)
        xlsx : str
            Filepath of xlsx file for results export (default '' - no export)

        Returns:
        -------
        Pandas dataframe
        """
        from numpy import pi
        from scipy.special import expn
        import pandas
        # Checks
        if min(t) <= 0 or min(r) <= 0:
            print('Error! All times and radii must be greater than 0.')
            return
        # Drawdown
        d = {'Time':t}
        df = pandas.DataFrame(data=d)
        df.set_index('Time', inplace=True)
        for rad in r:
            drawdown = []
            for tim in t:
                u = (rad**2) * self.aq.S / (4.0 * self.aq.T * tim)
                W = expn(1, u) # Well Function
                drawdown.append(self.well.q * W / (4.0 * pi * self.aq.T))
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

    def dd_grid(self, grid, t=1, plot=True, world=False, csv='', xlsx=''):
        """
        Compute a rectangular grid of drawdown values.

        Arguments:
        ---------
        grid : object
            PyGAF WellGrid object
        t : float
            Time to evaluate drawdown (default [1])
        plot : bool
            Display a drawdown plot (default True)
        world : bool
            Display the drawdown plot in 'local' or 'world' coordinates
            (Default 'local')
        csv : str
            Filepath of csv file for results export (default '' - no export)
        xlsx : str
            Filepath of xlsx file for results export (default '' - no export)

        Returns:
        -------
        Pandas dataframe
        """
        from numpy import pi
        from scipy.special import expn
        import matplotlib.pyplot as plt
        from matplotlib import ticker
        self.grid = grid
        if not world:
            x = self.grid.locx[0]
            y = self.grid.locy[0]
            wx, wy = 0, 0
        else:
            x = self.grid.worldx[0]
            y = self.grid.worldy[0]
            wx, wy = self.grid.well.x, self.grid.well.y
        drawdown = []
        for i in range(self.grid.grdim): # loop rows
            rr = self.grid.rad_pts[i]
            for i, r in enumerate(rr):
                if r <= self.grid.well.r:
                    rr[i] = self.grid.well.r
            ur = [(r**2) * self.aq.S / (4.0 * self.aq.T * t) for r in rr]
            Wr = [expn(1, u) for u in ur]
            drawdown.append(
            [self.grid.well.q * W / (4.0 * pi * self.aq.T) for W in Wr]
            )
        cm = plt.cm.get_cmap('Blues')
        fig, (ax1, ax2) = plt.subplots(
        2, 1, gridspec_kw={'height_ratios': [4, 1]}, figsize=(6, 7.6)
        )
        fig.suptitle(
        'Displacement at r < ' + str(self.grid.gr) + ' and t = ' + str(t)
        )
        ax1.contourf(x, y, drawdown, cmap=cm.reversed())
        cs = ax1.contour(x, y, drawdown, linewidths=[0.5], colors=['black'])
        ax1.clabel(cs, inline=1, fontsize=10)
        ax1.plot(wx, wy, 'o', c='red')
        ax1.set_title('Displacement Contours')
        ax1.grid(True)
        ax1.axis('equal')
        ax2.plot(x, drawdown[int(self.grid.grdim/2)], lw=2)
        ax2.set_title('Radial Displacement')
        ax2.grid(True)
        plt.show()
        return
