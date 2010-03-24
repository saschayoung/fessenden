#!/usr/bin/env python

import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import sdr_kml_writer
from geo_utils import geo_utils 
import test_coords
import alex_random

DEBUG = True
ENABLE_PLOTTING = False


def list_min(list):
    min = 9999
    for i in list:
        if i < min:
            min = i
    return min

def list_max(list):
    max = -9999
    for i in list:
        if i > max:
            max = i
    return max


def get_limits(x_list,y_list):
    xmin = list_min(x_list)
    xmax = list_max(x_list)
    ymin = list_min(y_list)
    ymax = list_max(y_list)
    return (xmin,xmax,ymin,ymax)

def resolve(x_results, y_results):

    (xmin,xmax,ymin,ymax) = get_limits(x_results, y_results)
    if DEBUG:    
        print 'xmin: ', xmin
        print 'xmax: ', xmax
        print 'ymin: ', ymin
        print 'ymax: ', ymax

    if ENABLE_PLOTTING:
        fig = plt.figure()
        plt.hexbin(x_results,y_results, cmap=cm.jet)
        plt.axis([xmin, xmax, ymin, ymax])
        plt.title("Likely Transmitter Location")
        cb = plt.colorbar()
        cb.set_label('counts')
        fig.patch.set_alpha(0.1)
        plt.savefig('density_plot.png',transparent=True)


    # 2D histogram
    H, xedges, yedges = np.histogram2d(x_results, y_results)
    idx = np.unravel_index(np.argmax(H),H.shape)
    x_lower = xedges[idx[0]]
    x_upper = xedges[idx[0]+1]
    y_lower = yedges[idx[1]]
    y_upper = yedges[idx[1]+1]


    print x_lower
    print x_upper
    print y_lower
    print y_upper


    print H[idx]
    print 'H: '
    print H
    print 'xedges'
    print xedges
    print 'yedges'
    print yedges
    print 'np.argmax(H): ',np.argmax(H)
    print np.unravel_index(np.argmax(H),H.shape)
    print 'len(xedges): ',len(xedges)
    print 'len(yedges): ',len(yedges)
    

    print ''


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

    plt.figure()
    H_p, xedges_p, yedges_p = np.histogram2d(x_refined, y_refined)
    extent_p = [xedges_p[0], xedges_p[-1], yedges_p[0], yedges_p[-1]]
    plt.imshow(H, extent=extent_p)

    idx_p = np.unravel_index(np.argmax(H_p),H_p.shape)
    x_lower_p = xedges_p[idx_p[0]]
    x_upper_p = xedges_p[idx_p[0]+1]
    y_lower_p = yedges_p[idx_p[1]]
    y_upper_p = yedges_p[idx_p[1]+1]


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

    plt.figure()
    H_pp, xedges_pp, yedges_pp = np.histogram2d(x_drefined, y_drefined)
    extent_pp = [xedges_pp[0], xedges_pp[-1], yedges_pp[0], yedges_pp[-1]]
    plt.imshow(H, extent=extent_pp)

    print 'H_pp: '
    print H_pp
    
    idx_pp = np.unravel_index(np.argmax(H_pp),H_pp.shape)
    x_lower_pp = xedges_pp[idx_pp[0]]
    x_upper_pp = xedges_pp[idx_pp[0]+1]
    y_lower_pp = yedges_pp[idx_pp[1]]
    y_upper_pp = yedges_pp[idx_pp[1]+1]

    print "idx_pp: ", idx_pp
    print "x_lower_pp: ", x_lower_pp
    print "x_upper_pp: ", x_upper_pp
    print "y_lower_pp: ", y_lower_pp
    print "y_upper_pp: ", y_upper_pp



# #     kml_write = sdr_kml_writer.kml_writer()

# #     for i in range(0,len(x_results)):
# #         coord = str(x_results[i])+','+str(y_results[i])
# #         kml_write.add_placemark('','',coord)
# #     kml_write.write_to_file('geoloc_kml_file.kml')

    # plt.figure()
    # H, xedges, yedges = np.histogram2d(x_results, y_results)
    # print H.shape, xedges.shape, yedges.shape
    # extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    # plt.imshow(H, extent=extent)
