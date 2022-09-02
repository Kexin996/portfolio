#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implementation of a simulated clock to check the order timestamp
"""

from datetime import datetime

# define a simulated clock class
# which can display two modes: simulated / real time
class SimulatedRealClock():
    def __init__(self,simulated = False): # default: display real time
        self.simulated = simulated
        self.simulated_time = None
    
    # we create a datetie object
    # when we receive a new order
    def receive_order(self,order):
        # datetime.strptime: create a new datatime object from a string
        self.simulated_time = datetime.strptime(order['timestamp'],'%Y-%m-%d %H:%M:%S.%f') # the 'Date' string  is like: year-month-day
        # for efficency use, we check even milliseconds
    # define a function to get the time
    def getTime(self):
        if not self.simulated: # we are in real time mode
      
            return datetime.now() # return current time
        else:
            return self.simulated_time


# we check the class
real_time = SimulatedRealClock()
print(real_time.getTime()) # we get the real time

# we continue to check for simulated clock
real_time = SimulatedRealClock(simulated = True)
real_time.receive_order({'timestamp':'2018-06-29 09:00:00.89'})
print(real_time.getTime()) # it works. great!