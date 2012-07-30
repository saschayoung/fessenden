#!/usr/bin/env python

import time

import numpy as np

from rf_functions import RadioObjectives
from time_function import TimeObjective
from z_function import ZObjective


class DecisionMaker(object):

    def __init__(self):
        # These are our knobs
        self.possible_speeds = [25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 
                                55.0, 60.0, 65.0, 70.0, 75.0, 80.0]

        # self.possible_modulations = ['FSK', 'GFSK', 'OOK']
        self.possible_modulations = ['FSK', 'GFSK']

        self.possible_eirp = [8.0, 11.0, 14.0, 17.0]
        self.possible_Rs = [2.0e3, 2.4e3, 4.8e3, 9.6e3, 19.2e3, 38.4e3, 57.6e3, 125.0e3]
    
        self.rf_objectives = RadioObjectives()
        self.time_objective = TimeObjective()
        self.z_objective = ZObjective()



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
        
        # paths = [path_a, path_b, path_c]

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

        # print dist, X, Y, RSSI
        record_of_parameters = {}
        solution_set = []

        tic = time.time()
        
        index = 0
        for i in range(3):
            p = paths[i].name
            x = X[i]
            y = Y[i]

            rssi = RSSI[i]
            d = dist[i]
            z = self.z_objective.calculate_z(x, y)

            for j in range(len(self.possible_speeds)):
                t = self.time_objective.calculate_time(self.possible_speeds[j], d)

                for k in range(len(self.possible_Rs)):
                    for m in self.possible_modulations:
                        for e in self.possible_eirp:
                            b = self.rf_objectives.calculate_ber(rssi, e, m, self.possible_Rs[k])
                            g = self.rf_objectives.calculate_goodput(self.possible_Rs[k], t)

                            solution_set.append([z, t, b, g])
                            record_of_parameters[index] = {'path' : p,
                                                           'X' : x,
                                                           'Y' : y,
                                                           'Z' : z,
                                                           'T' : t,
                                                           'dist' : d,
                                                           'speed' : self.possible_speeds[j],
                                                           'mod' : m,
                                                           'BER' : b,
                                                           'EIRP' : e,
                                                           'RSSI' : rssi,
                                                           'bitrate' : self.possible_Rs[k],
                                                           'goodput' : g}
                                                       
                            index += 1
        
        print index
        solution_space = np.array(solution_set).T


        max_z = np.max(solution_space[0])
        max_t = np.max(solution_space[1])
        max_b = np.max(solution_space[2])
        max_g = np.max(solution_space[3])

        # print max_z, max_t, max_b, max_g

        z_weight = 1.0
        t_weight = 1.0
        b_weight = 1.0
        g_weight = 1.0

        # this is the basic solution
        #############################################################
        scaled_z = solution_space[0] / max_z
        scaled_t = solution_space[1] / max_t
        scaled_b = solution_space[2] / max_b
        scaled_g = solution_space[3] / max_g

        unified_solution = (z_weight*scaled_z - t_weight*scaled_t
                            - b_weight*scaled_b + g_weight* scaled_g)
        #############################################################


        # print unified_solution

        solution = np.max(unified_solution)


        solution_index = np.where(unified_solution == solution)[0][0]

        toc1 = time.time()

        hist, bin_edges = np.histogram(unified_solution, 100)

        alternative_solution_indices = []

        for i in range(len(unified_solution)):
            s = unified_solution[i]
            if s == solution:
                continue
            elif ( s <= bin_edges[-1] and s >= bin_edges[-2] ):
                alternative_solution_indices.append(i)
            else:
                continue

        toc2 = time.time()

        base_time = toc1 - tic
        extended_time = toc2 - toc1

        print "Time of initial solution calculation: %f seconds" %(base_time,)
        print "Time of alternative solution extension: %f seconds" %(extended_time,)

        print "\n\nDetails of `solution`: "
        print solution_index, solution, record_of_parameters[solution_index]

        print "\n\nAlternate `solutions`: "
        for i in alternative_solution_indices:
            print i, unified_solution[i], record_of_parameters[i]






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

        # TODO: I will need to add additional logic here, this (above)
        # just covers choosing a path that hasn't been explored yet. I
        # will need to add the decision making stuff.
        else:
            return 2



