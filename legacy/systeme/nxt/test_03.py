#!/usr/bin/env python


import time
import sys


import nxt.locator
# from nxt.motor import *
from nxt.sensor import *
from nxt.motcont import MotCont





def main():

    b = nxt.locator.find_one_brick()

    mc = MotCont(b)

    # mc.start()
    
    mc.cmd(3, 50, 720)

    light = Light(b, PORT_1)
    light.set_illuminated(True)


    # mc.stop()

    




    while True:
        try:
            print "Light sensor reading: ", light.get_sample()
            time.sleep(0.1)
        except KeyboardInterrupt:
            light.set_illuminated(False)
            sys.exit(1)




if __name__=='__main__':
    main()

        



# def spin_around(b):
#     m_left = Motor(b, PORT_A)
#     m_right = Motor(b, PORT_B)
#     m_both = Motor(b, PORT_AB)

#     # m_left.turn(100, 360)
#     # m_right.turn(-100, 360)
#     m_both.turn(100, 360)
