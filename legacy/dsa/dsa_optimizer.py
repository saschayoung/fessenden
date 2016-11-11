#!/usr/bin/env python

import random
import wx
import geo_utils


def range_random(base, upperbound):
    """
    a simple function that returns a random float
    return value can greater than or equal to base and 
    less than upperbound
    """
    random.seed()
    scale = upperbound - base
    return((random.random()*scale)+base)

class component():
    def __init__(self):
        """
        constructor
        initializes values used-impotant for lists and dictionaries
        provides a default value for self.generations
        """
        self.output = []

        self.freq_list = None
        self.users = None
        self.request = None
        
        self.threshold_distance = 500
        self.geo = geo_utils.geo_utils()

        self.panel = None


    def get_name(self):
        """
        returns a human readable name for this class
        """
        return "DSA Optimizer"

    def start(self):
        self.output = self.work()


    def stop(self):
        pass

    def work(self):
        max_pref = -9999
        max_index = index = 0
        for pair in self.freq_list:
            if pair[1] > max_pref:
                max_pref = pair[1]
                max_index = index
            index += 1
        
        if max_pref < 0:
            result = -1
        else:
            result = self.freq_list[max_index][0]

        if result == -1:
            if (not(self.users == None)) and (not(self.request == None)):
                for i in range(len(self.users)):
                    if self.users[i]['id'] == self.request[0]:
                        index = i
                        break
                
                for user in self.users:
                    distance = self.geo.distance(user['location'], self.users[index]['location'])
                    print "Distance: ", distance
                    print "Threshold: ", self.threshold_distance
                    print "User: ", user
                    print "Request: ", self.users[index]
                    print
                    if distance > self.threshold_distance:
                        result = user['freq']
                        break



        return result
    
    def input_data(self, freqs = None, users = None, request = None):
        self.freq_list = None
        self.users = None
        self.request = None

        if not(freqs == None):
            for i in range(len(freqs)):
                if freqs[i][1] < 0:
                    if freqs[i][2] < 1:
                        freqs[i][1] = -1*freqs[i][2]
            self.freq_list = freqs
        
        if not(users == None):
            self.users = users
            
        if not(request == None):
            self.request = request


    def output_data(self):
        return self.output

    def get_boundaries(self):
        pass
        
    def get_input_data_labels(self):
        pass
#         return {'scores':'dictionary', 'bounds':'dictionary_repeat'}

    def __str__(self):
        """
        debug string to print out the current values of various 
        """
        string = "########\nDSA OPTIMIZER START"
        string += "\nFreq List: " + str(self.freq_list)
        string += "\nOutput: " + str(self.output)
        string += "\nDSA OPTIMIZER END\n########\n"
        return string
        
    def get_current_values(self):
        """
        returns the major items used
        """
        return [self.freq_list, self.output]
    

            
    def get_panel(self, parent):
        """
        Large wxPanel making method
        """
        panel = wx.Panel(parent, -1)

        return panel
        
if __name__ == "__main__":
    print "Hi"








