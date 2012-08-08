#!/usr/bin/env python

"""
Module: radio_uav

Threaded UAV radio subsystem.
"""

import logging
import threading
import time

import numpy as np

from data import NodeAData
from packet import Packet
from radio_api import RadioAPI


DEBUG = False

class RadioSubsystem(threading.Thread):
    """
    Threaded UAV radio subsystem.

    Enables threaded operation of radio.

    """

    def __init__(self, update_flag, update_data, reconfig_flag):
        """
        Extend threading class.

        Parameters
        ----------
        callback : obj
            Callback for controller, relays data from rf subsystem to
            controller

        """
        threading.Thread.__init__(self)

        self.update_flag = update_flag
        self.update_data = update_data
        self.reconfig_flag = reconfig_flag

        self.stop_event = threading.Event()
        
        self.data = NodeAData()
        self.packet = Packet('A')
        self.radio = RadioAPI()

        self.last_state = 'stop'
        self.current_state = 'stop'
        self.current_location = 1
        
        self.tx_packet_number = 1


    def set_state(self, current_state):
        """
        Set state of rf subsystem finite state machine.

        This function provides a method of cotrolling operation of the
        RF subsystem.

        Parameters
        ----------
        state : str
            One of {`stop` | `stream` | `update` | `reconfigure`}

        """
        if current_state not in ['stop', 'stream', 'update', 'reconfigure']:
            print "State error: `current_state` must be one of"
            print "{`stop` | `stream` | `update` | `reconfigure`}."
            raise ValueError
        self.current_state = current_state




    def run(self):
        """
        Run the radio subssytem.

        Start the threaded radio subsystem using `RadioSubsystem.start()`.

        """

        self.radio.startup()

        index = 0
        rssi = []

        # TODO: record RSSI before every tranmission
        while not self.stop_event.isSet():

            ###################################################################
            if self.current_state == 'stop':
                if self.last_state == 'stop':
                    continue

                # `update` and `reconfigure` should stop on their own
                elif self.last_state == 'stream':  
                    self.last_state = 'stop'
                    logging.info("radio_subsystem::run: stop")
                    continue
                

                elif self.last_state == 'update':  
                    self.last_state = 'stop'
                    logging.info("radio_subsystem::run: stop")
                    continue


                elif self.last_state == 'reconfigure':  
                    self.last_state = 'stop'
                    logging.info("radio_subsystem::run: stop")
                    continue


                else:
                    logging.debug("radio_subsystem::Error 1 in RadioSubsystem.run()")
                    logging.debug("radio_subsystem::self.current_state == %s" %(self.current_state,))
                    logging.debug("radio_subsystem::last state == %s" %(self.last_state,))
                    continue
            ###################################################################


            ###################################################################
            elif self.current_state == 'stream':
                if self.last_state in ['stop', 'stream']:
                    self.last_state = 'stream'
                    # logging.info("radio_subsystem::run: stream")

                    self.radio.configure_radio(self.eirp, self.frequency, self.bitrate, self.modulation)
                    rssi.append(self.radio.get_rssi_dBm())
                    self._send_packet('stream_data')
                    index += 1

                    continue

                else:
                    logging.debug("radio_subsystem::Error 2 in RadioSubsystem.run()")
                    logging.debug("radio_subsystem::self.current_state == %s" %(self.current_state,))
                    logging.debug("radio_subsystem::last state == %s" %(self.last_state,))
                    continue
            ###################################################################
                


            ###################################################################
            elif self.current_state == 'update':
                if self.last_state == 'stop':
                    self.last_state = 'update'
                    logging.info("radio_subsystem::run: update")

                    self.radio.configure_radio(self.eirp, self.frequency, self.bitrate, self.modulation)
                    self._send_packet('request_data')

                    pkt_num, loc, flags, data = self._receive_packet()
                    packets_received = self.data.unpack_data(data)

                    logging.info("radio_subsystem::packets received by Node B = %d" %(packets_received,))
                    logging.info("radio_subsystem::packets sent by Node A = %d" %(index,))

                    rssi = np.array(rssi)
                    rssi = np.mean(rssi)

                    self.update_data(tx_packets=index, rx_packets=packets_received, signal_strength=rssi)
                    self.update_flag(flag=True)

                    index = 0
                    rssi = []

                    self.current_state = 'stop'
                    continue

                else:
                    logging.debug("radio_subsystem::Error 3 in RadioSubsystem.run()")
                    logging.debug("radio_subsystem::self.current_state == %s" %(self.current_state,))
                    logging.debug("radio_subsystem::last state == %s" %(self.last_state,))
                    continue
            ###################################################################
                    

            ###################################################################
            elif self.current_state == 'reconfigure':
                if self.last_state == 'stop':
                    self.last_state = 'reconfigure'
                    logging.info("radio_subsystem::run: reconfigure")
                    self.radio.configure_radio(self.eirp, self.frequency, self.bitrate, self.modulation)
                    self._send_packet('send_reconfig_command', self.reconfig_mod,
                                      self.reconfig_eirp, self.reconfig_bitrate)

                    pkt_num, loc, flags, data = self._receive_packet()
                    print pkt_num, loc, flags, data
                    if (flags & 0x04) == 0x04:
                        logging.info("radio_subsystem::run: reconfigure acknowledged")
                        self.reconfig_flag(flag=True)
                        self.current_state = 'stop'
                        continue

                    else:
                        logging.debug("radio_subsystem::Warning 1 in RadioSubsystem.run()")
                        logging.debug("radio_subsystem::reconfig request not acknolwedged")
                        logging.debug("radio_subsystem::flagse = 0x%x" %(flags,))
                        continue

                else:
                    logging.debug("radio_subsystem::Error 4 in RadioSubsystem.run()")
                    logging.debug("radio_subsystem::self.current_state == %s" %(self.current_state,))
                    logging.debug("radio_subsystem::last state == %s" %(self.last_state,))
                    continue
            ###################################################################


            ###################################################################
            else:
                logging.debug("radio_subsystem::Error 5 in RadioSubsystem.run()")
                logging.debug("radio_subsystem::self.current_state == %s" %(self.current_state,))
                logging.debug("radio_subsystem::last state == %s" %(self.last_state,))
                continue
            ###################################################################
                    






    def _send_packet(self, mode, mod=None, eirp=None, bitrate=None):
        """
        Transmit data.

        Parameters
        ----------
        mode : str
            Mode of operation. Used to create appropriate packet header and payload.
            {`send_reconfig_command` | `request_data` | `stream_data`}.
        mod : str, opt
            Modulation, one of {`fsk` | `gfsk` | `ook` }.
        eirp : int, opt
            Transmit power, one of { 8 | 11 | 14 | 17 }.
        bitrate : float, opt
            Radio bitrate, one of {...}
            
        """

        if mode == 'stream_data':
            self.packet.set_flags_node_a(send_stream=True)
            payload = self.data.pack_data(mode)

        elif mode == 'send_reconfig_command':
            self.packet.set_flags_node_a(send_command=True)
            payload = self.data.pack_data(mode, mod, eirp, bitrate)

        elif mode == 'request_data':
            self.packet.set_flags_node_a(request_data=True)
            payload = self.data.pack_data(mode)

        else:
            print "error in _send_packet, no mode specified"
            raise ValueError

        tx_packet = self.packet.make_packet(self.tx_packet_number, self.current_location, payload)
        self.tx_packet_number += 1
        self.radio.transmit(tx_packet)
        # logging.info("packet sent")


    def _receive_packet(self):
        """
        Receive packet

        """
        rx_packet = self.radio.receive(rx_fifo_threshold=64, timeout=None)
        pkt_num, t, loc, flags, data = self.packet.parse_packet(rx_packet)

        return pkt_num, loc, flags, data

                    
    def set_current_location(self, current_location):
        """
        Set current location.

        Used by controller to tell radio subsytem the current physical
        location.

        Parameters
        ----------
        current_location : int
            Value of barcode representing current location.

        """

        self.current_location = current_location


    def set_config_packet_data(self, modulation, eirp, bitrate):
        """
        Set reconfig-packet data.

        This function is used by the controller to set the contents of
        the packet that is used in a reconfiguration request. NOTE:
        use this function to set the config packet data *before*
        sending a reconfiguration packet.

        """
        self.reconfig_mod = modulation
        self.reconfig_eirp = eirp
        self.reconfig_bitrate = bitrate

            
    def set_radio_configuration(self, modulation, eirp, bitrate, frequency):
        """
        Set radio configuration.

        This function is used by the controller to set the local radio
        configuration.

        Parameters
        ----------
        modulation : str
            Modulation, one of {`fsk` | `gfsk` | `ook` }.
        eirp : int
            Transmit power, one of { 8 | 11 | 14 | 17 }.
        bitrate : float
            Radio bitrate, one of {...}
        frequency : float
            Center frequency, this should be between 240.0e6 and 930.0e6.
         
        """
        self.modulation = modulation
        self.eirp = eirp
        self.bitrate = bitrate
        self.frequency = frequency
        

    def join(self, timeout=None):
        """
        Stop radio subsystem.

        """
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






    #     self._fsm_state = 'listen'
    #     self.radio_command = 'continue'
    #     self.tx_packet_number = 1

    #     self.ack_packet_number = 0
    #     self.goodput = 0






















    # def configure_radio(self, power, frequency, data_rate, modulation):
    #     """
    #     Configure radio for operation.

    #     """
    #     self.radio.configure_radio(power, frequency, data_rate, modulation)
        

    # def _send_packet(self):
    #     """
    #     Transmit packet.

    #     """
    #     self.packet.set_flags_node_a()
    #     # location = self.kb.get_state()['current_location']
    #     data = self.data.pack_data()
    #     tx_packet = self.packet.make_packet(self.tx_packet_number, location, data)
    #     # self.tic = time.time()
    #     self.radio.transmit(tx_packet)


    # def _receive_packet(self):
    #     """
    #     Receive packet.

    #     """
    #     # print "processing latency = %f" %(time.time() - self.tic,)
    #     self.rx_packet = self.radio.receive(rx_fifo_threshold=64, timeout=0.8)
    #     if self.rx_packet == []: # this occurs when timeout has been exceeded
    #         # print "timeout exceeded"
    #         return
    #     else:
    #         rx_packet_number, time_stamp, location, flags, data = self.packet.parse_packet(self.rx_packet)
    #         self.ack_packet_number, self.goodput = self.data.unpack_data(data)
    #         if DEBUG:
    #             pass



    # def _listen(self):
    #     """
    #     Listen before talk.

    #     """
    #     status = self.radio.listen(rssi_threshold=100, timeout=1.0)
    #     if status == 'clear':
    #         if DEBUG:
    #             print "channel clear"
    #         else:
    #             pass


    # def _fsm(self):
    #             self._listen()
    #             time.sleep(0.01)
    #             self._send_packet()
    #             time.sleep(0.01)
    #             self._receive_packet()
    #             time.sleep(0.01)



    # def control_radio_operation(self, command):
    #     """
    #     Control radio operation.

    #     This function provides a method of controlling operation of the
    #     radio.

    #     Parameters
    #     ----------
    #     command : str
    #         One of {`pause` | `continue` | `reconfigure` | ... }

    #     """
    #     self.radio_command = command


    # def run(self):
    #     """
    #     Run the radio subsystem.

    #     """
    #     print "Starting radio subsystem"

    #     self.radio.startup()
    #     # default_radio_profile = self.kb.get_state()['default_radio_profile']
    #     power = default_radio_profile['power']
    #     frequency = default_radio_profile['frequency']
    #     data_rate = default_radio_profile['data_rate']
    #     modulation = default_radio_profile['modulation']
    #     self._configure_radio(power, frequency, data_rate, modulation)

    #     while not self.stop_event.isSet():

    #         if self.radio_command == 'continue':
    #             self._fsm()
    #             if not self.rx_packet == []:
    #                 self.controller_callback(self.tx_packet_number, self.ack_packet_number, self.goodput)
    #                 # self.lock.acquire()
    #                 # self.kb.sent_packets.append(self.tx_packet_number)
    #                 # self.kb.ack_packets.append((self.ack_packet_number, self.goodput))
    #                 # self.lock.release()
    #             self.tx_packet_number += 1

    #         elif self.radio_command == 'pause':
    #             time.sleep(0.01)
    #             continue

    #         elif self.radio_command == 'reconfigure':
    #             pass
