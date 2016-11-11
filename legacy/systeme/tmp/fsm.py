#!/usr/bin/env python


from test_graph import Graph


class FiniteStateMachine(object):

    def __init__(self):
        self.boot_up = True
        self.stop_signal = False


    def main(self):
        while self.stop_signal == False:
            if self.boot_up == True:
                self.return_to_beginning()
                self.current_node = 1
                self.boot_up = False

                
            if self.current_node == 1:
                self.before_traverse()
                self.traverse_path()
                self.after_traverse()
                self.current_node = 2

                
            elif self.current_node == 2:
                self.return_to_beginning()
                self.current_node = 1









    def before_traverse(self):
        # pull data
        # make decisions



    def traverse_path(self):
        # set parameters
        # turn RF on
        # turn MOT on
        # ie, GO!


    def after_traverse(self):
        # get results
        # store all data
        
    

    def return_to_beginning(self):
        # set motion to default parameters
        # don't turn on radio
        # move to beginning
