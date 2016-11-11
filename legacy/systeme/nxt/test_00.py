#!/usr/bin/env python

import math
import time
import threading

import nxt.locator
# from nxt.motcont import MotCont
from nxt.motor import *


def spin_around(b):
    m_left = Motor(b, PORT_A)
    m_right = Motor(b, PORT_B)
    m_left.weak_turn(75, 360)
    m_right.weak_turn(-75, 360)

b = nxt.locator.find_one_brick()
spin_around(b)


# class ThreadClass(threading.Thread):
#     def run(self, brick, port, power, angle):
#         motor = Motor(brick, port)
#         motor.weak_turn(power, angle)



# b = nxt.locator.find_one_brick()

# m_left = ThreadClass()
# m_right = ThreadClass()
# m_left.run(b, PORT_A, -100, 360)
# m_right.run(b, PORT_B, 100, 360)


# motors = SynchronizedMotors(PORT_A, PORT_B, 1)
# # m_right = Motor(b, PORT_B)
# motors.run()
# time.sleep(0.5)
# motors.idle()





# mc = MotCont(b)
# mc.start()

# distance = 10

# wheel_diameter = 2.221
# servo_rotation = (180.0 * distance) / (math.pi * wheel_diameter / 2.0)


# m_left = Motor(b, PORT_A)
# m_right = Motor(b, PORT_B)
# m_both = Motor(b, 0x03)

# m_left.run(power=75, regulated=True)
# m_right.run(power=75, regulated=True)

# time.sleep(0.5)
# m_left.brake()
# m_right.brake()


# m_left.turn(100, 360)
# m_right.turn(-100, 360)


# mc.set_output_state(3, 50, servo_rotation)
# print "marker 1"
# mc.set_output_state(3, 0, 0)


# def spin_around(b):
    # m_left = Motor(b, PORT_B)

# b = nxt.locator.find_one_brick()
# spin_around(b)
