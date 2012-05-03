#!/usr/bin/env python


import time

import numpy as np

import nxt.locator
from nxt.motor import *
from nxt.sensor import *


DEBUG = False

class SimpleMotion(object):

    def __init__(self, knowledge_base, lock,
                 wheel_diameter = 2.221,
                 axle_length = 4.5,
                 left_motor_port = 'A',
                 right_motor_port = 'B',
                 light_sensor_port = '1'):
        """
        Basic motion control for Lego Mindstorms NXT brick using `nxt-python`.

        Parameters
        ----------
        knowledge_base : object
            Handle to shared knoweldge base.
        lock : object
            File lock for concurrent access to knowledge base.
        wheel_diameter : float, opt
            Diameter of wheel(s) in inches.
        axle_length : float, opt
            Distance between wheels in inches.
        left_motor : str, opt
            Port of NXT brick to which left motor is connected, a single
            character string, one of {`A`|`B`|`C`}.
        right_motor : str, opt
            Port of NXT brick to which right motor is connected, a single
            character string, one of {`A`|`B`|`C`}.
        light_sensor : str, opt
            Port of NXT brick to which light sensor is connected, a single
            character string, one of {`1`|`2`|`3`|`4`}.

        Raises
        ------
        ValueError : If `left_motor_port` not in ['A', 'B', 'C'], or
        `right_motor_port` not in ['A', 'B', 'C'], or
        `light_sensor_port` not in ['1', '2', '3', '4'].
        

        """
        self.kb = knowledge_base

        if left_motor_port not in ['A', 'B', 'C']:
            print "`left_motor_port` must be one of {`A`|`B`|`C`}."
            raise ValueError

        if right_motor_port not in ['A', 'B', 'C']:
            print "`right_motor_port` must be one of {`A`|`B`|`C`}."
            raise ValueError

        if left_motor_port == right_motor_port:
            print "`left_motor_port` and `right_motor_port` can not share the same port."
            raise ValueError

        if light_sensor_port not in ['1', '2', '3', '4']:
            print "light_sensor_port must be one of {`1`|`2`|`3`|`4`}."
            raise ValueError
        
        self.wheel_diameter = wheel_diameter
        self.axle_length = axle_length
        self.left_motor_port = left_motor_port
        self.right_motor_port = right_motor_port
        self.light_sensor_port = light_sensor_port

        self.brick = nxt.locator.find_one_brick()
        self.__init_motors()
        self.__init_light_sensor()
        self.__init_color_sensor()


    def __init_motors(self):
        """
        Initialize motors.

        This function initializes the left and right motors.
        This is a private/internal function.

        """
        # if self.left_motor_port == 'A':
        #     left = PORT_A
        # elif self.left_motor_port == 'B':
        #     left = PORT_B
        # else:
        #     left = PORT_C

        # if self.right_motor_port == 'A':
        #     right = PORT_A
        # elif self.right_motor_port == 'B':
        #     right = PORT_B
        # else:
        #     right = PORT_C

        # self.motor_left = Motor(self.brick, left)
        # self.motor_right = Motor(self.brick, right)

        self.motor_left = Motor(self.brick, PORT_A)
        self.motor_right = Motor(self.brick, PORT_B)
            

    def __init_light_sensor(self):
        """
        Initialize light sensor.

        This function initializes the light sensor and enables illumnination.
        This is a private/internal function.

        """
        if self.light_sensor_port == '1':
            l = PORT_1
        elif self.light_sensor_port == '2':
            l = PORT_2
        elif self.light_sensor_port == '3':
            l = PORT_3
        else:
            l = PORT_4

        self.light = Light(self.brick, l)
        self.light.set_illuminated(True)



    def __init_color_sensor(self):
        """
        Initialize light sensor.

        This function initializes the light sensor and enables illumnination.
        This is a private/internal function.

        """
        self.color = Color20(self.brick, PORT_2)




    def __kill_light_sensor(self):
        """
        Shutdown light sensor.

        This function turns off the illumination of the light sensor.

        """
        self.light.set_illuminated(False)



    def __kill_color_sensor(self):
        """
        Shutdown light sensor.

        This function turns off the illumination of the light sensor.

        """
        self.color.set_light_color()
        

    def __motors_busy(self):
        """
        Determine whether the motors are busy.

        This function determines whether the motors are currently in use.
        This is done by reading the current run_state of each motor.
        This is a private/internal function.

        Returns
        -------
        out : bool
            `True` if run_state of both motors is 0, `False` otherwise.
        """
        state  = self.motor_left._read_state()
        left_run_state = state[0].run_state
        state  = self.motor_right._read_state()
        right_run_state = state[0].run_state
        if (left_run_state == 0 and right_run_state == 0):
            return False
        else:
            return True


    
    def __calculate_motor_rotation(self, distance):
        """
        Calculate servo rotation.

        This function calculates the required angle to turn the
        motor/wheel in order to travel distance `distance`.
        This is a private/internal function.

        Parameters
        ----------
        distance : float
            Desired distance to travel.
        

        Returns
        -------
        out : float
            The required angle to turn the motor/wheel in order to
            travel distance `distance`.

        """
        # if DEBUG:
        #     print "motor rotation: ", 

        return (180.0 * distance) / (np.pi * (self.wheel_diameter / 2.0))

    

    def __get_light_reading(self, illumination = True):
        """
        Get reflected light reading.

        This function determines the reflected light observed by the
        light sensor. The illumination has been known to turn off when
        not in use, so we endure that the sensor illumination is enabled.
        This is a private/internal function.

        Parameters
        ----------
        illumination : bool, opt
            Whether to enable light sensor illumination.

        Returns
        -------
        out : int
            Value of reflected light from light sensor.

        """
        self.light.set_illuminated(illumination)
        return self.light.get_sample()



    def get_color_reading(self):
        """
        Get reflected light reading.

        This function determines the reflected color observed by the
        color sensor. 

        Returns
        -------
        out : int
            Value of reflected color from color sensor.

        """
        return self.color.get_sample()


    def __line_detected(self, threshold = 500):
        """
        Detect line.

        This function uses the light sensor readings to determine if
        there is a line to follow. This is a private/internal method.

        Parameters
        ----------
        threshold : int, opt
            The value below which indicates line found, above which
            indicates line not found.

        Returns
        -------
        out : bool
            `True` if line found, `False` otherwise.

        """
        if (self.__get_light_reading() < threshold):
            return True
        else:
            return False


    def __move_forward(self, power = 25, regulated = True):
        """
        Move forward forever.

        This function is responsible for forward motion, causing the motors
        to run indefinitely, until the motors are stopped by a `__halt_motion`
        command. Motors *should* synchronize for forward motion in a straight
        line. This is a private/internal function.

        Paramters
        ---------
        power : int, opt
            Speed of forward motion: 5 >= power >= 128.
        regulate : bool, opt
            If regulated == True, motors are supposed to synchronize for forward
            motion in a straight line.

        Raises
        ------
        ValueError : If not ( 5 >= power >= 128 ).

        """
        if (power < 5) or (power > 128):
            print "`power` must be: 5 >= power >= 128"
            raise ValueError
        self.motor_left.run(power, regulated)
        self.motor_right.run(power, regulated)


    def __go_forward_n(self, n, power = 75):
        """
        Move forward n inches.

        This function implements forward motion for a predetermined
        distance `n` in inches. This ia a private/internal function.

        Paramters
        ---------
        n : float
            Desired travel distance, in inches.
        power : int, opt
            Speed of forward motion: 64 >= power >= 128.

        Raises
        ------
        ValueError : If not ( 64 >= power >= 128 ).

        """
        if (power < 64) or (power > 128):
            print "`power` must be: 64 >= power >= 128"
            raise ValueError

        motor_rotation = self.__calculate_motor_rotation(n)
        self.motor_left.weak_turn(power, int(motor_rotation))
        self.motor_right.weak_turn(power, int(motor_rotation))


    def __turn_in_place(self, yaw, power = 75):
        """
        Turn in place.

        This function creates motion about a vertical axis, creating a
        turn in place.

        Parameters
        ----------
        yaw : float
            Turn angle about vertical axis, in degrees, measured positive
            clockwise, negative counter-clockwise.
        
        power : int, opt
            Speed of motion: 64 >= power >= 128.

        Raises
        ------
        ValueError : If not ( 64 >= power >= 128 ).

        """
        if (power < 64) or (power > 128):
            print "`power` must be: 64 >= power >= 128"
            raise ValueError

        turn_distance = (np.pi / 180.0) * abs(yaw) * (self.axle_length / 2.0)
        motor_rotation = self.__calculate_motor_rotation(turn_distance)
        if (yaw > 0):
            self.motor_left.weak_turn(power, int(motor_rotation))
            self.motor_right.weak_turn(-power, int(motor_rotation))
        elif (yaw < 0):
            self.motor_left.weak_turn(-power, int(motor_rotation))
            self.motor_right.weak_turn(power, int(motor_rotation))
        else:
            print "desired yaw angle is 0, nothing to do"




    def halt_motion(self, method = 'brake'):
        """
        Halt motion.

        This function stops the motors and halts all motion. This 
        is done by removing power and either locking the motors and
        braking or letting the motors roll free and coasting.        

        Parameters
        ----------
        method : str
            Method of braking, must be one of {`brake`|`coast`}.

        Raises
        ------
        ValueError : If `method` is not one of {`brake`|`coast`}.

        """
        if method not in ['brake', 'coast']:
            print "`method` must be one of {`brake`|`coast`}."
            raise ValueError

        if method == 'brake':
            self.motor_left.brake()
            self.motor_right.brake()
        else:
            self.motor_left.idle()
            self.motor_right.idle()



    def follow_line(self):
        """
        Follow line.

        This function moves in a forward direction following a
        line. If the line disappears, forward motion stops. The
        presence of the line is based on readings from the light
        sensor.

        """
        if DEBUG:
            print "Following line"
        self.__move_forward()
        while True:
            # print "line_detected", self.__line_detected()
            if not self.__line_detected():
                self.halt_motion()
                return





    def follow_line_until_location(self, location, speed):
        """
        Follow line.

        This function moves in a forward direction following a
        line. If the line disappears, forward motion stops. The
        presence of the line is based on readings from the light
        sensor.

        """
        if DEBUG:
            print "Following line"
        self.__move_forward(speed)
        while True:
            # print "line_detected", self.__line_detected()
            if not self.__line_detected():
                self.halt_motion()
                return 'line lost'
            # state = self.kb.get_state()
            # current_location = state['current_location']
            current_location = self.kb.get_state()['current_location']

            # print "Position: ", current_location
            # print "Target: ", location
            if location == int(current_location):
                self.halt_motion()
                return 'arrived at target'



    def find_line(self):
        """
        Find line.

        """
        if DEBUG:
            print "Finding line"


        # sweep_angle = [5, -10, 15, -20, 30, -40, 60, -80, 120, -160, 240, -320]
        sweep_angle = [10, -20, 30, -40, 60, -80, 120, -160, 240, -320]

        while not self.__line_detected():
            for sweep in sweep_angle:
                # print "turning %d degrees" %(sweep,)
                
                self.__turn_in_place(sweep)
                while self.__motors_busy():
                    # print "motors still working..."
                    if self.__line_detected():
                        self.halt_motion()
                        if DEBUG: 
                            print "found line, stopping search"
                        return
                    
                    
        




    def __acquire_path(self, angle):
        self.__go_forward_n(2, 75)
        state = self.motor_left._read_state()
        run_state = state[0].run_state
        while run_state != 0: 
            state = self.motor_left._read_state()
            run_state = state[0].run_state

        self.__turn_in_place(angle)
        state = self.motor_left._read_state()
        run_state = state[0].run_state
        while run_state != 0: 
            state = self.motor_left._read_state()
            run_state = state[0].run_state
        self.find_line()



    def shutdown(self):
        self.halt_motion('coast')
        self.__kill_light_sensor()
        # self.__kill_color_sensor()

    def debug_test(self):
        while True:
            self.follow_line()
            self.find_line()

    def move_until_location(self, location, speed):
        state = self.kb.get_state()
        current_location = state['current_location']
        
        while not location == current_location:
            motion_status = self.follow_line_until_location(location, speed)
            if motion_status == 'line lost':
                self.find_line()
            elif motion_status == 'arrived at target':
                break
            else:
                print "move_until_location() error"
            


    def move_from_here_to_there(self, here, there, speed = 25):
        coords = self.kb.get_state()['node_coordinates']
        # print "here: ", here
        # print "there: ", there
        src = coords[str(here)]
        dst = coords[str(there)]
        angle = np.arctan2(dst[0] - src[0], dst[1] - src[1]) * 180/np.pi
        if np.abs(angle) >= 40 and np.abs(angle) < 50:
            
            self.__acquire_path(angle)
        self.move_until_location(there, speed)






        
        
        



if __name__=='__main__':
    # import sys

    from threading import Lock
    
    from version_2.knowledge_base import KnowledgeBase
    
    kb = KnowledgeBase()
    lock = Lock()


    main = SimpleMotion(kb, lock)
    main.move_from_here_to_there(1,2)
    main.shutdown()

    # try:
    #     main.debug_test()
    # except KeyboardInterrupt:
    #     main.shutdown()
    #     # sys.exit(1)




        # while True:
        #     # print "Light reading: ", self.__get_light_reading()
        #     # print "Line detected: ", self.__line_detected()
        # # time.sleep(1)
        # # self.__go_forward_n(5)
        # # self.follow_line()
        # # while True:
        #     self.follow_line()
        #     self.find_line()
            
