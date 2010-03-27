#!/usr/bin/env python

import psycopg2

import struct

class reset_db:

    def __init__(self):
        pass


    def run(self):
        conn = psycopg2.connect(host = "192.168.42.200",
                                user = "sdrc_user",
                                password = "sdrc_pass",
                                database = "sdrc_db")


        cur = conn.cursor()


        #insert test code here




        conn.commit()
        cur.close() 
        conn.close()





if __name__=='__main__':
    main = reset_db()
    main.run()

       # data = struct.pack('!H', 24 & 0xffff)

  
                  
        # cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
        
        # cur.execute("SELECT * FROM test;")
        # (result,) = cur.fetchone()
        # print "result: ", result
 
        # cur.execute("DROP TABLE IF EXISTS %s;" % 'blob_table')
        # cur.execute("CREATE TABLE blob_table (id serial PRIMARY KEY, field_1 bytea);")

        # cur.execute("DROP TABLE IF EXISTS %s;" % 'data_table')
        # cur.execute("""CREATE TABLE data_table (idx serial PRIMARY KEY, 
        #                                         rpt_pkt_num INT, 
        #                                         rpt_team_id INT, 
        #                                         rpt_location CHAR(50), 
        #                                         rpt_timestamp CHAR(50), 
        #                                         beacon_id INT, 
        #                                         beacon_pkt_num INT);""")


#         sql = """CREATE TABLE %s (idx SERIAL, rpt_pkt_num INT, 
#                                    rpt_team_id INT, rpt_location CHAR(50), 
#                                    rpt_timestamp CHAR(50), beacon_id INT, 
#                                    beacon_pkt_num INT, INDEX (idx))""" % table2
#         cursor.execute (sql)


#         sql3 = """CREATE INDEX idx ON %s(idx)""" % table
#         cursor.execute (sql3)




#         table = 'test01_table'

#         cursor = db.cursor()
#         sql1 = "DROP TABLE IF EXISTS %s" % table
#         cursor.execute (sql1)






#         sql3 = """CREATE INDEX idx ON %s(idx)""" % table
#         cursor.execute (sql3)
