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
import time

PLOT = True


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

        x_tx = tx[0]
        y_tx = tx[1]
        x_rx1 = rx1[0]
        y_rx1 = rx1[1]

        x_rx2 = rx2[0]
        y_rx2 = rx2[1]
        x_rx3 = rx3[0]
        y_rx3 = rx3[1]

        tof_1 = self.geo_utils.time_of_flight(tx,rx1)
        tof_2 = self.geo_utils.time_of_flight(tx,rx2)
        tof_3 = self.geo_utils.time_of_flight(tx,rx3)

        (x_h1,y_h1) = self.geo_utils.hyperbola(rx1,rx2,tof_1,tof_2)
        (x_h2,y_h2) = self.geo_utils.hyperbola(rx1,rx3,tof_1,tof_3)

        return [x_h1,y_h1,x_h2,y_h2]



if __name__ == '__main__':
    
    t0 = time.time()
    main = geolocate()
    
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
    ans = main.tdoa_sim(tx,rx1,rx2,rx3)
    h.write_hyperbola(ans)

    # ans = main.tdoa_sim(tx,rx1,rx3,rx4)
    # hyp_kml_writer.write_hyperbola(ans,'hyp2.kml')

    # ans = main.tdoa_sim(tx,rx2,rx3,rx4)
    # hyp_kml_writer.write_hyperbola(ans,'hyp3.kml')

    # ans = main.tdoa_sim(tx,rx1,rx2,rx3)
    # x_results = np.concatenate([x_results,ans[0]])
    # x_results = np.concatenate([x_results,ans[2]])
    # y_results = np.concatenate([y_results,ans[1]])
    # y_results = np.concatenate([y_results,ans[3]])

    # ans = main.tdoa_sim(tx,rx1,rx2,rx3)
    # x_results = np.concatenate([x_results,ans[0]])
    # x_results = np.concatenate([x_results,ans[2]])
    # y_results = np.concatenate([y_results,ans[1]])
    # y_results = np.concatenate([y_results,ans[3]])

    # ans = main.tdoa_sim(tx,rx2,rx3,rx4)
    # x_results = np.concatenate([x_results,ans[0]])
    # x_results = np.concatenate([x_results,ans[2]])
    # y_results = np.concatenate([y_results,ans[1]])
    # y_results = np.concatenate([y_results,ans[3]])



    # i = 0
    # iterations = 1000
    # while i < iterations:
    #     rx1 = alex_random.get_random_coord()
    #     rx2 = alex_random.get_random_coord()
    #     rx3 = alex_random.get_random_coord()
    #     ans = main.tdoa_sim(tx,rx1,rx2,rx3)
    #     x_results = np.concatenate([x_results,ans[0]])
    #     x_results = np.concatenate([x_results,ans[2]])
    #     y_results = np.concatenate([y_results,ans[1]])
    #     y_results = np.concatenate([y_results,ans[3]])
    #     i+=1


    # t1 = time.time()
    # t_tot = t1 - t0
    # print 'total time = %.6f seconds' %t_tot

    # if PLOT:
    #     xmin = list_min(x_results)
    #     xmax = list_max(x_results)
    #     ymin = list_min(y_results)
    #     ymax = list_max(y_results)
    #     fig = plt.figure()
    #     plt.hexbin(x_results,y_results, cmap=cm.jet)
    #     plt.axis([xmin, xmax, ymin, ymax])
    #     plt.title("Likely Transmitter Location\n%d Iterations, Total time to run: %f seconds" %(iterations,t_tot))
    #     cb = plt.colorbar()
    #     cb.set_label('counts')
    #     fig.patch.set_alpha(0.1)
    #     plt.savefig('density_plot_%d_iters.png' %iterations)


    # f = open('x_results_%d_iters' %(iterations),'w+')
    # for num in x_results:
    #     f.write(str(num)+'\n')
    # f.close()

    # f = open('y_results_%d_iters' %(iterations),'w+')
    # for num in y_results:
    #     f.write(str(num)+'\n')
    # f.close()

    # if PLOT:
    #     plt.show()




























    # f = open('x_results','r')
    # a = f.readlines()
    # f.close()
    # a = [float(x.strip('\n')) for x in a]

    # f = open('y_results','r')
    # b = f.readlines()
    # f.close()
    # b = [float(x.strip('\n')) for x in b]

    # i = 0
    # while ( i < len(a) ):
    #     x_results.append(a[i])
    #     y_results.append(b[i])
    #     i +=1


        # print 'type(x_h1): ',type(x_h1)
        # print 'shape(x_h1): ', np.shape(x_h1)
        # print 'x_h1:\n', x_h1

        # print 'type(x_h2): ',type(x_h2)
        # print 'shape(x_h2): ', np.shape(x_h2)
        # print 'x_h2:\n', x_h2

        # x = np.concatenate((x_h1,x_h2))
        # y = np.concatenate((y_h1,y_h2))
        # print 'type(x): ',type(x)
        # print 'shape(x): ', np.shape(x)
        # print 'x:\n', x
        
        # fig = plt.figure()
        # # plt.hexbin(x_results,y_results, cmap=cm.jet)
        # plt.hexbin(x,y, cmap=cm.jet)
        # plt.axis([xmin, xmax, ymin, ymax])
        # plt.title("Likely Transmitter Location")
        # cb = plt.colorbar()
        # cb.set_label('counts')
        # fig.patch.set_alpha(0.1)
        # # 
        # plt.show()
        # plt.figure()
        # plt.plot(x_h1,y_h1,'b',
        #          x_h2,y_h2,'g',
        #          )
        # plt.grid(True)
        # # plt.show()


        # (x_coords,y_coords) = self.geo_utils.intersections(x_h1,y_h1,x_h2,y_h2)
        # if ( (x_coords == -1) and (y_coords == -1) ):
        #     print "intersection.m returns no data, return -1 to main"
        #     return -1

        # print x_coords
        # print y_coords

        # if self.PLOT:
        #     x_tx = tx[0]
        #     y_tx = tx[1]
        #     x_rx1 = rx1[0]
        #     y_rx1 = rx1[1]
        #     x_rx2 = rx2[0]
        #     y_rx2 = rx2[1]
        #     x_rx3 = rx3[0]
        #     y_rx3 = rx3[1]

        #     # plt.figure()
        #     plt.plot(x_tx,y_tx,'r^',x_rx1,y_rx1,'g^',
        #              x_rx2,y_rx2,'g^',x_rx3,y_rx3,'g^',
        #              x_h1,y_h1,'b',
        #              x_h2,y_h2,'g',
        #              x_coords,y_coords,'*',
        #              )
        #     plt.grid(True)
        #     plt.hold(True)
        # #     plt.show()


    # if PLOT:
    #     plt.figure()
    #     plt.plot(x_results,y_results,'.')
    #     plt.grid(True)



    #     # plt.savefig('density_plot.png',transparent=True)


    # # first pass histogram
    # H, xedges, yedges = np.histogram2d(x_results, y_results)
    # extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    # if PLOT:
    #     plt.figure()
    #     plt.imshow(H, extent=extent)
    #     plt.title('2-D Histogram: First Pass')

    # idx = np.unravel_index(np.argmax(H),H.shape)
    # x_lower = xedges[idx[0]]
    # x_upper = xedges[idx[0]+1]
    # y_lower = yedges[idx[1]]
    # y_upper = yedges[idx[1]+1]

    # print 'H: '
    # print H
    # print "idx: ", idx
    # print "x_lower: ", x_lower
    # print "x_upper: ", x_upper
    # print "y_lower: ", y_lower
    # print "y_upper: ", y_upper


    # x_refined = []
    # y_refined = []

    # i = 0
    # while ( i < len(x_results) ):
    #     test = ( ((x_results[i] >= x_lower)  and
    #               (x_results[i] <  x_upper)) and
    #              ((y_results[i] >= y_lower)  and
    #               (y_results[i] <  y_upper)) )
    #     if test:
    #         x_refined.append(x_results[i])
    #         y_refined.append(y_results[i])
    #     i +=1

    # # second pass histogram
    # H_p, xedges_p, yedges_p = np.histogram2d(x_refined, y_refined)
    # extent_p = [xedges_p[0], xedges_p[-1], yedges_p[0], yedges_p[-1]]
    # if PLOT:
    #     plt.figure()
    #     plt.title('2-D Histogram: Second Pass')
    #     plt.imshow(H, extent=extent_p)

    # print 'H_p: '
    # print H_p

    # idx_p = np.unravel_index(np.argmax(H_p),H_p.shape)
    # x_lower_p = xedges_p[idx_p[0]]
    # x_upper_p = xedges_p[idx_p[0]+1]
    # y_lower_p = yedges_p[idx_p[1]]
    # y_upper_p = yedges_p[idx_p[1]+1]

    # print "idx_p: ", idx_p
    # print "x_lower_p: ", x_lower_p
    # print "x_upper_p: ", x_upper_p
    # print "y_lower_p: ", y_lower_p
    # print "y_upper_p: ", y_upper_p

    # x_drefined = []
    # y_drefined = []

    # i = 0
    # while ( i < len(x_refined) ):
    #     test = ( ((x_refined[i] >= x_lower_p)  and
    #               (x_refined[i] <  x_upper_p)) and
    #              ((y_refined[i] >= y_lower_p)  and
    #               (y_refined[i] <  y_upper_p)) )
    #     if test:
    #         x_drefined.append(x_refined[i])
    #         y_drefined.append(y_refined[i])
    #     i +=1

    # H_pp, xedges_pp, yedges_pp = np.histogram2d(x_drefined, y_drefined)
    # extent_pp = [xedges_pp[0], xedges_pp[-1], yedges_pp[0], yedges_pp[-1]]
    # if PLOT:
    #     plt.figure()
    #     plt.imshow(H, extent=extent_pp)
    #     plt.title('2-D Histogram: Third Pass')

    # print 'H_pp: '
    # print H_pp
    
    # idx_pp = np.unravel_index(np.argmax(H_pp),H_pp.shape)
    # x_lower_pp = xedges_pp[idx_pp[0]]
    # x_upper_pp = xedges_pp[idx_pp[0]+1]
    # y_lower_pp = yedges_pp[idx_pp[1]]
    # y_upper_pp = yedges_pp[idx_pp[1]+1]

    # print "idx_pp: ", idx_pp
    # print "x_lower_pp: ", x_lower_pp
    # print "x_upper_pp: ", x_upper_pp
    # print "y_lower_pp: ", y_lower_pp
    # print "y_upper_pp: ", y_upper_pp
    
    # print 'tx coords: ', tx



    # f = open('x_results','w+')
    # for num in x_results:
    #     f.write(str(num)+'\n')
    # f.close()

    # f = open('y_results','w+')
    # for num in y_results:
    #     f.write(str(num)+'\n')
    # f.close()

    # # plt.show()


















    # intersection = main.tdoa_sim(tx,rx1,rx2,rx3)
    # plt.figure()
    # plt.plot(x_h1,y_h1,'b',
    #          x_h2,y_h2,'g',
    #          )
    # plt.grid(True)


    # intersection = main.tdoa_sim(tx,rx1,rx3,rx4)
    # x_results += intersection[0]
    # y_results += intersection[1]

    # intersection = main.tdoa_sim(tx,rx2,rx3,rx4)
    # x_results += intersection[0]
    # y_results += intersection[1]



    


    # print x_lower
    # print x_upper
    # print y_lower
    # print y_upper

    # print H[idx]
    # print 'H: '
    # print H
    # print 'xedges'
    # print xedges
    # print 'yedges'
    # print yedges
    # print 'np.argmax(H): ',np.argmax(H)
    # print np.unravel_index(np.argmax(H),H.shape)
    # print 'len(xedges): ',len(xedges)
    # print 'len(yedges): ',len(yedges)
    # print ''

