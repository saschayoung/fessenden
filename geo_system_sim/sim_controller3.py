#!/usr/bin/env python

import numpy as np
import time, random
import sys, os, struct, socket
import psycopg2

import test_coords
import alex_random
import sim_utils

from geo_utils import geo_utils
from beacon import beacon
from sim_data import data_utils


class simulation:

    def __init__(self):
        """__init__"""

        self.geo_utils = geo_utils()
        
        self.data = data_utils()
        
        self.DEBUG = True
        self.rx_number = 4
        self.packet_number = 0




    def init_sim(self,n):
        """
        initialize simulation for n receivers.
        """
        if n < 3:
            print 'Number of receivers %i is less than three.' %n
            print 'Simulation controller will not run.'
            print 'Now exiting.'
            sys.exit()
        
        self.data.set_rx_number(n)

        self.beacon = beacon()

        tx_loc = test_coords.get_tx_coords()
        self.data.set_tx_location(tx_loc)

        for i in range(n):
            rx_loc = alex_random.get_random_coord()
            self.data.set_rx_location(rx_loc)

            tof = self.geo_utils.time_of_flight(rx_loc,tx_loc)
            self.data.set_rx_time_delay(tof)

            id = i+1
            self.data.set_rx_team_id(id)

            if self.DEBUG:
                print 'tx_loc: ', tx_loc
                print 'rx_loc: ', rx_loc
                print 'time: ', repr(tof)
                print 'id: ', id


    def rx_beacon_packet(self):
        """
        receive a single beacon packet. this will then be copied n times.
        this tries to ensure clock synchronization across receivers.
        """        
        self.beacon.make_packet()
        rx_packet = self.beacon.tx_packet()
        rx_time = np.float128('%.20f'%(time.time()))
        print 'rx_time: ', repr(rx_time)

        self.data.set_timestamp_base(rx_time)
        self.data.set_beacon_packet(rx_packet)


    def receiver_chain(self):
        """
        simulate receiver chain for n repeaters
        """
        n = self.data.get_rx_number()
        beacon_packet = self.data.get_beacon_packet()
        time_base = self.data.get_timestamp_base()

        # lists containing data for all current teams
        team_id = self.data.get_rx_team_id()
        location = self.data.get_rx_location()
        tof = self.data.get_rx_time_delay()
        print "type(tof): ", type(tof)


        HOST = 'localhost'    # The remote host
        PORT = 1079           # The same port as used by the server


        for i in range(n):

            (rx_pktno,) = struct.unpack('!H', beacon_packet[0:2])
            (beacon_ID,) = struct.unpack('!H', beacon_packet[2:4])
            
            payload1 = struct.pack('!H', self.packet_number & 0xffff)

            id = team_id[i]
            payload2 = struct.pack('!H', id & 0xffff)

            loc = location[i]
            payload3 = sim_utils.pack_loc(loc)

            t = tof[i]
            print "t = tof[i]: ", repr(t)
            print "type(t): ", type (t)
            
            toa = time_base + t
            print "toa = time_base + t: ", repr(toa)
            print "type(toa): ", type(toa)
            payload4 = sim_utils.pack_time(toa)

            payload5 = struct.pack('!H', rx_pktno & 0xffff)
            payload6 = struct.pack('!H', beacon_ID & 0xffff)

            payload = (payload1 + payload2 +
                       payload3 + payload4 +
                       payload5 + payload6)

            conn = psycopg2.connect(host = "192.168.42.200",
                                    user = "sdrc_user",
                                    password = "sdrc_pass",
                                    database = "sdrc_db")


            cur = conn.cursor()


            cur.execute("INSERT INTO blob_table (field_1) VALUES (%s)", (psycopg2.Binary(payload),))


            conn.commit()
            cur.close() 
            conn.close()



            # don't use, adbapi can't handle too many db connections...
