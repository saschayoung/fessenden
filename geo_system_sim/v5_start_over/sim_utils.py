#!/usr/bin/env python

from geo_utils import geo_utils


DEBUG = False


    
'''
Functions for radio geolocation simulation
'''

def time_of_flight(p1,p2):
    
    g = geo_utils()
    d = g.distance(p1,p2)
    tof = d/g.speed_of_light

    return tof




if __name__=='__main__':
    import test_coords
    tx = test_coords.get_tx_coords()
    rx = test_coords.get_boathouse_coords()
    print 'test time: ', time_of_flight(tx,rx)
