class Well:
    """Parent well class."""
    def __init__(self, x, y, r, pd, name):
        self.x = x
        self.y = y
        self.r = r
        self.pd = pd
        self.name = name
        return


class SteadyWell(Well):
    """
    Steady state well.

    Arguments:
    ---------
    x : float
        Well x coordinate (default 0.0)
    y : float
        Well y coordinate (default 0.0)
    r : float
        Well radius [units: L] (default 0.05)
    q : float
        Well rate [units: L3/T] (default 0)
    pd : float
        Well penetration depth as a fraction of aquifer depth (default 1)
    name : str
        Well name (default '')
    """
    is_steady = True
    is_transient = False
    def __init__(self, x=0.0, y=0.0, r=0.05, q=0.0, pd=1, name=''):
        super().__init__(x, y, r, pd, name)
        self.q = q
        self.title = self.name
        return

    @property
    def r(self):
        return self._r
    @r.setter
    def r(self, v):
        if not (v > 0):
            raise Exception('Well radius must be greater than 0.')
        self._r = v

    @property
    def pd(self):
        return self._pd
    @pd.setter
    def pd(self, v):
        if not (v > 0 and v <= 1):
            raise Exception(
            'Well penetration must be greater than 0 and less than or equal 1.'
            )
        self._pd = v

    @property
    def state(self):
        """Well state."""
        if self.q < 0.0:
            return 'extract'
        elif self.q > 0.0:
            return 'inject'
        else:
            return 'off'

    def info(self):
        """Print the well information."""
        print('WELL INFORMATION')
        print('Name:', self.name)
        print('Type: steady state')
        print('Coordinates:', round(self.x, 1), ',', round(self.y, 1))
        print('Radius:', self.r, '[L]')
        print('Penetration:', self.pd)
        print('Well rate:', self.q, '[L3/T]')
        print('State:', self.state)
        return


class TransientWell(Well):
    """Transient well.

    Arguments:
    ---------
    x : float
        Well x coordinate (default 0.0)
    y : float
        Well y coordinate (default 0.0)
    r : float
        Well radius [units: L] (default 0.05)
    ss : pandas dataframe
        pyGAF stress series
    pd : float
        Well penetration depth as a fraction of aquifer depth (default 1)
    name : str
        Well name (default '')

    Properties:
    ----------
    state : str
        Well flow state (extract, inject or off)
    """
    import pandas
    is_steady = False
    is_transient = True
    def __init__(self, x=0.0, y=0.0, r=0.05, ss=None, pd=1, name=''):
        super().__init__(x, y, r, pd, name)
        self.ss = ss
        self.title = self.name
        return

    @property
    def r(self):
        return self._r
    @r.setter
    def r(self, v):
        if not (v > 0):
            raise Exception('Well radius must be greater than 0.')
        self._r = v

    @property
    def pd(self):
        return self._pd
    @pd.setter
    def pd(self, v):
        if not (v > 0 and v <= 1):
            raise Exception(
            'Well penetration must be greater than 0 and less than or equal 1.'
            )
        self._pd = v

    @property
    def state(self):
        """Well state."""
        s = []
        for rate in self.ss.series['values']:
            if rate < 0.0:
                s.append('extract')
            elif rate > 0.0:
                s.append('inject')
            else:
                s.append('off')
        return s

    def info(self):
        """Print the well information."""
        print('WELL INFORMATION')
        print('Name:', self.name)
        print('Type: transient')
        print('Coordinates:', round(self.x, 1), ',', round(self.y, 1))
        print('Radius:', self.r, '[L]')
        print('Penetration:', self.pd)
        unique_states = list(set(self.state))
        print('Unique well states:', unique_states)
        return

    def plot(self, dw=8):
        """
        Plot the well stresses.

        Arguments:
        ---------
        dw : float
            Width of plot figure (default 8)
        """
        import matplotlib.pyplot as plt
        periods = [p for p in list(self.ss.series['periods'])]
        rates = [v for v in list(self.ss.series['values'])]
        plot_times, plot_rates = [], []
        for i in range(len(periods)):
            plot_times.append(sum(periods[0:i]))
            plot_times.append(sum(periods[0:i+1]))
            plot_rates.append(rates[i])
            plot_rates.append(rates[i])
        fig = plt.figure(figsize=(dw, dw/3))
        plt.plot(plot_times, plot_rates, linewidth=3)
        plt.title(self.name)
        plt.xlabel('Time')
        plt.ylabel('Well Rate')
        plt.grid(True)
        plt.show()
        return