#             #self.data.set_rpt_packet(payload)
#             sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             sys.stdout.write("sock.connect((HOST, PORT))  ...")
#             sock.connect((HOST, PORT))
#             sys.stdout.write("  Done\n")
#             sys.stdout.write("sock.send...")
#             sock.send('%s\r\n' % payload)
#             sys.stdout.write("  Done\n")
#             sock.close()

        self.packet_number += 1
        
        

    # # don't use if using sockets above
    # def write_to_db(self):
        
    #     data = self.data.get_rpt_packet()

    #     print 'conn = MySQLdb.connect'
    #     db = MySQLdb.connect (host = "localhost",
    #                           user = "sdrc_user",
    #                           passwd = "sdrc_pass",
    #                           db = "test01")
    #     print 'cursor = conn.cursor ()'
    #     cursor = db.cursor ()

    #     table = 'test01_table'
    #     fields = '(rpt_pkt_num, rpt_team_id, rpt_location, rpt_timestamp, beacon_id, beacon_pkt_num)'

    #     # reset database
    #     cursor.execute("""DELETE FROM %s""" %(table,))
        

    #     for i in range(len(data)):
    #         sql = """ """
    #         print "loop: ",i
    #         payload = data[i]
    #         (rpt_packet_num,) = struct.unpack('!H',payload[0:2])
    #         (rpt_team_id,) = struct.unpack('!H',payload[2:4])
    #         rpt_location = sim_utils.unpack_loc(payload[4:24])
    #         rpt_timestamp = sim_utils.unpack_time(payload[24:36])
    #         (beacon_packet_num,) = struct.unpack('!H',payload[36:38])
    #         (beacon_id,) = struct.unpack('!H',payload[38:40])


    #         print type(beacon_id)



    #         sql = """INSERT INTO %s %s VALUES (\'%d\', \'%d\', \'%s\', \'%s\', \'%d\', \'%d\')""" %(table,fields,rpt_packet_num,
    #                                                                                     rpt_team_id,str(rpt_location),
    #                                                                                     repr(rpt_timestamp),beacon_id,
    #                                                                                     beacon_packet_num)

    #         print sql

    #         print 'cursor.execute(sql)'
    #         cursor.execute(sql)

    #         print 'db.commit()'
    #         db.commit()


    #     print 'db.close()'
    #     db.close()






    def send_rpt_packet(self):
        """
        transmit repeater packets
        """
        pass








                
                


    def run(self):
        """
        run.
        """
        pass

    def work(self):
        """
        work function.
        """
        pass

    def __str__(self):
        """
        Print data in class: simulation
        """
        string = '\n########\nSimulation START\n'
        string += 'tx_location: ' + repr(self.data.get_tx_location()) + '\n'
        string += 'rx_location: ' + repr(self.data.get_rx_location()) + '\n'
        string += 'rx_time_delay: ' + repr(self.data.get_rx_time_delay()) + '\n'
        string += 'rx_team_id: ' + str(self.data.get_rx_team_id()) + '\n'
        string += 'rpt_packet: ' + str(self.data.get_rpt_packet())
        string += '########\nSimulation END\n'
        return string
        







if __name__=='__main__':
    main = simulation()
    main.init_sim(3)
    for i in range(20):
        main.rx_beacon_packet()
        main.receiver_chain()









#         print main
#    main.write_to_db()
    

#             # not sure if we need this here
#             dist = self.geo_utils.distance(__tx_loc,__rx_loc)
#             self.__set_rx_distance(__dist)

#             __power = sim_utils.power(__dist)
#             self.set_rx_power(__power)


#     def add_receiver(self):
#         """
#         add additional receiver to simulation
#         """
#         pass

#     # do we really need this? don't think so...
#     def copy_beacon_packet(self):
#         """
#         make n copies of beacon packet
#         """
#         num = self.get_rx_number()
#         beacon_packet = self.get_beacon_packet()

#         for i in range(__num):
#             self.set_n_beacon_packet(__beacon_packet)


#             Prepare SQL query to INSERT a record into the database.
#        try:
#         Execute the SQL command
#         Commit your changes in the database
#         except:
#            # Rollback in case there is any error
#             print 'db.rollback()'
#             db.rollback()

#         # disconnect from server


            # cursor = db.cursor ()

            # table = 'blob_table'
            # fields = '(field_1)'



            # sql = """INSERT INTO %s %s VALUES (\'%\r')""" %(table,fields,payload)

            # print str(sql)

            # print 'cursor.execute(sql)'
            # cursor.execute(sql)

            # print 'db.commit()'
            # db.commit()

            # db.close()
