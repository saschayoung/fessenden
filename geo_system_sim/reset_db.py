#!/usr/bin/env python

import MySQLdb

class reset_db:

    def __init__(self):
        pass


    def run(self):
        db = MySQLdb.connect(host = "128.173.90.70",
                             user = "sdrc_user",
                             passwd = "sdrc_pass",
                             db = "test01")


        print 'table = test01_table'
        table = 'test01_table'

        print 'cursor = db.cursor()'
        cursor = db.cursor()
        sql1 = "DROP TABLE IF EXISTS %s" % table
        cursor.execute (sql1)



        sql2 = """CREATE TABLE %s (idx INT, rpt_pkt_num INT, 
                                   rpt_team_id INT, rpt_location CHAR(50), 
                                   rpt_timestamp CHAR(50), beaon_id INT, 
                                   beacon_pkt_num INT)""" % table
        cursor.execute (sql2)


        cursor = db.cursor()
        sql3 = """CREATE INDEX idx ON %s(idx)""" % table
        cursor.execute (sql3)


        cursor.close () 
        db.close ()





if __name__=='__main__':
    main = reset_db()
    main.run()

