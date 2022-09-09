#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Getting historical data about price for S&P 500 symbols from AlphaVantage  
"""
from datetime import datetime as dt
import json
import time
import warnings # for checking the transportation of data

import MySQLdb as mdb
import requests

avt_api_key = '4OX1V9GRDAL8EDVX'
avt_base_url = 'https://www.alphavantage.co'
# the following is used to get daily adjusted values from alphavantage
avt_time_series_call = 'query?function=TIME_SERIES_DAILY' 

ticker_count = 10 # we use 10 for testing purpose
wait_time_seconds = 12.0 # we can only call 5 times per minute for free users :(

# have the setting for connecting to MySQL
db_host = 'localhost'
db_user = 'sec_user'
db_pass = 'zkx20020729'
db_name = 'securities_master'
con = mdb.connect(host = db_host,user = db_user,passwd=db_pass,db = db_name)


# define a function to get the ticker from our current symbol table
# return type: list
def list_of_tickers():
    cursor = con.cursor()
    cursor.execute("SELECT id, ticker FROM symbol")
    con.commit()
    data = cursor.fetchall()
    # we return a list of tuples
    return [(d[0],d[1]) for d in data]

# define a function to connect to alpha vantage 
def alpha_vantage_call(ticker):
    # we just follow the sample provided on alphavantage
    # e.g.
    # https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo
    return "%s/%s&symbol=%s&outputsize=full&apikey=%s" %(avt_base_url,avt_time_series_call,ticker,avt_api_key)

# define a function to get the daily historical data from alphavantage
def get_daily_history_alphavantage(ticker):
    
    avt_url = alpha_vantage_call(ticker)
    print(avt_url)
    # try to get the json file
    
    try:
        data_js = requests.get(avt_url)
        data = data_js.json()['Time Series (Daily)'] # we load the data
    except Exception as e: # if we cannot load the data
        # notify the type of error
        print('Could not load the data for %s ... (%s) ... skipping...') %(ticker,e)
        return []
    else:
        # we save the price data
        prices = []
        for date in data:
            data_temp = data[date]
            prices.append(( # we append a large tuple
                dt.strptime(date,'%Y-%m-%d'), # price date: create a dataframe object
                float(data_temp['1. open']), # open price
                float(data_temp['2. high']), # high price
                float(data_temp['3. low']), # low price
                float(data_temp['4. close']), # close price
                int(data_temp['5. volume']) # volume
                # no adjusted close...
                # at first I decided to be the premium user
                # however, as soon as I found that alpha vantage has stopped providing real-time data
                # I've decided switched to other API 
                ))
        return prices

# define a function to directly insert daily data into database
def insert_data_into_db(data_vendor_id,symbol_id,daily_data):
    now = dt.utcnow() # the time for updating data
    
    # change the data inserted format
    daily_data = [(data_vendor_id,symbol_id,d[0],now,now,d[1],d[2],d[3],d[4],d[5]) for d in daily_data]
    # we don't have adjusted data now, so iwe ignore it now
    column = (
        "data_vendor_id, symbol_id, price_date, created_date, " 
        "last_updated_date, open_price, high_price, low_price, " 
        "close_price, volume")
    inserted_str = ('%s, '*10)[:-2]
    
    sql = ("INSERT INTO daily_price (%s) VALUES (%s)") %(column,inserted_str)
    
    # we update our table now
    cursor = con.cursor()
    cursor.executemany(sql,daily_data)
    con.commit() # commit it to finnish
    
if __name__ == '__main__':
    # we begin to check our functions
    warnings.filterwarnings('ignore') # we filter out warnings due to data truncation in precision
    # ignore: never print matching warning
    tickers = list_of_tickers()[:ticker_count] # we use 10 tickers for testing purpose
    total_tickers = len(tickers)
    
    # we begin to enumerate it
    for i,t in enumerate(tickers):
        # show that we are loading data
        print("Adding data for %s: %s out of %s"%(t[1],i+1,total_tickers))
        avt_data = get_daily_history_alphavantage(t[1])
        insert_data_into_db('1',t[0],avt_data)
        # 1 means that alpha vantage is the first vendor we have used
        time.sleep(wait_time_seconds) # wait for the time to connect to our API

print("Successfully added AlphaVantage pricing data to DB.")

# it works well
# but it takes such a long time to download...
# I gonna use ScraPy to write a better version for saving time...
    
    
