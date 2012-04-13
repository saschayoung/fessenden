#!/usr/bin/env python

"""
Module: barcode_server

A threaded barcode scanning `server`.
"""

import time
import threading

# from node_a import NodeA



class Sample(object):
    def __init__(self):
        self.thread = NodeAServer()


    def run(self):
        self.thread.start()
        while True:
            print "main time: ", time.time()
            time.sleep(0.6)
        


    def shutdown(self):
        self.thread.join()
    

class NodeAServer(threading.Thread):
    """
    Threaded RF node A.

    """

    def __init__(self):
        """
        Extend thread class.

        """
        # self.rf = NodeA()
        self.stop_event = threading.Event()
        threading.Thread.__init__(self)


    def run(self):
        """
        Run node A thread.

        This function waits for the hardware scanner to read a
        barcode. The barcode something something something.
        """
        # while True:
        while not self.stop_event.isSet():
            print "threaded time: ", time.time()
            time.sleep(0.5)
            # self.rf.fsm()



    def join(self, timeout=None):
        """
        Stop thread and wait for return.
        """
        self.stop_event.set()
        # self.rf.shutdown()

        threading.Thread.join(self, timeout)





if __name__=='__main__':
    main = Sample()
    try:
        main.run()
    except KeyboardInterrupt:
        main.shutdown()
