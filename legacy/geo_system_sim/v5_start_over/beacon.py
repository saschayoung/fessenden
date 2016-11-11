#!/usr/bin/env python

import numpy as np
import time, random
import sys, os
import struct


class beacon:

    def __init__(self,delay):
        self.delay = delay
        self.packet_size = 1500   # in bytes
        self.beacon_id = 42
        self.packet_number = 0
        self.max_delay = 5

    def make_packet(self):
        __data = (self.packet_size - 4) * chr(self.packet_number & 0xff)
        __payload1 = struct.pack('!H', self.packet_number & 0xffff)
        __payload2 = struct.pack('!H', self.beacon_id & 0xffff)

        self.packet = __payload1 + __payload2 + __data
        self.packet_number += 1

    def tx_packet(self):
        if self.delay:
            rand_delay = random.randint(0,self.max_delay)
            print 'random backoff %d seconds' % rand_delay
            time.sleep(rand_delay)
        return self.packet
    
    def run(self):
        pass


if __name__=='__main__':
    main = beacon()
    for i in range(7):
        main.make_packet()

    print main.packet_number
    # payload = main.tx_packet()
    # (pktno,) = struct.unpack('!H', payload[0:2])
    # (beacon_ID,) = struct.unpack('!H', payload[2:4])
    # print "pktno: ", pktno
    # print "beacon_ID: ", beacon_ID


