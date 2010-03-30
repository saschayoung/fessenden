#!/usr/bin/env python

import numpy as np



DEBUG = False

class geo_utils:
    
    '''
    Functions for geographic and geolocation math
        earth_radius = np.float(6371e3)
        speed_of_light = np.float(299792458.0)

        distance(self,p1,p2)
        midpoint(self,p1,p2)
        hyperbola(self,p1,p2,toa1,toa2)
    '''
    
    def __init__(self):

        '''
        Set default values
        '''

        # administrivia
        self.earth_radius = np.float(6371e3)
        self.speed_of_light = np.float(299792458.0)


    def distance(self,p1,p2):
        '''
        calculates distance between 2 points on earths surface
        assumes same hemisphere (i think) uses mean earth radius
        r = 6371 km

        input: p1,p2   location in the form (lat,lon)
        return: d      distance in meters
        '''
        lon1 = p1[0] / 180 * np.pi
        lat1 = p1[1] / 180 * np.pi

        lon2 = p2[0] / 180 * np.pi
        lat2 = p2[1] / 180 * np.pi

        e = np.arccos( np.sin(lat1)*np.sin(lat2) +
                       np.cos(lat1)*np.cos(lat2)*np.cos(lon2-lon1) )
        d = e * self.earth_radius

        return d
    

    def midpoint(self,p1,p2):
        '''
        calculates midpoint between 2 points on earths surface
        assumes points are not geographically diverse so that 
        ( (x1+x2)/2, (y1+y2)/2 ) is not sufficiently different from
        midpoint along great circle route

        input: p1,p2   location in the form (lat,lon)
        return: m      midpoint in the form (lat,lon)
        '''
        lon = ( p1[0]+p2[0] )/2.0
        lat = ( p1[1]+p2[1] )/2.0

        m = (lon,lat)

        return m


    def hyperbola(self,p1,p2,toa1,toa2):
        '''
        calculates the asymptotes of hyperbola that represents equidifference
        curves for time of arrival (TDOA) for two points.

        input:
               p1,p2           location in the form (lat,lon)
               toa1,toa2       timestamp in seconds

        return:
               (x1,y1,x2,y2)   x & y coordinates of asymptotes 1 & 2
        '''

        if DEBUG:
            print "p1: ", p1
            print "p2: ", p2
            print "toa1: ", repr(toa1)
            print "toa2: ", repr(toa2)
            print "type(toa1): ", type(toa1)
            print "type(toa2): ", type(toa2)
        x1 = p1[0]
        y1 = p1[1]

        x2 = p2[0]
        y2 = p2[1]

        # angle between two locations and 'horizontal'
        alpha = np.arctan((y2-y1)/(x2-x1))
        if DEBUG:
            print "alpha: ", alpha

        # approx. midpoint between two locations
        midpoint = self.midpoint(p1,p2)
        x_0 = midpoint[0]
        y_0 = midpoint[1]


        # 3) determine hyperbola asymptotes
        a = (0.5)*self.speed_of_light*(np.abs(toa1 - toa2))/(60*1852)
        distance = self.distance(p1,p2)/(60*1852)
        b = np.sqrt((distance/2.0)**2 - a**2)
        asymp_slope = (b/a, -b/a)


        # hyperbolas
        t = np.linspace(-3,3,100)

        # t = np.linspace(-2,2,100)

        dd = self.speed_of_light*((toa1 - toa2))/(60*1852)
        if x1 < x2:
            if DEBUG:
                print "x1 < x2"
                print "dd: ", dd
            if dd < 0:
                if DEBUG:
                    print "dd < 0"
                x_hyperbola = -a*np.cosh(t)
                y_hyperbola = b*np.sinh(t)
            else:  # dd > 0
                if DEBUG:
                    print "dd > 0"
                x_hyperbola = a*np.cosh(t)
                y_hyperbola = b*np.sinh(t)
        else:  # x1 > x2
            if DEBUG:
                print "x1 > x2"
                print "dd: ", dd
            if dd > 0:
                if DEBUG:
                    print "dd > 0"
                x_hyperbola = -a*np.cosh(t)
                y_hyperbola = b*np.sinh(t)
            else:  # dd < 0:
                if DEBUG:
                    print "dd < 0"
                x_hyperbola = a*np.cosh(t)
                y_hyperbola = b*np.sinh(t)
        
        
        x_hyperbola_p = x_hyperbola*np.cos(alpha) - y_hyperbola*np.sin(alpha)+x_0
        y_hyperbola_p = x_hyperbola*np.sin(alpha) + y_hyperbola*np.cos(alpha)+y_0
        

        return (x_hyperbola_p,y_hyperbola_p)


