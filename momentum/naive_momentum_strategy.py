#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 17:12:09 2022

@author: zhangkexin
"""

"""
Implementation of naive momentum strategy
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

# we define a function for creating trading signals based on the number of consecutive days of prices increasing / decreasing
# we execute orders based on the days
def naive_momentum_strategy(data,consecutive_days):
    signals = pd.DataFrame(index = data.index)
    signals['orders'] = 0
    init = True # we use it for checking the first date
    prior_price = 0
    cons_day = 0
    
    for i in range(len(data['Adj Close'])):
        curr_price = data['Adj Close'][i]
        if init:
            # it is like
            # we set the first price as the threshold for checking
            # price increase and decrease
            prior_price = curr_price
            init = False # we updating the variable for checking the first data
        elif curr_price > prior_price:
            # once we see an increase in price,
            # even if there are consecutive days of price decrease
            # we reset it
            # because the previous decrease days don't meet the requirement for consecutive_days
            
            if cons_day < 0:
                cons_day = 0
            cons_day += 1
        elif curr_price < prior_price:
            # same logic for price decrease
            if cons_day > 0:
                cons_day = 0
            cons_day -= 1
        # we don't act when the curr_price is equal to prior_price
        if cons_day == consecutive_days:
            signals['orders'][i] = 1
        elif cons_day == -consecutive_days:
            signals['orders'][i] = -1
    
    return signals

# we want to check how our 'naive momentum' strategy works
# we use 5 days as the size of consecutive days
ts = naive_momentum_strategy(amzn_data,5)

# we visualize the data
fig = plt.figure()
ax1 = fig.add_subplot(111,ylabel = 'amzn price in $')
amzn_data['Adj Close'].plot(ax = ax1, color = 'k',lw = 1)
ax1.plot(ts.loc[ts.orders == 1.0].index, amzn_data['Adj Close'][ts.orders == 1.0],'^',markersize = 7,color = 'g')
ax1.plot(ts.loc[ts.orders == -1.0].index, amzn_data['Adj Close'][ts.orders == -1.0],'v',markersize = 7,color = 'r')

plt.legend(["Price","Buy","Sell"]) 
plt.title("Turtle Trading Strategy")
plt.show()
# well, we will see that we will trade only once if the window size is 5...