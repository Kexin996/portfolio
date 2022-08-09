#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 18:02:31 2022

@author: zhangkexin
"""

"""
Implementation of Pairs Strategy
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn
from pandas_datareader import data
from statsmodels.tsa.stattools import coint

# we define the functions we need
def load_financial_data(symbols, start_date,end_date,output):
    try:
        df = pd.read_pickle(output)
    except FileNotFoundError:
        df = data.DataReader(symbols,'yahoo',start_date,end_date)
        df.to_pickle(output)
    return df

# we define a function for finding cointegrated pairs
def find_cointegrated_pairs(data):
    n = data.shape[1]
    pvalue_matrix = np.ones((n,n)) 
    keys = data.keys() # columns names
    pairs = []
    for i in range(n):
        for j in range(i+1,n):
            res = coint(data[keys[i]],data[keys[j]])
            # coint: return [coint)t,pvalue,crit_value]
            pvalue_matrix[i,j] = res[1]
            # we set the alpha to be 0.02
            if res[1] < 0.02:
                # we collect valid pairs
                pairs.append((keys[i],keys[j]))
    return pvalue_matrix, pairs

# we load many stocks to find the cointegrated pairs
# from 2000 to 2020
symbols = ['SPY','AAPL','ADBE','LUV','MSFT','SKYW','QCOM', 'HPQ','JNPR','AMD','IBM']
data = load_financial_data(symbols, '2000-01-01','2020-01-01','group_data.pkl')

# we find the pairs
pvalues,pairs = find_cointegrated_pairs(data['Adj Close']) # there is another matrix inside data['Adj Close']

# we use seaborn to visualize the heat map
# cmap: color of the map
# we use mask to hid the p values >= 0.98
seaborn.heatmap(pvalues,xticklabels = symbols, yticklabels = symbols, cmap = 'tab20c',mask = (pvalues >= 0.98))
                
            