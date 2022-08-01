#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 09:23:18 2022

@author: zhangkexin
"""

"""
implementation of mean average convergence divergence
"""
import pandas as pd
amzn = pd.read_pickle('amzn.pkl')
close = amzn['Adj Close']

# we set up variables
n_fast = 12
n_slow = 26
n_macd = 9

k_fast = 2/(n_fast+1)
k_slow = 2/(n_slow+1)
k_macd = 2/(n_macd+1)

fast_values = []
slow_values = []
macd_values = []
macd_ema = []
macd_hist = []

ema_fast = 0
ema_slow = 0
ema_macd = 0

for close_price in close:
    if ema_fast == 0:
        ema_fast = close_price
        ema_slow = close_price
    else:
        ema_fast = close_price * k_fast + ema_fast*(1-k_fast)
        ema_slow = close_price * k_slow + ema_slow*(1-k_slow)
    
    fast_values.append(ema_fast)
    slow_values.append(ema_slow)
    macd = ema_fast-ema_slow
    
    if ema_macd == 0:
        ema_macd = macd
    else:
        ema_macd = k_macd * macd + (1-k_macd)*ema_macd
        
    macd_values.append(macd)
    macd_ema.append(ema_macd)
    macd_hist.append(macd - ema_macd)


amzn = amzn.assign(fast_ema = pd.Series(fast_values,index = amzn.index))
amzn = amzn.assign(slow_ema = pd.Series(slow_values, index = amzn.index))
amzn = amzn.assign(macd_values = pd.Series(macd_values,index = amzn.index))
amzn = amzn.assign(macd_ema = pd.Series(macd_ema, index = amzn.index)) # it is also called the signal line
amzn = amzn.assign(macd_histogram = pd.Series(macd_hist, index = amzn.index))

import matplotlib.pyplot as plt
fig = plt.figure()
ax1 = fig.add_subplot(311, ylabel = 'price')
amzn['fast_ema'].plot(ax = ax1, color = 'b',lw = 1,legend = True)
amzn['slow_ema'].plot(ax = ax1, color = 'r',lw = 1,legend = True)
amzn['Adj Close'].plot(ax = ax1, color = 'black', lw = 1,legend = True)

ax2 = fig.add_subplot(312, ylabel = 'apo')
amzn['macd_values'].plot(ax = ax2, color = 'b', lw = 1,legend = True)
amzn['macd_ema'].plot(ax = ax2, color = 'r', lw = 1,legend = True)

ax3 = fig.add_subplot(313, ylabel = 'difference')

amzn['macd_histogram'].plot(ax = ax3, color = 'b',kind='bar', legend = True,use_index = False)

plt.show()

# it is not diffifcult to see

        




