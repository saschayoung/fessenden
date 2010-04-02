#!/usr/bin/env python

import numpy

class component:
    def __init__(self):
        self.freq_command_filename = "freq_commands"
        self.move_command_filename = "move_commands"
    
        f1 = open(self.freq_command_filename, 'w')
        f1.close()

        f1 = open(self.move_command_filename, 'w')
        f1.close()

        self.got_freq_string = "Team %d has been allocated frequency %f"
        self.booted_freq_string = "Team %d, please vacate your frequency"
        self.move_command_string = "%.15f,%.15f"

        self.freq_commands = []
        self.move_to_loc = None

    def start(self):
        self.work()

    def work(self):
        if self.freq_commands:
            if self.freq_commands[0]:
                if [tuple, list].count(type(self.freq_commands[0][0])) == 0:
                    self.freq_commands[0] = [self.freq_commands[0]]
                
                f1 = open(self.freq_command_filename, 'a')
                for pair in self.freq_commands[0]:
                    string = self.got_freq_string%(pair[0], pair[1])
                    f1.write(string)
                f1.close()

            if self.freq_commands[1]:
                if [tuple, list].count(type(self.freq_commands[1])) == 0:
                    self.freq_commands[1] = [self.freq_commands[1]]
                    
                f1 = open(self.freq_command_filename, 'a')
                for team_id in self.freq_commands[1]:
                    string = self.booted_freq_string%team_id
                    f1.write(string)
                f1.close()

        if self.move_to_loc:
            f1 = open(self.move_command_filename, 'a')
            string = self.move_command_string%(self.move_to_loc[0],self.move_to_loc[1])
            f1.write(string)
            f1.close()

    def input_data(self, freq_commands = None, move_to_loc = None):
        if freq_commands:
            #(got, booted)
            #got -> (id, freq)
            bad_type = True
            if not([tuple, list].count(type(freq_commands)) == 0):
                if len(freq_commands) > 1:
                    self.freq_commands = freq_commands
                    bad_type = False

            if bad_type:
                print "SDR Radio Error: Bad value for freq commands"
                print "Type: ", type(freq_commands)
                if not([tuple,list].count(type(freq_commands)) == 0):
                    print "Length: ", len(freq_commands)
                print "Value: ", freq_commands
                print

        if move_to_loc:
            bad_type = True
            if not([tuple, list].count(type(move_to_loc)) == 0):
                if len(move_to_loc) == 2:
                    # if not([float,long].count(type(move_to_loc[0])) == 0) and not([float,long].count(type(move_to_loc[1])) == 0):
                    self.move_to_loc = move_to_loc
                    bad_type = False

            if bad_type:
                print "SDR Radio Error: Bad value for move to loc"
                print "Type: ", type(move_to_loc)
                if not([tuple,list].count(type(move_to_loc)) == 0):
                    print "Length: ", len(move_to_loc)
                    for i in range(len(move_to_loc)):
                        string = "Element " + str(i) +" Type: " + str(type(move_to_loc[i]))
                        print string
                print "Value: ", move_to_loc

            
        
