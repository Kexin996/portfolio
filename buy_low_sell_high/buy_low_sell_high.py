"""
A simple trading strategy
we will get the data by using DataReader.
Documentation: https://pydata.github.io/pandas-datareader/
"""


import pandas_datareader.data as web
import pandas as pd
import numpy as np
import datetime as dt

start_date = "2016-07-29"
end_data = "2022-07-28"

# we want to see all the columns of the dataset
# none: just show all the columns
# that also works for display.max_rows
pd.set_option('display.max_columns', None)

# we just load the history data of Amazon
data = web.DataReader('AMZN','yahoo',start_date,end_data)

'''
adj close: the closing price of the stock that adjusts the price of the stock for corporate actions
e.g. stock splits / dividends
'''

print(data)
print()


amzn_data_signal = pd.DataFrame(index = data.index)  # we want to copy the row number
amzn_data_signal['Price'] = data['Adj Close']

print(amzn_data_signal)
print()

# since we buy low, sell high, we want to set a daily difference for us to buy low and sell high
# the daily difference will be the difference between adj prices in two consecutive days

amzn_data_signal['Daily Difference'] = amzn_data_signal['Price'].diff() # the default for peroids is 1
print(amzn_data_signal.head())
print()


'''
we set:
    signal = 0 ---> we want to buy the stocks, 
    where the difference is negative(today's price is lower than previous day)
    
    signal = 1 ---> we want to sell the stocks,
    where the difference is positive (today's price is higher than previous day')
    
    
                                    
'''
amzn_data_signal['Signal'] = 0.0
# np.where's parameters: condition, x (if true), y (if false)
amzn_data_signal['Signal'] = np.where(amzn_data_signal['Daily Difference']> 0,1.0,0.0)
print(amzn_data_signal.head())
print()


# we don't want to continuously buy / sell if the trend keeps going down / going up
# thus, just set a restriction about our current positions
# that is, we can only sell when we have the stocks
# we just use a simple method: we don't want to buy consecutively for two days / sell consecutively for two days
# we only buy at positions = 1 and sell it at positions = -1

# Note: it is not definite to earn profits
# e.g. if we buy at 152.593994 on 2020-07-30, the signal is 1 ---> we buy it
# but if on 2020-08-03, the price becomes 150, the difference isnegative, and signal is 0 ---> we sell it
# we lose money 

amzn_data_signal['positions'] = amzn_data_signal['Signal'].diff()
print(amzn_data_signal.head())

# aftering creating the signals, we want to visualize our profits
import matplotlib.pyplot as plt

fig = plt.figure()
# parameters:
# 111: 
# first 1 and second 1: size of the whole big image
# last 1: the index of the graph
ax1 = fig.add_subplot(111,ylabel = 'Price in $')

# then, we plot the price in black
# lw: linewidth
amzn_data_signal['Price'].plot(ax = ax1, color = '0', lw = 2)

# now, we draw an up arrow showing that we buy one share of stocks

# plot(x, y)     
# loc: using labels to locate
# iloc: use index to locate

# what it does:
# we first find out all the date where the position signal is 1 
# then, we find out the corresponding y value and use '^' to show them in red
ax1.plot(amzn_data_signal.loc[amzn_data_signal.positions == 1.0].index,amzn_data_signal.Price[amzn_data_signal.positions == 1.0],'^',markersize=5, color='r')

# now, we draw a down arrow showing that we short one share of stocks
ax1.plot(amzn_data_signal.loc[amzn_data_signal.positions == -1.0].index, amzn_data_signal.Price[amzn_data_signal.positions == -1.0],'v',markersize = 5, color = 'g')

# suppose we just invest $1,000
initial_capital = 1000.0

# create a data frame for the position and portfolio
positions = pd.DataFrame(index = amzn_data_signal.index).fillna(0.0) # for the nan date
portfolio = pd.DataFrame(index = amzn_data_signal.index).fillna(0.0)

# store positions
positions['amzn'] = amzn_data_signal['Signal']

# store amount of positions
portfolio['positions'] = positions.multiply(amzn_data_signal['Price'],axis = 0)

# store the cash we have
portfolio['cash'] = initial_capital - (positions.diff().multiply(amzn_data_signal['Price'],axis = 0)).cumsum()

portfolio['total'] = portfolio['cash']+portfolio['positions']
print(portfolio['total'])

# seeing the graph, we notice that our strategy is actually profitable
portfolio.plot()
plt.show()









