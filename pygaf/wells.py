class Well:
    """Parent well class."""
    def __init__(self, r, pd, name):
        self.r = r
        self.pd = pd
        self.name = name

        if self.r < 0:
            print('Error! well radius should be positive.')
            return
        elif self.r > 1:
            print('Notice! well radius is greater than 1 [L]')
        if self.pd <= 0 or self.pd > 1:
            print('Error! well penetration depth should be between 0 and 1.')
            return
        elif self.pd < 0.5:
            print('Notice! well penetration is less than half aquifer thickness.')

        return


class SteadyWell(Well):
    """
    Steady state well.

    Arguments:
    ---------
    r : float
        Well radius [units: L] (default 0.05)
    q : float
        Well rate [units: L3/T] (default 0)
    pd : float
        Well penetration depth as a fraction of aquifer depth (default 1)
    name : str
        Well name (default '')

    Properties:
    ----------
    state : str
        Well flow state (extract, inject or off)
    """
    is_steady = True
    is_transient = False
    def __init__(self, r=0.05, q=0.0, pd=1, name=''):
        super().__init__(r, pd, name)
        self.q = q
        self.title = self.name
        return

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
        print('Radius:', self.r, '[L]')
        print('Well rate:', self.q, '[L3/T]')
        print('State:', self.state)
        return


class TransientWell(Well):
    """Transient well.

    Arguments:
    ---------
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
    def __init__(self, r=0.05, ss=None, pd=1, name=''):
        super().__init__(r, pd, name)
        self.ss = ss
        self.title = self.name
        return

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
        print('Radius:', self.r, '[L]')
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
