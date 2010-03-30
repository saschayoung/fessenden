#!/usr/bin/env python

import struct
import numpy as np

DEBUG = False


def pack_loc(loc):
################################################################################
    loc = repr(loc)
    loc = loc.strip('[]')
    loc = loc.split(',')

    loc[0] = np.float128(loc[0]) 
    loc[1] = np.float128(loc[1])


    if (loc[0] < 0):
        lon_c = np.ceil(loc[0])
    else:
        lon_c = np.floor(loc[0])
    lon_m = loc[0] - lon_c

    lon1 = struct.pack('!i', int(lon_c))
    lon2 = struct.pack('!d', lon_m)

    if (loc[1] < 0):
        lat_c = np.ceil(loc[1])
    else:
        lat_c = np.floor(loc[1])
    lat_m = loc[1] - lat_c

    lat1 = struct.pack('!i', int(lat_c))
    lat2 = struct.pack('!d', lat_m)

    payload = lon1 + lon2 + lat1 + lat2
    if DEBUG:
        print loc
        print 'lon_c: ', repr(lon_c)
        print 'lon_m: ', repr(lon_m)
        print 'lat_c: ', repr(lat_c)
        print 'lat_m: ', repr(lat_m)

    return payload
################################################################################


def unpack_loc(loc):
################################################################################
    lon_payload = loc[0:12]
    lat_payload = loc[12:24]

    (lon1,) = struct.unpack('!i', loc[0:4])
    (lon2,) = struct.unpack('!d', loc[4:12])

    (lat1,) = struct.unpack('!i', loc[12:16])
    (lat2,) = struct.unpack('!d', loc[16:24])

    lon = np.float128(lon1) + np.float128(lon2)
    lat = np.float128(lat1) + np.float128(lat2)
        
    if DEBUG:
        print lon1,repr(np.float128(lon2))
        print lat1,repr(np.float128(lat2))
        print repr(lon), repr(lat)
    
    return (lon,lat)
################################################################################                    


def pack_time(t):
################################################################################
    t_c = np.floor(t)
    t_m = t - np.floor(t)

    t1 = struct.pack('!I', int(t_c))
    t2 = struct.pack('!d', t_m)

    payload = t1 + t2
    
    return payload
################################################################################


def unpack_time(payload):
################################################################################
    (t_c,) = struct.unpack('!I', payload[0:4])
    (t_m,) = struct.unpack('!d', payload[4:12])

    t = repr(np.float128(t_c) + np.float128(t_m))

    return t
################################################################################



if __name__=='__main__':
    import time
    import test_coords

    tx_loc = test_coords.get_tx_coords()
    print tx_loc
    x = pack_loc(tx_loc)
    print len(x)

    x = unpack_loc(x)
    print x
#     tx_loc_p = pack_loc(tx_loc)
#     tx_loc_unp = unpack_loc(tx_loc_p)
#     print tx_loc_unp
    

    
#     rx_time = np.float128(str('%.10f'%(time.time())))
#     print 'rx_time:\n', repr(rx_time).zfill(10)

#     a1 = pack_time(rx_time)
#     t = unpack_time(a1)
#     print repr(t)
    
    
    




#     # process longitude
#     lon = loc[0]
#     lon = lon.split('.')
#     lon_c = lon[0]
#     lon_m = lon[1]

#   # process latitude
#     lat = loc[1]
#     lat = lat.split('.')
#     lat_c = lat[0]
#     lat_m = lat[1]

#     lon1 = struct.pack('!h', int(lon_c) & 0xffff)
#     lon2 = struct.pack('!Q', int(lon_m) & 0xffffffffffffffff)
# #     print repr(lon1)
# #     print repr(lon2)
# #     print str(repr(lon2))
# #     (test,) = struct.unpack('!q',lon2)
# #     print test
# #     print type(test)
# #     print len(lon_m)
# #     print len(test)

#     lat1 = struct.pack('!h', int(lat_c) & 0xffff)
#     lat2 = struct.pack('!Q', int(lat_m) & 0xffffffffffffffff)

#     lon_payload = lon1 + lon2

#     lat_payload = lat1 + lat2

#     loc_payload = lon_payload + lat_payload
# #     print type(loc_payload)
# #     print len(loc_payload)

#     return loc_payload
