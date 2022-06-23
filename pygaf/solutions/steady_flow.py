class Steady1dConfFlow:
    """Steady state flow in a 1D confined aquifer.

    The default Steady1dFlow object...

    Attributes:
        aq (obj) : Aquifer object.
        x0_bc (obj) : SteadyBC object at x=0 (default type=2).
        xL_bc (obj) : SteadyBC object at x=L (default type=1).
        R (float) : Groundwater recharge rate (units L/T, default 0.0)

    """
    from pygaf.aquifers import Aq1dFiniteConf
    from pygaf.bcs import SteadyBC
    def __init__(self, aq=Aq1dFiniteConf(), x0_bc=SteadyBC(type=2),
    xL_bc=SteadyBC(type=1), R=0.0):
        self.aq = aq
        self.x0_bc = x0_bc
        self.xL_bc = xL_bc
        self.R = R
        return


    def bc_t2_t1(self, H, Q, L, T, R, x):
        """Aquifer solution for type 2 bc at x=0 and type 1 bc at x=L."""
        h = H + R*(L**2-x**2)/(2*T) + Q*(L-x)/T
        q = R*x + Q
        return h, q

    def bc_t1_t2(self, H, Q, L, T, R, x):
        """Aquifer solution for type 1 bc at x=0 and type 2 bc at x=L."""
        h = H + R*x**2/(2*T) + Q*x/T
        q = R*(L-x) + Q
        return h, q


    def head(self, n=25, plot=True, csv='', xlsx=''):
        """Calculate aquifer head.

        Args:
            n (int) : Number of evenly-spaced x values at which to evaluate
                aquifer head.
            csv (str) : Filepath for export of results to csv file; results
                are exported if the string is not empty (default '').
            xlsx (str) : Filepath for export of result to xlsx file; results
                are exported if the string is not empty (default '').

        Returns:
            Pandas dataframe containing head values.

        """
        import pandas
        df = pandas.DataFrame()
        df['x'] = [i * self.aq.L / (n-1) for i in range(n)]
        if self.x0_bc.type==2 and self.xL_bc.type==1:
            hds = []
            for x in list(df.x):
                h, q = self.bc_t2_t1(
                    self.xL_bc.value['head'],
                    self.x0_bc.value['flow'],
                    self.aq.L, self.aq.T, self.R, x
                    )
                hds.append(h)
            df['h'] = hds
        return df
