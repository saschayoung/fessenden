#!/usr/bin/env python

import socket
import time

import tftpy



class SocketInterferenceCoordinator(object):

    def __init__(self):
        self.remote_file = 'location'
        self.local_file = 'local_file'
        self.command_file = '/tftp/command_file'

        tftp_server = '192.168.43.50'
        tftp_port = 69
        self.client = tftpy.TftpClient(tftp_server, tftp_port)

        self.last_state = 'off'
        self.current_state = 'off'

        # self.interferers = [['192.168.42.61',43 '192.168.42.63', '192.168.42.64']
    

    def tftp_get(self):
        try:
            self.client.download(self.remote_file, self.local_file)
            return True
        except TypeError as e:
            print False
            # print e
            # print "\nCaught error, trying to recover"
            # time.sleep(1)
            # self.client.download(self.remote_file, self.local_file)
            # print "Recovered from error"


    def check_file(self):
        f = open(self.local_file, 'rt')
        self.lines = f.readlines()
        f.close()
        try:
            if self.lines[-1] != 'fin\n':
                return False
            else:
                return True
        except IndexError:
            return False


    def send_command(self, command):
        s = '432000000,' + command 
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('192.168.42.61', 42000))  
        sock.send(s)
        sock.close()

        s = '436000000,' + command 
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('192.168.42.63', 42000))  
        sock.send(s)
        sock.close()
        

        s = '438000000,' + command 
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('192.168.42.64', 42000))  
        sock.send(s)
        sock.close()




    def interference_logic(self):
        self.last_state = self.current_state
        location = int(self.lines[0].strip('\n'))

        if location == 2:
            self.current_state = 'on'
        else:
            self.current_state = 'off'

        machine_state = [self.last_state, self.current_state]

        if machine_state == ['on', 'on']:
            # print "['on', 'on']:"
            # print "last_state: ", self.last_state
            # print "last_state: ", self.current_state
            # print "no change in state, nothing to do"
            pass

        if machine_state == ['on', 'off']:
            # print "['on', 'off']:"
            # print "last_state: ", self.last_state
            # print "last_state: ", self.current_state
            # print "change in state, turn radio off"
            print "Turning interferers OFF"
            self.send_command('off')
            

        if machine_state == ['off', 'off']:
            # print "['off', 'off']:"
            # print "last_state: ", self.last_state
            # print "last_state: ", self.current_state
            # print "no change in state, nothing to do"
            pass

        if machine_state == ['off', 'on']:
            # print "['off', 'on']:"
            # print "last_state: ", self.last_state
            # print "last_state: ", self.current_state
            # print "change in state, turn radio on"
            print "Turning interferers ON"
            self.send_command('on')












    def run(self):
        print "Interference coordinator started"
        while True:
            success = self.tftp_get()
            if success:
                if self.check_file():
                    # print "Received complete file."
                    self.interference_logic()
                    time.sleep(0.5)

                else:
                    print "Did not receive complete file!"
                    time.sleep(1)
            else:
                print "Encountered tftp error, will try again shortly"
                time.sleep(1)







    
if __name__=='__main__':
    main = SocketInterferenceCoordinator()
    try:
        main.run()
    except KeyboardInterrupt:
        pass













    # def interference_logic(self):
    #     location = int(self.lines[0].strip('\n'))
    #     if location == 2:
    #         self.current_state = 'on'
    #         if self.last_state == 'off':
    #             print "Turning interferers ON"
    #             self.send_command('on')
    #         self.last_state = 'on'
    #     else:
    #         self.current_state = 'off'
    #         if self.last_state == 'on':
    #             print "Turning interferers OFF"
    #             self.send_command('off')
    #         self.last_state = 'off'





    # def interference_logic(self):
    #     location = int(self.lines[0].strip('\n'))
    #     if location == 2:
    #         self.current_state = 'on'
    #         if self.last_state == 'off':
    #             print "Turning interferers ON"
    #             s = "432000000\n"
    #             s = s + "434000000\n"
    #             s = s + "436000000\n"
    #             s = s + "438000000\n"
    #             s = s + "fin\n"
    #             f = open(self.command_file, 'w+')
    #             f.write(s)
    #             f.close()

    #         self.last_state = 'on'
    #     else:
    #         self.current_state = 'off'
    #         if self.last_state == 'on':
    #             print "Turning interferers OFF"
    #             s = "---------\n"
    #             s = s + "---------\n"
    #             s = s + "---------\n"
    #             s = s + "---------\n"
    #             s = s + "fin\n"
    #             f = open(self.command_file, 'w+')
    #             f.write(s)
    #             f.close()
    #         self.last_state = 'off'




        #     self.current_state = 'on'
        #     if self.last_state == 'off':
        #         print "Turning interferers ON"
        #         self.send_command('on')
        #     self.last_state = 'on'
        # else:
        #     self.current_state = 'off'
        #     if self.last_state == 'on':
        #         print "Turning interferers OFF"
        #         self.send_command('off')
        #     self.last_state = 'off'
