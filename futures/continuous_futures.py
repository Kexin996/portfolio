#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Building a continuous Hang Seng Index Futures price list by using Quandl
"""

import datetime
import numpy as np
import pandas as pd
import nasdaqdatalink # quandle has been bought by NASDAQ...

nasdaqdatalink.ApiConfig.api_key = 'u3_VrsLQap5mibVfyjBo'

# our main task is to define a function creating rollover series
def futures_rollover(start_date,expiry_date, contracts, rollover_days = 5):
    # it will carry a rollover of 5 days as default priot'
    # to the expiration of the earliest contract
    # in order to produce a continuous time series contracts
    
    # build a dataframe with frequency of business day
    dates =pd.date_range(start_date,expiry_date[-1],freq='b')

    
    # create an empty 2D array for saving our rolling weights
    roll_weights = pd.DataFrame(np.zeros((len(dates),len(contracts))), index = dates, columns = contracts)
    prev_date = roll_weights.index[0]
    
    # create specific weightings for *each contract*
    for i, (item,ex_date) in enumerate(expiry_date.iteritems()):
        # iteritems() ---> returns (column name, Series)
        if i < len(expiry_date)-1: 
            # why do we compare i to len(expiry_date)-1?
            # we only need o calculate decay weight
            # for the contracts we want to roll over
            # if i == len(expiry_date)-1, that means
            # we have reached the last contract
            # we stop
        
            # we use ex_date - pd.offsets.BDay() for the
            # weight factors before the rolling periods
            roll_weights.loc[prev_date:ex_date - pd.offsets.BDay(),item] = 1
            
            # create a pd.series consisting of the five rolling days
            roll_rng = pd.date_range(end = ex_date-pd.offsets.BDay(),periods=rollover_days + 1, freq='B')
            # in order to update the rolling weights
            decay_weights = np.linspace(0,1,rollover_days + 1)
            # why rollover_days + 1:
            # this parameter denotes how many points we will
            # create in the interval
            # we need 0,0.2,0.4,0.6,0.8,1.0
            
            # 1-decay_weights:
            # [1.  0.8 0.6 0.4 0.2 0. ]
            # # this is the weight for far_date price
            
            roll_weights.loc[roll_rng, item] = 1-decay_weights
            # now we are setting the decay weights for the second month
            # in the same period
            # but this period is the beginning period of the second contract
            # which is expiry_date.index[i+1]
            roll_weights.loc[roll_rng, expiry_date.index[i+1]] = decay_weights
        else:
            # we have reacbed the final contract
            roll_weights.loc[prev_date:,item] = 1
        prev_date = ex_date # we update the last expiry date
    print(roll_weights) # we print it out to check the weight factors
    return roll_weights
            


# we use two series 
data_near= nasdaqdatalink.get('HKEX/HSIF2021')
data_far= nasdaqdatalink.get('HKEX/HSIG2021')


# build a dataframe that we will use to adjust price
# note: if we turn a dictionary to a dataframe
# the dataframe's index will be the key in dictionary
df = pd.DataFrame({'JAN': data_near['Prev. Day Settlement Price'],'FEB': data_far['Prev. Day Settlement Price']},index = data_far.index)
# also build a series including the expiry dates
# for our function
expiry_dates = pd.Series({'JAN':datetime.datetime(2021,1,29),'FEB':datetime.datetime(2021,2,26)})

weights = futures_rollover(df.index[0],expiry_dates,df.columns)

# we get the dataframe containing the price of futures after adjustment
# note: np.sum() will take nan as 0.0
# we just combined the two contracts into a continuous one
# sum is ok since there is no overlapping between the two contracts
# after multiply the price data by the weights we calculated

df_adjusted = (df*weights).sum(axis = 1)

# due to the different cultures in China and U.S.
# there willl be some values equal to nan in some festivals, 
# such as spring festival
# the business day data will be nan, and the sum will be zero
# we just drop them
df_adjusted = df_adjusted[df_adjusted != 0]

# now we check our continuous data
print()
print("A continuous contract:")
print(df_adjusted)
# we plot it to see how smooth it has become
import matplotlib.pyplot as plt
plt.plot(df_adjusted)
plt.title('Future Prices in a Perpetual Series')
plt.show()
# it is not very smooth,though
# but it is much better than having two jumps between contracts



