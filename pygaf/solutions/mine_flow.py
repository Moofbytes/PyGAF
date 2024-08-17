class MineSteadyRadUnconfQ:
    """Steady, radial, unconfined flow to a large diameter well.

    Evaluate steady-state mine inflow for a specified mine pit water level.
    The MineSteadyRadUnconfQ class adopts the default Aq2dUnconf aquifer object
    with initial saturated thickness 100.

    Attributes:
        aq (obj) : Aquifer object.

    """
    from pygaf.aquifers import Aq2dUnconf
    def __init__(self):
        self.aq = self.Aq2dUnconf(B=100, name='2D unconfined aquifer')
        self.rp = 100
        self.hp = 90
        self.R = 1.0e-4
        return

    @property
    def R(self):
        """float : Groundwater recharge rate (units L/T, default 1.0e-4).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._R

    @R.setter
    def R(self, v):
        if not (v > 0):
            raise Exception('Recharge rate (R) must be positive.')
        self._R = v

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
        """float : Radius of influence (units L)."""
        from numpy import sqrt, log
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
        """float : Mine pit inflow rate (units L3/T)."""
        import numpy as np
        q = np.pi * self.R * (self.ri**2 - self.rp**2)
        return q

    @property
    def dp(self):
        """float : Drawdown of mine pit water level from initial water table
        (units L, default 10).
        """
        return self.aq.B - self.hp

    def info(self):
        """Print the solution information."""
        print('METHOD REFERENCE')
        print('----------------')
        print('Bouwer H. (1978) - Groundwater Hydrology.')
        print('\nRadial-symmetric, unconfined, horizontal flow to a large'
        '\ndiameter well. The solution estimates the steady-state inflow rate'
        '\nto the pit and drawdown with radial distance from the pit wall.')
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
        """Head at specified radius (units L).

        Args:
            r (float) : Radius at which to evaluate head (units L).

        """
        from numpy import sqrt, log
        h = sqrt(self.aq.B**2 - (self.R*self.ri**2*log(self.ri/r))/self.aq.K)
        return h

    def dr(self, r):
        """Drawdown at specified radius (units L).

        Args:
            r (float) : Radius at which to evaluate head (units L).

        """
        d = self.aq.B - self.hr(r)
        return d

    def dd(self, n=25, plot=True, csv='', xlsx=''):
        """Evaluate distance-drawdown (units L).

        Evaluate steady-state drawdown at specified distances from the mine pit
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

    def draw(self, dw=8):
        """Display the definition diagram.

        Args:
            dw (float) : Width of figure (default 8.0).

        """
        from pygaf.utils import display_image
        display_image('MineSteadyRadUnconf.png', dw=dw)
        return

class MineSteadyRadUnconfQ2:
    """Steady, radial, unconfined flow to a large diameter well with pit
    floor inflow.

    Evaluate steady-state mine inflow for a specified mine pit water level.
    The MineSteadyRadUnconfQ2 class adopts the default Aq2dUnconf aquifer object
    with initial saturated thickness 100 for the upper unconfined aquifer.

    Attributes:
        aq (obj) : Upper aquifer object.
        aq2kx (float) : Horizontal hydraulic conductivity of lower aquifer
            (units L/T, default 1)
        aq2kz (float) : Vertical hydraulic conductivity of lower aquifer
            (units L/T, default 1)

    """
    from pygaf.aquifers import Aq2dUnconf
    def __init__(self):
        self.aq = self.Aq2dUnconf(B=100, name='2D unconfined aquifer')
        self.rp = 100
        self.hp = 90
        self.R = 1.0e-4
        self.aq2kx = 1.0
        self.aq2kz = 1.0
        return

    @property
    def R(self):
        """float : Groundwater recharge rate (units L/T, default 1.0e-4).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._R

    @R.setter
    def R(self, v):
        if not (v > 0):
            raise Exception('Recharge rate (R) must be positive.')
        self._R = v

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
        """float : Radius of influence (units L)."""
        from numpy import sqrt, log
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
        """float : Mine pit inflow rate from upper aquifer (units L3/T)."""
        from numpy import pi
        q = pi * self.R * (self.ri**2 - self.rp**2)
        return q

    @property
    def qp2(self):
        """float : Mine pit inflow rate from lower aquifer (units L3/T)."""
        from numpy import sqrt
        q = 4.0 * self.rp * (self.aq.B-self.D) * sqrt(self.aq2kx * self.aq2kz)
        return q

    @property
    def qp(self):
        """float : Total mine pit inflow rate (units L3/T)."""
        q = self.qp1 + self.qp2
        return q

    @property
    def dp(self):
        """float : Drawdown of mine pit water level (units L, default 10)."""
        return self.aq.B - self.hp

    def info(self):
        """Print the solution information."""
        print('METHOD REFERENCE')
        print('----------------')
        print('Marinelle F. and Niccoli W. (2000) - Simple Analytical\n'
        'Equations for Estimating Ground Water Inflow to a Mine Pit.')
        print('\nRadial-symmetric, unconfined, horizontal flow to a large'
        '\ndiameter well. The solution estimates the steady-state inflow rate'
        '\nto the pit and drawdown with radial distance from the pit wall.')
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
        """Head at radius r (units L).

        Args:
            r (float) : radius at which to evaluate head (units L).
        """
        from numpy import sqrt, log
        h = sqrt(
            self.hp**2 + ((self.R/self.aq.K) *
            (self.ri**2 * log(r/self.rp) - (r**2 - self.rp**2)/2))
        )
        return h

    def dr(self, r):
        """Drawdown at radius r (units L).

        Args:
            r (float) : radius at which to evaluate drawdown (units L).
        """
        d = self.aq.B - self.hr(r)
        return d

    def dd(self, n=25, plot=True, csv='', xlsx=''):
        """Evaluate distance-drawdown (units L).

        Evaluate steady-state drawdown at specified distances from the mine pit
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

    def draw(self, dw=8):
        """Display the definition diagram.

        Args:
            dw (float) : Width of figure (default 8.0).

        """
        from pygaf.utils import display_image
        display_image('MineSteadyRadUnconf2.png', dw=dw)
        return

