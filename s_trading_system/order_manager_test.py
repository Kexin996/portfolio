#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit Testing file for Order Manager
"""
import unittest
from order_manager import OrderManager

class TestOrderManager(unittest.TestCase):
    # we define our set up function
    def setUp(self):
        self.order_manager = OrderManager()

    # first, we test whether our order manager can receive orders from trading strategy
    def test_order_from_trading_strategy(self):
        # we just create an arbitrary order to test it
        order1= {
            'id':10,
            'price':200,
            'quantity':10,
            'side':'buy'
            }
        self.order_manager.handle_order_from_trading_strategy(order1)
        self.assertEqual(len(self.order_manager.orders),1)
        
        self.order_manager.handle_order_from_trading_strategy(order1)
        self.assertEqual(len(self.order_manager.orders),2)
        self.assertEqual(self.order_manager.orders[0]['id'],1)
        self.assertEqual(self.order_manager.orders[1]['id'],2)

    # test whether our order manager can check error
    def test_order_from_trading_strategy_error(self):
        order1= {
            'id':10,
            'price':-200,
            'quantity':10,
            'side':'buy'
            }
        self.order_manager.handle_order_from_trading_strategy(order1)
        self.assertEqual(len(self.order_manager.orders),0)
        
        order2= {
            'id':10,
            'price':200,
            'quantity':-10,
            'side':'buy'
            }
        self.order_manager.handle_order_from_trading_strategy(order2)
        self.assertEqual(len(self.order_manager.orders),0)

    # test whether order manager can receive fill order
    def test_order_from_gateway_filled(self):
        self.test_order_from_trading_strategy()
        order_filled={
            'id':2,
            'price':200,
            'quantity':10,
            'side':'buy',
            'status':'filled'
            }
        self.order_manager.handle_order_from_gateway(order_filled)
        self.assertEqual(len(self.order_manager.orders),1)
        
    # test for non-filled order, whether we will update order status or not
    def test_order_from_gateway_acked(self):
        self.test_order_from_trading_strategy()
        order_filled={
            'id':2,
            'price':200,
            'quantity':10,
            'side':'buy',
            'status':'acked'
            }
        self.order_manager.handle_order_from_gateway(order_filled)
        self.assertEqual(len(self.order_manager.orders),2)
        self.assertEqual(self.order_manager.orders[1]['status'],'acked')
        
    
    # 
# we do the unit testing
if __name__ == '__main__':
    unittest.main()
        
