class MineSteadyRadUnconf:
    """Steady, radial, unconfined flow to a large diameter well.

    Predict steady mine inflow for a specified mine pit water level. The
    MineSteadyRadUnconf class uses the default Aq2dUnconf aquifer object with
    initial saturated thickness 100.

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
        from numpy import sqrt
        from numpy import log
        r1 = self.rp * 10 # initial estimate
        err = 0.01 # convergence error for iterative solution
        res = err + 1 # initialise residual
        count = 0
        while abs(res) > err:
            count = count + 1
            r2 = sqrt(
            self.aq.K * (self.aq.B**2 - self.hp**2)/(self.R * log(r1/self.rp))
            )
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
        print('- Mine pit is approximated by a cylinder.')
        print('- Dewatering via an imaginary pumping well with radius rp.')
        print('- Steady, horizontal, axially symmetric and unconfined flow.')
        print('- Uniform recharge.')
        print('- Horizontal pre-mining water table.')
        print('\nNotes:')
        print('- Steady state approximation is reasonable for moderate to\n'
        '  to large hydraulic conductivity and mine pits excavated over years.')
        print('- The radius of influence is implicit and defined by the radius\n'
        '  at which drawdown is zero.')
        print()

    def hr(self, r):
        """Head at radius r."""
        from numpy import sqrt
        from numpy import log
        h = sqrt(self.aq.B**2 - (self.R*self.ri**2*log(self.ri/r))/self.aq.K)
        return h

    def dr(self, r):
        """Drawdown at radius r."""
        d = self.aq.B - self.hr(r)
        return d

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
        h = [self.hr(i) for i in r]
        d = [self.dr(i) for i in r]
        df = pandas.DataFrame()
        df['radius'] = r
        df['drawdown'] = d
        df['head'] = h
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
        from pygaf.utils import display_image
        display_image('MineSteadyRadUnconf.png', dw=dw)
        return

class MineSteadyRadUnconf2:
    """Steady, radial, unconfined flow to a large diameter well with pit
    floor inflow.

    Predict steady mine inflow for a specified mine pit water level. The
    MineSteadyRadUnconf2 class uses the default Aq2dUnconf aquifer object with
    initial saturated thickness 100 for the upper unconfined aquifer.

    Attributes:
        aq (obj) : Upper aquifer object.
        R (float) : Groundwater recharge rate (units L/T, default 1.0e-4).
        aq2kx (float) : Horizontal hydraulic conductivity of lower aquifer
            (units L/T, default 1)
        aq2kz (float) : Vertical hydraulic conductivity of lower aquifer
            (units L/T, default 1)

    """
    from pygaf.aquifers import Aq2dUnconf
    def __init__(self):
        self.aq = self.Aq2dUnconf(B=100)
        self.rp = 100
        self.hp = 90
        self.R = 1.0e-4
        self.aq2kx = 1.0
        self.aq2kz = 1.0
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
    def D(self):
        """float : Depth of mine pit lake (units L, default 0).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._D

    @D.setter
    def D(self, v):
        if not (v <= self.hp and v >= 0):
            raise Exception('Pit lake depth must be 0 <= D <= B.')
        self._D = v

    @property
    def ri(self):
        """Radius of influence."""
        from numpy import sqrt
        from numpy import log
        r1 = self.rp * 10 # initial estimate
        err = 0.01 # convergence error for iterative solution
        res = err + 1 # initialise residual
        count = 0
        while abs(res) > err:
            count = count + 1
            r2 = sqrt(
            ((self.aq.B**2-self.hp**2)*self.aq.K/self.R + (r1**2-self.rp**2)/2) /
            log(r1/self.rp)
            )
            res = r2 - r1
            r1 = r2
            if count > 1000:
                raise Exception('More than 1000 iterations trying to solve ri.')
        return r2

    @property
    def qp1(self):
        """Mine pit inflow rate from upper aquifer."""
        from numpy import pi
        q = pi * self.R * (self.ri**2 - self.rp**2)
        return q

    @property
    def qp2(self):
        """Mine pit inflow rate from lower aquifer."""
        from numpy import sqrt
        q = 4.0 * self.rp * (self.aq.B-self.D) * sqrt(self.aq2kx * self.aq2kz)
        return q

    @property
    def qp(self):
        """Total mine pit inflow rate."""
        q = self.qp1 + self.qp2
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
        print('Marinelle F. and Niccoli W. (2000) - Simple Analytical\n'
        'Equations for Estimating Ground Water Inflow to a Mine Pit.')
        print('\nUpper Aquifer Conceptual Model:')
        print('- Infinite, unconfined and homogeneous aquifer.')
        print('- Mine pit is approximated by a cylinder.')
        print('- Mine pit fully penetrates aquifer.')
        print('- Steady, horizontal, axially symmetric and unconfined flow.')
        print('- Uniform recharge.')
        print('- Horizontal pre-mining water table.')
        print('\nLower Aquifer Conceptual Model:')
        print('- Semi-infinite, confined and anisotropic aquifer.')
        print('- Hydraulic head is initially hydrostatic and equal to B.')
        print('- The pit floor (disk sink) has uniform head equal to D.')
        print('- Flow to the pit floor is 3D and radially symmetric.')
        print('\nNotes:')
        print('- Steady state approximation is reasonable for moderate to\n'
        '  to large hydraulic conductivity and mine pits excavated over years.')
        print('- The inflows to the upper and lower aquifers are independent\n'
        '  of each other.')
        print('- If the pit is completely dewatered (D = 0) the disk sink\n'
        '  head is equal to the elevation of the pit floor.')
        print('- The radius of influence is implicit and defined by the radius\n'
        '  at which drawdown is zero.')
        print()

    def hr(self, r):
        """Head at radius r."""
        from numpy import sqrt
        from numpy import log
        h = sqrt(
            self.hp**2 + ((self.R/self.aq.K) *
            (self.ri**2 * log(r/self.rp) - (r**2 - self.rp**2)/2))
        )
        return h

    def dr(self, r):
        """Drawdown at radius r."""
        d = self.aq.B - self.hr(r)
        return d

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
        h = [self.hr(i) for i in r]
        d = [self.dr(i) for i in r]
        df = pandas.DataFrame()
        df['radius'] = r
        df['drawdown'] = d
        df['head'] = h
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
        from pygaf.utils import display_image
        display_image('MineSteadyRadUnconf2.png', dw=dw)
        return

