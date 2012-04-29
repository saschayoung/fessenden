#!/usr/bin/env python


from knowledge_base import KnowledgeBase
from radio.data import NodeAData
from radio.packet import Packet
from radio.radio_api import RadioAPI


class StandAloneRadioA(object):
    def __init__(self):
        self.kb = KnowledgeBase()

        self.data = NodeAData()
        self.packet = Packet('A')
        self.radio = RadioAPI()

        # self.data = []
        # for i in range(50):
        #     self.data.append(0xff)
        

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
        location = self.kb.get_state()['current_location']
        data = self.data.pack_data()
        tx_packet = self.packet.make_packet(location, data)
        self.radio.transmit(tx_packet)


    def _receive_packet(self):
        """
        Receive packet.

        """
        rx_packet = self.radio.receive(rx_fifo_threshold=64, timeout=1.0)
        if rx_packet == []: # this occurs when timeout has been exceeded
            return
        else:
            packet_number, time_stamp, location, flags, data = self.packet.parse_packet(rx_packet)
            # print "packet_number=%d  time_stamp=%f  location=%d  flags=0x%x" %(packet_number, time_stamp,
            #                                                                    location, flags)
            # print "goodput for acknowledged packet #%d = %f bits/second" %(ack_packet_number, goodput)


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
        self.radio.startup()
        default_radio_profile = location = self.kb.get_state()['default_radio_profile']
        power = default_radio_profile['power']
        frequency = default_radio_profile['frequency']
        data_rate = default_radio_profile['data_rate']
        modulation = default_radio_profile['modulation']
        self._configure_radio(power, frequency, data_rate, modulation)

        state = "listen"


        while True:
            if state == "listen":
                self._listen()
                state = "send"

            elif state == "send":
                self._send_packet()
                state = "receive"

            elif state == "receive":
                self._receive_packet()
                state = "listen"

            else:
                print "+++ Melon melon melon +++"
                state = "listen"



    def shutdown(self):
        self.radio.shutdown()


if __name__=='__main__':
    node_a = StandAloneRadioA()
    try:
        node_a.run()
    except KeyboardInterrupt:
        node_a.shutdown()
