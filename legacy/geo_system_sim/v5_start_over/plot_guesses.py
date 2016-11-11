#!/usr/bin/env python

# core libraries

# external libraries
import psycopg2
import numpy as np

# local imports
import sdr_kml_writer
from db_utils import geolocation_table


def main():
    g  = geolocation_table('128.173.90.68')
    g.start_db()

    l= []
    start = g.get_start()
    end = g.get_end()

    i = start
    while ( i <= end ):
        data = g.get_data(i)
        loc = data[6]
        loc = loc.strip(' ()')        # format location
        loc = loc.split(',')
        loc[0] = np.float128(loc[0])
        loc[1] = np.float128(loc[1])
        l.append(loc)
        i += 1

    g.stop_db()


    # print l[0]
    # print 'type(l[0]): ',type(l[0][0])

    kml_write = sdr_kml_writer.kml_writer()
    kml_write.add_colored_pushpin('red-pushpin','ff0000ff')
    n = 1
    for i in l:
        s = 'Guess' + str(n)
        kml_write.add_placemark(s,s,i,'red-pushpin')
        n += 1
    filename = 'guesses_degen.kml'
    kml_write.write_to_file(filename)
    # print 'data:'
    # for j in l:
    #     print j


if __name__=='__main__':
    main()
