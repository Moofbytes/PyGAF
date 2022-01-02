class Aquifer:
    """Parent aquifer class."""
    def __init__(self, K, B, bot):
        self.K = K
        self.B = B
        self.bot = bot
        return

    @property
    def T(self):
        """Aquifer transmissivity."""
        return self.K * self.B

    @property
    def top(self):
        """Aquifer top elevation."""
        return self.bot + self.B


class AqRadConf(Aquifer):
    """
    1D, radial confined aquifer.

    Arguments:
    ---------
    K : float
        Aquifer hydraulic conductivity [units: L/T] (default 1)
    Ss : float
        Aquifer specific storativity [units: 1/L] (default 1e-4)
    B : float
        Aquifer thickness [units: L] (default 10)
    bot : float
        Aquifer bottom elevation [units: L RL] (default 0)

    Properties:
    ----------
    T : float
        Aquifer transmissivity [units: L2/T]
    S : float
        Aquifer storage coefficient [units: 1]
    D : float
        Aquifer diffusivity [units: L2/T]
    top : float
        Aquifer top elevation [units: L RL]
    """
    is_infinite = True
    is_semifinite = False
    is_finite = False
    is_homogeneous = True
    is_heterogeneous = False
    is_radial = True
    is_1d = False
    is_2d = False
    is_confined = True
    is_leaky = False
    is_unconfined = False
    def __init__(self, K=1, Ss=1e-4, B=10, bot=0):
        super().__init__(K, B, bot)
        self.Ss = Ss

        for prop in [self.K, self.Ss, self.B]:
            if prop < 0:
                print('Error! all aquifer properties should be positive')
                return

        self.title = '1D, radial, confined homogeneous aquifer'
        return

    @property
    def S(self):
        """Aquifer storage coefficient."""
        return self.Ss * self.B

    @property
    def D(self):
        """Aquifer diffusivity."""
        return self.T / self.S

    def info(self):
        """Print the aquifer information."""
        print('AQUIFER INFORMATION')
        print('Type:', self.title)
        print('Hydraulic conductivity:', self.K, '[L/T]')
        print('Specific storativity:', self.Ss, '[1/L]')
        print('Aquifer thickness:', self.B, '[L]')
        print('Transmissivity:', self.T, '[L2/T]')
        print('Storage coefficient:', self.S, '[1]')
        print('Diffusivity:', self.D, '[L2/T]')
        print('Bottom elevation:', self.bot, '[RL]')
        print('Top elevation:', self.top, '[RL]')
        return

    def draw(self, dw=8):
        """
        Draw a picture of the aquifer as a Matplotlib axes.

        Arguments:
        ---------
        dw : float
            Width of aquifer drawing (default 8)
        """
        import matplotlib.pyplot as plt
        drawing_ratio = 3
        w, h = dw, dw/drawing_ratio
        plt.figure(figsize=(w, h))
        ax = plt.gca()
        ax.add_patch(plt.Rectangle((0, 0), width=w, height=h*0.1, facecolor='grey', edgecolor='black', hatch='///')) # bottom aquitard
        ax.add_patch(plt.Rectangle((0, h*0.1), width=w, height=h*0.8, hatch='...', facecolor='white')) # aquifer
        ax.add_patch(plt.Rectangle((0, h*0.9), width=w, height=h*0.1, facecolor='grey', edgecolor='black', hatch='///')) # top aquitard
        ax.add_line(plt.Line2D((w/2, w/2), (-h*0.05, h*1.1), color='black', linestyle='-.', linewidth=1)) # radial axis
        ax.arrow(w/2, h*1.1, w/10, 0, overhang=1, head_width=h/20, color='black', fill=False) # radius arrow
        ax.add_line(plt.Line2D((w, w*1.01), (h*0.1, h*0.1), color='black', lw=0.5)) # aquifer bottom tick
        ax.add_line(plt.Line2D((w, w*1.01), (h*0.9, h*0.9), color='black', lw=0.5)) # aquifer top tick
        ax.text(w*1.02, h*0.05, str(self.bot) +' RL', fontsize=12)
        ax.text(w*1.02, h*0.85, str(self.top) +' RL', fontsize=12)
        ax.text(w/2, h*1.2, 'r = 0', fontsize=12, horizontalalignment='center')
        ax.text(w*0.5, -h*0.2, self.title, fontsize=12, horizontalalignment='center', verticalalignment='top')
        plt.axis('scaled')
        plt.axis('off')
        plt.show()
        return


