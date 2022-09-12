#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implementation of Cointegrated Augmented Dickey-Fuller Test (CADF) in
pairs trading
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas_datareader import data

# we use twenty years of history on adobe and microsoft
# we load the data first
try:
    data1 = pd.read_pickle('adbe.pkl')
    data2 = pd.read_pickle('msft.pkl')
except:
    data1 = data.DataReader('ADBE','yahoo','2000-01-01','2020-01-01')
    data1.to_pickle('adbe.pkl')
    
    data2 = data.DataReader('MSFT','yahoo','2000-01-01','2020-01-01')
    data2.to_pickle('msft.pkl')

# we visualize our data

plt.plot(data1['Adj Close'],label = 'adbe')
plt.plot(data2['Adj Close'],label = 'msft')
plt.legend()
plt.show()
df = pd.DataFrame(data1['Adj Close'].values,columns = ['adbe'],index = data1.index)
df = df.assign(msft = data2['Adj Close'].values)
print(df) 

# we are not sure about its cointegration
# thus, we draw the scatter graph
plt.scatter(df.adbe,df.msft)
plt.show()

# it seems that we can get a linear regression for adbe and msft
# we try it
import statsmodels.api as sm
model = sm.OLS(df.msft,df.adbe)
res = model.fit()
print(res.params)
print()
beta = res.params[0]

# from the parameters, we can see that the beta is 0.462263
# we calculate the residuals
df['residuals'] = df['msft'] - beta * df['adbe']
# we plot our residuals
plt.plot(df['residuals'])
plt.show()

# now we use adfuller to check its stationarity
import statsmodels.tsa.stattools as ts
# we use adfuller to check it by looking at the results from pprint
import pprint 
pprint.pprint(ts.adfuller(df['residuals']))
# from our adfuller test, the new series is indeed stationary



