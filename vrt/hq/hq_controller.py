#!/usr/bin/env python


#!/usr/bin/env python

from sdr_kml_writer import kml_writer
import threading
import time, os, sys

from random_move import get_random_coord


import rx_side

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


class receiver_thread(threading.Thread):

    '''
    Implements a thread, tests the use of global stack.

    This class adapted from:
    Python Cookbook, p. 362, 2d ed., Alex Martelli et al.
    O'Reilly, 2005, 0-596-00797-3
    '''

    def __init__(self):

        """
        Constructor. Sets envrionment variables.

        self.stopevent: stop flag
        
        """

#         self.params = params
        self.stopevent = threading.Event()
        threading.Thread.__init__(self)


    def run(self):

        """ Executes main loop. """
        rx_side.run(shm)



    def join(self, timeout=None):

        """ Stop thread and wait for return """

        self.stopevent.set()
#         rx_side.stop()
        threading.Thread.join(self, timeout)





def main():

    # remove stop flag, but quietly
    silent = os.system('rm stop_flag 1>/dev/null 2>/dev/null')
    
    global shm
    
    shm = fifo_stack()
    

    # initialize all the kml stuff
    log = []
    doc = kml_writer()

    coord = '-80.42451235968072' + ',' + '37.23096190882968'
    description = "<![CDATA[Mobile Command<br> Registered Teams: Blacksburg Rescue<br> Freq in Use: 468 MHz<br>"
    doc.add_placemark("Command Center", description, coord, 'command-center')
    
    doc.write_to_file('random.kml')

    # start radio receiver
    radio_thread = receiver_thread()
    radio_thread.start()



    while shm.length() == 0:
        pass
        
    coord = shm.pop()
    team_frequency = 468

    coord = get_random_coord()
    description = "Object of the Search"
    doc.add_placemark("Lost Person", description, coord, 'plb')
    
    name = "Search Team"
    description = "<![CDATA[Blacksburg Rescue<br>Frequency: %d MHz<br><br>" % team_frequency
    doc.add_placemark(name, description, coord)
    doc.write_to_file('random.kml')

    while not_stop():
        if not(shm.length() == 0):
            coord = shm.pop()
            doc.update_placemark("Search Team", coord)
            doc.write_to_file('random.kml')
            log.append(coord)
            if len(log) == 11:
                log.pop(0)

        f = open('sdr_ge_log', 'w')
        log_string = "\n".join(log)
        f.write(log_string)
        f.close()


def not_stop():
    # returns 0 if stop_flag exists
    # returns 512 if stop_flag DNE
    status = os.system('ls -l stop_flag 1>/dev/null 2>/dev/null')
    return status 


if __name__=='__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
