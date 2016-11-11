#!/usr/bin/env python

import math
import sys
import time
import threading

import nxt.locator
from nxt.motor import *
from nxt.sensor import *





class BasicMotion(object):
    def __init__(self):
        self.brick = nxt.locator.find_one_brick()
        self.__init_light_sensor()
        self.__init_motors()



    def __init_light_sensor(self):
        self.light = Light(self.brick, PORT_1)
        self.light.set_illuminated(True)

    def __init_motors(self):
        self.motor_left = Motor(self.brick, PORT_A)
        self.motor_right = Motor(self.brick, PORT_B)


    def __servo_rotation(self, distance, wheel_diameter = 2.221):
        return (180.0 * distance) / (math.pi * wheel_diameter / 2.0)






    def run(self):
        while True:
            self.follow_line()
            self.find_line()

        # self.follow_line()
        # for i in range (10):
        #     print "Light sensor reading: ", self.get_light_reading()
        #     time.sleep(0.1)

        # self.turn_in_place(-90)

        # for i in range (10):
        #     print "Light sensor reading: ", self.get_light_reading()
        #     time.sleep(0.1)
        # self.shutdown()


    def shutdown(self):
        self.halt_motion('coast')
        self.light.set_illuminated(False)
        





    def turn_in_place(self, yaw, power = 75, axle_length = 4.5):
        arc_distance = (math.pi / 180.0) * abs(yaw) * (axle_length / 2.0)
        wheel_rotation = self.__servo_rotation(arc_distance)
        # print "arc_distance: ", arc_distance
        # print "wheel_rotation", wheel_rotation
        if (yaw > 0):
            self.motor_left.weak_turn(power, int(wheel_rotation))
            self.motor_right.weak_turn(-power, int(wheel_rotation))
        elif (yaw < 0):
            self.motor_left.weak_turn(-power, int(wheel_rotation))
            self.motor_right.weak_turn(power, int(wheel_rotation))
        else:
            print "desired yaw angle is 0, nothing to do"




    def get_light_reading(self, illumination=True):        
        self.light.set_illuminated(illumination)
        return self.light.get_sample()



    def move_forward(self, power = 75 , regulated = True):
        self.motor_left.run(power, regulated)
        self.motor_right.run(power, regulated)


    def halt_motion(self, method):
        if method not in ['brake',  'coast']:
            print "`method` must be one of {`brake`|`coast`}"
            raise ValueError
        if method == 'brake':
            self.motor_left.brake()
            self.motor_right.brake()
        else:
            self.motor_left.idle()
            self.motor_right.idle()
            


        
    def follow_line(self):
        print "following line"
        self.move_forward()
        while True:
            reflected_light = self.get_light_reading()
            # print "Light sensor reading: ", self.get_light_reading()
            if reflected_light > 500:
                self.halt_motion('brake')
                print "lost line, stopping motion"
                return



    def find_line(self):
        print "finding line"
        sweep_angle = [10, -20, 30, -40, 60, -80, 120, -160, 240, -320]
        line_found = False
        is_turning = True

        while not line_found:
            for sweep in sweep_angle:
                print "find line: sweeping %d degrees" % sweep
                self.turn_in_place(sweep)

                state = self.motor_left._read_state()
                run_state = state[0].run_state
                # print "run_state: ", run_state
                while run_state != 0: 
                    reflected_light = self.get_light_reading()
                
                    if reflected_light < 400:
                        line_found = True
                        self.halt_motion('brake')
                        print "found line, stopping search"
                        return
                    state = self.motor_left._read_state()
                    run_state = state[0].run_state





if __name__=='__main__':
    robot = BasicMotion()
    try:
        robot.run()
    except KeyboardInterrupt:
        robot.shutdown()





