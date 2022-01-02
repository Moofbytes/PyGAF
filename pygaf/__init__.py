
"""
PyGAF - Python Groundwater Analytic Flow.

Educational and practical environment for evaluating, displaying
and exploring analytic solutions to groundwater flow models.
"""

from .aquifers import (
  Aquifer,
  AqRadConf,
  AqRadUnconf,
  Aq1dFiniteConf,
  Aq1dFiniteUnconf,
  Aq1dSemifiniteConf,
  Aq1dSemifiniteUnconf
)
from .wells import Well, SteadyWell, TransientWell
from .stresses import StressSeries
from .solutions import *
