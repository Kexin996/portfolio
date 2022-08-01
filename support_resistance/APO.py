#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 23:30:25 2022

@author: zhangkexin
"""

"""
Absolute Price Oscillator
"""
import pandas as pd
n_fast = 10 # we want the fast EMA to be 10 days window size
n_slow = 40  # slow EMA to be 40 days
K_fast = 2/ (n_fast+1)
K_slow = 2 / (n_slow+1)
ema_fast = 0
ema_slow = 0

# we use three variables to save ema values for visualizations
ema_fast_values = []
ema_slow_values = []
apo_values = []

amzn_data = pd.read_pickle('amzn.pkl')
close = amzn_data['Adj Close']

for close_price in close:
    if ema_fast == 0:
        ema_fast = close_price
        ema_slow = close_price
    else:
        ema_fast = close_price * K_fast + (1-K_fast)*ema_fast
        ema_slow = close_price * K_slow + (1-K_slow)*ema_slow
    ema_fast_values.append(ema_fast)
    ema_slow_values.append(ema_slow)
    apo_values.append(ema_fast - ema_slow)
    
import matplotlib.pyplot as plt
fig = plt.figure()
ax1 = fig.add_subplot(211,ylabel = 'price')
close.plot(ax = ax1, color = 'g',lw = 1, legend = True)

amzn_data = amzn_data.assign(fast_ema = pd.Series(ema_fast_values,index = amzn_data.index))
amzn_data = amzn_data.assign(slow_ema = pd.Series(ema_slow_values, index = amzn_data.index))
amzn_data = amzn_data.assign(apo = pd.Series(apo_values, index = amzn_data.index))

amzn_data['fast_ema'].plot(ax = ax1, color = 'b',lw = 1, legend = True)
amzn_data['slow_ema'].plot(ax =ax1, color = 'r',lw = 1, legend = True)
ax2 = fig.add_subplot(212,ylabel = 'APO')
amzn_data['apo'].plot(ax = ax2, color = 'black',lw = 1,legend = True)
plt.show()

# we can observe that when APO is positive, there is a short-term upward trend
# when APO is negative, there is a short-term downward trend