class AqRadUnconf(Aquifer):
    """
    1D, radial unconfined aquifer.

    Arguments:
    ---------
    K : float
        Aquifer hydraulic conductivity [units: L/T] (default 1)
    Sy : float
        Aquifer specific yield [units: 1] (default 0.1)
    B : float
        Aquifer thickness [units: L] (default 10)
    bot : float
        Aquifer bottom elevation [units: L RL] (default 0)

    Properties:
    ----------
    T : float
        Aquifer transmissivity [units: L2/T]
    S : float
        Aquifer storage coefficient [units: 1]
    swl : float
        Aquifer static water table elevation [units: L RL]
    top : float
        Aquifer top elevation [units: L RL]
    """
    is_infinite = True
    is_finite = False
    is_semifinite = False
    is_homogeneous = True
    is_heterogeneous = False
    is_radial = True
    is_1d = False
    is_2d = False
    is_confined = False
    is_leaky = False
    is_unconfined = True
    def __init__(self, K=1, Sy=0.1, B=10, bot=0):
        super().__init__(K, B, bot)
        self.Sy = Sy

        for prop in [self.K, self.Sy, self.B]:
            if prop < 0:
                print('Error! all aquifer properties should be positive')
                return

        self.title = '1D, radial, unconfined homogeneous aquifer'
        return

    @property
    def S(self):
        """Aquifer storage coefficient."""
        return self.Sy

    @property
    def swl(self):
        """Aquifer static water table elevation."""
        return self.bot + self.B

    def info(self):
        """Print the aquifer information."""
        print('AQUIFER INFORMATION')
        print('Type:', self.title)
        print('Hydraulic conductivity:', self.K, '[L/T]')
        print('Specific yield:', self.Sy, '[1]')
        print('Static saturated thickness:', self.B, '[L]')
        print('Static transmissivity:', self.T, '[L2/T]')
        print('Bottom elevation:', self.bot, '[RL]')
        print('Static water level:', self.swl, '[RL]')
        return

    def draw(self, dw=8):
        """
        Draw a picture of the aquifer as a Matplotlib axes.

        Arguments:
        ---------
        dw : float
            Width of aquifer drawing (default 8)
        """
        import matplotlib.pyplot as plt
        import numpy as np
        drawing_ratio = 3
        w, h = dw, dw/drawing_ratio
        plt.figure(figsize=(w, h))
        ax = plt.gca()
        ax.add_patch(plt.Rectangle((0, 0), width=w, height=h*0.1, facecolor='grey', edgecolor='black', hatch='///')) # bottom aquitard
        ax.add_patch(plt.Rectangle((0, h*0.1), width=w, height=h*0.8, hatch='...', facecolor='white')) # aquifer
        ax.add_line(plt.Line2D((0, w), (h*0.9, h*0.9), color='black', lw=0.5)) # water table
        ax.add_patch(plt.Polygon(np.array([[0.95*w/3, h], [w/3, h*0.9], [1.05*w/3, h]]), closed=True, edgecolor='black', facecolor='white'))
        ax.add_line(plt.Line2D((w/2, w/2), (-h*0.05, h), color='black', linestyle='-.', linewidth=1)) # radial axis
        ax.arrow(w/2, h, w/10, 0, overhang=1, head_width=h/20, color='black', fill=False) # radius arrow
        ax.add_line(plt.Line2D((w, w*1.01), (h*0.1, h*0.1), color='black', lw=0.5)) # aquifer bottom tick
        ax.add_line(plt.Line2D((w, w*1.01), (h*0.9, h*0.9), color='black', lw=0.5)) # aquifer top tick
        ax.text(w*1.02, h*0.05, str(self.bot) +' RL', fontsize=12)
        ax.text(w*1.02, h*0.85, str(self.swl) +' RL', fontsize=12)
        ax.text(w/2, h*1.1, 'r = 0', fontsize=12, horizontalalignment='center')
        ax.text(w*0.5, -h*0.2, self.title, fontsize=12, horizontalalignment='center', verticalalignment='top')
        plt.axis('scaled')
        plt.axis('off')
        plt.show()
        return


