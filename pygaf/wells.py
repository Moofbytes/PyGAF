class Well:
    """Parent well class.

    The Well parent class defines attributes and properties common to all
    wells. They include the x and y coordinates of the well, well radius, well
    penetration depth and a name label for use in figures.

    Attributes:
        x (float) : Well x coordinate (units L, default 0.0).
        y (float) : Well y coordinate (units L, default 0.0).
        r (float) : Well radius (units L, default 0.05).
        pf (float) : Well penetration depth (fraction of aquifer depth,
            default 1.0).
        name (str) : Well name (default '').

    """
    def __init__(self, x, y, r, pf, name):
        self.x = x
        self.y = y
        self.r = r
        self.pf = pf
        self.name = name
        return


class SteadyWell(Well):
    """Steady state well subclass.

    A subclass of the Well class defining a fully penetrating well with steady
    state rate.

    The default SteadyWell object has coordinates x=0 and y=0, well radius
    r=0.05, penetration fraction pf=1 and well rate q=0. The well rate can be
    negative (state: extract), positive (state: inject) of zero (state: off).

    The .info method displays the well information.

    Attributes:
        q (float) : Well rate (units L3/T, default 0.0).

    """
    is_steady = True
    is_transient = False
    def __init__(self, x=0.0, y=0.0, r=0.05, q=0.0, pf=1, name='unnamed'):
        super().__init__(x, y, r, pf, name)
        self.q = q
        self.type = 'Steady state'
        self.name = self.name
        return

    @property
    def r(self):
        """float : Well radius.

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._r

    @r.setter
    def r(self, v):
        if not (v > 0):
            raise Exception('Well radius must be greater than 0.')
        self._r = v

    @property
    def pf(self):
        """float: Well penetration depth.

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._pf

    @pf.setter
    def pf(self, v):
        if not (v > 0 and v <= 1):
            raise Exception(
            'Well penetration must be greater than 0 and less than or equal 1.'
            )
        self._pf = v

    @property
    def state(self):
        """str: Well state."""
        if self.q < 0.0:
            return 'extract'
        elif self.q > 0.0:
            return 'inject'
        else:
            return 'off'

    def info(self):
        """Print the well information.

        Returns:
            Screen printout of well information.

        """
        print('WELL INFORMATION')
        print('----------------')
        print('Type:', self.type)
        print('Name:', self.name)
        print('Coordinates:', round(self.x, 1), ',', round(self.y, 1))
        print('Radius:', self.r, '[L]')
        print('Penetration:', self.pf)
        print('Well rate:', self.q, '[L3/T]')
        print('State:', self.state)
        print()
        return


class TransientWell(Well):
    """Transient well subclass.

    A subclass of the Well class defining a fully penetrating well with
    transient rates defined in stress periods.

    The default TransientWell object has well coordinates x= 0 and y= 0, well
    radius r= 0.05, penetration fraction pf= 1 and default StressSeries object.
    Well rates can be negative (state: extract), positive (state: inject) or
    zero (state: off). Exceptions will occur if invalid values are provided for
    r or pf.

    The .info method displays the well information. The .ss.draw method displays
    the stress seies as a plot.

    Attributes:
        ss (pandas dataframe) : pyGAF stress series (default
            pygaf.stresses.StressSeries).

    """
    is_steady = False
    is_transient = True
    import pandas
    from .stresses import StressSeries
    def __init__(self, x=0.0, y=0.0, r=0.05, ss=StressSeries(ylabel='Well rate'),
    pf=1, name='unnamed'):
        super().__init__(x, y, r, pf, name)
        self.ss = ss
        self.type = 'Transient state'
        self.name = self.name
        return

    @property
    def r(self):
        """float : Well radius.

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._r

    @r.setter
    def r(self, v):
        if not (v > 0):
            raise Exception('Well radius must be greater than 0.')
        self._r = v

    @property
    def pf(self):
        """float: Well penetration depth.

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._pf

    @pf.setter
    def pf(self, v):
        if not (v > 0 and v <= 1):
            raise Exception(
            'Well penetration must be greater than 0 and less than or equal 1.'
            )
        self._pf = v

    @property
    def state(self):
        """str: Well state."""
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
        """Print the well information.

        Returns:
            Screen printout of well information.

        """
        print('WELL INFORMATION')
        print('----------------')
        print('Type:', self.type)
        print('Name:', self.name)
        print('Coordinates:', round(self.x, 1), ',', round(self.y, 1))
        print('Radius:', self.r, '[L]')
        print('Penetration:', self.pf)
        print('Stress periods:', len(self.ss.periods))
        unique_states = list(set(self.state))
        print('Unique well states:', unique_states)
        print()
        return
