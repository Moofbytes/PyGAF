class Aquifer:
    """Aquifer parent class.

    The Aquifer parent class defines attributes and properties common to all
    aquifers. They include the aquifer transmissivity (defined by hydraulic
    conductivity and saturated thickness), the aquifer elevation datum and an
    aquifer name label for use in figures.

    Attributes:
        K (float) : Aquifer hydraulic conductivity (units L/T, default 1.0).
        B (float) : Aquifer thickness (units L, default 10.0).
        bot (float) : Aquifer bottom elevation (units L reduced level,
            default 0.0).
        name (str) : Aquifer label (default 'Unnamed Aquifer').

    """
    def __init__(self, K=1, B=10, bot=0, name='Unnamed Aquifer'):
        self.K = K
        self.B = B
        self.bot = bot
        self.name = name
        return

    @property
    def T(self):
        """float : aquifer transmissivity (units L2/T, default 10.0)."""
        return self.K * self.B

    @property
    def top(self):
        """float : aquifer top elevation (unts L, default 10.0)."""
        return self.bot + self.B


class Aq2dConf(Aquifer):
    """2D confined aquifer class.

    A subclass of the Aquifer class defining a horizontal, 2D confined aquifer
    with infinite lateral extent and confined storage.

    The default Aq2dConf object has hydraulic conductivity K=1, specific
    storativity Ss=0.0001, aquifer saturated thickness B=10 and aquifer bottom
    (datum) elevation bot=0. Exceptions will occur if invalid values are
    provided for K, Ss or B.

    The .info and .draw methods display the aquifer information and diagram.

    Attributes:
        Ss (float) : aquifer specific storativity (units 1/L, default 1.0e-4).

    """
    is_infinite = True
    is_semifinite = False
    is_finite = False
    is_homogeneous = True
    is_heterogeneous = False
    is_1d = False
    is_2d = True
    is_confined = True
    is_leaky = False
    is_unconfined = False
    def __init__(self, K=1, Ss=1e-4, B=10, bot=0, name='Unnamed Aquifer'):
        super().__init__(K, B, bot, name)
        self.Ss = Ss
        self.type = '2D, confined homogeneous aquifer'
        return

    @property
    def K(self):
        """float : aquifer hydraulic conductivity (units L/T, default 1.0).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._K

    @K.setter
    def K(self, v):
        if not (v > 0):
            raise Exception('Hydraulic conductivity (K) must be positive.')
        self._K = v

    @property
    def Ss(self):
        """float : aquifer specific storativity (units 1/L, default 1.0e-4).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._Ss

    @Ss.setter
    def Ss(self, v):
        if not (v > 0):
            raise Exception('Specific storage (Ss) must be positive.')
        self._Ss = v

    @property
    def B(self):
        """float : aquifer thickness (units L, default 10.0).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._B

    @B.setter
    def B(self, v):
        if not (v > 0):
            raise Exception('Aquifer thickness (B) must be positive.')
        self._B = v

    @property
    def S(self):
        """float : aquifer storage coefficient (units 1, default 1.0e-3)."""
        return self.Ss * self.B

    @property
    def D(self):
        """float : aquifer diffusivity (units L2/T, default 1.0e+4)."""
        return self.T / self.S

    def info(self):
        """Print the aquifer information."""
        print('AQUIFER INFORMATION')
        print('-------------------')
        print('Type:', self.type)
        print('Name:', self.name)
        print('Hydraulic conductivity:', self.K, '[L/T]')
        print('Specific storativity:', self.Ss, '[1/L]')
        print('Aquifer thickness:', self.B, '[L]')
        print('Transmissivity:', self.T, '[L2/T]')
        print('Storage coefficient:', self.S, '[1]')
        print('Diffusivity:', self.D, '[L2/T]')
        print('Bottom elevation:', self.bot, '[RL]')
        print('Top elevation:', self.top, '[RL]')
        print()
        return

    def draw(self, dw=6):
        """Display a drawing of the aquifer.

        Args:
            dw (float) : Width of figure (default 6.0).

        """
        import matplotlib.pyplot as plt
        drawing_ratio = 3
        w, h = dw, dw/drawing_ratio
        fig = plt.figure(figsize=(w, h))
        fig.suptitle(self.name, fontsize=14, fontweight=530)
        ax = plt.gca()
        ax.add_patch(
            plt.Rectangle((0, 0), width=w, height=h*0.1, facecolor='grey',
            edgecolor='black', hatch='///')
        ) # bottom aquitard
        ax.add_patch(
            plt.Rectangle((0, h*0.1), width=w, height=h*0.8, hatch='...',
            facecolor='white')
        ) # aquifer
        ax.add_patch(
            plt.Rectangle((0, h*0.9), width=w, height=h*0.1, facecolor='grey',
            edgecolor='black', hatch='///')
        ) # top aquitard
        ax.add_line(
            plt.Line2D((w, w*1.01), (h*0.1, h*0.1), color='black', lw=0.5)
        ) # aquifer bottom tick
        ax.add_line(
            plt.Line2D((w, w*1.01), (h*0.9, h*0.9), color='black', lw=0.5)
        ) # aquifer top tick
        ax.text(w*1.02, h*0.05, str(self.bot) +' RL', fontsize=12)
        ax.text(w*1.02, h*0.85, str(self.top) +' RL', fontsize=12)
        plt.axis('scaled')
        plt.axis('off')
        plt.tight_layout()
        plt.show()
        plt.close()
        return


class Aq2dUnconf(Aquifer):
    """2D unconfined aquifer subclass.

    A subclass of the Aquifer class defining a horizontal, 2D unconfined aquifer
    with infinite lateral extent and unconfined storage.

    The default Aq2dUnconf object has hydraulic conductivity K=1, specific yield
    Sy=0.1, static saturated thickness B=10 and aquifer bottom (datum) elevation
    bot=0. Exceptions will occur if invalid values are provided for K, Sy or B.

    The .info and .draw methods display the aquifer information and diagram.

    Attributes:
        Sy (float) : aquifer specific yield (units 1, default 0.1).

    """
    is_infinite = True
    is_finite = False
    is_semifinite = False
    is_homogeneous = True
    is_heterogeneous = False
    is_1d = False
    is_2d = True
    is_confined = False
    is_leaky = False
    is_unconfined = True
    def __init__(self, K=1, Sy=0.1, B=10, bot=0, name='Unnamed Aquifer'):
        super().__init__(K, B, bot, name)
        self.Sy = Sy
        self.type = '2D, unconfined homogeneous aquifer'
        return

    @property
    def K(self):
        """float : aquifer hydraulic conductivity (units L/T, default 1.0).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._K

    @K.setter
    def K(self, v):
        if not (v > 0):
            raise Exception('Hydraulic conductivity (K) must be positive.')
        self._K = v

    @property
    def Sy(self):
        """float : aquifer specific yield (units 1, default 0.1).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._Sy

    @Sy.setter
    def Sy(self, v):
        if not (v > 0 and v < 1):
            raise Exception(
            'Specific yield (Sy) must be positive and less than 1.'
            )
        self._Sy = v

    @property
    def B(self):
        """float : aquifer thickness (units L, default 10.0).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._B

    @B.setter
    def B(self, v):
        if not (v > 0):
            raise Exception('Aquifer thickness (B) must be positive.')
        self._B = v

    @property
    def S(self):
        """float : aquifer storage coefficient (units 1, default 0.1)."""
        return self.Sy

    @property
    def swl(self):
        """float : aquifer static water table elevation (units L reduced level,
        default 10.0).
        """
        return self.bot + self.B

    def info(self):
        """Print the aquifer information."""
        print('AQUIFER INFORMATION')
        print('-------------------')
        print('Type:', self.type)
        print('Name:', self.name)
        print('Hydraulic conductivity:', self.K, '[L/T]')
        print('Specific yield:', self.Sy, '[1]')
        print('Static saturated thickness:', self.B, '[L]')
        print('Static transmissivity:', self.T, '[L2/T]')
        print('Bottom elevation:', self.bot, '[RL]')
        print('Static water level:', self.swl, '[RL]')
        print()
        return

    def draw(self, dw=6):
        """Display a drawing of the aquifer.

        Args:
            dw (float) : width of figure (default 6.0).

        """
        import matplotlib.pyplot as plt
        import numpy as np
        drawing_ratio = 3
        w, h = dw, dw/drawing_ratio
        fig = plt.figure(figsize=(w, h))
        fig.suptitle(self.name, fontsize=14, fontweight=530)
        ax = plt.gca()
        ax.add_patch(
            plt.Rectangle((0, 0), width=w, height=h*0.1, facecolor='grey',
            edgecolor='black', hatch='///')
        ) # bottom aquitard
        ax.add_patch(
            plt.Rectangle((0, h*0.1), width=w, height=h*0.8, hatch='...',
            facecolor='white')
        ) # aquifer
        ax.add_line(
            plt.Line2D((0, w), (h*0.9, h*0.9), color='black', lw=0.5)
        ) # water table
        ax.add_patch(
            plt.Polygon(np.array([[0.95*w/3, h], [w/3, h*0.9], [1.05*w/3, h]]),
            closed=True, edgecolor='black', facecolor='white')
        )
        ax.add_line(
            plt.Line2D((w, w*1.01), (h*0.1, h*0.1), color='black', lw=0.5)
        ) # aquifer bottom tick
        ax.add_line(
            plt.Line2D((w, w*1.01), (h*0.9, h*0.9), color='black', lw=0.5)
        ) # aquifer top tick
        ax.text(w*1.02, h*0.05, str(self.bot) +' RL', fontsize=12)
        ax.text(w*1.02, h*0.85, str(self.swl) +' RL', fontsize=12)
        plt.axis('scaled')
        plt.axis('off')
        plt.tight_layout()
        plt.show()
        plt.close()
        return


