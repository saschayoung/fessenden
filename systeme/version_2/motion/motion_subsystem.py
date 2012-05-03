#!/usr/bin/env python

"""
Module: motion_subsystem

Threaded AV motion subsystem
"""

import threading
import time

import numpy as np

from motion_base import MotionBase

DEBUG = True

class MotionSubsystem(threading.Thread):
    """
    Threaded AV motion subsystem.

    Enables threaded operation of motion.

    """

    def __init__(self, knowledge_base, lock):
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

        self.stop_event = threading.Event()

        self.motion = MotionBase()
        

    def run(self):
        """
        Run the motion subsystem.

        Start the threaded motion subsystem using `MotionSubsystem.start()`.

        """
        

        path = [(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,1)]
        

        while not self.stop_event.isSet():
            for p in path:
                self.__general_motion(p[0],p[1], speed = 25)
            



    def join(self, timeout=None):
        """
        Stop radio subsystem.

        """
        self.motion.shutdown()

        self.stop_event.set()
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
        coords = self.kb.get_state()['node_coordinates']
        src = coords[str(source)]
        dst = coords[str(destination)]
        angle = np.arctan2(dst[0] - src[0], dst[1] - src[1]) * 180/np.pi
        if np.abs(angle) >= 40 and np.abs(angle) < 50:
            self.motion.turn_onto_new_path(angle)
        self.__simple_motion(dst, speed)
        
        

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
        current_location = self.kb.get_state()['current_location']

        while not location == current_location:
            motion_status = self.__follow_line_until_location(location, speed)
            if motion_status == 'line lost':
                self.motion.find_line()
            elif motion_status == 'arrived at target':
                break
            else:
                print "__simple_motion() error"

                




    def __follow_line_until_location(self, location, speed):
        """
        Follow line.

        This function moves in a forward direction following a
        line. If the line disappears, forward motion stops. The
        presence of the line is based on readings from the light
        sensor.

        """
        if DEBUG:
            print "Following line"
        self.motion.go_forward(speed)
        while True:
            if not self.motion.line_detected():
                self.motion.halt_motion()
                return 'line lost'
            current_location = self.kb.get_state()['current_location']

            if location == int(current_location):
                self.motion.halt_motion()
                return 'arrived at target'






    # def move_until_location(self, location, speed):
    #     state = self.kb.get_state()
    #     current_location = state['current_location']
        
    #     while not location == current_location:
    #         motion_status = self.follow_line_until_location(location, speed)
    #         if motion_status == 'line lost':
    #             self.find_line()
    #         elif motion_status == 'arrived at target':
    #             break
    #         else:
    #             print "move_until_location() error"


        # while not destination == current_location:
        #     self.motion.go_forward(speed)
        #     while True:
        #         if not self.motion.line_detected():
        #             self.motion.halt_motion()
        #             if DEBUG:
        #                 print "line_lost"
        #             self.find_line()
        #             continue
        #         self.


        # state = self.kb.get_state()
        # current_location = state['current_location']
        
        # while not location == current_location:
        #     self.__move_forward(speed)
        #     while True:
        #         if not self.__line_detected():
        #             self.halt_motion()
        #             self.find_line()
        #         current_location = self.kb.get_state()['current_location']

        #         if location == int(current_location):
        #             self.halt_motion()
        #             return 'arrived at target'
        #         motion_status = self.follow_line_until_location(location, speed)



        #     if motion_status == 'line lost':
        #         self.find_line()
        #     elif motion_status == 'arrived at target':
        #         break
        #     else:
        #         print "move_until_location() error"






        # self.__move_forward(speed)
        # while True:
        #     if not self.__line_detected():
        #         self.halt_motion()
        #         return 'line lost'
        #     current_location = self.kb.get_state()['current_location']

        #     if location == int(current_location):
        #         self.halt_motion()
        #         return 'arrived at target'

