#!/usr/bin/env python

import time, random, struct
import os, sys
import numpy as np
import psycopg2
#import matplotlib.pyplot as plt


import test_coords
import alex_random
import tdoa_stats
import check_accuracy
from geo_utils import geo_utils
from geolocation import geolocation
from hyperbola_writer import hyperbola_writer




class geo_module:

    def __init__(self):
        self.DEBUG = True

        self.hyp_iter = 1
        self.geo_utils = geo_utils()
        # self.geoloc = geolocation()
        self.method = 'tdoa'  # method {'tdoa'|'custom'}

        
        # self.tdoa_iterator = 1
        # self.t_sleep = 0.01

        self.user = 'sdrc_user'
        self.passwd = 'sdrc_pass'
        # self.kml_file_number = 1
        self.state = 1

        self.num_NaN = 0

        self.h = hyperbola_writer()



        self.empty_loop_iterations = 0
        self.max_empty_loop_iterations = 5
        
        #beacon packet number for extracting from db
        self.beacon_pkt_num = 0
        self.beacon_pkt_num_max = 0


        self.x_results = np.array([])
        self.y_results = np.array([])


        self.db_host = '192.168.42.200'
        self.db = 'sdrc_db'
        self.t1 = 'data_table'
        self.t1_fields = '(rpt_pkt_num, rpt_team_id, rpt_location, rpt_timestamp, beacon_id, beacon_pkt_num)'
        self.t1_field1 = '(rpt_location)'
        self.t1_field2 = '(rpt_timestamp)'

    def clean_exit(self):
        print 'shutting down connections...'
        self.conn.commit()
        self.cur.close() 
        self.conn.close()
        self.write_results()
        t_stop = time.time()
        t_tot = t_stop - self.t_start
        print ''
        print 'total run time: %s seconds' %t_tot
        print 'iterations lost to NaNs: ', self.num_NaN
        print 'total number of iterations: ', self.hyp_iter



  
    # db code
    ############################################################################
    def init_db(self):
        self.conn = psycopg2.connect(host = "128.173.90.88",
                                user = "sdrc_user",
                                password = "sdrc_pass",
                                database = "sdrc_db")
        # self.conn = psycopg2.connect(host = self.db_host,
        #                              user = self.user,
        #                              password = self.passwd,
        #                              database = self.db)
        self.cur = self.conn.cursor ()
        
    def db_sleep(self):
        t = random.random()
        print 'db sleep %f seconds' % t
        time.sleep(t)
        

    def close_cursor(self):
        self.cur.close()

    def close_db(self):
        self.conn.close()

    def get_max_beacon_pkt_num(self):
        self.cur.execute("SELECT MAX(beacon_pkt_num) FROM %s;" %(self.t1,))
        (result,) = self.cur.fetchone()
        self.beacon_pkt_num_max = result
        #self.new_idx_max = 10
        if self.DEBUG:
            print 'result: ', result

    def get_num_entries(self,n):
        self.cur.execute("SELECT %s FROM %s WHERE beacon_pkt_num = %s;" %(self.t1_fields,self.t1, n))
        data = self.cur.fetchall()
        return len(data)

    def db_get_loc(self,n):
        self.cur.execute("SELECT %s FROM %s WHERE beacon_pkt_num = %s;" %(self.t1_field1,self.t1, n))
        

    def db_get_time(self,n):
        self.cur.execute("SELECT %s FROM %s WHERE beacon_pkt_num = %s;" %(self.t1_field2,self.t1, n))
    ############################################################################



    def get_loc(self):
        self.db_get_loc(self.beacon_pkt_num)
        for (record,) in self.cur:
            self.loc.append(record.strip(' '))
        if self.DEBUG:
            print self.loc

    def get_time(self):
        self.db_get_time(self.beacon_pkt_num)
        for (record,) in self.cur:
            self.toa.append(record.strip(' '))
        if self.DEBUG:
            print self.toa


    def parse_loc(self):
        print self.loc
        for i in range(len(self.loc)):
            self.loc[i] =  self.loc[i].strip('()')
            tmploc =  self.loc[i].split(',')
            lon = np.float64(tmploc[0])
            lat = np.float64(tmploc[1])
            self.loc[i] = [lon,lat]
        # self.loc = np.array(self.loc)

    def parse_toa(self):
        print "toa: ", self.toa
        for i in range(len(self.toa)):
            self.toa[i] = np.float128(self.toa[i])
        # self.toa = np.array(self.toa)


            
    def write_results(self):
        host = os.uname()[1]
        d = time.localtime()
        date = '%s-%s-%s' %(str(d[0]),str(d[1]),str(d[2]))
        p = '/home/aryoung/batch_results/%s_%s' %(host, date)
        if not os.path.exists(p):
            os.makedirs(p)
        f = open('%s/x_results' %p,'w+')
        for num in self.x_results:
            f.write(str(num)+'\n')
        f.close()

        f = open('%s/y_results' %p,'w+')
        for num in self.y_results:
            f.write(str(num)+'\n')
        f.close()

    def tdoa(self,rx1,rx2,rx3, toa1, toa2, toa3):
        (x_h1,y_h1) = self.geo_utils.hyperbola(rx1,rx2,toa1,toa2)
        (x_h2,y_h2) = self.geo_utils.hyperbola(rx1,rx3,toa1,toa3)

        if self.DEBUG:
            print 'rx1: ', rx1
            print 'type(rx1): ', type(rx1)
            print 'x_h1: ', repr(x_h1)

        return [x_h1,y_h1,x_h2,y_h2]




    def fsm(self):
