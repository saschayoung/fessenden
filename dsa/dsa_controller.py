#!/usr/bin/env python

import threading

class controller():
    def __init__(self):
        self.components = {}

        self.msg_poster = None

        self.emphasis = None
        self.queue = []

        self.add_component('optimizer', 'dsa_optimizer')
        self.add_component('KB', 'dsa_know')

        self.time_thread = threading.Timer(15.0, self.check_channels)

        self.lock = threading.Lock()
        
        self.time_thread.start()

    def __del__(self):
        self.time_thread.join()

    def add_component(self, type, filename):
        keys = self.components.keys()
        if keys.count(type) == 0:
            module = __import__(filename)
            self.components[type] = module.component()

    def remove_component(self, type):
        keys = self.components.keys()
        if not(keys.count(type) == 0):
            del self.components[type]

    def check_channels(self):
        self.lock.acquire()
        for i in range(len(self.queue)):
            data = self.components['KB'].output_data()


            self.components['optimizer'].input_data(freqs=data[0], users=data[1], request=self.queue[i])
            self.components['optimizer'].start()
            result = self.components['optimizer'].output_data()


            if result > 0:
                #send vacate message 
                self.components['KB'].input_data(acquire_freqs = (self.queue[i][0], result))
                self.components['KB'].start()

        self.lock.release()

    def release_channel(self, channel):
        self.lock.acquire()
        self.components['KB'].input_data(release_freqs = channel)
        self.components['KB'].start()
        self.lock.release()

    def add_user(self, name, id, location, skill):
        self.lock.acquire()
        self.components['KB'].input_data(new_users = [name, id, location, skill])
        self.components['KB'].start()
        self.lock.release()

    def request_channel(self, team_id):
        self.lock.acquire()
        data = self.components['KB'].output_data()
        
        flag = -1 
        for user in data[1]:
            if user['id'] == team_id:
                flag = 0
                if user['skill'] == self.emphasis:
                    flag = 1

        if flag == -1:
            print "User with id %d not registered" % team_id
            self.lock.release()
            return
        
        tmp1 = []
        tmp2 = []
        self.queue.append((team_id, flag))

        for pair in self.queue:
            if pair[1] == 1:
                tmp1.append(pair)
            else:
                tmp2.append(pair)

        self.queue = tmp1 + tmp2
        self.lock.release()

    def set_poster(self, poster):
        self.msg_poster = poster

    def post_msg(self, msg):
        if not(self.msg_poster == None):
            self.msg_poster(msg)

if __name__ == '__main__':
    import time
    test = controller()
    test.add_user('bob', 42, [0,0], 'search')

    print 'Initial Spectral Map:'
    print test.components['KB']
    channel = test.request_channel(42)

    time.sleep(20)

    print '\nAfter Sleep:'
    print test.components['KB']

#     test.release_channel(42)
#     print '\nChannel Released:'
#     print test.components['KB']

    time.sleep(20)

    test.request_channel(42)
    print "\nSecond Request"
    print test.components['KB']
