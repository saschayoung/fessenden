#!/usr/bin/env python

from random_move import get_random_coord
from sdr_kml_writer import kml_writer
import random

if __name__ == '__main__':
    doc = kml_writer()
    
    coord = '-80.42451235968072' + ',' + '37.23096190882968'
    description = "<![CDATA[Mobile Command<br> "
    doc.add_placemark("Command Center", description, coord, 'command-center')

    n = 1;

    while n < 5:
        name = "Search Team %d" % n
        freq = random.randrange(460,471)
        coord = get_random_coord()
        description = "<![CDATA[Search Team %d<br>Frequency: %d MHz<br><br>" % (n, freq)
        doc.add_placemark(name, description, coord)
        n += 1

    name = "Fire House 9"
    description = "<![CDATA[Fire Fighters<br>Standard Fire Engine"
    coord = '-80.41451340175786,37.22984292113826'
    doc.add_placemark(name, description, coord, 'fire-truck')

    name = "Fire Team 1"
    description ="<![CDATA[Local Fire Rescue Team"
    coord = '-80.40111104756072,37.23731288400135'
    doc.add_placemark(name, description, coord, 'fire-helmet')

    name = "Fire Team 2"
    description = "<![CDATA[Blacksburg Fire and Rescue"
    coord = '-80.42610463514606,37.2240839458946'
    doc.add_placemark(name, description, coord, 'fire-helmet')

    n = 1
    while n < 3:
        name = "K9 Unit %d" % n
        description = "<![CDATA[K9 Search Team"
        coord = get_random_coord()
        doc.add_placemark(name, description, coord, 'k9-unit')
        n += 1


    doc.write_to_file('static_display.kml')
