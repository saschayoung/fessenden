#!/usr/bin/env python

import timer, threading, wx, numpy
import sdr_gui

class controller:
    def __init__(self):
        self.components = {}
        
        self.msg_poster = None
        
        self.add_component('dsa', 'sdr_dsa')
        self.add_component('radio', 'sdr_radio')
        self.add_component('geoloc', 'sdr_geoloc')
        self.add_component('kb', 'sdr_know')

        self.timer = timer.ResettableTimer(6, self.reset_timer, inc=1, update=self.handle_timer)
        
        self.lock = threading.Lock()

        self.timer.start()

        self.kill_flag = None

        #DSA Related Containers
        self.acquired_freqs = []
        self.released_freq_ids = []
        
        self.acquire_requests = []
        self.release_requests = []
        
        self.freq_data = []
        self.emphasis = None

        #KB Related Containers
        self.new_users = []

        #Geolocation Related Containers
        self.best_guess = None

        #GUI Interface variables
        self.__gui_new_users = []
        self.__gui_freq_requests = []
        self.__gui_freq_releases = []
        self.__gui_emphasis = None
        self.__gui_freq_data = []
        self.__gui_user_data = []
        self.__gui_geoloc_data = []

    def add_component(self, type, filename):
        keys = self.components.keys()
        if keys.count(type) == 0:
            module = __import__(filename)
            self.components[type] = module.component()

    def remove_component(self, type):
        keys = self.components.keys()
        if not(keys.count(type) == 0):
            del self.components[type]

    def reset_timer(self):
        if not(self.kill_flag):
            self.timer.reset()
            # self.timer.run()

    def handle_timer(self,state):
        if state == 1:
            self.__check_geoloc()
        elif state == 2:
            self.__check_gui_data()
        elif state == 3:
            self.__check_dsa()
        elif state == 4:
            self.__update_user_info()
        elif state == 5:
            self.__update_gui()
        elif state == 6:
            self.__push_commands()


    def __del__(self):
        self.kill_flag = 1
        self.timer.kill()

        keys = self.components.keys()
        for key in keys:
            del self.components[key]

        del self.components

    def __check_geoloc(self):
        self.components['geoloc'].start()
        self.best_guess = self.components['geoloc'].output_data()

    def __check_gui_data(self):
        print "Check GUI Data"
        self.lock.acquire()
        self.new_users = [k for k in self.__gui_new_users]
        self.acquire_requests = [k for k in self.__gui_freq_requests]
        self.release_requests = [k for k in self.__gui_freq_releases]
        self.__gui_freq_requests = []
        self.__gui_freq_releases = []
        if self.__gui_emphasis:
            self.emphasis = self.__gui_emphasis[0]
        self.lock.release()
        
        print "New Users: ", self.new_users
        print "Freq Requests: ", self.acquire_requests
        print "Freq Releases: ", self.release_requests
        print "Emphasis: ", self.emphasis
        print

    def __check_dsa(self):
        user_loc = self.components['kb'].output_data()
        user_loc = user_loc[1]

        self.components['dsa'].input_data(self.release_requests, self.acquire_requests,user_loc, self.emphasis)
        self.components['dsa'].start()
        output = self.components['dsa'].output_data()

        self.acquired_freqs = output[0]
        self.released_freq_ids = output[1]
        self.freq_data = output[2]

    def __update_user_info(self):
        self.components['kb'].input_data(self.new_users)

    def __update_gui(self):
        users = self.components['kb'].output_data()
        users = users[0]

        self.lock.acquire()
        self.__gui_freq_data = [k for k in self.freq_data]
        self.__gui_user_data = [k for k in users]
        self.__gui_geoloc_data = self.best_guess
        print "Setting Gui freq data to ", self.__gui_freq_data
        print "Setting Gui user data to ", self.__gui_user_data
        print "Setting Gui geoloc data to ", self.__gui_geoloc_data
        print
        self.lock.release()

    def __push_commands(self):
        freq_commands = [self.acquired_freqs, self.released_freq_ids]
        self.components['radio'].input_data(freq_commands, self.best_guess)
        self.components['radio'].start()


    def start_gui(self):
        app = wx.App()
        self.__gui = sdr_gui.gui(self.__set_new_users,self.__make_freq_request, self.__release_freq,self.__set_emphasis,
                                 self.__get_freq_data,self.__get_user_data,self.__get_geoloc_data)
        self.__gui.Show()
        app.MainLoop()

    #GUI Interface Functions
    def __set_new_users(self, new_users):
        self.lock.acquire()
        if not(type(new_users) is list):
            new_users = [new_users]
        self.__gui_new_users = new_users
        self.lock.release()

    def __make_freq_request(self, team_id):
        self.lock.acquire()
        self.__gui_freq_requests.append(team_id)
        self.lock.release()

    def __release_freq(self, freq):
        self.lock.acquire()
        self.__gui_freq_releases.append(freq)
        self.lock.release()

    def __set_emphasis(self, emphasis):
        self.lock.acquire()
        if not(type(emphasis) is list):
            emphasis = [emphasis]
        self.__gui_emphasis = emphasis
        self.lock.release()
    
    def __get_freq_data(self):
        self.lock.acquire()
        output = [k for k in self.__gui_freq_data]
        self.lock.release()
        return output

    def __get_user_data(self):
        self.lock.acquire()
        output = [k for k in self.__gui_user_data]
        self.lock.release()
        return output

    def __get_geoloc_data(self):
        self.lock.acquire()
        output = [k for k in self.__gui_geoloc_data]
        self.lock.release()
        return output

if __name__ == '__main__':
    import time

    test = controller()
    test.start_gui()
    # time.sleep(14)
