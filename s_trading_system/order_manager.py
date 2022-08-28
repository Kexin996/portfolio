#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implementation of Order Manager
"""

# order manager: collects the orders from all trading strategies 
# and communicate this order with the market

class OrderManager:
    # initialize order manager
    def __init__(self,ts_2_om = None,om_2_ts = None,om_2_gw = None,gw_2_om = None):
        self.orders = []
        self.id = 0
        self.ts_2_om = ts_2_om
        self.om_2_ts = om_2_ts
        self.om_2_gw = om_2_gw
        self.gw_2_om = gw_2_om
        
    # check input from trading strategy
    def handle_input_from_ts(self):
        if self.ts_2_om is None: # that means we ar in unit test 
            print('simulation mode')
        else:
            if len(self.ts_2_om) > 0:
                # else, we receive the order 
                # we define  new function to handle this order
                self.handle_order_from_trading_strategy(self.ts_2_om.popleft())
    
    def handle_order_from_trading_strategy(self,order_sent):
        # we check whether the order sent from trading strategy is valid
        if self.check_order_valid(order_sent):
            # if it, we append it to our current orders
            order = self.create_new_order(order_sent).copy()
            self.orders.append(order)
            # we check whether we could send the order to market 
            if self.om_2_gw is None:
                print('simulation mode')
            else:
                self.om_2_gw.append(order.copy())
    
    # define a function to handle order from market
    def handle_input_from_market(self):
        if self.gw_2_om is None: # that means we ar in unit test 
            print('simulation mode')
        else:
            if len(self.gw_2_om) > 0:
                # else, we receive the order from market
                # we define new function to handle this order
                self.handle_order_from_gateway(self.gw_2_om.popleft())
    
    def handle_order_from_gateway(self,order_sent):
        # for this function, we need to chec whether the market reaction is valid
        # that is, whether the order sent by the market has alreay exists in the orders from trading strategy
        # if not, there is an error
        order = self.look_up_order_by_id(order_sent['id'],order_sent['price'])
        if order is None: # we have an error
            print('Error: order not found.')
        else:
            order['status'] = order_sent['status'] # we update order status
            # and we send it back to trading strategy
            if self.om_2_ts is None: # unit testing
                print('simulation mode')
            else: # we send it to trading strategy
                self.om_2_ts.append(order.copy())
            self.clean_traded_orders() # we clean the order if it is filled
    
    # define a function to check whether the order is valid
    def check_order_valid(self,order):
        # we return True only for orders with positive amounts and positive prices
        if order['quantity'] < 0 or order['price'] < 0:
            return False
        return True # return true for valid order
    
    # define a function to create new order
    def create_new_order(self,order_received):
        # we update the id
        self.id += 1
        order = {
            'id':self.id,
            'price':order_received['price'],
            'quantity':order_received['quantity'],
            'side':order_received['side'],
            'status':'new',
            'action':'new'} # the status and action show that the order is newly created
        return order
    
    # define a function to look up order in current order management orders
    def look_up_order_by_id(self,id,price):
        for o in self.orders:
            if o['id'] == id and o['price'] == price: # return order if we have found it
                return o
        return None
    
    # define a function to clean the orders that have been already traded
    def clean_traded_orders(self):
        order_removed = []
        for i in range(len(self.orders)):
            if self.orders[i]['status'] == 'filled': # we have filed the trade, so we delete it from our current order list
                order_removed.append(i)
            
        # we remove the traded orders by their index
        for k in sorted(order_removed,reverse = True):
            # we need to use reverse order, since
            # we don't want deletion in the beginning to influence other orders'index
            del(self.orders[k])
        
            
    
    
        

