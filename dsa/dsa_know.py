#!/usr/bin/env python

import wx
import threading, dsa_timer



class component():
    def __init__(self):
        self.users = []
        self.to_acquire = None
        self.to_release = None
        self.new_users = None
        

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
        
        self.time_thread = dsa_timer.ResettableTimer(10.0, self.age_channels, inc=1)
        
        self.lock = threading.Lock()
        
        self.time_thread.start()

    def __del__(self):
        self.time_thread.kill()

    def age_channels(self):
        self.lock.acquire()
        for i in range(len(self.freqs)):
            if self.freqs[i][1] > 0:
                self.freqs[i][1] += 1
            if self.freqs[i][1] < 0:
                self.freqs[i][2] -= 1
        self.lock.release()

    def start(self):
        return self.work()
    

    def work(self):
        acq = 0
        rel = 0
        add = 0
        up = 0

        if not(self.to_acquire == None):
            if not([int,float].count(type(self.to_acquire[0])) == 0):
                acq = self.acquire_freq(self.to_acquire[0], self.to_acquire[1])

            else:
                acq = 0
                for i in range(len(self.to_acquire)):
                    if not(type(self.to_acquire) is str):
                        mini_acq = self.acquire_freq(self.to_acquire[i][0], self.to_acquire[i][1])
                        if mini_acq == 0:
                            self.to_acquire[i] = ''
                        elif mini_acq < acq:
                            acq = mini_acq
                        
            if acq == 0:
                self.to_acquire = None

        if not(self.to_release == None):
            if not([int,float,long].count(type(self.to_release)) == 0):
                index = self.user_lookup(self.to_release)
                if index > -1:
                    rel = self.release_freq(self.users[index]['freq'])
                else:
                    rel = self.release_freq(self.to_release)
                
            elif type(self.to_release) is str:
                id = self.id_lookup(self.to_release)
                index = self.user_lookup(id)
                rel = self.release_freq(self.users[index]['freq'])

            else:
                rel = 0
                for i in range(len(self.to_release)):
                    if not(type(self.to_release[i]) is list):
                        if type(self.to_release[i]) is str:
                            id = self.id_lookup(self.to_release[i])
                            index = self.user_lookup(id)
                            mini_rel = self.release_freq(self.users[index]['freq'])
                        else:
                            index = self.user_lookup(self.to_release[i])
                            if index > 0:
                                mini_rel = self.release_freq(self.users[index]['freq'])
                            else:
                                mini_rel = self.release_freq(self.to_release[i])

                        if mini_rel == 0:
                            self.to_release[i] = []
                        elif mini_rel < rel:
                            rel = mini_rel
                
            if rel == 0:
                self.to_release = None


        if not(self.new_users == None):
            key_list = ['name', 'id', 'location', 'skill', 'bitrate', 'bandwidth', 'modulation']
            if not([tuple,list].count(type(self.new_users)) == 0):
                if type(self.new_users[0]) is str:
                    input_len = len(self.new_users)

                    tmp = {}
                    for i in range(len(key_list)):
                        if i < input_len:
                            tmp[key_list[i]] = self.new_users[i]
                        else:
                            tmp[key_list[i]] = None

                    add = self.add_user(tmp)

                elif not([tuple,list].count(type(self.new_users[0])) == 0):
                    add = 0
                    for i in range(len(self.new_users)):
                        if not(type(self.new_users[i]) is list):
                            input_len = len(self.new_users)

                            tmp = {}
                            for i in range(len(key_list)):
                                if i < input_len:
                                    tmp[key_list[i]] = self.new_users[i]
                                else:
                                    tmp[key_list[i]] = None

                            mini_add = self.add_user(tmp)

                            if mini_add == 0:
                                self.new_users[i] = []
                            elif mini_add < add:
                                add = mini_add
                                
                else:
                    add = 0
                    for i in range(len(self.new_users)):
                        if not(type(self.new_users[i]) is str):
                            user_keys = self.new_users[i].keys()
                            
                            diff_keys = list(set(key_list)-set(user_keys))

                            tmp = self.new_users[i]
                            
                            for key in diff_keys:
                                tmp[key] = None

                            mini_add = self.add_user(tmp)

                            if mini_add == 0:
                                self.new_users[i] = ''
                            elif mini_add < add:
                                add = mini_add

            else:
                user_keys = self.new_users.keys()
                
                diff_keys = list(set(key_list)-set(user_keys))

                tmp = self.new_users

                for key in diff_keys:
                    tmp[key] = None
                add = self.add_user(tmp)


            if add == 0:
                self.new_users = None

        if not(self.user_up == None):
            
            up = self.update_user()

        acq *= -1
        acq = acq << 12
        
        rel *= -1 
        rel = rel << 8
        
        add *= -1
        add = add << 4

        up *= -1 
        
        result = acq | rel | add | up

        return result
                                           

    def input_data(self, acquire_freqs=None, release_freqs=None, new_users=None, user_up = None):
        acq = 0
        rel = 0
        use = 0
        up = 0

        self.to_acquire = None
        self.to_release = None
        self.new_users = None
        self.user_up = None

        if not(acquire_freqs == None):
            if not([tuple,list].count(type(acquire_freqs)) == 0):
                recheck = True
                if len(acquire_freqs) == 2:
                    if not([int,float].count(type(acquire_freqs[0])) == 0):
                        recheck = False
                        if not([int,float,long].count(type(acquire_freqs[1])) == 0):
                            self.to_acquire = acquire_freqs
                        else:
                            acq = 1
                    else:
                        acq = 1
                        
                if recheck:
                    self.to_acquire = []
                    for item in acquire_freqs:
                        if [tuple,list].count(type(item)) == 0:
                            acq = 1
                            break
                        elif not(len(item) == 2):
                            acq = 1
                            break
                        elif [int,float].count(type(item[0])) == 0:
                            acq = 1
                            break
                        elif [int,float,long].count(type(item[1])) == 0:
                            acq = 1
                            break
                        else:
                            self.to_acquire.append(item)

                    if acq == 1:
                        self.to_acquire = None
            else:
                acq = 1

        if not(release_freqs == None):
            if not([int,float,long,tuple,list].count(type(release_freqs)) == 0):
                if not([int,float,long].count(type(release_freqs)) == 0):
                    self.to_release = release_freqs

                elif not([tuple,list].count(type(release_freqs)) == 0):
                    self.to_release = []
                    type_flag = 0
                    for item in release_freqs:
                        if [int,float,long,str].count(type(item)) == 0:
                            rel = 1
                            break
                        elif not([int,float,long].count(type(item)) == 0):
                            if not(type_flag == 2):
                                type_flag = 1
                            else:
                                rel = 1
                                break
                        elif type(item) is str:
                            if not(type_flag == 1):
                                type_flag = 2
                            else:
                                rel = 1
                                break
                        else:
                            self.to_release.append(item)

                    if rel == 1:
                        self.to_release = None
                else:
                    rel = 1
                            
            elif type(release_freqs) is str:
                self.to_release = release_freqs

            else:
                rel = 1



        if not(new_users == None):
            if not([tuple,list].count(type(new_users)) == 0):
                recheck = True
                if len(new_users) >= 4:
                    if type(new_users[0]) is str:
                        recheck = False
                        if not([int,float].count(type(new_users[1])) == 0):
                            if not([tuple,list].count(type(new_users[2])) == 0):
                                if type(new_users[3]) is str:
                                    self.new_users = new_users
                                else:
                                    use = 1
                            else:
                                use = 1
                        else: 
                            use = 1
                    else:
                        use = 1

                if recheck:
                    self.new_users = []
                    type_flag= 0
                    for item in new_users:
                        if not([tuple,list].count(type(item)) == 0):
                            if not(type_flag== 2):
                                type_flag= 1
                            else:
                                use = 1
                                break

                            if not(len(item) >= 4):
                                use = 1
                                break
                            elif not(type(item[0]) is str):
                                use = 1
                                break
                            elif [int,float].count(type(item[1])) == 0:
                                use = 1
                                break
                            elif [list,tuple].count(type(item[2])) == 0:
                                use = 1
                                break
                            elif not(type(item[3]) is str):
                                use = 1
                                break
                            else:
                                self.new_users.append(item)

                        elif type(item) is dict:
                            if not(type_flag== 1):
                                type_flag= 2
                            else:
                                use = 1
                                break

                            if item.keys().count('name') == 0:
                                use = 1
                                break
                            elif not(type(item['name']) is str):
                                use = 1
                                break
                            elif item.keys().count('id') == 0:
                                use = 1
                                break
                            elif [int,float].count(type(item['id'])) == 0:
                                use = 1
                                break
                            elif item.keys().count('location') == 0:
                                use = 1
                                break
                            elif [tuple,list].count(type(item['location'])) == 0:
                                use = 1
                                break
                            elif item.keys().count('skill') == 0:
                                use = 1
                                break
                            elif not(type(item['skill']) is str):
                                use = 1
                                break

                            else:
                                self.new_users.append(item)

                        else:
                            use = 1
                            break

                if use == 1:
                    self.new_users = None

            elif type(new_users) is dict:
                if item.keys().count('name') == 0:
                    use = 1
                elif not(type(item['name']) is str):
                    use = 1
                elif item.keys().count('id') == 0:
                    use = 1
                elif [int,float].count(type(item['id'])) == 0:
                    use = 1
                elif item.keys().count('location') == 0:
                    use = 1
                elif [tuple,list].count(type(item['location'])) == 0:
                    use = 1
                elif item.keys().count('skill') == 0:
                    use = 1
                elif not(type(item['skill']) is str):
                    use = 1

                else:
                    self.new_users = new_users

            else:
                use = 1

        if not(user_up == None):
            if type(user_up) is dict:
                keys = user_up.keys()
                if (keys.count('name') == 0) and (keys.count('id') == 0):
                    up = 1
                else:
                    self.user_up = user_up
            else:
                up = 1
                
        acq = acq << 12
        rel = rel << 8
        use = use << 4
        result = acq | rel | use | up

        return result

    def release_freq(self, freq):
        freq_found = False
        freq_open = True
        self.lock.acquire()
        for i in range(len(self.freqs)):
            if self.freqs[i][0] == freq:
                freq_found = True
                if self.freqs[i][1] < 0:
                    freq_open = False
                    user_id = self.freqs[i][1]*-1
                    self.freqs[i][1] = 1
                    self.freqs[i][2] = 0
                break
        self.lock.release()
        
        if not(freq_found):
            print "DSA Know Error: Frequency requested not found"
            print "Request: ", freq
            print "Choices: ", self.freqs
            return -2
        if freq_open:
            return -1
        else:
            index = self.user_lookup(user_id)
            self.users[index]['freq'] = None
            return 0        

    def acquire_freq(self, id, freq):
        if type(id) is str:
            num = self.id_lookup(id)
            if num == -1:
                print "DSA Know Error: User not recognized"
                print "Username: ", id
                return -3
            else:
                user_id = num
        elif not([int,float].count(type(id)) == 0):
            user_id = id
        else:
            print "DSA Know Error:  ID bad type"
            print "Type: ", type(id)
            print "ID: ", id
            return -3
        
        index = self.user_lookup(user_id)

        if index < 0:
            print "DSA Know Error: Unregistered user requesting frequecny"
            print "Given User Id: ", id
            print "Possible Users: ", self.users
            return -3

        if not(self.users[index]['freq'] == None):
            print "Double Count"
            print "User: ", self.users[index]
            return -1

        freq_found = False
        freq_open = False

        self.lock.acquire()
        for i in range(len(self.freqs)):
            if self.freqs[i][0] == freq:
                freq_found = True
