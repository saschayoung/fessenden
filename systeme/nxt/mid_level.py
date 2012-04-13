#!/usr/bin/env python

import random
import time
import threading

import eggs as spi


from io_utils import GeneralPurposeIO

from low_level import LowLevel 


# this timer thread is too slow, it takes to long to kill
class Timer(threading.Thread):
    def __init__(self, delay):
        self.delay = delay
        self.flag = threading.Event()
        threading.Thread.__init__(self)

    def run(self):
        time.sleep(self.delay)
        self.flag.set()

    def join(self, timeout=None):
        threading.Thread.join(self, timeout)



class RandomBackOff(object):

    def __init__(self):
        t = 0.0
        self.index = 0

    def run(self):
        self._sleep()
        self.index += 1
        print "random back off %i" %(self.index,)
        if (self.index < 5):
            return "continue"
        else:
            self._reset()
            return "break"
        
    def _sleep(self):
        t = random.random()
        time.sleep(t)

    def _reset(self):
        t = 0.0
        self.index = 0


class MidLevel(object):
    def __init__(self):
        self.rfm22 = LowLevel()
        self.backoff = RandomBackOff()


    def _init_io(self):
        """
        Initialize I/O.

        This function initializes the radio I/O, including SPI, GPIO,
        and IRQ line.
        """        
        interrupt = 157
        tx_port = 138
        rx_port = 139

        spi.setup("/dev/spidev4.0")

        # setup the TR switch
        self.tx_ant = GeneralPurposeIO(tx_port, "out")
        self.tx_ant.write(0)
        self.rx_ant = GeneralPurposeIO(rx_port, "out")
        self.rx_ant.write(0)

        # setup irq line
        self.irq = GeneralPurposeIO(interrupt, "in")



    def _kill_io(self):
        """
        Shutdown I/O.

        This function closes and ends the radio I/O including GPIO and
        IRQ line.
        """
        self.tx_ant.close()
        self.rx_ant.close()
        self.irq.close()



    def _init_rf(self):
        """
        Initialize RF.

        This function intitializes the RF parameters, resetting all
        RFM 22 registers, disabling all interrupts, and enabling a
        default configuration.
        """
        self.rfm22.reset_all_registers()
        self.rfm22.disable_interrupts()
        self.rfm22.default_setup()




    def _tx_rx_switch(self, mode):
        """
        Switch T/R mode.

        This function turns the transmit/receive switch to
        receive, transmit, or off.

        Parameters
        ----------
        mode : str
            Mode for T/R switch operation, one of `tx`, `rx`, or `off`.

        Raises
        ------
        KeyError
            if mode not in [`tx`, `rx`, `off`].
        """
        if mode not in ['tx', 'rx', 'off']:
            raise ValueError
        else:
            if mode == 'tx':
                self.rx_ant.write(0)
                self.tx_ant.write(1)
            elif mode == 'rx':
                self.tx_ant.write(0)
                self.rx_ant.write(1)
            elif mode == 'off':
                self.tx_ant.write(0)
                self.rx_ant.write(0)
            else:
                print "+++ Melon melon melon +++"

        

    def startup(self):
        """
        General radio initialization.

        This helper function initializes the I/O and RF.
        """
        self._init_io()
        self._init_rf()


    def shutdown(self):
        """
        General radio cleanup.

        This helper function cleans up and shuts down any open
        processes.
        """
        self._kill_io()


    def transmit(self, data, freq, DEBUG=True):
        """
        Transmit data packet. 

        This function takes data and loads it into the TX FIFO buffer for
        transmission over the air.

        Parameters
        ----------
        data : list
            Input list of data to be transmitted, each element of which is 8
            bits. Maximum list size is 64 elements.
        freq : float
            Operating (center) frequency for transmission.
        DEBUG : bool, optional
            Flag to turn on debug message printing .

        Raises
        ------
        IndexError
            if length of `data` is greater than 64.
        """
        if len(data) > 64:
            raise IndexError
        else:
            self.rfm22.set_op_mode('ready')

            self.rfm22.disable_interrupts()
            self.rfm22.clear_interrupts()
            self.rfm22.clear_tx_fifo()

            self.rfm22.set_frequency(freq)
            self.rfm22.load_tx_fifo(data)

            self._tx_rx_switch('tx')

            self.rfm22.enable_interrupt('packet_sent')
            self.rfm22.set_op_mode('tx')

            r = self.irq.read()
            while (int(r) == 1):
                r = self.irq.read()
            if DEBUG:
                print "packet sent"
                
            self._tx_rx_switch('off')
       





    def listen(self, freq, rssi_threshold=100, timeout=0.5, DEBUG=True):
        """
        Listen before talk.

        This function implements listen-before-talk or carrier
        sense. RSSI is used to determine if the frequency of interest
        is busy. Timeout is used to interrupt the listening process,
        returning a value of `busy` to the parent (calling) function.

        Parameters
        ----------
        freq : float
            Operating (center) frequency of interest.
        rssi_threshold : int, optional
            RSSI threshold for determining whether channel is clear. Default
            value is 100. This value is not a power value; for relationship
            between RSSI and power, see [RFM22].
        timeout : float, optional
            Timeout value in seconds.
        DEBUG : bool, optional
            Flag to turn on debug message printing.

        Returns
        -------
        out : str
            Frequency (channel) status, either `clear` or `busy`.

        References
        ----------
        .. [RFM22] Figure 31, pg 64, RFM22 Data sheet.
        """
        self.rfm22.set_op_mode('ready')

        self.rfm22.disable_interrupts()
        self.rfm22.clear_interrupts()
        self.rfm22.clear_rx_fifo()

        self.rfm22.set_frequency(freq)

        self._tx_rx_switch('rx')

        self.rfm22.set_op_mode('rx')


        time.sleep(0.01) # need a bit of time before we read rssi values

        rssi_level = float('{0:d}'.format(spi.read(0x26)))

        while (rssi_level >= 100):
            b = self.backoff.run()
            if (b == "continue"):
                rssi_level = float('{0:d}'.format(spi.read(0x26)))
                continue
            else: # (b == "break")
                self._tx_rx_switch('off')
                return 'busy'

        self._tx_rx_switch('off')
        return 'clear'



    def receive(self, freq, rx_fifo_threshold=17, timeout=None, DEBUG=True):
        """
        Receive data.

        This function receives data and does more stuff. TODO: Add
        more here. If `timeout` is none, then there is no time limit
        on how long to wait to receive a packet.

        Parameters
        ----------
        freq : float
            Operating (center) frequency of interest.
        rx_fifo_threshold : int, optional
            Value for RX Almost Full threshold. When the incoming RX data
            reaches the Almost Full Threshold an interrupt will be generated
            to the microcontroller via the nIRQ pin. The microcontroller
            will then need to read the data from the RX FIFO.
        timeout : float, optional
            Timeout value in seconds. Default value is 120.
        DEBUG : bool, optional
            Flag to turn on debug message printing.

        Returns
        -------
        rx_buffer : list
            Received data, from RX FIFO buffer.
        """
        self.rfm22.set_op_mode('ready')

        self.rfm22.disable_interrupts()
        self.rfm22.clear_interrupts()
        self.rfm22.clear_rx_fifo()

        self.rfm22.set_frequency(freq)
        self.rfm22.set_rx_fifo_almost_full_threshold(rx_fifo_threshold)

        self._tx_rx_switch('rx')

        self.rfm22.enable_interrupt('valid_packet_received')
        self.rfm22.set_op_mode('rx')


        if timeout == None:
            if DEBUG:
                print "waiting for packet..."
            r = self.irq.read()
            while (int(r) == 1): # interrupt is driven low when packet arrives
                r = self.irq.read()

            rx_buffer = []
            for i in range(rx_fifo_threshold):
                rx_buffer.append(spi.read(0x7F))
            return rx_buffer

        else:
            timer=Timer(timeout)
            timer.start()
            if DEBUG:
                print "waiting for packet..."
            r = self.irq.read()
            while (int(r) == 1): # interrupt is driven low when packet arrives
                if timer.flag.isSet():
                    timer.join()
                    del(timer)
                    if DEBUG:
                        print "Time out exceeded"                
                    return []
                else:
                    r = self.irq.read()
            # timer.join() # this doesn't seem necessary, and it takes
                           # a long time to execute O(1 sec) 
            # del(timer)
            rx_buffer = []
            for i in range(rx_fifo_threshold):
                rx_buffer.append(spi.read(0x7F))
            return rx_buffer






