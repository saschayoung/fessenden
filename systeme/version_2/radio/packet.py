#!/usr/bin/env python

import struct
import time

class Packet(object):
    """
    Packet structure.

    Packet organization:    
    +---------+------------+----------+-----------------------+
    |  Byte   |  Component |  Field   |  Value                |
    +=========+============+==========+=======================+
    |    0    |            |          | packet_number[23:16]  |
    +---------+            |          |-----------------------+
    |    1    |            | packet   | packet_number[15:8]   |
    +---------+            | number   |-----------------------+
    |    2    |            |          | packet_number[7:0]    |
    +---------+            |----------+-----------------------+
    |    3    |            |          | time_stamp[63:56]     |
    +---------+            |          |-----------------------+
    |    4    |            |          | time_stamp[55:48]     |
    +---------+            |          |-----------------------+
    |    5    |            |          | time_stamp[47:40]     |
    +---------+            |          |-----------------------+
    |    6    |            | time     | time_stamp[39:32]     |
    +---------+            | stamp    |-----------------------+
    |    7    |  Header    |          | time_stamp[31:24]     |
    +---------+            |          |-----------------------+
    |    8    |            |          | time_stamp[23:16]     |
    +---------+            |          |-----------------------+
    |    9    |            |          | time_stamp[15:8]      |
    +---------+            |          |-----------------------+
    |   10    |            |          | time_stamp[7:0]       |
    +---------+            |----------+-----------------------+
    |   11    |            |          | location[15:8]        |
    +---------+            | location |-----------------------+
    |   12    |            |          | location[7:0]         |
    +---------+            |----------+-----------------------+
    |   13    |            | flags    | flags[7:0]            |
    +---------+------------+----------+-----------------------+
    |   14    |            |          |                       |
    +---------+            |          |                       |
    |   ...   |  Payload   | data     |   as the service      |
    +---------+            |          |   requires            |
    |   63    |            |          |                       |
    +---------+------------+----------+-----------------------+

    """

    def __init__(self, node):
        """
        Initialize packet structure.

        Parameters
        ----------
        node : str
            Either `A` or `B`, indicating packet something something
            something.

        Raises
        ------
        ValueError
            If node is not one of {`A` | `B`}.

        """
        if node not in ['A', 'B']:
            print "`node` must be one of {`A` | `B`}."
            raise ValueError

        self.node = node
        self.packet_number = 1


    def set_flags_node_b(self, ack_packet = False, ack_command = False):
        """
        Set header flags for node b.

        Set the lower nibble of the flags field in the header,
        used by the base station when transmitting.


        Parameters
        ----------
        ack_packet : bool
            Used to acknowledge receipt of a data packet sent from the UAV
            to the base station.
        ack_command : bool
            Used to acknowledge receipt of a command sent from the UAV
            to the base station.

        Notes
        -----
        Flags field organization:
        +---------+-----------------+
        |  Bit    |  Flag           |
        +=========+=================+
        |    0    |  node_b         |
        +---------+-----------------+
        |    1    | ack_packet      |
        +---------+-----------------+
        |    2    | ack_command     |
        +---------+-----------------+
        |    3    |  unused         |
        +---------+-----------------+
        |    4    |                 |
        +---------+                 |
        |    5    |  unavailable,   |
        +---------+  used by node_a |
        |    6    |  packet         |
        +---------+                 |
        |    7    |                 |
        +---------+-----------------+

        """
        self.flags = 0x01
        if ack_packet:
            self.flags = self.flags | 0x02
        if ack_command:
            self.flags = self.flags | 0x04



    def set_flags_node_a(self, send_command = False):
        """
        Set header flags for UAV.

        Set the upper nibble of the flags field in the header,
        used by the UAV when transmitting.

        Parameters
        ----------
        send_command : bool
            Used to indicate that UAV is sending a command
            (reconfiguration) to the base station.

        Notes
        -----
        Flags field organization:
        +---------+-----------------+
        |  Bit    |  Flag           |
        +=========+=================+
        |    0    |                 |
        +---------+                 |
        |    1    |  unavailable,   |
        +---------+  used by node_b |
        |    2    |  packet         |
        +---------+                 |
        |    3    |                 |
        +---------+-----------------+
        |    4    |  node_a         |
        +---------+-----------------+
        |    5    | send_command    |
        +---------+-----------------+
        |    6    |  unused         |
        +---------+-----------------+
        |    7    |  unused         |
        +---------+-----------------+

        """
        self.flags = 0x10
        if send_command:
            self.flags = self.flags | 0x20

        

    def make_packet(self, location, data):
        """
        Make packet.

        This function makes/packs/creates a full data packet for
        tranmission.

        Parameters
        ----------
        location : int
            Current location of node.
        data : list
            Data to transmit, maximum length of data is 50 elements.
            Longer lists will be truncated.

        Returns
        -------
        packet : list
            Packet for transmission. The packet is a list with
            64 elements, each element a single byte in the
            packet.
        
        """
        self.packet = []
        self._make_header(location)
        self.packet[0:14] = self.header
        self.packet[14:64] = data
        return self.packet


    def parse_packet(self, packet):
        """
        Parse received packet.

        This function parses (unmakes) a received packet.

        Parameters
        ----------
        packet : list
            Received packet. The packet is a list with
            64 elements, each element a single byte in the
            packet.

        Returns
        -------
        packet_number : int
            Packet number of received packet.
        time_stamp : float
            Time stamp in received packet.
        location : int
            Location of node that generated the received packet.
        flags : byte
            8 bits corresponding to 8 flags. More information as it
            is determined.
        data : list
            Data to transmit, maximum length of data is 50 elements.
            Longer lists will be truncated.
        """
        packet_number, time_stamp, location, flags = self._parse_header(packet[0:14])
        data = packet[14:64]
        return packet_number, time_stamp, location, flags, data


    def _make_header(self, location):
        """
        Make packet header.

        This function packs (makes) the header used in packets
        transmitted between nodes. The header 
        contains a packet number (3 bytes), time stamp (8 bytes),
        location (2 bytes), and flags (1 byte).        

        Parameters
        ----------
        location : int
            Current location of node.
        """
        self.header = []
        
        # packet number
        n3 = (self.packet_number & 0x00ff0000) >> 16
        n2 = (self.packet_number & 0x0000ff00) >> 8
        n1 = (self.packet_number & 0x000000ff)
        self.header[0:3] = [n3, n2, n1]
        self.packet_number += 1

        # time stamp
        t_array = []
        time_stamp = struct.pack('!d', time.time())
        for i in range(8):
            t_array.append(ord(time_stamp[i]))
        self.header[3:11] = t_array

        # location
        l2 = int(location) & 0xff00
        l1 = int(location) & 0x00ff
        self.header[11:13] = [l2, l1]
        
        # flags
        self.header.append(self.flags)
    

    def _parse_header(self, header):
        """
        Unpack packet header.

        Parameters
        ----------
        header : list
            Header for data packet, first 14 bytes of received packet.

        Returns
        -------
        packet_number : int
            Packet number of received packet.
        time_stamp : float
            Time stamp in received packet.
        location : int
            Location of node that generated the received packet.
        flags : byte
            8 bits corresponding to 8 flags. More information as it
            is determined.

        """
        # packet number
        n3, n2, n1 = header[0:3]
        packet_number = (n3 << 16) + (n2 << 8) + n1

        # time stamp
        t_array = header[3:11]
        s = ''
        for t in t_array:
            s = s + chr(t)
        (time_stamp,) = struct.unpack('!d', s)

        # location
        l2, l1 = header[11:13]
        location = (l2 << 8) + l1

        # flags
        flags = header[13]

        return packet_number, time_stamp, location, flags



if __name__ == '__main__':
    packet = Packet('A')

    location = 15

    data = []
    for i in range(50):
        data.append(0xff)

    for i in range(10):
        packet.set_flags_node_a()
        p = packet.make_packet(location, data)
        packet_number, time_stamp, location, flags, data = packet.parse_packet(p)
        print "packet_number=%d  time_stamp=%f  location=%d  flags=%x" %(packet_number,
                                                                         time_stamp,
                                                                         location,
                                                                         flags)
