class Steady1dConfFlow:
    """Steady state flow in a 1D confined aquifer.

    The Steady1dConfFlow class adopts the default Aq1dFiniteConf aquifer object,
    default SteadyBC type 2 boundary condition object at x=0, and default
    SteadyBC type 1 boundary condition object at x=L.

    Attributes:
        aq (obj) : Aquifer object.
        bc0 (obj) : SteadyBC object at x=0 (default type=2).
        bcL (obj) : SteadyBC object at x=L (default type=1).
        R (float) : Groundwater recharge rate (units L/T, default 0.0)

    """
    from pygaf.aquifers import Aq1dFiniteConf
    from pygaf.bcs import SteadyBC
    def __init__(self):
        self.aq = self.Aq1dFiniteConf()
        self.bc0 = self.SteadyBC(type=2)
        self.bcL = self.SteadyBC(type=1)
        self.R = 0.0
        return


    @property
    def types(self):
        """int : Boundary condition types."""
        bc_types = [self.bc0.type, self.bcL.type]
        if not (1 in bc_types):
            raise Exception(
                'At least one boundary condition must be type 1.'
            )
        return bc_types


    def bc_t2_t1(self, H, Q, L, T, R, x):
        """Aquifer solution for type 2 bc at x=0 and type 1 bc at x=L."""
        h = H + R*(L**2-x**2)/(2*T) + Q*(L-x)/T
        q = R*x + Q
        h_grad = q/T
        return h, q, h_grad


    def bc_t1_t1(self, H0, HL, L, T, R, x):
        """Aquifer solution for type 1 bc at x=0 and type 1 bc at x=L."""
        h = H0*(1-(x/L)) + HL*(x/L) + R*(L*x-x**2)/(2*T)
        q = T*(H0-HL)/L - R*(L-2*x)/2
        h_grad = q/T
        return h, q, h_grad


    def info(self):
        """Print the solution information."""
        print('FLOW SOLUTION INFORMATION')
        print('-------------------------')
        print('Flow in', self.aq.type)
        print('BC at x=0: type', str(self.bc0.type)+',', self.bc0.value)
        print('BC at x=L: type', str(self.bcL.type)+',', self.bcL.value)
        print('Recharge rate:', self.R, '[L/T]')
        print()
        return


    def h(self, n=25, plot=True, csv='', xlsx=''):
        """Evaluate aquifer head.

        Args:
            n (int) : Number of evenly-spaced x values at which to evaluate
                aquifer head.
            plot (bool) : Display a plot of the results (default True).
            csv (str) : Filepath for export of results to csv file; results
                are exported if the string is not empty (default '').
            xlsx (str) : Filepath for export of result to xlsx file; results
                are exported if the string is not empty (default '').

        Returns:
            Pandas dataframe containing head values.

        """
        import pandas
        import matplotlib.pyplot as plt
        df = pandas.DataFrame()
        df['x'] = [i * self.aq.L / (n-1) for i in range(n)]
        head = []
        if self.bc0.type==2 and self.bcL.type==1:
            for x in list(df.x):
                h, q, g = self.bc_t2_t1(
                    self.bcL.value['head'], self.bc0.value['flow'],
                    self.aq.L, self.aq.T, self.R, x
                    )
                if h <= self.aq.bot:
                    raise Exception('Aquifer is dry at x = ' + str(x))
                head.append(h)
            df['h'] = head
        elif self.bc0.type==1 and self.bcL.type==1:
            for x in list(df.x):
                h, q, g = self.bc_t1_t1(
                    self.bc0.value['head'], self.bcL.value['head'],
                    self.aq.L, self.aq.T, self.R, x
                    )
                if h <= self.aq.bot:
                    raise Exception('Aquifer is dry at x = ' + str(x))
                head.append(h)
            df['h'] = head
        # Plot results
        if plot:
            df.plot(
                x='x', y='h', figsize=(10,3), marker='.', lw=3, alpha=0.5
                )
            plt.plot(
                [min(list(df.x)), max(list(df.x))], [self.aq.bot, self.aq.bot],
                '-', c='black', lw=3, alpha=0.5)
            plt.title('Aquifer Head')
            plt.ylabel('Elevation')
            plt.axis([None, None, self.aq.bot-(max(head)-self.aq.bot)*0.1, None])
            plt.legend(['aquifer head', 'aquifer bottom'])
            plt.grid(True)
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
        return df


    def q(self, n=25, plot=True, csv='', xlsx=''):
        """Evaluate aquifer flow.

        Args:
            n (int) : Number of evenly-spaced x values at which to evaluate
                aquifer flow.
            plot (bool) : Display a plot of the results (default True).
            csv (str) : Filepath for export of results to csv file; results
                are exported if the string is not empty (default '').
            xlsx (str) : Filepath for export of result to xlsx file; results
                are exported if the string is not empty (default '').

        Returns:
            Pandas dataframe containing head values.

        """
        import pandas
        import matplotlib.pyplot as plt
        df = pandas.DataFrame()
        df['x'] = [i * self.aq.L / (n-1) for i in range(n)]
        flow = []
        if self.bc0.type==2 and self.bcL.type==1:
            for x in list(df.x):
                h, flx, g = self.bc_t2_t1(
                    self.bcL.value['head'], self.bc0.value['flow'],
                    self.aq.L, self.aq.T, self.R, x
                    )
                if h <= self.aq.bot:
                    raise Exception('Aquifer is dry at x = ' + str(x))
                flow.append(flx)
            df['q'] = flow
        elif self.bc0.type==1 and self.bcL.type==1:
            for x in list(df.x):
                h, flx, g = self.bc_t1_t1(
                    self.bc0.value['head'], self.bcL.value['head'],
                    self.aq.L, self.aq.T, self.R, x
                    )
                if h <= self.aq.bot:
                    raise Exception('Aquifer is dry at x = ' + str(x))
                flow.append(flx)
            df['q'] = flow
        # Plot results
        if plot:
            df.plot(x='x', y='q', figsize=(10,3), marker='.', lw=3, alpha=0.5)
            plt.title('Aquifer Flow')
            plt.ylabel('Flow rate')
            plt.legend(['aquifer flow'])
            plt.grid(True)
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
        return df


    def h_grad(self, n=25, plot=True, csv='', xlsx=''):
        """Evaluate aquifer head gradient.

        Args:
            n (int) : Number of evenly-spaced x values at which to evaluate
                aquifer flow.
            plot (bool) : Display a plot of the results (default True).
            csv (str) : Filepath for export of results to csv file; results
                are exported if the string is not empty (default '').
            xlsx (str) : Filepath for export of result to xlsx file; results
                are exported if the string is not empty (default '').

        Returns:
            Pandas dataframe containing head values.

        """
        import pandas
        import matplotlib.pyplot as plt
        df = pandas.DataFrame()
        df['x'] = [i * self.aq.L / (n-1) for i in range(n)]
        grad = []
        if self.bc0.type==2 and self.bcL.type==1:
            for x in list(df.x):
                h, q, g = self.bc_t2_t1(
                    self.bcL.value['head'], self.bc0.value['flow'],
                    self.aq.L, self.aq.T, self.R, x
                    )
                if h <= self.aq.bot:
                    raise Exception('Aquifer is dry at x = ' + str(x))
                grad.append(g)
            df['h_grad'] = grad
        elif self.bc0.type==1 and self.bcL.type==1:
            for x in list(df.x):
                h, q, g = self.bc_t1_t1(
                    self.bc0.value['head'], self.bcL.value['head'],
                    self.aq.L, self.aq.T, self.R, x
                    )
                if h <= self.aq.bot:
                    raise Exception('Aquifer is dry at x = ' + str(x))
                grad.append(g)
            df['h_grad'] = grad
        # Plot results
        if plot:
            df.plot(x='x', y='h_grad', figsize=(10,3), marker='.', lw=3, alpha=0.5)
            plt.title('Head Gradient')
            plt.ylabel('Rate of head change')
            plt.legend(['head gradient'])
            plt.grid(True)
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
        return df


