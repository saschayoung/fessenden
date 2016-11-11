#!/usr/bin/env python


import numpy as np


class RadioObjectives(object):

    def __init__(Self):
        pass



    def calculate_ber(self, rssi, EIRP, modulation, Rs):
        """
        Calculate BER.

        Parameters
        ----------
        rssi : int
            Received signal strength indicator, as determined by RFIC.
        EIRP : int
            Transmit power in dBm.
        modulation : str
            One of {`FSK` | `GFSK` | `OOK`}.
        Rs : float
            Data rate in bits per second.

        Returns
        -------
        Pb : float
            Probability of bit error.
            
        """
        if modulation not in ['FSK', 'GFSK', 'OOK']:
            print "Modulation not recognized, must be one of {`FSK` | `GFSK` | `OOK`}"
            raise ValueError
        
        SNR = self._snr(rssi, EIRP)

        Bw = 620.0e3
        snr = 10.0**(SNR/10.0)
        EbN0 = snr*Bw/Rs
        # print EbN0, Bw, Rs
        # ebn0 = 10.0**(EbN0/10.0)

        if modulation == 'FSK':
            Pb = (0.5)*np.exp((-0.5*EbN0))
        if modulation in ['GFSK', 'OOK']:
            x = np.sqrt(EbN0)
            Pb = (0.5)-(0.5)*self._erf(x/np.sqrt(2.0))

        return Pb



    def calculate_goodput(self, Rs, t):
        """
        Calculate goodput.

        Maximum number of packets in time t.

        """
        propogation_distance = 10.0
        speed_of_light = 3.0e8
        packet_size = 512.0

        goodput = t / (0.3 + (propogation_distance / speed_of_light) + (packet_size / Rs))
        
        return goodput






    def _snr(self, rssi, EIRP):
        """
        Calculate SNR.

        Parameters
        ----------
        rssi : int
            Received signal strength indicator, as determined by RFIC.
        EIRP : int
            Transmit power in dBm.

        Returns
        -------
        SNR : float
            Signal-to-Noise ratio in dB.
            
        """
        RSSI = (rssi - 125.0) / 2.0 - 60.0
        SNR = EIRP - RSSI
        return SNR
        




    def _erf(self, x):
        """
        Calculate error function.

        """
        # max error: 2.5e-5
        p = 0.47047
        a1 = 0.3480242
        a2 = -0.0958798
        a3 = 0.7478556

        t = 1.0 / (1.0 + p*x)

        erf = 1.0 - (a1*t + a2*t**2 + a3+t**3)*np.exp(-x**2)

        return erf
