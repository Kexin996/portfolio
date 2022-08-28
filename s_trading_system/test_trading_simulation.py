#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A unit testing on a real trading by incorporating all the 5 classes
"""

import unittest
from liquidity_provider import LiquidityProvider
from trading_strategy import TradingStrategy
from order_manager import OrderManager
from market_simulator import MarketSimulator
from order_book import OrderBook
from collections import deque # we use deque for speed

class TestTradingSimulation(unittest.TestCase):
    # initiate a setup function
    def setUp(self):
        self.lp_2_gateway = deque()
        
        self.ob_2_ts = deque()
        
        self.om_2_ts = deque()
        self.ts_2_om = deque()
        
        self.gw_2_om = deque()
        self.om_2_gw = deque()
        
        # initialize the class
        self.lp = LiquidityProvider(self.lp_2_gateway)
        self.ob = OrderBook(self.lp_2_gateway,self.ob_2_ts)
        self.ts = TradingStrategy(self.ob_2_ts,self.ts_2_om,self.om_2_ts)
        self.ms = MarketSimulator(self.om_2_gw,self.gw_2_om)
        self.om = OrderManager(self.ts_2_om,self.om_2_ts,self.om_2_gw,self.gw_2_om)
    
    # we test whether our strategy can make an arbitrage between 2 orders
    def test_arbitrage(self):
        order1= {
            'id':1,
            'price':220,
            'quantity':10,
            'side':'bid',
            'action':'new'
            }
        # check for liquidity provider
        self.lp.insert_manual_order(order1)
        self.assertEqual(len(self.lp_2_gateway),1)
        
        # check for order book
        self.ob.handle_order_from_gateway()
        self.assertEqual(len(self.ob_2_ts),1)
        
        # check for trading strategy
        self.ts.handle_input_from_ob()
        self.assertEqual(len(self.ts_2_om),0)
        
        # that works well. 
        # then, we check for the situation when we add an ask price
        order2= {
            'id':2,
            'price':215,
            'quantity':10,
            'side':'ask',
            'action':'new'
            }
        # check for liquidity provider
        self.lp.insert_manual_order(order2)
        self.assertEqual(len(self.lp_2_gateway),1)
        
        # check for order book
        self.ob.handle_order_from_gateway()
        self.assertEqual(len(self.ob_2_ts),1)
        
        # check for trading strategy
        self.ts.handle_input_from_ob()
        self.assertEqual(len(self.ts_2_om),2)
        
        # we check for order manager
        self.om.handle_input_from_ts()
        self.assertEqual(len(self.ts_2_om),1)
        self.assertEqual(len(self.om_2_gw),1)
        self.om.handle_input_from_ts()
        self.assertEqual(len(self.ts_2_om),0)
        self.assertEqual(len(self.om_2_gw),2)
        
        # we check for our market simulator
        self.ms.handle_order_from_om()
        self.assertEqual(len(self.gw_2_om),1)
        self.ms.handle_order_from_om()
        self.assertEqual(len(self.gw_2_om),2)
        
        # we check how order manager handle the orders back from market
        self.om.handle_input_from_market()
        self.om.handle_input_from_market()
        self.assertEqual(len(self.om_2_ts),2)
        
        # we check how trading strategy handle the orders back from order manager
        self.ts.handle_response_from_om()
        self.assertEqual(self.ts.get_pnls(),0)
        
        # zero value PnLs, since no order has been filled
        # now we fill all orders in market simulator
        self.ms.fill_all_orders()
        self.assertEqual(len(self.gw_2_om),2)
        
        # we check how order manager handle the orders back from market
        self.om.handle_input_from_market()
        self.om.handle_input_from_market()
        self.assertEqual(len(self.om_2_ts),3) 
        # why it is 3 here: 
        # the trading strategy only handles one response 
        # there is 1 left in om_2_ts
        
        # we check our how our trading strategy handles the three feedbacks from order manager
        self.ts.handle_response_from_om() 
        # this earliest order doesn't influence PnLs, 
        # as it is not filled
        self.assertEqual(self.ts.get_pnls(),0)
        
        # we check the PnLs brought by the two filled orders
        self.assertEqual(len(self.om_2_ts),2) 
        self.ts.handle_response_from_om()
        self.assertEqual(len(self.om_2_ts),1) 
        self.ts.handle_response_from_om()
        self.assertEqual(len(self.om_2_ts),0) 
        
        # then we check PnLs in our trading strategy
        # it should be 50, since (220-215) * 10 = 50
        self.assertEqual(self.ts.get_pnls(),50)
        

if __name__ == '__main__':
    unittest.main()
