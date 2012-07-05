#!/usr/bin/env python


import nxt.locator
from nxt.motor import *
from nxt.sensor import *


class NXTBase(object):

    def __init__(self):
        
        self.brick = nxt.locator.find_one_brick()


    def init_motors(self):
        self.motor_left = Motor(self.brick, PORT_A)
        self.motor_right = Motor(self.brick, PORT_B)



    def init_light_sensor(self):
        self.light = Light(self.brick, PORT_1)
        self.light.set_illuminated(True)

    def kill_light_sensor(self):
        self.light.set_illuminated(False)




    def init_color_sensor(self):
        self.color = Color20(self.brick, PORT_2)
        self.color.set_light_color(13)

    def kill_color_sensor(self):
        self.color.set_color(17)
