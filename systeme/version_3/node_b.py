#!/usr/bin/env python

import argparse
import time

from radio.packet import Packet
from radio.radio_api import RadioAPI


class NodeB(object):
    """
    Node B radio.

    Node B is the base station or `headquarters` node with which the
    AV communicates.

    """

    def __init__(self):
        self.radio = RadioAPI
        self.packet = Packet('B')

        self.tx_packet_number = 1
        self.rx_packet_list = []



    def run(self):
        """
        Run Node B.

        This function starts the operation of the Node B radio,
        excecuting all the one-time start-up funcitons, before handing
        off to the finite state machine.

        """
        parser = argparse.ArgumentParser()
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
        self.radio.configure_radio(power, frequency, data_rate, modulation)

        




    def _receive_packet(self):
        """
        Receive packet.

        This function blocks until it receives a packet.

        """
        rx_packet = self.radio.receive(rx_fifo_threshold=64, timeout=None)
        pkt_num, t, loc, flags, data = self.packet.parse_packet(rx_packet)
        



    def fsm(self):
        """
        Node B finite state machine.

        """

        
        
