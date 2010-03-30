#!/usr/bin/env python

import time, random, struct
import numpy as np
import psycopg2

import new_sim_utils




class db_blob2data:

    def __init__(self,options):

        DEBUG = True

        self.t_sleep = 0.01


        self.state = 1
        self.db_wait_loop = 0

        self.old_idx_max = 1
        self.new_idx_max = 1



        self.t1 = 'blob_table'
        self.t1_fields = '(field_1)'
        
        self.t2 = 'data_table'
        self.t2_fields = '(rpt_pkt_num, rpt_team_id, rpt_location, rpt_timestamp, beacon_id, beacon_pkt_num)'


        
    def init_db(self):
        self.host = options.host
        self.conn = psycopg2.connect(host = self.host,
                                     user = "sdrc_user",
                                     password = "sdrc_pass",
                                     database = "sdrc_db")
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

    def get_max_idx(self):
        self.cur.execute("SELECT MAX(idx) FROM %s;" %(self.t1,))
        (result,) = self.cur.fetchone()
        self.new_idx_max = result
        #self.new_idx_max = 10
        if DEBUG:
            print 'result: ', result

    def get_blob(self,n):
        self.cur.execute("SELECT %s FROM %s WHERE idx = %s;" %(self.t1_fields,self.t1, n))
        (self.blob,) = self.cur.fetchone()
        print "blob: ", self.blob
        print "blob length: ", len(self.blob)
#             if (len(self.blob) == 40):
#                 break
#             else:
#                 pass

    def parse_blob(self):
        print '\n\n\n'
        print "type(self.blob): ", type(self.blob)
        print "len(blob): ", len(self.blob)
        (self.rpt_packet_num,) = struct.unpack('!H',self.blob[0:2])        
        (self.rpt_team_id,) = struct.unpack('!H',self.blob[2:4])
        self.rpt_location = new_sim_utils.unpack_loc(self.blob[4:28])
        self.rpt_timestamp = new_sim_utils.unpack_time(self.blob[28:40])
        (self.beacon_packet_num,) = struct.unpack('!H',self.blob[40:42])

        (self.beacon_id,) = struct.unpack('!H',self.blob[42:44])

        if DEBUG:
            print "rpt_packet_num: ", self.rpt_packet_num
            print "rpt_team_id: ", self.rpt_team_id
            print "rpt_location: ", self.rpt_location
            print "rpt_timestamp: ", self.rpt_timestamp
            print "beacon_packet_num: ", self.beacon_packet_num
            print "beacon_id: ", self.beacon_id
            print '\n\n\n'



    def write_data(self):
        f = open('location_bt.data', 'a')
        f.write(str(self.rpt_location) + '\n')
        f.close

        f = open('time_bt.data', 'a')
        f.write(str(self.rpt_timestamp) + '\n')
        f.close
        self.cur.execute("""INSERT INTO %s %s VALUES (%s, %s, %s, %s, %s, %s);""" %(
                self.t2,
                self.t2_fields,
                self.rpt_packet_num,
                self.rpt_team_id,
                str(self.rpt_location),
                repr(self.rpt_timestamp),
                self.beacon_id,
                self.beacon_packet_num))
        self.conn.commit()





    def run(self):
################################################################################
        self.init_db()

        while True:

            # check db status
            ####################################################################
            if self.state == 1:
                self.get_max_idx()

                # db has no data
                if (self.new_idx_max == None):
                    print "self.new_idx_max == None"
                    self.state = 2
                    continue

                # db has no new data
                if not (self.new_idx_max > self.old_idx_max):
                    self.loop_escape += 1
                    print "no new data"
                    print "print loop_escape: ", self.loop_escape
                    if (self.loop_escape ==5):
                        print "no new data for 100 iterations"
                        print "ending program"
                        break
                    self.state = 2
                    continue

                # db has new data
                if (self.new_idx_max > self.old_idx_max):
                    print "new data"
                    print "(self.new_idx_max > self.old_idx_max): %d > %d" %(self.new_idx_max,self.old_idx_max)
                    self.state = 3
                    continue
            ####################################################################

            # sleep
            ####################################################################
            if self.state == 2:
                self.db_sleep()
                self.state = 1
                continue
            ####################################################################

            # get data
            ####################################################################
            if self.state == 3:
                # self.get_blob(1)
                # self.parse_blob()
                # self.write_data()
                for i in range(self.old_idx_max,self.new_idx_max):
                    # print "i in range: ", (i,range(self.old_idx_max,self.new_idx_max))                    
                    self.get_blob(i)
                    if not (len(self.blob) == 0):
                        self.parse_blob()
                        self.write_data()
                self.old_idx_max = self.new_idx_max
                self.state = 1
                continue
            ####################################################################
                


            # ??
            ####################################################################
            if self.state not in [1,2,3]:
                print "error!! unreachable state!!"
                continue
            ####################################################################

        
        self.conn.commit()
        self.cur.close() 
        self.conn.close()
################################################################################
            
                




if __name__=='__main__':
    from optparse import OptionParser
    usage = "usage: %prog option arg"

    parser = OptionParser(usage=usage)
    parser.add_option("", "--host", type="string", default="128.173.90.68",
                      help="database host in dotted decimal form [default=%default]")

    (options, args) = parser.parse_args()
    main = db_blob2data(options)
    main.run()













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
