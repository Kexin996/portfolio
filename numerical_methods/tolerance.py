"""
Input:
tol = prescribed tolerance
I numerical(n) = result of the numerical integration rule with
n intervals; any integration rule can be used 

Output:
I_approx = approximation o the integration of f (x) with tolerance tol

n = 4; I_old = Lnumerical(n)
n = 2n; I_new = I_numerical(n) 

while (abs(I_new - I_old) > tol)
    I_old = I_new
    n = 2n
    I_new = I_numerical(n) 
end

I_approx = I_new
"""

import numpy as np

from midpoint_rule import *
from simpson_rule import *
from trapezoidal_rule import *

def tolerance(tol,a,b,f,choice):

    n = 4
    I_old = choice(a,b,n,f)
 
    n = 2*n
    I_new = choice(a,b,n,f)
    
    

    while (abs(I_new - I_old) > tol):
        I_old = I_new
        n=2*n
        I_new = choice(a,b,n,f)
    
    return I_new


# testcase
'''
print()
tol = 0.5 * 10 ** (-7)
y = lambda x: np.e**(-x**2)
a = 0
b = 2
n = 512
print(tolerance(tol,a,b,y,simpson))
print()


y = lambda x: (x+1)**(-2)
a = 1
b = 3
n = 8
'''





