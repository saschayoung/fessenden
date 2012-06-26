#!/usr/bin/env python

import time

import nxt.locator
from nxt.sensor import *


def run():
    brick = nxt.locator.find_one_brick()
    
    color = Color20(brick, PORT_2)

    while True:
        print "Color sensor reading = ", color.get_sample()
        time.sleep(1)


if __name__=='__main__':
    try:
        run()
    except KeyboardInterrupt:
        pass

