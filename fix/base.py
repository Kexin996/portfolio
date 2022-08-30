#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The interfaces prepared for our parser
"""

# create the application class for both clients and servers
class Application(object):
   
    # it is called when quickfix creates a new trading session
    # once we create it, we can begin to send messages to it
    def onCreate(self,sessionID):
        return
    
    # when a valid logon is built by the counterparty
    # connection is established and completed
    def onLogon(self, sessionID): 
        return
    
    # fix session is no longer online
    def onLogout(self, sessionID): 
        return
    
    # check the administrtive message sent by ourselves
    def toAdmin(self, message, sessionID): 
        return
    
    # callback function
    # check for DoNotSend exception
    def toApp(self, message, sessionID): 
        return
    
    # when the counterparty has send us the administrative message
    # useful for: 
    # e.g. validating logon meesages
    def fromAdmin(self, message, sessionID): 
        return
    
    # receives application message
    def fromApp(self, message, sessionID): 
        return
