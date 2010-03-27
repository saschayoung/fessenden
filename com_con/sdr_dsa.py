#!/usr/bin/env python

import threading, timer

class component:
    def __init__(self):
        self.emphasis = None
        self.queue = []
        self.booted_list = []

        self.release_requests = []
        self.acquire_requests = []

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


    def input_data(release_request = None, acquire_request = None):
        if release_requests:
            if not([int,float,tuple,list].count(type(release_requests)) == 0):
                self.release_requests = release_request
            else:
                print "SDR DSA Error: Bad type for release request"
                print "Type: ", type(release_request)
                print "Request: ", release_request

        if acquire_request:
            if not([tuple, list].count(type(acquire_request)) == 0):
                self.acquire_requests = acquire_request
            else:
                print "SDR DSA Error: Bad type for acquire request"
                print "Type: ", type(acquire_request)
                print "Request: ", acquire_request

    def process_acquire_requests(self):
        #(id, skill)
        
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
