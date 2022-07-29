"""
Input:
t = present time (often equal to 0)
S = spot price of the underlying asset (at time t)
K = option strike
T = maturity date (time to maturity is T- t)
v = volatility of the underlying asset
r = constant interest rate
q = continuous dividend rate of the underlying asset

Output:
C = price of the European call option 
P = price of the European put option

d1 = (In (S/K ) + (r - q+ v^2/2)*(T-t))/(v * (T-t)**(1/2))
d2= d1 - v * (T-t)**(1/2)
C = S*e**(-q*(T-t))*cum_dist_normal(d1) - K*e ** (-r*(T-t)) * cum_dist_normal(d2)
P = K* e **(-r*(T-t))*cum_dist_normal(-d2) - S*e**(-q*(T-t)) * cum_dist_normal(-d1)
"""
import math 
import numpy as np
from cumulative_distribution import cum_dist_normal
def black_scholes_formula(t,S,K,T,v,r,q):
    d1 = (np.log(S / K)+(r-q+ v**2 / 2)*(T-t)) / (v * math.pow(T-t,0.5))
    d2 = d1 - v * math.pow(T-t,0.5)
    C = S * np.e ** (-q*(T-t)) * cum_dist_normal(d1) - K * np.e ** (-r*(T-t)) * cum_dist_normal(d2)
    P = K * np.e ** (-r*(T-t)) * cum_dist_normal(-d2) - S * np.e ** (-q*(T-t)) * cum_dist_normal(-d1)
    return [d1,d2,C,P]

# testcase
'''
print(black_scholes_formula(0,42,40,0.5,0.3,0.05,0.03))
'''