#!/usr/bin/env python

import time, random, struct
import os
import numpy as np
import psycopg2
#import matplotlib.pyplot as plt
import test_coords
import alex_random

from geo_utils import geo_utils
from geolocation import geolocation
import refine_results

class geo_module:

    def __init__(self,options):
        self.DEBUG = True

        self.geo_utils = geo_utils()
        self.geoloc = geolocation()
        self.method = 'tdoa'  # method {'tdoa'|'custom'}

        
        self.tdoa_iterator = 1
        self.t_sleep = 0.01

        self.user = 'sdrc_user'
        self.passwd = 'sdrc_pass'
        self.kml_file_number = 1
        self.state = 1
        self.dead_loop = 0
        self.loop_escape = 5
        
        #beacon packet number for extracting from db
        self.bpn = 0
        self.bpn_max = 0




        self.db_host = '192.168.42.200'
        self.db = 'sdrc_db'
        self.t1 = 'data_table'+options.number
        self.t1_fields = '(rpt_pkt_num, rpt_team_id, rpt_location, rpt_timestamp, beacon_id, beacon_pkt_num)'
        self.t1_field1 = '(rpt_location)'
        self.t1_field2 = '(rpt_timestamp)'
        self.x_results = []
        self.y_results = []


  
    # db code
    ############################################################################
    def init_db(self):
        self.conn = psycopg2.connect(host = "128.173.90.68",
                                user = "sdrc_user",
                                password = "sdrc_pass",
                                database = "sdrc_db")
        # self.conn = psycopg2.connect(host = self.db_host,
        #                              user = self.user,
        #                              password = self.passwd,
        #                              database = self.db)
        self.cur = self.conn.cursor ()
        
    def db_sleep(self):
        t = self.t_sleep
        print 'db sleep %f seconds' % t
        time.sleep(t)
        self.t_sleep = random.random()
        

    def close_cursor(self):
        self.cur.close()

    def close_db(self):
        self.conn.close()

    def get_max_bpn(self):
        self.cur.execute("SELECT MAX(beacon_pkt_num) FROM %s;" %(self.t1,))
        (result,) = self.cur.fetchone()
        self.bpn_max = result
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
        self.db_get_loc(self.bpn)
        for (record,) in self.cur:
            self.loc.append(record.strip(' '))
        if self.DEBUG:
            print self.loc

    def get_time(self):
        self.db_get_time(self.bpn)
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
            self.loc[i] = (lon,lat)

    def parse_toa(self):
        print "toa: ", self.toa
        for i in range(len(self.toa)):
            self.toa[i] = np.float128(self.toa[i])


            
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




    def fsm(self):
################################################################################
        self.init_db()
        t_start = time.time()

        while True:
            # check db status
            ####################################################################
            if self.state == 1:

                self.get_max_bpn()

                # db has no data
                if (self.bpn_max == None):
                    if self.DEBUG:
                        print "self.new_idx_max == None"
                    self.state = 2
                    continue

                # db has new data
                if (self.bpn_max > self.bpn):
                    if self.DEBUG:
                        print "new data"
                        print "(self.bpn_max > self.bpn): %d > %d" %(self.bpn_max,self.bpn)
                    self.state = 3
                    continue

                # db has no new data
                if not (self.bpn_max > self.bpn):
                    self.loop_escape += 1
                    if self.DEBUG:
                        print "no new data"
                        print "print dead loop iteration: ", self.dead_loop
                    if (self.loop_escape == self.loop_escape):
                        print "no new data for %d iterations" %self.loop_escape
                        print "checking for unresoved data before ending program"
                        break
                    self.state = 5
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

                print "bpn: ", self.bpn
                # this is a hack
                if (self.bpn > self.bpn_max):
                    self.state = 2 # sleep
                    continue

                # check if have enough entries to do tdoa
                entries = self.get_num_entries(self.bpn)
                if (entries < 3):
                    if self.DEBUG:
                        print "not enough entries for tdoa"
                    self.bpn +=1
                    self.state = 3 # try again
                    continue
                else:
                    self.get_loc()
                    self.parse_loc()
                    self.get_time()
                    self.parse_toa()
 
                    self.bpn +=1
                    self.state = 4
                    continue
            ####################################################################

            # perform tdoa
            ####################################################################
            if self.state == 4:
                if self.method == 'tdoa':
                    for i in range(len(self.loc)-2):
                        tmp_loc = []
                        tmp_toa = []
                        tmp_loc.append(self.loc[i])
                        tmp_loc.append(self.loc[i+1])
                        tmp_loc.append(self.loc[i+2])
                        tmp_toa.append(self.toa[i])
                        tmp_toa.append(self.toa[i+1])
                        tmp_toa.append(self.toa[i+2])

                        if self.DEBUG:
                            print "tmp_loc: ", tmp_loc
                            print "tmp_toa: ", tmp_toa
                        intersection = self.geoloc.tdoa(tmp_loc,tmp_toa)
                        if not (intersection == -1):
                            self.x_results += intersection[0]
                            self.y_results += intersection[1]
                            self.state = 5
                            self.tdoa_iterator += 1
                        else:
                            self.state = 1
                            continue
                    
                else: # method = 'custom'
                    pass
                # move the following line to the end of the file?
                # self.write_results()


                
                continue
            ####################################################################

            # resolve data
            ####################################################################
            if self.state == 5:
                if self.DEBUG:
                    print 'tdoa iterator: ', self.tdoa_iterator
                if ( ((self.tdoa_iterator%50)==0) or 
                     (self.loop_escape == self.loop_escape) ):
                    ret_code = refine_results.geo_hist(self.x_results,
                                                       self.y_results,
                                                       self.kml_file_number)
                    self.kml_file_number += 1
                    if not (ret_code == 0):
                        print 'error in running 2d histograms: ', ret_code
                else:
                    pass
                self.state = 1
                continue
            ####################################################################

            # error!!
            ####################################################################
            if self.state not in [1,2,3,4,5]:
                print "error!! unreachable state!!"
                continue
            ####################################################################

        
        self.conn.commit()
        self.cur.close() 
        self.conn.close()
        self.write_results()
        t_stop = time.time()
        t_tot = t_stop - t_start
        print ''
        print 'total run time: %s seconds' %t_tot
################################################################################




if __name__=='__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-n", "--number", type="string", default="01",
                      help="number of target machine in cluster")
    # parser.add_option("-D", "--DROP", action="store_true", default=False,
    #                   help="turn on dropped packets")
    # parser.add_option("-d", "--drop", type="int", default=10
    #                   help="percentage of dropped packets")
    # parser.add_option("-J", "--JITTER", action="store_true", default=False,
    #                   help="turn on clock jitter")
    # parser.add_option("-j", "--jitter", type="float",default=1e-12,
    #                   help="number of target machine in cluster")


    (options, args) = parser.parse_args()
    if len(args) != 0:
        parser.print_help(sys.stderr)
        sys.exit(1)


    main = geo_module(options)
    main.fsm()
    


