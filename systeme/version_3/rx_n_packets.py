#!/usr/bin/env python

import argparse
import struct
import time

from radio.data import NodeBData
from radio.packet import Packet
from radio.radio_api import RadioAPI


class RxNPackets(object):
    """
    Receiver.

    """

    def __init__(self):
        self.data = NodeBData()
        self.packet = Packet('B')
        self.radio = RadioAPI()

        self.tx_packet_number = 1
        self.rx_packet_list = []
        self.rssi_level = 0


    def _configure_radio(self, power, frequency, data_rate, modulation):
        """
        Configure radio for operation.

        """
        self.radio.configure_radio(power, frequency, data_rate, modulation)



    def _receive_packet(self):
        """
        Receive packet.

        This function blocks until it receives a packet.

        """
        (self.rssi_level, rx_packet) = self.radio.receive(rx_fifo_threshold=64, timeout=None)
        pkt_num, t, loc, flags, data = self.packet.parse_packet(rx_packet)
        return pkt_num, loc, flags, data



    def _send_packet(self, mode, received_packets = None):
        """
        Transmit data.

        Parameters
        ----------
        mode : str
            Mode of operation, used to create appropriate packet header.
            One of {`ack_command` | `send_data`}.
        received_packets : int, opt
            Number of packets received.

        """
        location = 44

        if mode == 'ack_command':
            self.packet.set_flags_node_b(ack_command = True)
            payload = self.data.pack_data(mode)

        elif mode == 'send_data':
            if received_packets == None:
                print "mode is `send_data`, but `received_packets` is `None`"
                raise ValueError
            self.packet.set_flags_node_b(send_data = True)
            payload = self.data.pack_data(mode, received_packets)

        else:
            print 'error in _send_packet, no mode specified'
            raise ValueError
        
        tx_packet = self.packet.make_packet(self.tx_packet_number, location, payload)
        self.tx_packet_number += 1
        self.radio.transmit(tx_packet)
        


    def run(self):
        """
        Run receiver.

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

        self.frequency = args.frequency
        modulation = args.modulation
        power = args.power
        data_rate = args.bitrate

        self.radio.startup()
        self.radio.configure_radio(power, self.frequency, data_rate, modulation)

        self.pkts_received = 0
        while True:
            pkt_num, loc, flags, data = self._receive_packet()
            self.rx_packet_list.append(pkt_num)
            self.pkts_received += 1

        # print "packet number %d received" %(pkt_num)



    def shutdown(self):
        print "\n\n\n\n"
        print "% d packets received" %(self.pkts_received,)
        print self.rx_packet_list
        print "\n\n\n\n"
        time.sleep(1)
        self.radio.shutdown()


if __name__=='__main__':
    rx = RxNPackets()
    try:
        rx.run()
    except KeyboardInterrupt:
        rx.shutdown()








    # def fsm(self):
    #     """
    #     Node B finite state machine.

    #     """
    #     while True:
    #         pkt_num, loc, flags, data = self._receive_packet()
        
    #         if (flags & 0x80) == 0x80:  # receive stream of packets
    #             print "receiving stream of packets, pkt_num = ", pkt_num
    #             self.rx_packet_list.append(pkt_num)
    #             # print "received data stream packet"
    #             continue

    #         elif (flags & 0x40) == 0x40: # receive data update request
    #             print "received request for data update"
    #             received_packets = len(self.rx_packet_list)
    #             time.sleep(0.5)
    #             self._send_packet('send_data', received_packets)
    #             self.rx_packet_list = []
    #             continue

    #         elif (flags & 0x20) == 0x20: # receive reconfiguration request
    #             print "received request for reconfiguration"
    #             # self.rx_packet_list = []
    #             mod, eirp, bitrate = self.data.unpack_data('reconfig', data)
    #             print mod, eirp, bitrate
    #             time.sleep(1.0)
    #             self._send_packet('ack_command')
    #             self.radio.configure_radio(eirp, self.frequency, bitrate, mod)
    #             print "reconfigured radio with new waveform, waiting for more packets..."
    #             continue

    #         else:
    #             print bin(flags)
    #             print "error in Node B FSM, will reset and continue"
    #             continue
