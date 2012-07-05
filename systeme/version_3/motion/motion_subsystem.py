#!/usr/bin/env python

import threading
import time

class MotionSubsystem(threading.Thread):
    """
    Threaded vehicle motion subsytem.

    Enables threaded vehicle motion.

    """

    def __init__(self, callback):
        """
        Extend threading class.

        Parameters
        ----------
        callback : object
            Callback to parent (calling) function.

        """
        threading.Thread.__init__(self)
        self.stop_event = threading.Event() 
        self.callback = callback


    def set_state(self, state):
        """
        Set state of motion subsystem finite state machine.

        This function provides a method of controlling operation of
        the motion subsystem.

        Parameters
        ----------
        state : str
            One of {`stop` | `go` }.

        """
        if state not in ['stop', 'go']:
            print "State error: `state` must be one of  {`stop` | `go` }."
            raise ValueError
        self.state = state


    def run(self):
        """
        Run the motion subsystem.

        Start the threaded motion subsystem using `MotionSubsystem.start()`.

        """
        while not self.stop_event.isSet():
            if self.state == 'stop':
                if DEBUG:
                    print "motion: stop"
                time.sleep(0.1)
                continue

            if self.state  == 'go':
                print "motion: go"
                self.
                continue



    def join(self, timeout=None):
        """
        Stop radio subsystem.

        """
        self.stop_event.set()
        threading.Thread.join(self, timeout)







    def set_destination(self, destination):
        """
        Set vehicle destination.

        Parameters
        ----------
        current_location : int
            Value of barcode representing destination.

        """
        self.destination = destination


    def set_speed(self, speed):
        """
        Set vehicle speed.

        Parameters
        ----------
        speed : int
            Vehicle speed

        """
        self.speed = speed


    def update_location(self, current_location):
        """
        Update vehicle location.

        This function is used by the controller to update the current
        location for the motion subsystem.

        Parameters
        ----------
        current_location : int
            Value of barcode representing current location.
        
        """
        self.currrent_location = current_location