class Aq1dFiniteConf(Aquifer):
    """
    1D, finite confined aquifer.

    Arguments:
    ---------
    K : float
        Aquifer hydraulic conductivity [units: L/T] (default 1)
    Ss : float
        Aquifer specific storativity [units: 1/L] (default 1e-4)
    B : float
        Aquifer thickness [units: L] (default 10)
    L : float
        Aquifer length [units: L] (default 1000)
    bot : float
        Aquifer bottom elevation [units: L RL] (default 0)

    Properties:
    ----------
    T : float
        Aquifer transmissivity [units: L2/T]
    S : float
        Aquifer storage coefficient [units: 1]
    D : float
        Aquifer diffusivity [units: L2/T]
    top : float
        Aquifer top elevation [units: L RL]
    """
    is_infinite = False
    is_semifinite = False
    is_finite = True
    is_homogeneous = True
    is_heterogeneous = False
    is_radial = False
    is_1d = True
    is_2d = False
    is_confined = True
    is_leaky = False
    is_unconfined = False
    def __init__(self, K=1, Ss=1e-4, B=10, L=1000, bot=0):
        super().__init__(K, B, bot)
        self.Ss = Ss
        self.L = L

        for prop in [K, Ss, B, L]:
            if prop < 0:
                print('Error! all aquifer parameters should be positive.')
                return

        self.title = '1D, finite, confined homogeneous aquifer'
        return

    @property
    def S(self):
        """Aquifer storage coefficient."""
        return self.Ss * self.B

    @property
    def D(self):
        """Aquifer diffusivity."""
        return self.T / self.S

    def info(self):
        """Print the aquifer information."""
        print('AQUIFER INFORMATION')
        print('Type:', self.title)
        print('Hydraulic conductivity:', self.K, '[L/T]')
        print('Specific storativity:', self.Ss, '[1/L]')
        print('Thickness:', self.B, '[L]')
        print('Length:', self.L, '[L]')
        print('Transmissivity:', self.T, '[L2/T]')
        print('Storage coefficient:', self.S, '[1]')
        print('Diffusivity:', self.D, '[L2/T]')
        print('Bottom elevation:', self.bot, '[RL]')
        print('Top elevation:', self.top, '[RL]')
        return

    def draw(self, dw=8):
        """
        Draw a picture of the aquifer as a Matplotlib axes.

        Arguments:
        ---------
        dw : float
            Width of aquifer drawing (default 8)
        """
        import matplotlib.pyplot as plt
        drawing_ratio = 3
        w, h = dw, dw/drawing_ratio
        plt.figure(figsize=(w, h))
        ax = plt.gca()
        ax.add_patch(plt.Rectangle((0, 0), width=w, height=h*0.1, facecolor='grey', edgecolor='black', hatch='///')) # bottom aquitard
        ax.add_patch(plt.Rectangle((0, h*0.1), width=w, height=h*0.8, hatch='...', facecolor='white', edgecolor='black')) # aquifer
        ax.add_patch(plt.Rectangle((0, h*0.9), width=w, height=h*0.1, facecolor='grey', edgecolor='black', hatch='///')) # top aquitard
        ax.add_line(plt.Line2D((0, 0), (-h*0.05, h*1.05), color='black', linestyle='-.', linewidth=1)) # x axis
        ax.add_line(plt.Line2D((w, w*1.01), (h*0.1, h*0.1), color='black', lw=0.5)) # aquifer bottom tick
        ax.add_line(plt.Line2D((w, w*1.01), (h*0.9, h*0.9), color='black', lw=0.5)) # aquifer top tick
        ax.text(w*1.02, h*0.05, str(self.bot) +' RL', fontsize=12)
        ax.text(w*1.02, h*0.85, str(self.top) +' RL', fontsize=12)
        ax.text(0, h*1.1, 'x = 0', fontsize=12, horizontalalignment='center')
        ax.text(w, h*1.1, 'x = ' + str(self.L), fontsize=12, horizontalalignment='center')
        ax.text(w*0.5, -h*0.2, self.title, fontsize=12, horizontalalignment='center', verticalalignment='top')
        plt.axis('scaled')
        plt.axis('off')
        plt.show()
        return

    @property
    def ve(self, h=3, w=10):
        """Vertical exaggeration of the aquifer drawing."""
        return self.L * h / (self.B * w)


