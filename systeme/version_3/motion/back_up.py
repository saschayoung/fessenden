#!/usr/bin/env python

import nxt.locator
# from nxt.motcont import MotCont
from nxt.motor import *


def spin_around(b):
    m_left = Motor(b, PORT_A)
    m_right = Motor(b, PORT_B)
    m_left.weak_turn(-75, 360)
    m_right.weak_turn(-75, 360)

b = nxt.locator.find_one_brick()

spin_around(b)


