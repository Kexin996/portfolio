#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implementation of a strategy using 'buy low, sell high' arbitrage
"""

"""
Idea: when the top of the order book is crossed, we execute an order
"""

class TradingStrategy:
    def __init__(self,ob_2_ts = None,ts_2_om = None,om_2_ts = None):
        # we initialize the strategy class
        self.orders = []
        self.order_id = 0
        self.position = 0
        self.pnls = 0
        self.cash = 10000 # we set the available cash we can use to be $10,000
        self.current_bid = 0
        self.current_ask = 0
        self.ob_2_ts = ob_2_ts
        self.ts_2_om = ts_2_om
        self.om_2_ts = om_2_ts
    
    # first, we check whether where are events we need to handle from order books
    def handle_input_from_ob(self,book_event = None):
        if self.ob_2_ts is None: # unit test
            print('simulation mode')
            self.hand_book_event(book_event) # book_event will be none for unit test
        else:
            if len(self.ob_2_ts) > 0: # we indeed have inputs from the gateway
                be = self.handle_book_event(self.ob_2_ts.popleft()) # popleft: we receive the earliest event
                self.handle_book_event(be)
    
    #  we define a function to handle the book event
    def handle_book_event(self,book_event):
        if book_event is not None: # make sure it is not our unit test case
            self.current_bid = book_event['bid_price']
            self.current_ask = book_event['ask_price']
        
        if self.signal(book_event): # check whether we will produce signal or not
            # if yes, we create orders
            # the quantity has to fulfill both bid and ask sides
            self.create_orders(book_event,min(book_event['bid_quantity'],book_event['ask_quantity'])) 
        
        # we do execution
        self.execution()
    
    # we define a function to check the production of signaks
    def signal(self,book_event):
        if book_event is not None:
            # check whether there is a chance for us to do arbitrage
            # we sell at the price other people are willing to buy
            # and buy at the price other people are willing to sell
            if book_event['bid_price'] > book_event['ask_price']:
                return True # we produce the signal
            else:
                return False # no signal
        return False # this is for unit test
    
    # we define a function to create orders
    def create_orders(self,book_event,quantity):
        # we increase our order ids, as we create new order
        self.order_id += 1
        # we create a sell order first
        # although the two orders actually have to be sent at the same time
        ord = {
            'id': self.order_id,
            'price': self.current_bid,
            'quantity':quantity,
            'side': 'sell',
            'action': 'to_be_sent'
            }
        
        # we append the order
        self.orders.append(ord.copy())
    
        self.order_id += 1
        # we create the buy order
        ord = {
            'id': self.order_id,
            'price': self.current_ask,
            'quantity':quantity,
            'side': 'buy',
            'action': 'to_be_sent'
            }
        
        # we append the order
        self.orders.append(ord.copy())
    
    # we execute the orders and check whether they are rejected or filled 
    def execution(self):
        orders_to_be_removed = [] # the orders are either rejected or filled
        for index,order in enumerate(self.orders):
            if order['action'] == 'to_be_sent': # if the order is to be sent
            # we update the order status
            # we are sending the order
                order['status'] = 'new'
                order['action'] = 'no_action'
            
            if self.ts_2_om is None:
                # unit test mode
                print('simulation mode')
            else:
                self.ts_2_om.append(order.copy()) # we send the order
            
            # if the order doesn't need to be sent
            # that is, it is an order we receive from market
            # we check for the market order status
            if order['status'] == 'rejected':
                orders_to_be_removed.append(index)
            
            if order['status'] == 'filled':
                orders_to_be_removed.append(index)
                # we update positions, and cash onls
                pos = order['quantity'] if order['side'] == 'buy' else -order['quantity']
                self.position += pos
                # for long position, we decrease pnls and cash
                # for short position, we increase pnls and cash
                self.pnls -= pos * order['price'] 
                self.cash -= pos * order['price']
            
        # and we remove the orders_to_be_removed
        for index in sorted(orders_to_be_removed):
            del(self.orders[index]) # question: do we need to reverse the sort order?
        
    # we also need to define functions to deal with feedback from market
    def handle_response_from_om(self):
        if self.om_2_ts is None: # unit test
            print('simulation mode')
        else:
            # we handle the marker response
            self.handle_market_response(self.om_2_ts.popleft())
    
    def handle_market_response(self,order_r):
        # I use two characteristics 
        # to make sure the order has no errors at all
        order,_ = self.lookup_orders(order_r['id'],order_r['price']) 
        
        if order is None: # we have not found the order, return error
            print('Error. Not found.')
            return
        # if we have found it in our current, we update the order status from order management
        order['status'] = order_r['status']
        self.execution() # now we connect back to the execution part
    
    # we define a look up function to check whether an order exists in our current orders
    def lookup_orders(self,id,price):
        count = 0
        for o in self.orders:
            # here, I add one more parameter price, to make sure the price is valid from the market
            if o['id'] == id and o['price'] == price:
                return o,count
            count += 1
        return None,None
        
        
        
        
    
            
        