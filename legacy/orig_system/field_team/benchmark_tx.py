#!/usr/bin/env python
#
# Copyright 2005,2006,2007,2009 Free Software Foundation, Inc.
# 
# This file is part of GNU Radio
# 
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

from gnuradio import gr, gru, modulation_utils
from gnuradio import usrp
from gnuradio import eng_notation
from gnuradio.eng_option import eng_option
from optparse import OptionParser

import random, time, struct, sys, os

# from current dir
import usrp_transmit_path

#import os 
#print os.getpid()
#raw_input('Attach and press enter')






def format_loc(loc):
    loc = loc.strip('[]-\n')
    loc = loc.split(',')

    # process longitude
    lon = loc[0]
    lon = lon.split('.')
    lon_mant = lon[0]
    lon_frac = lon[1]
    lon_frac1 = lon_frac[0:4]
    lon_frac2 = lon_frac[4:8]
    lon_frac3 = lon_frac[8:12]
    lon_frac4 = lon_frac[12:15]

#     print "lon_mant: ", lon_mant
#     print "lon_frac1: ", lon_frac1
#     print "lon_frac2: ", lon_frac2
#     print "lon_frac3: ", lon_frac3


    # process latitude
    lat = loc[1]
    lat = lat.split('.')
    lat_mant = lat[0]
    lat_frac = lat[1]
    lat_frac1 = lat_frac[0:4]
    lat_frac2 = lat_frac[4:8]
    lat_frac3 = lat_frac[8:12]
    lat_frac4 = lat_frac[12:15]

    lon1 = struct.pack('!H', int(lon_mant) & 0xffff)
    lon2 = struct.pack('!H', int(lon_frac1) & 0xffff)
    lon3 = struct.pack('!H', int(lon_frac2) & 0xffff)
    lon4 = struct.pack('!H', int(lon_frac3) & 0xffff)
    lon5 = struct.pack('!H', int(lon_frac4) & 0xffff)

    lat1 = struct.pack('!H', int(lat_mant) & 0xffff)
    lat2 = struct.pack('!H', int(lat_frac1) & 0xffff)
    lat3 = struct.pack('!H', int(lat_frac2) & 0xffff)
    lat4 = struct.pack('!H', int(lat_frac3) & 0xffff)
    lat5 = struct.pack('!H', int(lat_frac4) & 0xffff)

    lon_payload = lon1 + lon2 + lon3 + lon4 + lon5

    lat_payload = lat1 + lat2 + lat3 + lat4 + lat5

    loc_payload = lon_payload + lat_payload

    return loc_payload







class my_top_block(gr.top_block):
    def __init__(self, modulator, options):
        gr.top_block.__init__(self)

        self.txpath = usrp_transmit_path.usrp_transmit_path(modulator, options)

        self.connect(self.txpath)

# /////////////////////////////////////////////////////////////////////////////
#                                   main
# /////////////////////////////////////////////////////////////////////////////

def main():

    def send_pkt(payload='', eof=False):
        return tb.txpath.send_pkt(payload, eof)

    def rx_callback(ok, payload):
        print "ok = %r, payload = '%s'" % (ok, payload)

    mods = modulation_utils.type_1_mods()

    parser = OptionParser(option_class=eng_option, conflict_handler="resolve")
    expert_grp = parser.add_option_group("Expert")

    parser.add_option("-m", "--modulation", type="choice", choices=mods.keys(),
                      default='gmsk',
                      help="Select modulation from: %s [default=%%default]"
                            % (', '.join(mods.keys()),))

    parser.add_option("-s", "--size", type="eng_float", default=1500,
                      help="set packet size [default=%default]")
    parser.add_option("-M", "--megabytes", type="eng_float", default=1.0,
                      help="set megabytes to transmit [default=%default]")
    parser.add_option("","--discontinuous", action="store_true", default=False,
                      help="enable discontinous transmission (bursts of 5 packets)")
    parser.add_option("","--from-file", default=None,
                      help="use file for packet contents")
    parser.add_option("","--location", type="string", 
                      default = "[-80.422221051169391, 37.233082631938416]",
                      help="set radio location in [lon, lat] (default=%default)")

    usrp_transmit_path.add_options(parser, expert_grp)

    for mod in mods.values():
        mod.add_options(expert_grp)

    (options, args) = parser.parse_args ()

    if len(args) != 0:
        parser.print_help()
        sys.exit(1)

    if options.tx_freq is None:
        sys.stderr.write("You must specify -f FREQ or --freq FREQ\n")
        parser.print_help(sys.stderr)
        sys.exit(1)

    if options.from_file is not None:
        source_file = open(options.from_file, 'r')

    # build the graph
    tb = my_top_block(mods[options.modulation], options)

    r = gr.enable_realtime_scheduling()
    if r != gr.RT_OK:
        print "Warning: failed to enable realtime scheduling"

    tb.start()                       # start flow graph
        


    # generate and send packets
    team_ID = 30376

    n = 0
    pktno = 0
    pkt_size = int(options.size)


    f = open('plb_data','r')
    all_lines = f.readlines()
    f.close()
    os.system('cat /dev/null > plb_data')
    all_lines = "".join(all_lines)
    all_lines = all_lines.split("\n")
    all_lines.pop()

    payload4 = struct.pack('!H', team_ID & 0xffff)

    # original location
    # '[-80.422221051169391, 37.233082631938416]'
    loc_payload = format_loc(options.location)
   

    for n in all_lines:

        n = n.split(',')
        data = (pkt_size - 28) * chr(pktno & 0xff)
        payload1 = struct.pack('!H', pktno & 0xffff)
        payload2 = struct.pack('!H', int(n[0]) & 0xffff)
        payload3 = struct.pack('!H', int(n[1]) & 0xffff)
        payload = payload1 + payload2 + payload3 + payload4 + loc_payload + data

        send_pkt(payload)
        sys.stderr.write('.')
        if options.discontinuous and pktno % 5 == 4:
            time.sleep(1)
        pktno += 1
        if pktno % 20 == 0:
            print "\npktno: %d \n" %pktno 
            print "last location: ", options.location
            os.system('echo ' + options.location + ' > last_location')

    print "finished transmitting"


    # import all data from file
    # 
    # send out all pkt numbers
    # fin


         

        
    send_pkt(eof=True)

    tb.wait()                       # wait for it to finish

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass









#     while n < nbytes:
#         if options.from_file is None:
#             data = (pkt_size - 2) * chr(pktno & 0xff) 
#         else:
#             data = source_file.read(pkt_size - 2)
#             if data == '':
#                 break;

#         payload = struct.pack('!H', pktno & 0xffff) + data
#    nbytes = int(1e6 * options.megabytes)
#         n += len(payload)
