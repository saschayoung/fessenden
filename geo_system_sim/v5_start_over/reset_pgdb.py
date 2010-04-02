#!/usr/bin/env python




import psycopg2



class reset_db:

    def __init__(self):
        pass


    def run(self,h):
        self.host = options.host
        conn = psycopg2.connect(host = self.host,
                                user = "sdrc_user",
                                password = "sdrc_pass",
                                database = "sdrc_db")


        cur = conn.cursor()



        # # cur.execute("DROP TABLE IF EXISTS %s;" % 'blob_table')
        # cur.execute("DROP TABLE IF EXISTS %s;" % 'binary_data_table')
        # cur.execute("CREATE TABLE binary_data_table (idx serial PRIMARY KEY, binary_data bytea);")


        # # cur.execute("DROP TABLE IF EXISTS %s;" % 'data_table')
        # cur.execute("DROP TABLE IF EXISTS %s;" % 'hrf_data_table')
        # cur.execute("""CREATE TABLE hrf_data_table (idx serial PRIMARY KEY, 
        #                                         field_team_pkt_num INT, 
        #                                         field_team_id INT, 
        #                                         field_team_location CHAR(50), 
        #                                         field_team_time CHAR(50), 
        #                                         beacon_pkt_num INT,
        #                                         beacon_id INT);""")

        cur.execute("DROP TABLE IF EXISTS %s;" % 'geolocation_table')
        cur.execute("""CREATE TABLE geolocation_table (idx serial PRIMARY KEY, 
                                                hist_box1_c1 char(50), 
                                                hist_box1_c2 char(50), 
                                                hist_box2_c1 char(50), 
                                                hist_box2_c2 char(50), 
                                                hist_box3_c1 char(50), 
                                                hist_box3_c2 char(50), 
                                                guess CHAR(50),
                                                time CHAR(20));""")

        cur.execute("DROP TABLE IF EXISTS %s;" % 'kb_table')
        cur.execute("""CREATE TABLE kb_table (idx serial PRIMARY KEY, 
                                                field_team_id INT, 
                                                field_team_name CHAR(50), 
                                                field_team_skill CHAR(50), 
                                                field_team_location CHAR(50),
                                                field_team_freq FLOAT,
                                                time CHAR(20));""")


        conn.commit()
        cur.close() 
        conn.close()





if __name__=='__main__':
    from optparse import OptionParser
    usage = "usage: %prog [options] arg"

    parser = OptionParser(usage=usage)
    parser.add_option("", "--host", type="string", default="128.173.90.88",
                      help="database host in dotted decimal form [default=%default]")

    (options, args) = parser.parse_args()
    
    # if len(args) != 1:
    #     parser.error("incorrect number of arguments")
    #     parser.print_help()
    #     sys.exit(1)

    main = reset_db()
    main.run(options)

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
