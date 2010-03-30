#!/usr/bin/env python

# standard libraries
import time,sys

# external libraries
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt

# local imports
import tdoa_stats
from geo_utils import geo_utils 
from fast_db_access import fast_db_access
from hyperbola_writer import hyperbola_writer


# import sdr_kml_writer






DEBUG = False
PLOT = False


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

def db_sim():
    
    '''
    simulates db access to determine WTF: re NaN
    '''
    
    import test_coords
    import location_alexandria
    
    g_utils = geo_utils()
    
    tx = test_coords.get_tx_coords()
    rx1 = location_alexandria.get_random_coord()
    rx2 = location_alexandria.get_random_coord()
    rx3 = location_alexandria.get_random_coord()
    
    t1 = g_utils.time_of_flight(tx,rx1)
    t2 = g_utils.time_of_flight(tx,rx2)
    t3 = g_utils.time_of_flight(tx,rx3)
    
    return [[rx1,t1],[rx2,t2],[rx3,t3]]


class rx_data:
    def __init__(self):
        self.db = fast_db_access()
        self.db_sim_counter = 1

    def get(self):

        data = self.db.run()
        if ( data == -1):
            return -1

        # data = db_sim()
        # self.db_sim_counter += 1
        # if ( self.db_sim_counter == 1000 ):
        #     return -1
        else:
            loc = []
            time = []
            for i in data:
                [l, t] = i
                loc.append(l)
                time.append(t)
            #endfor

            if DEBUG:
                print 'loc: ', loc
                print 'type(loc[0]): ', type(loc[0])
                print 'time: ', time
                print 'type(time[0]): ', type(time[0])
            #fi
            return (loc,time)



class tdoa:
    def __init__(self):
        self.geo_utils = geo_utils()


    def hyperbola(self,rx1,rx2,rx3,toa1,toa2,toa3):

        (x_h1,y_h1) = self.geo_utils.hyperbola(rx1,rx2,toa1,toa2)
        (x_h2,y_h2) = self.geo_utils.hyperbola(rx1,rx3,toa1,toa3)

        return [x_h1,y_h1,x_h2,y_h2]



def update(iteration):
    sys.stdout.write("Working... iteration: %3d\r" % iteration)
    sys.stdout.flush()
    


if __name__=='__main__':
    t0 = time.time()

    # instantiate classes
    h = hyperbola_writer()
    tdoa = tdoa()
    db = rx_data()

    # initalize data arrays
    x_results = np.array([])
    y_results = np.array([])


    i = 0
    while True:
        data = db.get()
        if ( data == -1):
            sys.stdout.write('\nDone\n')
            break
        else:
            (loc,t) = data

            rx1 = loc[0]
            rx2 = loc[1]
            rx3 = loc[2]

            toa1 = t[0]
            toa2 = t[1]
            toa3 = t[2]

            ans = tdoa.hyperbola(rx1,rx2,rx3,toa1,toa2,toa3)
            h.write_hyperbola(ans)
            if (np.isnan(ans).any()):
                print 'answer contains NaN'
                print loc,t
                PLOT = False
                break

            x_results = np.concatenate([x_results,ans[0]])
            x_results = np.concatenate([x_results,ans[2]])
            y_results = np.concatenate([y_results,ans[1]])
            y_results = np.concatenate([y_results,ans[3]])
            if ( (i % 25) == 0):
                tdoa_stats.three_pass(x_results,y_results)
            #fi
            update(i)
            i += 1

        #fi
    #endwhile

    t1 = time.time()
    t_tot = t1 - t0
    print '\n\ntotal time = %.6f seconds' %t_tot
    print 'total iterations: ', i



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
        plt.show()











    # ans = main.tdoa_sim(tx,rx1,rx2,rx3,toa1,toa2,toa)
    # x_results = np.concatenate([x_results,ans[0]])
    # x_results = np.concatenate([x_results,ans[2]])
    # y_results = np.concatenate([y_results,ans[1]])
    # y_results = np.concatenate([y_results,ans[3]])

    # ans = main.tdoa_sim(tx,rx2,rx3,rx4)
    # x_results = np.concatenate([x_results,ans[0]])
    # x_results = np.concatenate([x_results,ans[2]])
    # y_results = np.concatenate([y_results,ans[1]])
    # y_results = np.concatenate([y_results,ans[3]])


    
    # ans = tdoa.hyperbola()
    # x_results = np.concatenate([x_results,ans[0]])
    # x_results = np.concatenate([x_results,ans[2]])
    # y_results = np.concatenate([y_results,ans[1]])
    # y_results = np.concatenate([y_results,ans[3]])

    # ans = tdoa.hyperbola()
    # x_results = np.concatenate([x_results,ans[0]])
    # x_results = np.concatenate([x_results,ans[2]])
    # y_results = np.concatenate([y_results,ans[1]])
    # y_results = np.concatenate([y_results,ans[3]])