class MineSteadyRadLeakyDD:
    """Steady, radial, leaky flow to a large diameter well.

    Evaluate steady-state drawdown for a specified mine pit inflow. The
    MineSteadyRadleakyDD class adopts the default Aq2dLeaky aquifer object
    with aquifer thickness 100 for the confined aquifer.

    Attributes:
        aq (obj) : Lower aquifer object.

    """
    from pygaf.aquifers import Aq2dLeaky
    def __init__(self):
        self.aq = self.Aq2dLeaky(B=100, name='2D leaky aquifer')
        self.rp = 100
        self.qp = 1000
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
        """float : Initial groundwater head (units L, default 120).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._h0

    @h0.setter
    def h0(self, v):
        if not (v > (self.aq.B + self.aq.Bleak)):
            raise Exception('Initial water level must be above the aquitard.')
        self._h0 = v

    @property
    def lfac(self):
        """float : Aquitard leakage factor (units L)."""
        from numpy import sqrt
        lf = sqrt(self.aq.T * self.aq.Bleak / self.aq.Kleak)
        return lf

    @property
    def ri(self):
        """float : Radius of influence (units L).

            Defined as radius at which drawdown is less than 0.1% of initial
            groundwater head.
        """
        from numpy import sqrt, pi
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
        """Drawdown at specified radius (units L).

        Args:
            r (float) : radius at which to evaluate drawdown (units L).
        """
        from numpy import pi
        from scipy.special import k0
        d = k0(r/self.lfac) * self.qp/(2*pi*self.aq.T)
        return d

    def hr(self, r):
        """Head at sepcified radius (units L).

        Args:
            r (float) : radius at which to evaluate head (units L).
        """
        h = self.h0 - self.dr(r)
        return h

    def leakr(self, r):
        """Leakage rate at specified radius (units L/T).

        Args:
            r (float) : radius at which to evaluate leakage (units L).
        """
        lr = self.dr(r) * self.aq.Kleak/self.aq.Bleak
        return lr

    def dd(self, n=25, plot=True, csv='', xlsx=''):
        """Evaluate distance-drawdown.

        Evaluate steady-state drawdown at specified distances from the mine pit
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

    def info(self):
        """Print the solution information."""
        print('METHOD REFERENCE')
        print('----------------')
        print('Bouwer H. (2000) - Groundwater Hydrology.')
        print('\nRadial-symmetric, leaky-confined, horizontal flow to a large'
        '\ndiameter well. The solution estimates the steady-state inflow rate'
        '\nto the pit and drawdown with radial distance from the pit wall.')
        print('\nLower Aquifer Conceptual Model:')
        print('- Infinite, leaky and homogeneous lower aquifer.')
        print('- Mine pit is approximated by a cylinder.')
        print('- Mine pit fully penetrates lower aquifer.')
        print('- Steady, horizontal, axially symmetric and confined flow.')
        print('- Horizontal pre-mining groundwater head.')
        print('\nNotes:')
        print('- A steady state occurs when inflow to the mine pit is equal\n'
        '  to leakage from the upper aquifer to the lower aquifer.')
        print()

    def draw(self, dw=8):
        """Display the definition diagram.

        Args:
            dw (float) : Width of figure (default 8.0).

        """
        from pygaf.utils import display_image
        display_image('MineSteadyRadLeaky.png', dw=dw)
        return

