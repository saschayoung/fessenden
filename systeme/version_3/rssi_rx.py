#!/usr/bin/env python

import argparse
import time

# from knowledge_base import KnowledgeBase
from radio.packet import Packet
from radio.radio_api import RadioAPI


class RssiRx(object):
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
                            help="Transmit frequency (default: %(default)s)")
        parser.add_argument("-m", type=str, default='gfsk', metavar='modulation', dest='modulation',
                            choices=['gfsk', 'fsk', 'ask'],
                            help="Select modulation from [%(choices)s] (default: %(default)s)")
        parser.add_argument("-p", type=int, default=17, metavar='power', dest='power',
                            choices=[8, 11, 14, 17],
                            help="Select transmit power from [%(choices)s] (default: %(default)s)")
        parser.add_argument("-r", type=float, default=4.8e3, metavar='bitrate',
                            dest='bitrate', help="Set bitrate (default: %(default)s)")
        args = parser.parse_args()

        frequency = args.frequency
        modulation = args.modulation
        power = args.power
        data_rate = args.bitrate


        self.radio.startup()

        self._configure_radio(power, frequency, data_rate, modulation)

        state = "listen"


        self.rssi_list = []

        for i in range(100):
            rssi = self.radio.get_rssi_raw()
            self.rssi_list.append(rssi)

            # RSSI = ((rssi - 125.0)/2.0) - 60.0
            # print "RSSI (raw) : %f  RSSI (dBm) : %f" %(rssi, RSSI)



        print self.rssi_list


    def shutdown(self):
        self.radio.shutdown()


if __name__=='__main__':
    rx = RssiRx()
    try:
        rx.run()
    except KeyboardInterrupt:
        rx.shutdown()




        # while True:
        #     rssi = self.radio.get_rssi_raw()
        #     RSSI = ((rssi - 125.0)/2.0) - 60.0
        #     print "RSSI (raw) : %f  RSSI (dBm) : %f" %(rssi, RSSI)
        #     # time.sleep(0.1)
