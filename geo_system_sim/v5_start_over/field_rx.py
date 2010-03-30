#!/usr/bin/env python

# core libraries
import struct, sys

# external libraries
import psycopg2

# local imports
import pack_utils
import sim_utils
import location_alexandria
import test_coords
from geo_utils import geo_utils

DEBUG = True


def update(iteration):
    sys.stdout.write("Working... iteration: %3d\r" % iteration)
    sys.stdout.flush()



class simulation:
    def __init__(self,options):
        self.host = options.host

    def start_db(self):
        self.conn = psycopg2.connect(host = self.host, user = "sdrc_user",
                                     password = "sdrc_pass", database = "sdrc_db")
        self.cur = self.conn.cursor()

    def stop_db(self):
        self.cur.close()
        self.conn.close()

    def write_db(self,payload):
        self.cur.execute("INSERT INTO binary_data_table (binary_data) VALUES (%s)", (psycopg2.Binary(payload),))
        self.conn.commit()




    def run(self):
        self.start_db()
        g = geo_utils()

        tx = test_coords.get_tx_coords()
        
        field_radios = options.radios
        iterations = options.iterations

        update_status = 0
        for i in range(iterations):
            ii = i + 1  # beacon pkt num
            jj = i + 1  # field team pkt num

            # this part simulates the beacon transmission
            ####################################################################
            beacon_pkt_num = ii
            beacon_id = 42
            b1 = struct.pack('!i', beacon_pkt_num)
            b2 = struct.pack('!i', beacon_id)
            beacon_payload = b1+b2
            ####################################################################

            for k in range(field_radios):
                kk = k + 1  # team id

                # this part simulates the field team re-transmission
                ################################################################
                # set the values
                field_radio_pkt_num = ii
                field_team_id = kk
                field_team_loc = location_alexandria.get_random_coord()
                field_team_time = sim_utils.time_of_flight(tx,field_team_loc)
                # pack the values
                f1 = struct.pack('!i', field_radio_pkt_num)
                f2 = struct.pack('!i', field_team_id)
                f3 = pack_utils.pack_loc(field_team_loc)
                f4 = pack_utils.pack_time(field_team_time)
                # build the payload
                field_team_payload = f1 + f2 + f3 + f4 + beacon_payload

                # (_field_radio_pkt_num,) = struct.unpack('!i',field_team_payload[0:4])        
                # (_field_team_id,) = struct.unpack('!i',field_team_payload[4:8])
                # _field_team_loc = pack_utils.unpack_loc(field_team_payload[8:32])
                # _field_team_time = pack_utils.unpack_time(field_team_payload[32:44])
                # (_beacon_pkt_num,) = struct.unpack('!i',field_team_payload[44:48])
                # (_beacon_id,) = struct.unpack('!i',field_team_payload[48:52])


                
                # print field_radio_pkt_num
                # print _field_radio_pkt_num
                # print field_team_id
                # print _field_team_id
                # print field_team_loc
                # print _field_team_loc
                # print field_team_time
                # print _field_team_time


                # sys.exit(1)
                # send the payload to hq
                self.write_db(field_team_payload)
                ################################################################
                update_status += 1
            #endfor
            update(update_status)
        #endfor
        self.stop_db()






if __name__=='__main__':
    from optparse import OptionParser
    usage = "usage: %prog [options] arg"

    parser = OptionParser(usage=usage)
    parser.add_option("", "--host", type="string", default="128.173.90.88",
                      help="database host in dotted decimal form [default=%default]")
    parser.add_option("-r", "--radios", type="int", default="3",
                      help="number of field radios to simulate [default=%default]")
    parser.add_option("-i", "--iterations", type="int", default="1000",
                      help="number of times to run simulation [default=%default]")
    # parser.add_option("-d", "--drop", action="store_true", default=False,
    #                   help="simlulate dropped packets [default=%default]")
    # parser.add_option("-j", "--jitter", type="store_true", default=False,
    #                   help="simulate clock jitter, drift... [default=%default]")

    (options, args) = parser.parse_args()

    sim = simulation(options)
    sim.run()
