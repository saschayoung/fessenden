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
        # self.options = options
        self.prev_loc = []

    # db access
    ############################################################################
    def start_db(self):

        self.conn = psycopg2.connect(host = options.host, user = "sdrc_user",
                                     password = "sdrc_pass", database = "sdrc_db")
        self.cur = self.conn.cursor()

    def stop_db(self):
        self.cur.close()
        self.conn.close()

    def write_db(self,payload):
        self.cur.execute("INSERT INTO binary_data_table (binary_data) VALUES (%s)", (psycopg2.Binary(payload),))
        self.conn.commit()
    ############################################################################

    def get_location(self,ii,kk):
        # add directed movement functionality here 
        if options.move:
            if ( ii == 1 ):  # first iteration
                loc = location_alexandria.get_random_coord()
                self.prev_loc.append(loc)
            else:
                loc = location_alexandria.random_move(self.prev_loc[kk-1])
                self.prev_loc[kk-1] = loc
        else:
            loc = location_alexandria.get_random_coord()

        return loc



    def run(self):
        # administrivia
        ########################################################################
        self.start_db()
        g = geo_utils()

        if ( options.backoff or options.drop ): 
            stoch = sim_utils.stochastics()            
            stoch.set_packet_error_rate(options.rate)
            stoch.set_max_delay(options.delay)

        tx = test_coords.get_tx_coords()
        
        field_radios = options.radios
        iterations = options.iterations
        
        update_status = 0
        ########################################################################


        
        
        for i in range(iterations):
            ii = i + 1  # beacon pkt num
            jj = i + 1  # field team pkt num

            # this part simulates the beacon transmission
            ####################################################################
            if ( not (ii == 1) and options.backoff ):
                stoch.backoff()
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
                field_team_loc = self.get_location(ii,kk)
                field_team_time = sim_utils.time_of_flight(tx,field_team_loc)
                # pack the values
                f1 = struct.pack('!i', field_radio_pkt_num)
                f2 = struct.pack('!i', field_team_id)
                f3 = pack_utils.pack_loc(field_team_loc)
                f4 = pack_utils.pack_time(field_team_time)
                # build the payload
                field_team_payload = f1 + f2 + f3 + f4 + beacon_payload
            
                if ( options.drop and stoch.drop_packet() ):
                    continue  # drop packet

                # send the payload to hq
                self.write_db(field_team_payload)
                ################################################################
                update_status += 1
            #endfor
            update(update_status)
        #endfor
        self.stop_db()

        sys.stdout.write('\nDone\n\n')
        sys.stdout.flush()





if __name__=='__main__':
    from optparse import OptionParser
    usage = "usage: %prog [options] arg"

    parser = OptionParser(usage=usage)
    parser.add_option("", "--host", type="string", default="128.173.90.88",
                      help="database host in dotted decimal form [default=%default]")
    parser.add_option("-r", "--radios", type="int", default="3",
                      help="number of field radios to simulate [default=%default]")
    parser.add_option("-i", "--iterations", type="int", default="10",
                      help="number of times to run simulation [default=%default]")
    parser.add_option("-d", "--drop", action="store_true", default=False,
                      help="simlulate dropped packets [default=%default]")
    parser.add_option("", "--rate", type="float", default=0.1,
                      help="packet error/drop rate [default=%default]")
    parser.add_option("-b", "--backoff", action="store_true", default=False,
                      help="enable beacon backoff... [default=%default]")
    parser.add_option("-t", "--delay", type="int", default=5,
                      help="maximum delay time between beacon transmissions [default=%default]")
    parser.add_option("-m", "--move", action="store_true", default=False,
                      help="enable incremental team movement (team movement is random otherwise) [default=%default]")

    

    (options, args) = parser.parse_args()

    sim = simulation(options)
    sim.run()
