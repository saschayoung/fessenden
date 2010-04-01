#!/usr/bin/env python


# external libraries
import psycopg2
import numpy as np

class geolocation_table:
    """
    Database access and manipulation tools for geolocation_table
    """

    def __init__(self, host):
        self.host = host
        

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

    def get_idx(self):
            self.cur.execute("SELECT MAX(idx) FROM geolocation_table;")
            (idx,) = self.cur.fetchone()
            return idx

    def get_data(self,idx):
            self.cur.execute("SELECT * FROM geolocation_table WHERE idx = %s;" %(idx,))
            r = self.cur.fetchone()
            if ( type(r) is NoneType ):
                self.stop_db()
                return -1
            else:
                (index,hist_box1_c1,hist_box1_c2,hist_box2_c1,hist_box2_c2,guess) = r
                r = r[1:]
                return r

class kb_table:
    """
    Database access and manipulation tools for knowledgebase (kb_table)
    """

    def __init__(self, host):
        self.host = host
        

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

    def get_loc_hrf_table(self,n):
            self.cur.execute("SELECT MAX(idx) FROM hrf_data_table WHERE field_team_id = %s;" %(n))
            (idx,) = self.cur.fetchone()
            self.cur.execute("SELECT field_team_location FROM hrf_data_table WHERE idx  = %s;" %(idx))
            (loc,) = self.cur.fetchone()
            return loc


    def write_data(self,data):
            s1 = 'kb_table'
            s2 = '(field_team_id, field_team_name, field_team_skill, field_team_location, beacon_pkt_freq)'
            

            self.cur.execute("""INSERT INTO %s %s VALUES (%s, %s, %s, %s, %s, %s);""" %(s1,s2,
                                                                                        data[0],data[1],
                                                                                        data[2],data[3],
                                                                                        data[4]))




