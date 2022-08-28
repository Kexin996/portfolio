#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit testing for the limit order book
"""

import unittest
from order_book import OrderBook

class TestOrderBook(unittest.TestCase):
    # define setUp function
    def setUp(self):
        self.order_book = OrderBook()
    
    # test the limit book's ability to receive new orders
    # and sort them in the correct orders
    def test_handlenew(self):
        # test for bid
        order1 = {
            'id':1,
            'price':200,
            'quantity':20,
            'side':'bid',
            'action':'new'
            }
        self.order_book.handle_order(order1)
        
        order2 = order1.copy()
        order2['id'] = 2
        order2['price'] = 204
        self.order_book.handle_order(order2)
    
        order3 = order1.copy()
        order3['id'] = 3
        order3['price'] = 203
        self.order_book.handle_order(order3)
        
        # test for ask
        order4 = order1.copy()
        order4['side'] = 'buy'
        order4['id'] = 4
        self.order_book.handle_order(order4)
        
        order5 = order4.copy()
        order5['id'] = 5
        order5['price'] = 205
        self.order_book.handle_order(order5)
        
        order6 = order4.copy()
        order6['id'] = 6
        order6['price'] = 206
        self.order_book.handle_order(order6)
        
        # check for bid list
        self.assertEqual(self.order_book.list_bids[0]['id'],2)
        self.assertEqual(self.order_book.list_bids[1]['id'],3)
        self.assertEqual(self.order_book.list_bids[2]['id'],1)
        
        # check for ask list
        self.assertEqual(self.order_book.list_asks[0]['id'],4)
        self.assertEqual(self.order_book.list_asks[1]['id'],5)
        self.assertEqual(self.order_book.list_asks[2]['id'],6)
    
    # then we check the order book's ability in modifying orders
    def test_handlemodify(self):
        self.test_handlenew()
        order={
            'id':2,
            'quantity':10,
            'action':'modify'
            }
        self.order_book.handle_order(order)
        
        # we only update for smaller amount of orders
        self.assertEqual(self.order_book.list_bids[0]['id'],2)
        self.assertEqual(self.order_book.list_bids[0]['quantity'],10)
    
    # check for the order oook's ability to remove orders
    def test_handleremove(self):
        self.test_handlenew()
        order = {
            'id':2,
            'action':'delete'
            }
        self.order_book.handle_order(order)
        
        self.assertEqual(self.order_book.list_bids[0]['id'],3)
    
    # check for the order book's ability to generate book event
    def test_generate_book_event(self):
        # we check the book event for inserting a bid order into the bid_lists
        order = {
            'id':1,
            'price':210,
            'quantity':10,
            'side':'bid',
            'action':'new'
            }
        self.assertEqual(self.order_book.handle_order(order),{'bid_price':210,'bid_quantity':10,'ask_price':-1,'ask_quantity':-1})
        
        
        # we check the book event for inserting a ask order into the ask_lists
        order2 = order.copy()
        order2['id'] = 2
        order2['price'] = 215
        order2['side'] = 'ask'
        self.assertEqual(self.order_book.handle_order(order2),{'bid_price':210,'bid_quantity':10,'ask_price':215,'ask_quantity':10})
        
        
if __name__ == '__main__':
    unittest.main()