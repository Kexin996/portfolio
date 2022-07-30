#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 15:38:03 2022

@author: zhangkexin
"""
"""
Implementation of EMA

"""
import pandas as pd
n = 20 # size of the window
K = 2 / (n +1)
ema_p = 0
ema_values = []

amzn_data = pd.read_pickle('amzn.pkl')
close = amzn_data['Adj Close']

# we calculate the ema following the recursion formula
for close_price in close:
    if ema_p == 0: # for the first observation, ema itself will be the price
        ema_p = close_price
    else:
        ema_p = K * close_price + (1-K) * ema_p
        
    ema_values.append(ema_p)

amzn_data = amzn_data.assign(EMA_in_20_days = pd.Series(ema_values, index = amzn_data.index))

# we draw the graph
import matplotlib.pyplot as plt
fig = plt.figure()
ax1 = fig.add_subplot(111,ylabel = 'price')
amzn_data['Adj Close'].plot(ax = ax1, color = 'g',lw = 1, label = "ClosePrice",legend = True)
amzn_data['EMA_in_20_days'].plot(ax = ax1, color = 'r',lw = 1,legend = True)
plt.plot()

