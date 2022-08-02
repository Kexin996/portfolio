#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 12:16:20 2022

@author: zhangkexin
"""

"""
Implementation of relative strength indicator
"""
import pandas as pd
import statistics as stats
data = pd.read_pickle('amzn.pkl')
close = data['Adj Close']

# we still use 20 days for convenience
n = 20 
# we use some variables to store data for later visualization
gain_history = []
loss_history = []
avg_gain = []
avg_loss = []

rsi = []
last_price = 0

for close_price in close:
    if last_price == 0:
        last_price = close_price
    # we consider the gain and loss
    gain_history.append(max(close_price - last_price,0))
    loss_history.append(max(last_price - close_price,0))
    last_price = close_price
    
    if len(gain_history) > n:
        del(gain_history[0]) # since they are appdned together
        del(loss_history[0]) # we delete them together
    
    avg_gain_v = stats.mean(gain_history)
    avg_loss_v = stats.mean(loss_history)
    avg_gain.append(avg_gain_v)
    avg_loss.append(avg_loss_v)
    
    rs = 0
    if avg_loss_v > 0:
        rs = avg_gain_v / avg_loss_v
    rsi_value = 100 * (1 - (1 / (rs+1)))
    rsi.append(rsi_value)

data = data.assign(rsi = pd.Series(rsi, index = data.index))
data = data.assign(avgloss = pd.Series(avg_loss, index = data.index))
data = data.assign(avggains = pd.Series(avg_gain, index = data.index))

import matplotlib.pyplot as plt
fig = plt.figure()
ax1 = fig.add_subplot(311, ylabel = 'price')
data['Adj Close'].plot(ax = ax1, color = 'black', title = 'close price',lw = 1, legend = True)

ax2 = fig.add_subplot(312, ylabel = 'price')
data['avgloss'].plot(ax =ax2, color = 'r',lw = 1, legend = True)
data['avggains'].plot(ax = ax2, color = 'g',lw = 1, legend = True)

ax3 = fig.add_subplot(313, ylabel = 'RSI')
data['rsi'].plot(ax =ax3, color = 'r',lw = 1, legend = True)
# when RSI > 50%, it is the time for us to buy it

    

