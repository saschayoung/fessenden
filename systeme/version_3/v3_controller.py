#!/usr/bin/env python

import argparse
import logging
import time


import utils 
from cognition.new_decision_making import DecisionMaker    
from location.location import Location
from motion.motion_subsystem import MotionSubsystem
from radio.radio_subsystem import RadioSubsystem
from route.new_path import Path
from sensor.target_tracker import TargetTracker






class Controller(object):

    def __init__(self):
        logging.basicConfig(filename='example.log', filemode='w', level=logging.DEBUG)

        self.current_location = 0
        brick = utils.connect_to_brick()

        self.cognition = DecisionMaker()
        self.location = Location(self.location_callback)
        self.motion = MotionSubsystem(brick)
        self.radio = RadioSubsystem(self.radio_update_flag, self.radio_update_data,
                                    self.radio_reconfig_flag)
        self.tracker = TargetTracker(brick)

        self.radio_update_flag = False
        self.reconfig_flag = False


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


    def radio_update_data(self, tx_packets=0, rx_packets=0, signal_strength=0):
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
        self.rssi = signal_strength
        

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
        self.reconfig_flag = flag
        

        
    def build_route(self):
        """
        Build route graph.

        """
        path_a = Path(name='A', distance=62.0, direction='left')
        path_b = Path(name='B', distance=48.0, direction='straight')
        path_c = Path(name='C', distance=87.5, direction='right')
        self.paths = [path_a, path_b, path_c]



    def run(self):
        """
        Run AV controller.

        """
        parser = argparse.ArgumentParser()
        parser.add_argument("-f", type=float, default=434e6, metavar='frequency', dest='frequency', 
                            nargs=1, help="Transmit frequency (default: %(default)s)")
        parser.add_argument("-m", type=str, default='gfsk', metavar='modulation', dest='modulation',
                            choices=['gfsk', 'fsk', 'ask'],
                            help="Select modulation from [%(choices)s] (default: %(default)s)")
        parser.add_argument("-p" "--power", type=int, default=17, metavar='power', dest='power',
                            choices=[8, 11, 14, 17],
                            help="Select transmit power from [%(choices)s] (default: %(default)s)")
        parser.add_argument("-r" "--bitrate", type=float, default=4.8e3, metavar='bitrate',
                            dest='bitrate', help="Set bitrate (default: %(default)s)")
        args = parser.parse_args()

        self.frequency = args.frequency
        self.modulation = args.modulation
        self.eirp = args.power
        self.bitrate = args.bitrate

        print "using default_settings"

        print "building route"
        self.build_route()
        print "starting location module"
        self.location.start()
        print "starting motion module"
        self.motion.start()
        print "starting radio module"
        self.radio.start()
        print "starting central fsm"
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
            ###################################################################
            if fsm_state == 'first_time':
                logging.info("v3_controller::fsm: first_time")
                
                self.motion.set_direction('straight')
                self.motion.set_speed(25)
                self.motion.set_state('go')

                while not self.current_location == start:
                    time.sleep(0.01)
                else:
                    self.motion.set_state('stop')
                    time.sleep(0.1)

                    self.radio.set_current_location(self.current_location)
                    self.radio.set_radio_configuration(self.modulation, self.eirp,
                                                       self.bitrate, self.frequency)


                    fsm_state = 'before_traverse'
                    continue
            ###################################################################



            ###################################################################
            if fsm_state == 'before_traverse':
                logging.info("v3_controller::fsm: before_traverse")
                for p in self.paths:
                    p.update_knobs()
                # self.path.update_meters()
                
                i = self.cognition.choose_path(self.paths)
                current_path = self.paths[i]

                if current_path.has_been_explored:
                    self.radio.set_config_packet_data(current_path.current_knobs['Modulation'],
                                                      current_path.current_knobs['EIRP'],
                                                      current_path.current_knobs['Rs'])
                    self.radio.set_state('reconfigure')
                    while not self.reconfig_flag:
                        time.sleep(0.1)
                    else:
                        self.radio.set_current_location(self.current_location)
                        self.radio.set_radio_configuration(current_path.current_knobs['Modulation'],
                                                           current_path.current_knobs['EIRP'],
                                                           current_path.current_knobs['Rs'],
                                                           self.frequency)
                        self.motion.set_speed(current_path.current_knobs['Speed'])
                else:
                    self.motion.set_speed(25)

                
                self.motion.set_direction(current_path.direction)

                fsm_state = 'traverse_path'
                continue
            ###################################################################
                

            ###################################################################
            if fsm_state == 'traverse_path':
                logging.info("v3_controller::fsm: traverse_path")

                self.radio.set_state('stream')
                self.motion.set_state('go')
                tic = time.time()

                while not self.current_location == destination:
                    self.tracker.run()
                    time.sleep(0.1)
                else:
                    print "stop motion"
                    self.motion.set_state('stop')
                    print "stop radio"
                    self.radio.set_state('stop')
                    toc = time.time()
                    time.sleep(1)
                    x, y = self.tracker.tally_results() 
                    logging.info("v3_controller::fsm:traverse_path: x = %d" %(x,))
                    logging.info("v3_controller::fsm:traverse_path: y = %d" %(y,))


                    self.shutdown()

                    # print "x = ", x
                    # print "y = ", y
                    self.tracker.reset()
                    current_path.current_meters['X'] = x
                    current_path.current_meters['Y'] = y
                    current_path.solution_as_observed['T'] = toc - tic

                    fsm_state = 'after_traverse'

                    # self.shutdown()
                    continue
            ###################################################################


            ###################################################################
            if fsm_state == 'after_traverse':
                # raise KeyboardInterrupt
                current_path.has_been_explored = True
                for p in self.paths:
                    p.update_meters()
                # self.path.update_meters()


                self.radio.set_state('update')
                while not self.radio_update_flag:
                    time.sleep(0.1)
                else:
                    current_path.current_meters['RSSI'] = self.rssi
                    current_path.solution_as_observed['G'] = self.rx_packets
                    current_path.solution_as_observed['Z'] = self.cognition.calculate_z(x, y)
                    current_path.solution_as_observed['B'] = self.cognition.estimate_ber(self.tx_packets,
                                                                                         self.rx_packets)

                    # TODO: add the part where we determine if the
                    # solution we used wasn any good
                


                fsm_state = 'go_to_beginning'
                continue
            ###################################################################


            ###################################################################
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
            ###################################################################

            




        
        

if __name__ == '__main__':
    main = Controller()
    try:
        main.run()
    except KeyboardInterrupt:
        main.shutdown()

    #     pass
    # finally:

























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
        
