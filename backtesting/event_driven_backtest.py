#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implementation of an event driven backtest system on a dual moving average strategy
"""

import sys
import os
import pandas as pd
from pandas_datareader import data
import matplotlib.pyplot as plt
import h5py
from dual_moving_strategy import TradingDualMA # import our trading stratgy

# we import the demo of trading system
sys.path.insert(0,'/Users/zhangkexin/Desktop/portfolio/s_trading_system'
) # we insert the folder we need at the top

from liquidity_provider import LiquidityProvider
from order_manager import OrderManager
from market_simulator import MarketSimulator
from order_book import OrderBook
from collections import deque # we use deque for speed

# define a function to call another function continuously 
# as the deque is not empty
def call_if_not_empty(deq, func):
    while len(deq) > 0:
        func()
    # we use it for processing new coming orders

# create a event based backtester
class EventBasedBackTester:
    # initiate it
    def __init__(self):
        # this is the same as the framework in the trading simulation file
        self.lp_2_gateway = deque()
        self.ob_2_ts = deque()
        self.om_2_ts = deque()
        self.ts_2_om = deque()
        self.om_2_gw = deque()
        self.gw_2_om = deque()
    
        self.lp = LiquidityProvider(self.lp_2_gateway)
        self.ob = OrderBook(self.lp_2_gateway,self.ob_2_ts)
        self.ts = TradingDualMA(self.ob_2_ts,self.ts_2_om,self.om_2_ts)
        self.ms = MarketSimulator(self.om_2_gw,self.gw_2_om)
        self.om = OrderManager(self.ts_2_om,self.om_2_ts,self.om_2_gw,self.gw_2_om)\
    
    # create a function to convert the incoming data
    # to something our system can read.
    # in the following, we just mimic a group of incoming immediate or cancel orders
    def process_data(self,price):
        # we set the amount of stocks to be 1000
        # for simplicity, we set the bid,ask orders to have the same price
        # also, we need to have signals to trade
        # so we create two orders
        order_bid = {
            'id':1,
            'price':price,
            'quantity':1000,
            'side':'bid',
            'action':'new'}
        order_ask = {
            'id':2,
            'price':price,
            'quantity':1000,
            'side':'ask',
            'action':'new'}
        # we mimic the process of adding new orders from liquidity provider to order book
        self.lp_2_gateway.append(order_ask) # we begin with ask, since we don't care about short selling
        self.lp_2_gateway.append(order_bid)
        self.process_events() # check the events
        # we need to delete the orders that are not filled
        # e.g. 10% orders are filled, and we need to delete the rest of the 90%
        order_ask['action'] = 'delete'
        order_bid['action'] = 'delete'
        self.lp_2_gateway.append(order_ask) 
        self.lp_2_gateway.append(order_bid) #
        
    
    # define a function to deal with the new events
    def process_events(self):
        while len(self.lp_2_gateway)>0: # as long as we have new orders
            call_if_not_empty(self.lp_2_gateway,self.ob.handle_order_from_gateway) # order book
            call_if_not_empty(self.ob_2_ts,self.ts.handle_input_from_ob) # trading strategy
            call_if_not_empty(self.ts_2_om,self.om.handle_input_from_ts) # order manager
            call_if_not_empty(self.om_2_gw,self.ms.handle_order_from_om) # market simulater
            self.ms.fill_all_orders(10) # try change it from 100 to 10
            call_if_not_empty(self.gw_2_om,self.om.handle_input_from_market) # come back of order manager
            call_if_not_empty(self.om_2_ts,self.ts.handle_response_from_om) # trading strategy handles response from market

# now we use amazon stocks to test it
backtester = EventBasedBackTester()

# load data
def load_financial_data(start_date,end_date,output_file):
    try:
        df = pd.read_pickle(output_file)
    except FileNotFoundError:
        df = data.DataReader('AMZN','yahoo',start_date,end_date)
        df.to_pickle(output_file)
    return df

amzn_data = load_financial_data(start_date = '2000-01-01',end_date = '2020-01-01',output_file = 'amzn.pkl')

for i in zip(amzn_data.index,amzn_data['Adj Close']):
    date = i[0]
    price = i[1]
    price_info = {'date':date,'price':price}
    backtester.process_data(price_info['price'])
    backtester.process_events() # clean deleted orders
    # we process_data

# we plot the data
plt.figure(figsize = (12,8))
plt.plot(backtester.ts.list_total,label = 'total')
plt.show()
plt.plot(backtester.ts.list_cash, label = 'Cash')
plt.show()

# it is quite interesting to see 
# if only 10% orders are filled
# we will earn a lot
# but if all the orders are filled
# we will lose.
    
