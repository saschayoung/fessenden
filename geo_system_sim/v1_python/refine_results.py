#!/usr/bin/env python

import os, time
import numpy as np
# import matplotlib.cm as cm
# import matplotlib.pyplot as plt
# import sdr_kml_writer


DEBUG = True
PLOT = False


def geo_hist(x_results,y_results,num):
    host = os.uname()[1]
    d = time.localtime()
    date = '%s-%s-%s' %(str(d[0]),str(d[1]),str(d[2]))
    p = '/home/aryoung/batch_results/%s_%s' %(host, date)
    if not os.path.exists(p):
        os.makedirs(p)
    
                              
    print 'geo_hist file number: ', num

    # First pass
    try:
        H, xedges, yedges = np.histogram2d(x_results, y_results)
        extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

        idx = np.unravel_index(np.argmax(H),H.shape)
        x_lower = xedges[idx[0]]
        x_upper = xedges[idx[0]+1]
        y_lower = yedges[idx[1]]
        y_upper = yedges[idx[1]+1]

        if DEBUG:
            print "First Pass"
            print 'H: '
            print H
            print 'idx: ', idx
            print 'x_lower: ', x_lower
            print 'x_upper: ', x_upper
            print 'y_lower: ', y_lower
            print 'y_upper: ', y_upper

        x_refined = []
        y_refined = []

        i = 0
        while ( i < len(x_results) ):
            test = ( ((x_results[i] >= x_lower)  and
                      (x_results[i] <  x_upper)) and
                     ((y_results[i] >= y_lower)  and
                      (y_results[i] <  y_upper)) )
            if test:
                x_refined.append(x_results[i])
                y_refined.append(y_results[i])
            i +=1

    except:
        print 'First pass failed'
        print 'probably not enough data'
        return -1


    # Second pass
    try:
        H_p, xedges_p, yedges_p = np.histogram2d(x_refined, y_refined)
        extent_p = [xedges_p[0], xedges_p[-1], yedges_p[0], yedges_p[-1]]

        idx_p = np.unravel_index(np.argmax(H_p),H_p.shape)
        x_lower_p = xedges_p[idx_p[0]]
        x_upper_p = xedges_p[idx_p[0]+1]
        y_lower_p = yedges_p[idx_p[1]]
        y_upper_p = yedges_p[idx_p[1]+1]

        if DEBUG:
            print 'Second Pass'
            print 'H_p: '
            print H_p
            print "idx_p: ", idx_p
            print "x_lower_p: ", x_lower_p
            print "x_upper_p: ", x_upper_p
            print "y_lower_p: ", y_lower_p
            print "y_upper_p: ", y_upper_p

        x_drefined = []
        y_drefined = []

        i = 0
        while ( i < len(x_refined) ):
            test = ( ((x_refined[i] >= x_lower_p)  and
                      (x_refined[i] <  x_upper_p)) and
                     ((y_refined[i] >= y_lower_p)  and
                      (y_refined[i] <  y_upper_p)) )
            if test:
                x_drefined.append(x_refined[i])
                y_drefined.append(y_refined[i])
            i +=1

    except:
        print 'Second pass failed'
        print 'probably not enough data'
        results = [x_lower,x_upper,y_lower,y_upper]
        # write_kml(results,num,'first_pass')
        write_file(results,num,p,'first_pass')
        return -2


    # Third pass
    try:
        H_pp, xedges_pp, yedges_pp = np.histogram2d(x_drefined, y_drefined)
        extent_pp = [xedges_pp[0], xedges_pp[-1], yedges_pp[0], yedges_pp[-1]]

        idx_pp = np.unravel_index(np.argmax(H_pp),H_pp.shape)
        x_lower_pp = xedges_pp[idx_pp[0]]
        x_upper_pp = xedges_pp[idx_pp[0]+1]
        y_lower_pp = yedges_pp[idx_pp[1]]
        y_upper_pp = yedges_pp[idx_pp[1]+1]

        if DEBUG:
            print 'Third Pass'
            print 'H_pp: '
            print H_pp
            print "idx_pp: ", idx_pp
            print "x_lower_pp: ", x_lower_pp
            print "x_upper_pp: ", x_upper_pp
            print "y_lower_pp: ", y_lower_pp
            print "y_upper_pp: ", y_upper_pp

    except:
        print 'Third pass failed'
        print 'probably not enough data'
        results = [x_lower_p,x_upper_p,y_lower_p,y_upper_p]
        # write_kml(results,num,'second_pass')
        write_file(results,num,p,'second_pass')
        return -3

    else:
        results = [x_lower_pp,x_upper_pp,y_lower_pp,y_upper_pp]
        # write_kml(results,num,'third_pass')
        write_file(results,num,p,'third_pass')
        return 0
        
def write_file(results,num,p,s):
    t = str(time.localtime()[3])+'-'+str(time.localtime()[4])+'-'+str(time.localtime()[5])
    p_x = (0.5)*(results[0] + results[1])
    p_y = (0.5)*(results[2] + results[3])
    filename = 'answer' + '_' + str(num)+ '_' + s
    f = open('%s/%s' %(p, filename),'w+')
    f.write('%s\n%s' %(p_x,p_y))
    f.close
            
             


    if DEBUG:
        print p_x,p_y
    f = open 

def write_kml(results,num,s):
    p_x = (0.5)*(results[0] + results[1])
    p_y = (0.5)*(results[2] + results[3])
    if DEBUG:
        print p_x,p_y
    kml_write = sdr_kml_writer.kml_writer()
    coord = str(results[0])+','+str(results[2])
    kml_write.add_placemark('','',coord)
    coord = str(results[1])+','+str(results[3])
    kml_write.add_placemark('','',coord)
    coord = str(p_x)+','+str(p_y)
    kml_write.add_placemark('','',coord)
    filename = 'answer' + '_' + str(num)+ '_' + s + '.kml'
    kml_write.write_to_file(filename)


if __name__=='__main__':
    results = geo_hist()
    print results

    p_x = (0.5)*(results[0] + results[1])
    p_y = (0.5)*(results[2] + results[3])
    print p_x,p_y

    kml_write = sdr_kml_writer.kml_writer()

    coord = str(results[0])+','+str(results[2])
    kml_write.add_placemark('','',coord)
    coord = str(results[1])+','+str(results[3])
    kml_write.add_placemark('','',coord)
    coord = str(p_x)+','+str(p_y)
    kml_write.add_placemark('','',coord)
    
    kml_write.write_to_file('guess.kml')

    # # f = open('/home/aryoung/prog/geolocation/geo_system_sim/x_results','r')
    # f = open('x_results','r')
    # a = f.readlines()
    # f.close()
    # a = [float(x.strip('\n')) for x in a]

    # # f = open('/home/aryoung/prog/geolocation/geo_system_sim/x_results','r')
    # f = open('y_results','r')
    # b = f.readlines()
    # f.close()
    # b = [float(x.strip('\n')) for x in b]

    # x_results = []
    # y_results = []

    # i = 0
    # while ( i < len(a) ):
    #     x_results.append(a[i])
    #     y_results.append(b[i])
    #     i +=1
    

        # print 'xedges'
        # print xedges
        # print 'yedges'
        # print yedges
        # print 'np.argmax(H): ',np.argmax(H)
        # print np.unravel_index(np.argmax(H),H.shape)
        # print 'len(xedges): ',len(xedges)
        # print 'len(yedges): ',len(yedges)
        # print ''
        # if PLOT:
        #     plt.figure()
        #     plt.imshow(H, extent=extent_pp)
        #     plt.show()
