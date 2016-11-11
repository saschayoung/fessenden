#!/usr/bin/env python


class parser:
    def __init__(self):
        self.filename = 'matlab_out'
        self.short_print = False
        

    def reset_containers(self):
        self.binary_packets = []
        self.decimal_packets = []
        self.delays = []
        self.original_packet_bin = None
        self.original_packet_dec = None
        self.tx_symbols = None
        self.rx_symbols = []

        self.bit_errors = []
        self.symbol_errors = []
        self.bit_error_average = None
        self.symbol_error_average = None
        self.num_correct_packets = None
        self.num_dropped = 0


    def read_file(self):
        self.reset_containers()

        f = open(self.filename, 'r')
        lines = f.readlines()
        f.close()
        
        counter = 0

        self.delays = []
        start = True
        tag = ''
        for line in lines:
            if (line[:3] == '***') and start:
                tag = line[3:].strip('\n')
                start = False
                counter = 8
                continue
            elif line[:3] == '***':
                start = True
                counter = 0
                continue
                
            if (line.strip('\n') == '###')and start:
                start = False
                counter = 0
                continue
            elif line.strip('\n') == '###':
                start = True
                continue

            if counter == 0:
                if line.strip('\n') == 'dropped':
                    self.num_dropped += 1
                    counter = 2
                    continue
                self.binary_packets.append(line.strip('\n'))
                counter = counter + 1
            elif counter == 1:
                self.delays.append(line.strip('\n'))
                counter = counter + 1
            elif counter == 8:
                counter = 0
                if tag == 'PKT':
                    self.original_packet_bin = line.strip('\n')
                elif tag == 'TX':
                    tmp = line.strip('\n').split('::')
                    tmp.pop()
                    self.tx_symbols = tmp
                elif tag == 'RX':
                    tmp = line.strip('\n').split('::')
                    tmp.pop()
                    self.rx_symbols.append(tmp)

                
            if line.strip('\n') == '###':
                counter = 0

    def translate_packets(self):
        tmp = []
        for packet in self.binary_packets:
           packet_num = packet[0:16];
           packet_num = self.bin_str2dec(packet_num)

           beacon_num = packet[16:32]
           beacon_num = self.bin_str2dec(beacon_num)

           tmp.append([packet_num,beacon_num])

        if self.original_packet_bin:
            packet_num = self.original_packet_bin [0:16]
            packet_num = self.bin_str2dec(packet_num)

            beacon_num = self.original_packet_bin[16:32]
            beacon_num = self.bin_str2dec(beacon_num)
            self.original_packet_dec = [packet_num, beacon_num]

        self.decimal_packets = [k for k in tmp]

    def __str__(self):
        string = ''
        if not(self.short_print):
            if self.original_packet_dec:
                string += "Original Packet Data\n"
                string += "Beacon Packet Number:\t%d\n"%self.original_packet_dec[0]
                string += "Beacon Id Number:\t%d\n"%self.original_packet_dec[1]
                string += "\n"

            num = 0
            for item in self.decimal_packets:
                string += "RX Number\t\t%d\n"%num
                string += "Beacon Packet Number:\t%d\n"%item[0]
                string += "Beacon Id Number:\t%d\n"%item[1]
                if self.bit_errors:
                    string += "Bit Errors:\t\t%d\n"%self.bit_errors[num]
                if self.symbol_errors:
                    string += "Symbol Errors:\t\t%d\n"%self.symbol_errors[num]
                string +="\n"
                num += 1


            if self.tx_symbols:
                string += "Sample of Tx Symbols: " + str(self.tx_symbols[:15]) + '\n\n'

            if self.rx_symbols:
                string += "Sample of Rx Symbols: " + str(self.rx_symbols[0][:15]) + '\n\n'
                                                         
        if not(self.bit_error_average == None):
            string += "Bit Error Average:\t\t\t%.2f\n"%self.bit_error_average
            string += "Total Bits per Packet:\t\t\t%d\n"%len(self.binary_packets[0].strip('\n'))
            string += "Average Percent of Bit Errors:\t\t%.2f"%(self.bit_error_average/
                                                                len(self.binary_packets[0].strip('\n'))*100)
            string += "%\n\n"

        if not(self.symbol_error_average == None):
            string += "Symbol Error Average:\t\t\t%.2f\n"%self.symbol_error_average
            string += "Total Symbols Sent:\t\t\t%d\n"%len(self.tx_symbols)
            string += "Average Percent of Symbol Errors:\t%.2f"%(self.symbol_error_average/
                                                                 len(self.tx_symbols)*100)
            string += "%\n\n"

        if not(self.num_correct_packets == None):
            string += "Number of Correct Packets:\t\t%d\n"%self.num_correct_packets
            string += "Total Number of Packets:\t\t%d\n"%(len(self.decimal_packets)+self.num_dropped)
            string += "Percent of Correct Packets:\t\t%.2f"%((float(self.num_correct_packets)/
                                                              (len(self.decimal_packets)+self.num_dropped))*100)
            string += "%\n\n"

        return string

    def count_errors(self):
        if self.original_packet_bin:
            self.num_correct_packets = 0
            for item in self.binary_packets:
                tmp = self.get_num_mismatch(item, self.original_packet_bin)
                self.bit_errors.append(tmp)
                if tmp == 0:
                    self.num_correct_packets += 1

        # if self.tx_symbols and self.rx_symbols:
        #     for item in self.rx_symbols:
        #         self.symbol_errors.append(self.get_num_mismatch(item, self.tx_symbols))

        if self.bit_errors:
            self.bit_error_average = float(sum(self.bit_errors)/len(self.bit_errors))

        # if self.symbol_errors:
        #     self.symbol_error_average = float(sum(self.symbol_errors))/len(self.symbol_errors)


    def get_num_mismatch(self, list1, list2):
        if not(len(list1) == len(list2)):
            print "Len(list1): ", len(list1)
            print "Len(list2): ", len(list2)
            return -1
        
        num = 0
        for i in range(len(list1)):
            if not(list1[i] == list2[i]):
                num += 1

        return num


    def bin_str2dec(self, str):
        length = len(str)

        i = 1
        num = 0
        brush = 1
        while i <= length:
            num += int(str[length - i])*brush
            brush = brush << 1
            i += 1

        return num

    def output_packets(self):
        return self.packets

    def work(self):
        self.read_file()
        self.translate_packets()
        self.count_errors()

    def set_filename(self, filename):
        self.filename = filename

    def set_short_print(self, bool):
        self.short_print = bool
        
if __name__ == '__main__':
    test = parser()
    list1 = [0,1,2,3,4]
    list2 = [0,1,2,3,4]
    test.work()
    print test

