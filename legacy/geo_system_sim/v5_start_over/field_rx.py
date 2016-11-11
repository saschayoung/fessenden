#!/usr/bin/env python

# core libraries
import struct, sys
from types import NoneType

# external libraries
import psycopg2

# local imports
import pack_utils
import sim_utils
import location_alexandria
import test_coords
from geo_utils import geo_utils
from db_utils import movement_table

DEBUG = True


def update(iteration):
    sys.stdout.write("Working... iteration: %3d\r" % iteration)
    sys.stdout.flush()

def is_inside_box(p1,c1,c2):
    test = ( ((c1[0] <= p1[0])  and
              (c2[0] >  p1[0])) and
             ((c1[1] <= p1[1])  and
              (c2[1] >  p1[1])) )
    return test



def find_closest_corner(p1,c1,c2):
    g = geo_utils()
    c3 = [c1[0],c2[1]]
    c4 = [c2[0],c1[1]]
    # print 'c1: ', c1, type(c1)
    # print 'c2: ', c2,type(c2)
    # print 'c3: ', c3,type(c3)
    # print 'c4: ', c4,type(c4)
    d1 = g.distance(p1,c1)
    d2 = g.distance(p1,c2)
    d3 = g.distance(p1,c3)
    d4 = g.distance(p1,c4)
    d = [[d1,c1], [d2,c2], [d3,c3], [d4,c4]]
    # print 'd: ', d
    d = sorted(d)
    return d[0][1]

class simulation:
    def __init__(self,options):
        # self.options = options
        self.prev_loc = []
        self.target = 0

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


    # location and movement
    ############################################################################
    def get_location(self,ii,kk):
        if ( ii == 1 ):       # first iteration
            loc = location_alexandria.get_random_coord()
            print 'first iteration'
            self.prev_loc.append(loc)
        else:
            print 'get data from db'
            move = movement_table(options.host)
            move.start_db()
            idx = move.get_end()
            if ( type(idx) == NoneType ):
                print 'type(idx) == NoneType'
                if ( options.inc_move ):         # incremental move enabled
                    print 'inc_move enabled'
                    loc = location_alexandria.random_move(self.prev_loc[kk-1])
                    self.prev_loc[kk-1] = loc

                else:                             # random move enabled
                    print 'random move enabled'
                    loc = location_alexandria.get_random_coord()
                    self.prev_loc[kk-1] = loc
            else:
                print 'type(idx) != NoneType'
                r = move.get_data(idx)
                print 'r: ', r
                if ( r == -1 ):
                    print 'r == -1'
                    if ( options.inc_move ):         # incremental move enabled
                        print 'inc_move enabled'
                        loc = location_alexandria.random_move(self.prev_loc[kk-1])
                        self.prev_loc[kk-1] = loc

                    else:                             # random move enabled
                        print 'random move enabled'
                        loc = location_alexandria.get_random_coord()
                        self.prev_loc[kk-1] = loc
                else:
                    print 'r != -1'
                    c1 = r[0]
                    c2 = r[1]
                    target = r[2]
                    p_loc = self.prev_loc[kk-1]
                    if ( is_inside_box(p_loc,c1,c2) ):
                        print 'currently inside box'
                        print 'present_loc: ', p_loc
                        print 'lower bounds: ', c1
                        print 'upper bounds: ', c2
                        loc = location_alexandria.directed_move(p_loc,target)
                        self.prev_loc[kk-1] = loc
                    else:
                        target_p = find_closest_corner(p_loc,c1,c2)
                        print 'target_p: ', target_p
                        print 'p_loc: ', p_loc
                        loc = location_alexandria.directed_move(p_loc,target_p)
                        print 'closest corner: ', loc
                        self.prev_loc[kk-1] = loc
        print 'loc: ', loc
        # sys.exit(1)
        return loc
    ############################################################################



    # # location and movement
    # ############################################################################
    # def get_location(self,ii,kk):
    #     move = sim_utils.get_move_loc(options.file)

    #     if ( ii == 1 ):       # first iteration
    #         loc = location_alexandria.get_random_coord()
    #         self.prev_loc.append(loc)

    #     elif ( move == -1):   # no targeted move coords available

    #         if ( self.target ):                # previous targeted move coords exist
    #             loc = location_alexandria.directed_move(self.prev_loc[kk-1],self.target)
    #             self.prev_loc[kk-1] = loc  
    #             # print 'no new coordinates, still moving to: ', loc

    #         elif ( options.inc_move ):         # incremental move enabled
    #             loc = location_alexandria.random_move(self.prev_loc[kk-1])
    #             self.prev_loc[kk-1] = loc

    #         else:                              # random move enabled
    #             loc = location_alexandria.get_random_coord()
    #             self.prev_loc[kk-1] = loc

    #     else:                 # (new) targeted move coords available
    #         self.target = move
    #         loc = location_alexandria.directed_move(self.prev_loc[kk-1],self.target)
    #         self.prev_loc[kk-1] = loc
    #         # print 'new coordinates, moving to: ', loc

    #     return loc
    # ############################################################################



    # main
    ############################################################################
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
        # iterations = options.iterations
        
        update_status = 0
        i = 0
        ########################################################################
        
        while True:
        # for i in range(iterations):
            ii = i + 1  # beacon pkt num
            jj = i + 1  # field team pkt num

            # this part simulates the beacon transmission
            ####################################################################
            # print '( not (ii == 1) and options.backoff ): ', ( not (ii == 1) and
            #                                                    options.backoff )
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
            i += 1
        #endfor
        self.stop_db()

        sys.stdout.write('\nDone\n\n')
        sys.stdout.flush()
    ############################################################################





if __name__=='__main__':
    from optparse import OptionParser
    usage = "usage: %prog [options] arg"

    parser = OptionParser(usage=usage)
    parser.add_option("", "--host", type="string", default="128.173.90.88",
                      help="database host in dotted decimal form [default=%default]")
    parser.add_option("-r", "--radios", type="int", default="3",
                      help="number of field radios to simulate [default=%default]")
    # parser.add_option("-i", "--iterations", type="int", default="10",
    #                   help="number of times to run simulation [default=%default]")
    parser.add_option("-d", "--drop", action="store_true", default=False,
                      help="simlulate dropped packets [default=%default]")
    parser.add_option("", "--rate", type="float", default=0.1,
                      help="packet error/drop rate [default=%default]")
    parser.add_option("-b", "--backoff", action="store_true", default=False,
                      help="enable beacon backoff... [default=%default]")
    parser.add_option("-t", "--delay", type="int", default=50,
                      help="maximum delay time between beacon transmissions [default=%default]")
    parser.add_option("", "--inc_move", action="store_true", default=False,
                      help="enable incremental team movement (team movement is random otherwise) [default=%default]")
    parser.add_option("-f", "--file", type="string", default="move_command",
                      help="file to check for new coordinate locations to head towards [default=%default]")
    # parser.add_option("-f", "--file", type="string", default="move_command",
    #                   help="file to check for new coordinate locations to head towards [default=%default]")

    

    (options, args) = parser.parse_args()

    sim = simulation(options)
    sim.run()
