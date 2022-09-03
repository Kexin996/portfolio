#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inplementatation of showing time values in order manager system
"""

from simulated_clock import SimulatedRealClock
import threading # for creating a thread
from time import sleep
from datetime import datetime, timedelta

# define a timeout class (a thread)
class TimeOut(threading.Thread):
    
    def __init__(self,sim_real_clock,time_to_stop,callback):
        super().__init__() # override the base class __init__
        self.sim_real_clock = sim_real_clock
        self.time_to_stop = time_to_stop
        self.callback = callback
        self.disable = False 
        # if self.disable is true: we don't need to
        # do the callback, since we have received the arket response
    
    def run(self): # for threading.start()
        # wait for the market response
        while not self.disable and self.sim_real_clock.getTime() < self.time_to_stop:
            sleep(1)

       
        # if the time is out and we still don't receive the response
        if not self.disable:
            self.callback() # we call the callback funcion
        else:
            print('We have received response!')

# define a simple order manager 
# only deal with the time value in receiving order in 5 seconds
class OMS:
    # initiate our class
    def __init__(self,sim_real_clock):
        self.sim_real_clock = sim_real_clock
        self.time_out = TimeOut(sim_real_clock,sim_real_clock.getTime()+timedelta(seconds = 5),self.OnTimeOut)
    
    # define a class about the time when we send order
    def send_order(self):
        self.time_out.disable = False # for run() function
        # we send order, 
        # and then we can begin to count down 5 seconds
        # waiting for the market response
        self.time_out.start() # it will run self.time_out.run()
        print('...send order')
    
    
    # if we receive a response, 
    # we will call a helper function to update disable in time_out
    def if_receive(self,response):
        self.sim_real_clock.receive_order(response)
        self.receive_market_response()
    def receive_market_response(self):
        self.time_out.disable = True # so we will not call the callback function
    
    # define a callback function
    def OnTimeOut(self):
        print('order time is out! \n')

# we check the oms in two cases: real time mode and simulated time mode
if __name__ == '__main__':
    print('case 1: real time')
    # initialize our simulated clock
    simulated_real_clock = SimulatedRealClock()
    oms = OMS(simulated_real_clock)
    oms.send_order() # begin to send order
    for i in range(10):  
        print('do something else:',i)
        sleep(1)
    # threads: Concurrency and Parallelism
    # we will see that when the time is 5 seconds, 
    # we will get the notification from callback()
    
    # we continue to check simulated time mode
    simulated_real_clock = SimulatedRealClock(simulated = True)
    simulated_real_clock.receive_order({'timestamp':'2018-06-29 09:00:00.89'})
    oms = OMS(simulated_real_clock)
    oms.send_order()
    sleep(1) 
    sleep(1)
    sleep(1)
    # suppose we receive our test order respone from market
    oms.if_receive({'timestamp':'2018-06-29 09:00:03.89'}) 
    
    
    
        
    
        