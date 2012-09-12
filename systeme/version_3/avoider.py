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
                                                                               

    def _listen(self):
        """
        Listen before talk.

        """
        status = self.radio.listen(rssi_threshold=150, timeout=1.0)
        # if status == 'clear':
        #     print "channel clear"
        return status


    def run(self):
        """
        Run the radio subsystem.

        """
        parser = argparse.ArgumentParser()
        parser.add_argument("-f", type=float, default=434e6, metavar='frequency', dest='frequency', 
                            help="Transmit frequency (default: %(default)s)")
        parser.add_argument("-m", type=str, default='gfsk', metavar='modulation', dest='modulation',
                            choices=['gfsk', 'fsk', 'ask', 'cw'],
                            help="Select modulation from [%(choices)s] (default: %(default)s)")
        parser.add_argument("-p", type=int, default=17, metavar='power', dest='power',
                            choices=[1, 2, 5, 8, 11, 14, 17, 20],
                            help="Select transmit power from [%(choices)s] (default: %(default)s)")
        parser.add_argument("-r", type=float, default=4.8e3, metavar='bitrate',
                            dest='bitrate', help="Set bitrate (default: %(default)s)")

        args = parser.parse_args()
        frequency = args.frequency
        modulation = args.modulation
        power = args.power
        data_rate = args.bitrate

        self.radio.startup()
        self.radio.configure_radio(power, frequency, data_rate, modulation)

        while True:
            status = self._listen()
            if status == 'clear':
                self._send_packet()
            else:
                frequency += 2e6
                print "changing to new center frequency: %f" %(frequency,)
                self.radio.configure_radio(power, frequency, data_rate, modulation)



    def shutdown(self):
        self.radio.shutdown()




if __name__=='__main__':

    main = Avoider()
    try:
        main.run()
    except KeyboardInterrupt:
        main.shutdown()




        


            # # self._listen()
            # self._send_packet()




#         packet_counter = 1
#         state = "listen"
#         # f = 434e6
#         f = [431e6, 432e6, 433e6, 434e6, 435e6, 436e6, 437e6, 438e6, 439e6]
#         g = 0


#         while True:
#             print "set frequency to %d" %(f[g],)
#             if packet_counter % 30 == 0:
#                 self.flag_node_a_freq_change_req = True
                
#             if state == "listen":
#                 self._listen(f[g])
#                 state = "transmit"

#             elif state == "transmit":
#                 self._transmit(f[g])
#                 packet_counter += 1
#                 state = "receive"

#             elif state == "receive":
#                 self._receive(f[g])
#                 state = "listen"

#             else:
#                 print "+++ Melon melon melon +++"
#                 state = "listen"

#             if ((self.flag_node_a_freq_change_req == True)  
#                 and (self.flag_node_a_freq_change_ack == True)):
                
#                 self.flag_node_a_freq_change_req = False
#                 self.flag_node_a_freq_change_ack = False
#                 g += 1
#                 if (g == 9):
#                     g = 0












