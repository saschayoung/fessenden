#!/usr/bin/env python

"""
Module: radio_uav

Threaded UAV radio subsystem.
"""

import threading
import time

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

        self.stop_event = threading.Event()

        self.data = NodeAData()
        self.packet = Packet('A')
        self.radio = RadioAPI()

        self._fsm_state = 'listen'
        self.command = 'continue'
        self.tx_packet_number = 1

        self.ack_packet_number = 0
        self.goodput = 0


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
        tx_packet = self.packet.make_packet(self.tx_packet_number, location, data)

        self.radio.transmit(tx_packet)


    def _receive_packet(self):
        """
        Receive packet.

        """
        self.rx_packet = self.radio.receive(rx_fifo_threshold=64, timeout=1.0)
        if self.rx_packet == []: # this occurs when timeout has been exceeded
            print "time_out_exceeded"
            return
        else:
            rx_packet_number, time_stamp, location, flags, data = self.packet.parse_packet(self.rx_packet)
            self.ack_packet_number, self.goodput = self.data.unpack_data(data)
            if DEBUG:
                print "rx_packet_number=%d  time_stamp=%f  location=%d  flags=0x%x" %(rx_packet_number,
                                                                                      time_stamp,
                                                                                      location,
                                                                                      flags)
                print "goodput for acknowledged packet #%d = %f bits/second" %(self.ack_packet_number, self.goodput)

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


    def _fsm(self):
                self._listen()
                time.sleep(0.01)
                self._send_packet()
                time.sleep(0.01)
                self._receive_packet()
                time.sleep(0.01)



    def control_radio_operation(self, command):
        """
        Control radio operation.

        This function provides a method of controlling operation of the
        radio.

        Parameters
        ----------
        command : str
            One of {`pause` | `continue` | `reconfigure` | ... }
        """
        self.command = command


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

        while not self.stop_event.isSet():
            self._fsm()
            
            if not self.rx_packet == []:
                self.lock.acquire()
                self.kb.sent_packets.append(self.tx_packet_number)
                self.kb.ack_packets.append((self.ack_packet_number, self.goodput))
                self.lock.release()
            self.tx_packet_number += 1

                








    def join(self, timeout=None):
        self.stop_event.set()
        self.radio.shutdown()
        threading.Thread.join(self, timeout)




        # while not self.stop_event.isSet():
        #     if self.command == 'pause':
        #         if self._fsm_state == 'recieve':
        #             self._fsm()
        #         else:
        #             time.sleep(0.01)
        #     continue
                
        #         if do_once:
        #             print "radio paused"
        #         time.sleep(0.001)
        #         continue
            
        #     if self.command == 'continue':
        #         self._fsm()






            # if self._fsm_state == "listen":
            #     self._listen()
            #     self._fsm_state = "send"
            # elif self._fsm_state == "send":
            #     self._send_packet()
            #     self._fsm_state = "receive"
            # elif self._fsm_state == "receive":
            #     self._receive_packet()
            #     self._fsm_state = "listen"
            # else:
            #     print "radio subsystem fsm error"
            #     self._fsm_state = "listen"





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






