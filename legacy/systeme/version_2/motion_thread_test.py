#!/usr/bin/env python

import pprint
import time
import threading

import numpy as np

from knowledge_base import KnowledgeBase
# from knowledge_base.route import Route
from location.barcode import Location
from motion.motion_subsystem import MotionSubsystem
# from radio.radio_subsystem import RadioSubsystem

DEBUG = True


class Controller(object):
    def __init__(self):
        self.kb = KnowledgeBase()

        self.lock = threading.Lock()

        self.location = Location(self.kb, self.lock)
        self.motion = MotionSubsystem(self.kb, self.lock)


    def run(self):
        """
        Start the controller.

        """
        self.kb.build_route()
        self.motion.start()
        self.location.start()
        
        

        while True:
            print "time: ", time.time()
            time.sleep(1)
            

    def shutdown(self):
        # self.kb.save_kb()
        
        # pprint.pprint(self.kb.get_state())
        # print "\n\n\n\n\n"
        # self.kb.route_debug()
        # print "\n\n\n\n\n"
        self.motion.join()
        # self.motion.shutdown()
        # self.rf.join()
        time.sleep(0.1)
        self.location.join()  # shut this down last
        



if __name__=='__main__':
    main = Controller()

    try:
        main.run()
        main.shutdown()
    except KeyboardInterrupt:
        main.shutdown()
    
