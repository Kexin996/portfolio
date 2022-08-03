#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 15:04:51 2022

@author: zhangkexin
"""

"""
Example of L1 and L2 regularization
"""

import pandas as pd
import numpy as np
import pandas_datareader as dr
from sample import load_financial_data, create_regression_trading_condition, create_train_test_split_group

# we import data first
# this time we use tesla
tsla_data = load_financial_data('2010-01-01','2020-01-01','TSLA','tela.pkl')

tsla_data,X,Y = create_regression_trading_condition(tsla_data)

X_train,X_test,Y_train,Y_test =create_train_test_split_group(X,Y)

print(Y_train)
# now we use l1 regularization
from sklearn import linear_model
lasso = linear_model.Lasso(alpha = 0.1)
lasso.fit(X_train,Y_train)
print('Coefficients: \n', lasso.coef_)
# I don't understand why it is -0...
# maybe the value is just toooooo small...

# we take a look at L2
ridge = linear_model.Ridge(alpha=10000)
ridge.fit(X_train, Y_train)
# The coefficients
print('Coefficients: \n', ridge.coef_)