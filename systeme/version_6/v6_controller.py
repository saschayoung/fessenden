#!/usr/bin/env python

import argparse
import time
import sys


import utils 
from cognition.newest_decision_making import DecisionMaker    
from location.location import Location
from motion.motion_subsystem import MotionSubsystem
from radio.radio_subsystem import RadioSubsystem
from route.new_path import Path
from sensor.target_tracker import TargetTracker






class Controller(object):

    def __init__(self):


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

        # self.iteration = 1
        self.current_m = {}
        self.previous_m = {}

        self.re_explore = False

        self.f = open('track_data', 'w')






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

        # preload values for path, bypass initial exploration
        path_a.current_meters['X'] = 5
        path_a.current_meters['Y'] = 1
        path_a.current_meters['RSSI'] = -86
        path_b.current_meters['X'] = 3
        path_b.current_meters['Y'] = 0
        path_b.current_meters['RSSI'] = -86
        path_c.current_meters['X'] = 5
        path_c.current_meters['Y'] = 3
        path_c.current_meters['RSSI'] = -86

        self.path_names = ['A', 'B', 'C'] # this is a hack


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

        self.build_route()
        self.location.start()
        self.motion.start()
        self.radio.start()
        self.fsm()
        print self.path_history
        print self.choice_history
        print self.score_history
        print self.soln_idx
        print self.current_m
        print self.previous_m
        self.shutdown()


    def shutdown(self):
        """
        Shutdown subsytems before stopping.

        """
        # self.f.close()
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
        
        convergence_iterator = 0
        self.path_history = []
        self.choice_history = []
        self.score_history = []
        self.prev_score = -10
        self.prev_param = {}
        self.prev_soln = []
        self.soln_idx = []

        iteration = 1

        while iteration < 11:


            if fsm_state == 'first_time':
            ###################################################################
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



            if fsm_state == 'before_traverse':
            ###################################################################
                if not current_path.current_meters == {}:
                    self.previous_m[name] = current_path.current_meters
                choice = self.cognition.choose_path(self.paths)

                if choice != -1:
                    current_path = self.paths[choice]
                    self.soln_idx.append('Explore')

                    current_path.current_knobs['Modulation'] = self.modulation
                    current_path.current_knobs['Rs'] = self.bitrate
                    current_path.current_knobs['EIRP'] = self.eirp
                    current_path.current_knobs['Speed'] = 25
                    self.motion.set_speed(25)

                else:
                    score, param, soln, s_i = self.cognition.solution(self.paths,
                                                                      iteration)

                    print "score: ", score
                    print "prev_score: ", self.prev_score

                    if score > self.prev_score:
                        print "current solution is better"
                        self.soln_idx.append(s_i)
                        self.score_history.append(score)

                        self.prev_score = score
                        self.prev_param = param
                        self.prev_soln = soln
                        name_of_chosen_path = param['name']
                        choice = self.path_names.index(name_of_chosen_path)
                        current_path = self.paths[choice]
                        self.choice_history.append(current_path.name)

                        current_path.current_knobs['Modulation'] = 'fsk'
                        current_path.current_knobs['EIRP'] = param['EIRP']
                        current_path.current_knobs['Rs'] = param['Rs']
                        current_path.current_knobs['Speed'] = param['rotor_power']

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
                        print "previous solution is better"

                        try:
                            name_of_chosen_path = self.prev_param['name']
                        except KeyError:
                            print "KeyError"
                            print self.prev_param
                            sys.exit(1)

                        comparison = self.compare(self.prev_param)
                        if comparison == True:
                            print "prev solution is better and old environment is unchanged"
                            convergence_iterator += 1
                            if convergence_iterator == 3:
                                convergence_iterator = 0
                                self.re_explore = True

                            self.soln_idx.append('prev result')
                            self.score_history.append(self.score_history[-1])

                            choice = self.path_names.index(name_of_chosen_path)
                            current_path = self.paths[choice]
                            self.choice_history.append(current_path.name)

                            current_path.current_knobs['Modulation'] = 'fsk'
                            current_path.current_knobs['EIRP'] = self.prev_param['EIRP']
                            current_path.current_knobs['Rs'] = self.prev_param['Rs']
                            current_path.current_knobs['Speed'] = self.prev_param['rotor_power']

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
                            print "prev solution is better but old environment has changed"
                            print "use current solution"
                            self.soln_idx.append(s_i)
                            self.score_history.append(score)

                            self.prev_score = score
                            self.prev_param = param
                            self.prev_soln = soln
                            name_of_chosen_path = param['name']
                            choice = self.path_names.index(name_of_chosen_path)
                            current_path = self.paths[choice]
                            self.choice_history.append(current_path.name)


                            current_path.current_knobs['Modulation'] = 'fsk'
                            current_path.current_knobs['EIRP'] = param['EIRP']
                            current_path.current_knobs['Rs'] = param['Rs']
                            current_path.current_knobs['Speed'] = param['rotor_power']

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








                self.motion.set_direction(current_path.direction)
                self.path_history.append(current_path.name)

                fsm_state = 'traverse_path'
                continue
            ###################################################################
                





            if fsm_state == 'traverse_path':
            ###################################################################
                if self.re_explore == True:
                    for p in self.paths:
                        p.has_been_explored = False
                    self.re_explore = False


                if not current_path.has_been_explored:
                    print "Exploring path"
                    self.radio.set_state('listen')

                else:
                    print "Exploiting path"
                    self.radio.set_state('stream')


                self.motion.set_state('go')
                tic = time.time()

                while not self.current_location == destination:
                    self.tracker.run()
                    time.sleep(0.1)
                else:
                    self.motion.set_state('stop')
                    self.radio.set_state('stop')
                    toc = time.time()
                    time.sleep(1)
                    x, y = self.tracker.tally_results() 

                    print "x = %d y = %d" %(x, y)

                    self.tracker.reset()
                    name = current_path.name
                    # self.previous_m[name] = current_path.current_meters

                    current_path.current_meters['X'] = x
                    current_path.current_meters['Y'] = y
                    current_path.solution_as_observed['T'] = toc - tic

                    fsm_state = 'after_traverse'

                    continue
            ###################################################################






            if fsm_state == 'after_traverse':
            ###################################################################
                print "updating meters"
                # for p in self.paths:
                #     p.update_meters()

                if not current_path.has_been_explored:
                    print "marking current path as explored"
                    current_path.has_been_explored = True
                    # fsm_state = 'go_to_beginning'
                    # continue
                else:
                    self.radio.set_state('update')
                    while not self.radio_update_flag:
                        time.sleep(0.1)
                    else:
                        current_path.current_meters['RSSI'] = self.rssi
                        # current_path.solution_as_observed['G'] = self.rx_packets
                        # current_path.solution_as_observed['Z'] = self.cognition.calculate_z(x, y)
                        # current_path.solution_as_observed['B'] = self.cognition.estimate_ber(self.tx_packets,
                        #                                                                      self.rx_packets)

                        name = current_path.name
                        self.current_m[name] = current_path.current_meters


                iteration += 1
                fsm_state = 'go_to_beginning'
                continue
            ###################################################################





            if fsm_state == 'go_to_beginning':
            ###################################################################
                print "current_m: ", self.current_m
                print "previous_m: ", self.previous_m
                print ""
                print "Iteration %d finished" %(iteration-1,)
                s = raw_input("AVEP has completed an iteration, press Y/y to continue ")

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
            ###################################################################

            









    def compare(self, param):
        """
        Determine if the environment has changed from one iteration to
        the next.

        """
        name = param['name']
        current_meters = self.current_m[name]
        previous_meters = self.previous_m[name]

        if current_meters['X'] != previous_meters['X']:
            print "current_meters['X'] != previous_meters['X']"
            return False
        elif current_meters['Y'] != previous_meters['Y']:
            print "current_meters['Y'] != previous_meters['Y']"
            return False
        # elif current_meters['RSSI'] == previous_meters['RSSI']:
        #     print "current_meters['Noise'] == previous_meters['Y']"
        #     return False
        else:
            return True





        
        

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
        



                # if current_path.has_been_explored:
                #     self.radio.set_config_packet_data(current_path.current_knobs['Modulation'],
                #                                       current_path.current_knobs['EIRP'],
                #                                       current_path.current_knobs['Rs'])
                #     self.radio.set_state('reconfigure')
                #     while not self.reconfig_flag:
                #         time.sleep(0.1)
                #     else:
                #         self.radio.set_current_location(self.current_location)
                #         self.radio.set_radio_configuration(current_path.current_knobs['Modulation'],
                #                                            current_path.current_knobs['EIRP'],
                #                                            current_path.current_knobs['Rs'],
                #                                            self.frequency)
                #         self.motion.set_speed(current_path.current_knobs['Speed'])
                # else:
                #     current_path.current_knobs['Modulation'] = self.modulation
                #     current_path.current_knobs['Rs'] = self.bitrate
                #     current_path.current_knobs['EIRP'] = self.eirp
                #     current_path.current_knobs['Speed'] = 25

                #     self.motion.set_speed(25)

                
                # self.motion.set_direction(current_path.direction)

                # else:
                #     # notify base station of new configuration
                #     self.radio.set_config_packet_data(current_path.current_knobs['Modulation'],
                #                                       current_path.current_knobs['EIRP'],
                #                                       current_path.current_knobs['Rs'])
                #     self.radio.set_state('reconfigure')

                #     while not self.reconfig_flag:
                #         # wait for acknowledgment
                #         time.sleep(0.1)
                #     else:
                #         # use new configuration
                #         self.radio.set_current_location(self.current_location)
                #         self.radio.set_radio_configuration(current_path.current_knobs['Modulation'],
                #                                            current_path.current_knobs['EIRP'],
                #                                            current_path.current_knobs['Rs'],
                #                                            self.frequency)
                #         self.motion.set_speed(current_path.current_knobs['Speed'])

                
                # self.motion.set_direction(current_path.direction)



                # s = "\n\n"
                # s += "Before traverse.\n"
                # s += "==================================================\n"
                # s += "Iteration %d.\n" %(self.iteration,)
                # for p in self.paths:
                #     s += "\n\nPath %s information:\n" %(p.name,)
                #     s += "Path explored yet? " + str(p.has_been_explored) + "\n"
                #     s += "solution_parameters: " + str(p.solution_parameters) + "\n"
                #     s += "solution_as_implemented: " + str(p.solution_as_implemented) + "\n"
                #     s += "previous_meters: " + str(p.previous_meters)  + "\n"
                #     s += "current_knobs: " + str(p.current_knobs)  + "\n"

                # s += "\n\nChosen path is %s.\n" %(current_path.name,)
                # s += "=================================================="
                # i = self.cognition.choose_path(self.paths)
                # current_path = self.paths[i]
                # current_path.iteration = self.iteration
                            
                # if not current_path.has_been_explored:
                #     # use default values
                #     current_path.current_knobs['Modulation'] = self.modulation
                #     current_path.current_knobs['Rs'] = self.bitrate
                #     current_path.current_knobs['EIRP'] = self.eirp
                #     current_path.current_knobs['Speed'] = 25
                #     self.motion.set_speed(25)
