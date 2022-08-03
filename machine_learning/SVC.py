#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 16:38:23 2022

@author: zhangkexin
"""

"""
Implementation of Support Vector Machine
"""
import pandas as pd
import numpy as np
import pandas_datareader as dr
import matplotlib.pyplot as plt
from sample import load_financial_data, create_classification_trading_condition, \
create_train_test_split_group, calculate_return, calculate_strategy_return, sharpe_ratio, plot_chart

# we import data first
# this time we use apple
aapl_data = load_financial_data('2000-01-01','2020-01-01','AAPL','aapl.pkl')

aapl_data,X,Y = create_classification_trading_condition(aapl_data)

X_train,X_test,Y_train,Y_test = create_train_test_split_group(X,Y)

# next, we fit the model
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

svc = SVC()
svc.fit(X_train,Y_train)

# we check the model performance through accuracy
accuracy_train = accuracy_score(Y_train, svc.predict(X_train))
print('Accuracy for training set:',accuracy_train)
accuracy_test = accuracy_score(Y_test, svc.predict(X_test))
print('Accuracy for testing set:',accuracy_test)

# we forecast the values
aapl_data['Predicted_Signal'] = svc.predict(X)
aapl_data['AAPL_Returns'] = np.log(aapl_data['Close'] / aapl_data['Close'].shift(1))

cum_aapl_return = calculate_return(aapl_data,len(X_train),'AAPL')
cum_aapl_strategy_return = calculate_strategy_return(aapl_data,len(X_train),'AAPL')

# we visualize the returns
plot_chart(cum_aapl_return,cum_aapl_strategy_return,'AAPL')

# our strategy returns don't beat the market
# we check sharpe ratio

print('Sharpe Ratio: ', sharpe_ratio(cum_aapl_return,cum_aapl_strategy_return))