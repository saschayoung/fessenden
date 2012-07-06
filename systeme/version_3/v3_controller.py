#!/usr/bin/env python

import time

import utils 

from sensor.color_sensor import ColorSensor

    
from location.location import Location

from motion.motion_subsystem import MotionSubsystem





class Controller(object):

    def __init__(self):
        self.current_location = 0
        self.fsm_state = 'beginning'
        brick = utils.connect_to_brick()
        
        self.color = ColorSensor(brick)
        self.location = Location(self.location_callback)
        self.motion = MotionSubsystem(self.motion_callback, brick)


    def location_callback(self, current_location):
        """
        Callback for location module.

        This function is used by the location module to relay the
        current location--as read by the barcode reader--back to the
        controller.

        Parameters
        ----------
        current_location : int
            Value of barcode representing current location.

        """
        self.current_location = current_location



    def run(self):
        """
        Run AV controller.

        """
        self.location.start()
        self.motion.start()
        self.fsm()


    def shutdown(self):
        """
        Shutdown subsytems before stopping.

        """
        self.color.kill_color_sensor()
        self.location.join()  # shut this down last



    def fsm(self):
        destination = 7
        while True:
            if self.fsm_state == 'beginning':
                self.fsm_state = 'traverse_path'
                continue

            if self.fsm_state == 'traverse_path':
                print "fsm: motion.set_State('go')"
                self.motion.set_state('go')
                while True:
                    if self.current_location == destination:
                        print "current_location = %s" %(self.current_location,)
                        self.motion.set_state('stop')
                        break
                    else:
                        continue
                print "arrived at destination"
                break
        
        

if __name__ == '__main__':
    main = Controller()
    try:
        main.run()
    except KeyboardInterrupt:
        pass
    main.shutdown()






    # def motion_callback(self, has_arrived):
    #     """
    #     Callback for motion module.

    #     This function is used by the motion subsystem to relay the
    #     current status--whether the robot has arrived at the desired
    #     destination--back to the controller.

    #     Parameters
    #     ----------
    #     has_arrived : bool
    #         `True` if robot has arrived at desired destination.

    #     """
    #     self.has_arrived = has_arrived


# class Test(object):

#     def __init__(self):
#         brick = utils.connect_to_brick()
#         self.color = ColorSensor(brick)

#     def run(self):
#         print self.color.get_color_reading()

#     def shutdown(self):
        
#         self.color.kill_color_sensor()




