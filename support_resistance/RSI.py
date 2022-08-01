#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 12:16:20 2022

@author: zhangkexin
"""

"""
Implementation of relative strength indicator
"""
import pandas as pd
data = pd.read_pickle('amzn.pkl')
close = data['Adj Close']

# we still use 20 days for convenience
n = 20 
# we use some variables to store data for later visualization
gain_history = []
loss_history = []

