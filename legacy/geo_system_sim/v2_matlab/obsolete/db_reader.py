import MySQLdb

class db_reader:

    def __init__(self):
        self.n = 5


    def get_data(self):
        db = MySQLdb.connect(host = "localhost",
                             user = "sdrc_user",
                             passwd = "sdrc_pass",
                             db = "test01")

        cursor = db.cursor()

        table = 'test01_table'
        fields = '(rpt_pkt_num, rpt_team_id, rpt_location, rpt_timestamp, beacon_id, beacon_pkt_num)'
        
        sql = """SELECT %s  FROM %s WHERE beacon_pkt_num = %s""" %(fields, table, self.n)
        cursor.execute (sql)

        result = cursor.fetchall()
        cursor.close ()
        db.close ()

#         if len(result) < 3:
#             print "error, not enough unique repeater packets for beacon packet number %d" % n



        print "result of database query:"
        print result
        print "len(result): ", len(result)

if __name__=='__main__':
    main = db_reader()
    main.get_data()








#!/usr/bin/env python

# import MySQLdb
# import numpy as np


# #import MySQLdb
# from twisted.enterprise import adbapi
# from twisted.internet import reactor

# dbpool = adbapi.ConnectionPool("MySQLdb",
#                                host = "localhost",
#                                user = "sdrc_user",
#                                passwd = "sdrc_pass",
#                                db = "test01")

# def get_location(id):
#     return dbpool.runQuery("SELECT * FROM test01_table WHERE beacon_pkt_num = 5")

# def printResult(l):
#     if l:
#         print "result: ", l
#         print "type(result): ", type(l)
#         print "len(result): ", len(l)
#     else:
#         print "not found"

# get_location(1).addCallback(printResult)

# reactor.callLater(4, reactor.stop)
# reactor.run()








# import MySQLdb
# import sys, struct
# import numpy as np

# from twisted.enterprise import adbapi
# from twisted.internet import protocol, reactor, defer, utils
# from twisted.protocols import basic

# # local imports
# import sim_utils

# class dbReaderProtocol(basic.LineReceiver):

#     def __init__(self):
#         #self.setRawMode()
#         pass
        
#     def lineReceived(self, data):
#         d = self.factory.runQuery(data)

#         # def onError(err):
#         #     return 'Internal server error'
#         # d.addErrback(onError)

#         def returnResult(message):
#             self.transport.write(str(message) + '\r\n')
#             self.transport.loseConnection()
#         d.addCallback(writeResponse)

        

# class dbReaderFactory(protocol.ServerFactory):
#     protocol = dbReaderProtocol

#     def __init__(self):
#         pass

#     def parseData(self,payload):
#         (self.rpt_packet_num,) = struct.unpack('!H',payload[0:2])
#         (self.rpt_team_id,) = struct.unpack('!H',payload[2:4])
#         self.rpt_location = sim_utils.unpack_loc(payload[4:24])
#         self.rpt_timestamp = sim_utils.unpack_time(payload[24:36])
#         (self.beacon_packet_num,) = struct.unpack('!H',payload[36:38])
#         (self.beacon_id,) = struct.unpack('!H',payload[38:40])



#     def writeData(self, data):
#         self.parseData(data)
        
#         dbpool = adbapi.ConnectionPool("MySQLdb",
#                                        host = "localhost",
#                                        user = "sdrc_user",
#                                        passwd = "sdrc_pass",
#                                        db = "test01")


#         table = 'test01_table'
#         fields = '(rpt_pkt_num, rpt_team_id, rpt_location, rpt_timestamp, beacon_id, beacon_pkt_num)'


#         sql = """INSERT INTO %s %s VALUES (\'%d\', \'%d\', \'%s\', \'%s\', \'%d\', \'%d\')""" %(table,fields,
#                                                                                                 self.rpt_packet_num,
#                                                                                                 self.rpt_team_id,
#                                                                                                 repr(self.rpt_location),
#                                                                                                 repr(self.rpt_timestamp),
#                                                                                                 self.beacon_id,
#                                                                                                 self.beacon_packet_num)


#         return dbpool.runQuery(sql)

# reactor.listenTCP(1079, dbReaderFactory())
# reactor.run()

