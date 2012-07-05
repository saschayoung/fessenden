#!/usr/bin/env python

from nxt.sensor import *



class ColorSensor(object):
    """
    NXT color sensor object.

    """
        
    def __init__(self, brick):
        """
        Initialize color sensor

        Parameters
        ----------
        brick : obj
            NXT brick connection object.

        """
        self.color = Color20(brick, PORT_2)
        self.color.set_light_color(13)


    def get_color_reading(self):
        """
        Get color value from NXT color sensor.

        Returns
        -------
        out : int
            Value of color observed by color sensor.
            
        """
        return self.color.get_sample()


    def kill_color_sensor(self):
        """
        Turn off NXT color sensor

        """
        self.color.set_color(17)
