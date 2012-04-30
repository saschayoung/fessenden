#!/usr/bin/env python

from mid_level import MidLevel


class NodeA(object):
    def __init__(self):
        self.radio = MidLevel()
        self.flag_node_a_freq_change_req = False
        self.flag_node_a_freq_change_ack = False

    def startup(self):
        self.radio.startup()

    def shutdown(self):
        self.radio.shutdown()


    def _listen(self, freq):
        status = self.radio.listen(freq, rssi_threshold=100, timeout=1.0)
        if status == 'clear':
            print "channel clear"
    


    def _receive(self, freq):
        ack = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
               0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
               0xff, 0xff, 0xff]
        packet = self.radio.receive(freq, rx_fifo_threshold=17, timeout=2.0)
        if packet == []:
            return
        else:
            if (packet[0] == 0xff):
                print "ACK received"
            if (packet[0] == 0x01):
                print "change freq request acknowledged"
                self.flag_node_a_freq_change_ack = True
            



    def _transmit(self, freq):
        data = [0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 
                0x37, 0x38, 0x39, 0x3A, 0x3B, 0x3C, 0x3D,
                0x3E, 0x3F, 0x78]
        if self.flag_node_a_freq_change_req == True:
            print "requesting frequency change"
            data[0] = 0x01
        self.radio.transmit(data, freq)



    def fsm(self):
        """
        Primary control loop.

        This function is the finite state machine that controls the
        operation of the system.
        """

        self.startup()

        packet_counter = 1
        state = "listen"
        # f = 434e6
        f = [431e6, 432e6, 433e6, 434e6, 435e6, 436e6, 437e6, 438e6, 439e6]
        g = 0


        while True:
            print "set frequency to %d" %(f[g],)
            if packet_counter % 30 == 0:
                self.flag_node_a_freq_change_req = True
                
            if state == "listen":
                self._listen(f[g])
                state = "transmit"

            elif state == "transmit":
                self._transmit(f[g])
                packet_counter += 1
                state = "receive"

            elif state == "receive":
                self._receive(f[g])
                state = "listen"

            else:
                print "+++ Melon melon melon +++"
                state = "listen"

            if ((self.flag_node_a_freq_change_req == True)  
                and (self.flag_node_a_freq_change_ack == True)):
                
                self.flag_node_a_freq_change_req = False
                self.flag_node_a_freq_change_ack = False
                g += 1
                if (g == 9):
                    g = 0




if __name__=='__main__':

    try:
        main = NodeA()
        main.fsm()
        main.shutdown()
    except KeyboardInterrupt:
        main.shutdown()



# import os
# import random
# import sys
# import time
# import threading

# import eggs as spi
# import freq_utils

# from io_utils import GeneralPurposeIO

# from new_rf_module import RFM22

# class Timer(threading.Thread):
#     def __init__(self, delay):
#         self.delay = delay
#         self.timer_event = threading.Event()
#         # self.stop_event = threading.Event()
#         threading.Thread.__init__(self)


#     def run(self):
#         time.sleep(self.delay)
#         self.timer_event.set()


#     def join(self, timeout=None):
#         threading.Thread.join(self, timeout)





# class RF(object):
#     def __init__(self):
#         self.rfm22 = RFM22()
#         self.back_off = RandomBackOff()
#         # self.rssi_threshold = 100


#     def _init_io(self):
#         interrupt = 157
#         tx_port = 138
#         rx_port = 139

#         spi.setup("/dev/spidev4.0")

#         # setup the TR switch
#         self.tx_ant = GeneralPurposeIO(tx_port, "out")
#         self.tx_ant.write(0)
#         self.rx_ant = GeneralPurposeIO(rx_port, "out")
#         self.rx_ant.write(0)

#         # setup irq line
#         self.irq = GeneralPurposeIO(interrupt, "in")


#     def _kill_io(self):
#         self.tx_ant.close()
#         self.rx_ant.close()
#         self.irq.close()


#     def _init_rf(self):
#         self.rfm22.reset_all_registers()
#         self.rfm22.disable_interrupts()
#         self.rfm22.default_rf22_setup()