# class geolocate:

#     def __init__(self):
#         self.geo_utils = geo_utils()
#         # self.PLOT = True

#     def tdoa_sim(self,tx,rx1,rx2,rx3):
#         '''
#         geolocation function using time difference of arrival and
#         hyperbolic curves
#         '''

#         # x_tx = tx[0]
#         # y_tx = tx[1]
#         # x_rx1 = rx1[0]
#         # y_rx1 = rx1[1]

#         # x_rx2 = rx2[0]
#         # y_rx2 = rx2[1]
#         # x_rx3 = rx3[0]
#         # y_rx3 = rx3[1]

#         # tof_1 = self.geo_utils.time_of_flight(tx,rx1)
#         # tof_2 = self.geo_utils.time_of_flight(tx,rx2)
#         # tof_3 = self.geo_utils.time_of_flight(tx,rx3)
        
#         if DEBUG:
#             print 'rx1: ', rx1
#             print 'type(rx1): ', type(rx1)
#         (x_h1,y_h1) = self.geo_utils.hyperbola(rx1,rx2,tof_1,tof_2)
#         if DEBUG:
#             print 'x_h1: ', x_h1
#         (x_h2,y_h2) = self.geo_utils.hyperbola(rx1,rx3,tof_1,tof_3)

#         return [x_h1,y_h1,x_h2,y_h2]



# if __name__ == '__main__':
    

#     main = geolocate()


#     


#     # coordinates
#     
#     rx1 = test_coords.get_boathouse_coords()
#     rx2 = test_coords.get_uspto_coords()
#     rx3 = test_coords.get_tcwhs_coords()
#     rx4 = test_coords.get_lee_st_coords()

#     # write hyperbolas to kml file
#     # ans = main.tdoa_sim(tx,rx1,rx2,rx3)
#     # hyp_kml_writer.write_hyperbola(ans,'hyp1.kml')

#     # ans = main.tdoa_sim(tx,rx1,rx3,rx4)
#     # hyp_kml_writer.write_hyperbola(ans,'hyp2.kml')

#     # ans = main.tdoa_sim(tx,rx2,rx3,rx4)
#     

#     ans = main.tdoa_sim(tx,rx1,rx2,rx3)
#     x_results = np.concatenate([x_results,ans[0]])
#     x_results = np.concatenate([x_results,ans[2]])
#     y_results = np.concatenate([y_results,ans[1]])
#     y_results = np.concatenate([y_results,ans[3]])

#     ans = main.tdoa_sim(tx,rx1,rx2,rx3)
#     x_results = np.concatenate([x_results,ans[0]])
#     x_results = np.concatenate([x_results,ans[2]])
#     y_results = np.concatenate([y_results,ans[1]])
#     y_results = np.concatenate([y_results,ans[3]])

#     ans = main.tdoa_sim(tx,rx2,rx3,rx4)
#     x_results = np.concatenate([x_results,ans[0]])
#     x_results = np.concatenate([x_results,ans[2]])
#     y_results = np.concatenate([y_results,ans[1]])
#     y_results = np.concatenate([y_results,ans[3]])



#     # i = 0
#     # iterations = 2000
#     # while i < iterations:
#     #     rx1 = location_alexandria.get_random_coord()
#     #     rx2 = location_alexandria.get_random_coord()
#     #     rx3 = location_alexandria.get_random_coord()
#     #     ans = main.tdoa_sim(tx,rx1,rx2,rx3)

#     #     x_results = np.concatenate([x_results,ans[0]])
#     #     x_results = np.concatenate([x_results,ans[2]])
#     #     y_results = np.concatenate([y_results,ans[1]])
#     #     y_results = np.concatenate([y_results,ans[3]])
#     #     if ( (i % 25) == 0):
#     #         tdoa_stats.three_pass(x_results,y_results)
#     #     i+=1



#     if PLOT:
#         xmin = list_min(x_results)
#         xmax = list_max(x_results)
#         ymin = list_min(y_results)
#         ymax = list_max(y_results)
#         fig = plt.figure()
#         plt.hexbin(x_results,y_results, cmap=cm.jet)
#         plt.axis([xmin, xmax, ymin, ymax])
#         plt.title("Likely Transmitter Location")#\n%d Iterations, Total time to run: %f seconds" %(iterations,t_tot))
#         cb = plt.colorbar()
#         cb.set_label('counts')
#         fig.patch.set_alpha(0.1)
#         # plt.savefig('density_plot_%d_iters.png' %iterations)


#     # f = open('x_results_%d_iters' %(iterations),'w+')
#     # for num in x_results:
#     #     f.write(str(num)+'\n')
#     # f.close()

#     # f = open('y_results_%d_iters' %(iterations),'w+')
#     # for num in y_results:
#     #     f.write(str(num)+'\n')
#     # f.close()

#     if PLOT:
#         plt.show()

