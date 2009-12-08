#!/usr/bin/env python


import sys,os, time, wx
from random_move import random_move
from repeater_gui import repeater_gui
#import threading 

#class fifo_stack:
#    def __init__(self):
#        self.nextin = 0
#        self.nextout = 0
#        self.data = {}

#    def push(self, value):
#        self.data[self.nextin] = value
#        self.nextin += 1

#    def pop(self):
#        value = self.data[self.nextout]
#        del self.data[self.nextout]
#        self.nextout += 1
#        return value

#    def length(self):
#        return len(self.data)

#    def debug(self):
#        print ""
#        print "debug info follows..."
#        print ""
#        print "nextin:           ", self.nextin
#        print "nextout:          ", self.nextout
#        print "self.data length: ", self.length()
#        print "self.data:        ", self.data
#        print ""

#class gui_thread(threading.Thread):
#    def __init__(self):
#        self.stopevent = threading.Event()
#        threading.Thread.__init__(self)

#     def run(self):
#         while not(self.stopevent.isSet()):
#             app = wx.App()
#             gui = repeater_gui(shm)
#             app.MainLoop()

#     def join(self, timeout = None):
#         self.stopevent.set()
#         threading.Thread.join(self, timeout)

def main():
#     global shm
    
#     shm = fifo_stack()

#     thread = gui_thread()
#     thread.run()



    n = 0
    m = 0


#receiver start for Geoloaction data collection
    print ""
    print "starting reciever"
    os.system('sudo ./receive.sh') 

    for n in range(0,1000):

        # rx side
        #############################################
#only start reciever once for Geoloaction data collection
#         print ""
#         print "receiving..."
#         # start receiver

#         os.system('sudo ./receive.sh') 

#        if os.path.exists('gui_beacon_data'):
#             f = open('gui_becon_data')
#             beacon_pktno = f.readlines()
#             beacon_pktno = beacon_pktno[0]
#             shm.push('B' + beacon_pktno)
        time.sleep(5)
   
#RX shutdown commented out for Geoloaction data collection
'''
        print "shutting down receiver..."
        # stop receiver
        status = os.system('sudo kill -9 `ps ax | grep benchmark | grep rx | grep -v grep | awk {\'print $1\'}`')
        if status:   #status==256 -> proc not killed
            print "failed to shutdown receiver"
        #############################################
'''

#        time.sleep(1)



#TX side commented out for Geolocation data collection
'''

        # tx side
        #############################################
        print ""
        print "transmitting..."
        # start transmitter
        if os.path.exists('last_location'):
            f = open('last_location','r')
            location = f.readlines()
            location = location[0]
        else:
            location = None
#        shm.push('L' + location)
        location = random_move(location)
        os.system('sudo ./transmit.sh ' + location)
        time.sleep(2)
        print "\nshutting down transmitter..."
        # stop transmitter


        # these two lines are needed on fessenden, but not on gretsky
        # fessenden is faster, and so the following check is used
#         not_running = os.system('ps ax | grep benchmark | grep tx | grep -v grep | awk {\'print $1\'} 1> /dev/null 2> /dev/null')
#         if not_running:
 
        # if the two lines above are used (uncommented)
        # indent the following two line appropriately
        status = os.system('sudo kill -9 `ps ax | grep benchmark | grep tx | grep -v grep | awk {\'print $1\'}`')
        if status:   #status==256 -> proc not killed
            print "failed to shutdown transmitter"
        #############################################

'''
    #endfor

#stop receiver at end of for loop for Geolocation data collection
        print "shutting down receiver..."
        # stop receiver
        status = os.system('sudo kill -9 `ps ax | grep benchmark | grep rx | grep -v grep | awk {\'print $1\'}`')
        if status:   #status==256 -> proc not killed
            print "failed to shutdown receiver"
    
#    thread.join()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass




