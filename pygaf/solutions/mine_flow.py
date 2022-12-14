class MineSteadyRadUnconf:
    """Steady, radial, unconfined flow to a large diameter well.

    The MineSteadyRadUnconf class uses the default Aq2dUnconf aquifer object
    with initial saturated thickness 100.

    Attributes:
        aq (obj) : Aquifer object.
        R (float) : Groundwater recharge rate (units L/T, default 1.0e-4).

    """
    from pygaf.aquifers import Aq2dUnconf
    def __init__(self):
        self.aq = self.Aq2dUnconf(B=100)
        self.rp = 100
        self.hp = 90
        self.R = 1.0e-4
        return

    @property
    def rp(self):
        """float : Equivalent radius of mine pit (units L, default 100).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._rp

    @rp.setter
    def rp(self, v):
        if not (v > 0):
            raise Exception('Equivalent mine pit radius (rp) must be positive.')
        self._rp = v

    @property
    def hp(self):
        """float : Mine pit water level (units L, default 90).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._hp

    @hp.setter
    def hp(self, v):
        if not (v < self.aq.B and v > 0):
            raise Exception('Water level must be 0 < hp < B.')
        self._hp = v

    @property
    def ri(self):
        """Radius of influence."""
        import numpy as np
        r1 = self.rp * 10 # initial estimate
        err = 0.01 # convergence error for iterative solution
        res = err + 1 # initialise residual
        count = 0
        while abs(res) > err:
            count = count + 1
            r2 = np.sqrt(self.aq.K * (self.aq.B**2 - self.hp**2)/(self.R * np.log(r1/self.rp)))
            res = r2 - r1
            r1 = r2
            if count > 1000:
                raise Exception('More than 1000 iterations trying to solve ri.')
        return r2

    @property
    def qp(self):
        """Mine pit inflow rate."""
        import numpy as np
        q = np.pi * self.R * (self.ri**2 - self.rp**2)
        return q

    @property
    def dp(self):
        """float : Drawdown of mine pit water level from initial (pre-mining)
        water table (units L, default 10)
        """
        return self.aq.B - self.hp

    def info(self):
        """Print the solution information.

        Returns:
        Screen printout of solution information.

        """
        print('METHOD REFERENCE')
        print('----------------')
        print('Bouwer H. (1978) - Groundwater Hydrology.')
        print('\nConceptual Model:')
        print('- Infinite, unconfined and homogeneous aquifer.')
        print('- Dewatering via an imaginary pumping well with radius rp.')
        print('- Steady, horizontal, axially symmetric and unconfined flow.')
        print('- Uniform recharge.')
        print('- Horizontal pre-mining water table.')
        print()

    def dr(self, r):
        """Drawdown at radius r."""
        from numpy import sqrt
        from numpy import log
        value = sqrt(self.aq.B**2 - (self.R*self.ri**2*log(self.ri/r))/self.aq.K)
        return value

    def dd(self, n=25, plot=True, csv='', xlsx=''):
        """Evaluate steady drawdown.

        Evaluate steady state drawdown at specified distances from the mine pit
        wall. Results are returned in a Pandas dataframe. A drawdown graph is
        displayed as default and can be suppressed by setting plot=False.

        Args:
            n (int) : Number of radial values for evaluating drawdown (default 25).
            plot (bool) : Display a plot of results (default True).
            csv (str) : Full filepath for export of results to csv file;
                results are exported if the string is not empty (default '').
            xlsx (str) : Full filepath for export of result to xlsx file;
                results are exported if the string is not empty (default '').

        Returns:
            Results in a pandas dataframe.

        """
        from numpy import linspace
        import pandas
        r = linspace(self.rp, self.ri, n)
        h = [self.dr(i) for i in r]
        d = [self.aq.B - i for i in h]
        df = pandas.DataFrame()
        df['radius'] = r
        df['drawdown'] = d
        # Plot results
        if plot:
            import matplotlib.pyplot as plt
            df.plot(
                x='radius', y='drawdown', grid=True, marker='.', lw=3, alpha=0.5,
                legend=False, ylabel='drawdown'
                )
            plt.axis([0, None, max(d), min(d)])
            plt.title('Radial Drawdown')
            plt.show()
        return df

    def draw(self, dw=8):
        """Display a drawing of the aquifer.

        Args:
            dw (float) : Width of figure (default 8.0).

        """
        import pygaf
        import os
        import matplotlib.pyplot as plt
        import matplotlib. image as mpimg
        file_path = pygaf.__file__
        dir = os.path.join(os.path.dirname(file_path), 'images')
        image_file = os.path.join(dir, 'MineSteadyRadUnconf.png')
        image = mpimg.imread(image_file)
        image_h = len(image)
        image_w = len(image[0])
        plt. figure(figsize = (dw, dw*image_h/image_w))
        image_plot = plt.imshow(image)
        plt.axis('off')
        plt.show()
        plt.close()
        return image
