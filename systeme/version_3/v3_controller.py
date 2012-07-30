#!/usr/bin/env python

import logging
import time


import utils 
from cognition.decision_making import DecisionMaker    
from location.location import Location
from motion.motion_subsystem import MotionSubsystem
from radio.radio_subsystem import RadioSubsystem
from route.new_path import Path
from sensor.target_tracker import TargetTracker






class Controller(object):

    def __init__(self):
        logging.basicConfig(filename='example.log',level=logging.DEBUG)

        self.current_location = 0
        brick = utils.connect_to_brick()

        self.cognition = DecisionMaker()
        self.location = Location(self.location_callback)
        self.motion = MotionSubsystem(brick)
        self.radio = RadioSubsystem(self.radio_update_flag, self.radio_update_data,
                                    self.radio_reconfig_flag)
        self.tracker = TargetTracker(brick)


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


    def radio_update_flag(self, flag=False):
        """
        Callback for radio subsystem.

        This function simply sets a flag true or false, to indicate if
        there is data from the radio subsystem.

        Parameters
        ----------
        flag : bool
            `True` if radio subsystem has passed data through the
            `radio_callback_data`.

        """
        self.radio_update_flag = flag


    def radio_update_data(self, tx_packets=0, rx_packets=0, rssi=0):
        """
        Callback for radio subsystem.

        This function is used for the radio susbsytem to pass data
        back to the controller.

        Parameters
        ----------
        tx_packets : int
            Number of streamed packets sent by radio.
        rx_packets : int
            Number of streamed packets received by Node B.
        rssi : int

        """
        self.tx_packets = tx_packets
        self.rx_packets = rx_packets
        self.rssi = rssi
        

    def radio_reconfig_flag(self, flag=False):
        """
        Callback for radio subsystem.

        This function is use by the radio subsystem to indicate that a
        reconfiguration request has been acknowledged by Node B.

        Parameters
        ----------
        flag : bool
            `True` if radio subsystem has received an acknowledgment from
            Node B for a reconfiguration request.

        """
        self.flag = flag
        

        
    def build_route(self):
        path_a = Path(name='A', distance=62.0, direction='left')
        path_b = Path(name='B', distance=48.0, direction='straight')
        path_c = Path(name='C', distance=87.5, direction='right')
        self.paths = [path_a, path_b, path_c]


    def run(self):
        """
        Run AV controller.

        """
        self.build_route()
        self.location.start()
        self.motion.start()
        self.fsm()
 

    def shutdown(self):
        """
        Shutdown subsytems before stopping.

        """
        self.tracker.kill_sensor()
        self.motion.join()
        self.location.join()  # shut this down last



    def fsm(self):
        """
        AV finite state machine.

        """
        fsm_state = 'first_time'
        start = 1
        destination = 2
        

        while True:
            if fsm_state == 'first_time':
                self.motion.set_direction('straight')
                self.motion.set_speed(25)
                self.motion.set_state('go')

                while not self.current_location == start:
                    time.sleep(0.01)
                else:
                    self.motion.set_state('stop')
                    time.sleep(0.1)
                    fsm_state = 'before_traverse'
                    continue


            if fsm_state == 'before_traverse':
                i = self.cognition.choose_path(self.paths)
                current_path = self.paths[i]
                fsm_state = 'traverse_path'
                continue
                

            if fsm_state == 'traverse_path':
                logging.info("v3_controller::fsm: motion.set_State('go')")
                
                self.motion.set_direction(current_path.direction)
                self.motion.set_speed(25)
                self.motion.set_state('go')
                tic = time.time()

                while not self.current_location == destination:
                    self.tracker.run()
                    time.sleep(0.1)
                else:
                    self.motion.set_state('stop')
                    toc = time.time()
                    x, y = self.tracker.tally_results()
                    self.tracker.reset()
                    fsm_state = 'after_traverse'
                    continue


            if fsm_state == 'after_traverse':
                current_path.has_been_explored = True
                current_path.current_meters['X'] = x
                current_path.current_meters['Y'] = y
                current_path.solution_as_observed['T'] = toc - tic

                fsm_state = 'go_to_beginning'
                continue



            if fsm_state == 'go_to_beginning':
                self.motion.set_direction('straight')
                self.motion.set_speed(55)
                self.motion.set_state('go')

                while not self.current_location == start:
                    time.sleep(0.01)
                else:
                    self.motion.set_state('stop')
                    time.sleep(0.1)
                    fsm_state = 'before_traverse'
                    continue

            




        
        

if __name__ == '__main__':
    main = Controller()
    try:
        main.run()
    except KeyboardInterrupt:
        pass
    finally:
        main.shutdown()


    # main.run()
    





    # def profile_speed(self):
    #     """
    #     Determine actual speed of AV.

    #     """
    #     speed = 75
    #     start = 1
    #     destination = 2
    #     while True:
    #         if self.fsm_state == 'beginning':
    #             self.motion.set_speed(speed)
    #             self.motion.set_state('go')
    #             while not self.current_location == start:
    #                 time.sleep(0.01)
    #             else:
    #                 self.motion.set_state('stop')
    #                 time.sleep(0.1)

    #                 self.fsm_state = 'traverse_path'
    #                 continue

    #         if self.fsm_state == 'traverse_path':
    #             print "fsm: motion.set_State('go')"

    #             self.motion.set_speed(speed)
    #             self.motion.set_state('go')
    #             tic = time.time()
                
    #             while not self.current_location == destination:
    #                 time.sleep(0.01)

    #             else:
    #                 self.motion.set_state('stop')
    #                 toc = time.time()
    #                 print "speed = %d   time = %f" %(speed, toc-tic)

    #             break
        
