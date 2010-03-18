#!/usr/bin/env python


# ignore deprecation warning from struct.unpack('!h'...
import warnings
warnings.filterwarnings("ignore")


import random, struct
import numpy as np


def power(dist):
    __power = random.random()
    return __power


def pack_loc(loc):
    loc = repr(loc)
    loc = loc.strip('[]')
    loc = loc.split(',')

    # process longitude
    lon = loc[0]
    lon = lon.split('.')
    lon_c = lon[0]
    lon_m = lon[1]
#     print lon_m
#     print int(lon_m)
#     print type (lon_m)

  # process latitude
    lat = loc[1]
    lat = lat.split('.')
    lat_c = lat[0]
    lat_m = lat[1]

    lon1 = struct.pack('!h', int(lon_c) & 0xffff)
    lon2 = struct.pack('!Q', int(lon_m) & 0xffffffffffffffff)
#     print repr(lon1)
#     print repr(lon2)
#     print str(repr(lon2))
#     (test,) = struct.unpack('!q',lon2)
#     print test
#     print type(test)
#     print len(lon_m)
#     print len(test)

    lat1 = struct.pack('!h', int(lat_c) & 0xffff)
    lat2 = struct.pack('!Q', int(lat_m) & 0xffffffffffffffff)

    lon_payload = lon1 + lon2

    lat_payload = lat1 + lat2

    loc_payload = lon_payload + lat_payload
#     print type(loc_payload)
#     print len(loc_payload)

    return loc_payload

def unpack_loc(loc):

    lon_payload = loc[0:10]
    lat_payload = loc[10:20]

    (lon1,) = struct.unpack('!h', loc[0:2])
    (lon2,) = struct.unpack('!Q', loc[2:10])

    (lat1,) = struct.unpack('!h', loc[10:12])
    (lat2,) = struct.unpack('!Q', loc[12:20])


    
    lon = np.float64(repr(lon1) + '.' + repr(lon2).zfill(15))
    lat = np.float64(repr(lat1) + '.' + repr(lat2).zfill(15))


    return [lon,lat]

    



def pack_time(t):
    t = repr(t)

    print "pack_time(t): ", repr(t)
    t = t.split('.')
    t_c = t[0]
    t_m = t[1]

    print "t_m: ", t_m
    print "len(t_m): ", len(t_m)

    if t_m[0] == '0':
        print "warning!! fractional part of time has leading zero!!"
        t_m = '-1'+t_m[1:]
#         print ""
#         print t_m
#         print "^"
#         print ""

    t1 = struct.pack('!L', int(t_c) & 0xffffffff)
    t2 = struct.pack('!Q', int(t_m) & 0xffffffffffffffff)

    payload = t1 + t2
    

    return payload


def unpack_time(payload):
    (t_c,) = struct.unpack('!L', payload[0:4])
    (t_m,) = struct.unpack('!Q', payload[4:12])
#     s = repr(t_c) + '.' + repr(t_m).zfill(10)

    time = repr(t_m).zfill(10)
    if time[0:2] == '-1':
        time = '0' + time[2:]
    s = repr(t_c) + '.' + time

    print "unpack_time:"
    print "s = repr(t_c) + '.' + repr(t_m).zfill(10): ", repr(s)


    t = np.float128(s)
    print "t = np.float128(s): ", repr(t)

    return t



if __name__=='__main__':
    import time
    import test_coords

#     tx_loc = test_coords.get_tx_coords()
#     print tx_loc
#     tx_loc_p = pack_loc(tx_loc)
#     tx_loc_unp = unpack_loc(tx_loc_p)
#     print tx_loc_unp
    

    
    rx_time = np.float128(str('%.10f'%(time.time())))
    print 'rx_time:\n', repr(rx_time).zfill(10)

    a1 = pack_time(rx_time)
    t = unpack_time(a1)
    print repr(t)
    
    
    

