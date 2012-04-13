#!/usr/bin/env python

import math
import time
import sys


import nxt.locator
from nxt.sensor import *
from nxt.motcont import MotCont





class BasicMotion(object):

    def __init__(self):
        self.is_started = False
        self.is_stopped = True

        self.b = nxt.locator.find_one_brick()
        self.mc = MotCont(self.b)


    def wait_until_motors_ready(self):
        ready  = ( self.mc.is_ready(0) and self.mc.is_ready(1) )
        while not ready:
            # print "Not ready, motors still executing last command"
            ready  = ( self.mc.is_ready(0) and self.mc.is_ready(1) )

    



    def run(self):
        self.start_motion()
        

        self.init_light_sensor()

        while True:
            self.follow_line()
            self.find_line()





    def follow_line(self):
        print "is_started: ", self.is_started
        self.start_motion()
        print "is_started: ", self.is_started
        self.wait_until_motors_ready()

        print "following line"
        self.move_forward(150.0)
        while True:
            reflected_light = self.get_light_reading()
            if reflected_light > 500:
                self.stop_motion()
                print "lost line, stopping motion"
                return



    def find_line(self):
        print "is_started: ", self.is_started
        self.start_motion()
        print "is_started: ", self.is_started
        self.wait_until_motors_ready()

        print "finding line"
        sweep_angle = [-10, 20, -30, 40, -60, 80, -120, 160, -240, 320]
        line_found = False
        is_turning = True

        while not line_found:
            for sweep in sweep_angle:
                self.turn_in_place(sweep)
                is_turning = True

                while is_turning:
                    reflected_light = self.get_light_reading()
                    if reflected_light < 400:
                        line_found = True
                        self.stop_motion()
                        print "found line, stopping search"
                        return

                    motor_a_ready = self.mc.is_ready(0)
                    if motor_a_ready:
                        is_turning = False
            
                
                    
        



    def init_light_sensor(self):
        self.light = Light(self.b, PORT_1)


    def get_light_reading(self, illumination=True):        
        self.light.set_illuminated(illumination)
        return self.light.get_sample()
        


    def __servo_rotation(self, distance):
        wheel_diameter = 2.221
        return (180.0 * distance) / (math.pi * wheel_diameter / 2.0)
        

    def start_motion(self):
        if self.is_started == False:
            self.mc.start()
            self.is_started = True
            time.sleep(0.5)
        else:
            pass


    def stop_motion(self):
        self.mc.stop()
        self.is_started = False
        time.sleep(0.2)


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
            







if __name__=='__main__':
    robot = BasicMotion()
    robot.run()






        # self.move_forward(50.0)

        # while True:
        #     reflected_light = self.get_light_reading()
        #     # print "reflected light value: ", reflected_light
        #     if reflected_light > 500:
        #         self.mc.stop()
        #         print "lost line, stopping motion"
        #         time.sleep(1)
        #         break
        
        # self.start_motion()


        # self.turn_in_place(-10)
        # for i in range(100):
        #     reflected_light = self.get_light_reading()
        #     print "reflected light value: ", reflected_light


        # self.turn_in_place(-90)
        # time.sleep(2)
        # motor_a = self.mc.is_ready(0)
        # print "motor_a", motor_a




        # self.stop_motion()
        # self.move_backward(10.0)    



        # for i in range(10):
        #     print "Light sensor reading: ", light.get_sample()
        #     time.sleep(0.1)

        # light.set_illuminated(False)


    #     except KeyboardInterrupt:
    #         sys.exit(1)

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
