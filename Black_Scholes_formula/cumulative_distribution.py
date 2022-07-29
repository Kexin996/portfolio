"""
Input:
t = real number 

Output:
function nn = cum_dist_normal(t)

z = abs(t)
y = 1/(1 +0.2316419z)

a1 = 0.319381530; 
a2 = -0.356563782; 
a3 = 1.781477937;
a4 = -1.821255978; 
a5 = 1.330274429;
m=1- exp(-t^2/2) * (a1*y + a2*y^2 + a3*y^3 + a4*y^4+a5*y^5)/(2pi)^(1/2) 
if t > 0
    nn=m
else
    nn = 1-m
end
"""

import numpy as np
import math


def cum_dist_normal(t):
    z = abs(t)
    y = 1 / (1+0.2316419*z)

    a1 = 0.319381530
    a2 = -0.356563782
    a3 = 1.781477937
    a4 = -1.821255978
    a5 = 1.330274429

    m = 1 -  np.e**(-t**2 / 2)*(a1*y + a2*y**2 + a3*y**3 + a4*y**4 + a5*y**5) / pow(2*math.pi,0.5)
    
    if t > 0:
        return round(m,6)
    else:
        return round(1-m,6)

# testcase
'''
print(cum_dist_normal(0.383206))
print(cum_dist_normal(0.171073))
'''