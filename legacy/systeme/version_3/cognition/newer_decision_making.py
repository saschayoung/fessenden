#!/usr/bin/env python

import time

import numpy as np

# from rf_functions import RadioObjectives
# from time_function import TimeObjective
# from z_function import ZObjective


class DecisionMaker(object):

    def __init__(self):
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
        self.poly3 = np.poly1d(z3) # 3rd degree polynomial fit of data above

        # These are our knobs
        self.possible_speeds = [25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 
                                55.0, 60.0, 65.0, 70.0, 75.0, 80.0]

        self.possible_modulations = ['fsk', 'gfsk']

        self.possible_eirp = [8.0, 11.0, 14.0, 17.0]
        self.possible_Rs = [2.0e3, 2.4e3, 4.8e3, 9.6e3, 19.2e3, 38.4e3, 57.6e3, 125.0e3]
    

    def generate_solutions(self, paths):
        """
        Generate solutions.

        This would be where the GA or other guided search thingy would
        go.

        Parameters
        ----------
        paths : list
            List of path objects.

        """
        

        # our `meters`
        dist = []
        X = []
        Y = []
        RSSI = []


        for p in paths:
            dist.append(p.distance)
            X.append(p.previous_meters['X'])
            Y.append(p.previous_meters['Y'])
            RSSI.append(p.previous_meters['RSSI'])

        record_of_parameters = {}
        solution_set = []

        tic = time.time()
        
        index = 0
        for i in range(3):
            name = paths[i].name
            x = X[i]
            y = Y[i]

            rssi = RSSI[i]
            d = dist[i]
            z = self.calculate_z(x, y)

            for j in range(len(self.possible_speeds)):
                t = self.calculate_time(self.possible_speeds[j], d)

                for k in range(len(self.possible_Rs)):
                    for m in self.possible_modulations:
                        for e in self.possible_eirp:
                            b = self.calculate_ber(rssi, e, m, self.possible_Rs[k])
                            g = self.calculate_goodput(self.possible_Rs[k], t)

                            soln = [z, t, b, g]

                            params = {'path' : name, 'X' : x, 'Y' : y, 'Z' : z, 'T' : t,
                                      'dist' : d, 'speed' : self.possible_speeds[j],
                                      'mod' : m, 'BER' : b, 'EIRP' : e, 'RSSI' : rssi,
                                      'bitrate' : self.possible_Rs[k], 'goodput' : g}

                            solution_set.append(soln)
                            record_of_parameters[index] = params

                            index += 1

        solution_space = np.array(solution_set).T

        max_z = np.max(solution_space[0])
        max_t = np.max(solution_space[1])
        max_b = np.max(solution_space[2])
        max_g = np.max(solution_space[3])


        # TODO: make weights settable from higher-up
        z_weight = 1.0
        t_weight = 1.0
        b_weight = 1.0
        g_weight = 1.0

        scaled_z = solution_space[0] / max_z
        scaled_t = solution_space[1] / max_t
        scaled_g = solution_space[3] / max_g
        if max_b <= 1.0e-16:    # ber may be functionally zero, don't divide by 0
            scaled_b = solution_space[2]
        else:
            scaled_b = solution_space[2] / max_b

        unified_scores = (z_weight*scaled_z - t_weight*scaled_t
                         - b_weight*scaled_b + g_weight* scaled_g)

        a_scores = []
        a_parameters = []
        
        b_scores = []
        b_parameters = []

        c_scores = []
        c_parameters = []

        for i in range(len(unified_scores)):
            if record_of_parameters[i]['path'] == 'A':
                a_scores.append(unified_scores[i])
                a_parameters.append(record_of_parameters[i])
            if record_of_parameters[i]['path'] == 'B':
                b_scores.append(unified_scores[i])
                b_parameters.append(record_of_parameters[i])
            if record_of_parameters[i]['path'] == 'C':
                c_scores.append(unified_scores[i])
                c_parameters.append(record_of_parameters[i])

        a_scores = np.array(a_scores)
        a_rank = np.max(a_scores)
        a_idx = np.where(a_scores == a_rank)[0][0]

        b_scores = np.array(b_scores)
        b_rank = np.max(b_scores)
        b_idx = np.where(b_scores == b_rank)[0][0]

        c_scores = np.array(c_scores)
        c_rank = np.max(c_scores)
        c_idx = np.where(c_scores == c_rank)[0][0]

        ranking_result = np.array([a_rank, b_rank, c_rank])
        winner = np.argwhere(ranking_result == np.max(ranking_result))[0][0]

        parameters = [a_parameters[a_idx], b_parameters[b_idx], c_parameters[c_idx]]

        for i in range(len(parameters)):
            parameters[i]['score'] = ranking_result[i]
            parameters[i]['Z_scaled'] = parameters[i]['Z'] / max_z
            parameters[i]['T_scaled'] = parameters[i]['T'] / max_t
            parameters[i]['goodput_scaled'] = parameters[i]['goodput'] / max_g
            if max_b <= 1.0e-16:
                parameters[i]['BER_scaled'] = parameters[i]['BER']
            else:
                parameters[i]['BER_scaled'] = parameters[i]['BER'] / max_b


        # for i in range(len(paths)):
        #     paths[i].solution_parameters = parameters[i]

        #     paths[i].solution_as_implemented['Z'] = parameters[i]['Z']
        #     paths[i].solution_as_implemented['T'] = parameters[i]['T']
        #     paths[i].solution_as_implemented['B'] = parameters[i]['BER']
        #     paths[i].solution_as_implemented['G'] = parameters[i]['goodput']

        #     paths[i].current_knobs['Modulation'] = parameters[i]['mod']
        #     paths[i].current_knobs['Rs'] = parameters[i]['bitrate']
        #     paths[i].current_knobs['EIRP'] = parameters[i]['EIRP']
        #     paths[i].current_knobs['Speed'] = parameters[i]['speed']
        

        return winner









    def choose_path(self, paths):
        """
        Determine which path to take.

        This function implements decision making as necessary.
        
        Parameters
        ----------
        paths : list
            List of path objects.


        Returns
        -------
        out : int
            Path which to take, indicated by index of element in `paths`
            representing appropriate path choice.

        """
        has_been_explored = []

        for p in paths:
            has_been_explored.append(p.has_been_explored)

        if False in has_been_explored:
            return has_been_explored.index(False)
        else:
            return self.generate_solutions(paths)






    def calculate_z(self, X, Y):
        """
        Calculate Z.

        Calculate the paramter called Z, a function of X and Y, where
        X is targets and Y is anti-targets.

        Parameters
        ----------
        X : int
            Targets along path
        Y : int
            Anti-targets along path.

        """
        if X < Y:
            Z = 0

        if X == 0:
            Z = 0

        if X in [1, 2, 3]:
            if Y in [0, 1]:
                Z = 0.2*(X-Y)
            else:
                Z = 0

        if X in [4, 5, 6]:
            if Y in [0, 1, 2]:
                Z = 0.15*(X-Y)
            elif Y in [3, 4, 5]:
                Z = 0.1*(X-Y)
            else:
                Z = 0

        if X > 6:
            if Y <= X-5:
                if 0.15*(X-Y) > 1.0:
                    Z = 1.0
                else:
                    Z = 0.15*(X-Y)
            else:
                Z = 0

        return Z




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
            One of {`gfsk` | `fsk`}.
        Rs : float
            Data rate in bits per second.

        Returns
        -------
        Pb : float
            Probability of bit error.
            
        """
        if modulation not in ['fsk', 'gfsk']:
            print "Modulation not recognized, must be one of {`gfsk` | `fsk`}"
            raise ValueError
        
        SNR = self._snr(rssi, EIRP)

        Bw = 620.0e3
        snr = 10.0**(SNR/10.0)
        EbN0 = snr*Bw/Rs
        # print EbN0, Bw, Rs
        # ebn0 = 10.0**(EbN0/10.0)

        if modulation == 'fsk':
            Pb = (0.5)*np.exp((-0.5*EbN0))
        if modulation in ['gfsk', 'ook']:
            x = np.sqrt(EbN0)
            Pb = (0.5)-(0.5)*self._erf(x/np.sqrt(2.0))

        return Pb


    def estimate_ber(self, tx_packets, rx_packets):
        """
        Approximate actual BER.

        Parameters
        ----------
        tx_packets : int
            Number of packets sent by Node A
        rx_packets : int
            Number of packets received by Node B

        """
        # TODO: add actual algorithm
        return 0.5


    def calculate_goodput(self, Rs, t):
        """
        Calculate goodput.

        Maximum number of packets in time t.

        Parameters
        ----------
        Rs : float
            bitrate
        t : float
            time

        Returns
        -------
        goodput : int
            Maximum numbet of packets in time `t`.
        
        """
        propogation_distance = 10.0
        speed_of_light = 3.0e8
        packet_size = 512.0

        goodput = t / (0.3 + (propogation_distance / speed_of_light) + (packet_size / Rs))
        
        return int(np.floor(goodput))






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



    def calculate_time(self, rotor_power, distance):
        """
        Calculate total time to traverse a path.

        Parameters
        ----------
        rotor_power : int
            Power applied to rotors (wheels).
        distance : float
            Length of path (in inches).

        Returns
        -------
        total_time : float
            Total time to traverse `distance` at `rotor_power`.
        
        """

        unit_time_given_power = self.poly3(rotor_power)
        total_time = unit_time_given_power * distance
        return total_time




if __name__=='__main__':
    main = DecisionMaker()
    main.generate_solutions()








