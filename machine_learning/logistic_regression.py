#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 16:47:51 2022

@author: zhangkexin
"""

"""
Implementation of Logistic regression
"""

import pandas as pd
import numpy as np
import pandas_datareader as dr
import matplotlib.pyplot as plt
from sample import load_financial_data, create_classification_trading_condition, \
create_train_test_split_group, calculate_return, calculate_strategy_return, sharpe_ratio, plot_chart

# we import data first
# we still use apple
aapl_data = load_financial_data('2000-01-01','2020-01-01','AAPL','aapl.pkl')

aapl_data,X,Y = create_classification_trading_condition(aapl_data)

X_train,X_test,Y_train,Y_test = create_train_test_split_group(X,Y)

# we fit the model
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
# for convenience, we just use the default parameters
log = LogisticRegression()
log.fit(X_train,Y_train)

# we check the model performance through accuracy
accuracy_train = accuracy_score(Y_train, log.predict(X_train))
print('Accuracy for training set:',accuracy_train)
accuracy_test = accuracy_score(Y_test, log.predict(X_test))
print('Accuracy for testing set:',accuracy_test)
# it seems that logistic regression performs slightly better than svc in testing set

# we forecast the values
# we forecast the values
aapl_data['Predicted_Signal'] = log.predict(X)
aapl_data['AAPL_Returns'] = np.log(aapl_data['Close'] / aapl_data['Close'].shift(1))

cum_aapl_return = calculate_return(aapl_data,len(X_train),'AAPL')
cum_aapl_strategy_return = calculate_strategy_return(aapl_data,len(X_train),'AAPL')

# we visualize the returns
plot_chart(cum_aapl_return,cum_aapl_strategy_return,'AAPL')

# our strategy returns don't beat the market, but it is better than svc from the graph
# we check sharpe ratio
print('Sharpe Ratio: ', sharpe_ratio(cum_aapl_return,cum_aapl_strategy_return))

# from sharpe ratio, we see that indeed, logistic regression outperforms svc
# for apple's stocks