class MineTransRadConfDD:
    """Transient, radial, confined flow to a large diameter well.

    Evaluate transient drawdown for a specified mine pit inflow. The
    MineTransRadConfDD class adopts the default Aq2dConf aquifer object with
    aquifer thickness 100.

    Attributes:
        aq (obj) : Lower aquifer object.

    """
    from pygaf.aquifers import Aq2dConf
    def __init__(self):
        self.aq = self.Aq2dConf(B=100, name='2D confined aquifer')
        self.rp = 100
        self.qp = 1000
        self.h0 = 110
        self.dp_targ = 10

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
        """float : Initial groundwater head (units L, default 110).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._h0

    @h0.setter
    def h0(self, v):
        if not (v > self.aq.B):
            raise Exception('Initial water level must be above aquifer top.')
        self._h0 = v

    @property
    def dp_targ(self):
        """float :  Mine pit drawdown target (units L, default 10).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._dp_targ

    @dp_targ.setter
    def dp_targ(self, v):
        if not (v > 0):
            raise Exception('Mine pit drawdown target must be positive.')
        self._dp_targ = v

    def drt(self, r, t):
        """Drawdown at specified radius and time (units L).

        Args:
            r (float) : radius (units L).
            t (float) : time (units T).
        """
        from numpy import pi
        from scipy.special import expn
        u = (r**2) * self.aq.S / (4.0 * self.aq.T * t)
        W = expn(1, u) # Well Function
        d = W * self.qp / (4.0 * pi * self.aq.T)
        return d

    def hrt(self, r, t):
        """Head at specified radius and time (units L).

        Args:
            r (float) : radius (units L).
            t (float) : time (units T).
        """
        h = self.h0 - self.drt(r, t)
        return h

    @property
    def dp_targ_time(self):
        """float : Time at which the mine pit drawdown target is reached
        (units T)."""
        t1 = 1 # intitialise
        t2 = 1.0e10 # initialise
        d1 = self.drt(self.rp, t1)
        d2 = self.drt(self.rp, t2)
        res = t2 - t1
        err = 0.01
        count = 0
        while abs(res) > err:
            count = count + 1
            t3 = t1 + (t2-t1)/2
            d3 = self.drt(self.rp, t3)
            if d3 < self.dp_targ:
                t1 = t3
            else:
                t2 = t3
            res = t2 - t1
            if count > 1000:
                raise Exception(('More than 1000 iterations solving dp_targ_time.'))
        return t3

    def ri(self, t):
        """Radius of influence at specified time.

        Defined as radius within which change in storage is equal to 95% of
        total discharge.

        Args:
            t (float) : time (units T).
        """
        from numpy import sqrt, log
        e = 0.95
        r = sqrt(log(1-e) * -4.0 * self.aq.T * t / self.aq.S)
        return r

    def dp(self, n=25, plot=True, csv='', xlsx=''):
        """Transient drawdown of mine pit water level.

        Evaluate transient drawdown of the water level in the mine pit.
        Results are returned in a Pandas dataframe. A drawdown graph is
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
        t = linspace(self.dp_targ_time/n, self.dp_targ_time, n)
        d = [self.drt(self.rp, i) for i in t]
        h = [self.hrt(self.rp, i) for i in t]
        r = [self.ri(i) for i in t]
        df = pandas.DataFrame()
        df['time'] = t
        df['drawdown'] = d
        df['head'] = h
        df['ri'] = r
        # Plot results
        if plot:
            import matplotlib.pyplot as plt
            df.plot(
                x='time', y='drawdown', grid=True, marker='.', lw=3, alpha=0.5,
                legend=False, ylabel='drawdown'
                )
            plt.axis([0, None, max(d), min(d)])
            plt.title('Time Drawdown at Mine Pit')
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

    def dd(self, t, n=25, plot=True, csv='', xlsx=''):
        """Evaluate radial-drawdown at specified time.

        Results are returned in a Pandas dataframe. A drawdown graph is
        displayed as default and can be suppressed by setting plot=False.

        Args:
            t (float) : Time for evaluating drawdown (units T).
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
        r = linspace(self.rp, self.ri(t), n)
        d = [self.drt(i, t) for i in r]
        h = [self.hrt(i, t) for i in r]
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
            plt.title('Radial Drawdown at Time: ' + str(round(t, 0)))
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

    def info(self):
        """Print the solution information."""
        print('METHOD REFERENCE')
        print('----------------')
        print('Leczfalvy S. (1982) - Simplified Mathematical Models for the\n'
        'Calculation of Dewatering.')
        print('\nRadial-symmetric, confined, horizontal flow to a large'
        '\ndiameter well. The solution estimates transient drawdown at the pit'
        '\nwall for a constant inflow rate to the pit.')
        print('\nAquifer Conceptual Model:')
        print('- Infinite, confined and homogeneous aquifer.')
        print('- Mine pit is approximated by a cylinder.')
        print('- Dewatering via an imaginary pumping well with radius rp.')
        print('- Mine pit fully penetrates aquifer.')
        print('- Transient, horizontal, axially symmetric and confined flow.')
        print('- Horizontal pre-mining groundwater head.')
        print('\nNotes:')
        print('- Inflow to the mine pit is constant and drawdown is transient.')
        print('- A steady state is not reached because all discharge is from\n'
        '  aquifer storage.')
        print()

    def draw(self, dw=8):
        """Display the drawing definition.

        Args:
            dw (float) : Width of figure (default 8.0).

        """
        from pygaf.utils import display_image
        display_image('MineTransRadConf.png', dw=dw)
        return

