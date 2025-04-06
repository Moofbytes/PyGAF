class GloverSWI:
    """Glover (1959) abrupt saltwater interface solution.

    Attributes:
        rho_fresh (float) : Density of freshwater (units kg/kL, default 1000).
        rho_salt (float) : Density of saltwater (units kg/kL, default 1023).
        K (float) : Aquifer hydraulic conductivity (units L/T, default 1.0).
        L (float) : Length of aquifer for evaluating the solution (units L, default 100).
        Q (float) : Groundwater flow toward the sea (units L3/T per L of shoreline, default 0.2).
        n (int) : Number of x values at which to evaluate the interface solution (default 25).

    """
    from pygaf.aquifers import Aq1dFiniteUnconf
    def __init__(self, rho_fresh=1000.0, rho_salt=1023.0, K=1.0, L=100.0, Q=0.2, n=25):
        self.rho_fresh = rho_fresh
        self.rho_salt = rho_salt
        self.K = K
        self.L = L
        self.Q = Q
        self.n = n
        return
    
    @property
    def rho_fresh(self):
        """float : Freshwater density (units kg/kL, default 1000).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._rho_fresh

    @rho_fresh.setter
    def rho_fresh(self, v):
        if not (v > 0):
            raise Exception('Freshwater density must be positive.')
        self._rho_fresh = v
        
    @property
    def rho_salt(self):
        """float : Saltwater density (units kg/kL, default 1023).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._rho_salt

    @rho_salt.setter
    def rho_salt(self, v):
        if not (v > 0):
            raise Exception('Saltwater density must be positive.')
        self._rho_salt = v
        
    @property
    def K(self):
        """float : Aquifer hydraulic conductivity (units L/T, default 1.0).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._K

    @K.setter
    def K(self, v):
        if not (v > 0):
            raise Exception('Aquifer hydraulic conductivity must be positive.')
        self._K = v
    
    @property
    def L(self):
        """float : Length of aquifer for evaluating the solution (units L, default 100).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._L

    @L.setter
    def L(self, v):
        if not (v > 0):
            raise Exception('Aquifer length must be positive.')
        self._L = v
    
    @property
    def Q(self):
        """float : Groundwater flow toward the sea (units L3/T per L of shoreline, default 0.01).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._Q

    @Q.setter
    def Q(self, v):
        if not (v > 0):
            raise Exception('Aquifer flow toward the sea must be positive.')
        self._Q = v
    
    @property
    def n(self):
        """int : Number of x values for evaluating the solution (default 50).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._n

    @n.setter
    def n(self, v):
        if not (v > 0):
            raise Exception('Number of x values must be positive.')
        self._n = v
        
    @property
    def alpha_bar(self):
        """float : Density difference ratio."""
        if self.rho_fresh >= self.rho_salt:
            raise Exception('rho_salt must be greater than rho_fresh.')
        return (self.rho_salt - self.rho_fresh)/self.rho_fresh
    
    @property
    def gap(self):
        """float : Length of freshwater seepage face."""
        return self.Q/(2*self.alpha_bar*self.K)
    
    def info(self):
        """Print the solution information."""
        print('METHOD REFERENCE')
        print('----------------')
        print('Glover (1959) - The Pattern of Fresh-water Flow in a Coastal Aquifer.')
        print('\nConceptual Model:')
        print('- Immiscible fluids with abrupt interface.')
        print('- Static saltwater.')
        print('- Hydrostatic pressure.')
        print('- Steady state flow.')
        print('- Homogeneous and isotropic aquifer.')
        print('- Seepage face between shoreline and interface.')
        print()
    
    def swi(self, plot=True, csv='', xlsx=''):
        """Glover (1959) saltwater interface.
        
        Args:
            plot (bool) : Display a plot of the results (default True).
            csv (str) : Filepath for export of results to csv file; results
                are exported if the string is not empty (default '').
            xlsx (str) : Filepath for export of result to xlsx file; results
                are exported if the string is not empty (default '').

        Returns:
            Pandas dataframe containing head and swi values.
            
        """
        import matplotlib.pyplot as plt
        import pandas
        from numpy import sqrt
        df = pandas.DataFrame()
        df['x'] = [-self.gap + (i*(self.gap+self.L) / (self.n-1)) for i in range(self.n)]
        wt_elev = []
        swi_elev = []
        for x in df.x:
            if x > 0:
                w = sqrt(2*self.alpha_bar*self.Q*x/self.K)
            else:
                w = 0.0
            if (2*self.Q*x/(self.K*self.alpha_bar) + (self.Q/(self.K*self.alpha_bar))**2) > 0:
                s = -sqrt(2*self.Q*x/(self.K*self.alpha_bar) + (self.Q/(self.K*self.alpha_bar))**2)
            else:
                s = 0.0
            wt_elev.append(w)
            swi_elev.append(s)
        df['h'] = wt_elev
        df['swi'] = swi_elev
        print('Freshwater density:', self.rho_fresh)
        print('Saltwater density:', self.rho_salt)
        print('Density ratio:', self.alpha_bar)
        print('Aquifer hydraulic conductivity:', self.K)
        print('Freshwater discharge:', self.Q)
        print('Length of freshwater seepage face:', round(self.gap,2))
        # Plot results
        if plot:
            df.plot(x='x', y='h', figsize=(10,3), marker='.', lw=3, alpha=0.5)
            plt.plot(df.x, df.swi, '.-', c='red', lw=3, alpha=0.5)
            plt.plot(0.0, 0.0, '^', c='black')
            plt.title(
                'Glover (1959) Saltwater Interface\n' +
                '(K = ' + str(round(self.K, 4)) + ', ' +
                'Q = ' + str(round(self.Q, 4)) + ', ' +
                'density ratio = ' + str(round(self.alpha_bar, 4)) + ')'
            )
            plt.xlabel('Distance from shoreline')
            plt.ylabel('Elevation')
            plt.axis([None, None, None, None])
            plt.legend(['aquifer head', 'saltwater interface', 'shoreline'])
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
    