#     f = open('x_results','w+')
#     for num in x_results:
#         f.write(str(num)+'\n')
#     f.close()

#     f = open('y_results','w+')
#     for num in y_results:
#         f.write(str(num)+'\n')
#     f.close()


#     print x_results
#     print y_results


# # # #     print xmin
# # # #     print xmax
# # # #     print ymin
# # # #     print ymax

#     fig = plt.figure()
#     plt.hexbin(x_results,y_results, cmap=cm.jet)
#     plt.axis([xmin, xmax, ymin, ymax])
#     plt.title("Likely Transmitter Location")
#     cb = plt.colorbar()
#     cb.set_label('counts')
#     fig.patch.set_alpha(0.1)
#     plt.savefig('density_plot.png',transparent=True)

# # #     kml_write = sdr_kml_writer.kml_writer()

# # #     for i in range(0,len(x_results)):
# # #         coord = str(x_results[i])+','+str(y_results[i])
# # #         kml_write.add_placemark('','',coord)
# # #     kml_write.write_to_file('geoloc_kml_file.kml')

#     plt.figure()
#     H, xedges, yedges = np.histogram2d(x_results, y_results)
#     print H.shape, xedges.shape, yedges.shape
#     extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
#     plt.imshow(H, extent=extent)


#     idx = np.unravel_index(np.argmax(H),H.shape)
#     x_lower = xedges[idx[0]]
#     x_upper = xedges[idx[0]+1]
#     y_lower = yedges[idx[1]]
#     y_upper = yedges[idx[1]+1]

