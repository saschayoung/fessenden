#!/usr/bin/env python

"""
Module: motion_subsystem

Threaded AV motion subsystem
"""

import threading
import time

import numpy as np

from motion_base import MotionBase

DEBUG = False

class MotionSubsystem(threading.Thread):
    """
    Threaded AV motion subsystem.

    Enables threaded operation of motion.

    """

    def __init__(self, knowledge_base, lock, callback):
        """
        Extend threading class.

        Parameters
        ----------
        knowledge_base : object
            Handle to shared knoweldge base.
        lock : object
            File lock for concurrent access to knowledge base.
        callback : object
            Callback to parent (calling) function.

        """

        threading.Thread.__init__(self)

        self.kb = knowledge_base
        self.lock = lock
        self.callback = callback

        self.stop_event = threading.Event()

        self.motion = MotionBase(self.kb)

        self.motion_command = 'pause'
        

    def set_source_destination(self, source, destination):
        self.source = source
        self.destination = destination

    def set_speed(self, speed):
        self.speed = speed
    


    def control_motion_operation(self, command):
        """
        Contol motion operation.

        This function provides a method of controlling operation of
        the motion subsystem.

        Parameters
        ----------
        command : str
            One of {`pause` | `go` | ... }

        """
        self.motion_command = command


    def run(self):
        """
        Run the motion subsystem.

        Start the threaded motion subsystem using `MotionSubsystem.start()`.

        """
        

        
        while not self.stop_event.isSet():
            if self.motion_command == 'pause':
                if DEBUG:
                    print "motion is paused"
                time.sleep(0.1)
                continue

            if self.motion_command == 'go':
                print "motion is go"
                
                self.__general_motion(self.source, self.destination, self.speed)
                
                continue
            


            

    def join(self, timeout=None):
        """
        Stop radio subsystem.

        """
        self.stop_event.set()
        self.motion.shutdown()
        threading.Thread.join(self, timeout)





    def __general_motion(self, source, destination, speed):
        """
        High level motion.

        Move from origin to destination.

        Parameters
        ----------
        source : int
            Starting location, a graph node corresponding to the
            current location.
        destination : int
            Desired final location, corresponding to a graph node
            at the end of the current graph edge (path).
        speed : int
            Vehicle speed

        """
        if source != 0:
            coords = self.kb.get_state()['node_coordinates']
            src = coords[str(source)]
            dst = coords[str(destination)]
            angle = np.arctan2(dst[0] - src[0], dst[1] - src[1]) * 180/np.pi
            if np.abs(angle) >= 40 and np.abs(angle) < 50:
                self.motion.turn_onto_new_path(angle)
        # else:
        "simple_motion to destination node %d" %(destination,)
        self.__simple_motion(destination, speed)
        
        

    def __simple_motion(self, location, speed):
        """
        Simple motion.

        Move until arriving at destination.

        Parameters
        ----------
        location : int
            Desired final location, corresponding to a graph node
            at the end of the current graph edge (path).
        speed : int
            Vehicle speed

        """

        while True:
            if self.stop_event.isSet():
                break
            motion_status = self.motion.follow_line_advanced(location, speed)
            if motion_status == 'line lost':
                self.motion.find_line()
            elif motion_status == 'arrived at target':
                self.motion_command = 'pause'
                self.callback(True)
                break
            else:
                print "motion.__simple_motion() error"
            

        if DEBUG:
            print "motion.__simple_motion(), pausing motion"








    def color_reading(self):
        return self.motion.get_color_reading()















            

