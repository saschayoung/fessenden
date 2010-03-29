#!/usr/bin/env python

import timer

class controller:
    def __init__(self):
        self.components = {}
        
        self.msg_poster = None
        
        self.add_component('dsa', 'sdr_dsa')

        self.timer = timer.ResettableTimer(6, self.reset_timer, inc=1, update=self.handle_timer)

        self.timer.start()

        self.kill_flag = None

        self.acquired_freqs = []
        self.released_freq_ids = []
        
        self.acquire_requests = []
        self.release_requests = []

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
            self.timer.run()

    def handle_timer(self,state):
        if state == 1:
            self.__check_geoloc()
        elif state == 2:
            self.__check_dsa()
        elif state == 3:
            self.__check_gui_data()
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
        print "Check Geoloc"

    def __check_dsa(self):
        self.components['dsa'].input_data(self.release_requests, self.acquire_requests)
        self.components['dsa'].work()
        output = self.components['dsa'].output_data()
        print "DSA out: ", output

        self.acquired_freqs = output[0]
        self.released_freq_ids = output[1]

    def __check_gui_data(self):
        print "Check GUI Data"


    def __update_user_info(self):
        print "Update User Info"

    def __update_gui(self):
        print "Update GUI Data"

    def __push_commands(self):
        print "Push Commands"


if __name__ == '__main__':
    import time

    test = controller()
    time.sleep(30)
