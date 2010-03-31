#!/usr/bin/env python


import struct
from types import NoneType

import psycopg2
import numpy as np

DEBUG = False

class fast_db_access:

    def __init__(self, host):
        self.host = host
        self.current_beacon_pkt_num = 0
        self.first_run = True
        

    def start_db(self):
        self.conn = psycopg2.connect(host = self.host,
                                     user = "sdrc_user",
                                     password = "sdrc_pass",
                                     database = "sdrc_db")
        self.cur = self.conn.cursor()

    def stop_db(self):
        # conn.commit() <- is this needed?
        self.cur.close() 
        self.conn.close()

    # specific db queries
    ############################################################################
    def get_first(self):
            self.cur.execute("SELECT MIN(beacon_pkt_num) FROM hrf_data_table;")
            (self.current_beacon_pkt_num,) = self.cur.fetchone()

    def get_idxs(self):
        self.cur.execute("SELECT idx FROM hrf_data_table WHERE beacon_pkt_num = %s;"
                         %(self.current_beacon_pkt_num,))
        idxs = self.cur.fetchall()
        return idxs

            

    def run(self):
        self.start_db()

        # get first beacon packet number in db        
        ########################################################################
        if self.first_run:
            self.get_first()
            self.first_run = False
        ########################################################################


        # get indices 
        ########################################################################
        current_idxs = self.get_idxs()
        self.current_beacon_pkt_num += 1 

        if ( current_idxs == [] ):             # if no data
            self.stop_db()                     # exit
            return -1

        
        # while ( len(current_idxs) < 3 ):       # get more data if there's 
        #     current_idxs = self.get_idxs()     # not three sets
        #     self.current_beacon_pkt_num += 1

        #     if ( current_idxs == [] ):             # if no data
        #         self.stop_db()                     # exit
        #         return -1


        for i in range(len(current_idxs)):
            (current_idxs[i],) = current_idxs[i]
        ########################################################################



        # get data
        ########################################################################            
        data = []
        for i in current_idxs:
            self.cur.execute("SELECT * FROM hrf_data_table WHERE idx = %s;" %(i,))
            r = self.cur.fetchone()
            if ( type(r) is NoneType ):
                self.stop_db()
                return -1
            else:
                (index,pkt_num,team_id,loc,t,beacon_pkt_num,beacon_id) = r
                loc = loc.strip(' ()')        # format location
                loc = loc.split(',')
                loc[0] = np.float128(loc[0])
                loc[1] = np.float128(loc[1])

                t = t.strip(' ')              # format time
                t = np.float128(t)
                data.append([loc,t])
        ########################################################################            



        self.stop_db()
        return data




if __name__=='__main__':
    from optparse import OptionParser

    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage=usage)
    parser.add_option("", "--host", type="string", default="128.173.90.88",
                      help="database host in dotted decimal form [default=%default]")
    (options, args) = parser.parse_args()
    
    db = fast_db_access()
    data = db.run()
    
    # print data



            # if DEBUG:
            #     print "current_idxs: ", current_idxs
            #     print "data: ", data
            # #fi

