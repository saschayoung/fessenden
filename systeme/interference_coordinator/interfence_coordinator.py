#!/usr/bin/env python

import time

import tftpy


class InterferenceCoordinator(object):

    def __init__(self):
        self.remote_file = 'location'
        self.local_file = 'local_file'
        self.command_file = '/tftp/command_file'

        tftp_server = '192.168.42.50'
        tftp_port = 69
        self.client = tftpy.TftpClient(tftp_server, tftp_port)

        self.last_state = 'off'
        self.current_state = 'off'
    

    def tftp_get(self):
        self.client.download(self.remote_file, self.local_file)

    def check_file(self):
        f = open(self.local_file, 'rt')
        self.lines = f.readlines()
        f.close()
        if self.lines[-1] != 'fin':
            return False
        else:
            return True


    def interference_logic(self):
        location = int(self.lines[0].strip('\n'))
        if location == 3:
            self.current_state = 'on'
            if self.last_state == 'off':
                print "Turning interferers ON"
                s = "432000000\n"
                s = s + "434000000\n"
                s = s + "436000000\n"
                s = s + "438000000\n"
                s = s + "fin"
                f = open(self.command_file, 'w+')
                f.write(s)
                f.close()

            self.last_state = 'on'
        else:
            self.current_state = 'off'
            if self.last_state == 'on':
                print "Turning interferers OFF"
                s = "---------\n"
                s = s + "---------\n"
                s = s + "---------\n"
                s = s + "---------\n"
                s = s + "fin"
                f = open(self.command_file, 'w+')
                f.write(s)
                f.close()
            self.last_state = 'off'


    def run(self):
        while True:
            self.tftp_get()
            if self.check_file():
                # print "Received complete file."
                self.interference_logic()
                time.sleep(1)

            else:
                print "Did not receive complete file!"
                time.sleep(0.1)



    
if __name__=='__main__':
    main = InterferenceCoordinator()
    try:
        main.run()
    except KeyboardInterrupt:
        pass
