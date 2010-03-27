#!/usr/bin/env python

import numpy as np
import sdr_kml_writer



def main():

    f = open('../hq/x_results','r')
    a = f.readlines()
    f.close()
    a = [float(x.strip('\n')) for x in a]

    f = open('../hq/y_results','r')
    b = f.readlines()
    f.close()
    b = [float(x.strip('\n')) for x in b]

    x_results = []
    y_results = []

    i = 0
    while ( i < len(a) ):
        x_results.append(a[i])
        y_results.append(b[i])
        i +=1

    kml_write = sdr_kml_writer.kml_writer()

    for i in range(0,len(x_results)):
        coord = str(x_results[i])+','+str(y_results[i])
        kml_write.add_placemark('','',coord)
    kml_write.write_to_file('geoloc_kml_file.kml')


if __name__=='__main__':
    main()
