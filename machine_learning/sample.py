#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 10:16:54 2022

@author: zhangkexin
"""

"""
simple machine learning in finance
"""
import pandas as pd
import numpy as np
import pandas_datareader as dr
import matplotlib.pyplot as plt
# %%
# we define a function for loading data
def load_financial_data(s_date,e_date,name,output_file):
    try:
        df = pd.read_pickle(output_file)
    except FileNotFoundError:
        df = dr.get_data_yahoo(name,s_date,e_date)
        df.to_pickle(output_file)
        
    return df

# %%

# we define a simple classification signal for whether the price goes up or down
def create_classification_trading_condition(df):
    # it is no inplace, so we need to returnm a new dataframre
    df['Open-Close'] = df['Open']-df['Close']
    df['High-Low'] = df['High'] - df['Low']
    
    df = df.dropna() # we drop out the nan value
    # the default for dropna() is dropping row
    
    X = df[['Open-Close','High-Low']]
    # we shift close to the 0 by 1
    # we are checking whether yesterday's close price is higher than today's close price
    # if so,y is 1
    # else, we use -1
    Y = np.where(df['Close'].shift(-1)>df['Close'], 1,-1)
    df['Target'] = Y
    
    return df,X,Y


# %%

# we define a regression condition function
def create_regression_trading_condition(df):
    
    # the only difference is how we define y
    df['Open-Close'] = df['Open']-df['Close'] 
    # it is no inplace, so we need to returnm a new dataframre
    df['High-Low'] = df['High'] - df['Low']
    df['Target'] = df['Close'].shift(-1)-df['Close']
    df = df.dropna()
    X = df[['Open-Close','High-Low']]
    
    # if Y is positive, the close price goes up
    # if Y is negative, the close price goes down
    # if it is 0, the close price doesn't change
    # it catches both direction and magnitude
    # we can see the last value is NaN, as we have shifted by -1
 
    Y = df['Target']
    
    return df,X,Y
    

# %%

# now we want to split the dataset into training and testing parts
from sklearn.model_selection import train_test_split

# we set the default split ratio to be 0.8
def create_train_test_split_group(X,Y,split_ratio = 0.8):
    # shuffle : randomly selecting data
    return train_test_split(X,Y,shuffle = False, train_size = split_ratio)

# %%
# define a function for calculating return without strategy
def calculate_return(df,split_value,symbol):
    cum_return = df[split_value:]['%s_Returns'%symbol].cumsum()*100
    # we just do some preparations for strategy return
    # for preidct_signal, since we want to predict tomorrow
    # we also shift it by 1
    df['Strategy_Returns'] = df[split_value:]['%s_Returns'%symbol]*df['Predicted_Signal'].shift(1)
    return cum_return

# define a functin for calculating strategy return
def calculate_strategy_return(df,split_value,symbol):
    cum_strategy_return = df[split_value:]['Strategy_Returns'].cumsum()*100
    return cum_strategy_return

# we plot our strategy return
def plot_chart(cum_return, cum_strategy_return,symbol):
    plt.figure(figsize=(10,5)) # set up figure's size
    plt.plot(cum_return,label = "%s Returns"%symbol)
    plt.plot(cum_strategy_return, label = '%s Strategy Return'%symbol)
    plt.legend()

# %%
# we define a function for checking the sharpe ratio
def sharpe_ratio(returns, strategy_returns):
    strategy_std = strategy_returns.std()
    sharpe = (strategy_returns - returns) / strategy_std
    return sharpe.mean() # we use mean since we are looking at expected values