################################################################################
        self.init_db()
        self.t_start = time.time()

        while True:

            # check db status
            ####################################################################
            if self.state == 1:

                self.get_max_beacon_pkt_num()

                # db has no data
                # sleep
                if (self.beacon_pkt_num_max == None):
                    if self.DEBUG:
                        print "self.new_idx_max == None"
                    self.state = 2
                    continue

                # db has new data
                # get data and process
                if (self.beacon_pkt_num_max > self.beacon_pkt_num):
                    if self.DEBUG:
                        print "new data"
                        print "(self.beacon_pkt_num_max > self.beacon_pkt_num): %d > %d" %(self.beacon_pkt_num_max,self.beacon_pkt_num)
                    self.state = 3
                    continue

                # db has no new data
                # sleep and check again
                if not (self.beacon_pkt_num_max > self.beacon_pkt_num):
                    self.empty_loop_iterations += 1
                    if self.DEBUG:
                        print "no new data"
                        print "number of times checking for data with no result: ", self.empty_loop_iterations
                    if (self.empty_loop_iterations == self.max_empty_loop_iterations):
                        print "no new data for %d iterations" %self.empty_loop_iterations
                        print "ending program"
                        break
                    self.state = 2
                    continue
            ####################################################################




            # sleep
            ####################################################################
            if self.state == 2:
                self.db_sleep()
                self.state = 1
                continue
            ####################################################################




            # get data & parse
            ####################################################################
            if self.state == 3:
                self.loc = []
                self.toa = []

                if self.DEBUG:
                    print "beacon_pkt_num: ", self.beacon_pkt_num
                # this is a hack
                if (self.beacon_pkt_num > self.beacon_pkt_num_max):
                    self.state = 2 # sleep
                    continue

                # check if have enough entries to do tdoa
                entries = self.get_num_entries(self.beacon_pkt_num)
                if (entries < 3):
                    if self.DEBUG:
                        print "not enough entries for tdoa"
                    self.beacon_pkt_num +=1
                    self.state = 3 # try again
                    continue
                else:
                    self.get_loc()
                    self.parse_loc()
                    if self.DEBUG:
                        print '\n\n\n\n\n\n\n\n\n\n\n'
                        print '####################################################################'
                        print 'type(self.loc): ', type(self.loc)
                        print 'self.loc:\n', self.loc
                        print 'type(np.array(self.loc)): ',type(np.array(self.loc))
                        print 'np.array(self.loc):\n',np.array(self.loc)
                        print '####################################################################'
                        print '\n\n\n\n\n\n\n\n\n\n\n'                            
                    self.get_time()
                    self.parse_toa()
 
                    self.beacon_pkt_num +=1
                    self.state = 4
                    continue
            ####################################################################




            # build hyperbolas
            ####################################################################
            if self.state == 4:
                if self.method == 'tdoa':


                    # for i in range(len(self.loc)):
                    #     f = open('location_out.data','a')
                    #     f.write(str(self.loc[i]) + '\n')
                    #     f.close()

                    #     f = open('time_out.data','a')
                    #     f.write(str(self.toa[i]) + '\n')
                    #     f.close()

                    for i in range(len(self.loc)-2):

                        if self.DEBUG:
                            print 'type self.loc[i]: ', type(self.loc[i])
                            print 'self.loc[i]: ', self.loc[i]
                            print 'self.loc: ', self.loc
                        #fi

                        ans = self.tdoa(self.loc[i],self.loc[i+1],self.loc[i+2],
                                        self.toa[i],self.toa[i+1],self.toa[i+2])
                        if (np.isnan(ans).any()):
                            print 'answer containt NaN'
                            print 'dropping array and continuing'
                            self.num_NaN += 1
                            self.state = 1
                            continue
                        else:
                            self.x_results = np.concatenate([self.x_results,ans[0]])
                            self.x_results = np.concatenate([self.x_results,ans[2]])
                            self.y_results = np.concatenate([self.y_results,ans[1]])
                            self.y_results = np.concatenate([self.y_results,ans[3]])

                            self.h.write_hyperbola(ans)

                        if ( (self.hyp_iter % 10) == 0):
                            # code = tdoa_stats.three_pass(self.x_results,self.y_results)
                            # print 'code: ', code
                            guess = tdoa_stats.three_pass(self.x_results,self.y_results)
                            print 'guess: ', guess
                            if (guess == (-1,-1)):
                                print '(guess == (-1,-1)'
                        #     else:
                        #         # check how close guess is to real location
                        #         test_dist = 10 # meters
                        #         alarm = check_accuracy.check_accuracy(guess,test_dist)
                        #         if alarm:
                        #             print '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'
                        #             print '####################################################################'
                        #             print '\n\n\n\n\n\n\n\n\n\n\n'
                        #             print 'Guess is within %d meters of transmitter location!!'
                        #             print 'number of hyperbola pairs (iterations): ', self.hyp_iter
                        #             print '\n\n\n\n\n\n\n\n\n\n\n'
                        #             print '####################################################################'
                        #             print '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'
                        #             sys.exit()
                        #         #fi
                        #     # fi
                        # # fi    
                        self.hyp_iter +=1




                            

                    
                else: # method = 'custom'
                    pass
                self.state = 1

                
                continue
            ####################################################################

            # resolve data
            ####################################################################
            # if self.state == 5:
            #     if self.DEBUG:
            #         print 'tdoa iterator: ', self.tdoa_iterator
            #     if ( ((self.tdoa_iterator%50)==0) or 
            #          (self.loop_escape == self.loop_escape) ):
            #         ret_code = refine_results.geo_hist(self.x_results,
            #                                            self.y_results,
            #                                            self.kml_file_number)
            #         self.kml_file_number += 1
            #         if not (ret_code == 0):
            #             print 'error in running 2d histograms: ', ret_code
            #     else:
            #         pass
            #     self.state = 1
            #     continue
            ####################################################################

            # error!!
            ####################################################################
            if self.state not in [1,2,3,4]:
                print "error!! unreachable state!!"
                continue
            ####################################################################


        self.clean_exit()
        
