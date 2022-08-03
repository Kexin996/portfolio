#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 16:08:30 2022

@author: zhangkexin
"""
"""
Implementation of KNN 
"""

import pandas as pd
import numpy as np
import pandas_datareader as dr
import matplotlib.pyplot as plt
from sample import load_financial_data, create_classification_trading_condition, \
create_train_test_split_group, calculate_return, calculate_strategy_return, sharpe_ratio, plot_chart

# we import data first
tsla_data = load_financial_data('2010-01-01','2020-01-01','TSLA','tela.pkl')

tsla_data,X,Y = create_classification_trading_condition(tsla_data)


X_train,X_test,Y_train,Y_test = create_train_test_split_group(X,Y)

# then, we use KNN and set neightbors number to 16
# since after trying different values, we can achieve rough 50% accuracy
# on testing set
from sklearn.neighbors import KNeighborsClassifier 
from sklearn.metrics import accuracy_score
knn = KNeighborsClassifier(n_neighbors=16)
# we fit the model
knn.fit(X_train,Y_train)

# we check the model performance through accuracy
accuracy_train = accuracy_score(Y_train, knn.predict(X_train))
print('Accuracy for training set:',accuracy_train)
accuracy_test = accuracy_score(Y_test, knn.predict(X_test))
print('Accuracy for testing set:',accuracy_test)

# after that, we just create the predicted signal
tsla_data['Predicted_Signal'] = knn.predict(X)
tsla_data['TSLA_Returns'] = np.log(tsla_data['Close'] / tsla_data['Close'].shift(1))

# and we compare the strategy performance with the market
cum_tsla_return = calculate_return(tsla_data,len(X_train),'TSLA')
cum_strategy_return = calculate_strategy_return(tsla_data,len(X_train),'TSLA')

plot_chart(cum_tsla_return,cum_strategy_return,'TSLA')

# it is quite interesting to see that my strategy return beats the market !!!
# the sharpe ratio is more than 31.5 ---> which is gotten by 3 times 0.5
print('Sharpe Ratio: ', sharpe_ratio(cum_tsla_return,cum_strategy_return))