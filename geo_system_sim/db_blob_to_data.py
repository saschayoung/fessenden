#!/usr/bin/env python

import time, random
import numpy as np
iport MySQLdb

class db_blob_2_data:

    def __init__(self):

        self.t_sleep = 0.01

        self.user = 'sdrc_user'
        self.passwd = 'sdrc_passwd'

        self.db_idx = 1
        self.db_host = 'localhost'
        self.db = 'blob_test'
        self.t1 = 'blob_table'
        self.t1_fields = '(field_1)'
        
        self.t2 = 'data_table'
        self.t2_fields = '(rpt_pkt_num, rpt_team_id, rpt_location, rpt_timestamp, beacon_id, beacon_pkt_num)'


        
    def init_db(self):

        self.db = MySQLdb.connect (host = self.db_host,
                                   user = self.user,
                                   passwd = self.passwd,
                                   db = self.db)

        self.cursor = self.db.cursor ()
        


    def db_sleep(self):
        t = self.t_sleep
        print 'db backoff & sleep %f seconds' % t
        time.sleep(
        
        




    def close_cursor(self):
        self.cursor.close()

    def close_db(self):
        self.db.close()

    def get_max_idx(self):
        s = "SELECT MAX(idx) FROM %s" %t1

        self.cursor.execute(s)

result = cursor.fetchone ()

print "result: ", result



    def run(self):
        
        # get max(idx) from t1
        # if result == none
        #   wait/backoff/sleep
        #   repeat get max(idx) from t1
        # for 1 to max(idx):
        #   get blob(idx) from t1
        #   parse blob
        #   write data to t2
        # update db_idx





cursor.execute("SELECT MAX(idx) FROM test01_table")

result = cursor.fetchone ()

print "result: ", result

print 'cursor.close ()'
cursor.close ()

print 'db.close ()'
db.close ()



    def run(self):

        
        db = MySQLdb.connect (host = "localhost",
                              user = "sdrc_user",
                              passwd = "sdrc_pass",
                              db = "blob_test")

        cursor = db.cursor ()

        table = 'blob_table'
        fields = '(field_1)'



        sql = """INSERT INTO %s %s VALUES (\'%s\')""" %(table,fields,payload)


        print 'cursor.execute(sql)'
        cursor.execute(sql)

        print 'db.commit()'
        db.commit()

        db.close()
