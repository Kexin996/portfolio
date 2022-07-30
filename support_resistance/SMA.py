#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 15:00:25 2022

@author: zhangkexin
"""

'''
Implementation of the simple moving average
'''
import statistics as stats
import pandas as pd

amzn_data = pd.read_pickle('amzn.pkl')
close = amzn_data['Adj Close']

time_period = 20 # set the number of days (the window size) we need
history = [] # this one is used to track history data
sma_values = []
    
for close_price in close:
    history.append(close_price)
    if len(history) > time_period:
        # we replace the oldest price since we need a "moving average"
        del(history[0]) # we use del so we don't need to move the whole list
        
    sma_values.append(sum(history) / len(history))
    


amzn_data = amzn_data.assign(ClosePrice = pd.Series(close,index = amzn_data.index))
amzn_data = amzn_data.assign(SMA_in_20_days = pd.Series(sma_values,index = amzn_data.index))

import matplotlib.pyplot as plt

fig = plt.figure()
ax1 = fig.add_subplot(111,ylabel = 'price')
amzn_data['ClosePrice'].plot(ax = ax1, color = 'g', lw = 1, legend = True)
amzn_data['SMA_in_20_days'].plot(ax = ax1, color = 'r',lw = 1, legend = True)

plt.show() # we can see how smoother the price now becomes


        

