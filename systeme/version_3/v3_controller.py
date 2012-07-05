#!/usr/bin/env python

import time

from utils import nxt

# from location.location import Location

# from motion.motion_subsystem import MotionSubsystem

# class Controller(object):

#     def __init__(self):
#         self.location = Location(self.location_callback)

#         brick = nxt_api.connect_to_brick()
#         self.color_sensor(brick)
        

#     def location_callback(self, current_location):
#         """
#         Callback for location module.

#         This function is used by the location module to relay the
#         current location--as read by the barcode reader--back to the
#         controller.

#         Parameters
#         ----------
#         current_location : int
#             Value of barcode representing current location.

#         """
#         self.current_location = current_location




class Test(object):

    def __init__(self):
        brick = nxt.connect_to_brick()
        self.color = Color20(brick, PORT_2)
        self.color.set_light_color(13)
        
    
    def get_color_reading(self):
        """
        Get color value from NXT color sensor.

        """
        return self.color.get_sample()


    def kill_color_sensor(self):
        """
        Turn off NXT color sensor

        """
        self.color.set_color(17)



if __name__ == '__main__':
    main = Test()
    while True:
        try:
            print main.get_color_reading()
            time.sleep(0.5)
        except KeyboardInterrupt:
            break
    main.kill_color_sensor()
