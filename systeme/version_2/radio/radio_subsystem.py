#!/usr/bin/env python

"""
Module: radio_uav

Threaded UAV radio subsystem.
"""

import threading

from data import NodeAData
from packet import Packet
from radio_api import RadioAPI


DEBUG = True

class RadioSubsystem(threading.Thread):
    """
    Threaded UAV radio subsystem.

    Enables threaded operation of radio.

    """

    def __init__(self, knowledge_base, lock):
        """
        Extend threading class.

        Parameters
        ----------
        knowledge_base : object
            Handle to shared knoweldge base.
        lock : object
            File lock for concurrent access to knowledge base.
        initial_config : dict
            Initial radio configuration

        """
        threading.Thread.__init__(self)

        self.kb = knowledge_base
        self.lock = lock

        self._flag = False

        self.stop_event = threading.Event()

        self.data = NodeAData()
        self.packet = Packet('A')
        self.radio = RadioAPI()

        self._fsm_state = 'listen'


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
        rx_packet = self.radio.receive(rx_fifo_threshold=64, timeout=2.0)
        if rx_packet == []: # this occurs when timeout has been exceeded
            print "time_out_exceeded"
            return
        else:
            packet_number, time_stamp, location, flags, data = self.packet.parse_packet(rx_packet)
            ack_packet_number, goodput = self.data.unpack_data(data)
            if DEBUG:
                print "packet_number=%d  time_stamp=%f  location=%d  flags=0x%x" %(packet_number, time_stamp,
                                                                                   location, flags)
                print "goodput for acknowledged packet #%d = %f bits/second" %(ack_packet_number, goodput)
            

    def _listen(self):
        """
        Listen before talk.

        """
        status = self.radio.listen(rssi_threshold=100, timeout=1.0)
        if status == 'clear':
            if DEBUG:
                print "channel clear"
            else:
                pass


    def run(self):
        """
        Run the radio subsystem.

        """
        print "Starting radio subsystem"

        self.radio.startup()
        default_radio_profile = self.kb.get_state()['default_radio_profile']
        power = default_radio_profile['power']
        frequency = default_radio_profile['frequency']
        data_rate = default_radio_profile['data_rate']
        modulation = default_radio_profile['modulation']
        self._configure_radio(power, frequency, data_rate, modulation)

        # state = "listen"


        while not self.stop_event.isSet():
            self._fsm_state()

            # if state == "listen":
            #     self._listen()
            #     state = "send"

            # elif state == "send":
            #     self._send_packet()
            #     state = "receive"

            # elif state == "receive":
            #     self._receive_packet()
            #     state = "listen"

            # else:
            #     print "radio subsystem fsm error"
            #     state = "listen"



    def _fsm(self):
        

            if self._fsm_state == "listen":
                self._listen()
                self._fsm_state = "send"
                return

            elif self._fsm_state == "send":
                self._send_packet()
                self._fsm_state = "receive"
                return

            elif self._fsm_state == "receive":
                self._receive_packet()
                self._fsm_state = "listen"
                return
            
            else:
                print "radio subsystem fsm error"
                self._fsm_state = "listen"
                return






    def join(self, timeout=None):
        self.stop_event.set()
        self.radio.shutdown()
        threading.Thread.join(self, timeout)










    # def set_interrupt_flag(self):
    #     """
    #     Interrupt radio operation.

    #     This function sets the flag `True`. This is used to interrupt
    #     the standard operational flow of the radio.

    #     """
    #     self.flag = True


    # def set_command(self, command):
    #     """
    #     Pass command to radio subsystem.

    #     This function is used to send a command to the radio control
    #     subsystem. 

    #     Parameters
    #     ----------
    #     command : str
    #         One of {`configure` | `scan` | `continue`}

    #     """
    #     self.command = command






