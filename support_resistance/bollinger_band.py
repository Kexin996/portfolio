#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 11:42:46 2022

@author: zhangkexin
"""

"""
Implementation of Bollinger Band by using SMA as the 'mean'
"""
import pandas as pd


# we first define a function for calculating the standard deviation
def standard_deviation(interval,mean):
    if len(interval) == 0:
        return "try again please." # we rule out the base case
    
    s = 0
    for i in interval:
        s += (i-mean) ** 2
    return (s / len(interval)) ** 0.5

data = pd.read_pickle('amzn.pkl')
close = data['Adj Close']

n = 20 # we use 20 days as the time interval for SMA
factor = 2 # we set the std scaling factor to be 2

history = [] # we save the price history, sma_values, upper and lower of the bollinger bands for later display
sma_values = []
upper = []
lower = []

for close_price in close:
    history.append(close_price)
    
    if len(history) > n:
        del(history[0])
    
    sma = sum(history) / len(history)
    sma_values.append(sma) # this is the middle part of bollinger band
    
    # we want to get the std
    std = standard_deviation(history,sma)
    
    bband_upper = sma + factor*std
    bband_lower = sma - factor*std
    
    upper.append(bband_upper)
    lower.append(bband_lower)

# we visualize the graph
data = data.assign(sma = pd.Series(sma_values,index = data.index))
data = data.assign(bband_upper = pd.Series(upper, index = data.index))
data = data.assign(bband_lower = pd.Series(lower, index = data.index))

import matplotlib.pyplot as plt
fig = plt.figure()
ax1 = fig.add_subplot(111,ylabel = "price in $")
data['sma'].plot(color = 'g',lw = 1.,legend = True)
data['bband_upper'].plot(color = 'b',lw = 1., legend = True)
data['bband_lower'].plot(color = 'r',lw = 1., legend = True)
data['Adj Close'].plot(color = 'black', label = 'price', lw = 1., legend = True)
plt.show() # there are two competing opinions with respect to the samd band