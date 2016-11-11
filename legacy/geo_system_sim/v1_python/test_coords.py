#!/usr/bin/env python

import numpy as np

def get_tx_coords():
    tx_lat = np.float64(38.80734722222222)
    tx_lon = np.float64(-77.0647611111111)

    coords = [tx_lon,tx_lat]
    return coords

def get_boathouse_coords():
    tx_lat = np.float64(38.81201111111111)
    tx_lon = np.float64(-77.03778888888888)

    coords = [tx_lon,tx_lat]
    return coords

def get_uspto_coords():
    tx_lat = np.float64(38.80172777777778)
    tx_lon = np.float64(-77.06365833333334)

    coords = [tx_lon,tx_lat]
    return coords

def get_tcwhs_coords():
    tx_lat = np.float64(38.82368333333334)
    tx_lon = np.float64(-77.08458333333333)

    coords = [tx_lon,tx_lat]
    return coords

def get_lee_st_coords():
    tx_lat = np.float64(38.79973611111111)
    tx_lon = np.float64(-77.04163611111112)

    coords = [tx_lon,tx_lat]
    return coords

if __name__ == '__main__':
    tx = get_tx_coords()
    rx1 = get_boathouse_coords()
    rx2 = get_uspto_coords()
    rx3 = get_tcwhs_coords()
    rx4 = get_lee_st_coords()

    print "Transmitter coordinates:\t\t", tx
    print "RX1 - Boathouse coordinates:\t\t",rx1
    print "RX2 - USPTO coordinates:\t\t",rx2
    print "RX3 - TC Williams HS coordinates:\t",rx3
    print "RX4 - Lee St Park coordinates:\t\t",rx4







