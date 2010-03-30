#!/usr/bin/env python




import psycopg2



class reset_db:

    def __init__(self):
        pass


    def run(self,h):
        self.host = h
        conn = psycopg2.connect(host = self.host,
                                user = "sdrc_user",
                                password = "sdrc_pass",
                                database = "sdrc_db")


        cur = conn.cursor()



        cur.execute("DROP TABLE IF EXISTS %s;" % 'blob_table')
        cur.execute("CREATE TABLE blob_table (idx serial PRIMARY KEY, field_1 bytea);")

        cur.execute("DROP TABLE IF EXISTS %s;" % 'data_table')
        cur.execute("""CREATE TABLE data_table (idx serial PRIMARY KEY, 
                                                rpt_pkt_num INT, 
                                                rpt_team_id INT, 
                                                rpt_location CHAR(50), 
                                                rpt_timestamp CHAR(50), 
                                                beacon_id INT,
                                                beacon_pkt_num INT);""")


        conn.commit()
        cur.close() 
        conn.close()





if __name__=='__main__':
    from optparse import OptionParser
    usage = "usage: %prog [options] arg"

    parser = OptionParser(usage=usage)
    parser.add_option("", "--host", type="string", default="128.173.90.68",
                      help="database host in dotted decimal form [default=%default]")

    (options, args) = parser.parse_args()
    
    # if len(args) != 1:
    #     parser.error("incorrect number of arguments")
    #     parser.print_help()
    #     sys.exit(1)

    main = reset_db()
    main.run(options.host)

       # data = struct.pack('!H', 24 & 0xffff)
        # cur.execute("INSERT INTO blob_table (field_1) VALUES (%s)", (psycopg2.Binary(data),))
  
                  
        # cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
        
        # cur.execute("SELECT * FROM test;")
        # (result,) = cur.fetchone()
        # print "result: ", result
 


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
