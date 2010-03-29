#!/usr/bin/env python

import threading, timer
import geo_utils


class component:
    def __init__(self):
        self.emphasis = None
        self.queue = []
        self.booted_list = []

        self.release_requests = []
        self.acquire_requests = []

        self.acquire_out = []
        self.release_out = []

        self.freqs = [[462.5625*10**6, 1, 0],
                      [462.5875*10**6, 1, 0],
                      [462.6125*10**6, 1, 0],
                      [462.6375*10**6, 1, 0],
                      [462.6625*10**6, 1, 0],
                      [462.6875*10**6, 1, 0],
                      [462.7125*10**6, 1, 0],
                      [467.5625*10**6, 1, 0],
                      [467.5875*10**6, 1, 0],
                      [467.6125*10**6, 1, 0],
                      [467.6375*10**6, 1, 0],
                      [467.6625*10**6, 1, 0],
                      [467.6875*10**6, 1, 0],
                      [467.7125*10**6, 1, 0]]

        
        self.user_locs = []
        self.threshold_distance = 5000
        self.geo = geo_utils.geo_utils()

        self.channel_time = 10
        
        self.time_thread = timer.ResettableTimer(10.0, self.timer_flip, inc=1)
        
        self.lock = threading.Lock()
        
        self.time_thread.start()

        self.kill_flag = None


    def __del__(self):
        self.kill_flag = 1
        self.time_thread.kill()

    def timer_flip(self):
        self.lock.acquire()
        for i in range(len(self.freqs)):
            print self.freqs[i]

            if self.freqs[i][1] > 0:
                self.freqs[i][1] += 1
            elif self.freqs[i][1] < 0:
                self.freqs[i][2] -= 1
            if self.freqs[i][2] < 0:
                booted_id = self.freqs[i][1] * -1
                if self.booted_list.count(booted_id) == 0:
                    self.booted_list.append(booted_id)
        self.lock.release()

        if not(self.kill_flag):
            self.time_thread.reset()
            self.time_thread.run()


    def work(self):
        if self.release_requests:
            self.release_frequency()

        if self.acquire_requests:
            self.process_acquire_requests()

        if self.queue:
            self.acquire_frequency()

    def output_data(self):
        self.lock.acquire()
        for i in self.booted_list:
            if self.release_out.count(i) == 0:
                self.release_out.append(i)
        self.booted_list = []
        self.lock.release()
        
        return [self.acquire_out, self.release_out]

    def input_data(self, release_request = None, acquire_request = None, user_locs = None, emphasis = None):
        if release_request:
            #freqs
            if not([int,float,tuple,list].count(type(release_request)) == 0):
                if [tuple, list].count(type(release_request)) == 0:
                    self.release_requests = [release_request]
                else:
                    self.release_requests = release_request
            else:
                print "SDR DSA Error: Bad type for release request"
                print "Type: ", type(release_request)
                print "Request: ", release_request
                print

        if acquire_request:
            #(id, skill,loc)
            if not([tuple, list].count(type(acquire_request)) == 0):
                if [tuple, list].count(type(self.acquire_requests[0])) == 0:
                    self.acquire_requests = [self.acquire_requests]
                else:
                    self.acquire_requests = acquire_request
            else:
                print "SDR DSA Error: Bad type for acquire request"
                print "Type: ", type(acquire_request)
                print "Request: ", acquire_request
                print

        if user_locs:
            #Assumed order [id, loc, freq]
            bad_type = True
            if not([tuple, list, dict].count(type(user_locs)) == 0):
                if type(users) is dict:
                    bad_type = False
                    self.user_locs = [user_locs]
                else:
                    if type(user_locs[0]) is dict:
                        bad_type = True
                        self.user_locs = user_locs

            if bad_type:
                print "SDR DSA Error: Bad type for users"
                print "Type: ", type(user_locs)
                if not([tuple, list].count(type(user_locs)) == 0):
                    print "Inner Type: ", type(user_locs[0])
                print "Users: ", user_locs
                print

        if emphasis:
            if type(emphasis) is str:
                self.emphasis = emphasis
            else:
                print "SDR DSA Error: Bad type for emphasis"
                print "Type: ", type(emphasis)
                print "Emphasis: ", emphasis
                print

    def process_acquire_requests(self):
        user_list = []
        self.lock.acquire()
        for data in self.freqs:
            if data[1] > 0:
                user_list.append(-1*data[0])
        self.lock.release()


        for item in self.acquire_requests:
            if user_list.count(item[0]) == 0:
                if self.queue.count(item) == 0:
                    self.queue.append(item)

        self.acquire_requests = []
        
        
        tmp1 = []
        tmp2 = []
        for item in self.queue:
            if len(item) > 1:
                if item[1] == self.emphasis:
                    tmp1.append(item)
                else:
                    tmp2.append(item)
            else:
                tmp2.append(item)

        self.queue = tmp1 + tmp2
        

    def acquire_frequency(self):
        index = 0
        satisfied = []
        #(id, freq)
        self.acquire_out = []
        for item in self.queue:
            if len(item) > 2:
                loc = item[2]
            else:
                loc = None

            (freq_index, success) = self.get_open_channel(loc)

            if success:
                satisfied.append(index)
                self.lock.acquire()
                self.acquire_out.append([item[0], self.freqs[freq_index][0]])
                self.freqs[1] = -1*item[0]
                self.freqs[2] = self.channel_time
                self.lock.release()

        satisfied.sort()
        satisfied.reverse()
        for i in satisfied:
            self.queue.pop(i)
    
    def release_frequency(self):
        #list of released ids
        self.release_out = []

        self.lock.acquire()
        for freq in self.release_requests:
            for i in range(len(self.freqs)):
                if freq == self.freqs[i][0]:
                    self.release_out.append(self.freqs[i][1]*-1)
                    self.freqs[i][1] = 1
                    self.freqs[i][2] = 0
                    break
        self.lock.release()

        self.release_requests = []

    def get_open_channel(self, request_loc = None):
        max_pref = -9999
        max_index = 0
        index = 0
        self.lock.acquire()
        for data in self.freqs:
            if data[1] > max_pref:
                max_pref = data[1]
                max_index = index
            index += 1
        self.lock.release()

        if max_pref < 0:
            result = -1
        else:
            result = 0

        if result == -1:
            if self.user_locs and request_loc:
                for user in user_locs:
                    if not(user[2]):
                        continue
                    
                    freq = -1
                    distance = self.geo.distance(user[1], request_loc)
                    if distance > self.threshold_distance:
                        freq = user[2]
                        break
                
                if freq > -1:
                    index = 0
                    self.lock.acquire()
                    for data in self.freqs:
                        if data[0] == freq:
                            max_index = index
                            result = 0
                            break
                        index += 1
                    self.lock.release()
        
        return (max_index, result)



    # def check_channels(self):
    #     statisfied = []
    #     for i in range(len(self.queue)):


    #         # data = self.components['KB'].output_data()

    #         # self.components['optimizer'].input_data(freqs=data[0], users=data[1], request=self.queue[i])
    #         # self.components['optimizer'].start()
    #         # result = self.components['optimizer'].output_data()


    #         if result > 0:
    #             #send vacate message 
    #             debug1 = self.components['KB'].input_data(acquire_freqs = (self.queue[i][0], result))
    #             debug2 = self.components['KB'].start()
    #             statisfied.append(i)
                
    #     statisfied.sort()
    #     statisfied.reverse()

    #     for i in statisfied:
    #         self.queue.pop(i)

    #     if self.DEBUG:
    #         print "Check Channels"
    #         print "Optimizer Result: ", result
    #         print "KB Input Result: ", hex(debug1)
    #         print "KB Start Result: ", hex(debug2)
    #         print

    # def release_channel(self, channel):
    #     debug1 = self.components['KB'].input_data(release_freqs = channel)
    #     debug2 = self.components['KB'].start()

    #     if self.DEBUG:
    #         print "Release Channel"
    #         print "KB Input Result: ", hex(debug1)
    #         print "KB Start Result: ", hex(debug2)
    #         print

    # def request_channel(self, team_id):
    #     data = self.components['KB'].output_data()
        
    #     flag = -1 
    #     for user in data[1]:
    #         if user['id'] == team_id:
    #             flag = 0
    #             if user['skill'] == self.emphasis:
    #                 flag = 1

    #     if flag == -1:
    #         print "User with id %d not registered" % team_id
    #         return
        
    #     tmp1 = []
    #     tmp2 = []
    #     self.queue.append((team_id, flag))

    #     for pair in self.queue:
    #         if pair[1] == 1:
    #             tmp1.append(pair)
    #         else:
    #             tmp2.append(pair)

    #     self.queue = tmp1 + tmp2

    # def set_emphasis(self, emph):
    #     self.emphasis = emph