class MineSteadyStripUnconfQ:
    """Steady, unconfined 1D flow to mine pit wall.

    Evaluate steady-state mine inflow for a specified mine pit water level. The
    MineSteadyStripUnconfQ class adopts the default Aq2dUnconf aquifer object with
    initial saturated thickness 100.

    Attributes:
        aq (obj) : Aquifer object.

    """
    from pygaf.aquifers import Aq2dConf
    def __init__(self):
        self.aq = self.Aq2dConf(B=100, name='2D unconfined aquifer')
        self.hp = 90
        self.R = 1.0e-4
        self.Y = 1000

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
            raise Exception('Pit water level (hp) must be 0 < hp < B.')
        self._hp = v

    @property
    def dp(self):
        """float : Drawdown of mine pit water level from initial water table
        (units L, default 10).
        """
        return self.aq.B - self.hp

    @property
    def R(self):
        """float : Groundwater recharge rate (units L/T, default 1.0e-4).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._R

    @R.setter
    def R(self, v):
        if not (v > 0):
            raise Exception('Recharge rate (R) must be positive.')
        self._R = v

    @property
    def Y(self):
        """float : Length of mine strip (units L, default 1000).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._Y

    @Y.setter
    def Y(self, v):
        if not (v > 0):
            raise Exception('Mine strip length (Y) must be positive.')
        self._Y = v

    @property
    def xi(self):
        """float : Length of influence (units L)."""
        from numpy import sqrt
        l = sqrt(self.aq.K * (self.aq.B**2 - self.hp**2) / self.R)
        return l

    @property
    def qp(self):
        """float : Mine pit inflow rate (units L3/T)."""
        q = 2 * self.R * self.xi * self.Y
        return q


    def info(self):
        """Print the solution information."""
        print('METHOD REFERENCE')
        print('----------------')
        print('Singh R. N., Ngah S. A. and Atkins A. S. (1985) - Applicability'
        '\nof Current Groundwater Theories for the Prediction of Water Inflows'
        '\nto Surface mining Excavations.')
        print('\nMine strip with steady, unconfined, horizontal flow'
        '\nperpendicular to the mine pit wall. The solution estimates the'
        '\nsteady-state inflow rate and drawdown with distance from the pit'
        '\nwall.')
        print('\nConceptual Model:')
        print('- Semi-infinite, unconfined and homogeneous aquifer each side\n'
        '  of the mine pit.')
        print('- Mine pit walls are approximated by a vertical faces.')
        print('- Flow is steady, horizontal and perpendicular to the pit walls.')
        print('- Uniform recharge.')
        print('- Horizontal pre-mining water table.')
        print('- The mine pit should be long compared to its width such that\n'
        '  it is reasonable to neglect groundwater inflow from the end walls.')
        print('\nNotes:')
        print('- Steady state approximation is reasonable for moderate to\n'
        '  to large hydraulic conductivity and mine pits excavated over years.')
        print('- The length of influence is defined by the length of aquifer\n'
        '  over which recharge is equal to mine pit inflow.')
        print()

    def hx(self, x):
        """Head at specified distance from pit wall (units L).

        Args:
            x (float) : Distance from pit wall (units L).

        """
        from numpy import sqrt
        h = sqrt(self.hp**2 + self.R * (2*self.xi*x - x**2) / self.aq.K)
        return h

    def dx(self, x):
        """Drawdown at specified distance from pit wall (unit L).

        Args:
            x (float) : Distance from pit wall (units L).

        """
        d = self.aq.B - self.hx(x)
        return d

    def dd(self, n=25, plot=True, csv='', xlsx=''):
        """Evaluate distance-drawdown (units L).

        Evaluate steady-state drawdown at specified distances from the mine pit
        wall. Results are returned in a Pandas dataframe. A drawdown graph is
        displayed as default and can be suppressed by setting plot=False.

        Args:
            n (int) : Number of values for evaluating drawdown (default 25).
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
        x = linspace(0, self.xi, n)
        h = [self.hx(i) for i in x]
        d = [self.dx(i) for i in x]
        df = pandas.DataFrame()
        df['distance'] = x
        df['drawdown'] = d
        df['head'] = h
        # Plot results
        if plot:
            import matplotlib.pyplot as plt
            df.plot(
                x='distance', y='drawdown', grid=True, marker='.', lw=3,
                alpha=0.5, legend=False, ylabel='drawdown'
                )
            plt.axis([0, None, max(d), min(d)])
            plt.title('Distance Drawdown')
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

    def draw(self, dw=8):
        """Display the drawing definition.

        Args:
            dw (float) : Width of figure (default 8.0).

        """
        from pygaf.utils import display_image
        display_image('MineSteadyStripUnconf.png', dw=dw)
        return

class MineSteadyStripLeakyQ:
    """Steady, leaky 1D flow to mine pit wall.

    Evaluate steady-state mine inflow for a specified mine pit water level.
    The MineSteadyStripLeakyQ class adopts the default Aq2dLeaky aquifer
    object with aquifer thickness 100 for the confined aquifer.

    Attributes:
        aq (obj) : Aquifer object.

    """
    from pygaf.aquifers import Aq2dLeaky
    def __init__(self):
        self.aq = self.Aq2dLeaky(B=100, name='2d leaky aquifer')
        self.hp = 90
        self.h0 = 120
        self.Y = 1000
        return

    @property
    def hp(self):
        """float : Mine pit water level (units L, default 90).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._hp

    @hp.setter
    def hp(self, v):
        if not (v > 0):
            raise Exception('Pit water level (hp) must be positive.')
        self._hp = v

    @property
    def dp(self):
        """float : Drawdown of mine pit water level from initial water table
        (units L, default 10).
        """
        return self.h0 - self.hp

    @property
    def h0(self):
        """float : Initial groundwater head (units L, default 120).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._h0

    @h0.setter
    def h0(self, v):
        if not (v > (self.aq.B + self.aq.Bleak)):
            raise Exception('Initial water level must be above the aquitard.')
        self._h0 = v

    @property
    def Y(self):
        """float : Length of mine strip (units L, default 1000).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._Y

    @Y.setter
    def Y(self, v):
        if not (v > 0):
            raise Exception('Mine strip length (Y) must be positive.')
        self._Y = v

    @property
    def beta(self):
        """float : Solution term (units L)."""
        from numpy import sqrt
        b = sqrt(self.aq.K * self.aq.B * self.aq.Bleak / self.aq.Kleak)
        return b

    @property
    def xi(self):
        """float : Length of influence defined where drawdown is equal to 0.1%
        of initial aquifer head (units L).
        """
        from numpy import log
        e = 0.001
        l = -self.beta * log(e * self.h0 / self.dp)
        return l

    @property
    def qp(self):
        """float : Mine pit inflow rate (units L3/T)."""
        q = 2 * self.Y * self.aq.K * self.aq.B * self.dp / self.beta
        return q

    def info(self):
        """Print the solution information."""
        print('METHOD REFERENCE')
        print('----------------')
        print('Nguyen V. U. and Raudkivi A. J. 1982. Transient two-dimensional'
        '\ngroundwater flow. Hydrological Sciences; 4, 427-438.')
        print('\nMine strip with steady-state, leaky-confined, horizontal flow'
        '\nperpendicular to the pit wall. The solution estimates the inflow'
        '\nrate to the pit for prescribed drawdown at the pit wall.')
        print('\nLower Aquifer Conceptual Model:')
        print('- Infinite, leaky and homogeneous lower aquifer each side of'
        '\n  mine pit.')
        print('- Mine pit fully penetrates lower aquifer.')
        print('- Steady, horizontal, 1D and leaky flow.')
        print('- Horizontal pre-mining groundwater head.')
        print('- The mine pit should be long compared to its width such that\n'
        '  it is reasonable to neglect groundwater inflow from the end walls.')
        print('\nNotes:')
        print('- A steady state occurs when inflow to the mine pit is equal\n'
        '  to leakage from the upper aquifer to the lower aquifer.')
        print()

    def hx(self, x):
        """Head at specified distance from pit wall (units L).

        Args:
            x (float) : Distance from pit wall (units L).

        """
        from numpy import exp
        h = self.h0 - self.dp * exp(-x / self.beta)
        return h

    def dx(self, x):
        """Drawdown at specified distance from pit wall (unit L).

        Args:
            x (float) : Distance from pit wall (units L).

        """
        d = self.h0 - self.hx(x)
        return d

    def dd(self, n=25, plot=True, csv='', xlsx=''):
        """Evaluate distance-drawdown (units L).

        Evaluate steady-state drawdown at specified distances from the mine pit
        wall. Results are returned in a Pandas dataframe. A drawdown graph is
        displayed as default and can be suppressed by setting plot=False.

        Args:
            n (int) : Number of values for evaluating drawdown (default 25).
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
        x = linspace(0, self.xi, n)
        h = [self.hx(i) for i in x]
        d = [self.dx(i) for i in x]
        df = pandas.DataFrame()
        df['distance'] = x
        df['drawdown'] = d
        df['head'] = h
        # Plot results
        if plot:
            import matplotlib.pyplot as plt
            df.plot(
                x='distance', y='drawdown', grid=True, marker='.', lw=3,
                alpha=0.5, legend=False, ylabel='drawdown'
                )
            plt.axis([0, None, max(d), min(d)])
            plt.title('Distance Drawdown')
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

    def draw(self, dw=8):
        """Display the drawing definition.

        Args:
            dw (float) : Width of figure (default 8.0).

        """
        from pygaf.utils import display_image
        display_image('MineSteadyStripLeaky.png', dw=dw)
        return

class MineSteadyStripLeakyDD:
    """Steady, leaky 1D flow to mine pit wall.

    Evaluate steady-state mine drawdown for a specified mine pit inflow.
    The MineSteadyStripLeakyDD class adopts the default Aq2dLeaky aquifer
    object with aquifer thickness 100 for the confined aquifer.

    Attributes:
        aq (obj) : Aquifer object.

    """
    from pygaf.aquifers import Aq2dLeaky
    def __init__(self):
        self.aq = self.Aq2dLeaky(B=100, name='2D leaky aquifer')
        self.qp = 0.0
        self.h0 = 120
        self.Y = 1000
        return

    @property
    def qp(self):
        """float : Mine pit inflow rate (units L/T, default 0.0).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._qp

    @qp.setter
    def qp(self, v):
        if not (v >= 0):
            raise Exception('Pit inflow rate (qp) must be positive.')
        self._qp = v

    @property
    def h0(self):
        """float : Initial groundwater head (units L, default 120).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._h0

    @h0.setter
    def h0(self, v):
        if not (v > (self.aq.B + self.aq.Bleak)):
            raise Exception('Initial water level must be above the aquitard.')
        self._h0 = v

    @property
    def Y(self):
        """float : Length of mine strip (units L, default 1000).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._Y

    @Y.setter
    def Y(self, v):
        if not (v > 0):
            raise Exception('Mine strip length (Y) must be positive.')
        self._Y = v

    @property
    def beta(self):
        """float : Solution term (units L)."""
        from numpy import sqrt
        b = sqrt(self.aq.K * self.aq.B * self.aq.Bleak / self.aq.Kleak)
        return b

    @property
    def xi(self):
        """float : Length of influence defined where drawdown is equal to 0.1%
        of initial aquifer head (units L).
        """
        from numpy import log
        e = 0.001
        l = -self.beta * log(2 * e * self.h0 * self.aq.T / (self.qp * self.beta / self.Y))
        return l

    @property
    def hp(self):
        """float : Mine pit head (units L)."""
        from numpy import exp
        h = self.h0 - self.qp * self.beta / (self.Y * 2 * self.aq.T)
        return h

    @property
    def dp(self):
        """float : Mine pit drawdown (units L)."""
        d = self.h0 - self.hp
        return d

    def info(self):
        """Print the solution information."""
        print('METHOD REFERENCE')
        print('----------------')
        print('Nguyen V. U. and Raudkivi A. J. 1982. Transient two-dimensional'
        '\ngroundwater flow. Hydrological Sciences; 4, 427-438.')
        print('\nMine strip with steady-state, leaky-confined, horizontal flow'
        '\nperpendicular to the pit wall. The solution estimates the drawdown'
        '\nat the pit wall for prescribed total inflow to the pit from both'
        '\nside of the strip.')
        print('\nConceptual Model:')
        print('\nLower Aquifer Conceptual Model:')
        print('- Infinite, leaky and homogeneous lower aquifer each side of'
        '\n  mine pit.')
        print('- Mine pit fully penetrates lower aquifer.')
        print('- Steady, horizontal, 1D and leaky flow.')
        print('- Horizontal pre-mining groundwater head.')
        print('- The mine pit should be long compared to its width such that\n'
        '  it is reasonable to neglect groundwater inflow from the end walls.')
        print('\nNotes:')
        print('- A steady state occurs when inflow to the mine pit is equal\n'
        '  to leakage from the upper aquifer to the lower aquifer.')
        print()

    def hx(self, x):
        """Head at specified distance from pit wall (units L).

        Args:
            x (float) : Distance from pit wall (units L).

        """
        from numpy import exp
        h = self.h0 - self.qp * self.beta * exp(-x/self.beta) / (self.Y * 2 * self.aq.T)
        return h

    def dx(self, x):
        """Drawdown at specified distance from pit wall (unit L).

        Args:
            x (float) : Distance from pit wall (units L).

        """
        d = self.h0 - self.hx(x)
        return d

    def dd(self, n=25, plot=True, csv='', xlsx=''):
        """Evaluate distance-drawdown (units L).

        Evaluate steady-state drawdown at specified distances from the mine pit
        wall. Results are returned in a Pandas dataframe. A drawdown graph is
        displayed as default and can be suppressed by setting plot=False.

        Args:
            n (int) : Number of values for evaluating drawdown (default 25).
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
        x = linspace(0, self.xi, n)
        h = [self.hx(i) for i in x]
        d = [self.dx(i) for i in x]
        df = pandas.DataFrame()
        df['distance'] = x
        df['drawdown'] = d
        df['head'] = h
        # Plot results
        if plot:
            import matplotlib.pyplot as plt
            df.plot(
                x='distance', y='drawdown', grid=True, marker='.', lw=3,
                alpha=0.5, legend=False, ylabel='drawdown'
                )
            plt.axis([0, None, max(d), min(d)])
            plt.title('Distance Drawdown')
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

    def draw(self, dw=8):
        """Display the drawing definition.

        Args:
            dw (float) : Width of figure (default 8.0).

        """
        from pygaf.utils import display_image
        display_image('MineSteadyStripLeaky.png', dw=dw)
        return

class MineTransStripUnconfQ:
    """Transient, unconfined 1D flow to mine pit wall.

    Evaluate transient inflow for a specified mine pit water level.
    The MineTransStripUnconfQ class adopts the default Aq2dUnconf aquifer
    object with initial saturated thickness 100.

    Attributes:
        aq (obj) : Aquifer object.

    """
    from pygaf.aquifers import Aq2dUnconf
    def __init__(self):
        self.aq = self.Aq2dUnconf(B=100, name='2D unconfined aquifer')
        self.hp = 90.0
        self.Y = 1000
        return

    @property
    def hp(self):
        """float : Mine pit water level (units L, default 90).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._hp

    @hp.setter
    def hp(self, v):
        if not (v > 0):
            raise Exception('Pit water level (hp) must be positive.')
        self._hp = v

    @property
    def dp(self):
        """float : Drawdown of mine pit water level (units L)."""
        return self.aq.B - self.hp

    @property
    def Y(self):
        """float : Length of mine strip (units L, default 1000).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._Y

    @Y.setter
    def Y(self, v):
        if not (v > 0):
            raise Exception('Mine strip length (Y) must be positive.')
        self._Y = v

    def xi(self, t):
        """Length of influence at specified time, defined where drawdown
        is equal to 0.1% of initial aquifer head (units L).

        Args:
            t (float) : time (units T)
        """
        from scipy.special import erfinv
        from numpy import sqrt
        e = 0.001
        t1 = sqrt(4 * self.aq.T * t / self.aq.Sy)
        t2 = ((self.aq.B - e*self.aq.B)**2 - self.hp**2) / (self.aq.B**2 - self.hp**2)
        l = t1 * erfinv(t2)
        return l

    def qp(self, t):
        """Inflow to mine pit at specified time (units L3/T).

        Args:
            t (float) : time (units T)
        """
        from numpy import sqrt, pi
        e = 0.001
        t1 = self.Y * self.aq.K * (self.aq.B**2 - self.hp**2)
        t2 = self.aq.Sy / (pi * self.aq.T * t)
        q = t1 * sqrt(t2)
        return q

    def qp_cum(self, t):
        """Cumulative inflow to mine pit at specified time (units L3).

        Args:
            t (float) : time (units T)
        """
        from numpy import sqrt, pi
        e = 0.001
        t1 = 2 * self.Y * self.aq.K * t * (self.aq.B**2 - self.hp**2)
        t2 = self.aq.Sy / (pi * self.aq.T * t)
        q = t1 * sqrt(t2)
        return q

    def info(self):
        """Print the solution information."""
        print('METHOD REFERENCE')
        print('----------------')
        print('Nguyen V. U. and Raudkivi A. J. 1982. Transient two-dimensional'
        '\ngroundwater flow. Hydrological Sciences; 4, 427-438.')
        print('\nMine strip with transient, unconfined, horizontal flow'
        '\nperpendicular to the pit wall. The solution estimates the transient'
        '\ninflow rate for constant drawdown at the pit wall.')
        print('\nConceptual Model:')
        print('- Infinite, unconfined and homogeneous aquifer each side of mine pit.')
        print('- Mine pit fully penetrates the aquifer.')
        print('- Transient, horizontal, 1D and unconfined flow.')
        print('- Horizontal pre-mining groundwater head.')
        print('- The mine pit should be long compared to its width such that\n'
        '  it is reasonable to neglect groundwater inflow from the end walls.')
        print('\nNotes:')
        print('- Time zero corresponds to an instantaneous drawdown of the mine pit\n'
        '  water level from the initial condition.')
        print('- No steady state is reached (inflow tends toward zero at large times).')
        print('- The analytical solution was obtained by linearising the non-linear\n'
        '  PDE; the soultion will be most reliable when dp is small compared to hp.')
        print()

    def hxt(self, x, t):
        """Head at specified distance and time (units L).

        Args:
            x (float) : distance from pit wall (units L).
            t (float) : time (units T).
        """
        from scipy.special import erf
        from numpy import sqrt
        t1 = self.aq.B**2 - self.hp**2
        t2 = x * sqrt(self.aq.Sy / (4 * self.aq.T * t))
        h = sqrt(self.hp**2 + t1 * erf(t2))
        return h

    def dxt(self, x, t):
        """Drawdown at specified distance and time (units L).

        Args:
            x (float) : distance from pit wall (units L).
            t (float) : time (units T).
        """
        return self.aq.B - self.hxt(x,t)

    def draw(self, dw=8):
        """Display the drawing definition.

        Args:
            dw (float) : Width of figure (default 8.0).

        """
        from pygaf.utils import display_image
        display_image('MineTransStripUnconf.png', dw=dw)
        return

    def dd(self, t, n=25, plot=True, csv='', xlsx=''):
        """Evaluate distance-drawdown at specified time(units L).

        Evaluate drawdown at specified distances from the mine pit wall at
        specified time. Results are returned in a Pandas dataframe. A drawdown
        grapph is displayed as default and can be suppressed by setting plot=False.

        Args:
            t (float) : Time (units T)
            n (int) : Number of values for evaluating drawdown (default 25).
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
        x = linspace(0, self.xi(t), n)
        h = [self.hxt(i,t) for i in x]
        d = [self.dxt(i,t) for i in x]
        df = pandas.DataFrame()
        df['distance'] = x
        df['drawdown'] = d
        df['head'] = h
        # Plot results
        if plot:
            import matplotlib.pyplot as plt
            df.plot(
                x='distance', y='drawdown', grid=True, marker='.', lw=3,
                alpha=0.5, legend=False, ylabel='drawdown'
                )
            plt.axis([0, None, max(d), min(d)])
            plt.title('Distance Drawdown')
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

