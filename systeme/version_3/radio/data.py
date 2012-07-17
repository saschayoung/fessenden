#!/usr/bin/env python


import struct

class NodeAData(object):
    def __init__(self):
        pass


    def pack_data(self):
        data = []
        for i in range(50):
            data.append(0xff)
        return data


    def unpack_data(self, data):
        n3, n2, n1 = data[0:3]
        packet_number = (n3 << 16) + (n2 << 8) + n1

        # time stamp
        g_array = data[3:11]
        s = ''
        for g in g_array:
            s = s + chr(g)
        (goodput,) = struct.unpack('!d', s)
        
        return packet_number, goodput
        




class NodeBData(object):
    def __init__(self):
        pass


    def pack_data(self, mode, received_packets = None):
        """
        Create packet payload.

        Parameters
        ----------
        mode : str
            Mode of operation, used to create appropriate
            data payload. One of {`ack_command` | `send_data`}.
        received_packets : int, opt
            Number of packets received by Node B.

        Returns
        -------
        data : list
            List of 50 elements where each element is part of the packet
            payload.
            
        """
        data = []
        if mode == 'ack_command':
            data = [0 for i in range(50)]
            return data
        elif mode == 'send_data':
            if received_packets == None:
                print "mode is `send_data`, but `received_packets` is `None`"
                raise ValueError
            n2 = (received_packets & 0x0000ff00) >> 8
            n1 = (received_packets & 0x000000ff)
            data[0:2] = [n2, n1]
            data[2:48] = [0 for i in range(48)]
            return data
            
        else:
            print 'error in pack_data, no mode specified'
            raise ValueError
        




    def unpack_data(self, data):
        """
        Unpack packet payload.

        Parameters
        ----------
        data : list

        Returns
        -------
        mod : str
            Modulation, one of {`fsk` | `gfsk` | `ook` }.
        eirp : int
            Transmit power, one of { 8 | 11 | 14 | 17 }.
        bitrate : float
            Radio bitrate, one of {...}

        """
        if data[0] == 0x01:
            mod = 'fsk'
        elif data[0] == 0x02:
            mod = 'gfsk'
        elif data[0] = 0x03:
            mod = 'ook'
        else:
            print "error unpacking data[0], value out of bounds."
            raise ValueError


        if data[1] == 0x01:
            eirp = 8
        elif data[1] == 0x02:
            eirp = 11
        elif data[1] = 0x03:
            eirp = 14
        elif data[1] = 0x04:
            eirp = 17
        else:
            print "error unpacking data[1], value out of bounds."
            raise ValueError


        if data[2] == 0x01:
            bitrate = 2e3
        elif data[2] == 0x02:
            bitrate = 2.4e3
        elif data[2] == 0x03:
            bitrate = 4.8e3
        elif data[2] == 0x04:
            bitrate = 9.6e3
        elif data[2] == 0x05:
            bitrate = 19.2e3
        elif data[2] == 0x06:
            bitrate = 38.4e3
        elif data[2] == 0x07:
            bitrate = 57.6e3
        elif data[2] == 0x08:
            bitrate = 125.0e3
        else:
            print "error unpacking data[2], value out of bounds."
            raise ValueError
            
        return mod, eirp, bitrate

    # def pack_data(self, packet_number, goodput):
    #     data = []
    #     # packet_number
    #     n3 = (packet_number & 0x00ff0000) >> 16
    #     n2 = (packet_number & 0x0000ff00) >> 8
    #     n1 = (packet_number & 0x000000ff)
    #     data[0:3] = [n3, n2, n1]

    #     # goodput
    #     g_array = []
    #     g  = struct.pack('!d', goodput)
    #     for i in range(8):
    #         g_array.append(ord(g[i]))
    #     data[3:11] = g_array

    #     # data padding
    #     for i in range(39):
    #         data.append(0xff)

    #     return data




if __name__=='__main__':
    b = NodeBData()
    a = NodeAData()
    data = b.pack_data(1336, 2582.309935)
    print data
    print len(data)
    n, g = a.unpack_data(data)
    print n, g
