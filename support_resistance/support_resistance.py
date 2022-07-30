#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 11:54:32 2022

@author: zhangkexin
"""

'''
we buy at the support line
sell at the resistance line

a momentum strategy
'''
import pandas as pd
from pandas_datareader import data
import matplotlib.pyplot as plt

start_date = '2018-07-29'
end_date = '2022-07-29'

# for convenience, we will save the dataset as a local file for reusing it for 
# the following analysis

# if the dataset file doesn't exist, we just create it
# else, we will use the existing file

# Note: why do we use pickle
# pickcle is used to serialize data into binary files for transfering them
try:
    amzn_data1 = pd.read_pickle('amzn.pkl')
    
except FileNotFoundError:
    amzn_data1 = data.DataReader('AMZN','yahoo',start_date,end_date)
    amzn_data1.to_pickle('amzn.pkl')

amzn_data = amzn_data1.tail(620)
print(amzn_data)
lows = amzn_data['Low']
highs = amzn_data['High']

# we want to visualize the data
fig = plt.figure()
ax1 = fig.add_subplot(111,ylabel = 'price in $')
highs.plot(ax=ax1, color = 'c',lw = 2.)
lows.plot(ax = ax1,color = 'y',lw = 2.)

# parameters: y(y value of the line), xMin, xMax
# lows.index.values: we just turn the index into an array
plt.hlines(highs.head(200).max(),lows.index.values[0],lows.index.values[-1],linewidth = 2,color = 'g')
plt.hlines(lows.head(200).min(),lows.index.values[0],lows.index.values[-1],linewidth = 2, color = 'r')

# we draw a vertical line to show the time interval 
plt.axvline(linewidth = 2, color ='b',x = lows.index.values[200],linestyle=":")

# we will find that we will never make money if we just follow those resistence and support lines...
# we will continuously short, but never buy back
# we recognize that we have to adjust the interval

# we want to set an horizontal interval, where we can buy and sell at a value very close to support / resistance level
# we set the initial rolling window to be 20 ---> we use the max and min in 20 consecutive days 
import numpy as np
def trading_at_support_resistance(data,bin_width = 20):
    # we set up the variables we need
    data['sup_tolerance'] = pd.Series(np.zeros(len(data)))
    data['res_tolerance'] = pd.Series(np.zeros(len(data)))
    data['sup_count'] = pd.Series(np.zeros(len(data)))
    data['res_count'] = pd.Series(np.zeros(len(data)))
    data['sup'] = pd.Series(np.zeros(len(data)))
    data['res'] = pd.Series(np.zeros(len(data)))
    data['positions'] = pd.Series(np.zeros(len(data)))
    data['signal'] = pd.Series(np.zeros(len(data)))
    in_support = 0
    in_resistance = 0
    
    # we begin to roll over the dataset
    for x in range(bin_width,len(data)):
        # we start at bin_width-1
        data_section = data['price'][x-bin_width:x+1] # we want it to be approximate bin_width
   
        support_level = min(data_section)
        resistance_level = max(data_section)
        range_level = resistance_level - support_level
        data['res'][x] = resistance_level
        data['sup'][x] = support_level
        # the tolerance we use is 20% of the range
        data['sup_tolerance'][x] = support_level +0.2*range_level
        data['res_tolerance'][x] = resistance_level-0.2*range_level
        
        # if the price falls in the tolerance, we buy or sell the stocks
        if data['price'][x] >= data['res_tolerance'][x] and data['price'][x] <= data['res'][x]:
            in_resistance += 1
            data['res_count'][x] = in_resistance
        elif data['price'][x] <= data['sup_tolerance'][x] and data['price'][x] >= data['sup'][x]:
            in_support += 1
            data['sup_count'][x] = in_support
        else:
            # we reset the number
            # if the price is not in thr range we defined
            in_support = 0
            in_resistance = 0
        
        # we check whether we can buy or sell the stocks
        # why? 
        # we only buy when there are two consecutive days that the price stays in support tolerance
        # and we only sell when they are two consecutive days that the price stays in resistance tolerance
        if in_resistance > 2:
            data['signal'][x] = 1 # 1: long
        elif in_support > 2:
            data['signal'][x] = 0
        else:
            data['signal'][x] = data['signal'][x-1] # in this way, we will not buy nor sell
            # our positions are defined by the difference between signals value
            
    data['positions'] = data['signal'].diff()

amzn_data_signal = pd.DataFrame(index = amzn_data.index)
amzn_data_signal['price'] = amzn_data['Adj Close']

trading_at_support_resistance(amzn_data_signal)

# now we want to see the graph
fig = plt.figure()
ax1 = fig.add_subplot(111,ylabel = 'price')
amzn_data_signal['sup'].plot(ax=ax1, color = 'g',lw = 2)
amzn_data_signal['res'].plot(ax = ax1, color = 'b', lw = 2)
amzn_data_signal['price'].plot(ax = ax1, color = 'r', lw = 2)

ax1.plot(amzn_data_signal.loc[amzn_data_signal.positions == 1].index, amzn_data_signal.price[amzn_data_signal.positions == 1.0],'^',markersize = 7, color = 'k',label = 'buy')
ax1.plot(amzn_data_signal.loc[amzn_data_signal.positions == -1].index, amzn_data_signal.price[amzn_data_signal.positions == -1],'v',markersize = 7, color = 'k',label = 'sell')
plt.legend()
plt.show()
        
        
        
        
        
    
    
    
