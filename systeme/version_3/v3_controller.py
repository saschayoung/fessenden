#!/usr/bin/env python

import time

import utils 

from sensor.color_sensor import ColorSensor

class Test(object):

    def __init__(self):
        brick = utils.connect_to_brick()
        self.color = ColorSensor(brick)

    def run(self):
        print self.color.get_color_reading()

    def shutdown(self):
        
        self.color.kill_color_sensor()
    
    


if __name__ == '__main__':
    main = Test()
    while True:
        try:
            main.run()
            time.sleep(0.5)
        except KeyboardInterrupt:
            break
    main.shurdown()






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







