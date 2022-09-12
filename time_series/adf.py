#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Use Augmented Dickey-Fuller Test to check whether Tesla stock price is a random walk
"""

from pandas_datareader import data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller

# we download the data first
try:
    data = pd.read_pickle('tsla.pkl')
except:
    data = data.DataReader('TSLA','yahoo',start = '2010-01-01',end = '2020-01-01')
    data.to_pickle('tsla.pkl')

# we check the data we download
plt.plot(data['Adj Close'])

# since the test statistics returned is a negative number
# for the critival interval values, the test statistics results
# have to be smaller to reject the null hypothesis (gemma = 0)

# we use lag value of 1 for historical financial data
adf = adfuller(data['Adj Close'],1)

# we use python data prettier printer to check it
from pprint import pprint
pprint(adf)

# the first value is the test statistics
# the second value is the p-value
# combining them and 
# through checking the test statistics at different criticl values
# we find that we fail to reject the null hypothesis
# that is, the time series is a random walk!