"""
Functions for to evaluate Theis (1935) well solution
"""

from numpy import sqrt, log, pi, linspace
from scipy.special import expn


#########################################################
def ri(aq, t, qf):
    """
    Compute radius of influence, defined as radius of aquifer from which
    qf fraction (0 < qf < 1.0) of the pumped volume has been drawn
    aq - confined aquifer object
    q - well pumping rate
    t - time since start of pumping
    qf - fraction of pumped volume
    """
    r = sqrt(-4.0 * aq.T * t * log(1-qf)/aq.S)
    return r


#########################################################
def dd_rt(aq, q, r, t):
    """
    Compute drawdown at specified radius and t
    aq - confined aquifer object
    q - well pumping rate
    r - radius
    t - time since start of pumping
    """
    if t <= 0:
        print('ERROR! The time value must be greater than 0.0')
        return
    u = (r**2) * aq.S/(4.0 * aq.T * t)
    W = expn(1, u) # Well Function
    d = q * W/(4.0 * pi * aq.T) # drawdown
    return d


#########################################################
def dd_r(aq, q, r, tv):
    """
    Compute drawdown at specified radius over specified time period
    aq - confined aquifer object
    q - well pumping rate
    r - radial distance
    tv - time vector
    """
    d = []
    for i in range(tv.len):
        u = (r**2) * aq.S/(4.0 * aq.T * tv.times[i])
        W = expn(1, u) # Well Function
        d.append(q * W/(4.0 * pi * aq.T)) # drawdown
    return d