################################################################################




if __name__=='__main__':
    # from optparse import OptionParser
    # parser = OptionParser()
    # parser.add_option("-n", "--number", type="string", default="01",
    #                   help="number of target machine in cluster")
    # # parser.add_option("-D", "--DROP", action="store_true", default=False,
    # #                   help="turn on dropped packets")
    # # parser.add_option("-d", "--drop", type="int", default=10
    # #                   help="percentage of dropped packets")
    # # parser.add_option("-J", "--JITTER", action="store_true", default=False,
    # #                   help="turn on clock jitter")
    # # parser.add_option("-j", "--jitter", type="float",default=1e-12,
    # #                   help="number of target machine in cluster")


    # (options, args) = parser.parse_args()
    # if len(args) != 0:
    #     parser.print_help(sys.stderr)
    #     sys.exit(1)


    main = geo_module()
    main.fsm()
    




                        # tmp_loc = []
                        # tmp_toa = []
                        # tmp_loc.append(self.loc[i])
                        # tmp_loc.append(self.loc[i+1])
                        # tmp_loc.append(self.loc[i+2])
                        # tmp_toa.append(self.toa[i])
                        # tmp_toa.append(self.toa[i+1])
                        # tmp_toa.append(self.toa[i+2])

                        # if self.DEBUG:
                        #     print "tmp_loc: ", tmp_loc
                        #     print "tmp_toa: ", tmp_toa
                        # self.geoloc.tdoa(tmp_loc,tmp_toa)
                        # if not (intersection == -1):
                        #     self.x_results += intersection[0]
                        #     self.y_results += intersection[1]
                        #     self.state = 5
                        #     self.tdoa_iterator += 1
                        # else:
                        #     self.state = 1
                        #     continue



                        # (x_h1,y_h1) = self.geo_utils.hyperbola(self.loc[i],self.loc[i+1],
                        #                                        self.toa[i],self.toa[i+1])
                        # if self.DEBUG:
                        #     print '\n\n\n\n\n\n\n\n\n\n\n'
                        #     print '####################################################################'
                        #     print 'len(x_h1): ', len(x_h1)
                        #     print 'len(y_h1): ', len(y_h1)
                        #     print 'type x_h1: ', type(x_h1)
                        #     print 'type self.x_hyperbola: ', type(self.x_hyperbola)
                        #     print 'self.x_hyperbola:\n', self.x_hyperbola
                        #     print 'x_h1:\n', x_h1
                        #     print 'type x_h1[1]: ', type(x_h1[1])
                        #     print 'x_h1[1]:\n', x_h1[1]
                        #     print 'shape(self.x_hyperbola): ', np.shape(self.x_hyperbola)
                        #     print 'shape(x_h1): ', np.shape(x_h1)
                        #     print '####################################################################'
                        #     print '\n\n\n\n\n\n\n\n\n\n\n'
                            
                        
                        # self.x_hyperbola = np.array([self.x_hyperbola,x_h1])
                        # self.y_hyperbola = np.array([self.y_hyperbola,y_h1])

                        #  = self.geo_utils.hyperbola(self.loc[i],self.loc[i+2],
                        #                                 self.toa[i],self.toa[i+2])
                        # self.x_hyperbola = np.array([self.x_hyperbola,x_h2])
                        # self.y_hyperbola = np.array([self.y_hyperbola,y_h2])
                        # ans = [x_h1,y_h1,x_h2,y_h2]
                        # h.write_hyperbola(ans)
