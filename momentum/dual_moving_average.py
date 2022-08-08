#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 16:33:42 2022

@author: zhangkexin
"""

"""
Implementation of dual moving average strategy
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

# we create a dual moving average function
#
# input:
# short_mavg: Short-term moving average values 
# long_mavg: Long-term moving average values
# signal: True if the short-term moving average is higher than the long-term moving average
# orders: 1 for the buy order, and -1 for the sell order

# output:
#
# a dataframe recording the signals for buying and selling
def dual_moving_average(dataset,short_window,long_window):
    # we build the signals dataframe first
    signals = pd.DataFrame(index = dataset.index)
    signals['signals'] = 0.0
    
    signals['short_mavg'] = dataset['Close'].rolling(window = short_window,min_periods = 1,center = False).mean()
    # center: center = True ---> rolling at the center of the window index
    # e.g. windowsize = 3 ---> begins rolling at index 1 (0,1,2)
    
    signals['long_mavg'] = dataset['Close'].rolling(window = long_window, min_periods = 1, center = False).mean()
    signals['signals'][short_window:] = np.where(signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:],1.0,0.0)
    signals['orders'] = signals['signals'].diff()
    return signals

# we use 20 as the short_window size, 100 as the long window_size
ts = dual_moving_average(amzn_data,20,100)

    
# now we want to visualize our trading strategy
# our strategy is based on normal close, since 'adj close' will be influenced by news
# we check our strategy
fig = plt.figure()
ax1 = fig.add_subplot(111,ylabel = 'amazon stock price in $')
amzn_data['Adj Close'].plot(ax = ax1, color = 'k',lw = 1.)
ts['short_mavg'].plot(ax = ax1, color = 'b',lw = 1)
ts['long_mavg'].plot(ax = ax1, color = 'r',lw = 1)

# we plot the signals for buying and selling
ax1.plot(ts.loc[ts.orders == 1.0].index, amzn_data['Adj Close'][ts.orders == 1],'^',markersize = 7,color = 'g')
ax1.plot(ts.loc[ts.orders == -1].index, amzn_data['Adj Close'][ts.orders == -1],'v',markersize = 7, color = 'r')

plt.legend(['Price',"Short mavg","Long mavg","Buy","Sell"]) 
plt.title("Double Moving Average Trading Strategy")
plt.show()

# from the graph, we can see that we don't buy / sell frequently
# the change in momentum is reflected by the change in short moving average