#!/usr/bin/env python

import MySQLdb

class reset_db:

    def __init__(self):
        pass


    def run(self):
        db = MySQLdb.connect(host = "localhost",
                             user = "sdrc_user",
                             passwd = "sdrc_pass",
                             #db = "test01")
                             db = "blob_test")


        table1 = 'blob_table'
        table2 = 'data_table'

        cursor = db.cursor()

        sql = "DROP TABLE IF EXISTS %s" % table1
        cursor.execute (sql)

        sql = "DROP TABLE IF EXISTS %s" % table2

        cursor.execute (sql)


        sql = """CREATE TABLE %s (idx INT NOT NULL AUTO_INCREMENT, field_1 BINARY(128), INDEX (idx))"""  % table1
        cursor.execute (sql)

        sql = """CREATE TABLE %s (idx INT NOT NULL AUTO_INCREMENT, rpt_pkt_num INT, 
                                   rpt_team_id INT, rpt_location CHAR(50), 
                                   rpt_timestamp CHAR(50), beacon_id INT, 
                                   beacon_pkt_num INT, INDEX (idx))""" % table2
        cursor.execute (sql)


#         sql3 = """CREATE INDEX idx ON %s(idx)""" % table
#         cursor.execute (sql3)




#         table = 'test01_table'

#         cursor = db.cursor()
#         sql1 = "DROP TABLE IF EXISTS %s" % table
#         cursor.execute (sql1)






#         sql3 = """CREATE INDEX idx ON %s(idx)""" % table
#         cursor.execute (sql3)


        cursor.close () 
        db.close ()





if __name__=='__main__':
    main = reset_db()
    main.run()

