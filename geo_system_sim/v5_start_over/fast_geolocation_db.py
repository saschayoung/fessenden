#!/usr/bin/env python

# standard libraries
import time,sys,random

# external libraries
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt

# local imports
import loc_utils
import hyperbola_writer 
from geo_utils import geo_utils 
from fast_db_access import fast_db_access
# from hyperbola_writer import *



DEBUG = True
PLOT = True

def update(iteration):
    sys.stdout.write("Working... iteration: %3d\r" % iteration)
    sys.stdout.flush()

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


class rx_data:
    def __init__(self,host):
        self.db = fast_db_access(host)
        self.db_sim_counter = 1
        self.db.start_db()


    def get(self):
        data = self.db.run()
        if ( data == -1):
            return -1

        loc = []
        time = []
        for i in data:
            [l, t] = i
            loc.append(l)
            time.append(t)

            # if DEBUG:
            # print 'loc: ', loc
            # print 'type(loc[0]): ', type(loc[0])
            # print 'time: ', time
            # print 'type(time[0]): ', type(time[0])
        return (loc,time)

    def stop(self):
        self.db_stop()


class tdoa:
    def __init__(self):
        self.geo_utils = geo_utils()

    def hyperbola(self,rx1,rx2,rx3,toa1,toa2,toa3):
        (x_h1,y_h1) = self.geo_utils.hyperbola(rx1,rx2,toa1,toa2)
        (x_h2,y_h2) = self.geo_utils.hyperbola(rx1,rx3,toa1,toa3)
        return [x_h1,y_h1,x_h2,y_h2]

class tdoa_degen:
    def __init__(self):
        self.geo_utils = geo_utils()

    def hyperbola(self,rx1,rx2,toa1,toa2):
        # if DEBUG:
        #     print "\nDegenerate state, only 1 hyperbola possible\n"
        #     # raw_input()
        (x_h1,y_h1) = self.geo_utils.hyperbola(rx1,rx2,toa1,toa2)
        # print 'len(x_h1)', len(x_h1)
        # print 'len(y_h1)', len(y_h1)
        return [x_h1,y_h1]




class main:


    def __init__(self,options):
        self.options = options

    def sleep(self):
        t = random.random()
        time.sleep(t)

    
    def run(self):
        t0 = time.time()

        # instantiate classes
        h1 = hyperbola_writer.h1()
        h2 = hyperbola_writer.h2()
        f_tdoa = tdoa()
        f_tdoa_degen = tdoa_degen()
        db = rx_data(self.options.host)

        # initalize data arrays
        x_results = np.array([])
        y_results = np.array([])
        guess = np.array([])

        d = 0
        iterations = 0
        n_sleep = 0
        j = 0

        print "self.options.cluster: ", self.options.cluster

        ########################################################################
        while True:
            
            data = db.get()
            ####################################################################
            if ( data == -1):
                self.sleep()
                n_sleep += 1
                # if ( n_sleep >= 1000 ):
                #     sys.stdout.write('\nDone\n')
                #     break
                continue
            else:
                n_sleep=0
            ####################################################################

            (loc,t) = data

            if ( len(loc) >= 3 ):       # regular case: 2 hyperbolas
                for k in range(len(loc)-2):
                    rx1 = loc[k]
                    rx2 = loc[k+1]
                    rx3 = loc[k+2]

                    toa1 = t[k]
                    toa2 = t[k+1]
                    toa3 = t[k+2]

                    ans = f_tdoa.hyperbola(rx1,rx2,rx3,toa1,toa2,toa3)

                    # if not self.options.cluster:
                    # print 'writing hyperbolas'
                    h2.write_hyperbola(ans)

                    x_results = np.concatenate([x_results,ans[0]])
                    y_results = np.concatenate([y_results,ans[1]])
                    x_results = np.concatenate([x_results,ans[2]])
                    y_results = np.concatenate([y_results,ans[3]])

                    update(iterations)
                    iterations += 1

            elif ( len(loc) == 2 ):     # degenerate case: not enough data
                rx1 = loc[0]            # for intersection, but we still 
                rx2 = loc[1]            # plot and store 1 hyperbola
                toa1 = t[0]
                toa2 = t[1]
                ans = f_tdoa_degen.hyperbola(rx1,rx2,toa1,toa2)
                # if not self.options.cluster:
                # print 'writing hyperbolas'
                h1.write_hyperbola(ans)
                x_results = np.concatenate([x_results,ans[0]])
                y_results = np.concatenate([y_results,ans[1]])
                d += 1
                update(iterations)
                iterations += 1
            else: # ( len(loc) == 1 )
                pass

            if ( (iterations % 25) == 0):
                loc_utils.iter_hist(self.options.host,x_results,y_results)
        ########################################################################

        db.stop()
        t1 = time.time()
        t_tot = t1 - t0
        print '\n\ntotal time = %.6f seconds' %t_tot
        print 'total iterations: ', iterations

        print 'degenerate cases: ', d