class Aq1dFiniteConf(Aquifer):
    """1D, finite confined aquifer subclass.

    A subclass of the Aquifer class defining a horizontal, 1D confined aquifer
    with finite lateral extent and confined storage.

    The default Aq1dFiniteConf object has hydraulic conductivity K=1, specific
    storativity Ss=0.0001, aquifer saturated thickness B=10, aquifer length
    L=1000 and aquifer bottom (datum) elevation bot=0. Exceptions will occur if
    invalid values are provided for K, Ss, B or L.

    The .info and .draw methods display the aquifer information and diagram.

    Attributes:
        Ss (float) : aquifer specific storativity (units 1/L, default 1.0e-4).
        L (float) : aquifer length (units L, default 1000.0).

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
    def __init__(self, K=1, Ss=1e-4, B=10, L=1000, bot=0,
    name='Unnamed Aquifer'):
        super().__init__(K, B, bot, name)
        self.Ss = Ss
        self.L = L
        self.type = '1D, finite, confined homogeneous aquifer'
        return

    @property
    def K(self):
        """float : aquifer hydraulic conductivity (units L/T, default 1.0).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._K

    @K.setter
    def K(self, v):
        if not (v > 0):
            raise Exception('Hydraulic conductivity (K) must be positive.')
        self._K = v

    @property
    def Ss(self):
        """float : aquifer specific storativity (units 1/L, default 1.0e-4).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._Ss

    @Ss.setter
    def Ss(self, v):
        if not (v > 0):
            raise Exception('Specific storage (Ss) must be positive.')
        self._Ss = v

    @property
    def B(self):
        """float : aquifer thickness (units L, default 10.0).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._B

    @B.setter
    def B(self, v):
        if not (v > 0):
            raise Exception('Aquifer thickness (B) must be positive.')
        self._B = v

    @property
    def L(self):
        """float : aquifer length (units L, default 1000.0).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._L

    @L.setter
    def L(self, v):
        if not (v > 0):
            raise Exception('Aquifer length (L) must be positive.')
        self._L = v

    @property
    def S(self):
        """float : aquifer storage coefficient (units 1, default 1.0e-3)."""
        return self.Ss * self.B

    @property
    def D(self):
        """float : aquifer diffusivity (units L2/T, default 1.0e+4)."""
        return self.T / self.S

    def info(self):
        """Print the aquifer information."""
        print('AQUIFER INFORMATION')
        print('-------------------')
        print('Type:', self.type)
        print('Name:', self.name)
        print('Hydraulic conductivity:', self.K, '[L/T]')
        print('Specific storativity:', self.Ss, '[1/L]')
        print('Thickness:', self.B, '[L]')
        print('Length:', self.L, '[L]')
        print('Transmissivity:', self.T, '[L2/T]')
        print('Storage coefficient:', self.S, '[1]')
        print('Diffusivity:', self.D, '[L2/T]')
        print('Bottom elevation:', self.bot, '[RL]')
        print('Top elevation:', self.top, '[RL]')
        print()
        return

    def draw(self, dw=6):
        """Display a drawing of the aquifer.

        Args:
            dw (float) : width of figure (default 6.0).

        """
        import matplotlib.pyplot as plt
        drawing_ratio = 3
        dw = dw * 1.13
        w, h = dw, dw/drawing_ratio
        fig = plt.figure(figsize=(w, h))
        fig.suptitle(self.name, fontsize=14, fontweight=530)
        ax = plt.gca()
        ax.add_patch(plt.Rectangle(
            (0, 0), width=w, height=h*0.1, facecolor='grey', edgecolor='black',
            hatch='///')
        ) # bottom aquitard
        ax.add_patch(
            plt.Rectangle((0, h*0.1), width=w, height=h*0.8, hatch='...',
            facecolor='white', edgecolor='black')
        ) # aquifer
        ax.add_patch(
            plt.Rectangle((0, h*0.9), width=w, height=h*0.1, facecolor='grey',
            edgecolor='black', hatch='///')
        ) # top aquitard
        ax.add_line(
            plt.Line2D((0, 0), (-h*0.05, h*1.05), color='black', linestyle='-.',
            linewidth=1)
        ) # x = 0
        ax.add_line(
            plt.Line2D((w, w), (-h*0.05, h*1.05), color='black', linestyle='-.',
            linewidth=1)
        ) # x = L
        ax.add_line(
            plt.Line2D((w, w*1.01), (h*0.1, h*0.1), color='black', lw=0.5)
        ) # aquifer bottom tick
        ax.add_line(
            plt.Line2D((w, w*1.01), (h*0.9, h*0.9), color='black', lw=0.5)
        ) # aquifer top tick
        ax.text(w*1.02, h*0.05, str(self.bot) +' RL', fontsize=12)
        ax.text(w*1.02, h*0.85, str(self.top) +' RL', fontsize=12)
        ax.text(0, h*1.1, 'x = 0', fontsize=12, horizontalalignment='center')
        ax.text(
            w, h*1.1, 'x = ' + str(self.L), fontsize=12,
            horizontalalignment='center'
        )
        plt.axis('scaled')
        plt.axis('off')
        plt.tight_layout()
        plt.show()
        plt.close()
        return


class Aq1dFiniteUnconf(Aquifer):
    """1D, finite unconfined aquifer subclass.

    A subclass of the Aquifer class defining a horizontal, 1D unconfined aquifer
    with finite lateral extent and unconfined storage.

    The default Aq1dFiniteUnconf object has hydraulic conductivity K=1, specific
    yield Sy=0.1, static saturated thickness B=10, aquifer length L=1000 and
    aquifer bottom (datum) elevation bot=0. Exceptions will occur if invalid
    values are provided for K, Sy, B or L.

    The .info and .draw methods display the aquifer information and diagram.

    Attributes:
        Sy (float) : aquifer specific yield (units 1, default 0.1).
        L (float) : aquifer length (units L, default 1000.0).

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
    def __init__(self, K=1, Sy=0.1, B=10, L=1000, bot=0,
    name='Unnamed Aquifer'):
        super().__init__(K, B, bot, name)
        self.Sy = Sy
        self.L = L
        self.type = '1D, finite, unconfined homogeneous aquifer'
        return

    @property
    def K(self):
        """float : aquifer hydraulic conductivity (units L/T, default 1.0).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._K

    @K.setter
    def K(self, v):
        if not (v > 0):
            raise Exception('Hydraulic conductivity (K) must be positive.')
        self._K = v

    @property
    def Sy(self):
        """float : aquifer specific yield (units 1, default 0.1).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._Sy

    @Sy.setter
    def Sy(self, v):
        if not (v > 0 and v < 1):
            raise Exception(
            'Specific yield (Sy) must be positive and less than 1.'
            )
        self._Sy = v

    @property
    def B(self):
        """float : aquifer thickness (units L, default 10.0).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._B

    @B.setter
    def B(self, v):
        if not (v > 0):
            raise Exception('Aquifer thickness (B) must be positive.')
        self._B = v

    @property
    def L(self):
        """float : aquifer length (units L, default 1000.0).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._L

    @L.setter
    def L(self, v):
        if not (v > 0):
            raise Exception('Aquifer length (L) must be positive.')
        self._L = v

    @property
    def T(self):
        """float : aquifer transmissivity (units L2/T, default 10.0)."""
        return self.K * self.B

    @property
    def S(self):
        """float : aquifer storage coefficient (units 1, default 0.1)."""
        return self.Sy

    @property
    def swl(self):
        """float : aquifer static water table elevation (units L reduced level,
        default 10.0).
        """
        return self.bot + self.B

    def info(self):
        """Print the aquifer information."""
        print('AQUIFER INFORMATION')
        print('-------------------')
        print('Type:', self.type)
        print('Name:', self.name)
        print('Hydraulic conductivity:', self.K, '[L/T]')
        print('Specific yield:', self.Sy, '[1]')
        print('Static saturated thickness:', self.B, '[L]')
        print('Length:', self.L, '[L]')
        print('Static transmissivity:', self.T, '[L2/T]')
        print('Bottom elevation:', self.bot, '[RL]')
        print('Static water table:', self.swl, '[RL]')
        print()
        return

    def draw(self, dw=6):
        """Display a drawing of the aquifer.

        Args:
            dw (float) : width of figure (default 6.0).

        """
        import matplotlib.pyplot as plt
        import numpy as np
        drawing_ratio = 3
        dw = dw * 1.13
        w, h = dw, dw/drawing_ratio
        fig = plt.figure(figsize=(w, h))
        fig.suptitle(self.name, fontsize=14, fontweight=530)
        ax = plt.gca()
        ax.add_patch(
            plt.Rectangle((0, 0), width=w, height=h*0.1, facecolor='grey',
            edgecolor='black', hatch='///')
        ) # bottom aquitard
        ax.add_patch(
            plt.Rectangle((0, h*0.1), width=w, height=h*0.8, hatch='...',
            edgecolor='black', facecolor='white')
        ) # aquifer
        ax.add_patch(
            plt.Polygon(np.array([[0.95*w/3, h], [w/3, h*0.9], [1.05*w/3, h]]),
            closed=True, edgecolor='black', facecolor='white')
        )
        ax.add_line(
            plt.Line2D((0, 0), (-h*0.05, h), color='black', linestyle='-.',
            linewidth=1)
        ) # x = 0
        ax.add_line(
            plt.Line2D((w, w), (-h*0.05, h), color='black', linestyle='-.',
            linewidth=1)
        ) # x = L
        ax.add_line(
            plt.Line2D((w, w*1.01), (h*0.1, h*0.1), color='black', lw=0.5)
        ) # aquifer bottom tick
        ax.add_line(
            plt.Line2D((w, w*1.01), (h*0.9, h*0.9), color='black',
            lw=0.5)
        ) # aquifer top tick
        ax.text(w*1.02, h*0.05, str(self.bot) +' RL', fontsize=12)
        ax.text(w*1.02, h*0.85, str(self.swl) +' RL', fontsize=12)
        ax.text(0, h*1.1, 'x = 0', fontsize=12, horizontalalignment='center')
        ax.text(
            w, h*1.1, 'x = ' + str(self.L), fontsize=12,
            horizontalalignment='center'
        )
        plt.axis('scaled')
        plt.axis('off')
        plt.tight_layout()
        plt.show()
        plt.close()
        return


