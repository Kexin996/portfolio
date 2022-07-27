"""
Input:
n = number of cash flows
t_cash_flow = vector of cash flow dates (of size n) 
v_cash_flow = vector of cash flows (of size n) 
r_inst(t) =  instantaneous rate corresponding to time t
tol = vector of tolerances in the numerical approximation of discount factor integrals (of size n)

Output:
B = bond price

B=O     
for i = 1:n
    I_numerical(i) = 
    result of the numerical integration of r_inst(t) on the interval [0, t_cash_flow(i)] with tolerance tol(i);
    disc(i) = exp(-I_numerical(i))
    B = B +v_cash_flow(i) disc(i) 
end

"""
import numpy as np
import sys
sys.path.insert(0, '/Users/zhangkexin/Desktop/learning-algo/learning-trading-strategies/numerical_methods')
from simpson_rule import simpson
from tolerance import tolerance

def bond_price_instantaneous_rate(n, t_cash_flow, v_cash_flow, r_inst,tol):
    if (len(t_cash_flow) != n or len(v_cash_flow) != n or len(tol)== 0):
        return "try again please."
    B = 0
    disc = []
    for i in range(1, n+1): # for convenience, i just use simpson 
        I_numerical = tolerance(tol[i-1],0,t_cash_flow[i-1],r_inst,simpson)
        disc_temp = np.e**(-I_numerical)
        B += v_cash_flow[i-1]*disc_temp
        disc.append(round(disc_temp,6))
    
    # we leave 6 digits after decimal points
    return [disc,round(B,6)]

# testcase
# case 1
n = 4
t = [2/12,8/12,14/12,20/12]
v = [3,3,3,103]
r = lambda x: 0.0525+ 1 / (100*(1+np.e**(-x**2)))
tol = [10 ** (-4),10 ** (-4),10 ** (-4),10 ** (-6)]
print(bond_price_instantaneous_rate(n, t, v, r,tol))

# case 2

n = 4
t = [2/12,8/12,14/12,20/12]
v = [3,3,3,103]
r = lambda x: 0.0525+ np.log(1+2*x) / 200 + x / (100*(1+2*x))
tol = [10 ** (-4),10 ** (-4),10 ** (-4),10 ** (-6)]
print(bond_price_instantaneous_rate(n, t, v, r,tol))

# case 3
n = 4
t = [2/12,8/12,14/12,20/12]
v = [3,3,3,103]
r = lambda x: 0.0525+ np.log(1+2*x) / 200 + x / (100*(1+2*x))
tol = [10 ** (-4),10 ** (-4),10 ** (-4),10 ** (-4)]
print(bond_price_instantaneous_rate(n, t, v, r,tol))











