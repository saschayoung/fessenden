#!/usr/bin/env python


import nxt.locator

def connect_to_brick():
    """
    Connect to NXT Brick.
    
    """
    return nxt.locator.find_one_brick()
    