class MineSteadyRadLeaky:
    """Steady, radial, leaky flow to a large diameter well.

    Predict steady drawdown for a specified mine pit inflow. The
    MineSteadyRadleaky class uses the default Aq2dConf aquifer object with
    initial thickness 100 for the lower confined aquifer.

    Attributes:
        aq (obj) : Lower aquifer object.

    """
    from pygaf.aquifers import Aq2dConf
    def __init__(self):
        self.aq = self.Aq2dConf(B=100)
        self.rp = 100
        self.qp = 1000
        self.Kleak = 1.0e-5
        self.Bleak = 10
        self.h0 = 120
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
    def qp(self):
        """float : Mine pit inflow rate (units L/T, default 1000).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._qp

    @qp.setter
    def qp(self, v):
        if not (v > 0):
            raise Exception('Mine pit inflow (qp) must be positive.')
        self._qp = v

    @property
    def h0(self):
        """float : Initial groundwater head (units L, default 90).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._h0

    @h0.setter
    def h0(self, v):
        if not (v > (self.aq.B + self.Bleak)):
            raise Exception('Initial water level must be above the aquitard.')
        self._h0 = v

    @property
    def Kleak(self):
        """float : Hydraulic conductivity of leaky aquitard (units L/T,
            default 1e-5).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._Kleak

    @Kleak.setter
    def Kleak(self, v):
        if not (v > 0):
            raise Exception('Aquitard conductivity (Kleak) must be positive.')
        self._Kleak = v

    @property
    def Bleak(self):
        """float : Thickness of leaky aquitard (units L, default 10)

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._Bleak

    @Bleak.setter
    def Bleak(self, v):
        if not (v > 0):
            raise Exception('Aquitard thickness (Bleak) must be positive.')
        self._Bleak = v

    @property
    def lfac(self):
        """float : Aquitard leakage factor (units L)."""
        from numpy import sqrt
        lf = sqrt(self.aq.T * self.Bleak / self.Kleak)
        return lf

    @property
    def ri(self):
        """Radius of influence.

            Defined as radius at which drawdown is less than 0.1% of initial
            groundwater head.
        """
        from numpy import sqrt
        from numpy import pi
        from scipy.special import k0
        e = 0.001
        r1 = self.rp # initial estimate
        r2 = self.rp * 1e6 # initial estimate
        targ = 2 * pi * self.aq.T * e * self.h0 / self.qp
        err = 0.01 # convergence error for iterative solution
        res = r2 - r1 # initialise residual
        count = 0
        while abs(res) > err:
            count = count + 1
            r3 = r1 + (r2 - r1)/2
            bess = k0(r3/self.lfac)
            if bess > targ:
                r1 = r3
            else:
                r2 = r3
            res = r2 - r1
            if count > 1000:
                raise Exception(('More than 1000 iterations trying to solve ri.'))
        return r3

    def dr(self, r):
        """Drawdown at radius r."""
        from numpy import pi
        from scipy.special import k0
        d = k0(r/self.lfac) * self.qp/(2*pi*self.aq.T)
        return d

    def hr(self, r):
        """Head at radius r."""
        h = self.h0 - self.dr(r)
        return h

    def leakr(self, r):
        """Leakage rate at radius r."""
        lr = self.dr(r) * self.Kleak/self.Bleak
        return lr

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
        h = [self.hr(i) for i in r]
        d = [self.dr(i) for i in r]
        leak = [self.leakr(i) for i in r]
        df = pandas.DataFrame()
        df['radius'] = r
        df['drawdown'] = d
        df['head'] = h
        df['leakage'] = leak
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

    def info(self):
        """Print the solution information.

        Returns:
        Screen printout of solution information.

        """
        print('METHOD REFERENCE')
        print('----------------')
        print('Bouwer H. (2000) - Groundwater Hydrology.')
        print('\nLower Aquifer Conceptual Model:')
        print('- Infinite, leaky and homogeneous lower aquifer.')
        print('- Mine pit is approximated by a cylinder.')
        print('- Mine pit fully penetrates aquifer.')
        print('- Steady, horizontal, axially symmetric and confined flow.')
        print('- Horizontal pre-mining groundwater head.')
        print('\nNotes:')
        print('- A steady state occurs when inflow to the mine pit is equal\n'
        '  to leakage from the upper aquifer to the lower aquifer.')
        print()

    def draw(self, dw=8):
        """Display a drawing of the aquifer.

        Args:
            dw (float) : Width of figure (default 8.0).

        """
        from pygaf.utils import display_image
        display_image('MineSteadyRadLeaky.png', dw=dw)
        return
