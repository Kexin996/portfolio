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
# %%
# we define a function for loading data
def load_financial_data(s_date,e_date,name,output_file):
    try:
        df = pd.read_pickle(output_file)
    except FileNotFoundError:
        df = dr.get_data_yahoo(name,s_date,e_date)
        df.to_pickle(output_file)
        
    return df

# we load the data from 2015 to 2020
# %%

# we see the head of the data
amzn_data = load_financial_data('2015-01-01','2020-01-01','AMZN','amzn.pkl')


# %%

# we define a simple classification signal for whether the price goes up or down
def create_classification_trading_condition(df):
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
    
    return X,Y

# %%
X,Y = create_classification_trading_condition(amzn_data)

# %%

# we define a regression condition function
def create_regression_trading_condition(df):
    # the only difference is how we define y
    df['Open-Close'] = df['Open']-df['Close']
    df['High-Low'] = df['High'] - df['Low']
    df = df.dropna() 
    X = df[['Open-Close','High-Low']]
    
    # if Y is positive, the close price goes up
    # if Y is negative, the close price goes down
    # if it is 0, the close price doesn't change
    # it catches both direction and magnitude
    Y = df['Close'].shift(-1)-df['Close']
    return X,Y
# %%
X,Y = create_regression_trading_condition(amzn_data)
# we can see the last value is NaN, as we have shifted by -1
print(Y)

# %%

# now we want to split the dataset into training and testing parts
from sklearn.model_selection import train_test_split

# we set the default split ratio to be 0.8
def create_train_test_split_group(X,Y,split_ratio = 0.8):
    # shuffle : randomly selecting data
    return train_test_split(X,Y,shuffle = False, train_size = split_ratio)

# %%

