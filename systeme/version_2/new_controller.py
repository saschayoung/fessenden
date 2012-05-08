#!/usr/bin/env python

import time
from threading import Lock


import numpy as np

from knowledge_base import KnowledgeBase
from location.barcode import Location
from motion.motion_subsystem import MotionSubsystem
from radio.radio_subsystem import RadioSubsystem

DEBUG = True

class Controller(object):

    def __init__(self):
        self.lock = Lock()

        self.kb = KnowledgeBase()

        self.location = Location(self.kb, self.lock)
        self.motion = MotionSubsystem(self.kb, self.lock, self.motion_callback)
        self.rf = RadioSubsystem(self.kb, self.lock, self.radio_data_callback)

        self.fsm_state = 'at_beginning'

        self.sent_packet = np.array([])
        self.ack_packet = np.array([])
        self.goodput = np.array([])

        self.arrived = False


    def run(self):
        """
        Start the controller.

        """
        self.kb.build_route()
        self.location.start()
        self.motion.start()
        self.rf.start()
        # time.sleep(0.1)


        self.fsm()


    def motion_callback(self, has_arrived):
        self.arrived = has_arrived


    def radio_data_callback(self, sent_packet, ack_packet, goodput):
        """
        Radio Subsystem IPC.

        """
        self.sent_packet = np.append(self.sent_packet, sent_packet)
        self.ack_packet = np.append(self.ack_packet, ack_packet)
        self.goodput = np.append(self.goodput, goodput)


    def reset_radio_data(self):
        """
        Reset local radio data storage.

        """
        self.sent_packet = np.array([])
        self.ack_packet = np.array([])
        self.goodput = np.array([])


    def fsm(self):
        while True:
            if self.fsm_state == 'at_beginning':
                if DEBUG:
                    print "at_beginning"
                before_start = 0
                start_node = self.kb.get_start_node()
                self.motion.set_source_destination(before_start, start_node)
                self.motion.set_speed(25)
                self.motion.control_motion_operation('go')


                print "current_location: ", self.kb.get_state()['current_location']
                print "start_node: ", start_node
                # while not self.kb.get_state()['current_location'] == start_node:
                while not self.arrived:
                    print "current_location: ", self.kb.get_state()['current_location']
                    print "start_node: ", start_node
                    time.sleep(0.1)

                if DEBUG:
                    print "arrived at first node: %d" %(start_node,)

                next_node = self.kb.get_next_node(start_node)
                self.kb.set_current_node(start_node)
                self.kb.set_next_node(next_node)
                self.kb.set_next_edge((start_node, next_node))

                self.fsm_state = 'traversing_edge'
                # break
                continue


            elif self.fsm_state == 'traversing_edge':
                if DEBUG:
                    print "traversing_edge"

                kb_state = self.kb.get_state()
                print kb_state
                current_edge = kb_state['next_edge']

                if DEBUG:
                    print "current_edge: ", current_edge

                next_edge = None
                last_node = kb_state['current_node']
                current_node = None
                next_node = kb_state['next_node']

                self.kb.set_current_edge(current_edge)
                self.kb.set_next_edge(next_edge)
                self.kb.set_last_node(last_node)
                self.kb.set_current_node(current_node)
                
                if DEBUG:
                    print "current_edge: ", current_edge
                    print "current_edge[0]: ", current_edge[0]
                    print "current_edge[1]: ", current_edge[1]

                self.arrived = False
                self.motion.set_source_destination(current_edge[0], current_edge[1])
                self.motion.set_speed(25)
                tic = time.time()

                if DEBUG:
                    print "starting motion again"
                self.motion.control_motion_operation('go')

                if DEBUG:
                    print "waiting to reach destination"
                    print "current_location: ", self.kb.get_state()['current_location']
                    print "current_edge[1]: ", current_edge[1]
                while not self.arrived:
                # while not self.kb.get_state()['current_location'] == current_edge[1]:
                    print "current_location: ", self.kb.get_state()['current_location']
                    print "current_edge[1]: ", current_edge[1]
                    # print "\n\n\n\n"
                    # print "Blah blah blah"
                    time.sleep(0.2)

                toc = time.time() - tic
                weight = toc * np.average(self.goodput)
                if DEBUG:
                    print "weight value for edge %s = %0.2f" %(str(current_edge), weight)
                self.kb.set_edge_weight(current_edge, weight)

                self.fsm_state = 'at_a_node'
                continue


            elif self.fsm_state == 'at_a_node':
                if DEBUG:
                    print "at_a_node"
                    self.rf.control_radio_operation('pause')
                    kb_state = self.kb.get_state()
                    current_node = kb_state['next_node']
                    next_node = self.kb.get_next_node(current_node)

                    if DEBUG:
                        print "at_a_node, current_node = ", current_node
                        print "at_a_node, next_node = ", next_node

                    current_edge = None
                    last_edge = kb_state['current_edge']
                    next_edge = (current_node, next_node)

                    self.kb.set_current_node(current_node)
                    self.kb.set_next_node(next_node)
                    self.kb.set_current_edge(current_edge)
                    self.kb.set_last_edge(last_edge)
                    self.kb.set_next_edge(next_edge)

                    self.fsm_state = 'traversing_edge'
                    self.reset_radio_data()
                    self.rf.control_radio_operation('continue')
                    continue

            else:
                print "controller.fsm() error"
                print "state == ", state
                break



            

    def shutdown(self):
        self.kb.save_kb()
        self.motion.join()
        self.rf.join()
        time.sleep(0.1)
        self.location.join()  # shut this down last



if __name__=='__main__':
    main = Controller()


    try:
        main.run()
        main.shutdown()
    except KeyboardInterrupt:
        main.shutdown()

