#!/usr/bin/env python

import struct
import time


class UAVPacket(object):
    """
    Packet structure for UAV node.
    """
    def __init__(self):
        self.packet_number = 1

    def _pack_header(self, loc, flags):
        """
        Pack UAV transmit packet header.

        This function packs (creates) the header used in packets
        transmitted by UAV nodes to base station nodes. The header 
        contains a packet number (4 bytes), time stamp (8 bytes),
        location (1 byte), and flag bits (1 byte).        

        Parameters
        ----------
        loc : byte
            Current location of UAV.
            TODO: this only allows 255 location, may need to increase
            the size of this.
        flags : byte
            8 bits corresponding to 8 flags. More information as it
            is determined.

        Returns
        -------
        header : list
            Header for base station transmit packet. The header is a
            list with 14 elements, each element a single byte in
            the packet header.
        """
        header = []
        
        # packet number
        n4 = int((self.packet_number & 0xff000000) >> 24)
        n3 = (self.packet_number & 0x00ff0000) >> 16
        n2 = (self.packet_number & 0x0000ff00) >> 8
        n1 = (self.packet_number & 0x000000ff)
        header[0:4] = [n4, n3, n2, n1]
        self.packet_number += 1

        # time stamp
        # print "time.time() :", time.time()
        t = struct.pack('!d', time.time())
        t_array = []
        for i in range(8):
            t_array.append(ord(t[i]))
        # print "t_array: ", t_array
        header[4:12] = t_array

        # loc and flags
        loc = loc & 0xff
        flags = flags & 0xff
        header[12:14] = [loc, flags]

        return header


    def _unpack_header(self, header):
        """
        Unpack UAV receive packet header.

        This function unpacks the header used in packets
        received UAV nodes from base station nodes. The header 
        contains a packet number (4 bytes) and flag bits (1 byte).        


        Parameters
        ----------
        header : list
            Header for UAV receive. The header is a list with
            five elements, each element a single byte in the
            packet header.

        Returns
        -------
        packet_number : int
            Packet number of received packet.
        flags : byte
            8 bits corresponding to 8 flags. More information as it
            is determined.
        """
        # packet number
        n4, n3, n2, n1 = header[0:4]
        packet_number = (n4 << 24) + (n3 << 16) + (n2 << 8) + n1

        # flags 
        flags = header[-1]

        return packet_number, flags




    def make_packet(self, loc, flags, data):
        """
        Make UAV transmit packet.

        This function creates a packet for transmission
        by UAV to a base station. The maximum length of
        a packet is 64 bytes, including header and data.

        Parameters
        ----------
        loc : byte
            Current location of UAV.
            TODO: this only allows 255 location, may need to increase
            the size of this.
        flags : byte
            8 bits corresponding to 8 flags. More information as it
            is determined.
        data : list
            Data to transmit. Each element in the list is a single byte
            of data.

        Returns
        -------
        packet : list
            Packet for UAV transmit. The packet is a list with
            64 elements, each element a single byte in the
            packet.
        """
        packet = []
        packet[0:14] = self._pack_header(loc, flags)
        packet[14:64] = data

        return packet


    def parse_packet(self, packet):
        """
        Parse a received packet.

        This function parses the packet received by UAV nodes from
        base station nodes.

        Parameters
        ----------
        packet : list
            Packet received by UAV. The packet is a list with
            64 elements, each element a single byte in the
            packet.
        
        Returns
        -------
        packet_number : int
            Packet number of received packet.
        flags : byte
            8 bits corresponding to 8 flags. More information as it
            is determined.
        data : list
            Data to transmit. Each element in the list is a single byte
            of data.
        """
        packet_number, flags = self._unpack_header(packet[0:5])
        data = packet[5:64]
        return packet_number, flags, data











