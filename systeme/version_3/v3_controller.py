#!/usr/bin/env python

import time

import utils 


    
from location.location import Location

from motion.motion_subsystem import MotionSubsystem
from route.path import Path
from sensor.target_tracker import TargetTracker




class Controller(object):

    def __init__(self):
        self.current_location = 0
        self.fsm_state = 'beginning'
        brick = utils.connect_to_brick()
        
        self.tracker = TargetTracker(brick)
        self.location = Location(self.location_callback)
        self.motion = MotionSubsystem(brick)


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



    def build_route(self):
        self.path_a = Path(name='A', distance=62.0, direction='left')
        self.path_b = Path(name='B', distance=48.0, direction='straight')
        self.path_c = Path(name='C', distance=87.5, direction='right')






    def run(self):
        """
        Run AV controller.

        """
        self.location.start()
        self.motion.start()
        self.profile_speed()
        # self.fsm()
 

    def shutdown(self):
        """
        Shutdown subsytems before stopping.

        """
        self.tracker.kill_sensor()
        self.motion.join()
        self.location.join()  # shut this down last




    def profile_speed(self):
        """
        Determine actual speed of AV.

        """
        speed = 75
        start = 1
        destination = 2
        while True:
            if self.fsm_state == 'beginning':
                self.motion.set_speed(speed)
                self.motion.set_state('go')
                while not self.current_location == start:
                    time.sleep(0.1)
                else:
                    self.motion.set_state('stop')
                    self.fsm_state = 'traverse_path'
                    break

            if self.fsm_state == 'traverse_path':
                print "fsm: motion.set_State('go')"

                self.motion.set_speed(speed)
                self.motion.set_state('go')
                tic = time.time()
                
                while not self.current_location == destination:
                    time.sleep(0.01)

                else:
                    self.motion.set_state('stop')
                    toc = time.time()
                    print "speed = %d   time = %f" %(speed, toc-tic)

                break
        



    def fsm(self):
        """
        AV finite state machine.

        """
        start = 1
        destination = 2
        while True:
            if self.fsm_state == 'beginning':
                self.motion.set_speed(25)
                self.motion.set_state('go')
                
                self.fsm_state = 'traverse_path'
                continue

            if self.fsm_state == 'traverse_path':
                print "fsm: motion.set_State('go')"
                self.motion.set_speed(25)
                self.motion.set_state('go')
                
                while not self.current_location == destination:
                    self.tracker.run()
                    time.sleep(0.1)

                else:
                    self.motion.set_state('stop')
                    x, y = self.tracker.tally_results()
                    self.tracker.reset()
                    print "Targets found = %d" %(x,)
                    print "Anti-targets found = %d" %(y,)

                break
        
        

if __name__ == '__main__':
    main = Controller()
    try:
        main.run()
    except KeyboardInterrupt:
        pass
    main.shutdown()



