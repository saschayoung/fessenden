#!/usr/bin/env python

import time, random, struct
import numpy as np
import psycopg2
#import matplotlib.pyplot as plt
import test_coords
import alex_random

from geo_utils import geo_utils
from geolocation import geolocation
import refine_results

class geo_module:

    def __init__(self):
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
        self.t1 = 'data_table'
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
        f = open('x_results','w+')
        for num in self.x_results:
            f.write(str(num)+'\n')
        f.close()

        f = open('y_results','w+')
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
    main = geo_module()
    main.fsm()
    


    # tdoa
    # ############################################################################
    # def tdoa(self):
    #     # tx = test_coords.get_tx_coords()
    #     # loc0 = test_coords.get_boathouse_coords()
    #     # loc1 = test_coords.get_uspto_coords()
    #     # loc2 = test_coords.get_tcwhs_coords()
    #     loc0 = self.loc[0]
    #     loc1 = self.loc[1]
    #     loc2 = self.loc[2]
        
    #     # toa0 = self.geo_utils.time_of_flight(tx,loc0)
    #     # toa1 = self.geo_utils.time_of_flight(tx,loc1)
    #     # toa2 = self.geo_utils.time_of_flight(tx,loc2)
    #     print self.toa
    #     toa0 = self.toa[0]
    #     toa1 = self.toa[1]
    #     toa2 = self.toa[2]
    #     if ( (toa0 == toa1) and (toa0 == toa2) ):
    #         print '\n\n\n\n\n\n\nerror!!!'
    #         print "(toa0 == toa1) and (toa0 == toa2)!!"
    #         print '\n\n\n\n\n\n\n'
    #         self.errors +=1
    #         self.err1 +=1
    #         return -1
    #     elif ( (toa0 == toa1) and not (toa0 == toa2) ):
    #         (x_h1,y_h1) = self.geo_utils.hyperbola(loc2,loc1,toa2,toa1)
    #         (x_h2,y_h2) = self.geo_utils.hyperbola(loc0,loc2,toa0,toa2)
    #     elif ( not (toa0 == toa1) and  (toa0 == toa2) ):
    #         (x_h1,y_h1) = self.geo_utils.hyperbola(loc0,loc1,toa0,toa1)
    #         (x_h2,y_h2) = self.geo_utils.hyperbola(loc1,loc2,toa1,toa2)
    #     else:
    #         (x_h1,y_h1) = self.geo_utils.hyperbola(loc0,loc1,toa0,toa1)
    #         (x_h2,y_h2) = self.geo_utils.hyperbola(loc0,loc2,toa0,toa2)
            

    #     if ( np.isnan(x_h1[0]) or np.isnan(y_h1[0]) ):
    #         print '\n\n\n\n\n\n\n\n\n\n\n\n\nerror!!!'
    #         print "np.isnan(x_h1[0]) or np.isnan(y_h1[0])!!"
    #         print '\n\n\n\n\n\n\n\n\n\n\n\n\n'        
    #         self.errors +=1
    #         self.err2 +=1
    #         return -1
    #     if ( np.isnan(x_h2[0]) or np.isnan(y_h2[0]) ):
    #         print '\n\n\n\n\n\n\n\n\n\n\n\n\nerror!!!'
    #         print "np.isnan(x_h2[0]) or np.isnan(y_h2[0])!!"
    #         print '\n\n\n\n\n\n\n\n\n\n\n\n\n'
    #         self.errors +=1
    #         self.err2 +=1
    #         return -1
        
    #     (x_coords,y_coords) = self.geo_utils.intersections(x_h1,y_h1,x_h2,y_h2)
    #     if ( (x_coords == -1) and (y_coords == -1) ):
    #         print "intersection.m returns no data, return -1 to main"
    #         self.errors +=1
    #         self.err3 +=1
    #         return -1
        

    #     if self.DEBUG:
    #         print loc0
    #         print loc1
    #         print loc2

    #         plt.figure()
    #         plt.plot(loc0[0],loc0[1],'g^',
    #                  loc1[0],loc1[1],'g^',
    #                  loc2[0],loc2[1],'g^',
    #                  x_h1,y_h1,'b',
    #                  x_h2,y_h2,'g',
    #                  x_coords,y_coords,'*',
    #                  )
    #         plt.grid(True)
    #         plt.show()
    #     return [x_coords, y_coords]






        # (self.data,) = self.cur.fetchone()
        # print "blob: ", self.blob
