#!/usr/bin/env python


import sys
import os
import time
import threading
import signal

###############################################################################
#
# This class adapted from:
#   Python Cookbook, p. 362, 2d ed., Alex Martelli et al.
#   O'Reilly, 2005, 0-596-00797-3

class token(threading.Thread):

    def __init__(self):

        """
        Constructor. Sets envrionment variables.

        self.stopevent: stop flag
        self.reconfig_request:reconfig_request flag
        self._sleepperiod: not used at this time
        
        """

        self.stopevent = threading.Event()
        self.stopreceive = threading.Event()
        self.stoptransmit = threading.Event()
        self._sleepperiod = 1.0
        threading.Thread.__init__(self)

    def run(self):

        """ Executes main polling loop. """

        self.stopreceive.clear()
        self.stoptransmit.set()

        while not self.stopevent.isSet():
            
            # sleep while receiver is running
            time.sleep(2)

            # stop receiving, start transmitting
            self.stopreceive.set()
            self.stoptransmit.clear()

            # sleep while transmitter is running
            time.sleep(2)

            # start receiving, stop transmitting
            self.stopreceive.clear()
            self.stoptransmit.set()

        # end while



    def join(self, timeout=None):

        """ Stop thread and wait for return """

        self.stopevent.set()
        threading.Thread.join(self, timeout)


def main():


    

    flag = token()
    flag.start()

    print "wtf, eh?"

    n = 0
    m = 0


    # pre-emptive kill
#    os.sys('kill -9 `ps ax | grep python | grep benchmark | awk {\'print $1\'}`')
#    os.system('kill -9 `ps ax | grep xterm | awk {\'print $1\'}`')

    for m in range(0,200):
        print "flag.stopreceive.isSet?: ",flag.stopreceive.isSet()
        print "flag.stoptransmit.isSet?: ",flag.stoptransmit.isSet()
        if not flag.stopreceive.isSet():
            print "receiving..."
            
#             print "status = ps ax | grep benchmark | grep rx | grep -v grep"
#             os.system('ps ax | grep benchmark | grep rx | grep -v grep')
#             status = os.system('ps ax | grep benchmark | grep rx | grep -v grep')
#             print status
#             if status:
#                 os.system('sudo ./receive.sh')
        # end if


        if not flag.stoptransmit.isSet():
            print "transmitting..."
#             for n in range(0,10):
#                 pass
# #            os.sys('kill -9 `ps ax | grep python | grep rx | awk {\'print $1\'}`')
#             os.system('kill -9 `ps ax | grep xterm | grep receive | awk {\'print $1\'}`')
#             print "transmitting..."
#             os.system('xterm -tn transmit -e ./transmit.sh')
#             time.sleep(0.5)
#             # end if
    # end while
    
            
    print "done"
    flag.join()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit(0)  




#            os.sys('kill -9 `ps ax | grep python | grep tx | awk {\'print $1\'}`')
 #           os.system('kill -9 `ps ax | grep xterm | grep transmit | awk {\'print $1\'}`')
#            os.system('ps ax | grep xterm | grep receive | grep -v grep')
