"""
Input:
a = left endpoint of the integration interval 
b = right endpoint of the integration interval 
n = number of partition intervals
I_int(x) = routine evaluating f(x)

Output:

I_trap = Trapezoidal Rule approximation of integration of f (x)
h=(b-a)/n
I_trap = I_int(a)/2 + I_int(b)/2 

for i = 1 : (n - 1)
    I_trap = I_trap +I_int(a+ih) 
end

I_trap = h * I_trap
"""

import numpy as np
def trapezoidal(a,b,n,f):
    h=(b-a)/n
    I_trap = f(a)/2 + f(b)/2 

    for i in range(1,n):
        I_trap = I_trap + f(a+i*h)
    return h*I_trap


# testcase
'''
print()
y = lambda x: np.e**(-x**2)
a = 0
b = 2
n = 4
print(trapezoidal(a,b,n,y))
print()

y = lambda x: (x+1)**(-2)
a = 1
b = 3
n = 8
print(trapezoidal(a,b,n,y))
'''


