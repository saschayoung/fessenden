#!/usr/bin/env python

import time, random, struct
import numpy as np
import psycopg2

import sim_utils


class db_blob2data:

    def __init__(self):

        self.DEBUG = True

        self.t_sleep = 0.01

        self.user = 'sdrc_user'
        self.passwd = 'sdrc_pass'

        self.state = 1
        self.loop_escape = 0

        #self.old_idx_min = 1
        self.old_idx_max = 1
        #self.new_idx_min = 1
        self.new_idx_max = 1

        # self.db_host = '192.168.42.200'
        self.db_host = '128.173.90.67'
        self.db = 'sdrc_db'
        self.t1 = 'blob_table'
        self.t1_fields = '(field_1)'
        
        self.t2 = 'data_table'
        self.t2_fields = '(rpt_pkt_num, rpt_team_id, rpt_location, rpt_timestamp, beacon_id, beacon_pkt_num)'


        
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

    def get_max_idx(self):
        self.cur.execute("SELECT MAX(idx) FROM %s;" %(self.t1,))
        (result,) = self.cur.fetchone()
        self.new_idx_max = result
        #self.new_idx_max = 10
        if self.DEBUG:
            print 'result: ', result

    def get_blob(self,n):
        self.cur.execute("SELECT %s FROM %s WHERE idx = %s;" %(self.t1_fields,self.t1, n))
        (self.blob,) = self.cur.fetchone()
        print "blob: ", self.blob
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
        self.rpt_location = sim_utils.unpack_loc(self.blob[4:24])
        self.rpt_timestamp = sim_utils.unpack_time(self.blob[24:36])
        (self.beacon_packet_num,) = struct.unpack('!H',self.blob[36:38])

        (self.beacon_id,) = struct.unpack('!H',self.blob[38:40])

        if self.DEBUG:
            print "rpt_packet_num: ", self.rpt_packet_num
            print "rpt_team_id: ", self.rpt_team_id
            print "rpt_location: ", self.rpt_location
            print "rpt_timestamp: ", self.rpt_timestamp
            print "beacon_packet_num: ", self.beacon_packet_num
            print "beacon_id: ", self.beacon_id
            print '\n\n\n'



    def write_data(self):
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
        self.init_db()


        while True:
            

            # check db status
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
                    if (self.loop_escape == 100):
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

            # sleep
            if self.state == 2:
                self.db_sleep()
                self.state = 1
                continue

            # get data
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
                


            # ??
            if self.state not in [1,2,3]:
                print "error!! unreachable state!!"
                continue

        
        self.conn.commit()
        self.cur.close() 
        self.conn.close()

            
                

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



if __name__=='__main__':
    main = db_blob2data()
    main.run()
    




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