class Aq1dFiniteUnconf(Aquifer):
    """
    1D, finite unconfined aquifer.

    Arguments:
    ---------
    K : float
        Aquifer hydraulic conductivity [units: L/T] (default 1)
    Sy : float
        Aquifer specific yield [units: 1] (default 0.1)
    B : float
        Aquifer thickness [units: L] (default 10)
    L : float
        Aquifer length [units: L] (default 1000)
    bot : float
        Aquifer bottom elevation [units: L RL] (default 0)

    Properties:
    ----------
    T : float
        Aquifer transmissivity [units: L2/T]
    S : float
        Aquifer storage coefficient [units: 1]
    swl : float
        Aquifer static water table elevation [units: L RL]
    top : float
        Aquifer top elevation [units: L RL]
    """
    is_infinite = False
    is_semifinite = False
    is_finite = True
    is_homogeneous = True
    is_heterogeneous = False
    is_radial = False
    is_1d = True
    is_2d = False
    is_confined = False
    is_leaky = False
    is_unconfined = True
    def __init__(self, K=1, Sy=0.1, B=10, L=1000, bot=0):
        super().__init__(K, B, bot)
        self.Sy = Sy
        self.L = L

        for prop in [K, Sy, B, L]:
            if prop < 0:
                print('Error! all aquifer parameters should be positive.')
                return

        self.title = '1D, finite, unconfined homogeneous aquifer'
        return

    @property
    def T(self):
        """Aquifer transmissivity."""
        return self.K * self.B

    @property
    def S(self):
        """Aquifer storage coefficient."""
        return self.Sy

    @property
    def swl(self):
        """Aquifer static water table elevation."""
        return self.bot + self.B

    def info(self):
        """Print the aquifer information."""
        print('AQUIFER INFORMATION')
        print('Type:', self.title)
        print('Hydraulic conductivity:', self.K, '[L/T]')
        print('Specific yield:', self.Sy, '[1]')
        print('Static saturated thickness:', self.B, '[L]')
        print('Length:', self.L, '[L]')
        print('Static transmissivity:', self.T, '[L2/T]')
        print('Bottom elevation:', self.bot, '[RL]')
        print('Static water table:', self.swl, '[RL]')
        return

    def draw(self, dw=8):
        """
        Draw a picture of the aquifer as a Matplotlib axes.

        Arguments:
        ---------
        dw : float
            Width of aquifer drawing (default 8)
        """
        import matplotlib.pyplot as plt
        import numpy as np
        drawing_ratio = 3
        w, h = dw, dw/drawing_ratio
        plt.figure(figsize=(w, h))
        ax = plt.gca()
        ax.add_patch(plt.Rectangle((0, 0), width=w, height=h*0.1, facecolor='grey', edgecolor='black', hatch='///')) # bottom aquitard
        ax.add_patch(plt.Rectangle((0, h*0.1), width=w, height=h*0.8, hatch='...', edgecolor='black', facecolor='white')) # aquifer
        ax.add_patch(plt.Polygon(np.array([[0.95*w/3, h], [w/3, h*0.9], [1.05*w/3, h]]), closed=True, edgecolor='black', facecolor='white'))
        ax.add_line(plt.Line2D((0, 0), (-h*0.05, h), color='black', linestyle='-.', linewidth=1)) # x axis
        ax.add_line(plt.Line2D((w, w*1.01), (h*0.1, h*0.1), color='black', lw=0.5)) # aquifer bottom tick
        ax.add_line(plt.Line2D((w, w*1.01), (h*0.9, h*0.9), color='black', lw=0.5)) # aquifer top tick
        ax.text(w*1.02, h*0.05, str(self.bot) +' RL', fontsize=12)
        ax.text(w*1.02, h*0.85, str(self.swl) +' RL', fontsize=12)
        ax.text(0, h*1.1, 'x = 0', fontsize=12, horizontalalignment='center')
        ax.text(w, h*1.1, 'x = ' + str(self.L), fontsize=12, horizontalalignment='center')
        ax.text(w*0.5, -h*0.2, self.title, fontsize=12, horizontalalignment='center', verticalalignment='top')
        plt.axis('scaled')
        plt.axis('off')
        plt.show()
        return

    @property
    def ve(self, h=3, w=10):
        """Vertical exaggeration of the aquifer drawing."""
        return self.L * h / (self.B * w)


