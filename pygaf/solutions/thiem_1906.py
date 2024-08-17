class ThiemWell:
    """Thiem (1906) radial flow solution.

    The default ThiemWell object adopts the Aq2dConf aquifer class and
    SteadyWell class. A single method (.hd) is defined representing the
    head difference between two radii under a pumping stress; for example,
    representing the head difference between two observation boress at different
    radial distances from the pumping bore, or representing the head difference
    between the pumping bore at its well radius and an observation bore. Default
    radii are r1=0.1 and r2=1.

    Attributes:
        aq (obj) : Aq2dConf aquifer object.
        well (obj) : SteadyWell object.
    """
    from pygaf.aquifers import Aq2dConf
    from pygaf.wells import SteadyWell
    def __init__(self):
        self.aq = self.Aq2dConf()
        self.well = self.SteadyWell()
        self.well.q = -1000
        return
    
    def info(self):
        """Print the solution information."""
        print('METHOD REFERENCE')
        print('----------------')
        print('Thiem G. (1906) - Hydrologische Methoden.')
        print('\nConceptual Model:')
        print('- Infinite, confined, uniform and homogeneous aquifer.')
        print('- Steady state radial groundwater flow.')
        print('- Steady state and fully penetrating well.')
        print('- No groundwater recharge.')
        print()
    
    def hd(self, r1=0.1, r2=1):
        """Head difference between two radii."""
        from numpy import log, pi
        # Checks
        if r1 <= 0 or r2 <= 0:
            print('Error! Both radii must be greater than zero.')
            return
        Q = self.well.q
        T = self.aq.T
        hdiff = Q * log(r2/r1) / (2.0 * pi * T)
        print('Aquifer transmissivity:', self.aq.T)
        print('Pumping rate:', self.well.q)
        print('Pumping state:', self.well.state)
        print('Head difference between radii', r1, 'and', r2,':')
        return hdiff