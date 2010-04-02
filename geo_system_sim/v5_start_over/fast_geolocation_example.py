#!/usr/bin/env python

# core libraries
import time,sys

# external libraries
import numpy as np
import matplotlib
# matplotlib.use('Agg')
import matplotlib.cm as cm
import matplotlib.pyplot as plt

# local imports
import fig2img
import sim_utils
import test_coords
import tdoa_stats
import hyperbola_writer
import sdr_kml_writer
import location_alexandria
from geo_utils import geo_utils 



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
        pass


    def tdoa_sim(self,tx,rx1,rx2,rx3):
        '''
        geolocation function using time difference of arrival and
        hyperbolic curves
        '''
        g = geo_utils()

        # x_tx = tx[0]
        # y_tx = tx[1]
        # x_rx1 = rx1[0]
        # y_rx1 = rx1[1]

        # x_rx2 = rx2[0]
        # y_rx2 = rx2[1]
        # x_rx3 = rx3[0]
        # y_rx3 = rx3[1]

        tof_1 = sim_utils.time_of_flight(tx,rx1)
        tof_2 = sim_utils.time_of_flight(tx,rx2)
        tof_3 = sim_utils.time_of_flight(tx,rx3)

        (x_h1,y_h1) = g.hyperbola(rx1,rx2,tof_1,tof_2)
        (x_h2,y_h2) = g.hyperbola(rx1,rx3,tof_1,tof_3)

        return [x_h1,y_h1,x_h2,y_h2]



if __name__ == '__main__':
    

    main = geolocate()

    t0 = time.time()
    # h = hyperbola_writer()

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
    #     if (np.isnan(ans).any()):
    #         print 'answer contains NaN'
    #         print loc,t
    #         PLOT = False
    #         break

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
        # print 'x_min: ', repr(xmin)
        # print 'y_min: ', repr(ymin)
        # print 'x_max: ', repr(xmax)
        # print 'y_max: ', repr(ymax)
        fig = plt.figure()
        plt.hexbin(x_results,y_results, cmap=cm.jet)
        plt.axis([xmin, xmax, ymin, ymax])
        # ax = fig.add_axes([0,0,1,1],frameon=False)
        plt.title("Likely Transmitter Location")#\n%d Iterations, Total time to run: %f seconds" %(iterations,t_tot))
        cb = plt.colorbar()
        cb.set_label('counts')
        fig.patch.set_alpha(0.01)
        # plt.draw()
        # # ax = plt.gca()
        # ax.set_axis_off()
        # ax.set_xticks([])
        # ax.set_yticks([])

        # ax.set_xbound([0,1])
        # ax.set_ybound([0,1])
        # im=fig2img.fig2img(fig)
        # # box = (100,60,720,540)  # matplotlib imgs
        # box = (80,48,577,433)
        # c_im = im.crop(box)
        # c_im.show()
        # im.save('pyplot_crop','png')
        plt.savefig('density_plot.png',transparent=False)
    # print 'continuing to run...'
    # raw_input()

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

