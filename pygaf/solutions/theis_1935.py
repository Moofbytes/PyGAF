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
        self.T = aq.T
        self.S = aq.S
        self.q = w.q
        print(self.__dict__)
        self.title = 'Theis (1935) well flow solution'
        return

    def ri(self, qf=0.99, t=[1], plot=True):
        """
        Compute radius of influence from which qf fraction of the pumped volume
        has been drawn (0 < qf < 1.0).

        Keyword Arguments:
        -----------------
        qf : float
            Fraction of pumped volume (default 0.99)
        t : float
            List of times to evaluate radius of influence (default [1])
        plot : bool
            Display a graph of radius of influence (default True)

        Returns:
        -------
        Pandas dataframe.
        """
        from numpy import sqrt, log
        import pandas
        # Checks
        if qf < 0 or qf > 1:
            print('Error! The value of qf must be between 0 and 1.')
            return
        if min(t) <= 0:
            print('Error! All times must be greater than 0.')
            return
        if min(r) <= 0:
            print('Error! All radii must be greater than 0.')
            return
        # Radius of influence
        ri = []
        for tim in t:
            ri.append(sqrt(-4.0 * self.T * tim * log(1-qf) / self.S))
        d = {'Time':t, 'ri':ri}
        df = pandas.DataFrame(data=d)
        df.set_index('Time', inplace=True)
        if plot:
            import matplotlib.pyplot as plt
            df.plot(grid=True, marker='.', ylabel='Radius')
            plt.title('T = ' + str(self.T) +
                      ', S = ' + str(self.S) +
                      ' and q = ' + str(self.q)
                      )
            plt.show()
        return df

    def dd(self, t=[1], r=[1], plot=True):
        """
        Compute drawdown at radii and times.

        Keyword Arguments:
        -----------------
        t : float
            List of times to evaluate drawdown (default [1])
        r : float
            List of radii to evaluate drawdown (default [1])

        Returns:
        -------
        Pandas dataframe
        """
        from numpy import pi
        from scipy.special import expn
        import pandas
        # Checks
        if min(t) <= 0:
            print('Error! All times must be greater than 0.')
            return
        if min(r) <= 0:
            print('Error! All radii must be greater than 0.')
            return
        # Drawdown
        d = {'Time':t}
        df = pandas.DataFrame(data=d)
        df.set_index('Time', inplace=True)
        for rad in r:
            dd = []
            for tim in t:
                u = (rad**2) * self.S / (4.0 * self.T * tim)
                W = expn(1, u) # Well Function
                dd.append(self.q * W / (4.0 * pi * self.T))
            df['r' + str(rad)] = dd
        if plot:
            import matplotlib.pyplot as plt
            df.plot(grid=True, marker='.', ylabel='Displacement')
            plt.title('T = ' + str(self.T) +
                      ', S = ' + str(self.S) +
                      ' and q = ' + str(self.q)
                      )
            plt.show()
        return df
