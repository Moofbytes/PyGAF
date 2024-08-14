"""
Analytic solutions for groundwater flow.

"""

from pygaf.solutions.thiem_1906 import ThiemWell
from .dupuit_thiem import DupuitThiemWell
from .theis_1935 import TheisWell
from .glover_1960 import GloverRectBasinSteady
from .steady_flow import Steady1dConfFlow
from .mine_flow import *
