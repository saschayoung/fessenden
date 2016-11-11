#! /usr/bin/env python

import os, matlab_parse, random

class chan_test:
    def __init__(self):
        self.packet_num = 0
        self.beacon_id = 42
        self.num_rx = 20
        self.chan_mode = 1
        self.code = 0
        self.matlab_filename = 'matlab_out'
        self.log_filename = 'matlab_test_log'

        self.parser = matlab_parse.parser()

        # self.test_profile=[{'num_rx':20, 'chan_mode':0, 'packet_num':0, 'name':'Default', 'num_tests':5, 'code':0}]
        self.test_profile = []

        self.num_random_tests = 0

    def set_num_rx(self, num):
        self.num_rx = num
    
    def run_matlab(self,file_mod = ''):
        filename=self.matlab_filename + str(file_mod)
        string = 'matlab -nojvm -nodesktop -nosplash -nodisplay -r \"rx_link(%d,%d, %d,0,%d,\''%(self.num_rx,
                                                                                                 self.chan_mode,
                                                                                                 self.code,
                                                                                                 self.packet_num)
        string += filename+'\',0,1,1)\"'


        header = '/software/matlab-2009b/bin/'
        string = header+string

        os.system(string)

    def collect_data(self,file_mod = ''):
        filename = self.matlab_filename + str(file_mod)
        self.parser.set_filename(filename)
        self.parser.work()

        if len(str(file_mod)):
            spacer = (('~'+str(file_mod)+'~')*15)+'\n'
        else:
            spacer = ''

        f = open(self.log_filename, 'a')
        f.write(spacer)
        f.write(str(self.parser))
        f.write('\n\n')
        f.close()

    def write_test_header(self, test_name):
        string = ('#'*50) + '\n'
        string += "Test Name:\t\t" + str(test_name) +'\n'
        string += "Number of Receivers:\t%d\n"%self.num_rx
        string += "Channel Mode Used:\t%d\n"%self.chan_mode
        string += "Number of Times Tested:\t%d\n"%self.num_tests
        if self.code:
            string += "BCH Coding Used\n\n"
        else:
            string += "BCH Coding Not Used\n\n"

        f = open(self.log_filename, 'a')
        f.write(string)
        f.close()

    def work(self):
        self.parser.set_short_print(True)
        self.clear_files()
        test_num = 0
        for item in self.test_profile:
            test_num += 1
            self.num_rx = item['num_rx']
            self.chan_mode = item['chan_mode']
            self.packet_num = item['packet_num']
            self.num_tests = item['num_tests']
            self.code = item['code']

            self.write_test_header(item['name'])
            
            for i in range(self.num_tests):
                file_mod = str(test_num) +'_'+ str(i+1)
                self.run_matlab(file_mod)
                self.collect_data(file_mod)

    def add_test(self, num_rx, chan_mode, packet_num, name, num_tests, code):
        tmp = {'num_rx':num_rx, 'chan_mode':chan_mode, 'packet_num':packet_num, 'name':name,
               'num_tests':num_tests, 'code':code}
        self.test_profile.append(tmp)

    def add_random_tests(self, num2add):
        max_rx = 100
        min_rx = 1

        max_chan = 17
        min_chan = 0

        max_num = 9999
        min_num = 0

        max_tests = 1
        min_tests = 1

        max_code = 1
        min_code = 0

        for i in range(num2add):
            self.num_random_tests += 1
            num_rx = random.randrange(min_rx, max_rx+1)
            chan = random.randrange(min_chan, max_chan+1)
            num = random.randrange(min_num, max_num+1)
            tests = random.randrange(min_tests, max_tests+1)
            code = random.randrange(min_code, max_code+1)

            name = "Random Test #", self.num_random_tests

            self.add_test(num_rx,chan,num,name,tests,code)

    def clear_tests(self):
        self.test_profile = []

    def clear_files(self):
        string = "rm " +self.matlab_filename+'*; rm '+self.log_filename
        os.system(string)

        
        for i in range(len(self.test_profile)):
            num_tests = self.test_profile[i]['num_tests']

            for j in range(num_tests):
                filename  = self.matlab_filename + str(i+1) +'_'+ str(j+1)
                f = open(filename,'w')
                f.close()
        

if __name__ == '__main__':
    test = chan_test()
    for i in range(17):
        test.add_test(100,i+1,0,'Chan Mode '+str(i+1),1, 1)

    test.work()
