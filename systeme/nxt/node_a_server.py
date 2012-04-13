#!/usr/bin/env python

"""
Module: barcode_server

A threaded barcode scanning `server`.
"""

import threading

from node_a import NodeA

class NodeAServer(threading.Thread):
    """
    Threaded RF node A.

    """

    def __init__(self):
        """
        Extend thread class.

        """
        self.rf = NodeA()
        self.stop_event = threading.Event()
        threading.Thread.__init__(self)


    def run(self):
        """
        Run node A thread.

        This function waits for the hardware scanner to read a
        barcode. The barcode something something something.
        """
        # while not self.stop_event.isSet():
        self.rf.fsm()



    def join(self, timeout=None):
        """
        Stop thread and wait for return.
        """
        self.stop_event.set()
        self.rf.shutdown()

        threading.Thread.join(self, timeout)





if __name__=='__main__':
    main = NodeAServer()
    try:
        main.start()
    except KeyboardInterrupt:
        main.join()
