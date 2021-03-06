#!/usr/bin/env python

import threading
import time

import tftpy
import netifaces

from transmitter import RF



class Interferer(object):

    def __init__(self):
        self.remote_file = 'command_file'
        self.local_file = 'local_file'

        tftp_server = '192.168.42.10'
        tftp_port = 69
        self.client = tftpy.TftpClient(tftp_server, tftp_port)

        self.ip = netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr']

        self.radio_command = 'off'

        self.radio_transmitter = Radio()
        

    



    def tftp_get(self):
        try:
            self.client.download(self.remote_file, self.local_file)
        except TypeError as e:
            print e
            print "\nCaught error, trying to recover"
            time.sleep(1)
            self.client.download(self.remote_file, self.local_file)


    def check_file(self):
        f = open(self.local_file, 'rt')
        self.lines = f.readlines()
        f.close()
        if self.lines[-1] != 'fin\n':
            return False
        else:
            return True


    def parse_file(self):
        if self.ip == '192.168.42.61':
            line = self.lines[0]
        elif self.ip == '192.168.42.62':
            line = self.lines[1]
        elif self.ip == '192.168.42.63':
            line = self.lines[2]
            pass
        elif self.ip == '192.168.42.64':
            line = self.lines[3]
        else:
            print "File parsing error"
        
        line = line.strip('\n')
        if line == '---------':
            self.radio_command = 'off'
        else:
            self.radio_command = 'on'
            self.radio_freq = int(line)



    def run(self):
        self.radio_transmitter.start()

        while True:
            self.tftp_get()
            if self.check_file():
                # print "Received complete file."
                self.parse_file()
                if self.radio_command == 'off':
                    # print "Turning radio off"
                    self.radio_transmitter.set_radio_state('off')

                else:
                    # print "Turning radio on"
                    self.radio_transmitter.set_freq(self.radio_freq)
                    self.radio_transmitter.set_radio_state('on')

                time.sleep(0.1)

            else:
                print "Did not receive complete file!"
                time.sleep(0.1)
            


    def stop(self):
        self.radio_transmitter.join()





        

class Radio(threading.Thread):
    """
    Threaded radio interferer.

    """

    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.radio_current_state = 'off'
        self.radio_last_state = 'off'
        self.rf = RF()


    def set_radio_state(self, state):
        """
        Control radio operation.

        This function provides a method of controlling operation of the
        radio.

        Parameters
        ----------
        state : str
            One of {`on` | `off` }

        """
        # if state == 'on':
        #     self.current_radio_state = 'on'
        
        # self.radio_last_state = self.radio_current_state
        self.radio_current_state = state


    def set_freq(self, freq):
        """
        Set radio frequency.

        """
        self.freq = freq


    def join(self, timeout=None):
        """
        Stop radio subsystem.

        """
        self.stop_event.set()
        self.rf.close_gpio()
        threading.Thread.join(self, timeout)

        

    def run(self):
        """
        Run radio interferer.

        """
        print "Interferer OFF"

        while not self.stop_event.isSet():
            if self.radio_current_state == 'on':
                if self.radio_last_state == 'on':
                    try:
                        self.rf.run(self.freq)
                    except Exception as e:
                        print e
                        time.sleep(0.001)
                    self.radio_last_state = 'on'
                elif self.radio_last_state == 'off':
                    print "Interferer ON"
                    try:
                        self.rf.run(self.freq)
                    except Exception as e:
                        print e
                        time.sleep(0.001)
                    self.radio_last_state = 'on'
                else:
                    print "Interferer error:"
                    print "self.radio_current_state == `on`"
                    print "self.radio_current_state == ???"

            elif self.radio_current_state == 'off':
                if self.radio_last_state == 'on':
                    print "Interferer OFF"
                    self.radio_last_state = 'off'
                    continue
                elif self.radio_last_state == 'off':
                    self.radio_last_state = 'off'
                    continue
                else:
                    print "Interferer error:"
                    print "self.radio_current_state == `off`"
                    print "self.radio_current_state == ???"
                    
            else:
                print "Interferer error:"
                print "self.radio_current_state == `???`"


            
        


if __name__=='__main__':
    main = Interferer()
    try:
        main.run()
    except KeyboardInterrupt:
        main.stop()
