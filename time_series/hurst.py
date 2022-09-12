#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Use hurst exponent to test the stationarity of tesla stock price
"""

import numpy as np
import pandas as pd
from pandas_datareader import data
import matplotlib.pyplot as plt



# define a function to get hurst exponent
# note: the number of maximum periods will somewhat influence
# our conclusion
# which we will explore soon
def hurst_exponent(ts,max_periods = 20):
    # why lag starts at 2:
    # we gonna calculate the variance and mean
    # of the percantage changes in returns
    # and in python, np.std use (n-1) as denominator
    lags = range(2,max_periods) 
    
    # we calculate the difference for our poly fit
    lag_diff = [np.std(np.subtract(ts[lag:], ts[:-lag])) for lag in lags]
    # it will be the y value
    poly = np.polyfit(np.log(lags),np.log(lag_diff),1) # a linear relation
    
    # the specific steps for how to getting the linear relation
    # have been posted in a note in this folder
    return poly[0]

# first, we make several random function to check the hurst exponent
# np.random.rand(n): returns a n*n matrix consisting of values from standard
# normal distribution 

# sum them up with noise ---> random walk!
random_walk = np.log(np.cumsum(np.random.randn(10000))+100)
plt.plot(random_walk)
plt.show()

# check different parameters for hurst exponent
# we can see although they are slightly different
print('random walk:')
# they all around 0.5
for i in range(1,10):
    print(hurst_exponent(random_walk,i*10))
print()

# how about mean reverting and trending series?
# for values very close to 0, we will have mean-reversion
mean_reverting = np.random.randn(10000)
plt.plot(mean_reverting)
plt.show()
print('mean reverting:')
for i in range(1,10):
    print(hurst_exponent(mean_reverting,i*10))
print()
    
# for values > 0.5, we will have trend-following
trend_following = np.log(np.cumsum(np.random.randn(10000)+1))+1000# have a trend of 1
plt.plot(trend_following)
plt.show()

# we will find that with the trend, the hurst exponent converges to 0.6
# meaning that it is a trend-following series
print('trend following:')
for i in range(1,10):
    print(hurst_exponent(trend_following,i*10))
print()
    
# we use tesla stock price to see whether it is trend-following, random walk or mean-reverting
data = pd.read_pickle('tsla.pkl')
plt.plot(data['Adj Close'])
price = data['Adj Close']


# from the graph, it seems to be trend following
# we check hurst exponent
print('TSLA stock price:')
for i in range(1,10):
    # extract the value of pandas dataframrfor polyfit
    print(hurst_exponent(price.values,i*10)) 
print()

# from the result, we find it is close to mean-reverting
# for example, we can look at tsla stock exponent when lag = 500
print('TSLA stock price (lags = 500):')
print(hurst_exponent(price.values,500)) 
# as we increase the number of lags, the hurst exponent decreases
# the hurst exponent may change depending on the length of the period we have set

# By the way, when actually using it in market, 
# we may only look at only the 2 decimal numbers after the decimal points