class Aq1dSemifiniteConf(Aquifer):
    """
    1D, semi-infinite confined aquifer.

    Arguments:
    ---------
    K : float
        Aquifer hydraulic conductivity [units: L/T] (default 1)
    Ss : float
        Aquifer specific storativity [units: 1/L] (default 1e-4)
    B : float
        Aquifer thickness [units: L] (default 10)
    bot : float
        Aquifer bottom elevation [units: L RL] (default 0)

    Properties:
    ----------
    T : float
        Aquifer transmissivity [units: L2/T]
    S : float
        Aquifer storage coefficient [units: 1]
    D : float
        Aquifer diffusivity [units: L2/T]
    top : float
        Aquifer top elevation [units: L RL]
    """
    is_infinite = False
    is_semifinite = True
    is_finite = False
    is_homogeneous = True
    is_heterogeneous = False
    is_radial = False
    is_1d = True
    is_2d = False
    is_confined = True
    is_leaky = False
    is_unconfined = False
    def __init__(self, K=1, Ss=1e-4, B=10, bot=0):
        super().__init__(K, B, bot)
        self.Ss = Ss

        for prop in [K, Ss, B]:
            if prop < 0:
                print('Error! all aquifer parameters should be positive.')
                return

        self.title = '1D, semi-infinite, confined homogeneous aquifer'
        return

    @property
    def S(self):
        """Aquifer storage coefficient."""
        return self.Ss * self.B

    @property
    def D(self):
        """Aquifer diffusivity."""
        return self.T / self.S

    def info(self):
        """Print the aquifer information."""
        print('AQUIFER INFORMATION')
        print('Type:', self.title)
        print('Hydraulic conductivity:', self.K, '[L/T]')
        print('Specific storativity:', self.Ss, '[1/L]')
        print('Thickness:', self.B, '[L]')
        print('Transmissivity:', self.T, '[L2/T]')
        print('Storage coefficient:', self.S, '[1]')
        print('Diffusivity:', self.D, '[L2/T]')
        print('Bottom elevation:', self.bot, '[RL]')
        print('Top elevation:', self.top, '[RL]')
        return

    def draw(self, dw=8):
        """
        Draw a picture of the aquifer as a Matplotlib axes.

        Arguments:
        ---------
        dw : float
            Width of aquifer drawing (default 8)
        """
        import matplotlib.pyplot as plt
        drawing_ratio = 3
        w, h = dw, dw/drawing_ratio
        plt.figure(figsize=(w, h))
        ax = plt.gca()
        ax.add_patch(plt.Rectangle((0, 0), width=w, height=h*0.1, facecolor='grey', edgecolor='black', hatch='///')) # bottom aquitard
        ax.add_patch(plt.Rectangle((0, h*0.1), width=w, height=h*0.8, hatch='...', facecolor='white')) # aquifer
        ax.add_line(plt.Line2D((0, 0), (0, h), color='black', lw=0.5)) # aquifer boundary
        ax.add_patch(plt.Rectangle((0, h*0.9), width=w, height=h*0.1, facecolor='grey', edgecolor='black', hatch='///')) # top aquitard
        ax.add_line(plt.Line2D((0, 0), (-h*0.05, h*1.1), color='black', linestyle='-.', linewidth=1)) # x axis
        ax.arrow(0, h*1.1, w/10, 0, overhang=1, head_width=h/20, color='black', fill=False) # x arrow
        ax.add_line(plt.Line2D((w, w*1.01), (h*0.1, h*0.1), color='black', lw=0.5)) # aquifer bottom tick
        ax.add_line(plt.Line2D((w, w*1.01), (h*0.9, h*0.9), color='black', lw=0.5)) # aquifer top tick
        ax.text(w*1.02, h*0.05, str(self.bot) +' RL', fontsize=12)
        ax.text(w*1.02, h*0.85, str(self.top) +' RL', fontsize=12)
        ax.text(0, h*1.2, 'x = 0', fontsize=12, horizontalalignment='center')
        ax.text(w*0.5, -h*0.2, self.title, fontsize=12, horizontalalignment='center', verticalalignment='top')
        plt.axis('scaled')
        plt.axis('off')
        plt.show()
        return