#     def _listen(self, freq):
#         self.rfm22.set_frequency(freq)
#         self.rfm22.disable_interrupts()
#         self.rfm22.set_op_mode('ready')
#         self.tx_ant.write(0)
#         self.rx_ant.write(1)
#         self.rfm22.clear_rx_fifo()
#         self.rfm22.clear_interrupts()
#         self.rfm22.set_op_mode('rx')
#         time.sleep(0.01) # need a bit of time before we read rssi values
#         rssi_level = float('{0:d}'.format(spi.read(0x26)))
#         while (rssi_level >= 100):
#             b = self.back_off.run()
#             if (b == "continue"):
#                 continue
#             else: # (b == "break")
#                 keep_looping = False
#                 break



        
#     def _receive(self, freq):
#         time_out = Timer(2.0)
#         ack = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
#                0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
#                0xff, 0xff, 0xff]
#         self.rfm22.set_frequency(freq)
#         self.rfm22.disable_interrupts()
#         self.rfm22.set_op_mode('ready')
#         self.tx_ant.write(0)
#         self.rx_ant.write(1)
#         self.rfm22.clear_rx_fifo()
#         self.rfm22.clear_interrupts()
#         self.rfm22.set_rx_fifo_almost_full_threshold(17)
#         self.rfm22.enable_interrupt('valid_packet_received')
#         self.rfm22.set_op_mode('rx')

#         print "waiting for ACK..."
#         r = self.irq.read()
#         time_out.start()
#         while (int(r) == 1):
#             if time_out.timer_event.isSet():
#                 time_out.join()
#                 del(time_out)
#                 print "Time out exceeded"                
#                 return
#             else:
#                 r = self.irq.read()
#         rx_buffer = []
#         for i in range(17):
#             rx_buffer.append(spi.read(0x7F))
#         if (rx_buffer == ack):
#             print "ACK Received"




#     def _transmit(self, freq):
#         data = [0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 
#                 0x37, 0x38, 0x39, 0x3A, 0x3B, 0x3C, 0x3D,
#                 0x3E, 0x3F, 0x78]

#         self.rfm22.set_frequency(freq)
#         self.rfm22.disable_interrupts()
#         self.rfm22.set_op_mode('ready')
#         self.rx_ant.write(0)
#         self.tx_ant.write(1)
#         self.rfm22.clear_tx_fifo()
#         self.rfm22.load_tx_fifo(data)
#         self.rfm22.enable_interrupt('packet_sent')
#         self.rfm22.clear_interrupts()
#         self.rfm22.set_op_mode('tx')

#         r = self.irq.read()
#         while (int(r) == 1):
#             r = self.irq.read()
#         print "packet sent"
        
#         self.rx_ant.write(0)
#         self.tx_ant.write(0)


#     def run(self):
#         pass
        


#     def fsm(self):
#         """
#         Primary control loop.

#         This function is the finite state machine that controls the
#         operation of the system.
#         """

#         self._init_io()
#         self._init_rf()

#         state = "listen"
#         f = 434e6

#         while True:
#             if state == "listen":
#                 self._listen(f)
#                 state = "transmit"

#             elif state == "transmit":
#                 self._transmit(f)
#                 state = "receive"

#             elif state == "receive":
#                 self._receive(f)
#                 state = "listen"

#             else:
#                 print "+++ Melon melon melon +++"
#                 state = "listen"
            
        




#     def shutdown(self):
#         self._kill_io()






# class RandomBackOff(object):

#     def __init__(self):
#         t = 0.0
#         self.index = 0

#     def run(self):
#         self._sleep()
#         self.index += 1
#         print "random back off %i" %(self.index,)
#         if (self.index < 5):
#             return "continue"
#         else:
#             self._reset()
#             return "break"
        
#     def _sleep(self):
#         t = random.random()
#         time.sleep(t)

#     def _reset(self):
#         t = 0.0
#         self.index = 0


# if __name__=='__main__':

#     try:
#         radio = RF()
#         radio.fsm()
#         radio.shutdown()
#     except KeyboardInterrupt:
#         radio.shutdown()