#     print x_lower
#     print x_upper
#     print y_lower
#     print y_upper


#     print H[idx]
#     print 'H: '
#     print H
#     print 'xedges'
#     print xedges
#     print 'yedges'
#     print yedges
#     print 'np.argmax(H): ',np.argmax(H)
#     print np.unravel_index(np.argmax(H),H.shape)
#     print 'len(xedges): ',len(xedges)
#     print 'len(yedges): ',len(yedges)
    

#     print ''


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

#     plt.figure()
#     H_p, xedges_p, yedges_p = np.histogram2d(x_refined, y_refined)
#     extent_p = [xedges_p[0], xedges_p[-1], yedges_p[0], yedges_p[-1]]
#     plt.imshow(H, extent=extent_p)

#     idx_p = np.unravel_index(np.argmax(H_p),H_p.shape)
#     x_lower_p = xedges_p[idx_p[0]]
#     x_upper_p = xedges_p[idx_p[0]+1]
#     y_lower_p = yedges_p[idx_p[1]]
#     y_upper_p = yedges_p[idx_p[1]+1]


#     print 'H_p: '
#     print H_p
#     print "idx_p: ", idx_p
#     print "x_lower_p: ", x_lower_p
#     print "x_upper_p: ", x_upper_p
#     print "y_lower_p: ", y_lower_p
#     print "y_upper_p: ", y_upper_p

