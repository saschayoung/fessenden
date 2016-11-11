#!/usr/bin/env python

import os
import numpy as np

# local import
import hyperbola


class geolocation:
    """
    Geolocation module
    """

    def __init__(self):
        self.DEBUG = False
        self.ERR = False

        # self.hyperbola = hyperbola()

    def tdoa(self,loc,time):
        self.loc = loc
        self.toa = time


        x1 = self.loc[0][0]
        y1 = self.loc[0][1]
        x2 = self.loc[1][0]
        y2 = self.loc[1][1]
        x3 = self.loc[2][0]
        y3 = self.loc[2][1]
        
        toa1 = self.toa[0]
        toa2 = self.toa[1]
        toa3 = self.toa[2]

        if self.DEBUG:
            print self.loc
            print self.toa

        string = 'cd matlab_files;matlab -nojvm -nodesktop -nosplash -nodisplay -r \"matlab_gw()\" '



        f = open('./matlab_files/matlab_gw_params','w+')
        f.write('%.15f\n%.15f\n%.15f\n%.15f\n%.15f\n%.15f\n%.10f\n%.10f\n%.10f' %(x1,y1,x2,y2,x3,y3,toa1,toa2,toa3))
        f.close()
        

        os.system(string)


        f = open('results','r')
        a = f.readlines()
        f.close()

        # check to make sure a is even length
        if (len(a) % 2):
            sys.exit('error, odd length vector result')

        try: 
            a = [float(x.strip('\n')) for x in a]
        except ValueError:
            print 'no data in file -> no intersection'
            return (-1,-1)

        x_result = []
        y_result = []

        if ( len(a) > 2 ):
            i = 0
            m = len(a)/2
            while ( i < len(a)/2 ):
                x_result.append(a[i])
                y_result.append(a[m])
                i +=1
                m +=1
        else:
            x_result.append(a[0])
            y_result.append(a[1])


        return [x_result,y_result]



        

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












        # if ( (x_coords == -1) and (y_coords == -1) ):
        #     if self.ERR:
        #         print "intersection.m returns no data, return -1 to main"
        #     return -1



        # if ( (toa0 == toa1) and (toa0 == toa2) ):
        #     if self.ERR:
        #         print '\n\n\n\n\n\n\nerror!!!'
        #         print "(toa0 == toa1) and (toa0 == toa2)!!"
        #         print '\n\n\n\n\n\n\n'
        #     return -1

        # elif ( (toa0 == toa1) and not (toa0 == toa2) ):
        #     (x_h1,y_h1) = self.hyperbola.hyperbola(loc2,loc1,toa2,toa1)
        #     (x_h2,y_h2) = self.hyperbola.hyperbola(loc0,loc2,toa0,toa2)
        # elif ( not (toa0 == toa1) and  (toa0 == toa2) ):
        #     (x_h1,y_h1) = self.hyperbola.hyperbola(loc0,loc1,toa0,toa1)
        #     (x_h2,y_h2) = self.hyperbola.hyperbola(loc1,loc2,toa1,toa2)
        # else:
        #     (x_h1,y_h1) = self.hyperbola.hyperbola(loc0,loc1,toa0,toa1)
        #     (x_h2,y_h2) = self.hyperbola.hyperbola(loc0,loc2,toa0,toa2)
            

        # if ( np.isnan(x_h1[0]) or np.isnan(y_h1[0]) ):
        #     if self.ERR:
        #         print '\n\n\n\n\n\n\n\n\n\n\n\n\nerror!!!'
        #         print "np.isnan(x_h1[0]) or np.isnan(y_h1[0])!!"
        #         print '\n\n\n\n\n\n\n\n\n\n\n\n\n'        
        #     return -1

        # if ( np.isnan(x_h2[0]) or np.isnan(y_h2[0]) ):
        #     if self.ERR:
        #         print '\n\n\n\n\n\n\n\n\n\n\n\n\nerror!!!'
        #         print "np.isnan(x_h2[0]) or np.isnan(y_h2[0])!!"
        #         print '\n\n\n\n\n\n\n\n\n\n\n\n\n'
        #     return -1
        
        # (x_coords,y_coords) = self.hyperbola.intersections(x_h1,y_h1,x_h2,y_h2)
        


# x1 = p1(1);
# y1 = p1(2);

# x2 = p2(1);
# y2 = p2(2);

# x2 = p2(1);
# y2 = p2(2);



#  self.loc[0]
#  self.loc[1]
#  self.loc[2]
  	  
#  self.toa[0]
#  self.toa[1]
#  self.toa[2]

