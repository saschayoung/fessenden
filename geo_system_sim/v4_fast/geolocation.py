#!/usr/bin/env python

import time, random, struct
import numpy as np

from geo_utils import geo_utils


class geolocation:
    """
    Geolocation module
    """

    def __init__(self):
        self.DEBUG = False
        self.ERR = False

        self.geo_utils = geo_utils()

    def tdoa(self,loc,time):
        self.loc = loc
        self.toa = time
        loc0 = self.loc[0]
        loc1 = self.loc[1]
        loc2 = self.loc[2]
        
        toa0 = self.toa[0]
        toa1 = self.toa[1]
        toa2 = self.toa[2]
        if self.DEBUG:
            print self.loc
            print self.toa

        if ( (toa0 == toa1) and (toa0 == toa2) ):
            if self.ERR:
                print '\n\n\n\n\n\n\nerror!!!'
                print "(toa0 == toa1) and (toa0 == toa2)!!"
                print '\n\n\n\n\n\n\n'
            return -1

        elif ( (toa0 == toa1) and not (toa0 == toa2) ):
            (x_h1,y_h1) = self.geo_utils.hyperbola(loc2,loc1,toa2,toa1)
            (x_h2,y_h2) = self.geo_utils.hyperbola(loc0,loc2,toa0,toa2)
        elif ( not (toa0 == toa1) and  (toa0 == toa2) ):
            (x_h1,y_h1) = self.geo_utils.hyperbola(loc0,loc1,toa0,toa1)
            (x_h2,y_h2) = self.geo_utils.hyperbola(loc1,loc2,toa1,toa2)
        else:
            (x_h1,y_h1) = self.geo_utils.hyperbola(loc0,loc1,toa0,toa1)
            (x_h2,y_h2) = self.geo_utils.hyperbola(loc0,loc2,toa0,toa2)
            

        if ( np.isnan(x_h1[0]) or np.isnan(y_h1[0]) ):
            if self.ERR:
                print '\n\n\n\n\n\n\n\n\n\n\n\n\nerror!!!'
                print "np.isnan(x_h1[0]) or np.isnan(y_h1[0])!!"
                print '\n\n\n\n\n\n\n\n\n\n\n\n\n'        
            return -1

        if ( np.isnan(x_h2[0]) or np.isnan(y_h2[0]) ):
            if self.ERR:
                print '\n\n\n\n\n\n\n\n\n\n\n\n\nerror!!!'
                print "np.isnan(x_h2[0]) or np.isnan(y_h2[0])!!"
                print '\n\n\n\n\n\n\n\n\n\n\n\n\n'
            return -1
        
        (x_coords,y_coords) = self.geo_utils.intersections(x_h1,y_h1,x_h2,y_h2)
        
        if ( (x_coords == -1) and (y_coords == -1) ):
            if self.ERR:
                print "intersection.m returns no data, return -1 to main"
            return -1
        

        if self.DEBUG:
            print loc0
            print loc1
            print loc2

        return [x_coords, y_coords]

    def custom(self):
        """
        This is the container method for Hedieh's code
        """
        pass