class Aq1dSemifiniteUnconf(Aquifer):
    """
    1D, semi-infinite unconfined aquifer.

    Arguments:
    ---------
    K : float
        Aquifer hydraulic conductivity [units: L/T] (default 1)
    Sy : float
        Aquifer specific yield [units: 1] (default 0.1)
    B : float
        Aquifer thickness [units: L] (default 10)
    bot : float
        Aquifer bottom elevation [units: L RL] (default 0)

    Properties:
    ----------
    T : float
        Aquifer transmissivity [units: L2/T]
    S : float
        Aquifer storage coefficient [units: 1]
    swl : float
        Aquifer static water table elevation [units: L RL]
    top : float
        Aquifer top elevation [units: L RL]
    """
    is_infinite = False
    is_semifinite = True
    is_finite = False
    is_homogeneous = True
    is_heterogeneous = False
    is_radial = False
    is_1d = True
    is_2d = False
    is_confined = False
    is_leaky = False
    is_unconfined = True
    def __init__(self, K=1, Sy=0.1, B=10, bot=0):
        super().__init__(K, B, bot)
        self.Sy = Sy

        for prop in [K, Sy, B]:
            if prop < 0:
                print('Error! all aquifer parameters should be positive.')
                return

        self.title = '1D, semi-infinite, unconfined homogeneous aquifer'
        return

    @property
    def T(self):
        """Aquifer transmissivity."""
        return self.K * self.B

    @property
    def S(self):
        """Aquifer storage coefficient."""
        return self.Sy

    @property
    def swl(self):
        """Aquifer static water table elevation."""
        return self.bot + self.B

    def info(self):
        """Print the aquifer information."""
        print('AQUIFER INFORMATION')
        print('Type:', self.title)
        print('Hydraulic conductivity:', self.K, '[L/T]')
        print('Specific yield:', self.Sy, '[1]')
        print('Static saturated thickness:', self.B, '[L]')
        print('Static transmissivity:', self.T, '[L2/T]')
        print('Bottom elevation:', self.bot, '[RL]')
        print('Static water table:', self.swl, '[RL]')
        return

    def draw(self, dw=8):
        """
        Draw a picture of the aquifer as a Matplotlib axes.

        Arguments:
        ---------
        dw : float
            Width of aquifer drawing (default 8)
        """
        import matplotlib.pyplot as plt
        import numpy as np
        drawing_ratio = 3
        w, h = dw, dw/drawing_ratio
        plt.figure(figsize=(w, h))
        ax = plt.gca()
        ax.add_patch(plt.Rectangle((0, 0), width=w, height=h*0.1, facecolor='grey', edgecolor='black', hatch='///')) # bottom aqitard
        ax.add_patch(plt.Rectangle((0, h*0.1), width=w, height=h*0.8, hatch='...', edgecolor='black', facecolor='white')) # aquifer
        ax.add_line(plt.Line2D((0, w), (h*0.9, h*0.9), color='black', lw=0.5)) # water table
        ax.add_line(plt.Line2D((0, 0), (0, h*0.9), color='black', lw=0.5)) # aquifer boundary
        ax.add_patch(plt.Polygon(np.array([[0.95*w/3, h], [w/3, h*0.9], [1.05*w/3, h]]), closed=True, edgecolor='black', facecolor='white'))
        ax.add_line(plt.Line2D((0, 0), (-h*0.05, h), color='black', linestyle='-.', linewidth=1)) # x axis
        ax.arrow(0, h, w/10, 0, width=0.01, overhang=1, head_width=h/20, color='black', fill=False) # x arrow
        ax.add_line(plt.Line2D((w, w*1.01), (h*0.1, h*0.1), color='black', lw=0.5)) # aquifer bottom tick
        ax.add_line(plt.Line2D((w, w*1.01), (h*0.9, h*0.9), color='black', lw=0.5)) # aquifer bottom tick
        ax.text(w*1.02, h*0.05, str(self.bot) +' RL', fontsize=12)
        ax.text(w*1.02, h*0.85, str(self.swl) +' RL', fontsize=12)
        ax.text(0, h*1.1, 'x = 0', fontsize=12, horizontalalignment='center')
        ax.text(w*0.5, -h*0.2, self.title, fontsize=12, horizontalalignment='center', verticalalignment='top')
        plt.axis('scaled')
        plt.axis('off')
        plt.show()
        return