#             if (len(self.blob) == 40):
#                 break
#             else:
#                 pass

#                    print "result == \'None\'"
#                 print 'database table %s has no data' %self.t1
#                 self.db_sleep()
#             else:
#                 print 'break'
#                 break
                # 
                # if yes, sleep then repeat



#             self.get_max_idx()
#             if (self.db_idx == None):
#                 print "result == \'None\'"
#                 print 'database table %s has no data' %self.t1
#                 self.db_sleep()
#             else:
#                 print 'break'
#                 break

#         print 'for i in range(self.db_idx):'
#         for i in range(self.db_idx,self.db_idx_max):
#             self.get_blob()
#             self.parse_blob()
#             self.write_data()


#         self.close_cursor()
#         self.close_db()
            




        
        
        # get max(idx) from t1
        # if result == none
        #   wait/backoff/sleep
        #   repeat get max(idx) from t1
        # for 1 to max(idx):
        #   get blob(idx) from t1
        #   parse blob
        #   write data to t2
        # update db_idx


                # self.get_blob(1)
                # self.parse_blob()
                # self.write_data()
                # for i in range(self.old_idx_max,self.new_idx_max):
                #     print "i: ", range(self.old_idx_max,self.new_idx_max)
                #     self.get_blob(i)
                #     self.parse_blob()
                #     self.write_data()
                # self.old_idx_max = self.new_idx_max
                # self.state = 1
                # continue
                


            # ??



# cursor.execute("SELECT MAX(idx) FROM test01_table")

# result = cursor.fetchone ()

# print "result: ", result

# print 'cursor.close ()'
# cursor.close ()

# print 'db.close ()'
# db.close ()



#     def run(self):

        
#         db = MySQLdb.connect (host = "localhost",
#                               user = "sdrc_user",
#                               passwd = "sdrc_pass",
#                               db = "blob_test")

#         cursor = db.cursor ()

#         table = 'blob_table'
#         fields = '(field_1)'



#         sql = """INSERT INTO %s %s VALUES (\'%s\')""" %(table,fields,payload)


#         print 'cursor.execute(sql)'
#         cursor.execute(sql)

#         print 'db.commit()'
#         db.commit()

#         db.close()


    # def parse_blob(self):
    #     print '\n\n\n'
    #     print "type(self.blob): ", type(self.blob)
    #     print "len(blob): ", len(self.blob)
    #     (self.rpt_packet_num,) = struct.unpack('!H',self.blob[0:2])        
    #     (self.rpt_team_id,) = struct.unpack('!H',self.blob[2:4])
    #     self.rpt_location = sim_utils.unpack_loc(self.blob[4:24])
    #     self.rpt_timestamp = sim_utils.unpack_time(self.blob[24:36])
    #     (self.beacon_packet_num,) = struct.unpack('!H',self.blob[36:38])

    #     (self.beacon_id,) = struct.unpack('!H',self.blob[38:40])

    #     if self.DEBUG:
    #         print "rpt_packet_num: ", self.rpt_packet_num
    #         print "rpt_team_id: ", self.rpt_team_id
    #         print "rpt_location: ", self.rpt_location
    #         print "rpt_timestamp: ", self.rpt_timestamp
    #         print "beacon_packet_num: ", self.beacon_packet_num
    #         print "beacon_id: ", self.beacon_id
    #         print '\n\n\n'



    # def write_data(self):
    #     self.cur.execute("""INSERT INTO %s %s VALUES (%s, %s, %s, %s, %s, %s);""" %(
    #             self.t2,
    #             self.t2_fields,
    #             self.rpt_packet_num,
    #             self.rpt_team_id,
    #             str(self.rpt_location),
    #             repr(self.rpt_timestamp),
    #             self.beacon_id,
    #             self.beacon_packet_num))
    #     self.conn.commit()
