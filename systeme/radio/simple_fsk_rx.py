#!/usr/bin/env python
"""
A `simple` FSK radio.

"""


import time

# import rf22_registers as rf22_reg

import eggs as spi
import freq_utils

from base_class import RadioBaseClass
from io_utils import GeneralPurposeIO as gpio





class SimpleRadio(RadioBaseClass):
    def __init__(self):
        nint_port = 157
        tx_port = 138
        rx_port = 139

        spi.setup("/dev/spidev4.0")

        # setup the TR switch
        self.tx_ant = gpio(tx_port, "out")
        self.tx_ant.write(0)

        self.rx_ant = gpio(rx_port, "out")
        self.rx_ant.write(0)

        # setup irq line
        self.irq = gpio(nint_port, "in")




    def setup_rf(self, fc, hbsel, fb):
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
        spi.write(0x70, 0x0C) 		# No manchester code, no data whiting, data rate < 30Kbps
        spi.write(0x1C, 0x8A) 		# IF filter bandwidth
        spi.write(0x1D, 0x40) 		# AFC Loop
        spi.write(0x20, 0x60) 		# clock recovery
        spi.write(0x21, 0x01) 		# clock recovery
        spi.write(0x22, 0x55) 		# clock recovery
        spi.write(0x23, 0x55) 		# clock recovery
        spi.write(0x24, 0x02) 		# clock recovery timing
        spi.write(0x25, 0xAD) 		# clock recovery timing
        spi.write(0x2C, 0x40) 
        spi.write(0x2D, 0x0A) 
        spi.write(0x2E, 0x50) 
        spi.write(0x6E, 0x20) 		# TX data rate 1
        spi.write(0x6F, 0x00) 		# TX data rate 0
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
        # spi.write(0x6D, 0x04) 		# Tx power to max
        spi.write(0x6D, 0x07) 		# Tx power to max
        spi.write(0x79, 0x00) 		# no frequency hopping
        spi.write(0x7A, 0x00) 		# no frequency hopping
        spi.write(0x71, 0x22) 		# GFSK, fd[8]=0, no invert for TX/RX data, FIFO mode, txclk-->gpio
        spi.write(0x72, 0xc8) 		# Frequency deviation setting to 45K=72*625
        spi.write(0x73, 0x00) 		# No frequency offset
        spi.write(0x74, 0x00) 		# No frequency offset

        val = 0x40 | hbsel << 5 | fb
        spi.write(0x75, val) 		# frequency set to 434MHz
        spi.write(0x76, fc >> 8) 		# frequency set to 434MHz
        spi.write(0x77, fc & 0xff) 		# frequency set to 434Mhz

        

        spi.write(0x5A, 0x7F) 
        spi.write(0x59, 0x60) 
        spi.write(0x58, 0x80) 
        spi.write(0x6A, 0x0B) 
        spi.write(0x68, 0x04) 
        spi.write(0x1F, 0x03)

        # spi.write(0x07, 0x80)           # reset all the registers
        # spi.write(0x05, 0x00)           # Disable interrupts in IntStatReg1
        # spi.write(0x06, 0x00)           # Disable interrupts in IntStatReg2

        # spi.write(0x07, 0x01) 		# Set READY mode
        # spi.write(0x09, 0x7F) 		# Cap = 12.5pF
        # spi.write(0x0A, 0x05) 		# Clk output is 2MHz
        # spi.write(0x0B, 0xF4) 		# GPIO0 is for RX data output
        # spi.write(0x0C, 0xEF) 		# GPIO1 is TX/RX data CLK output
        # spi.write(0x0D, 0x00) 		# GPIO2 for MCLK output
        # spi.write(0x0E, 0x00) 		# GPIO port use default value
        # spi.write(0x0F, 0x70) 		# NO ADC used
        # spi.write(0x10, 0x00) 		# no ADC used
        # spi.write(0x12, 0x00) 		# No temp sensor used
        # spi.write(0x13, 0x00) 		# no temp sensor used
        # spi.write(0x70, 0x20) 		# No manchester code, no data whiting, data rate < 30Kbps
        # spi.write(0x1C, 0x1D) 		# IF filter bandwidth
        # spi.write(0x1D, 0x40) 		# AFC Loop
        # spi.write(0x20, 0xA1) 		# clock recovery
        # spi.write(0x21, 0x20) 		# clock recovery
        # spi.write(0x22, 0x4E) 		# clock recovery
        # spi.write(0x23, 0xA5) 		# clock recovery
        # spi.write(0x24, 0x00) 		# clock recovery timing
        # spi.write(0x25, 0x0A) 		# clock recovery timing
        # spi.write(0x2C, 0x00) 
        # spi.write(0x2D, 0x00) 
        # spi.write(0x2E, 0x00) 
        # spi.write(0x6E, 0x27) 		# TX data rate 1
        # spi.write(0x6F, 0x52) 		# TX data rate 0
        # spi.write(0x30, 0x8C) 		# Data access control
        # spi.write(0x32, 0xFF) 		# Header control
        # spi.write(0x33, 0x42) 		# Header 3, 2, 1, 0 used for head length,
        #                                 # fixed packet length, synchronize word length 3, 2,
        # spi.write(0x34, 64) 		# 64 nibble = 32 byte preamble
        # spi.write(0x35, 0x20) 		# 0x35 need to detect 20bit preamble
        # spi.write(0x36, 0x2D) 		# synchronize word
        # spi.write(0x37, 0xD4) 
        # spi.write(0x38, 0x00) 
        # spi.write(0x39, 0x00) 
        # spi.write(0x3A, 0xff) 		# set tx header 3
        # spi.write(0x3B, 0xff) 		# set tx header 2
        # spi.write(0x3C, 0xff) 		# set tx header 1
        # spi.write(0x3D, 0xff) 		# set tx header 0
        # spi.write(0x3E, 17) 		# set packet length to 17 bytes
        # spi.write(0x3F, 0xff) 		# set rx header
        # spi.write(0x40, 0xff) 
        # spi.write(0x41, 0xff) 
        # spi.write(0x42, 0xff) 
        # spi.write(0x43, 0xFF) 		# check all bits
        # spi.write(0x44, 0xFF) 		# Check all bits
        # spi.write(0x45, 0xFF) 		# check all bits
        # spi.write(0x46, 0xFF) 		# Check all bits
        # spi.write(0x56, 0x01) 
        # # spi.write(0x6D, 0x04) 		# Tx power to max
        # spi.write(0x6D, 0x07) 		# Tx power to max
        # spi.write(0x79, 0x00) 		# no frequency hopping
        # spi.write(0x7A, 0x00) 		# no frequency hopping
        # spi.write(0x71, 0x22) 		# GFSK, fd[8]=0, no invert for TX/RX data, FIFO mode, txclk-->gpio
        # spi.write(0x72, 0x48) 		# Frequency deviation setting to 45K=72*625
        # spi.write(0x73, 0x00) 		# No frequency offset
        # spi.write(0x74, 0x00) 		# No frequency offset

        # val = 0x40 | hbsel << 5 | fb
        # spi.write(0x75, val) 		# frequency set to 434MHz
        # spi.write(0x76, fc >> 8) 		# frequency set to 434MHz
        # spi.write(0x77, fc & 0xff) 		# frequency set to 434Mhz

        # spi.write(0x5A, 0x7F) 
        # spi.write(0x59, 0x40) 
        # spi.write(0x58, 0x80) 
        # spi.write(0x6A, 0x0B) 
        # spi.write(0x68, 0x04) 
        # spi.write(0x1F, 0x03)




    def clear_tx_fifo(self):
        spi.write(0x08, 0x01)
        spi.write(0x08, 0x00)


    def clear_rx_fifo(self):
        spi.write(0x08, 0x02)
        spi.write(0x08, 0x00)


    def clear_fifo(self):
        spi.write(0x08, 0x03)
        spi.write(0x08, 0x00)


    def clear_interrupt(self):
        i = spi.read(0x03)    
        i = spi.read(0x04)
        

    def set_mode(self, mode):
        if mode in ["ready", "tx", "rx"]:
            if mode == "ready":
                spi.write(0x07, 0x01)
            elif mode == "tx":
                spi.write(0x07, 0x09)
            else: # mode == "rx"
                spi.write(0x07, 0x05)
        else:
            raise ValueError("set_mode(mode): mode must be one of ['ready', 'tx', 'rx']")






    def rx_mode(self):
        self.set_mode("ready")
        self.rx_ant.write(1)
        self.tx_ant.write(0)
        time.sleep(0.05)
        self.rx_reset()






    def rx_reset(self):
        spi.write(0x07, 0x01)   # Ready Mode

        self.clear_interrupt() # Read Interrupt Registers to reset


        # Set RX FIFO Almost Full level: 17 bytes
        spi.write(0x7E, 17)    

        # Clear TX. RX FIFO Buffers
        spi.write(0x08, 0x03)  
        spi.write(0x08, 0x00)

        spi.write(0x07, 0x05)
        spi.write(0x05, 0x02)




    def run(self, freq):
        fc, hbsel, fb = freq_utils.carrier_freq(freq)

        print "changing to freq: ", freq
        self.setup_rf(fc, hbsel, fb)

        while True:
            self.tx_data()
            print "transmitted packet"
            time.sleep(0.1)



    def close_gpio(self):
        self.tx_ant.close()
        self.rx_ant.close()
        self.irq.close()
            



