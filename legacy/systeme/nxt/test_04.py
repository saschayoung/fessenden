#!/usr/bin/env python

import math
import time
import sys


import nxt.locator
# from nxt.motor import *
from nxt.sensor import *
from nxt.motcont import MotCont





class BasicMotion(object):

    def __init__(self):
        self.b = nxt.locator.find_one_brick()
        self.mc = MotCont(self.b)


    def wait_until_motors_ready(self):
        ready  = ( self.mc.is_ready(0) and self.mc.is_ready(1) )
        while not ready:
            # print "Not ready, motors still executing last command"
            ready  = ( self.mc.is_ready(0) and self.mc.is_ready(1) )





    def main(self):
        self.mc.start()
        time.sleep(0.2)

        # self.turn_in_place(-90)
        # time.sleep(0.2)
        # self.wait_until_motors_ready()


        self.move_forward(20.0)
        time.sleep(0.2)
        self.wait_until_motors_ready()

        self.turn_in_place(180)
        time.sleep(0.2)
        self.wait_until_motors_ready()

        self.move_forward(20.0)
        time.sleep(0.2)
        self.wait_until_motors_ready()

        self.turn_in_place(180)
        time.sleep(0.2)
        self.wait_until_motors_ready()

        self.mc.stop()
        


        # light = Light(self.b, PORT_1)
        # light.set_illuminated(True)
        # # self.turn_in_place(-90)
        # # motor_a = self.mc.is_ready(0)
        # # print "motor_a", motor_a
        # # time.sleep(2)
        # # motor_a = self.mc.is_ready(0)
        # # print "motor_a", motor_a
        # reflected_light = light.get_sample()

        # while True:
        #     reflected_light = light.get_sample()
        #     print "reflected light value: ", reflected_light

        #     if reflected_light > 500:
        #         self.mc.stop()
        #         print "lost line, stopping motion"
        #         break
        

        # self.stop_motion()
        # self.move_backward(10.0)    



        # for i in range(10):
        #     print "Light sensor reading: ", light.get_sample()
        #     time.sleep(0.1)

        # light.set_illuminated(False)


    #     except KeyboardInterrupt:
    #         sys.exit(1)

    def __servo_rotation(self, distance):
        wheel_diameter = 2.221
        return (180.0 * distance) / (math.pi * wheel_diameter / 2.0)
        
    def start_motion(self):
        self.mc.start()


    def stop_motion(self):
        self.mc.stop()
        # self.mc.set_output_state(0, 0, 0)
        # self.mc.set_output_state(1, 0, 0)


    def move_forward(self, distance, power = 50):
        wheel_rotation = self.__servo_rotation(distance)
        self.mc.cmd(3, power, int(wheel_rotation))
                

    def move_backward(self, distance, power = 50):
        wheel_rotation = self.__servo_rotation(distance)
        self.mc.cmd(3, -power, int(wheel_rotation))


    def turn_in_place(self, yaw, power = 50):
        axle_length = 4.5
        wheel_distance = (math.pi / 180.0) * abs(yaw) * (axle_length / 2.0)
        
        wheel_rotation = self.__servo_rotation(wheel_distance)

        if (yaw > 0):
            self.mc.cmd(0, power, int(wheel_rotation))
            self.mc.cmd(1, -power, int(wheel_rotation))
        elif (yaw < 0):
            self.mc.cmd(0, -power, int(wheel_rotation))
            self.mc.cmd(1, power, int(wheel_rotation))

        else:
            print "+++ melon melon melon +++"
            
        # self.mc.cmd(3, power, int(wheel_rotation))




if __name__=='__main__':
    robot = BasicMotion()
    robot.main()
        



    # print "turn left"
    # mc.cmd(0, 50, 360)
    # mc.cmd(1, 150, 360)

    # time.sleep(1)
    # print "now turn right"
    # mc.cmd(0, 150, 360)
    # mc.cmd(1, 50, 360)



    # mc.stop()

    




    # while True:
    #     try:
    #         print "Light sensor reading: ", light.get_sample()
    #         time.sleep(0.1)
    #     except KeyboardInterrupt:
    #         light.set_illuminated(False)
    #         sys.exit(1)




# def spin_around(b):
#     m_left = Motor(b, PORT_A)
#     m_right = Motor(b, PORT_B)
#     m_both = Motor(b, PORT_AB)

#     # m_left.turn(100, 360)
#     # m_right.turn(-100, 360)
#     m_both.turn(100, 360)
