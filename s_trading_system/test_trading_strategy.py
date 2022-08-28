#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inplemention of a unit testing of a simple arbitrage trading strategy
"""

import unittest
from trading_strategy import TradingStrategy

class TestStrategy(unittest.TestCase):
    def setUp(self): # we use it for our unit testing
    # this function will be called before we make the first test
        self.trading_strategy = TradingStrategy()
    
    # we create an arbitrary book event to test the reception of book event trading strategy
    def test_receive_book_event(self):
        book_event = {
            'bid_price':12,
            'bid_quantity':100,
            'ask_price':10,
            'ask_quantity':125}
        # we begin our testing...
        self.trading_strategy.handle_book_event(book_event)
        self.assertEqual(len(self.trading_strategy.orders),2)
        self.assertEqual(self.trading_strategy.orders[0]['side'],'bid') # we insert sell order first
        self.assertEqual(self.trading_strategy.orders[1]['side'],'ask')
        self.assertEqual(self.trading_strategy.orders[0]['price'],12)
        self.assertEqual(self.trading_strategy.orders[1]['price'],10)
        self.assertEqual(self.trading_strategy.current_bid, 12)
        self.assertEqual(self.trading_strategy.current_ask, 10)
        self.assertEqual(self.trading_strategy.orders[0]['quantity'],100)
        self.assertEqual(self.trading_strategy.orders[1]['quantity'],100)
        self.assertEqual(self.trading_strategy.orders[0]['action'], 'no_action')
        self.assertEqual(self.trading_strategy.orders[1]['action'], 'no_action')
    
    # we test the rejected order part in our trading strategy
    def test_rejected_order(self):
        self.test_receive_book_event()
        order_execution = { # receive order from order management
            'id':1,
            'price':12,
            'quantity':100,
            'side':'ask',
            'status':'rejected'}
        
        self.trading_strategy.handle_market_response(order_execution)
        self.assertEqual(self.trading_strategy.orders[0]['side'],'ask') # we deque the first sell order
        self.assertEqual(self.trading_strategy.orders[0]['price'],10)
        self.assertEqual(self.trading_strategy.orders[0]['quantity'], 100) 
        self.assertEqual(self.trading_strategy.orders[0]['status'], 'new')
    
    # we test on filled orders
    def test_filled_order(self):
        self.test_receive_book_event()
        order_execution = { 
            # receive order from order management
            'id':1,
            'price':12,
            'quantity':100,
            'side':'bid',
            'status':'filled'}
        self.trading_strategy.handle_market_response(order_execution)
        self.assertEqual(len(self.trading_strategy.orders),1)
        
        order_execution = { 
            # receive order from order management
            'id':2,
            'price':10,
            'quantity':100,
            'side':'ask',
            'status':'filled'}
        self.trading_strategy.handle_market_response(order_execution)
        self.assertEqual(self.trading_strategy.position, 0)
        self.assertEqual(self.trading_strategy.cash, 10200)
        self.assertEqual(self.trading_strategy.pnls, 200)
        
        
    
if __name__ == '__main__':
    unittest.main() # all three tests are passed
        
        
    
    