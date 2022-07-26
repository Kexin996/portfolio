"""
Input:
a = left endpoint of the integration interval 
b = right endpoint of the integration interval 
n = number of partition intervals
f_int(x) = routine evaluating f(x)

Output:
I_midpoint = Midpoint Rule approximation of integration of f(x)

h=(b-a)/n
I_midpoint=0 

for i= 1:n
    I_midpoint = I_midpoint + f_int(a + (i - 1/2)h) 
end

I_midpoint = h * I_midpoint
"""

import numpy as np
def midpoint(a,b,n,f):

    h = (b-a) / n
    I_midpoint = 0

    for i in range(1,n+1):
        I_midpoint = I_midpoint+f(a+(i-0.5)*h)
    
    I_midpoint = h * I_midpoint
    
    return I_midpoint

# testcase
print()
y = lambda x: np.e**(-x**2)
a = 0
b = 2
n = 4
print(midpoint(a,b,n,y))
print()

y = lambda x: (x+1)**(-2)
a = 1
b = 3
n = 8
print(midpoint(a,b,n,y))



