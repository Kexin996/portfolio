#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Retrieving data from our database securities master
"""

import pandas as pd
import MySQLdb as mdb

if __name__ == '__main__':
    # connect to our database first
    db_host = 'localhost'
    db_user = 'sec_user'
    db_pass = 'zkx20020729'
    db_name = 'securities_master'
    con = mdb.connect(host = db_host,user = db_user,passwd=db_pass,db = db_name)
    
    # as an example, we select ABBV data with price_date and close
    sql = """
        SELECT dp.price_date,dp.close_price
        FROM symbol as sym
        INNER JOIN daily_price as dp
        ON dp.symbol_id = sym.id
        WHERE sym.ticker = 'ABBV'
        ORDER BY dp.price_date ASC;
    """
    
    # we change the table into a pandas dataframe
    abbv = pd.read_sql_query(sql,con=con,index_col = 'price_date')
    
    # our example works quite well
    print(abbv.head())