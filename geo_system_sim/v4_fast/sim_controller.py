#!/usr/bin/env python

import numpy as np
import time, random
import sys, os, struct, socket
import psycopg2

import test_coords
import alex_random
import new_sim_utils
import sdr_kml_writer

from geo_utils import geo_utils
from beacon import beacon
from sim_data import data_utils

ENABLE_JITTER = False
ENABLE_DROPPED_PACKETS = False
ENABLE_LOCATION_HISTORY = True
ENABLE_BEACON_DELAY = False


class simulation:

    def __init__(self):
        """__init__"""

        self.geo_utils = geo_utils()
        
        
        
        self.DEBUG = True
        self.rx_number = 4
        self.packet_number = 0

        self.iterator = 1
        self.packet_error_rate = 0.1
        self.all_locations = []



    def init_sim(self,n):
        """
        initialize simulation for n receivers.
        """
        self.beacon = beacon(ENABLE_BEACON_DELAY)
        self.data = data_utils(n)
        random.seed()

        if n < 3:
            print 'Number of receivers %i is less than three.' %n
            print 'Simulation controller will not run.'
            print 'Now exiting.'
            sys.exit()
        
        self.data.set_rx_number(n)



        tx_loc = test_coords.get_tx_coords()
        self.data.set_tx_location(tx_loc)
        # self.data.reset_rx_location()

        for i in range(n):
            rx_loc = alex_random.get_random_coord()
            if self.DEBUG:
                print "\n\n\n\n\n\nstore location: ", rx_loc
                print '\n\n\n\n\n\n'
            self.data.set_rx_location(i,rx_loc)

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
        if self.DEBUG:
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
        if ENABLE_LOCATION_HISTORY:
            self.record_location_history(location)
        tof = self.data.get_rx_time_delay()

        if self.DEBUG:
            print "\n\n\n\n\n\nretrieve location: ", location
            print ''
            print "type(tof): ", type(tof)


        HOST = 'localhost'    # The remote host
        PORT = 1079           # The same port as used by the server

        # conn = psycopg2.connect(host = "192.168.42.200",
        #                         user = "sdrc_user",
        #                         password = "sdrc_pass",
        #                         database = "sdrc_db")

        conn = psycopg2.connect(host = "128.173.90.88",
                                user = "sdrc_user",
                                password = "sdrc_pass",
                                database = "sdrc_db")

        cur = conn.cursor()


        for i in range(n):
            f = open('data_in.data', 'a')

            (rx_pktno,) = struct.unpack('!H', beacon_packet[0:2])
            (beacon_ID,) = struct.unpack('!H', beacon_packet[2:4])

            # packet number
            payload1 = struct.pack('!H', self.packet_number & 0xffff)
            f.write(str(self.packet_number) + ';')

            # team id
            ident = team_id[i]
            payload2 = struct.pack('!H', ident & 0xffff)
            f.write(str(ident) + ';')

            # location
            if (self.iterator == 1):
                loc = location[i]
            else:
                # old_loc = location[i]
                # loc = alex_random.random_move(old_loc)
                loc = alex_random.get_random_coord()
                self.data.set_rx_location(i,loc)

            f.write(str(loc)+';')

            self.iterator += 1
            payload3 = new_sim_utils.pack_loc(loc)
            

            # toa
            t = tof[i]
            toa = time_base + t
            # if (ENABLE_JITTER):
            #     jitter = self.random_timing_jitter()
            #     toa = toa+jitter
            # else:
            #     pass
            if self.DEBUG:
                print "t = tof[i]: ", repr(t)
                print "type(t): ", type (t)
                print "toa = time_base + t: ", repr(toa)
                print "type(toa): ", type(toa)
            payload4 = new_sim_utils.pack_time(toa)

            f.write(repr(toa)+';')


            # beacon payload
            payload5 = struct.pack('!H', rx_pktno & 0xffff)
            f.write(str(rx_pktno) + ';')
            payload6 = struct.pack('!H', beacon_ID & 0xffff)
            f.write(str(beacon_ID) + '\n')
            f.close()
            # check if packet dropped
            drop = self.drop_packet()
            # this if evaluates true even if drop == False
            # if (ENABLE_DROPPED_PACKETS and drop): # if drop == 'True'
            #     print 'ENABLE_DROPPED_PACKETS ', ENABLE_DROPPED_PACKETS
            #     print 'drop ', drop
            #     print (ENABLE_DROPPED_PACKETS and drop)
            #     print 'packet dropped'
            #     payload = ''
            if ENABLE_DROPPED_PACKETS:
                print 'ENABLE_DROPPED_PACKETS ', ENABLE_DROPPED_PACKETS
                print 'drop ', drop
                if drop: # if drop == 'True'
                    print 'drop ', drop
                    print 'packet dropped'
                    payload = ''
                else:    # if drop == 'False'
                    payload = (payload1 + payload2 +
                               payload3 + payload4 +
                               payload5 + payload6)
            else:    # if drop == 'False'
                payload = (payload1 + payload2 +
                           payload3 + payload4 +
                           payload5 + payload6)


            print "len(payload): ", len(payload)
            cur.execute("INSERT INTO blob_table (field_1) VALUES (%s)", (psycopg2.Binary(payload),))


        conn.commit()
        cur.close() 
        conn.close()

        self.packet_number += 1
        


    def record_location_history(self,loc):
        self.all_locations.append(loc)
        # if self.DEBUG:
        #     print 'all locations:\n', self.all_locations

    # def write_location_history(self):
    #     # f = open('location_history','w+')
    #     for i in self.all_locations:
    #         print repr(i[0][0][0]), repr(i[0][0][1]))
    #         # f.write(repr(i)+'\n')
    #         print '\n\n\n\n\n\n\n'
    #         print len(i)
    #     # f.close()

        # kml_write = sdr_kml_writer.kml_writer()

        # for i in range(0,len(x_results)):
        #     coord = str(x_results[i])+','+str(y_results[i])
        #     kml_write.add_placemark('','',coord)
        # kml_write.write_to_file('geoloc_kml_file.kml')        


    def random_timing_jitter(self):
        r = random.uniform(0,1)
        jitter = r*1e-9
        if self.DEBUG:
            print 'Random timing jitter %f seconds' %(jitter)
        return jitter



    def drop_packet(self):
        r = random.uniform(0,1)
        print 'random value: ', r
        print 'error rate: ', self.packet_error_rate
        if (r > self.packet_error_rate):
            
            drop = False
        else:
            drop = True
        if self.DEBUG:
            print 'Probability of dropped packet: ', self.packet_error_rate
            print 'Packet dropped?  ', drop
        return drop
        
        




