#!/usr/bin/env python

import numpy as np
import time, random
import sys, os
import struct


class beacon:

    def __init__(self):
        self.packet_size = 1500   # in bytes
        self.beacon_id = 42
        self.packet_number = 0

    def make_packet(self):
        __data = (self.packet_size - 4) * chr(self.packet_number & 0xff)
        __payload1 = struct.pack('!H', self.packet_number & 0xffff)
        __payload2 = struct.pack('!H', self.beacon_id & 0xffff)

        self.packet = __payload1 + __payload2 + __data
        self.packet_number += 1

    def tx_packet(self):
        rand_delay = random.randint(0,5)
        print 'random backoff %d seconds' % rand_delay
        time.sleep(rand_delay/10)
        return self.packet
    
    def run(self):
        pass


if __name__=='__main__':
    main = beacon()
    main.make_packet()
    payload = main.tx_packet()
    (pktno,) = struct.unpack('!H', payload[0:2])
    (beacon_ID,) = struct.unpack('!H', payload[2:4])
    print "pktno: ", pktno
    print "beacon_ID: ", beacon_ID



        #this is not used currently
#         #time magic
#         t = "%.15f" % time.time()
#         t = t.split('.')
#         t_mant = t[0]
#         t_frac = t[1]
        
#         payload3 = struct.pack('!H', int(t_mant[0:4]) & 0xffff)
#         payload4 = struct.pack('!H', int(t_mant[4:8]) & 0xffff)
#         payload5 = struct.pack('!H', int(t_mant[8:len(t_mant)]) & 0xffff)

#         payload6 = struct.pack('!H', int(t_frac[0:4]) & 0xffff)
#         payload7 = struct.pack('!H', int(t_frac[4:8]) & 0xffff)
#         payload8 = struct.pack('!H', int(t_frac[8:12]) & 0xffff)
#         payload9 = struct.pack('!H', int(t_frac[12:len(t_frac)]) & 0xffff)