#                 if self.freqs[i][1] > 0:
#                     freq_open = True
                self.freqs[i][1] = -1*user_id
                self.freqs[i][2] = self.channel_time
                break
        self.lock.release()

        if not(freq_found):
            print "DSA Know Error: Frequency requested not found"
            print "Request: ", freq
            print "Choices: ", self.freqs
            return -3
#         elif not(freq_open):
#             return -2
        else:
            index = self.user_lookup(user_id)
            self.users[index]['freq'] = freq
            return 0

    def add_user(self,user):
        if not(user['id']) or (user['id'] < 0):
            user['id'] = self.auto_id()

        user['freq'] = None

        if self.users.count(user) == 0:
            self.users.append(user)
            return 0
        else:
            return -1

#     def del_user(self, user_info):
#         if not(self.users.count(user_info) == 0):
#             self.users.pop(self.users.index(user_info))


    def update_user(self):
        keys = self.user_up.keys()
        
        index = 0
        recheck = True
        if not(keys.count('id') == 0):
            keys.remove('id')
            if self.user_up['id']:
                index = self.user_lookup(self.user_up['id'])
                recheck = False

        if recheck:
            id = self.id_lookup(self.user_up['name'])
            index = self.user_lookup(id)
            
        if not(keys.count('name') == 0):
            keys.remove('name')

            
        if index < 0:
            return -1

        old_keys = self.users[index].keys()
        
        for key in keys:
            if not(old_keys.count(key) == 0):
                self.users[index][key] = self.user_up[key]

        self.user_up = None

        return 0

    def user_lookup(self, id):
        index = -1
        for i in range(len(self.users)):
            if self.users[i]['id'] == id:
                index = i
                break
        return index

    def id_lookup(self, name):
        id = -1
        for user in self.users:
            if name == user['name']:
                id = user['id']
                break
        return id
               
    def auto_id(self):
        id = 1
        loop = True
        while loop:
            loop = False
            i = self.user_lookup(id)
            if i > -1:
                id += 1
                loop = True

        return id

    def output_data(self):
        self.lock.acquire()
        freqs = [k for k in self.freqs]
        self.lock.release()

        return [freqs, self.users]

    def get_name(self):
        '''
        lets the controller know what to put on the panel
        '''
        return "Knowledge Base"

    def __str__(self):
        '''
        Easy print method
        '''
        data = self.output_data()
        freqs = data[0]
        users = data[1]

        string = "########\nKB START\n"
        string += "Freq Listing: " + str(freqs)
        string += "\nUsers: " + str(users)
        string += "\nKB STOP\n########\n"        
        return string
        
    def get_current_values(self):
        return [self.output_data(),self.users]

    def get_panel(self, parent):
        '''
        Big gnarly GUI panel making function
        Abandon all hold yee who enter here
        '''
        panel = wx.Panel(parent, -1)
       
        return panel
    
if __name__ == '__main__':
    import time
    test = component()
    print test
    time.sleep(15)
    print test
