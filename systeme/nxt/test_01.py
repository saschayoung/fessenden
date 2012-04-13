#!/usr/bin/env python


import time
import sys


import nxt.locator
from nxt.motor import *
from nxt.sensor import *


PORT_AB = 0x03

def spin_around(b):
    m_left = Motor(b, PORT_A)
    m_right = Motor(b, PORT_B)
    # m_both = Motor(b, PORT_AB)

    m_left.weak_turn(100, 360)
    m_right.weak_turn(-100, 360)
    # m_both.turn(100, 360)

def main():
    b = nxt.locator.find_one_brick()
    
    light = Light(b, PORT_1)
    light.set_illuminated(True)

    spin_around(b)

    while True:
        try:
            print "Light sensor reading: ", light.get_sample()
            time.sleep(0.1)
        except KeyboardInterrupt:
            light.set_illuminated(False)
            sys.exit(1)




if __name__=='__main__':
    main()

        
