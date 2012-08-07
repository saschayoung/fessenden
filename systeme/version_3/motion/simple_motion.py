#!/usr/bin/env python

import nxt.locator

from motion_api import MotionAPI

brick = nxt.locator.find_one_brick()

motion = MotionAPI(brick)

try:
    while True:
        motion.find_line()
        motion.go_forward(25)
except KeyboardInterrupt:
    motion.shutdown()