if __name__=='__main__':
    main = simulation()
    main.init_sim(3)
    for i in range(10):
        
        main.rx_beacon_packet()
        main.receiver_chain()
#     main.write_location_history()




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
    #         rpt_location = new_sim_utils.unpack_loc(payload[4:24])
    #         rpt_timestamp = new_sim_utils.unpack_time(payload[24:36])
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






    # def send_rpt_packet(self):
    #     """
    #     transmit repeater packets
    #     """
    #     pass








                
                


    # def run(self):
    #     """
    #     run.
    #     """
    #     pass

    # def work(self):
    #     """
    #     work function.
    #     """
    #     pass

    # def __str__(self):
    #     """
    #     Print data in class: simulation
    #     """
    #     string = '\n########\nSimulation START\n'
    #     string += 'tx_location: ' + repr(self.data.get_tx_location()) + '\n'
    #     string += 'rx_location: ' + repr(self.data.get_rx_location()) + '\n'
    #     string += 'rx_time_delay: ' + repr(self.data.get_rx_time_delay()) + '\n'
    #     string += 'rx_team_id: ' + str(self.data.get_rx_team_id()) + '\n'
    #     string += 'rpt_packet: ' + str(self.data.get_rpt_packet())
    #     string += '########\nSimulation END\n'
    #     return string
        







#         print main
#    main.write_to_db()
    

#             # not sure if we need this here
#             dist = self.geo_utils.distance(__tx_loc,__rx_loc)
#             self.__set_rx_distance(__dist)

#             __power = new_sim_utils.power(__dist)
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
