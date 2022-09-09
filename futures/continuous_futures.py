#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Building a continuous HK China gas futures price list by using Quandl
"""

import datetime
import numpy as np
import pandas as pd
import nasdaqdatalink # quandle has been bought by NASDAQ...


# we load our data by using inde code
data = nasdaqdatalink.get('HKEX/00003')
# we check for the tail to see the validity of the downloaded pandas dataframe
print(data.tail())