if __name__=='__main__':
    main = DecisionMaker()
    main.generate_solutions()























    #     tic = time.time()
        
    #     solution_set = []
        
    #     # this is the collection of observed parameters, the meters, organized by path
    #     path_a = {'X' : 2, 'Y' : 3, 'SNR' : 10, 'dist' : 60}
    #     path_b = {'X' : 3, 'Y' : 1, 'SNR' :  3, 'dist' : 50}
    #     path_c = {'X' : 3, 'Y' : 3, 'SNR' :  4, 'dist' : 60}

    #     # the observed parameters, organized by individual meter
    #     path = ['A', 'B', 'C']
    #     X = [2, 4, 4]
    #     Y = [3, 1, 3]
    #     SNR = [10.0, 3.0, 4.0]
    #     dist = [60.0, 50.0, 60.0]
        
    #     # our knobs
    #     speed = [5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 55.0, 60.0, 65.0, 70.0, 75.0]
    #     modulation = ['FSK', 'GFSK', 'OOK']
    #     alpha = 0.3
    #     Rs = [2.0e3, 2.4e3, 4.8e3, 9.6e3, 19.2e3, 38.4e3, 57.6e3, 125.0e3]

    #     index = 0
    #     for i in range(3):
    #         p = path[i]
    #         x = X[i]
    #         y = Y[i]
    #         snr = SNR[i]
    #         d = dist[i]
    #         z = self.calculate_z(x, y)

    #         for j in range(len(speed)):
    #             t = self.calculate_time(d, speed[j])

    #             for k in range(len(Rs)):
    #                 for m in modulation:
    #                     b = self.calculate_ber(snr, m, Rs[k], alpha)
    #                     g = self.calculate_goodput(Rs[k], t)
    #                     solution_set.append([z, t, b, g])
    #                     record_of_parameters[index] = {'path' : p,
    #                                                    'X' : x,
    #                                                    'Y' : y,
    #                                                    'Z' : z,
    #                                                    'T' : t,
    #                                                    'dist' : d,
    #                                                    'speed' : speed[j],
    #                                                    'mod' : m,
    #                                                    'BER' : b,
    #                                                    'SNR' : snr,
    #                                                    'bitrate' : Rs[k],
    #                                                    'goodput' : g}
                                                       
    #                     index += 1

    #     solution_space = np.array(solution_set).T

    #     max_z = np.max(solution_space[0])
    #     max_t = np.max(solution_space[1])
    #     max_b = np.max(solution_space[2])
    #     max_g = np.max(solution_space[3])

    #     z_weight = 1.0
    #     t_weight = 1.0
    #     b_weight = 1.0
    #     g_weight = 1.0

    #     # this is the basic solution
    #     #############################################################
    #     scaled_z = solution_space[0] / max_z
    #     scaled_t = solution_space[1] / max_t
    #     scaled_b = solution_space[2] / max_b
    #     scaled_g = solution_space[3] / max_g

    #     unified_solution = (z_weight*scaled_z - t_weight*scaled_t
    #                         - b_weight*scaled_b + g_weight* scaled_g)
    #     #############################################################

    #     solution = np.max(unified_solution)
    #     solution_index = np.where(unified_solution == solution)[0][0]

    #     toc1 = time.time()

    #     hist, bin_edges = np.histogram(unified_solution, 100)

    #     alternative_solution_indices = []

    #     for i in range(len(unified_solution)):
    #         s = unified_solution[i]
    #         if s == solution:
    #             continue
    #         elif ( s <= bin_edges[-1] and s >= bin_edges[-2] ):
    #             alternative_solution_indices.append(i)
    #         else:
    #             continue

    #     toc2 = time.time()

    #     base_time = toc1 - tic
    #     extended_time = toc2 - toc1

    #     print "Time of initial solution calculation: %f seconds" %(base_time,)
    #     print "Time of alternative solution extension: %f seconds" %(extended_time,)

    #     print "\n\nDetails of `solution`: "
    #     print solution_index, solution, record_of_parameters[solution_index]

    #     print "\n\nAlternate `solutions`: "
    #     for i in alternative_solution_indices:
    #         print i, unified_solution[i], record_of_parameters[i]

            
    #     # self.plot_data(unified_solution, solution_space)



    # def calculate_z(self, X, Y):
    #     """
    #     Calculate Z.

    #     Calculate the paramter called Z, a function of X and Y, where
    #     X is targets and Y is anti-targets.

    #     Parameters
    #     ----------
    #     X : int
    #         Targets along path
    #     Y : int
    #         Anti-targets along path.

    #     """
    #     if X < Y:
    #         Z = 0
    #     if X == 0:
    #         Z = 0
    #     if X in [1, 2, 3]:
    #         if Y in [0, 1]:
    #             Z = 0.2*(X-Y)
    #         else:
    #             Z = 0
    #     if X in [4, 5, 6]:
    #         if Y in [0, 1, 2]:
    #             Z = 0.15*(X-Y)
    #         elif Y in [3, 4, 5]:
    #             Z = 0.1*(X-Y)
    #         else:
    #             Z = 0
    #     if X > 6:
    #         if Y <= X-5:
    #             if 0.15*(X-Y) > 1.0:
    #                 Z = 1.0
    #             else:
    #                 Z = 0.15*(X-Y)
    #         else:
    #             Z = 0
    #     return Z


        

    # def calculate_ber(self, SNR, modulation, Rs, alpha):
    #     """
    #     Calculate BER.

    #     """
    #     if modulation not in ['FSK', 'GFSK', 'OOK']:
    #         print "Modulation not recognized, must be one of {`FSK` | `GFSK` | `OOK`}"
    #         raise ValueError
        
    #     Bw = 620.0e3
    #     snr = 10.0**(SNR/10.0)
    #     EbN0 = snr*Bw/Rs
    #     # print EbN0, Bw, Rs
    #     # ebn0 = 10.0**(EbN0/10.0)

    #     if modulation == 'FSK':
    #         Pb = (0.5)*np.exp((-0.5*EbN0))
    #     if modulation in ['GFSK', 'OOK']:
    #         x = np.sqrt(EbN0)
    #         Pb = (0.5)-(0.5)*self._erf(x/np.sqrt(2.0))

    #     return Pb



    # def calculate_goodput(self, Rs, t):
    #     """
    #     Calculate goodput.

    #     Maximum number of packets in time t.

    #     """
    #     propogation_distance = 10.0
    #     speed_of_light = 3.0e8
    #     packet_size = 512.0

    #     goodput = t / ((propogation_distance / speed_of_light) + (packet_size / Rs))
        
    #     return goodput




    # def calculate_time(self, distance, speed):
    #     """
    #     Calculate time of travel.

    #     """
    #     return distance/speed




    # def _erf(self, x):
    #     """
    #     Calculate error function.

    #     """
    #     # max error: 2.5e-5
    #     p = 0.47047
    #     a1 = 0.3480242
    #     a2 = -0.0958798
    #     a3 = 0.7478556

    #     t = 1.0 / (1.0 + p*x)

    #     erf = 1.0 - (a1*t + a2*t**2 + a3+t**3)*np.exp(-x**2)

    #     return erf





    # def plot_data(unified_solution, solution_space):
    #     """
    #     Plot data for visualization.

    #     """
    #     import matplotlib.mlab as mlab
    #     import matplotlib.pyplot as plt
    #     from mpl_toolkits.mplot3d import axes3d, Axes3D

    #     z_vec = solution_space[0]
    #     t_vec = solution_space[1]
    #     b_vec = solution_space[2]                             
    #     g_vec = solution_space[3]                             

    #     plt.rc('xtick', direction = 'out')
    #     plt.rc('ytick', direction = 'out')

    #     fig = plt.figure(figsize=(8,6), dpi=72, facecolor='w')
    #     axes = plt.subplot(111)
    #     axes.hist(unified_solution, 50)
    #     axes.set_xlabel('Unified Solution')
    #     axes.set_ylabel('Instances in Solution Space')
    #     axes.spines['right'].set_color('none')
    #     axes.spines['top'].set_color('none')
    #     axes.xaxis.set_ticks_position('bottom')
    #     axes.yaxis.set_ticks_position('left')

    #     fig = plt.figure(figsize=(8,6), dpi=72, facecolor='w')
    #     axes = plt.subplot(221)
    #     axes.hist(z_vec, 50)
    #     axes.set_xlabel('Z parameter')
    #     axes.set_ylabel('Instances in Solution Space')
    #     axes.spines['right'].set_color('none')
    #     axes.spines['top'].set_color('none')
    #     axes.xaxis.set_ticks_position('bottom')
    #     axes.yaxis.set_ticks_position('left')

    #     axes = plt.subplot(222)
    #     axes.hist(t_vec, 50)
    #     axes.set_xlabel('Time')
    #     axes.set_ylabel('Instances in Solution Space')
    #     axes.spines['right'].set_color('none')
    #     axes.spines['top'].set_color('none')
    #     axes.xaxis.set_ticks_position('bottom')
    #     axes.yaxis.set_ticks_position('left')

    #     axes = plt.subplot(223)
    #     axes.hist(b_vec, 50)
    #     axes.set_xlabel('BER')
    #     axes.set_ylabel('Instances in Solution Space')
    #     axes.spines['right'].set_color('none')
    #     axes.spines['top'].set_color('none')
    #     axes.xaxis.set_ticks_position('bottom')
    #     axes.yaxis.set_ticks_position('left')

    #     axes = plt.subplot(224)
    #     axes.hist(g_vec, 50)
    #     axes.set_xlabel('Goodput')
    #     axes.set_ylabel('Instances in Solution Space')
    #     axes.spines['right'].set_color('none')
    #     axes.spines['top'].set_color('none')
    #     axes.xaxis.set_ticks_position('bottom')
    #     axes.yaxis.set_ticks_position('left')


    #     fig = plt.figure(figsize=(8,6), dpi=72, facecolor='w')
    #     ax = fig.add_subplot(111, projection='3d')
    #     ax.scatter(z_vec, t_vec, b_vec)
    #     ax.set_xlabel('Z parameter')
    #     ax.set_ylabel('Time')
    #     ax.set_zlabel('BER')

    #     plt.show()







