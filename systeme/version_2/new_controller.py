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
        self.color_values = np.array([])

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
                before_start = 0
                start_node = self.kb.get_start_node()
                self.motion.set_source_destination(before_start, start_node)
                self.motion.set_speed(25)
                self.motion.control_motion_operation('go')


                while not self.arrived:
                    time.sleep(0.1)

                next_node = self.kb.get_next_node(start_node)
                self.kb.set_current_node(start_node)
                self.kb.set_next_node(next_node)
                self.kb.set_next_edge((start_node, next_node))

                self.fsm_state = 'traversing_edge'
                continue


            elif self.fsm_state == 'traversing_edge':
                if DEBUG:
                    print "traversing_edge"

                kb_state = self.kb.get_state()
                print kb_state
                current_edge = kb_state['next_edge']


                next_edge = None
                last_node = kb_state['current_node']
                current_node = None
                next_node = kb_state['next_node']

                self.kb.set_current_edge(current_edge)
                self.kb.set_next_edge(next_edge)
                self.kb.set_last_node(last_node)
                self.kb.set_current_node(current_node)
                

                self.arrived = False
                self.motion.set_source_destination(current_edge[0], current_edge[1])
                self.motion.set_speed(45)
                tic = time.time()

                self.motion.control_motion_operation('go')

                while not self.arrived:
                    self.color_values = np.append(self.color_values, self.motion.color_reading())
                    time.sleep(0.1)

                toc = time.time() - tic
                weight = toc * np.average(self.goodput)
                targets = self.count_targets(self.color_values)
                if DEBUG:
                    print "values for edge %s: weight = %0.2f, targets = %d" %(str(current_edge),
                                                                               weight,
                                                                               targets)
                self.kb.set_edge_values(current_edge, weight, targets)

                self.fsm_state = 'at_a_node'
                continue


            elif self.fsm_state == 'at_a_node':
                self.rf.control_radio_operation('pause')
                kb_state = self.kb.get_state()
                current_node = kb_state['next_node']
                next_node = self.kb.get_next_node(current_node)

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
                self.color_values = np.array([])
                self.rf.control_radio_operation('continue')
                continue

            else:
                print "controller.fsm() error"
                print "state == ", state
                break




    def count_targets(self, a):
        a[a!=5] = 0
        j = 0
        for i in range(len(a)-1):
            if a[i] == 0 and a[i+1] == 5:
                j += 1
        return j
        

            

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