if __name__=='__main__':
    try:
        radio = SimpleRadio()
        # radio.sweep()
        radio.run(434e6)
        radio.close_gpio()
    except KeyboardInterrupt:
        radio.close_gpio()
















    # def tx_data(self):
    #     spi.write(0x07, 0x01)
        
    #     self.rx_ant.write(0)
    #     self.tx_ant.write(1)

    #     time.sleep(0.05)

    #     self.clear_fifo()

    #     tx_buf =[0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 
    #              0x37, 0x38, 0x39, 0x3A, 0x3B, 0x3C, 0x3D,
    #              0x3E, 0x3F, 0x78]


    #     for i in tx_buf:
    #         spi.write(0x7F, i) 	# send payload to the FIFO

    #     spi.write(0x05, 0x04)   # enable packet sent interrupt
        

    #     self.clear_interrupt()
        
    #     spi.write(0x07, 0x09)   # Start TX


    #     result = self.irq.read()
    #     while ( int(result) == 1 ):
    #         result = self.irq.read()


    #     self.rx_ant.write(0)
    #     self.tx_ant.write(0)
        


    def sweep(self):
        f = 295e6
        freqs = []

        while f < 930e6:
            freqs.append(f)
            f += 10e6

        for i in freqs:
            fc, hbsel, fb = freq_utils.carrier_freq(i)
            print "changing to freq: ", i
            for j in range(10):
                self.setup_rf(fc, hbsel, fb)
                self.tx_data()
                print "transmitted packet"
                time.sleep(0.01)