#     x_drefined = []
#     y_drefined = []

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

#     plt.figure()
#     H_pp, xedges_pp, yedges_pp = np.histogram2d(x_drefined, y_drefined)
#     extent_pp = [xedges_pp[0], xedges_pp[-1], yedges_pp[0], yedges_pp[-1]]
#     plt.imshow(H, extent=extent_pp)

#     print 'H_pp: '
#     print H_pp
    
#     idx_pp = np.unravel_index(np.argmax(H_pp),H_pp.shape)
#     x_lower_pp = xedges_pp[idx_pp[0]]
#     x_upper_pp = xedges_pp[idx_pp[0]+1]
#     y_lower_pp = yedges_pp[idx_pp[1]]
#     y_upper_pp = yedges_pp[idx_pp[1]+1]

#     print "idx_pp: ", idx_pp
#     print "x_lower_pp: ", x_lower_pp
#     print "x_upper_pp: ", x_upper_pp
#     print "y_lower_pp: ", y_lower_pp
#     print "y_upper_pp: ", y_upper_pp

    

# # #     plt.figure()
# # #     x_n, x_bins, x_patches = plt.hist(x_results,10,facecolor='blue',alpha=0.75)

# # #     x_n_max = np.argmax(x_n)
# # #     x_lower = x_bins[x_n_max]
# # #     x_upper = x_bins[x_n_max+1]

# # #     print ''
# # #     print 'length of x_n: ',len(x_n)
# # #     print 'x_n: '
# # #     print x_n
# # #     print np.argmax(x_n)
# # #     print 'length of x_bins: ', len(x_bins)
# # #     print 'x_bins: '
# # #     print x_bins
# # #     print 'x_lower: ', x_lower
# #     print 'x_upper: ', x_upper
    



# #     plt.figure()
# #     y_n, y_bins, y_patches = plt.hist(y_results,10,facecolor='blue',alpha=0.75)




# #     print y_n,
# #     print np.max(y_n)
# #     print y_bins

    


    # plt.show()



