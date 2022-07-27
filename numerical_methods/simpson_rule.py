"""
Input:
a = left endpoint of the integration interval 
b = right endpoint of the integration interval 
n = number of partition intervals
I_int(x) = routine evaluating f(x)

Output:
I_Simpson = Simpson's Rule approximation of the integration of f(x)
h=(b-a)/n
I_Simpson = I_int(a)/6 + I_int(b)/6 

for i = 1 : (n - 1)
    I_Simpson = I-Bimpson +I_int(a+ih)/3 
end

for i = 1 : n
    I_Simpson=I_Simpson+f_int(a+(i-1/2)h)/3
end

I_Simpson = h * I_Simpson
"""

import numpy as np
def simpson(a,b,n,f):
    h=(b-a)/n
    I_simpson = f(a)/6 + f(b)/6 

    for i in range(1,n):
        I_simpson = I_simpson + f(a+i*h)/3
    
    for i in range(1,n+1):
        I_simpson = I_simpson + 2*f(a+(i-1/2)*h)/3

    return h*I_simpson


# testcase
'''
print()
y = lambda x: np.e**(-x**2)
a = 0
b = 2
n = 4
print(simpson(a,b,n,y))
print()

y = lambda x: (x+1)**(-2)
a = 1
b = 3
n = 8
print(simpson(a,b,n,y))
'''


