#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 17:30:43 2022

@author: zhangkexin
"""

"""
Implementation of turtle strategy
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas_datareader import data



def load_financial_data(start_date,end_date,output):
    try:
        df = pd.read_pickle(output)
    except FileNotFoundError:
        df = data.DataReader('AMZN','yahoo',start_date,end_date)
        df.to_pickle(output)
    return df

# we load the data first
# we use amazon stocks price in the past 4 years
amzn_data = load_financial_data('2016-01-01','2020-01-01','amzn.pkl')

# we define a turtle strategy
# we long when the price reaches the highest in the window
# we short when the price reaches the lowest in the window

def turtle_strategy(data,window_size):
    signals = pd.DataFrame(index = data.index)
    signals['orders'] = 0
    
    # we use two columns to save the highest and lowest price
    signals['high'] = data['Adj Close'].shift(1).rolling(window = window_size).max()
    signals['low'] = data['Adj Close'].shift(1).rolling(window = window_size).min()
    
    # we use avg to show the moving average of the window size
    signals['avg'] = data['Adj Close'].shift(1).rolling(window = window_size).mean()
    
    # we enter long position when the price > highest price in the window
    # we enter short position when the price < lowest price in the window
    signals['long_entry'] = data['Adj Close'] > signals['high']
    signals['short_entry'] = data['Adj Close'] < signals['low']
    
    # we leave a short position as the price < signals[low]
    # we leave a long position as the price > signals[high]
    signals['long_exit'] = data['Adj Close'] < signals['low']
    signals['short_exit'] = data['Adj Close'] > signals['high']
    
    # now we begin to set the orders
    # we leave positions only when we have positions in hand
    # for simplification, we cannot hold multiple postions in hand
    position = 0
    for i in range(len(data)):
        if signals['long_entry'][i] == 1 and position == 0:
            signals.orders.values[i] = 1 # use values to cope with the potential warning of copt of dataframe
            position = 1
        elif signals['short_entry'][i] == -1 and position == 0:
            signals.orders.values[i] = -1
            position = -1
        elif signals['long_exit'][i] == -1 and position == -1:
            signals.orders.values[i] = 1 # we exit our short position through buying (long)
            position = 0
        elif signals['short_exit'][i] == 1 and position == 1:
            signals.orders.values[i] = -1 # we exit our long position through selling (short)
            position = 0
        # else, we just keep the orders as 0.0
    
    return signals

ts = turtle_strategy(amzn_data,50) # we use 50 days as the window size

# we visualize the graph
fig = plt.figure()
ax1 = fig.add_subplot(111,ylabel = 'stock price in $')

amzn_data['Adj Close'].plot(ax = ax1, color = 'k',lw = 1.)
ts['high'].plot(ax = ax1, color = 'g',lw = 1.0)
ts['low'].plot(ax = ax1, color = 'r',lw = 1.0)
ts['avg'].plot(ax = ax1, color = 'b',lw = 1.0)

# we plot the signals
ax1.plot(ts.loc[ts.orders == 1.0].index, amzn_data['Adj Close'][ts.orders == 1.0],'^',color = 'g',markersize = 7)
ax1.plot(ts.loc[ts.orders == -1.0].index, amzn_data['Adj Close'][ts.orders == -1.0],'v',color = 'r',markersize = 7)


plt.legend(["Price","High","Low","Average","Buy","Sell"]) 
plt.title("Improved Turtle Trading Strategy")
plt.show()

# we can see that the buy and sell signals are closely followed by each other

      