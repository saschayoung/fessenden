#!/usr/bin/env python


import argparse
import time
import sys

from radio.packet import Packet
from radio.radio_api import RadioAPI


class Avoider(object):
    def __init__(self):

        self.radio = RadioAPI()
        self.packet = Packet('A')

        self.data = []
        for i in range(50):
            self.data.append(0xff)
        self.tx_packet_number = 1
        

    def _configure_radio(self, power, frequency, data_rate, modulation):
        """
        Configure radio for operation.

        """
        self.radio.configure_radio(power, frequency, data_rate, modulation)
        

    def _send_packet(self):
        """
        Transmit packet.

        """
        self.packet.set_flags_node_a()
        # location = self.kb.get_state()['current_location']
        location = 1
        tx_packet = self.packet.make_packet(self.tx_packet_number, location, self.data)
        self.radio.transmit(tx_packet)
        self.tx_packet_number += 1


    def _receive_packet(self):
        """
        Receive packet.

        """
        rx_packet = self.radio.receive(rx_fifo_threshold=63, timeout=1.0)
        if rx_packet == []: # this occurs when timeout has been exceeded
            return
        else:
            packet_number, time_stamp, location, flags, data = self.packet.parse_packet(rx_packet)
            print "packet_number=%d  time_stamp=%f  location=%d  flags=0x%x" %(packet_number, time_stamp,
                                                                               location, flags)
                                                                               

    def _listen(self, threshold):
        """
        Listen before talk.

        """
        status = self.radio.listen(threshold, timeout=1.0)
        # if status == 'clear':
        #     print "channel clear"
        return status


    def run(self):
        """
        Run the radio subsystem.

        """
        parser = argparse.ArgumentParser()
        parser.add_argument("-f", type=float, default=432e6, metavar='frequency', dest='frequency', 
                            help="Transmit frequency (default: %(default)s)")
        parser.add_argument("-m", type=str, default='gfsk', metavar='modulation', dest='modulation',
                            choices=['gfsk', 'fsk', 'ask', 'cw'],
                            help="Select modulation from [%(choices)s] (default: %(default)s)")
        parser.add_argument("-p", type=int, default=17, metavar='power', dest='power',
                            choices=[1, 2, 5, 8, 11, 14, 17, 20],
                            help="Select transmit power from [%(choices)s] (default: %(default)s)")
        parser.add_argument("-r", type=float, default=4.8e3, metavar='bitrate',
                            dest='bitrate', help="Set bitrate (default: %(default)s)")
        parser.add_argument("-t", type=int, default=150, metavar='threshold',
                            dest='threshold', help="Set rssi threshold (default: %(default)s)")
        parser.add_argument("-d", type=str, default="data_file.txt", metavar='data_file',
                            dest='data_file', help="Data file to store results (default: %(default)s)")

        args = parser.parse_args()
        frequency = args.frequency
        modulation = args.modulation
        power = args.power
        bitrate = args.bitrate
        threshold = args.threshold
        data_file = args.data_file

        print "data_file", data_file
        f = open(data_file, 'r+')
        
        
        
        if f.readlines() == []:
            self.first_time = True
        else:
            self.first_time = False
            l = f.readlines()
            jump_freq = float(l[0].strip('\n'))
            
        

        self.radio.startup()
        self.radio.configure_radio(power, frequency, bitrate, modulation)

        hop = False

        while True:
            status = self._listen(threshold)
            if first_time == True:

                if status == 'clear':
                    if hop == True:
                        self.toc = time.time()
                        print "arrived at final destination, time to find new channel: ", self.toc - self.tic
                        hop = False

                        s = str(frequency) + "\n"
                        f.write(s)
                        f.close()


                    self._send_packet()
                else:
                    if hop == False:
                        print "reconfiguring radio, starting timer"
                        hop = True
                        self.tic = time.time()
                    frequency += 2e6
                    print "changing to new center frequency: %f" %(frequency,)
                    self.radio.configure_radio(power, frequency, bitrate, modulation)

            else:
                if status == 'clear':
                    if hop == True:
                        self.toc = time.time()
                        print "arrived at final destination, time to find new channel: ", self.toc - self.tic
                        hop = False

                    self._send_packet()
                else:
                    if hop == False:
                        print "reconfiguring radio, starting timer"
                        hop = True
                        self.tic = time.time()
                    frequency = jump_freq
                    print "changing to new center frequency: %f" %(frequency,)
                    self.radio.configure_radio(power, frequency, bitrate, modulation)


    def shutdown(self):
            
        self.radio.shutdown()




if __name__=='__main__':

    main = Avoider()
    try:
        main.run()
    except KeyboardInterrupt:
        
        pass
    finally:
        main.shutdown()




        











