#!/usr/bin/env python

import time, random, os
from geo_utils import geo_utils


DEBUG = False

def time_of_flight(p1,p2):
    """
    calculate direct line time of flight between
    two geographic points
    """
    g = geo_utils()
    d = g.distance(p1,p2)
    tof = d/g.speed_of_light

    return tof

    
def get_move_loc(filename):
    try:
        f = open(filename,'r')
        l = f.readlines()
        f.close()
        l = l[0].split(',')
        lon = np.float64(l[0])
        lat = np.float64(l[1])
        os.remove(filename)
        return [lon,lat]
    except Exception,e:
        if DEBUG:
            print 'Exception: ', e
        return -1


class stochastics:
    """
    class for random events
    """
    def __init__(self):
        random.seed()
        self.max_delay = 50

    def set_packet_error_rate(self,n):
        """
        decimal value between 0 and 1
        """
        self.packet_error_rate = n

    def drop_packet(self):
        r = random.uniform(0,1)
        if (r > self.packet_error_rate):
            return False
        else:
            return True

    def set_max_delay(self,t):
        self.max_delay = t

    def backoff(self):
        """
        beacon random 'backoff time'
        can be as much as 50 seconds
        """
        rand_delay = random.randint(0,self.max_delay)
        if DEBUG:
            print 'random backoff %d seconds' % rand_delay
        time.sleep(rand_delay)


if __name__=='__main__':
    import test_coords
    tx = test_coords.get_tx_coords()
    rx = test_coords.get_boathouse_coords()
    print 'test time: ', time_of_flight(tx,rx)
