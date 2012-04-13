#!/usr/bin/env python

import struct

from mid_level import MidLevel

from new_packet_utils import UAVPacket

class NodeA(object):
    def __init__(self):
        self.radio = MidLevel()

        self.packet = UAVPacket()
        self.loc = 0

    def startup(self):
        self.radio.startup()

    def shutdown(self):
        self.radio.shutdown()


    def _listen(self, freq):
        status = self.radio.listen(freq, rssi_threshold=100, timeout=1.0)
        if status == 'clear':
            print "channel clear"
    


    def _receive(self, freq):
        rx_packet = self.radio.receive(freq, rx_fifo_threshold=17, timeout=2.0)
        (rx_packet_num, rx_flags, rx_data) = self.packet.parse_packet(rx_packet)

        # this chunk of code should probably be moved into
        # packet_utils: UAVPacket.unpack_data()
        s = ''
        for i in range(8):
            s = s + chr(rx_data[i])

        (goodput,) = struct.unpack('!d', s)

        a4, a3, a2, a1 = rx_data[8:12]
        ack_number = (a4 << 24) + (a3 << 16) + (a2 << 8) + a1
        print "Calculated goodput for packet %d = %f" %(ack_number, goodput)






    def _transmit(self, freq):
        data = []
        for i in range(50):
            data.append(0xff)
        flags = 0x00
        tx_packet = self.packet.make_packet(self.loc, flags, data)
        self.radio.transmit(tx_packet, freq)
        self.loc += 1


    def fsm(self):
        """
        Primary control loop.

        This function is the finite state machine that controls the
        operation of the system.
        """

        self.startup()

        state = "listen"
        f = 434e6

        while True:
            if state == "listen":
                self._listen(f)
                state = "transmit"

            elif state == "transmit":
                self._transmit(f)
                state = "receive"

            elif state == "receive":
                self._receive(f)
                state = "listen"

            else:
                print "+++ Melon melon melon +++"
                state = "listen"


if __name__=='__main__':

    try:
        main = NodeA()
        main.fsm()
        main.shutdown()
    except KeyboardInterrupt:
        main.shutdown()