class Steady1dUnconfFlow:
    """Steady state flow in a 1D unconfined aquifer.

    The Steady1dUnconfFlow class adopts the default Aq1dFiniteUnconf aquifer object,
    default SteadyBC type 2 boundary condition object at x=0, and default
    SteadyBC type 1 boundary condition object at x=L.

    Attributes:
        aq (obj) : Aquifer object.
        bc0 (obj) : SteadyBC object at x=0 (default type=2).
        bcL (obj) : SteadyBC object at x=L (default type=1).
        R (float) : Groundwater recharge rate (units L/T, default 0.0)

    """
    from pygaf.aquifers import Aq1dFiniteUnconf
    from pygaf.bcs import SteadyBC
    def __init__(self):
        self.aq = self.Aq1dFiniteUnconf()
        self.bc0 = self.SteadyBC(type=2)
        self.bcL = self.SteadyBC(type=1)
        self.R = 0.0
        return


    @property
    def types(self):
        """int : Boundary condition types."""
        bc_types = [self.bc0.type, self.bcL.type]
        if not (1 in bc_types):
            raise Exception(
                'At least one boundary condition must be type 1.'
            )
        return bc_types


    def bc_t2_t1(self, H, Q, L, K, R, x):
        """Aquifer solution for type 2 bc at x=0 and type 1 bc at x=L."""
        from numpy import sqrt
        if (H**2 + R*(L**2-x**2)/K + 2*Q*(L-x)/K) < 0:
            raise Exception('Aquifer is dry at x = ' + str(x))
        h = sqrt(H**2 + R*(L**2-x**2)/K + 2*Q*(L-x)/K)
        q = R*x + Q
        h_grad = q/(K*h)
        return h, q, h_grad

    def bc_t1_t1(self, H0, HL, L, K, R, x):
        """Aquifer solution for type 1 bc at x=0 and type 1 bc at x=L."""
        from numpy import sqrt
        h = sqrt((H0**2)*(1-(x/L)) + (HL**2)*(x/L) + R*(L*x-x**2)/K)
        q = K*(H0-HL)/(2*L) - R*(L-2*x)/2
        h_grad = q/(K*h)
        return h, q, h_grad


    def info(self):
        """Print the solution information."""
        print('FLOW SOLUTION INFORMATION')
        print('-------------------------')
        print('Flow in', self.aq.type)
        print('BC at x=0: type', str(self.bc0.type)+',', self.bc0.value)
        print('BC at x=L: type', str(self.bcL.type)+',', self.bcL.value)
        print('Recharge rate:', self.R, '[L/T]')
        print()
        return


    def h(self, n=25, plot=True, csv='', xlsx=''):
        """Evaluate aquifer head.

        Args:
            n (int) : Number of evenly-spaced x values at which to evaluate
                aquifer head.
            plot (bool) : Display a plot of the results (default True).
            csv (str) : Filepath for export of results to csv file; results
                are exported if the string is not empty (default '').
            xlsx (str) : Filepath for export of result to xlsx file; results
                are exported if the string is not empty (default '').

        Returns:
            Pandas dataframe containing head values.

        """
        import pandas
        import matplotlib.pyplot as plt
        df = pandas.DataFrame()
        df['x'] = [i * self.aq.L / (n-1) for i in range(n)]
        head = []
        if self.bc0.type==2 and self.bcL.type==1:
            for x in list(df.x):
                h, q, g = self.bc_t2_t1(
                    self.bcL.value['head'], self.bc0.value['flow'],
                    self.aq.L, self.aq.K, self.R, x
                    )
                if h <= self.aq.bot:
                    raise Exception('Aquifer is dry at x = ' + str(x))
                head.append(h)
            df['h'] = head
        elif self.bc0.type==1 and self.bcL.type==1:
            for x in list(df.x):
                h, q, g = self.bc_t1_t1(
                    self.bc0.value['head'], self.bcL.value['head'],
                    self.aq.L, self.aq.K, self.R, x
                    )
                if h <= self.aq.bot:
                    raise Exception('Aquifer is dry at x = ' + str(x))
                head.append(h)
            df['h'] = head
        # Plot results
        if plot:
            df.plot(
                x='x', y='h', figsize=(10,3), marker='.', lw=3, alpha=0.5
                )
            plt.plot(
                [min(list(df.x)), max(list(df.x))], [self.aq.bot, self.aq.bot],
                '-', c='black', lw=3, alpha=0.5)
            plt.title('Aquifer Head')
            plt.ylabel('Elevation')
            plt.axis([None, None, self.aq.bot-(max(head)-self.aq.bot)*0.1, None])
            plt.legend(['aquifer head', 'aquifer bottom'])
            plt.grid(True)
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
        return df


    def q(self, n=25, plot=True, csv='', xlsx=''):
        """Evaluate aquifer flow.

        Args:
            n (int) : Number of evenly-spaced x values at which to evaluate
                aquifer flow.
            plot (bool) : Display a plot of the results (default True).
            csv (str) : Filepath for export of results to csv file; results
                are exported if the string is not empty (default '').
            xlsx (str) : Filepath for export of result to xlsx file; results
                are exported if the string is not empty (default '').

        Returns:
            Pandas dataframe containing head values.

        """
        import pandas
        import matplotlib.pyplot as plt
        df = pandas.DataFrame()
        df['x'] = [i * self.aq.L / (n-1) for i in range(n)]
        flow = []
        if self.bc0.type==2 and self.bcL.type==1:
            for x in list(df.x):
                h, flx, g = self.bc_t2_t1(
                    self.bcL.value['head'], self.bc0.value['flow'],
                    self.aq.L, self.aq.K, self.R, x
                    )
                if h <= self.aq.bot:
                    raise Exception('Aquifer is dry at x = ' + str(x))
                flow.append(flx)
            df['q'] = flow
        elif self.bc0.type==1 and self.bcL.type==1:
            for x in list(df.x):
                h, flx, g = self.bc_t1_t1(
                    self.bc0.value['head'], self.bcL.value['head'],
                    self.aq.L, self.aq.K, self.R, x
                    )
                if h <= self.aq.bot:
                    raise Exception('Aquifer is dry at x = ' + str(x))
                flow.append(flx)
            df['q'] = flow
        # Plot results
        if plot:
            df.plot(x='x', y='q', figsize=(10,3), marker='.', lw=3, alpha=0.5)
            plt.title('Aquifer Flow')
            plt.ylabel('Flow rate')
            plt.legend(['aquifer flow'])
            plt.grid(True)
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
        return df


    def h_grad(self, n=25, plot=True, csv='', xlsx=''):
        """Evaluate aquifer head gradient.

        Args:
            n (int) : Number of evenly-spaced x values at which to evaluate
                aquifer flow.
            plot (bool) : Display a plot of the results (default True).
            csv (str) : Filepath for export of results to csv file; results
                are exported if the string is not empty (default '').
            xlsx (str) : Filepath for export of result to xlsx file; results
                are exported if the string is not empty (default '').

        Returns:
            Pandas dataframe containing head values.

        """
        import pandas
        import matplotlib.pyplot as plt
        df = pandas.DataFrame()
        df['x'] = [i * self.aq.L / (n-1) for i in range(n)]
        grad = []
        if self.bc0.type==2 and self.bcL.type==1:
            for x in list(df.x):
                h, q, g = self.bc_t2_t1(
                    self.bcL.value['head'], self.bc0.value['flow'],
                    self.aq.L, self.aq.K, self.R, x
                    )
                if h <= self.aq.bot:
                    raise Exception('Aquifer is dry at x = ' + str(x))
                grad.append(g)
            df['h_grad'] = grad
        elif self.bc0.type==1 and self.bcL.type==1:
            for x in list(df.x):
                h, q, g = self.bc_t1_t1(
                    self.bc0.value['head'], self.bcL.value['head'],
                    self.aq.L, self.aq.K, self.R, x
                    )
                if h <= self.aq.bot:
                    raise Exception('Aquifer is dry at x = ' + str(x))
                grad.append(g)
            df['h_grad'] = grad
        # Plot results
        if plot:
            df.plot(x='x', y='h_grad', figsize=(10,3), marker='.', lw=3, alpha=0.5)
            plt.title('Head Gradient')
            plt.ylabel('Rate of head change')
            plt.legend(['head gradient'])
            plt.grid(True)
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
        return df
