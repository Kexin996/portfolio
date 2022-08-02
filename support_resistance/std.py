#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 23:17:47 2022

@author: zhangkexin
"""

"""
Implementation of Standard Deviation by Using 20-days SMA
"""
import pandas as pd
data = pd.read_pickle('amzn.pkl')
close = data['Adj Close']


n = 20 # we set 20-days as the interval
history = []
sma_values = []
std_values = []

for close_price in close:
    history.append(close_price)
    if len(history) > n:
        del(history[0])
    
    sma = sum(history) / len(history)
    sma_values.append(sma)
    
    variance = 0 # we calculate the variance and then take the square root
    for temp in history:
        variance += (temp - sma)**2
    
    variance /= len(history)
    
    std_values.append(variance ** 0.5)
    
import matplotlib.pyplot as plt
data = data.assign(sma = pd.Series(sma_values, index = data.index))
data = data.assign(std = pd.Series(std_values, index = data.index))

fig = plt.figure()
ax1 = fig.add_subplot(211, ylabel = 'price')
close.plot(ax = ax1, lw = 1, color = 'g',legend = True)

ax2 = fig.add_subplot(212, ylabel = 'price')
data['std'].plot(ax =ax2, lw = 1, color = 'b',legend = True)