class Aq1dSemifiniteConf(Aquifer):
    """1D, semi-infinite confined aquifer subclass.

    A subclass of the Aquifer class defining a horizontal, 1D confined aquifer
    with semi-finite (semi-infinite) lateral extent and confined storage.

    The default Aq1dSemifiniteConf object has hydraulic conductivity K=1,
    specific storativity Ss=0.0001, aquifer saturated thickness B=10 and aquifer
    bottom (datum) elevation bot=0. Exceptions will occur if invalid values are
    provided for K, Ss or B.

    The .info and .draw methods display the aquifer information and diagram.

    Attributes:
        Ss (float) : aquifer specific storativity (units 1/L, default 1.0e-4).

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
    def __init__(self, K=1, Ss=1e-4, B=10, bot=0, name='Unnamed Aquifer'):
        super().__init__(K, B, bot, name)
        self.Ss = Ss
        self.type = '1D, semi-infinite, confined homogeneous aquifer'
        return

    @property
    def K(self):
        """float : aquifer hydraulic conductivity (units L/T, default 1.0).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._K

    @K.setter
    def K(self, v):
        if not (v > 0):
            raise Exception('Hydraulic conductivity (K) must be positive.')
        self._K = v

    @property
    def Ss(self):
        """float : aquifer specific storativity (units 1/L, default 1.0e-4).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._Ss

    @Ss.setter
    def Ss(self, v):
        if not (v > 0):
            raise Exception('Specific storage (Ss) must be positive.')
        self._Ss = v

    @property
    def B(self):
        """float : aquifer thickness (units L, default 10.0).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._B

    @B.setter
    def B(self, v):
        if not (v > 0):
            raise Exception('Aquifer thickness (B) must be positive.')
        self._B = v

    @property
    def S(self):
        """float : aquifer storage coefficient (units 1, default 1.0e-3)."""
        return self.Ss * self.B

    @property
    def D(self):
        """float : aquifer diffusivity (units L2/T, default 1.0e+4)."""
        return self.T / self.S

    def info(self):
        """Print the aquifer information."""
        print('AQUIFER INFORMATION')
        print('-------------------')
        print('Type:', self.type)
        print('Name:', self.name)
        print('Hydraulic conductivity:', self.K, '[L/T]')
        print('Specific storativity:', self.Ss, '[1/L]')
        print('Thickness:', self.B, '[L]')
        print('Transmissivity:', self.T, '[L2/T]')
        print('Storage coefficient:', self.S, '[1]')
        print('Diffusivity:', self.D, '[L2/T]')
        print('Bottom elevation:', self.bot, '[RL]')
        print('Top elevation:', self.top, '[RL]')
        print()
        return

    def draw(self, dw=6):
        """Display a drawing of the aquifer.

        Args:
            dw (float) : Width of figure (default 6.0).

        """
        import matplotlib.pyplot as plt
        drawing_ratio = 3
        dw = dw * 1.2
        w, h = dw, dw/drawing_ratio
        fig = plt.figure(figsize=(w, h))
        fig.suptitle(self.name, fontsize=14, fontweight=530)
        ax = plt.gca()
        ax.add_patch(
            plt.Rectangle((0, 0), width=w, height=h*0.1, facecolor='grey',
            edgecolor='black', hatch='///')
        ) # bottom aquitard
        ax.add_patch(
            plt.Rectangle((0, h*0.1), width=w, height=h*0.8, hatch='...',
            facecolor='white')
        ) # aquifer
        ax.add_line(
            plt.Line2D((0, 0), (0, h), color='black', lw=0.5)
        ) # aquifer boundary
        ax.add_patch(
            plt.Rectangle((0, h*0.9), width=w, height=h*0.1, facecolor='grey',
            edgecolor='black', hatch='///')
        ) # top aquitard
        ax.add_line(
            plt.Line2D((0, 0), (-h*0.05, h*1.1), color='black', linestyle='-.',
            linewidth=1)
        ) # x = 0
        ax.add_line(
            plt.Line2D((w, w*1.01), (h*0.1, h*0.1), color='black', lw=0.5)
        ) # aquifer bottom tick
        ax.add_line(
            plt.Line2D((w, w*1.01), (h*0.9, h*0.9), color='black', lw=0.5)
        ) # aquifer top tick
        ax.text(w*1.02, h*0.05, str(self.bot) +' RL', fontsize=12)
        ax.text(w*1.02, h*0.85, str(self.top) +' RL', fontsize=12)
        ax.text(0, h*1.2, 'x = 0', fontsize=12, horizontalalignment='center')
        plt.axis('scaled')
        plt.axis('off')
        plt.tight_layout()
        plt.show()
        plt.close()
        return


