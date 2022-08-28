#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A simple liquidity provider class
Only for sample purpose
"""

from random import randrange
from random import sample, seed # we use random module to mimic an actual liquidity provider (e.g. an exchange)

class LiquidityProvider:
    
    def __init__(self,lp_2_gateway = None): # lp_2_gateway: liquidity provider to gateway
        self.orders = [] # a list of dictionaries(individual order)
        self.order_id = 0 # the id of the last order
        seed(7) # we define the random seed for unit testing purpose
        self.lp_2_gateway = lp_2_gateway # also a list
    
    # lookup_order(self,id): check whether the order exists in our current orders
    def lookup_order(self,id):
        count = 0
        for o in self.orders:
            if o['id'] == id:
                return o,count # if we have found the order, we return it and its id
            count += 1
            
        return None,None
    
    # insert_manual_order(self,order): insert order manually
    # unit testing purpose
    def insert_manual_order(self,order):
        if self.lp_2_gateway == None:
            print('SIMULATION MODE') # unit testing purpose
            return order

        # manually insert the order
        self.lp_2_gateway.append(order) # update the orders to order book
    
    # generate_random_order: 
    # there are three modes: new / modify / delete
    def generate_random_order(self):
        price = randrange(8,12) # randomly produces a price in [8,12)
        side = sample(['ask','bid'],1)[0] # this method returns a list of length 1, either buy or sell
        quantity = randrange(1,10)*100 # a quantity in [100,900]
        order_id = randrange(0,self.order_id+1) # randomly produces a valid id
        o,_ = self.lookup_order(order_id)
        
        new_order = False # we use it to check whether we are creating a new order
        # or we modify / delete an existing order
        if o is None: # 'is': checks whether two variables are the same object
            new_order = True
            action = 'new'
        else:
            action = sample(['modify','delete'],1)[0]
        
        # we create the order dictionary
        ord = {
            'id':order_id,
            'price':price,
            'quantity':quantity,
            'side':side,
            'action':action
            }
        
        # check whether it is a new order
        if not new_order:
            self.order_id += 1
            self.orders.append(ord)
        
        # we use it for unit testing case
        if not self.lp_2_gateway:
            print('SIMULATION MODE') # unit testing purpose
            self.orders.append(ord)
            return ord
        
        self.lp_2_gateway.append(ord.copy()) # we update our gateway since we have new actions
        
        
            
            
    
    
        


    
