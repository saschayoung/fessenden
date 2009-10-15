#!/usr/bin/env python

from sdr_kml_writer import kml_writer
import threading
import time

from random_move import random_move
from ge_controller import range_random, get_random_coord

class fifo_stack:
    '''
    Implements a (supposed) very fast stack (of fifo queue. This
    implementation was adapted from Raymond Hettinger's post on
    ActiveState in 'Recipe 68436: Fifo as single linked lists.'

    http://code.activestate.com/recipes/68436/
    '''

    def __init__(self):
        self.nextin = 0
        self.nextout = 0
        self.data = {}
    def push(self, value):
        self.data[self.nextin] = value
        self.nextin += 1

    def pop(self):
        value = self.data[self.nextout]
        del self.data[self.nextout]
        self.nextout += 1
        return value

    def length(self):
        ret = len(self.data)
        return ret

    def debug(self):
        print ""
        print "debug info follows..."
        print ""
        print "nextin:           ", self.nextin
        print "nextout:          ", self.nextout
        print "self.data length: ", self.length()
        print "self.data:        ", self.data
        print ""

class data_thread(threading.Thread):
    
    '''
    This does nothing right now. Used to run
    coordinate randomizer.
    '''

    def __init__(self):
        self.team_coord = get_random_coord()
        self.stopevent = threading.Event()
        threading.Thread.__init__(self)

    def run(self):
        while not(self.stopevent.isSet()):
            time.sleep(3)
            self.team_coord = random_move(self.team_coord, 0.0006)
            shm.push(self.team_coord)
        print ("data_thread stopping")

    def join(self, timeout=None):
        self.stopevent.set()
        threading.Thread.join(self, timeout)

class kml_thread(threading.Thread):

    '''
    This takes care of all (we think) of the initialization for
    the kml writing. This requires get_random_coord() in random_move.py
    '''

    def __init__(self):
        self.log = []
        self.doc = kml_writer()
        coord = get_random_coord()
        description = "Object of the Search"
        self.doc.add_placemark("Lost Person", description, coord, 'plb')

        coord = get_random_coord()
        description = "<![CDATA[Mobile Command<br> Registered Teams: Blacksburg Rescue<br> Freq in Use: 467 MHz<br>"
        self.doc.add_placemark("Command Center", description, coord, 'command-center')

        self.stopevent = threading.Event()
        threading.Thread.__init__(self)

    def run(self):
        while shm.length() == 0:
            pass
        
        coord = shm.pop()
        team_frequency = 467

        name = "Search Team"
        description = "<![CDATA[Blacksburg Rescue<br>Frequency: %d MHz<br><br>" % team_frequency
        self.doc.add_placemark(name, description, coord)
        self.doc.write_to_file('random.kml')

        while not(self.stopevent.isSet()):
            if not(shm.length() == 0):
                coord = shm.pop()
                self.doc.update_placemark("Search Team", coord)
                self.doc.write_to_file('random.kml')
                self.log.append(str(coord))
                if len(self.log) == 11:
                    self.log.pop(0)

        f = open('sdr_ge_log', 'w')
        log_string = "\n".join(self.log)
        f.write(log_string)
        f.close()
        print ("kml_thread stopping")
            
    def join(self, timeout = None):
        self.stopevent.set()
        threading.Thread.join(self, timeout)

if __name__=='__main__':
    global shm
    
    shm = fifo_stack()
    
    thread1 = data_thread()
    thread2 = kml_thread()

    thread1.start()
    thread2.start()

    raw_input("Please Enter to End program")

    thread1.join()
    thread2.join()
