#!/usr/bin/env python

import numpy as np
import sdr_kml_writer


class hyperbola_writer:

    def __init__(self):
        pass
    
    def create_first_part(self):
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
        return s


    def add_first_hyperbola(self,s,a):
        i = 0
        while ( i < len(a[0]) ):
            s += '          %.15f, %.15f, 50\n' %(a[0][i],a[1][i])
            i += 1
        return s


    def create_middle_part(self,s):
        s += '          </coordinates>\n'
        s += '        </LineString>\n'
        s += '      </Placemark>\n'
        s += '      <Placemark>\n'
        s += '        <name>Hyperbola1</name>\n'
        s += '        <styleUrl>#tdoa_hyperbola</styleUrl>\n'
        s += '        <LineString>\n'
        s += '          <tessellate>0</tessellate>\n'
        s += '          <coordinates>\n'
        return s


    def add_second_hyperbola(self,s,a):
        i = 0
        while ( i < len(a[0]) ):
            s += '          %.15f, %.15f, 50\n' %(a[2][i],a[3][i])
            i += 1
        return s

    def create_end_part(self,s):
        s += '          </coordinates>\n'
        s += '        </LineString>\n'
        s += '      </Placemark>\n'
        s += '  </Document>\n'
        s += '</kml>\n'
        return s

    # def write_hyperbola(self,h1,h2):
    #     s = self.create_first_part()
    #     s += self.add_first_hyperbola(s,h1)
    #     s += self.create_middle_part(s)
    #     s += self.add_second_hyperbola(s,h2)
    #     s += self.create_end_part(s)

    #     f = open('hyperbolas.kml','w+')
    #     f.write(s)
    #     f.close()

    def write_hyperbola(self,a):
        s = self.create_first_part()
        s = self.add_first_hyperbola(s,a)
        s = self.create_middle_part(s)
        s = self.add_second_hyperbola(s,a)
        s = self.create_end_part(s)

        f = open('hyperbolas.kml','w+')
        f.write(s)
        f.close()



    # print s



