#!/usr/bin/env python

# core libraries
import time, random, struct,sys
from types import NoneType

# external libraries
import psycopg2
import numpy as np

# local imports
import pack_utils


DEBUG = True


def update(iteration):
    sys.stdout.write("Working... iteration: %3d\r" % iteration)
    sys.stdout.flush()


class db_agent:

    def __init__(self,options):
        pass

    def start_db(self):
        self.host = options.host
        self.conn = psycopg2.connect(host = self.host,
                                     user = "sdrc_user",
                                     password = "sdrc_pass",
                                     database = "sdrc_db")
        self.cur = self.conn.cursor()
        
    def stop_db(self):
        self.cur.close()
        self.conn.close()

    def sleep(self):
        t = random.random()
        if DEBUG:
            print 'db sleep %f seconds' % t
        time.sleep(t)
        
    def max_idx(self):
            self.cur.execute("SELECT MAX(idx) FROM binary_data_table;" )
            (idx,) = self.cur.fetchone()
            return idx

    def get_binary_data(self,n):
        self.cur.execute("SELECT (binary_data) FROM binary_data_table WHERE idx = %s;" %(n,))
        (binary_data,) = self.cur.fetchone()
        return binary_data

   
    def run(self):
        self.start_db()

        max_idx = self.max_idx()

        for i in range(max_idx):
            j = i+1

            # get the data from db
            binary_data = self.get_binary_data(j)

            # parse data into readable form
            (field_radio_pkt_num,) = struct.unpack('!i',binary_data[0:4])        
            (field_team_id,) = struct.unpack('!i',binary_data[4:8])
            field_team_loc = pack_utils.unpack_loc(binary_data[8:32])
            field_team_time = pack_utils.unpack_time(binary_data[32:44])
            (beacon_pkt_num,) = struct.unpack('!i',binary_data[44:48])
            (beacon_id,) = struct.unpack('!i',binary_data[48:52])

            # write to db
            s1 = 'hrf_data_table'
            s2 = '(field_team_pkt_num, field_team_id, field_team_location, field_team_time, beacon_pkt_num, beacon_id)'

            self.cur.execute("""INSERT INTO %s %s VALUES (%s, %s, %s, %s, %s, %s);""" %(s1,s2,field_radio_pkt_num,
                                                                                        field_team_id, field_team_loc,
                                                                                        field_team_time, beacon_pkt_num,
                                                                                        beacon_id))
            self.conn.commit()
            update(j)


        self.stop_db()






if __name__=='__main__':
    from optparse import OptionParser
    usage = "usage: %prog option arg"

    parser = OptionParser(usage=usage)
    parser.add_option("", "--host", type="string", default="128.173.90.88",
                      help="database host in dotted decimal form [default=%default]")

    (options, args) = parser.parse_args()
    
    agent = db_agent(options)
    agent.run()







