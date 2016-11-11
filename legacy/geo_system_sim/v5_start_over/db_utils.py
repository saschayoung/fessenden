#!/usr/bin/env python

# core libraries
import time
from types import NoneType

# external libraries
import psycopg2
import numpy as np

# class hrf_data_table:
#     """
#     Database access and manipulation tools for hrf_data_table
#     """

#     def __init__(self, host):
#         self.host = host
        

#     def start_db(self):
#         self.conn = psycopg2.connect(host = self.host,
#                                      user = "sdrc_user",
#                                      password = "sdrc_pass",
#                                      database = "sdrc_db")
#         self.cur = self.conn.cursor()

#     def stop_db(self):
#         # conn.commit() <- is this needed?
#         self.cur.close() 
#         self.conn.close()

#     def get_end(self):
#         self.cur.execute("SELECT MAX(idx) FROM geolocation_table;")
#         (idx,) = self.cur.fetchone()
#         return idx

#     def get_start(self):
#         self.cur.execute("SELECT MIN(idx) FROM geolocation_table;")
#         (idx,) = self.cur.fetchone()
#         return idx

#     def get_data(self,idx):
#         self.cur.execute("SELECT * FROM geolocation_table WHERE idx = %s;" %(idx,))
#         r = self.cur.fetchone()
#         if ( type(r) is NoneType ):
#             self.stop_db()
#             return -1
#         else:
#             (index, hist_box1_c1, hist_box1_c2, hist_box2_c1, 
#              hist_box3_c2, hist_box3_c1, hist_box3_c2, guess, time) = r
#             r = r[1:]
#             return r


#     def write_data(self,data):
#             s1 = 'geolocation_table'
#             s2 = '(hist_box1_c1, hist_box1_c2, hist_box2_c1, hist_box2_c2, hist_box3_c1, hist_box3_c2, guess, time)'
#             t = time.localtime()
#             t = psycopg2.Time(t[3], t[4], t[4]) 

#             self.cur.execute("""INSERT INTO %s %s VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""" %(s1,s2,
#                                                                                                 data[0],data[1],data[2],
#                                                                                                 data[3],data[4],data[5],
#                                                                                                 data[6],t))

#             self.conn.commit()



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

    def get_end(self):
        self.cur.execute("SELECT MAX(idx) FROM geolocation_table;")
        (idx,) = self.cur.fetchone()
        return idx

    def get_start(self):
        self.cur.execute("SELECT MIN(idx) FROM geolocation_table;")
        (idx,) = self.cur.fetchone()
        return idx

    def get_data(self,idx):
        self.cur.execute("SELECT * FROM geolocation_table WHERE idx = %s;" %(idx,))
        r = self.cur.fetchone()
        if ( type(r) is NoneType ):
            self.stop_db()
            return -1
        else:
            (index, hist_box1_c1, hist_box1_c2, hist_box2_c1, 
             hist_box3_c2, hist_box3_c1, hist_box3_c2, guess, time) = r
            r = r[1:]
            return r


    def write_data(self,data):
            s1 = 'geolocation_table'
            s2 = '(hist_box1_c1, hist_box1_c2, hist_box2_c1, hist_box2_c2, hist_box3_c1, hist_box3_c2, guess, time)'
            t = time.localtime()
            t = psycopg2.Time(t[3], t[4], t[4]) 

            self.cur.execute("""INSERT INTO %s %s VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""" %(s1,s2,
                                                                                                data[0],data[1],data[2],
                                                                                                data[3],data[4],data[5],
                                                                                                data[6],t))

            self.conn.commit()


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

    def get_team_locations(self,l):
        loc_now = []
        for i in l:
            self.cur.execute("SELECT MAX(idx) FROM hrf_data_table WHERE field_team_id = %s;" %(i,))
            (idx,) = self.cur.fetchone()
            self.cur.execute("SELECT field_team_location FROM hrf_data_table WHERE idx  = %s;" %(idx,))
            (loc,) = self.cur.fetchone()
            loc = loc.strip(' ()')        # format location
            loc = loc.split(',')
            loc[0] = np.float128(loc[0])
            loc[1] = np.float128(loc[1])
            loc_now.append(loc)
        return loc_now




    def write_data(self,data):
        s1 = 'kb_table'
        s2 = '(field_team_id, field_team_name, field_team_skill, field_team_location, field_team_freq, time)'
        t = time.localtime()
        t = psycopg2.Time(t[3], t[4], t[4]) 


        self.cur.execute("""INSERT INTO %s %s VALUES (%s, %s, %s, %s, %s, %s, %s);""" %(s1,s2,
                                                                                        data[0],data[1],
                                                                                        data[2],data[3],
                                                                                        data[4]),t)
        
        self.conn.commit()
            


class movement_table:
    """
    Database access and manipulation tools for movement_table
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

    def get_end(self):
        self.cur.execute("SELECT MAX(idx) FROM movement_table;")
        (idx,) = self.cur.fetchone()
        return idx


    def get_data(self,idx):
        self.cur.execute("SELECT * FROM movement_table WHERE idx = %s;" %(idx,))
        r = self.cur.fetchone()
        if ( type(r) is NoneType ):
            self.stop_db()
            return -1
        else:
            # (index, box_c1, box_c2, target) = r
            r = r[1:]
            c1 = r[0].strip(' ()')
            c1= c1.split(',')
            c1[0] = np.float128(c1[0])
            c1[1] = np.float128(c1[1])

            c2 = r[1].strip(' ()')
            c2 = c2.split(',')
            c2[0] = np.float128(c2[0])
            c2[1] = np.float128(c2[1])

            target = r[2].strip(' ()')
            target = target.split(',')
            target[0] = np.float128(target[0])
            target[1] = np.float128(target[1])

            data = [c1,c2,target]
            return data


    def write_data(self,data):
            s1 = 'movement_table'
            s2 = '(box_c1, box_c2, target)'

            self.cur.execute("""INSERT INTO %s %s VALUES (%s, %s, %s);""" %(s1,s2,data[0],data[1],data[2]))

            self.conn.commit()
