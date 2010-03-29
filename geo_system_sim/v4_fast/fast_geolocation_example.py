#!/usr/bin/env python

#geoloc_main.py
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import sdr_kml_writer
from geo_utils import geo_utils 
import test_coords
import alex_random
from hyperbola_writer import hyperbola_writer
import tdoa_stats
import time

PLOT = True
DEBUG = True


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


class geolocate:

    def __init__(self):
        self.geo_utils = geo_utils()
        # self.PLOT = True

    def tdoa_sim(self,tx,rx1,rx2,rx3):
        '''
        geolocation function using time difference of arrival and
        hyperbolic curves
        '''

        # x_tx = tx[0]
        # y_tx = tx[1]
        # x_rx1 = rx1[0]
        # y_rx1 = rx1[1]

        # x_rx2 = rx2[0]
        # y_rx2 = rx2[1]
        # x_rx3 = rx3[0]
        # y_rx3 = rx3[1]

        tof_1 = self.geo_utils.time_of_flight(tx,rx1)
        tof_2 = self.geo_utils.time_of_flight(tx,rx2)
        tof_3 = self.geo_utils.time_of_flight(tx,rx3)
        
        if DEBUG:
            print 'rx1: ', rx1
            print 'type(rx1): ', type(rx1)
        (x_h1,y_h1) = self.geo_utils.hyperbola(rx1,rx2,tof_1,tof_2)
        if DEBUG:
            print 'x_h1: ', x_h1
        (x_h2,y_h2) = self.geo_utils.hyperbola(rx1,rx3,tof_1,tof_3)

        return [x_h1,y_h1,x_h2,y_h2]



