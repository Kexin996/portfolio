#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 10:29:51 2022

@author: zhangkexin
"""

"""
Implementation of Momentum
"""
import pandas as pd
data = pd.read_pickle('amzn.pkl')
close = data['Adj Close']

n = 20
history = []
mom_values = []

for close_price in close:
    history.append(close_price)
    
    if len(history) > n:
        del history[0]
    
    mom = close_price - history[0]
    mom_values.append(mom)


# we visualize it
data = data.assign(mom = pd.Series(mom_values, index = data.index))

import matplotlib.pyplot as plt
fig = plt.figure()
ax1 = fig.add_subplot(211, ylabel = 'price')
close.plot(ax=ax1, legend = True, color = 'g', lw = 1)

ax2 = fig.add_subplot(212, ylabel = 'price')
data['mom'].plot(ax = ax2, legend = True, color = 'b',lw = 1)
plt.show()
# we can see that mom is positive for consecutive days where the price has an upward trend
# mom is negative for consecutive days where the price has a downward trend

