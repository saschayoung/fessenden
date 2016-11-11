#!/usr/bin/env python

import numpy as np
import sdr_kml_writer



def write_hyperbola(a,filename):

    s =  '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n'
    s += '<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n'
    s += '  <Document>\n'
    s += '      <Style id=\"tdoa_hyperbola\">\n'
    s += '        <LineStyle>\n'
    s += '          <color>7f0000ff</color>\n'
    s += '          <width>4</width>\n'
    s += '        </LineStyle>\n'
    s += '      </Style>\n'
    s += '      <Placemark>\n'
    s += '        <name>Hyperbola1</name>\n'
    s += '        <styleUrl>#tdoa_hyperbola</styleUrl>\n'
    s += '        <visibility>1</visibility>\n'
    s += '        <LineString>\n'
    s += '          <tessellate>0</tessellate>\n'
    s += '          <coordinates>\n'

    i = 0
    while ( i < len(a[0]) ):
        s += '          %.15f, %.15f, 50\n' %(a[0][i],a[1][i])
        i += 1

    s += '          </coordinates>\n'
    s += '        </LineString>\n'
    s += '      </Placemark>\n'
    s += '      <Placemark>\n'
    s += '        <name>Hyperbola1</name>\n'
    s += '        <styleUrl>#tdoa_hyperbola</styleUrl>\n'
    s += '        <LineString>\n'
    s += '          <tessellate>0</tessellate>\n'
    s += '          <coordinates>\n'

    i = 0
    while ( i < len(a[0]) ):
        s += '          %.15f, %.15f, 50\n' %(a[2][i],a[3][i])
        i += 1
    s += '          </coordinates>\n'
    s += '        </LineString>\n'
    s += '      </Placemark>\n'
    s += '  </Document>\n'
    s += '</kml>\n'

    f = open(filename,'w+')
    f.write(s)
    f.close()



    # print s



