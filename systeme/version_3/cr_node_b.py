#!/usr/bin/env python


import argparse
import time

# from knowledge_base import KnowledgeBase
from radio.packet import Packet
from radio.radio_api import RadioAPI


class StandAloneRadioB(object):
    def __init__(self):
        # self.kb = KnowledgeBase()

        self.radio = RadioAPI()
        self.packet = Packet('B')

        self.data = []
        for i in range(50):
            self.data.append(0xff)
        self.tx_packet_number = 1
        self.rssi_level = 0

    def _configure_radio(self, power, frequency, data_rate, modulation):
        """
        Configure radio for operation.

        """
        self.radio.configure_radio(power, frequency, data_rate, modulation)
        

    def _send_packet(self):
        """
        Transmit packet.

        """
        self.packet.set_flags_node_b()
        # location = self.kb.get_state()['current_location']
        location = 1
        tx_packet = self.packet.make_packet(self.tx_packet_number, location, self.data)
        self.radio.transmit(tx_packet)
        self.tx_packet_number += 1


    def _receive_packet(self):
        """
        Receive packet.

        """
        (self.rssi_level, rx_packet) = self.radio.receive(rx_fifo_threshold=63, timeout=None)
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
        status = self.radio.listen(rssi_threshold=100, timeout=1.0)
        if status == 'clear':
            print "channel clear"


    def run(self):
        """
        Run the radio subsystem.

        """
        parser = argparse.ArgumentParser()
        # parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument("-f", type=float, default=434e6, metavar='frequency', dest='frequency', 
                            nargs=1, help="Transmit frequency (default: %(default)s)")
        parser.add_argument("-m", type=str, default='gfsk', metavar='modulation', dest='modulation',
                            choices=['gfsk', 'fsk', 'ask'],
                            help="Select modulation from [%(choices)s] (default: %(default)s)")
        parser.add_argument("-p" "--power", type=int, default=17, metavar='power', dest='power',
                            choices=[8, 11, 14, 17],
                            help="Select transmit power from [%(choices)s] (default: %(default)s)")
        parser.add_argument("-r" "--bitrate", type=float, default=4.8e3, metavar='bitrate',
                            dest='bitrate', help="Set bitrate (default: %(default)s)")
        args = parser.parse_args()

        frequency = args.frequency
        modulation = args.modulation
        power = args.power
        data_rate = args.bitrate


        self.radio.startup()

        self._configure_radio(power, frequency, data_rate, modulation)




        time.sleep(1)

        # self.i = 0
        
        self.rssi_list = []

        # for i in range(100):
        #     rssi_list.append(self.radio.get_rssi_dBm())



        for i in range(100):
        # while True:
            # self.rssi_list.append(self.radio.get_rssi_dBm())
            self._receive_packet()
            self.rssi_list.append(self.rssi_level)
            print "received packet"
            # self.i += 1
            # print "RSSI (raw) : %f  RSSI (dBm) : %f" %(rssi, RSSI)

            

        print self.rssi_list



    def shutdown(self):


        # print "\n\n\n"
        # print "%d packets received." %(self.i,)
        # print "\n\n\n"
        self.radio.shutdown()




if __name__=='__main__':

    node_a = StandAloneRadioB()
    try:
        node_a.run()
    except KeyboardInterrupt:
        node_a.shutdown()

        



