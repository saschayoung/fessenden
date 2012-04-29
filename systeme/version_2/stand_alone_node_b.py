#!/usr/bin/env python


from knowledge_base import KnowledgeBase
from radio.packet import Packet
from radio.radio_api import RadioAPI


class StandAloneRadioB(object):
    def __init__(self):
        self.kb = KnowledgeBase()

        self.radio = RadioAPI()
        self.packet = Packet('B')

        self.data = []
        for i in range(50):
            self.data.append(0xff)
        

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
        location = self.kb.get_state()['current_location']
        tx_packet = self.packet.make_packet(location, self.data)
        self.radio.transmit(tx_packet)


    def _receive_packet(self):
        """
        Receive packet.

        """
        rx_packet = self.radio.receive(rx_fifo_threshold=63, timeout=None)
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
                state = "receive"

            elif state == "receive":
                self._receive_packet()
                state = "send"

            elif state == "send":
                self._send_packet()
                state = "listen"

            else:
                print "+++ Melon melon melon +++"
                state = "listen"


    def shutdown(self):
        self.radio.shutdown()


if __name__=='__main__':
    node_b = StandAloneRadioB()
    try:
        node_b.run()
    except KeyboardInterrupt:
        node_b.shutdown()
