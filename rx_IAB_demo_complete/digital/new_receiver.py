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

import random
import struct
import sys

# from current dir
import usrp_receive_path

#import os
#print os.getpid()
#raw_input('Attach and press enter: ')

class my_top_block(gr.top_block):
    def __init__(self, demodulator, rx_callback, options):
        gr.top_block.__init__(self)

        # Set up receive path
        self.rxpath = usrp_receive_path.usrp_receive_path(demodulator, rx_callback, options) 

        self.connect(self.rxpath)

# /////////////////////////////////////////////////////////////////////////////
#                                   main
# /////////////////////////////////////////////////////////////////////////////

global n_rcvd, n_right

def main():
    global n_rcvd, n_right

    n_rcvd = 0
    n_right = 0
    
    def rx_callback(ok, payload):
        global n_rcvd, n_right
        (pktno,) = struct.unpack('!H', payload[0:2])
        (beacon_pktno,) = struct.unpack('!H', payload[2:4])
        (beacon_ID,) = struct.unpack('!H', payload[4:6])
        (team_ID,) = struct.unpack('!H', payload[6:8])
        (lon_mant,) = struct.unpack('!H', payload[8:10])
        (lon_frac1,) = struct.unpack('!H', payload[10:12])
        (lon_frac2,) = struct.unpack('!H', payload[12:14])
        (lon_frac3,) = struct.unpack('!H', payload[14:16])
        (lon_frac4,) = struct.unpack('!H', payload[16:18])
        (lat_mant,) = struct.unpack('!H', payload[18:20])
        (lat_frac1,) = struct.unpack('!H', payload[20:22])
        (lat_frac2,) = struct.unpack('!H', payload[22:24])
        (lat_frac3,) = struct.unpack('!H', payload[24:26])
        (lat_frac4,) = struct.unpack('!H', payload[26:28])


        n_rcvd += 1
        if ok:
            n_right += 1

        print "ok = %5s  pktno = %4d  n_rcvd = %4d  n_right = %4d" % (
            ok, pktno, n_rcvd, n_right)
        print ""
        print "plb beacon number: ", beacon_pktno
        print "beacon ID: ", beacon_ID
        print "team ID: ", team_ID
        print "longitude: -%d.%d%d%d%d" %(int(lon_mant), lon_frac1, lon_frac2, lon_frac3, lon_frac4)
        print "latitude: %d.%d%d%d%d" %(lat_mant, lat_frac1, lat_frac2, lat_frac3, lat_frac4)


    demods = modulation_utils.type_1_demods()

    # Create Options Parser:
    parser = OptionParser (option_class=eng_option, conflict_handler="resolve")
    expert_grp = parser.add_option_group("Expert")

    parser.add_option("-m", "--modulation", type="choice", choices=demods.keys(), 
                      default='gmsk',
                      help="Select modulation from: %s [default=%%default]"
                            % (', '.join(demods.keys()),))

    usrp_receive_path.add_options(parser, expert_grp)

    for mod in demods.values():
        mod.add_options(expert_grp)

    (options, args) = parser.parse_args ()

    if len(args) != 0:
        parser.print_help(sys.stderr)
        sys.exit(1)

    if options.rx_freq is None:
        sys.stderr.write("You must specify -f FREQ or --freq FREQ\n")
        parser.print_help(sys.stderr)
        sys.exit(1)


    # build the graph
    tb = my_top_block(demods[options.modulation], rx_callback, options)

    r = gr.enable_realtime_scheduling()
    if r != gr.RT_OK:
        print "Warning: Failed to enable realtime scheduling."

    tb.start()        # start flow graph
    tb.wait()         # wait for it to finish

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
