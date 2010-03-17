#!/usr/bin/env python

import MySQLdb
import sys, struct
import numpy as np

from twisted.enterprise import adbapi
from twisted.internet import protocol, reactor, defer, utils
from twisted.protocols import basic

# local imports
import sim_utils

class TestProtocol(basic.LineReceiver):

    def __init__(self):
        #self.setRawMode()
        pass
        
    def lineReceived(self, data):
        d = self.factory.writeData(data)

        # def onError(err):
        #     return 'Internal server error'
        # d.addErrback(onError)

        def writeResponse(message):
            self.transport.write(str(message) + '\r\n')
            self.transport.loseConnection()
        d.addCallback(writeResponse)

        

class TestFactory(protocol.ServerFactory):
    protocol = TestProtocol

    def __init__(self):
        pass

    def parseData(self,payload):
        (self.rpt_packet_num,) = struct.unpack('!H',payload[0:2])
        (self.rpt_team_id,) = struct.unpack('!H',payload[2:4])
        self.rpt_location = sim_utils.unpack_loc(payload[4:24])
        self.rpt_timestamp = sim_utils.unpack_time(payload[24:36])
        (self.beacon_packet_num,) = struct.unpack('!H',payload[36:38])
        (self.beacon_id,) = struct.unpack('!H',payload[38:40])



    def writeData(self, data):
        self.parseData(data)
        
        dbpool = adbapi.ConnectionPool("MySQLdb",
                                       host = "localhost",
                                       user = "sdrc_user",
                                       passwd = "sdrc_pass",
                                       db = "test01")


        table = 'test01_table'
        fields = '(rpt_pkt_num, rpt_team_id, rpt_location, rpt_timestamp, beacon_id, beacon_pkt_num)'


        sql = """INSERT INTO %s %s VALUES (\'%d\', \'%d\', \'%s\', \'%s\', \'%d\', \'%d\')""" %(table,fields,
                                                                                                self.rpt_packet_num,
                                                                                                self.rpt_team_id,
                                                                                                repr(self.rpt_location),
                                                                                                repr(self.rpt_timestamp),
                                                                                                self.beacon_id,
                                                                                                self.beacon_packet_num)


        return dbpool.runQuery(sql)

reactor.listenTCP(1079, TestFactory())
reactor.run()



#         text = 'fdajdljkf__woo_hoo'
#         print "INSERT INTO table01 (text) VALUES (\'%s\')" %(text,)
