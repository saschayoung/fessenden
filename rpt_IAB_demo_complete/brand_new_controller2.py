#!/usr/bin/env python


import sys,os, time



def main():


    n = 0
    m = 0

    for n in range(0,5):
        print ""
        print "receiving..."
        # start receiver
        os.system('sudo ./receive.sh')
        time.sleep(2)
        print "shutting down receiver..."
        # stop receiver
        status = os.system('sudo kill -9 `ps ax | grep benchmark | grep rx | grep -v grep | awk {\'print $1\'}`')
        if status:   #status==256 -> proc not killed
            print "failed to shutdown receiver"

        print ""
        print "transmitting..."
        # start transmitter
        os.system('sudo ./transmit.sh')
        time.sleep(2)
        print "\nshutting down transmitter..."
        # stop transmitter
        status = os.system('sudo kill -9 `ps ax | grep benchmark | grep tx | grep -v grep | awk {\'print $1\'}`')
        if status:   #status==256 -> proc not killed
            print "failed to shutdown transmitter"
    #endfor


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass




