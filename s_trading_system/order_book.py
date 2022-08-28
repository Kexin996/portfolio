#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implementation of a simple limit order book, first-in-first-out (FIFO)
"""

"""
3 operations (ideal):
    1. insertion - O(logn) / O(1)
    2. modification (use id) - O(logn) / O(1)
    3. deletion (use id) - O(logn) / O(1)

since this file is only a demo in Python, not a real limit order book for high-frequency trading
in this file, the time complexity becomes:
    1. insertion - O(n)
    2. modification - O(n) 
    3. deletion - O(n) 

note: use more advanced data structure can improve the algorithm efficency
and I will revisit it later. 
"""

class OrderBook:
    # we initialize our order book
    # since we are using python, we don't pay much attention to velocity
    # as high frequency trading
    def __init__(self,lp_2_ob = None,ob_2_ts = None):
        self.list_asks = []
        self.list_bids = []
        self.lp_2_ob = lp_2_ob
        self.ob_2_ts = ob_2_ts
        self.current_bid = None # current asks / bids are lists
        self.current_ask = None
    
    # receive order from liquidity provider
    def handle_order_from_gateway(self,order = None):
        if self.lp_2_ob is None: # unit testing
            print('simulation mode')
            self.handle_order(order)
        else:
            if len(self.lp_2_ob) > 0:
                # we handle valid order
                self.handle_order(self.lp_2_ob.popleft())
    
    # handle the orders received
    def handle_order(self,order):
        if order['action'] == 'new': # it is a new order
            self.handle_new(order)
        elif order['action'] == 'modify': # modify the properties of current bid/ask orders
            self.handle_modify(order)
        elif order['action'] == 'delete': # delete one of the current orders
            self.handle_delete(order)
        else: # the order we received is invalid
            print('Error - the order is invalid')
        # if we have some actions about the order
        # we need to generate a book event and send it to trading strategies
        return self.check_generate_book_event()

    # add new order
    def handle_new(self,order):
        # we check which list to insert the new order
        if order['side'] == 'bid': 
            self.list_bids.append(order)
            # and we sort it 
            # since for bids, it is the price other people want to buy
            # we sort the list in the prices from largest to lowest
            self.list_bids.sort(key = lambda x: x['price'],reverse = True)
        else:
            self.list_asks.append(order)
            self.list_asks.sort(key = lambda x: x['price'])
                
    # modify existing orders
    def handle_modify(self,o):
        # we first find this order
        order = self.find_order(o)
        # ???: this operation is only valid if we want to decrease the quantity of the existing order
        # will revisist later
        #
        # guess: we only update for smaller quantity
        # because we need of min(bid_quantity,ask_quantity) to create signals
        if order['quantity'] > o['quantity']:
            # update quantity
            order['quantity'] = o['quantity']
        else:
            print("Invalid size")
            
    # delete order
    def handle_delete(self,o):
        # we use get_list to get the side of the list
        # then search the order in its side (ask/bid) list
        list_get = self.get_list(o)
        order = self.find_order(o,list_get) # if we find the order, it will not be none
        if order is not None: # we have found it, and we delete it
            list_get.remove(order)
    
    # we define get_list to find out the side of the order
    def get_list(self,order):
        # we check whether the order contains 'side'
        if 'side' in order:
            if order['side'] == 'ask':
                return self.list_asks
            elif order['side'] == 'bid':
                return self.list_bids # we return the valid sides
            else:
                print('Invalid side') # tell the user that there is an error
                return None
        else:
            # if the order doesn't have side, we decide it by its id
            # we check the two lists
            for o in self.list_bids:
                if o['id'] == order['id']:
                    return self.list_bids
            for o in self.list_asks:
                if o['id'] == order['id']:
                    return self.list_asks
            
            # if we still haven't found it, notify the user
            print("Not found - depended on side and id")
            return None
    
    # find the order in its side list
    def find_order(self,order,lookup_list = None):
        # if the list is None, we directly find the list through get_list
        if lookup_list is None:
            lookup_list = self.get_list(order)
        
        # if we have gotten the lookup_list
        if lookup_list is not None:
            # we find the order through its id
            for o in lookup_list:
                if o['id'] == order['id']:
                    # we have found it
                    # we return it
                    return o
        # if the lookup_list doesn't exist / we don't find out the order, we tell the user and return none
        print('Error - order not found in the side list')
        return None
    
    # create a book event
    def create_book_event(self,bid,ask):
        book_event = {
            'bid_price':bid['price'] if bid else -1, 
            'bid_quantity':bid['quantity'] if bid else -1,
            # here, we set price to -1 if it is none
            'ask_price':ask['price'] if ask else -1,
            'ask_quantity':ask['quantity'] if ask else -1
            }
        return book_event
    
    # check whether we generate a book event
    # condition: we will only create a book event if the tops of our bid/ask side lists have changed
    # it is not the same as signal
    # we will handle signal in trading strategy
    def check_generate_book_event(self):
        tob_changed = False
        # first, check for whether there is a change in our bids list
        current_list = self.list_bids
        if len(current_list) == 0: # the list_bids is empty
            # we check for our current_bid
            # if current_bid is None, that means we have not changed the order book
            # that is, we have not inserted any bid order, so current_bids is none
            
            # else, we have changed the top of bids list, since now the list of bids is empty,
            # but current_bid is not None
            if self.current_bid is not None:
                tob_changed = True
                self.current_bid = None # update the current bid
        else: # we check the top of bid list and current_bid
            # if current_list is not empty, current_bid will not be empty
            if self.current_bid != current_list[0]:
                tob_changed = True
                self.current_bid = current_list[0]
        
        # repeat the same process for ask lists
        current_list = self.list_asks
        if len(current_list) == 0: # the list_asks is empty
            # we check for our current_ask
            # if current_ask is None, that means we have not changed the order book
            # that is, we have not inserted any ask order, so current_asks is none
            
            # else, we have changed the top of ask lists, since now the list of asks is empty,
            # but current_ask is not None
            if self.current_ask is not None:
                tob_changed = True
                self.current_ask = None # update the current ask
                
        else: # we check the top of ask list and current_ask
            # if current_list is not empty, current_ask will not be empty
            if self.current_ask != current_list[0]:
                tob_changed = True
                self.current_ask = current_list[0]
                    
        # if either / both top of the ask / bid list has changed
        # we gonna send a book event to trading strategy
        if tob_changed:
            book_event = self.create_book_event(self.current_bid,self.current_ask)
            
            # if our gateway is not None (not in simulation mode), we send it
            # to the trading strategy
            if self.ob_2_ts is not None:
                self.ob_2_ts.append(book_event)
            else: # else, we just return the book_event
                return book_event
            
            
            
        
        