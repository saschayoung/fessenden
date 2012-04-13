#!/usr/bin/env python



import os
import subprocess
import time


import eggs as spi


interrupt = 157
tx_port = 138
rx_port = 139




class RF(object):
    def __init__(self):
        spi.setup("/dev/spidev4.0")

        s = "echo " + str(tx_port) + " > /sys/class/gpio/export"
        result = subprocess.call(s, shell=True)
        s = "echo out > /sys/class/gpio/gpio" + str(tx_port) + "/direction"
        result = subprocess.call(s, shell=True)
        s = "echo 0 > /sys/class/gpio/gpio" + str(tx_port) + "/value"
        result = subprocess.call(s, shell=True)

        s = "echo " + str(rx_port) + " > /sys/class/gpio/export"
        result = subprocess.call(s, shell=True)
        s = "echo out > /sys/class/gpio/gpio" + str(rx_port) + "/direction"
        result = subprocess.call(s, shell=True)
        s = "echo 0 > /sys/class/gpio/gpio" + str(rx_port) + "/value"
        result = subprocess.call(s, shell=True)

        s = "echo " + str(interrupt) + " > /sys/class/gpio/export"
        result = subprocess.call(s, shell=True)




    def setup_rf(self):
        spi.write(0x07, 0x80)           # reset all the registers


        spi.write(0x05, 0x00)           # Disable interrupts in IntStatReg1
        spi.write(0x06, 0x00)           # Disable interrupts in IntStatReg2

        spi.write(0x07, 0x01) 		# Set READY mode
        spi.write(0x09, 0x7F) 		# Cap = 12.5pF
        spi.write(0x0A, 0x05) 		# Clk output is 2MHz
        spi.write(0x0B, 0xF4) 		# GPIO0 is for RX data output
        spi.write(0x0C, 0xEF) 		# GPIO1 is TX/RX data CLK output
        spi.write(0x0D, 0x00) 		# GPIO2 for MCLK output
        spi.write(0x0E, 0x00) 		# GPIO port use default value
        spi.write(0x0F, 0x70) 		# NO ADC used
        spi.write(0x10, 0x00) 		# no ADC used
        spi.write(0x12, 0x00) 		# No temp sensor used
        spi.write(0x13, 0x00) 		# no temp sensor used
        spi.write(0x70, 0x20) 		# No manchester code, no data whiting, data rate < 30Kbps
        spi.write(0x1C, 0x1D) 		# IF filter bandwidth
        spi.write(0x1D, 0x40) 		# AFC Loop
        spi.write(0x20, 0xA1) 		# clock recovery
        spi.write(0x21, 0x20) 		# clock recovery
        spi.write(0x22, 0x4E) 		# clock recovery
        spi.write(0x23, 0xA5) 		# clock recovery
        spi.write(0x24, 0x00) 		# clock recovery timing
        spi.write(0x25, 0x0A) 		# clock recovery timing
        spi.write(0x2C, 0x00) 
        spi.write(0x2D, 0x00) 
        spi.write(0x2E, 0x00) 
        spi.write(0x6E, 0x27) 		# TX data rate 1
        spi.write(0x6F, 0x52) 		# TX data rate 0
        spi.write(0x30, 0x8C) 		# Data access control
        spi.write(0x32, 0xFF) 		# Header control
        spi.write(0x33, 0x42) 		# Header 3, 2, 1, 0 used for head length,
                                        # fixed packet length, synchronize word length 3, 2,
        spi.write(0x34, 64) 		# 64 nibble = 32 byte preamble
        spi.write(0x35, 0x20) 		# 0x35 need to detect 20bit preamble
        spi.write(0x36, 0x2D) 		# synchronize word
        spi.write(0x37, 0xD4) 
        spi.write(0x38, 0x00) 
        spi.write(0x39, 0x00) 
        spi.write(0x3A, 0xff) 		# set tx header 3
        spi.write(0x3B, 0xff) 		# set tx header 2
        spi.write(0x3C, 0xff) 		# set tx header 1
        spi.write(0x3D, 0xff) 		# set tx header 0
        spi.write(0x3E, 17) 		# set packet length to 17 bytes
        spi.write(0x3F, 0xff) 		# set rx header
        spi.write(0x40, 0xff) 
        spi.write(0x41, 0xff) 
        spi.write(0x42, 0xff) 
        spi.write(0x43, 0xFF) 		# check all bits
        spi.write(0x44, 0xFF) 		# Check all bits
        spi.write(0x45, 0xFF) 		# check all bits
        spi.write(0x46, 0xFF) 		# Check all bits
        spi.write(0x56, 0x01) 
        spi.write(0x6D, 0x07) 		# Tx power to max
        spi.write(0x79, 0x00) 		# no frequency hopping
        spi.write(0x7A, 0x00) 		# no frequency hopping
        spi.write(0x71, 0x22) 		# GFSK, fd[8]=0, no invert for TX/RX data, FIFO mode, txclk-->gpio
        spi.write(0x72, 0x48) 		# Frequency deviation setting to 45K=72*625
        spi.write(0x73, 0x00) 		# No frequency offset
        spi.write(0x74, 0x00) 		# No frequency offset
        spi.write(0x75, 0x53) 		# frequency set to 434MHz
        spi.write(0x76, 0x64) 		# frequency set to 434MHz
        spi.write(0x77, 0x00) 		# frequency set to 434Mhz
        spi.write(0x5A, 0x7F) 
        spi.write(0x59, 0x40) 
        spi.write(0x58, 0x80) 
        spi.write(0x6A, 0x0B) 
        spi.write(0x68, 0x04) 
        spi.write(0x1F, 0x03)

        

    def tx_data(self):
        spi.write(0x07, 0x01)
        
        s = "echo 0 > /sys/class/gpio/gpio" + str(rx_port) + "/value"
        result = subprocess.call(s, shell=True)

        s = "echo 1 > /sys/class/gpio/gpio" + str(tx_port) + "/value"
        result = subprocess.call(s, shell=True)

        time.sleep(0.05)

        spi.write(0x08, 0x03)
        spi.write(0x08, 0x00)

        spi.write(0x34, 64) 	# preamble = 64nibble
        spi.write(0x3E, 17) 	# packet length = 17bytes


        ack = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
               0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
               0xff, 0xff, 0xff]


        for i in ack:
            spi.write(0x7F, i) 	# send payload to the FIFO

        spi.write(0x05, 0x04)   # enable packet sent interrupt
        
        i = spi.read(0x03)      # Read Interrupt status1 register
        i = spi.read(0x04)

        spi.write(0x07, 0x09)   # Start TX


        s = "cat /sys/class/gpio/gpio" + str(interrupt) + "/value"
        result = subprocess.check_output(s, shell=True)
        while ( int(result) == 1 ):
            print "interrupt == 1"
            result = subprocess.check_output(s, shell=True)

        if ( int(result) == 0 ):
            print "interrupt == 0"

        print "Register 0x03: ", '{0:08b}'.format(spi.read(0x03))
        print "Register 0x04: ", '{0:08b}'.format(spi.read(0x04))

        spi.write(0x07, 0x01)

        s = "echo 0 > /sys/class/gpio/gpio" + str(rx_port) + "/value"
        result = subprocess.call(s, shell=True)

        s = "echo 0 > /sys/class/gpio/gpio" + str(tx_port) + "/value"
        result = subprocess.call(s, shell=True)






    def rx_mode(self):
        spi.write(0x07, 0x01)     # Ready Mode
        
        s = "echo 0 > /sys/class/gpio/gpio" + str(tx_port) + "/value"
        result = subprocess.call(s, shell=True)

        s = "echo 1 > /sys/class/gpio/gpio" + str(rx_port) + "/value"
        result = subprocess.call(s, shell=True)

        time.sleep(0.05)

        self.rx_reset()






    def rx_reset(self):
        spi.write(0x07, 0x01)   # Ready Mode

        # Read Interrupt Registers to reset
        i = spi.read(0x03)      # IntStatReg1
        i = spi.read(0x04)      # IntStatReg2

        # Set RX FIFO Almost Full level: 17 bytes
        spi.write(0x7E, 17)    

        # Clear TX. RX FIFO Buffers
        spi.write(0x08, 0x03)  
        spi.write(0x08, 0x00)

        spi.write(0x07, 0x05)
        spi.write(0x05, 0x02)




    def run(self):
        tx_buf =[0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 
                 0x37, 0x38, 0x39, 0x3A, 0x3B, 0x3C, 0x3D,
                 0x3E, 0x3F, 0x78]

        self.setup_rf()

        self.rx_mode()

        print "Register 0x02: ", '{0:08b}'.format(spi.read(0x02))
        print "Register 0x03: ", '{0:08b}'.format(spi.read(0x03))
        print "Register 0x04: ", '{0:08b}'.format(spi.read(0x04))

        print "receiving packet..."
        while True:
            s = "cat /sys/class/gpio/gpio" + str(interrupt) + "/value"
            result = subprocess.check_output(s, shell=True)

            print "Register 0x02: ", '{0:08b}'.format(spi.read(0x02))
            print "Register 0x03: ", '{0:08b}'.format(spi.read(0x03))
            print "Register 0x04: ", '{0:08b}'.format(spi.read(0x04))

            print "interrupt: ", int(result)
            if ( int(result) == 0 ):
                rx_buffer = []

                for i in range(17):
                    rx_buffer.append(spi.read(0x7F))

                if ( rx_buffer == tx_buf ):
                    print "Packet Received"
                    time.sleep(1)
                    print "Sending ACK"
                    self.tx_data()
                    break

                spi.write(0x07, 0x01)

                self.rx_reset()

            reg = spi.read(0x02)
            if ( reg & 1 == 0 ):
                print ""
                print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                print "not in rx state !!!!"
                print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                print ""
                self.rx_reset()

                
            time.sleep(0.05)
            




            

    def close_gpio(self):
        s = "echo " + str(tx_port) + " > /sys/class/gpio/unexport"
        result = subprocess.call(s, shell=True)

        s = "echo " + str(rx_port) + " > /sys/class/gpio/unexport"
        result = subprocess.call(s, shell=True)

        s = "echo " + str(interrupt) + " > /sys/class/gpio/unexport"
        result = subprocess.call(s, shell=True)





