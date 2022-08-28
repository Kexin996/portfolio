#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A unit testing on liquidity provider class
"""
import unittest
from liquidity_provider import LiquidityProvider

class test_liquidity_provider(unittest.TestCase):
    def setUp(self):
        self.liquidity_provider = LiquidityProvider([])
    
    def test_liquidity(self):
        self.liquidity_provider.generate_random_order()
        # we check for the details of the order
        # to see whether it is valid
        self.assertEqual(self.liquidity_provider.orders[0]['id'],0)
        self.assertEqual(self.liquidity_provider.orders[0]['side'],'ask')
        self.assertEqual(self.liquidity_provider.orders[0]['quantity'],700)
        self.assertEqual(self.liquidity_provider.orders[0]['price'],10) 
        # those numbers are randomly chosen
        # only to present how to unit test it
    
if __name__ == '__main__':
    unittest.main()