class Aq1dSemifiniteUnconf(Aquifer):
    """1D, semi-infinite unconfined aquifer subclass.

    A subclass of the Aquifer class defining a horizontal, 1D unconfined aquifer
    with semi-finite (semi-infinte) lateral extent and unconfined storage.

    The default Aq1dFiniteUnconf object has hydraulic conductivity K=1,
    specific yield Sy=0.1, static saturated thickness B=10 and aquifer bottom
    (datum) elevation bot=0. Exceptions will occur if invalid values are
    provided for K, Sy or B.

    The .info and .draw methods display the aquifer information and diagram.

    Attributes:
        Sy (float) : aquifer specific yield (units 1, default 0.1).

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
    def __init__(self, K=1, Sy=0.1, B=10, bot=0, name='Unnamed Aquifer'):
        super().__init__(K, B, bot, name)
        self.Sy = Sy
        self.type = '1D, semi-infinite, unconfined homogeneous aquifer'
        return

    @property
    def K(self):
        """float : aquifer hydraulic conductivity (units L/T, default 1.0).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._K

    @K.setter
    def K(self, v):
        if not (v > 0):
            raise Exception('Hydraulic conductivity (K) must be positive.')
        self._K = v

    @property
    def Sy(self):
        """float : aquifer specific yield (units 1, default 0.1).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._Sy

    @Sy.setter
    def Sy(self, v):
        if not (v > 0 and v < 1):
            raise Exception(
            'Specific yield (Sy) must be positive and less than 1.'
            )
        self._Sy = v

    @property
    def B(self):
        """float : aquifer thickness (units L, default 10.0).

        Setter method checks for valid values and triggers an exception if
        invalid values are specified.
        """
        return self._B

    @B.setter
    def B(self, v):
        if not (v > 0):
            raise Exception('Aquifer thickness (B) must be positive.')
        self._B = v

    @property
    def T(self):
        """float : aquifer transmissivity (units L2/T, default 10.0)."""
        return self.K * self.B

    @property
    def S(self):
        """float : aquifer storage coefficient (units 1, default 0.1)."""
        return self.Sy

    @property
    def swl(self):
        """float : aquifer static water table elevation (units L reduced level,
        default 10.0).
        """
        return self.bot + self.B

    def info(self):
        """Print the aquifer information."""
        print('AQUIFER INFORMATION')
        print('-------------------')
        print('Type:', self.type)
        print('Name:', self.name)
        print('Hydraulic conductivity:', self.K, '[L/T]')
        print('Specific yield:', self.Sy, '[1]')
        print('Static saturated thickness:', self.B, '[L]')
        print('Static transmissivity:', self.T, '[L2/T]')
        print('Bottom elevation:', self.bot, '[RL]')
        print('Static water table:', self.swl, '[RL]')
        print()
        return

    def draw(self, dw=6):
        """Display a drawing of the aquifer.

        Args:
            dw (float) : width of figure (default 6.0).

        """
        import matplotlib.pyplot as plt
        import numpy as np
        drawing_ratio = 3
        dw = dw * 1.13
        w, h = dw, dw/drawing_ratio
        fig = plt.figure(figsize=(w, h))
        fig.suptitle(self.name, fontsize=14, fontweight=530)
        ax = plt.gca()
        ax.add_patch(
            plt.Rectangle((0, 0), width=w, height=h*0.1, facecolor='grey',
            edgecolor='black', hatch='///')
        ) # bottom aqitard
        ax.add_patch(
            plt.Rectangle((0, h*0.1), width=w, height=h*0.8, hatch='...',
            facecolor='white')
        ) # aquifer
        ax.add_line(
            plt.Line2D((0, w), (h*0.9, h*0.9), color='black', lw=0.5)
        ) # water table
        ax.add_line(
            plt.Line2D((0, 0), (0, h*0.9), color='black', lw=0.5)
        ) # aquifer boundary
        ax.add_patch(
            plt.Polygon(np.array([[0.95*w/3, h], [w/3, h*0.9], [1.05*w/3, h]]),
            closed=True, edgecolor='black', facecolor='white')
        )
        ax.add_line(
            plt.Line2D((0, 0), (-h*0.05, h), color='black', linestyle='-.',
            linewidth=1)
        ) # x = 0
        ax.add_line(
            plt.Line2D((w, w*1.01), (h*0.1, h*0.1), color='black', lw=0.5)
        ) # aquifer bottom tick
        ax.add_line(
            plt.Line2D((w, w*1.01), (h*0.9, h*0.9), color='black', lw=0.5)
        ) # aquifer bottom tick
        ax.text(w*1.02, h*0.05, str(self.bot) +' RL', fontsize=12)
        ax.text(w*1.02, h*0.85, str(self.swl) +' RL', fontsize=12)
        ax.text(0, h*1.1, 'x = 0', fontsize=12, horizontalalignment='center')
        plt.axis('scaled')
        plt.axis('off')
        plt.tight_layout()
        plt.show()
        plt.close()
        return
