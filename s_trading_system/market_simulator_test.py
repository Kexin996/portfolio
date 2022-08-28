#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implementation of Unit testing of Market Simulator
"""

import unittest
from market_simulator import MarketSimulator

class TestMarketSimulator(unittest.TestCase):
    # initiate the setup function
    def setUp(self):
        self.market_simulator = MarketSimulator()
    
    # define a function to test whether the simulator can accept new orders from order manager
    def test_accept_new_orders(self):
        order1 = {
            'id':10,
            'price':200,
            'quantity':50,
            'side':'buy',
            'action':'New'}
        self.market_simulator.handle_order(order1)
        self.assertEqual(len(self.market_simulator.orders),1)
        self.assertEqual(self.market_simulator.orders[0]['status'],'accepted')
    
    # define a function to test whether the simulator can find out questionable orders
    def test_amend_new_orders(self):
        order1 = {
            'id':10,
            'price':200,
            'quantity':50,
            'side':'buy',
            'action':'Amend'}
        self.market_simulator.handle_order(order1)
        self.assertEqual(len(self.market_simulator.orders),0)


if __name__ == '__main__':
    unittest.main()
    
