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



