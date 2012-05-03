#!/usr/bin/env python

import pprint
import time
import threading

import numpy as np

from knowledge_base import KnowledgeBase
# from knowledge_base.route import Route
from location.barcode import Location
from motion.simple_motion import SimpleMotion
from radio.radio_subsystem import RadioSubsystem

DEBUG = True


class Controller(object):
    def __init__(self):
        self.kb = KnowledgeBase()

        self.lock = threading.Lock()

        self.location = Location(self.kb, self.lock)
        self.motion = SimpleMotion(self.kb, self.lock)
        self.rf = RadioSubsystem(self.kb, self.lock, self.radio_data_callback)

        self.fsm_state = 'at_beginning'

        self.sent_packet = np.array([])
        self.ack_packet = np.array([])
        self.goodput = np.array([])


    def run(self):
        """
        Start the controller.

        """
        self.kb.build_route()
        self.location.start()
        self.rf.start()
        
        while True:
            self.fsm()



    def radio_data_callback(self, sent_packet, ack_packet, goodput):
        self.sent_packet = np.append(self.sent_packet, sent_packet)
        self.ack_packet = np.append(self.ack_packet, ack_packet)
        self.goodput = np.append(self.goodput, goodput)

    def reset_radio_data(self):
        self.sent_packet = np.array([])
        self.ack_packet = np.array([])
        self.goodput = np.array([])


    def fsm(self):
        if self.fsm_state == 'at_beginning':
            start_node = self.kb.get_start_node()
            self.motion.move_until_location(start_node, speed = 25)
            while not self.kb.get_state()['current_location'] == start_node:
                time.sleep(0.2)
            next_node = self.kb.get_next_node(start_node)

            # self.lock.acquire()
            self.kb.set_current_node(start_node)
            self.kb.set_next_node(next_node)
            self.kb.set_next_edge((start_node, next_node))
            # self.lock.release()

            self.fsm_state = 'traversing_edge'

            return
            

        elif self.fsm_state == 'traversing_edge':
            kb_state = self.kb.get_state()
            current_edge = kb_state['next_edge']
            next_edge = None
            last_node = kb_state['current_node']
            current_node = None
            next_node = kb_state['next_node']

            # self.lock.acquire()
            self.kb.set_current_edge(current_edge)
            self.kb.set_next_edge(next_edge)
            self.kb.set_last_node(last_node)
            self.kb.set_current_node(current_node)
            # self.lock.release()

            tic = time.time()
            self.motion.move_from_here_to_there(last_node, next_node, speed = 45)
            while not self.kb.get_state()['current_location'] == next_node:
                color = motion.get_color_reading()
                print "\n\n\n\n"
                print "Detected color: ", color
                print "\n\n\n\n"
                time.sleep(0.01)
            
            toc = time.time() - tic
            weight = toc * np.average(self.goodput)
            print "weight value for edge %s = %0.2f" %(str(current_edge), weight)
            self.kb.set_edge_weight(current_edge, weight)
            # print self.goodput
            # print "average goodput for edge %s = %0.2f" %(str(current_edge), np.average(self.goodput))
            self.fsm_state = 'at_a_node'

            return


        elif self.fsm_state == 'at_a_node':
            self.rf.control_radio_operation('pause')
            kb_state = self.kb.get_state()

            current_node = kb_state['next_node']
            next_node = self.kb.get_next_node(current_node)

            current_edge = None
            last_edge = kb_state['current_edge']
            next_edge = (current_node, next_node)

            # self.lock.acquire()
            self.kb.set_current_node(current_node)
            self.kb.set_next_node(next_node)
            self.kb.set_current_edge(current_edge)
            self.kb.set_last_edge(last_edge)
            self.kb.set_next_edge(next_edge)
            # self.lock.release()

            self.fsm_state = 'traversing_edge'
            self.rf.control_radio_operation('continue')
            self.reset_radio_data()
            return

        else:
            if DEBUG:
                print "controller.fsm() error"
                print "state == ", state
            else:
                pass
        
            


    


    def shutdown(self):
        self.kb.save_kb()
        
        # pprint.pprint(self.kb.get_state())
        # print "\n\n\n\n\n"
        # self.kb.route_debug()
        # print "\n\n\n\n\n"
        self.motion.shutdown()
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





        # self.fsm() # at_beginning
        # time.sleep(0.1)
        # self.fsm() # traversing_edge

        # path = self.route.get_path()

        # # path = [001, 002, 003, 004, 005, 006, 007]

        # for p in path:
        #     self.motion.move_until_location(p)

            # this should be attached to the route graph
            # ==========================================
            # if p == 1:
            #     tic = time.time()
            # else:
            #     toc = time.time()
            #     self.kb.duration.append(toc-tic)
            #     tic = time.time()

