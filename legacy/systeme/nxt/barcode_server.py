#!/usr/bin/env python

"""
Module: barcode_server

A threaded barcode scanning `server`.
"""

import threading

import barcode

class BarcodeServer(threading.Thread):
    """
    Threaded barcode scanner server.

    """

    def __init__(self, callback):
        """
        Extend thread class for barcode scanner.

        Parameters
        ----------
        callback : method
            Callback to instantiating (parent) class to return scanned
            barcode.
        """
        self.stop_event = threading.Event()
        threading.Thread.__init__(self)
        self.callback = callback


    def run(self):
        """
        Get barcode data.

        This function waits for the hardware scanner to read a
        barcode. The barcode something something something.
        """
        while not self.stop_event.isSet():
            barcode_data = barcode.get_barcode()
            self.callback(barcode_data)



    def join(self, timeout=None):
        """
        Stop thread and wait for return.
        """
        self.stop_event.set()
        threading.Thread.join(self, timeout)