class BaseStationPacket(object):
    """
    Packet structure for base station node.
    """
    def __init__(self):
        
        self.packet_number = 1

    def _pack_header(self, flags):
        """
        Pack base station tx packet header.

        This function packs (creates) the header used in packets
        transmitted by base station nodes to UAV nodes. The header 
        contains a packet number (4 bytes) and flag bits (1 byte).        

        Parameters
        ----------
        flags : byte
            8 bits corresponding to 8 flags. More information as it
            is determined.

        Returns
        -------
        header : list
            Header for base station transmit packet. The header is a
            list with five elements, each element a single byte in
            the packet header.
        """
        header = []

        # packet number
        n4 = int((self.packet_number & 0xff000000) >> 24)
        n3 = (self.packet_number & 0x00ff0000) >> 16
        n2 = (self.packet_number & 0x0000ff00) >> 8
        n1 = (self.packet_number & 0x000000ff)
        header[0:4] = [n4, n3, n2, n1]
        self.packet_number += 1

        # flags
        header.append(flags & 0xff) 

        return header



    def _unpack_header(self, header):
        """
        Unpack base station rx header.

        This function unpacks the header used in packets
        received by base station nodes from UAV nodes. 

        Parameters
        ----------
        header : list
            Header for base station transmit packet. The header is a
            list with 14 elements, each element a single byte in
            the packet header.

        Returns
        -------
        packet_number : int
            Packet number of received packet.
        r_timestamp : float
            Remote timestamp, timestamp from UAV when sending packet.
        l_timestamp : float
            Local timestamp, timestamp from base staion, generated at
            location in the process comparable to UAV timestamp generation.
        loc : byte
            Current location of UAV.
            TODO: this only allows 255 location, may need to increase
            the size of this.
        flags : byte
            8 bits corresponding to 8 flags. More information as it
            is determined.

        """
        # packet number
        n4, n3, n2, n1 = header[0:4]
        packet_number = (n4 << 24) + (n3 << 16) + (n2 << 8) + n1
        t_array = header[4:12]
        # print "t_array: ", t_array

        # time stamps
        s = ''
        for t in t_array:
            s = s + chr(t)
        (r_timestamp,) = struct.unpack('!d', s)
        l_timestamp = time.time()

        # location and flags
        (loc, flags) = header[12:14]

        return packet_number, r_timestamp, l_timestamp, loc, flags


    def make_packet(self, flags, data):
        """
        Make base station transmit packet.

        This function creates a packet for transmission
        by base station to a UAV. The maximum length of
        a packet is 64 bytes, including header and data.

        Parameters
        ----------
        flags : byte
            8 bits corresponding to 8 flags. More information as it
            is determined.
        data : list
            Data to transmit. Each element in the list is a single byte
            of data.

        Returns
        -------
        packet : list
            Packet for base station transmit. The packet is a list with
            64 elements, each element a single byte in the packet.
        """
        # print loc
        packet = []
        packet[0:5] = self._pack_header(flags)
        packet[5:64] = data
        return packet


    def parse_packet(self, packet):
        """
        Parse a received packet.

        This function parses the packet received by base station
        odes from UAV nodes.

        Parameters
        ----------
        packet : list
            Packet received by UAV. The packet is a list with
            64 elements, each element a single byte in the
            packet.

        Returns
        -------
        packet_number : int
            Packet number of received packet.
        r_timestamp : float
            Remote timestamp, timestamp from UAV when sending packet.
        l_timestamp : float
            Local timestamp, timestamp from base staion, generated at
            location in the process comparable to UAV timestamp generation.
        loc : byte
            Current location of UAV.
            TODO: this only allows 255 location, may need to increase
            the size of this.
        flags : byte
            8 bits corresponding to 8 flags. More information as it
            is determined.
        data : list
            Received data. Each element in the list is a single byte
            of data.
        """
        packet_number, r_timestamp, l_timestamp, loc, flags = self._unpack_header(packet[0:14])
        data = packet[12:64]
        return packet_number, r_timestamp, l_timestamp, loc, flags, data




if __name__=='__main__':
    packet = Packet()
    data = []
    for i in range(52):
        data.append(0xff)

    # for j in range(50):
    while True:
        p = packet.make_packet(data)
        # time.sleep(0.5)
        packet_number, r_timestamp, l_timestamp, rx_data = packet.parse_packet(p)

        # print "packet_number: ", packet_number
        # print "time difference: ", l_timestamp - r_timestamp
        # print "data == data?: ", data == rx_data
















# class Packet(object):
#     def __init__(self):
#         self.packet_number = 1

#     def _pack_header(self, loc, flags):
#         # print loc
#         header = []
#         n4 = int((self.packet_number & 0xff000000) >> 24)
#         n3 = (self.packet_number & 0x00ff0000) >> 16
#         n2 = (self.packet_number & 0x0000ff00) >> 8
#         n1 = (self.packet_number & 0x000000ff)
#         header[0:4] = [n4, n3, n2, n1]
#         self.packet_number += 1

#         t = struct.pack('!d', time.time())
#         t_array = []
#         for i in range(8):
#             t_array.append(ord(t[i]))
#         header[4:12] = t_array
#         header[12:14] = [loc, flags]


#         return header


#     def _unpack_header(self, header):
#         n4, n3, n2, n1 = header[0:4]
#         packet_number = (n4 << 24) + (n3 << 16) + (n2 << 8) + n1
#         t_array = header[4:12]
#         s = ''
#         for t in t_array:
#             s = s + chr(t)
#         (r_timestamp,) = struct.unpack('!d', s)
#         l_timestamp = time.time()
#         (loc, flags) = header[12:14]
#         # flags = header[14]
#         return packet_number, r_timestamp, l_timestamp, loc, flags


#     def _pack_data(self, data):
#         pass



#     def _unpack_data(self, packet):
#         pass



#     def make_packet(self, loc, flags, data):
#         """
#         Make a packet to transmit.
#         """
#         # print loc
#         packet = []
#         packet[0:14] = self._pack_header(loc, flags)
#         packet[14:64] = data
#         return packet


#     def parse_packet(self, packet):
#         """
#         Parse a received packet.
#         """
#         packet_number, r_timestamp, l_timestamp, loc, flags = self._unpack_header(packet[0:14])
#         data = packet[12:64]
#         return packet_number, r_timestamp, l_timestamp, loc, flags, data
