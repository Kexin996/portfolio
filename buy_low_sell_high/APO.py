#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 23:30:25 2022

@author: zhangkexin
"""

"""
Absolute Price Oscillator
"""
n_fast = 10 # we want the fast EMA to be 10 days window size
n_slow = 40  # slow EMA to be 40 days
K_fast = 2/ (n_fast+1)
K_slow = 2 / (n_slow+1)
ema_fast = 0
ema_slow = 0
