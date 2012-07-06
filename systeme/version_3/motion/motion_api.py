#!/usr/bin/env python

import numpy as np

from nxt.motor import *
from nxt.sensor import *


DEBUG = True

class MotionAPI(object):

    def __init__(self, brick):
        self.wheel_diameter = 2.221
        self.axle_length = 4.5

        self.brick = brick
        self.init_motors()
        self.init_light_sensor()



    def init_motors(self):
        self.motor_left = Motor(self.brick, PORT_A)
        self.motor_right = Motor(self.brick, PORT_B)

    def init_light_sensor(self):
        self.light = Light(self.brick, PORT_1)
        self.light.set_illuminated(True)

    def kill_light_sensor(self):
        self.light.set_illuminated(False)
    



    def motors_busy(self):
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


    def calculate_motor_rotation(self, distance):
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
        return (180.0 * distance) / (np.pi * (self.wheel_diameter / 2.0))





    def turn_in_place(self, yaw, power = 75):
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
        motor_rotation = self.calculate_motor_rotation(turn_distance)
        if (yaw > 0):
            self.motor_left.weak_turn(power, int(motor_rotation))
            self.motor_right.weak_turn(-power, int(motor_rotation))
        elif (yaw < 0):
            self.motor_left.weak_turn(-power, int(motor_rotation))
            self.motor_right.weak_turn(power, int(motor_rotation))
        else:
            print "desired yaw angle is 0, nothing to do"


    def go_forward(self, power = 25, regulated = True):
        """
        Move forward forever.

        This function is responsible for forward motion, causing the
        motors to run indefinitely, until the motors are stopped by a
        `__halt_motion` command. Control should return to calling
        function immediately. Motors *should* synchronize for forward
        motion in a straight line. This is a private/internal
        function.

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



    def line_detected(self, threshold = 500):
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
        self.light.set_illuminated(True)
        light_reading = self.light.get_sample()
        if (light_reading() < threshold):
            return True
        else:
            return False





    def find_line(self):
        """
        Find line.

        """
        if DEBUG:
            print "Finding line"
        sweep_angle = [10, -20, 30, -40, 60, -80, 120, -160, 240, -320]
        while not self.line_detected():
            for sweep in sweep_angle:
                self.turn_in_place(sweep)
                while self.motors_busy():
                    if self.line_detected():
                        self.halt_motion()
                        if DEBUG: 
                            print "found line, stopping search"
                        return
    
       
     # def shutdown(self):
     #    # self.stop_flag = True
     #    # self.halt_motion('coast')
     #    self.nxt.kill_light_sensor()
