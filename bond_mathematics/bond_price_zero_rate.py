"""
Input:
n = number of cash flows
t_cash_flow = vector of cash flow dates (of size n) 
v_cash_flow = vector of cash flows (of size n) 
r_zero(t) = zero rate corresponding to time t

Output:
B = bond price

B=O     
for i = 1:n
    disc(i) = exp(-t_cash_flow(i) *r_zero(t_cash_flow(i)) )
    B = B +v_cash_flow(i) disc(i) 
end

"""
import numpy as np
def bond_price_zero(n, t_cash_flow, v_cash_flow, r_zeros):
    if (len(t_cash_flow) != n or len(v_cash_flow) != n):
        return "try again please."
    B = 0
    disc = []
    for i in range(1, n+1):
        disc_temp = np.e**(-t_cash_flow[i-1]*r_zeros(t_cash_flow[i-1]))
        B += v_cash_flow[i-1]*disc_temp
        disc.append(round(disc_temp,6))
    
    # we leave 6 digits after decimal points
    return [disc,round(B,6)]

# testcase
'''
n = 4
t = [2/12,8/12,14/12,20/12]
v = [3,3,3,103]
r = lambda x: 0.0525+np.log(1+2*x) / 200
print(bond_price_zero(n,t,v,r))
'''










