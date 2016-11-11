#!/usr/bin/env python

import time

from barcode_server import BarcodeServer
from flight_path import FlightPath
from knowledge_base import KnowledgeBase
from motion import Motion
from node_a_server import NodeAServer



class Controller(object):

    def __init__(self):
        self.kb = KnowledgeBase()



        self.location = BarcodeServer(self.location_callback)
        self.flight_path = FlightPath()
        self.motion = Motion(self.kb)

        self.node_a = NodeAServer()


    def _init_fp(self):
        self.flight_path.build_full_graph()



    def location_callback(self, position):
        """
        Location callback.

        This function is used by the threaded location module to
        update the current location for the controller.

        Parameters
        ----------
        position : str
            String representation of six digit number indicating current position.

        """
        self.kb.current_location = position
        # print "Position: ", self.kb.current_location
        
        

    def run(self):
        self.location.start()
        self.node_a.start()

        path = [100001, 100002, 100003, 100004, 100005, 100006, 100007]

        for p in path:
            self.motion.move_until_location(p)
            if p == 100001:
                tic = time.time()
            else:
                toc = time.time()
                self.kb.duration.append(toc-tic)
                tic = time.time()
        print "kb.duration: ", self.kb.duration



    def shutdown(self):
        self.motion.shutdown()
        self.node_a.join()







if __name__=='__main__':
    main = Controller()
    try:
        main.run()
        main.shutdown()
    except KeyboardInterrupt:
        main.shutdown()










