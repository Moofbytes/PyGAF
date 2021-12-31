
"""
PyGAF: python modules for evaluating and exploring analytic solutions
to groundwater flow problems.

PyGAF stands for Python Groundwater Analytic Flow.

The package concept is to provide an educational and practical
environment for exploration of groundwater flow concepts and published
analytic (closed-form) mathematical solutions.

PyGAF has the following main modules:
  aq.py - aquifer classes
  well.py - well classes
  stress.py - aquifer stress classes
  welflo.py - well flow solution classes
  rch.py - groundwater recharge solution classes
"""

from pygaf import aq
from pygaf import well
from pygaf import stress
from pygaf import welflo

_all__ = [
    'aq',
    'well',
    'stress',
    'welflo',
    'rch'
]
