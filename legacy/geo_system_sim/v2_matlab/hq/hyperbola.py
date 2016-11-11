#!/usr/bin/env python


import sys,os


def hyperbola(self,p1,p2,p3,toa1,toa2,toa3):
    '''
    wrapper calls matlab using os bash call, reads data that matlab writes to file

    input:
           p1,p2           location in the form (lat,lon)
           toa1,toa2       timestamp in seconds

    return:
           [x,y]   x & y coordinates of intersections
    '''

    if ( (toa0 == toa1) and (toa0 == toa2) ):
        if self.ERR:
            print '\n\n\n\n\n\n\nerror!!!'
            print "(toa0 == toa1) and (toa0 == toa2)!!"
            print '\n\n\n\n\n\n\n'
        return -1

    elif ( (toa0 == toa1) and not (toa0 == toa2) ):
        (x_h1,y_h1) = self.hyperbola.hyperbola(loc2,loc1,toa2,toa1)
        (x_h2,y_h2) = self.hyperbola.hyperbola(loc0,loc2,toa0,toa2)
    elif ( not (toa0 == toa1) and  (toa0 == toa2) ):
        (x_h1,y_h1) = self.hyperbola.hyperbola(loc0,loc1,toa0,toa1)
        (x_h2,y_h2) = self.hyperbola.hyperbola(loc1,loc2,toa1,toa2)
    else:
        (x_h1,y_h1) = self.hyperbola.hyperbola(loc0,loc1,toa0,toa1)
        (x_h2,y_h2) = self.hyperbola.hyperbola(loc0,loc2,toa0,toa2)


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

    (x_coords,y_coords) = self.hyperbola.intersections(x_h1,y_h1,x_h2,y_h2)

    if ( (x_coords == -1) and (y_coords == -1) ):
        if self.ERR:
            print "intersection.m returns no data, return -1 to main"
        return -1



    string = 'cd matlab_files; matlab -nojvm -nodesktop -nosplash -nodisplay -r'
    string += '\"hyperbola(%.15f, %.15f, %.10f, %.10f)\"' %(p1,p2,toa1,toa2)
    os.system(string)

    f = open('intersect.txt','r')
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
