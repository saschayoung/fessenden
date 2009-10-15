#!/usr/bin/env python


import sys,os, time
from random_move import random_move


def main():


    n = 0
    m = 0

    for n in range(0,6):

        # rx side
        #############################################
        print ""
        print "receiving..."
        # start receiver
        os.system('sudo ./receive.sh')
        time.sleep(5)
        print "shutting down receiver..."
        # stop receiver
        status = os.system('sudo kill -9 `ps ax | grep benchmark | grep rx | grep -v grep | awk {\'print $1\'}`')
        if status:   #status==256 -> proc not killed
            print "failed to shutdown receiver"
        #############################################







        # tx side
        #############################################
        print ""
        print "transmitting..."
        # start transmitter
        f = open('last_location','r')
        location = f.readlines()
        location = location[0]
        location = random_move(location)
        os.system('sudo ./transmit.sh ' + location)
        time.sleep(2)
        print "\nshutting down transmitter..."
        # stop transmitter
        not_running = os.system('ps ax | grep benchmark | grep tx | grep -v grep | awk {\'print $1\'} 1> /dev/null 2> /dev/null')
        if not_running:
            status = os.system('sudo kill -9 `ps ax | grep benchmark | grep tx | grep -v grep | awk {\'print $1\'}`')
            if status:   #status==256 -> proc not killed
                print "failed to shutdown transmitter"
        #############################################


    #endfor


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass




