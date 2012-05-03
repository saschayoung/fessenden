#!/usr/bin/env python

import time

import numpy as np

from nxt_base import NXTBase


DEBUG = True

class MotionBase(object):

    def __init__(self):
        self.nxt = NXTBase()
        self.nxt.init_motors()
        self.nxt.init_light_sensor()

        self.wheel_diameter = 2.221
        self.axle_length = 4.5

        

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
        state  = self.nxt.motor_left._read_state()
        left_run_state = state[0].run_state
        state  = self.nxt.motor_right._read_state()
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
        return (180.0 * distance) / (np.pi * (self.wheel_diameter / 2.0))
        

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
            self.nxt.motor_left.weak_turn(power, int(motor_rotation))
            self.nxt.motor_right.weak_turn(-power, int(motor_rotation))
        elif (yaw < 0):
            self.nxt.motor_left.weak_turn(-power, int(motor_rotation))
            self.nxt.motor_right.weak_turn(power, int(motor_rotation))
        else:
            print "desired yaw angle is 0, nothing to do"


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
        self.nxt.light.set_illuminated(illumination)
        return self.nxt.light.get_sample()

    

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
        if (self.__get_light_reading() < threshold):
            return True
        else:
            return False
        



    



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
            self.nxt.motor_left.brake()
            self.nxt.motor_right.brake()
        else:
            self.nxt.motor_left.idle()
            self.nxt.motor_right.idle()

    

    def go_forward(self, power = 25, regulated = True):
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
        self.nxt.motor_left.run(power, regulated)
        self.nxt.motor_right.run(power, regulated)



    def go_forward_n(self, n, power = 75):
        """
        Move forward n inches.

        This function implements forward motion for a predetermined
        distance `n` in inches. 

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
        self.nxt.motor_left.weak_turn(power, int(motor_rotation))
        self.nxt.motor_right.weak_turn(power, int(motor_rotation))



    def turn_onto_new_path(self, angle):
        """
        Turn onto a new path.

        This function implements vehicle turning for path choice. Move
        forward a small distance and then turn in place according to
        `angle`. Finally reacquire path with `find_line()`.

        Parameters
        ----------
        angle : float
            Turn angle, in degrees, measured positive
            clockwise, negative counter-clockwise.

        """
        
        self.__go_forward_n(2, 75)
        while self.__motors_busy():
            time.sleep(0.01)

        self.__turn_in_place(angle)
        while self.__motors_busy():
            time.sleep(0.01)

        self.find_line()



    def find_line(self):
        """
        Find line.

        """
        if DEBUG:
            print "Finding line"
        sweep_angle = [10, -20, 30, -40, 60, -80, 120, -160, 240, -320]
        while not self.line_detected():
            for sweep in sweep_angle:
                self.__turn_in_place(sweep)
                while self.__motors_busy():
                    if self.line_detected():
                        self.halt_motion()
                        if DEBUG: 
                            print "found line, stopping search"
                        return



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
        self.go_forward()
        while True:
            if DEBUG:
                print "line_detected", self.line_detected()
            if not self.line_detected():
                self.halt_motion()
                return
    

    def debug_test(self):
        while True:
            self.follow_line()
            self.find_line()


    def shutdown(self):
        self.halt_motion('coast')
        self.nxt.kill_light_sensor()



if __name__=='__main__':
    main = MotionBase()
    try:
        main.debug_test()
    except KeyboardInterrupt:
        main.shutdown()
    
