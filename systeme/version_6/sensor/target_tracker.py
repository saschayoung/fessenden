#!/usr/bin/env python

# import logging

from nxt.sensor import *

import numpy as np


class TargetTracker(object):
    """
    NXT color sensor object.

    """
        
    def __init__(self, brick, X='yellow', Y='red'):
        """
        Initialize color sensor

        Parameters
        ----------
        brick : obj
            NXT brick connection object.
        X : str
            Color used to represent `targets`. One of
            {`black` | `blue` | `green` | `yellow` | `red` | `white` }.
        Y : str
            Color used to represent `anti_targets`. One of
            {`black` | `blue` | `green` | `yellow` | `red` | `white` }.

        """
        self.sensor = Color20(brick, PORT_2)
        self.target_color = self._color_to_number(X)
        self.anti_target_color = self._color_to_number(Y)

        self.sensor.set_light_color(13)
        
        self.tracking_array = []




    def _color_to_number(self, color):
        """
        Convert color in string form to number.

        Parameters
        ----------
        color : str
            Name of color.

        Returns
        -------
        out : int
            Corresponding integer value of `color`.

        """
        if color == 'black':
            return 1
        elif color == 'blue':
            return 2
        elif color == 'green':
            return 3
        elif color == 'yellow':
            return 4
        elif color == 'red':
            return 5
        else: # color == 'white'
            return 6
        
        
        

    def _get_value(self):
        """
        Get color value from NXT color sensor.

        Returns
        -------
        out : int
            Value of color observed by color sensor.
            
        """
        return self.sensor.get_sample()





    def kill_sensor(self):
        """
        Turn off NXT color sensor

        """
        self.sensor.set_light_color(17)





    def reset(self):
        """
        Reset coounters.

        """
        self.tracking_array = []


    def run(self):
        """
        Count targets and anti_targets.

        """
        r = self._get_value()
        # print r
        self.tracking_array.append(r)
        # = np.append(self.tracking_array, self._get_value())


    def tally_results(self):
        """
        Count up results.

        This function counts up the results of the target (and
        anti_target) tracking.

        Returns
        -------
        x : int
            Number of targets tracked.
        y : int
            Number of anti_targets tracked.

        """
        # print self.tracking_array
        # logging.info("target_tracker::tally_results: tracking_array = %d" %(x,))
        
        a = np.array(self.tracking_array)
        b = np.array(self.tracking_array)

        a[a!=self.target_color] = 0
        b[b!=self.anti_target_color] = 0

        # print a
        # print b
        x = 0
        for i in range(len(a)-2):
            if (a[i] == 0) and (a[i+1] == self.target_color)and (a[i+2] == self.target_color):
                x += 1
        y = 0
        for i in range(len(b)-2):
            if (b[i] == 0) and (b[i+1] == self.anti_target_color) and (b[i+2] == self.anti_target_color):
                y += 1


        return x, y

