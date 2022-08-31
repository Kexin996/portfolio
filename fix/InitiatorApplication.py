#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implementation of initiator application class
"""

import quickfix as fix 


# inherit interface Application from base.py

class Initiator(fix.Application):
    
    # create a logger
    def create_logger(self,logger):
        self.logger = logger

    def onCreate(self,sessionID):
        self.logger.info("we have created a seesion:",sessionID)
        return
    
    def onLogon(self,sessionID):
        self.logger.info("succesfully log on:",sessionID)
        return
    
    def onLogout(self,sessionID):
        self.logger.info('succesfully log out',sessionID)
        return
    
    def fromAdmin(self,sessionID):
        self.logger.info('Received:',sessionID)
        return
    
    def toApp(self,sessionID):
        self.logger.info('callback:',sessionID)
        return
     
         
        
dir(fix)