
"""
PyGAF - Python Groundwater Analytic Flow.

Educational and practical environment for evaluating, displaying
and exploring analytic solutions to groundwater flow models.
"""

from .aq import (
  Aquifer,
  D1RadConf,
  D1RadUnconf,
  D1FiniteConf,
  D1FiniteUnconf,
  D1SemifiniteConf,
  D1SemifiniteUnconf
)
from .well import (
  Well,
  Steady,
  Transient
)
from .stress import StressSeries
from .solutions import *

_all__ = [
  'Aquifer',
  'D1RadConf',
  'D1RadUnconf',
  'D1FiniteConf',
  'D1FiniteUnconf',
  'D1SemifiniteConf',
  'D1SemifiniteUnconf',
  'Well',
  'Steady',
  'Transient',
  'StressSeries'
]
