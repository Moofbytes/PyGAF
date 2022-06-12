
"""
PyGAF - Python Groundwater Analytic Flow.

Python package for evaluation and display of analytic solutions for
groundwater flow.

Repository: https://github.com/Moofbytes/PyGAF
Documentation: https://pygaf.readthedocs.io/en/latest/index.html

"""

from .aquifers import (
    Aquifer,
    Aq2dConf,
    Aq2dUnconf,
    Aq1dFiniteConf,
    Aq1dFiniteUnconf,
    Aq1dSemifiniteConf,
    Aq1dSemifiniteUnconf
 )

from .wells import (
    Well,
    SteadyWell,
    TransientWell
)

from .stresses import (
    StressSeries
)

from .grids import (
    WellGrid,
    BasinGrid
)

from .basins import (
    Basin,
    RectBasin,
    CircBasin
)

from .solutions import *
