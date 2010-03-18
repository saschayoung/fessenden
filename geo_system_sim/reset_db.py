import MySQLdb

class reset_db:

    def __init__(self):
        pass


    def run(self):
        db = MySQLdb.connect(host = "localhost",
                             user = "sdrc_user",
                             passwd = "sdrc_pass",
                             db = "test01")

        cursor = db.cursor()

        table = 'test01_table'
        
        
        sql = """DROP TABLE %s""" % table
        cursor.execute (sql)

        sql = """CREATE TABLE %s(index INT AUTO_INCREMENT, rpt_pkt_num INT, 
                 rpt_team_id INT, rpt_location CHAR(50),
                 rpt_timestamp CHAR(50), beaon_id INT, beacon_pkt_num INT)%s""" % table
        cursor.execute (sql)


        sql = """CREATE INDEX index ON %s(index)""" % table
        cursor.execute (sql)


        cursor.close ()
        db.close ()





if __name__=='__main__':
    main = reset_db()
    main.run()

