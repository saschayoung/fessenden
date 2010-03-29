#!/usr/bin/env python

import numpy as np
import sdr_kml_writer



def main():

    # n = [2,3,4,5,6,7,8,9,10]
    # # n = [25,50,75,100,125,150]
    # for i in n:
    #     f = open('/home/aryoung/batch_results/fessenden_2010-3-27/answer_%s_third_pass' %str(i),'r')
    #     a = f.readlines()
    #     f.close()
    #     a = [float(x.strip('\n')) for x in a]

    f = open('/home/aryoung/batch_results/fessenden_2010-3-27/x_results','r')
    a = f.readlines()
    f.close()
    a = [float(x.strip('\n')) for x in a]

    f = open('/home/aryoung/batch_results/fessenden_2010-3-27/y_results','r')
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


        # coord = str(a[0])+','+str(a[1])
        # kml_write.add_placemark('','',coord)
        # kml_write.write_to_file('/home/aryoung/Desktop/guess_%s.kml' %i)

    for i in range(0,len(x_results)):
        coord = str(x_results[i])+','+str(y_results[i])
        kml_write.add_placemark('','',coord)
    kml_write.write_to_file('/home/aryoung/Desktop/geoloc_kml_file.kml')


if __name__=='__main__':
    main()
