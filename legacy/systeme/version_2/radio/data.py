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

    def pack_data(self, packet_number, goodput):
        data = []
        # packet_number
        n3 = (packet_number & 0x00ff0000) >> 16
        n2 = (packet_number & 0x0000ff00) >> 8
        n1 = (packet_number & 0x000000ff)
        data[0:3] = [n3, n2, n1]

        # goodput
        g_array = []
        g  = struct.pack('!d', goodput)
        for i in range(8):
            g_array.append(ord(g[i]))
        data[3:11] = g_array

        # data padding
        for i in range(39):
            data.append(0xff)

        return data




if __name__=='__main__':
    b = NodeBData()
    a = NodeAData()
    data = b.pack_data(1336, 2582.309935)
    print data
    print len(data)
    n, g = a.unpack_data(data)
    print n, g
