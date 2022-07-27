"""
Input:
n = number of cash flows
t_cash_flow = vector of cash flow dates (of size n) in years
v_cash_flow = vector of cash flows (of size n) 
y = yield of the bond 

Output:
B = price of the bond
D = duration of the bond 
C = convexity of the bond

B=0;D=0;C=0  
for i = 1:n
    disc(i) = exp(-t_cash_flow(i) * y)
    B = B + v_cash_flow(i) * disc(i) 
    D = D + t_cash_flow(i)* v_cashJlow(i)* disc(i) 
    C = C + t_cashJlow(i)^2 * v_cash_flow(i) * disc(i)
end

"""
import numpy as np
def b_d_c(n, t_cash_flow, v_cash_flow, y):
    if (len(t_cash_flow) != n or len(v_cash_flow) != n):
        return "try again please."
    B = 0
    D = 0
    C = 0
    disc = []
    for i in range(1, n+1):
        disc_temp = np.e**(-t_cash_flow[i-1]*y)
        B += v_cash_flow[i-1] * disc_temp
        D += t_cash_flow[i-1] * v_cash_flow[i-1] * disc_temp
        C +=  (t_cash_flow[i-1])**2 * v_cash_flow[i-1] * disc_temp
        disc.append(round(disc_temp,6))
    
    # we leave 6 digits after decimal points
    D = D/B
    C = C/B
    return [disc,round(B,6),round(D,6),round(C,6)]

# testcase


n = 4
t = [2/12,8/12,14/12,20/12]
v = [3,3,3,103]
y = 0.065
print(b_d_c(n,t,v,y))











