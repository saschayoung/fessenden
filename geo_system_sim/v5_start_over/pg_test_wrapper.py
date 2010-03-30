#!/usr/bin/env python


import struct

import psycopg2
import numpy as np

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


        #insert test code here
        # f = open('data_out.data','w+')

        beacon_packet_number = 11
        cur.execute("SELECT idx FROM data_table WHERE beacon_pkt_num = %s;" %(beacon_packet_number,))
        result = cur.fetchall()
        print result
        if ( result == [] ):
            print 'result == []'



        # # result comes back from cur.fetchall() like this: [(7,), (8,), (9,)]
        # # turn it into this: [7, 8, 9]
        # for i in range(len(result)):
        #     (result[i],) = result[i]
        # #endfor
        # print result


        # # get the max value of the index
        # cur.execute("SELECT MAX(idx) FROM data_table;" )
        # (max_index,) = cur.fetchone()
        # print "result: ", max_index

        # # # check that what went into the database is what comes out
        # # for i in range(max_index):
        # #     cur.execute("SELECT * FROM data_table WHERE idx = %s;" %(i+1,))
        # #     (index,pkt_num,team_id,loc,t,beacon_id,beacon_pkt_num) = cur.fetchone()
        # #     loc = loc.strip(' ()')
        # #     loc = loc.split(',')
        # #     loc[0] = np.float128(loc[0])
        # #     loc[1] = np.float128(loc[1])

        # #     t = t.strip(' ')
        # #     t = t[4:]
        # #     t = np.float128(t)

        # #     f.write(str(pkt_num) + ';' + str(team_id) + ';' + repr(loc) + ';' + repr(t) + ';' + 
        # #             str(beacon_id) + ';' + str(beacon_pkt_num) + '\n')
        # #     print "result: ", index,pkt_num,team_id,repr(loc),repr(t),beacon_id,beacon_pkt_num
        # # #endfor

        # # f.close()
        conn.commit()
        cur.close() 
        conn.close()


# 1285752659
# 12857526587322

# 1269955491.128575325
#    1209600
#     604800
if __name__=='__main__':
    from optparse import OptionParser
    usage = "usage: %prog [options] arg"

    parser = OptionParser(usage=usage)
    parser.add_option("", "--host", type="string", default="128.173.90.88",
                      help="database host in dotted decimal form [default=%default]")

    (options, args) = parser.parse_args()
    
    # if len(args) != 1:
    #     parser.error("incorrect number of arguments")

    main = reset_db()
    main.run(options.host)

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
