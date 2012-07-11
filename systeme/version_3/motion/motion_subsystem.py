#!/usr/bin/env python

import threading
import time

from motion_api import MotionAPI

class MotionSubsystem(threading.Thread):
    """
    Threaded vehicle motion subsytem.

    Enables threaded vehicle motion.

    """

    def __init__(self, brick):
        """
        Extend threading class.

        Parameters
        ----------
        brick : object
            NXT brick connection object.
            
        """
        threading.Thread.__init__(self)
        self.stop_event = threading.Event() 

        self.motion = MotionAPI(brick)

        self.last_state = 'stop'
        self.current_state = 'stop'



    def set_state(self, current_state):
        """
        Set state of motion subsystem finite state machine.

        This function provides a method of controlling operation of
        the motion subsystem.

        Parameters
        ----------
        state : str
            One of {`stop` | `go` }.

        """
        if current_state not in ['stop', 'go']:
            print "State error: `current_state` must be one of  {`stop` | `go` }."
            raise ValueError
        self.current_state = current_state



    def run(self):
        """
        Run the motion subsystem.

        Start the threaded motion subsystem using `MotionSubsystem.start()`.

        """
        while not self.stop_event.isSet():
            if self.current_state == 'stop':
                if self.last_state == 'stop':
                    continue
                
                elif self.last_state == 'go':
                    self.last_state = 'stop'
                    print "motion: stop"
                    continue

                else:
                    print "Error 1 in MotionSubsystem.run()"
                    print "self.current_state == %s" %(self.current_state,)
                    print "last state == %s" %(self.last_state,)
                    continue

            if self.current_state  == 'go':
                if self.last_state == 'stop':
                    self.last_state = 'go'
                    print "motion: go"
                    self.general_motion()
                    continue
                
                elif self.last_state == 'go':
                    continue

                else:
                    print "Error 2 in MotionSubsystem.run()"
                    print "self.current_state == %s" %(self.current_state,)
                    print "last state == %s" %(self.last_state,)
                    continue



    def join(self, timeout=None):
        """
        Stop radio subsystem.

        """
        self.stop_event.set()
        self.motion.kill_light_sensor()
        threading.Thread.join(self, timeout)


    def set_direction(self, direction):
        """
        Set turn direction.

        """
        self.direction = direction


    def set_speed(self, speed):
        """
        Set vehicle speed.

        Parameters
        ----------
        speed : int
            Vehicle speed

        """
        print "speed set to %d" %(speed,)
        self.speed = speed


    def make_turn(self):
        pass
    # def turn_onto_new_path(self, angle):
    #     """
    #     Turn onto a new path.

    #     This function implements vehicle turning for path choice. Move
    #     forward a small distance and then turn in place according to
    #     `angle`. Finally reacquire path with `find_line()`.

    #     Parameters
    #     ----------
    #     angle : float
    #         Turn angle, in degrees, measured positive
    #         clockwise, negative counter-clockwise.

    #     """
        
    #     self.go_forward_n(2, 75)
    #     while self.__motors_busy():
    #         time.sleep(0.01)

    #     self.__turn_in_place(angle)
    #     while self.__motors_busy():
    #         time.sleep(0.01)

    #     self.find_line()



    def general_motion(self):
        """
        General motion.

        """
        self.motion.go_forward(self.speed)
        while True:
            if self.stop_event.isSet():
                self.motion.halt_motion()
                break
            if self.current_state == 'stop':
                self.motion.halt_motion()
                break
            if not self.motion.line_detected():
                self.motion.halt_motion()
                self.motion.find_line()
                self.motion.go_forward(self.speed)
                continue
                
            
            
            





    # def set_destination(self, destination):
    #     """
    #     Set vehicle destination.

    #     Parameters
    #     ----------
    #     current_location : int
    #         Value of barcode representing destination.

    #     """
    #     self.destination = destination




    # def update_location(self, current_location):
    #     """
    #     Update vehicle location.

    #     This function is used by the controller to update the current
    #     location for the motion subsystem.

    #     Parameters
    #     ----------
    #     current_location : int
    #         Value of barcode representing current location.
        
    #     """
    #     self.currrent_location = current_location