if __name__=='__main__':
    try:
        radio = RF()
        radio.run()
        radio.close_gpio()
    except KeyboardInterrupt:
        radio.close_gpio()









        # spi.write(0x08, 0x03)
        # spi.write(0x08, 0x00)


        # spi.write(0x34, 64) 	# preamble = 64nibble
        # spi.write(0x3E, 17) 	# packet length = 17bytes




        # for i in tx_buf:
        #     spi.write(0x7F, i) 	# send payload to the FIFO

        # spi.write(0x05, 0x04)   # enable packet sent interrupt
        
        # i = spi.read(0x03)      # Read Interrupt status1 register
        # print "RF22_REG_03_INTERRUPT_STATUS1: ", hex(i) 

        # i = spi.read(0x04)
        # print "RF22_REG_04_INTERRUPT_STATUS2: ", hex(i)

        # spi.write(0x07, 0x09)   # Start TX




        # i = spi.read(0x03)      # Read Interrupt status1 register
        # print "RF22_REG_03_INTERRUPT_STATUS1: ", hex(i) 

        # i = spi.read(0x04)
        # print "RF22_REG_04_INTERRUPT_STATUS2: ", hex(i)


        # spi.write(0x07, 0x01)

        # s = "echo 0 > /sys/class/gpio/gpio" + str(rx_port) + "/value"
        # result = subprocess.call(s, shell=True)

        # s = "echo 0 > /sys/class/gpio/gpio" + str(tx_port) + "/value"
        # result = subprocess.call(s, shell=True)
        
