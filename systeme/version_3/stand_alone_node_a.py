#!/usr/bin/env python

import argparse
import time
import sys

from radio.packet import Packet
from radio.radio_api import RadioAPI


class StandAloneRadioA(object):
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

        
        self.radio.startup()

        # default_radio_profile = {'power': 14,
        #                          'frequency' : 434e6,
        #                          'data_rate' : 4.8e3,
        #                          'modulation' : "gfsk"}

        # frequency = default_radio_profile['frequency']
        # modulation = default_radio_profile['modulation']
        # power = default_radio_profile['power']
        # data_rate = default_radio_profile['data_rate']

        frequency = args.frequency
        modulation = args.modulation
        power = args.power
        data_rate = args.bitrate


        print "frequency: ", frequency
        print "modulation: ", modulation
        print "power: ", power
        print "data_rate: ", data_rate


        self.shutdown()

        self._configure_radio(power, frequency, data_rate, modulation)

        state = "listen"


        while True:
            self._send_packet()

        # while True:
        #     if state == "listen":
        #         self._listen()
        #         state = "send"
        #         time.sleep(0.1)

        #     elif state == "send":
        #         self._send_packet()
        #         state = "receive"
        #         # state = "receive"
        #         time.sleep(0.1)

        #     elif state == "receive":
        #         self._receive_packet()
        #         state = "listen"
        #         time.sleep(0.1)

        #     else:
        #         print "+++ Melon melon melon +++"
        #         state = "listen"



    def shutdown(self):
        self.radio.shutdown()


if __name__=='__main__':

    node_a = StandAloneRadioA()
    try:
        node_a.run()
    except KeyboardInterrupt:
        node_a.shutdown()
