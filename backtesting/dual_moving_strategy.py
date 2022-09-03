#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implementation of a dual moving average trading strategy used in a trading system
"""
from collections import deque # we use deque for speed

# note: our strategy is only based on the dual moving average of our bid price.
def average(nums): # define a function for calculating the average of a list
    return sum(nums) / len(nums)

class TradingDualMA:
    # initiate it
    def __init__(self,ob_2_ts,ts_2_om,om_2_ts):
        self.orders = [] # same as the example i our simple trading system
        self.order_id = 0

        self.pnls = 0
        self.current_bid = 0
        self.current_ask = 0
        self.ob_2_ts = ob_2_ts
        self.ts_2_om = ts_2_om
        self.om_2_ts = om_2_ts
        self.pnls = 0

        self.shortSMA = deque()
        self.longSMA = deque()
        # we define some variables to record positions, cash, current position holdings,
        # and total (current positon holdings + cash)
        self.list_positions = [] # for visualization purpose
        self.list_cash = []
        self.list_holdings = []
        self.list_total = []
        
        # we define several signals for showing when we should buy or sell
        self.long_signal = False
        self.position = 0 # we set the number of shares we can buy to 10
        self.cash = 100000 # we use 100000 as our initial cash
        self.holdings = 0
        self.total = 0
        
        # we also define a group of paper trading variables
        # that is, we don't consider the fill ratio. we think every order will be filled.
        self.paper_position = 0
        self.paper_holdings = 0
        self.paper_pnls = 0
        self.paper_cash = 100000
        self.list_paper_positions = []
        self.list_paper_cash = []
        self.list_paper_holdings = []
        self.list_paper_total = []
        
    # define a function to create signals based on the bid price updates
    def create_signal(self,price_update):
        self.shortSMA.append(price_update)
        self.longSMA.append(price_update)

        # check whether current two SMA lists have exceeded the time period we have set
        if len(self.shortSMA) > 20:
            self.shortSMA.popleft()
        if len(self.longSMA) > 40:
            self.longSMA.popleft()

        # the rule for the creation of trading signal is:
        # as the size os shortSMA = 20
        # we can begin our compare
        if len(self.shortSMA) == 20:
            # check for their average
            if average(self.shortSMA) > average(self.longSMA):
                # we set our trend-following signal
                self.long_signal = True
            else:
                self.long_signal = False
            return True # we return true, represents that we are indeed creating a signal
        return False # we don't compare two SMA, no signal has been produced
    
    
    # define a function to check our action
    def buy_sell_hold(self,book_event):
        if self.long_signal and self.paper_position <= 0: # enter a long position / buy some back in a short position
            self.create_orders(book_event,book_event['bid_quantity'],'bid')
            self.paper_position += book_event['bid_quantity'] # we change our paper trading variables
            self.paper_cash -= book_event['bid_quantity'] * book_event['bid_price']
        elif not self.long_signal and self.paper_position > 0:
            # enter a short position 
            # the system doesn't not support short selling now
            # as it will be difficult to update the cash acmount
            self.create_orders(book_event,book_event['bid_quantity'],'ask')
            self.paper_position -= book_event['bid_quantity']
            self.paper_cash += book_event['bid_quantity'] * book_event['bid_price']
        # for other values, we don't act, we hold
        
        # calculate the value of our current paper holdings with respect to current market price
        self.paper_holdings = self.paper_position * book_event['bid_price']
        self.paper_total = self.holdings + self.cash
        # we append them to our list for visualization
        self.list_paper_holdings.append(self.holdings)
        self.list_paper_positions.append(self.position)
        self.list_paper_total.append(self.total)
        self.list_paper_cash.append(self.cash)
        
        # calculate the value of our current real holdings with respect to current market price
        self.holdings = self.position * book_event['bid_price']
        self.total = self.holdings + self.cash
        # we append them to our list for visualization
        self.list_holdings.append(self.holdings)
        self.list_positions.append(self.position)
        self.list_total.append(self.total)
        self.list_cash.append(self.cash)
    
    # define a function to create orders
    def create_orders(self,book_event,quantity,side):
        # we increase our order ids, as we create new order
        self.order_id += 1
        # we create a sell order first
        # although the two orders actually have to be sent at the same time

        ord = {
            'id': self.order_id,
            'price': book_event['bid_price'],
            'quantity':quantity,
            'side': side,
            'action': 'to_be_sent'
            }
        
        # we append the order
        self.orders.append(ord.copy())
    
    # define an acntion to for new coming book events
    def signal(self,book_event):
        if book_event['bid_quantity'] != -1 and book_event['ask_quantity'] != -1:
            # for new prices, we check whether there are signals
            self.create_signal(book_event['bid_price'])
            self.buy_sell_hold(book_event)
    
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
            if order['status'] == 'rejected' or order['status'] == 'cancelled':
                orders_to_be_removed.append(index)
            
            if order['status'] == 'filled':
                # we update our real-time variables
                orders_to_be_removed.append(index)
                # we update positions, and cash onls
                pos = order['quantity'] if order['side'] == 'ask' else -order['quantity']
                self.position += pos
                # we also update our holdings
                self.holdings = self.position * order['price']
                # for long position, we decrease pnls and cash
                # for short position, we increase pnls and cash
                self.pnls -= pos * order['price'] 
                self.cash -= pos * order['price']
            
        # and we remove the orders_to_be_removed
        for index in sorted(orders_to_be_removed,reverse = True):
            # we need to use reverse order, since
            # we don't want deletion in the beginning to influence other orders'index
            del(self.orders[index]) 
    
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
    
    # first, we check whether where are events we need to handle from order books
    def handle_input_from_ob(self,book_event = None):
        if self.ob_2_ts is None: # unit test
            print('simulation mode')
            self.hand_book_event(book_event) # book_event will be none for unit test
        else:
            if len(self.ob_2_ts) > 0: # we indeed have inputs from the gateway
                self.handle_book_event(self.ob_2_ts.popleft()) # popleft: we receive the earliest event
              
    
    #  we define a function to handle the book event
    def handle_book_event(self,book_event):
        if book_event is not None: # make sure it is not our unit test case
            self.current_bid = book_event['bid_price']
            self.current_ask = book_event['ask_price']
            self.signal(book_event) # update our buy, sell or hold status
            # we do execution
            self.execution()
        
    # we define a look up function to check whether an order exists in our current orders
    def lookup_orders(self,id,price):
        count = 0
        for o in self.orders:
            # here, I add one more parameter price, to make sure the price is valid from the market
            if o['id'] == id and o['price'] == price:
                return o,count
            count += 1
        return None,None
        
    # we define a function to calculate current total PnLs
    # both realized & unrealized
    def get_pnls(self):
        return self.pnls + self.position * (self.current_bid + self.current_ask)/2     