#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implementation of a market simulator 
"""

class MarketSimulator:
    def __init__(self,om_2_gw = None, gw_2_om = None): # we have two channels
        self.orders= [] # note, we have no id for market simulator
        self.om_2_gw = om_2_gw
        self.gw_2_om = gw_2_om
    
    # we define a look up function to look up orders
    def lookup_orders(self,order):
        for i in range(len(self.orders)):
            if self.orders[i]['id'] == order['id']:
                # we have found the order
                return self.orders[i],i
        return None,None
    
    # define a function to handle order from order manager
    def handle_order_from_om(self):
        if self.om_2_gw is None: # unit testing
            print('simulation mode')
        else:
            if len(self.om_2_gw) > 0: # make sure the gateway is not empty
                self.handle_order(self.om_2_gw.popleft()) # we handle valid orders
            
    def handle_order(self,order):
        o,offset = self.lookup_orders(order)
        # check whether the order exists in our current order list or not
        # if not, we will act under the action of the order
        if o is None:
            # check whether the order we received is new or not
            if order['action'] == 'new': # new order, we accept it
                order['status'] = 'accepted'
                self.orders.append(order)
                # we attach a copy the gateway
                if self.gw_2_om is not None:
                    self.gw_2_om.append(order.copy())
                else:
                    print('simulation mode')
                    return
            elif order['action'] == 'delete' or order['action'] == 'modify': # questionable orders
                print('Order id - not found - Rejection')
                # we will not keep questionable orders in our current order list
                # we append a copy to gateway for order manager to deal with it
                order['status'] = 'rejected'
                if self.gw_2_om is not None:
                    self.gw_2_om.append(order.copy())
                else:
                    print('simulation mode')
                    return
        else: # if the order exists
            if order['action'] == 'new': # duplication order!
                print('The order has already existed - duplication!')
                return
            elif order['action'] == 'delete': # we need to cancel existing orders
                o['status'] = 'cancelled'
                # we put it on the gatewat
                if self.gw_2_om is not None:
                    self.gw_2_om.append(o.copy())
                    
                else:
                    print('simulation mode')
                
                # we delete the order from our current order list, because we have cancelled it
                del(self.orders[offset])
                print('Order Cancelled')
            elif order['action'] =='modify': # we just need to amend some properties of current order
                o['status'] = 'accepted'
                # we put it on the gateway to order manager
                if self.gw_2_om is not None:
                    self.gw_2_om.append(o.copy())
                    
                else:
                    print('simulation mode')
        # note: for sending new orders / amend existing orders, we choose the sttus to be accepted
    
    # we define a function to fill all the orders
    # because the market simulator is just simulating the real market situation
    def fill_all_orders(self):
        orders_removed = []
        for index,order in enumerate(self.orders):
            order['status'] = 'filled'
            # we put it on the gateway
            orders_removed.append(index)
            if self.gw_2_om is not None:
                self.gw_2_om.append(order.copy())
            else:
                print('simulation mode') # unit testing
        
        # we remove the orders
        for index in sorted(orders_removed,reverse = True): 
            # we need to use reverse order, since
            # we don't want deletion in the beginning to influence other orders'index
            del(self.orders[index])
            
            
                    
                
        
        
        
            
        