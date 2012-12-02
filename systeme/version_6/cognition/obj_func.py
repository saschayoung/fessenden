#!/usr/bin/env python

import numpy as np

class ObjectiveFunctions(object):

    def __init__(self):
        self._generate_time_function()



    def _generate_time_function(self):
        """
        Create a polynomial fit for time.

        This private function creates a 3rd order polynomial fit to
        represent unit time (time per inch traveled) for input rotor
        power.

        """
        distance = 30.0

        t_total = np.array([6.636803, 7.384832, 6.820400, 7.033324, 6.615562,
                            6.011670, 5.473605, 5.078091, 4.992305, 5.963818,
                            4.268262, 4.179882, 3.975959, 4.217389, 4.037789, 
                            4.829124, 4.848656, 3.488006, 3.301235, 4.727865,
                            4.387924, 5.452579, 6.348041, 6.948240, 4.474748,
                            5.597478, 4.591388, 6.627983, 6.298144, 7.116761])

        unit_t = t_total / distance
        
        power = [25, 25, 25, 25, 25,
                 35, 35, 35, 35, 35,
                 45, 45, 45, 45, 45,
                 55, 55, 55, 55, 55,
                 65, 65, 65, 65, 65,
                 75, 75, 75, 75, 75]

        z3 = np.polyfit(power, unit_t, 3)
        self.poly3 = np.poly1d(z3)
        




    def calculate_z_score(self, x, y):
        """
        Calculate target/anti-target score.

        This is a piecewise-defined function that describes a Z score
        for a path that is based on the number of targets (objects to
        find) and anti-targets (objects to avoid) along the path.

        Parameters
        ----------
        x : int
            Number of targets on path (x >= 0).
        y : int
            Number of anti-targets on path (y >= 0).

        Returns
        -------
        z : float
            Combined target/anti-target score (0 <= z <= 1).

        """
        if (x == 0) or (x < y):
            z = 0
        elif (x == 1) and (y == 0):
            z = 0.2
        elif ((1 < x) and (x <= 3)) and (y <= x-2):
            z = 0.2 * (x - y)

        elif ((4 < x) and (x <= 6)) and (y <= x-3):
            z = 0.15 * (x - y)
        elif ((4 < x) and (x <= 6)) and (y <= x-2):
            z = 0.2 * (x - y)
                        
        elif (x > 6) and (y <= x-4):
            if ((0.2 * (x - y)) > 1.0):
                z = 1.0
            else:
                z = 0.2 * (x - y)

        elif (x > 6) and (y <= x-3):
            z =  0.15 * (x - y)
        elif (x > 6) and (y <= x-2):
            z = 0.1 * (x - y)

        else:
            z = 0

        return z



    def calculate_packet_delivery(self, Rs, time, d_prop):
        """
        Calculate packet delivery along a path.

        This function calculates the maximum number of packets that
        can be sent during a single traverse of a given test bed path.

        Parameters
        ----------
        Rs : float
            Data rate (bits/sec).
        time : float
            Time to traverse a given test bed path (seconds).
        d_prop : float
            Distance between transmitter and receiver (meters).

        Returns
        -------
        packet_delivery : int
            Number of packets that can be sent during a single travers of a
            given test bed path.

        """
        system_latency = 0.3
        d_prop = 10.0
        speed_of_light = 3.0e8
        packet_size = 137*8

        packet_delivery = time / (system_latency + (packet_size / Rs))
        return int(np.floor(packet_delivery))


    def calculate_ber(self, EIRP, Rs, Noise, Lp):
        """
        Calculate probability of bit error.

        This function calculates the probability of bit error for
        non-coherent FSK.

        Parameters
        ----------
        EIRP : float
            Transmit power (dBm).
        Rs : float
            Data rate (bits/sec).
        Noise : float
            Noise power (dBm).
        Lp : float
            Path loss (dB).

        Returns
        -------
        Pb : float
            Probability of bit error

        """

        rate_list = [2e3, 2.4e3, 4.8e3, 9.6e3, 19.2e3, 38.4e3, 57.6e3, 125e3]
        idx = rate_list.index(Rs)

        fd_list = [2e3, 2.4e3, 4.8e3, 9.6e3, 19.2e3, 38.4e3, 57.6e3, 125e3]
        fd = fd_list[idx]

        # Bw = 2*(fd + Rs/2) # per T. Pratt and http://www.edaboard.com/thread24570.html
        Bw = 100e3
        
        SNR = EIRP - Lp - Noise
        snr = 10.0**(SNR/10.0)
        ebn0 = snr*Bw/Rs
        Pb = (0.5)*np.exp((-0.5*ebn0))
        return Pb


    def calculate_time(self, rotor_power, distance):
        """
        Calculate time to travers path.

        This function use a 3rd order polynomial fit to caluclate the
        time to traverse a path given the length of the path and rotor
        power.

        Parameters
        ----------
        rotor_power : float
            (Unitless) power applied to rotor.
        distance : float
            Path distance (inches).

        Returns
        -------
        total_time : float
            Time required to traverse given test bed path.

        """
        unit_time_given_power = self.poly3(rotor_power)
        total_time = unit_time_given_power * distance
        return total_time



if __name__=='__main__':
    main = ObjectiveFunctions()
    score = main.calculate_z_score(8, 0)
    print score