class MineTransStripConfQ:
    """Transient, confined 1D flow to mine pit wall.

    Evaluate transient inflow for a specified mine pit water level.
    The MineTransStripConfQ class adopts the default Aq2dConf aquifer
    object with aquifer thickness 100.

    Attributes:
        aq (obj) : Aquifer object.

    """
    from pygaf.aquifers import Aq2dConf
    def __init__(self):
        self.aq = self.Aq2dConf(B=100, name='2D confined aquifer')
        self.hp = 90.0
        self.Y = 1000
        self.h0 = 120.0
        return

    def info(self):
        """Print the solution information."""
        print('METHOD REFERENCE')
        print('----------------')
        print('Nguyen V. U. and Raudkivi A. J. 1982. Transient two-dimensional'
        '\ngroundwater flow. Hydrological Sciences; 4, 427-438.')
        print('\nMine strip with transient, unconfined, horizontal flow perpendicular'
        '\nto the pit wall. The solution estimates the transient inflow rate'
        '\nfor constant drawdown at the pit wall.')
        print('\nConceptual Model:')
        print('- Infinite, confined and homogeneous aquifer each side of mine pit.')
        print('- Mine pit fully penetrates the aquifer.')
        print('- Transient, horizontal, 1D and confined flow.')
        print('- Horizontal pre-mining groundwater head.')
        print('- The mine pit should be long compared to its width such that\n'
        '  it is reasonable to neglect groundwater inflow from the end walls.')
        print('\nNotes:')
        print('- Time zero corresponds to an instantaneous drawdown of the mine pit\n'
        '  water level from the initial condition.')
        print('- No steady state is reached (inflow tends toward zero at large times).')
        print()

    def draw(self, dw=8):
        """Display the drawing definition.

        Args:
            dw (float) : Width of figure (default 8.0).

        """
        from pygaf.utils import display_image
        display_image('MineTransStripConf.png', dw=dw)
        return

    @property
    def hp(self):
        """float : Mine pit water level (units L, default 90).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._hp

    @hp.setter
    def hp(self, v):
        if not (v > 0):
            raise Exception('Pit water level (hp) must be positive.')
        self._hp = v

    @property
    def dp(self):
        """float : Drawdown of mine pit water level (units L)."""
        return self.aq.B - self.hp

    @property
    def Y(self):
        """float : Length of mine strip (units L, default 1000).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._Y

    @Y.setter
    def Y(self, v):
        if not (v > 0):
            raise Exception('Mine strip length (Y) must be positive.')
        self._Y = v

    @property
    def h0(self):
        """float : Initial groundwater head (units L, default 110).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._h0

    @h0.setter
    def h0(self, v):
        if not (v > self.aq.B):
            raise Exception('Initial water level must be above aquifer top.')
        self._h0 = v

    def xi(self, t):
        """Length of influence at specified time, defined where drawdown
        is equal to 0.1% of initial aquifer head (units L).

        Args:
            t (float) : time (units T)
        """
        from scipy.special import erfcinv
        from numpy import sqrt
        e = 0.001
        t1 = 4 * self.aq.T * t / self.aq.S
        t2 = e * self.h0 / (self.h0 - self.hp)
        l = sqrt(t1) * erfcinv(t2)
        return l

    def qp(self, t):
        """Inflow to mine pit at specified time (units L3/T).

        Args:
            t (float) : time (units T)
        """
        from numpy import sqrt, pi
        e = 0.001
        t1 = 2 * self.Y * self.aq.T * (self.h0 - self.hp)
        t2 = self.aq.S / (pi * self.aq.T * t)
        q = t1 * sqrt(t2)
        return q

    def qp_cum(self, t):
        """Cumulative inflow to mine pit at specified time (units L3).

        Args:
            t (float) : time (units T)
        """
        from numpy import sqrt, pi
        e = 0.001
        t1 = 4 * self.Y * self.aq.T * t * (self.h0 - self.hp)
        t2 = self.aq.S / (pi * self.aq.T * t)
        q = t1 * sqrt(t2)
        return q

    def dxt(self, x, t):
        """Drawdown at specified distance and time (units L).

        Args:
            x (float) : distance from pit wall (units L).
            t (float) : time (units T).
        """
        from scipy.special import erfc
        from numpy import sqrt
        t1 = self.h0 - self.hp
        t2 = x * sqrt(self.aq.S / (4 * self.aq.T * t))
        d = t1 * erfc(t2)
        return d

    def hxt(self, x, t):
        """Head at specified distance and time (units L).

        Args:
            x (float) : distance from pit wall (units L).
            t (float) : time (units T).
        """
        return self.h0 - self.dxt(x,t)

    def dd(self, t, n=25, plot=True, csv='', xlsx=''):
        """Evaluate distance-drawdown at specified time(units L).

        Evaluate drawdown at specified distances from the mine pit wall at
        specified time. Results are returned in a Pandas dataframe. A drawdown
        grapph is displayed as default and can be suppressed by setting plot=False.

        Args:
            t (float) : Time (units T)
            n (int) : Number of values for evaluating drawdown (default 25).
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
        x = linspace(0, self.xi(t), n)
        h = [self.hxt(i,t) for i in x]
        d = [self.dxt(i,t) for i in x]
        df = pandas.DataFrame()
        df['distance'] = x
        df['drawdown'] = d
        df['head'] = h
        # Plot results
        if plot:
            import matplotlib.pyplot as plt
            df.plot(
                x='distance', y='drawdown', grid=True, marker='.', lw=3,
                alpha=0.5, legend=False, ylabel='drawdown'
                )
            plt.axis([0, None, max(d), min(d)])
            plt.title('Distance Drawdown')
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

