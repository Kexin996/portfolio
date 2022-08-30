#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testing file for receiving price updates and orders by using quickfix
"""

import quickfix

price = quickfix.Price()
i = quickfix.Message()
i.getField(price)
print(i)