if __name__=='__main__':
    from optparse import OptionParser
    usage = "usage: %prog [options] arg"

    parser = OptionParser(usage=usage)
    parser.add_option("", "--host", type="string", default="128.173.90.88",
                      help="database host in dotted decimal form [default=%default]")
    parser.add_option("-f", "--file", type="string", default="guess",
                      help="filename for writing location guesses and image [default=%default]")
    parser.add_option("-c", "--cluster", action="store_true", default="False",
                      help="program is running on cluster [default=%default]")

    (options, args) = parser.parse_args()


    m = main(options)
    m.run()


    # t0 = time.time()

    # # instantiate classes
    # h1 = hyperbola_writer.h1()
    # h2 = hyperbola_writer.h2()

    # tdoa = tdoa()
    # tdoa_degen = tdoa_degen()
    # db = rx_data(options.host)

    # # initalize data arrays
    # x_results = np.array([])
    # y_results = np.array([])
    # guess = np.array([])

    # d = 0
    # iterations = 0

    # j = 0
    # while True:
    #     data = db.get()
    #     if ( data == -1):
    #         sys.stdout.write('\nDone\n')
    #         break

    #     (loc,t) = data

    #     if ( len(loc) >= 3 ):       # regular case: 2 hyperbolas
    #         for k in range(len(loc)-2):
    #             rx1 = loc[k]
    #             rx2 = loc[k+1]
    #             rx3 = loc[k+2]
    #             # print len(loc)
    #             # print loc
    #             # print k
    #             # print  range(len(loc)-2)

    #             # sys.exit(1)

    #             toa1 = t[k]
    #             toa2 = t[k+1]
    #             toa3 = t[k+2]

    #             ans = tdoa.hyperbola(rx1,rx2,rx3,toa1,toa2,toa3)

    #             # if (np.isnan(ans).any()):
    #             #     print 'answer contains NaN'
    #             #     print loc,t
    #             #     PLOT = False
    #             #     break
    #             if ( (iterations % 2) == 0):
    #                 h2.write_hyperbola(ans)
    #             x_results = np.concatenate([x_results,ans[0]])
    #             y_results = np.concatenate([y_results,ans[1]])
    #             x_results = np.concatenate([x_results,ans[2]])
    #             y_results = np.concatenate([y_results,ans[3]])
    #             update(iterations)
    #             iterations += 1
    #             # if not ( len(x_results) == len(y_results) ):
    #             #     print 'len(x_results) != len(y_results)', len(x_results),len(y_results)
    #             #     sys.exit(1)
        
    #     else:                       # degenerate case: not enough data
    #         rx1 = loc[0]            # for intersection, but we still 
    #         rx2 = loc[1]            # plot and store 1 hyperbola
    #         toa1 = t[0]
    #         toa2 = t[1]
    #         ans = tdoa_degen.hyperbola(rx1,rx2,toa1,toa2)
    #         if ( (iterations % 2) == 0):
    #             h1.write_hyperbola(ans)
    #         x_results = np.concatenate([x_results,ans[0]])
    #         y_results = np.concatenate([y_results,ans[1]])
    #         # if not ( len(x_results) == len(y_results) ):
    #         #     print 'degenerate case'
    #         #     print 'iteration: %d', i
    #         #     print 'len(x_results) != len(y_results)', len(x_results),len(y_results)
    #         #     sys.exit(1)
    #         d += 1
    #         update(iterations)
    #         iterations += 1
        
    #     if ( (iterations % 25) == 0):
    #         loc_utils.iter_hist(options.host,x_results,y_results)
    #         # guess = np.concatenate([guess,g])
            

    #     #fi
    # #endwhile

    # # f = open(options.file + '.dat', 'w+')
    # # for i in guess:
    # #     f.write(str(i) + '\n')
    # # f.close

    # t1 = time.time()
    # t_tot = t1 - t0
    # print '\n\ntotal time = %.6f seconds' %t_tot
    # print 'total iterations: ', iterations

    # print 'degenerate cases: ', d

    # # print 'x: ',len(x_results), np.shape(x_results)
    # # print 'y: ',len(y_results), np.shape(y_results)


    # if PLOT:
    #     xmin = list_min(x_results)
    #     xmax = list_max(x_results)
    #     ymin = list_min(y_results)
    #     ymax = list_max(y_results)
    #     fig = plt.figure()
    #     final = plt.hexbin(x_results,y_results, cmap=cm.jet)
    #     plt.axis([xmin, xmax, ymin, ymax])
    #     plt.title("Likely Transmitter Location\n%d Iterations, Total time to run: %f seconds" %(iterations,t_tot))
    #     cb = plt.colorbar()
    #     cb.set_label('counts')
    #     fig.patch.set_alpha(0.1)
    #     plt.savefig(options.file + '.png',transparent=True)
    #     plt.show()