class MineTransStripLeakyQ:
    """Transient, leaky 1D flow to mine pit wall.

    Evaluate transient inflow for a specified mine pit water level.
    The MineTransStripLeakyQ class adopts the default Aq2dLeaky aquifer
    object with aquifer thickness 100.

    Attributes:
        aq (obj) : Aquifer object.

    """
    from pygaf.aquifers import Aq2dLeaky
    def __init__(self):
        self.aq = self.Aq2dLeaky(B=100, name='2D leaky aquifer')
        self.hp = 90.0
        self.Y = 1000
        self.h0 = 120.0
        return

    def info(self):
        """Print the solution information."""
        print('METHOD REFERENCE')
        print('----------------')
        print('Nguyen V. U. and Raudkivi A. J. 1982. Transient two-dimensional'
        '\ngroundwater flow. Hydrological Sciences; 4, 427-438.')
        print('\nMine strip with transient, leaky-confined, horizontal flow'
        '\nperpendicular to the pit wall. The solution estimates the transient'
        '\ninflow rate for constant drawdown at the pit wall.')
        print('\nConceptual Model:')
        print('- Infinite, leaky and homogeneous aquifer each side of mine pit.')
        print('- Mine pit fully penetrates the aquifer.')
        print('- Transient, horizontal, 1D and leaky flow.')
        print('- Horizontal pre-mining groundwater head.')
        print('- The mine pit should be long compared to its width such that\n'
        '  it is reasonable to neglect groundwater inflow from the end walls.')
        print('\nNotes:')
        print('- Time zero corresponds to an instantaneous drawdown of the mine pit\n'
        '  water level from the initial condition.')
        print('- A steady state can be reached when inflow to the pit is matched\n'
        '  by leakage from the upper aquifer to the lower aquifer.')
        print()

    def draw(self, dw=8):
        """Display the drawing definition.

        Args:
            dw (float) : Width of figure (default 8.0).

        """
        from pygaf.utils import display_image
        display_image('MineTransStripLeaky.png', dw=dw)
        return

    @property
    def hp(self):
        """float : Mine pit water level (units L, default 90).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._hp

    @hp.setter
    def hp(self, v):
        if not (v > 0):
            raise Exception('Pit water level (hp) must be positive.')
        self._hp = v

    @property
    def dp(self):
        """float : Drawdown of mine pit water level (units L)."""
        return self.h0 - self.hp

    @property
    def Y(self):
        """float : Length of mine strip (units L, default 1000).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._Y

    @Y.setter
    def Y(self, v):
        if not (v > 0):
            raise Exception('Mine strip length (Y) must be positive.')
        self._Y = v

    @property
    def h0(self):
        """float : Initial groundwater head (units L, default 110).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._h0

    @h0.setter
    def h0(self, v):
        if not (v > (self.aq.B + self.aq.Bleak)):
            raise Exception('Initial water level must be above aquitard top.')
        self._h0 = v

    @property
    def beta(self):
        "float : Leakage factor."
        from numpy import sqrt
        t1 = self.aq.K * self.aq.B * self.aq.Bleak / self.aq.Kleak
        return sqrt(t1)

    @property
    def xi_steady(self):
        """Length of influence at specified time, defined where drawdown
        is equal to 0.1% of initial aquifer head (units L)."""
        from numpy import log
        e = 0.001
        return -self.beta * log(e * self.h0 / self.dp)

    @property
    def qp_steady(self):
        """float : Inflow to mine pit at steady state (units L3/T)."""
        return 2 * self.Y * self.aq.T * self.dp / self.beta

    def qp(self, t):
        """Inflow to mine pit at specified time (units L3/T).

        Args:
            t (float) : time (units T)
        """
        from numpy import sqrt, exp, pi
        from scipy.special import erfc
        t1 = 2 * self.Y * self.aq.T
        t2 = self.dp / self.beta
        t3 = exp(-self.aq.D*t/self.beta**2) * self.dp / (2*sqrt(self.aq.D*t))
        t4 = erfc(sqrt(self.aq.D*t)/self.beta) * sqrt(pi)*self.dp / (2*self.beta)
        q = t1 * (t2 + t3 - t4)
        return q

    def hxt(self, x, t):
        """Head at specified distance and time (units L).

        Args:
            x (float) : distance from pit wall (units L).
            t (float) : time (units T).
        """
        from scipy.special import erfc
        from numpy import sqrt, exp, pi
        alpha = (sqrt(self.aq.D*t)/self.beta) - (x/(2*sqrt(self.aq.D*t)))
        gamma = (sqrt(self.aq.D*t)/self.beta) + (x/(2*sqrt(self.aq.D*t)))
        t1 = self.dp * exp(-x/self.beta)
        t2 = sqrt(pi)*self.dp/4
        t3 = exp(-x/self.beta) * erfc(alpha) - exp(x/self.beta) * erfc(gamma)
        return self.h0 - t1 + t2*t3

    def dxt(self, x, t):
        """Drawdown at specified distance and time (units L).

        Args:
            x (float) : distance from pit wall (units L).
            t (float) : time (units T).
        """
        return self.h0 - self.hxt(x,t)

    def dd(self, t, n=25, plot=True, csv='', xlsx=''):
        """Evaluate distance-drawdown at specified time(units L).

        Evaluate drawdown at specified distances from the mine pit wall at
        specified time. Results are returned in a Pandas dataframe. A drawdown
        grapph is displayed as default and can be suppressed by setting plot=False.

        Args:
            t (float) : Time (units T)
            n (int) : Number of values for evaluating drawdown (default 25).
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
        x = linspace(0, self.xi_steady, n)
        h = [self.hxt(i,t) for i in x]
        d = [self.dxt(i,t) for i in x]
        df = pandas.DataFrame()
        df['distance'] = x
        df['drawdown'] = d
        df['head'] = h
        # Plot results
        if plot:
            import matplotlib.pyplot as plt
            df.plot(
                x='distance', y='drawdown', grid=True, marker='.', lw=3,
                alpha=0.5, legend=False, ylabel='drawdown'
                )
            plt.axis([0, None, max(d), min(d)])
            plt.title('Distance Drawdown')
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
