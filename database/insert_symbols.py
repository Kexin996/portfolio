#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Using requests and beautifulsoup to add stock symbols to MySQL database directly
"""

# we import library first
import datetime
from math import ceil

import bs4
import MySQLdb as mdb
import requests

# define a function to get the names of stocks in S&P 500 by using requests and b4s
# output: a list of tuples
def get_name_wiki():
    
    # we store the created_time in our table
    # note: the time is in UTC form
    now = datetime.datetime.utcnow()
    # print(now)
    
    # we load the website and use soup to read the table
    website = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs4.BeautifulSoup(website.text,'html.parser')
    
    # we only want the first table for now
    symbol_list = soup.find_all('table')[0].find_all('tr')[1:] 

    # we don't want to header
    # we just select all the table rows starting at row 1

    symbols = []
    for i,symbol in enumerate(symbol_list):
        td = symbol.find_all('td') # all the data in the row
        
        # we append a list to symbols
    
        symbols.append(
        (td[0].text[:-1], # it is the symbol name
         'stock', # type of instrument
         td[1].text, # full name of the company
         td[3].text, # sector
         'USD', # for american exchange, the currency is $
         now, # created date
         now # last updated date
            ))
    return symbols
    # questions: how should I update the values of stocks while we use tuple structure?
    # would it be too slow to convert it to list to change it?
    # note: tuple is faster than list as it is immutable ---> less memory space

    
# define a function to insert the symbols we have created into MySQL database
def insert_symbols(symbols):
    # we first connect to the database
    db_host = 'localhost'
    db_user = 'sec_user'
    db_pass = 'zkx20020729'
    db_name = 'securities_master'
    con = mdb.connect(host = db_host,user = db_user,passwd=db_pass,db = db_name)
    
    # make a sql statement to insert
    
    column = "ticker, instrument, name, sector, currency, created_date, last_updated_date"
    insert_column = ('%s, ' *7)[:-2] # the format of inserting
    
    # insert all the values in string mat
    sql = "INSERT INTO symbol (%s) VALUES (%s)"%(column,insert_column)
    
    # send it to MySQL database
    cursor = con.cursor()
    cursor.executemany(sql,symbols)
    # commit it
    con.commit()
   

if __name__ == '__main__':
    symbols = get_name_wiki()
    insert_symbols(symbols)

# we are not sure about the data we have stored
# so we create a new program to retrieve the data we have gotten