if __name__ == '__main__':
    

    main = geolocate()

    t0 = time.time()
    h = hyperbola_writer()

    x_results = np.array([])
    y_results = np.array([])

    # coordinates
    tx = test_coords.get_tx_coords()
    rx1 = test_coords.get_boathouse_coords()
    rx2 = test_coords.get_uspto_coords()
    rx3 = test_coords.get_tcwhs_coords()
    rx4 = test_coords.get_lee_st_coords()

    # write hyperbolas to kml file
    # ans = main.tdoa_sim(tx,rx1,rx2,rx3)
    # hyp_kml_writer.write_hyperbola(ans,'hyp1.kml')

    # ans = main.tdoa_sim(tx,rx1,rx3,rx4)
    # hyp_kml_writer.write_hyperbola(ans,'hyp2.kml')

    # ans = main.tdoa_sim(tx,rx2,rx3,rx4)
    # hyp_kml_writer.write_hyperbola(ans,'hyp3.kml')

    ans = main.tdoa_sim(tx,rx1,rx2,rx3)
    x_results = np.concatenate([x_results,ans[0]])
    x_results = np.concatenate([x_results,ans[2]])
    y_results = np.concatenate([y_results,ans[1]])
    y_results = np.concatenate([y_results,ans[3]])

    ans = main.tdoa_sim(tx,rx1,rx2,rx3)
    x_results = np.concatenate([x_results,ans[0]])
    x_results = np.concatenate([x_results,ans[2]])
    y_results = np.concatenate([y_results,ans[1]])
    y_results = np.concatenate([y_results,ans[3]])

    ans = main.tdoa_sim(tx,rx2,rx3,rx4)
    x_results = np.concatenate([x_results,ans[0]])
    x_results = np.concatenate([x_results,ans[2]])
    y_results = np.concatenate([y_results,ans[1]])
    y_results = np.concatenate([y_results,ans[3]])



    # i = 0
    # iterations = 1000
    # while i < iterations:
    #     rx1 = alex_random.get_random_coord()
    #     rx2 = alex_random.get_random_coord()
    #     rx3 = alex_random.get_random_coord()
    #     ans = main.tdoa_sim(tx,rx1,rx2,rx3)
    #     h.write_hyperbola(ans)

    #     x_results = np.concatenate([x_results,ans[0]])
    #     x_results = np.concatenate([x_results,ans[2]])
    #     y_results = np.concatenate([y_results,ans[1]])
    #     y_results = np.concatenate([y_results,ans[3]])
    #     if ( (i % 25) == 0):
    #         tdoa_stats.three_pass(x_results,y_results)
    #     i+=1


    t1 = time.time()
    t_tot = t1 - t0
    print 'total time = %.6f seconds' %t_tot

    if PLOT:
        xmin = list_min(x_results)
        xmax = list_max(x_results)
        ymin = list_min(y_results)
        ymax = list_max(y_results)
        fig = plt.figure()
        plt.hexbin(x_results,y_results, cmap=cm.jet)
        plt.axis([xmin, xmax, ymin, ymax])
        plt.title("Likely Transmitter Location")#\n%d Iterations, Total time to run: %f seconds" %(iterations,t_tot))
        cb = plt.colorbar()
        cb.set_label('counts')
        fig.patch.set_alpha(0.1)
        # plt.savefig('density_plot_%d_iters.png' %iterations)


    # f = open('x_results_%d_iters' %(iterations),'w+')
    # for num in x_results:
    #     f.write(str(num)+'\n')
    # f.close()

    # f = open('y_results_%d_iters' %(iterations),'w+')
    # for num in y_results:
    #     f.write(str(num)+'\n')
    # f.close()

    if PLOT:
        plt.show()


        #     print "First Pass"
        #     print 'H: '
        #     print H
        #     print 'idx: ', idx
        #     print 'x_lower: ', x_lower
        #     print 'x_upper: ', x_upper
        #     print 'y_lower: ', y_lower
        #     print 'y_upper: ', y_upper

        #     x_refined = []
        #     y_refined = []

        #     i = 0
        #     while ( i < len(x_results) ):
        #         test = ( ((x_results[i] >= x_lower)  and
        #                   (x_results[i] <  x_upper)) and
        #                  ((y_results[i] >= y_lower)  and
        #                   (y_results[i] <  y_upper)) )
        #         if test:
        #             x_refined.append(x_results[i])
        #             y_refined.append(y_results[i])
        #         i +=1

        #     H_p, xedges_p, yedges_p = np.histogram2d(x_refined, y_refined)
        #     extent_p = [xedges_p[0], xedges_p[-1], yedges_p[0], yedges_p[-1]]

        #     idx_p = np.unravel_index(np.argmax(H_p),H_p.shape)
        #     x_lower_p = xedges_p[idx_p[0]]
        #     x_upper_p = xedges_p[idx_p[0]+1]
        #     y_lower_p = yedges_p[idx_p[1]]
        #     y_upper_p = yedges_p[idx_p[1]+1]

        #     i = 0
        #     while ( i < len(x_refined) ):
        #         test = ( ((x_refined[i] >= x_lower_p)  and
        #                   (x_refined[i] <  x_upper_p)) and
        #                  ((y_refined[i] >= y_lower_p)  and
        #                   (y_refined[i] <  y_upper_p)) )
        #         if test:
        #             x_drefined.append(x_refined[i])
        #             y_drefined.append(y_refined[i])
        #         i +=1

        #     results = [x_lower,x_upper,y_lower,y_upper]


        #     p_x = (0.5)*(results[0] + results[1])
        #     p_y = (0.5)*(results[2] + results[3])
        #     kml_write = sdr_kml_writer.kml_writer()
        #     coord = str(p_x)+','+str(p_y)
        #     kml_write.add_placemark('','',coord)
        #     filename = 'guess.kml'
        #     kml_write.write_to_file(filename)


        # if ( (i % 10) == 0 ):
        #     H, xedges, yedges = np.histogram2d(x_results, y_results)
        #     extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

        #     idx = np.unravel_index(np.argmax(H),H.shape)
        #     x_lower = xedges[idx[0]]
        #     x_upper = xedges[idx[0]+1]
        #     y_lower = yedges[idx[1]]
        #     y_upper = yedges[idx[1]+1]
