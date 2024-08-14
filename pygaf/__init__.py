
"""
PyGAF - Python Groundwater Analytic Flow.

Python package for evaluation and display of analytic solutions for
groundwater flow.

Repository: https://github.com/Moofbytes/PyGAF
Documentation: https://pygaf.readthedocs.io/en/latest/index.html

"""

from pygaf.aquifers import (
    Aquifer,
    Aq2dConf,
    Aq2dLeaky,
    Aq2dUnconf,
    Aq1dFiniteConf,
    Aq1dFiniteUnconf,
    Aq1dSemifiniteConf,
    Aq1dSemifiniteUnconf
 )

from pygaf.wells import (
    Well,
    SteadyWell,
    TransientWell
)

from pygaf.stresses import (
    StressSeries
)

from pygaf.grids import (
    SteadyWellGrid,
    BasinGrid
)

from pygaf.basins import (
    RectBasin,
    CircBasin
)

from pygaf.bcs import (
    SteadyBC
)

from pygaf.solutions import *

import pygaf.utils
