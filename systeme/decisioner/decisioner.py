#!/usr/bin/env python


# The basic facts
# Q(x) = (1/2)-(1/2)erf(x/sqrt(2))
# Q(x) = (1/2)erfc(x/sqrt(2))


# BER
# =========================================
# OOK & FSK (coherent)
# Pb = Q(sqrt(Eb/N0))
#
# FSK (non-coherent)
# Pb = (1/2)exp(-(1/2)(Eb/N0))
# =========================================


# Time
# =========================================
# T = d/speed
# =========================================


# Z (target/anti-target function)
# =========================================
# piece-wise defined

# if X < Y:
#     Z = 0
#
# for X == 0:
#     for Y in ZZ:
#         Z = 0
#
# for X in {1 , 2, 3}:
#     if Y in {0, 1}:
#         Z = 0.2*(X-Y)
#     else:
#         Z = 0
#       
# for X in {4 , 5, 6}:
#     if Y in {0, 1, 2}:
#         Z = 0.15*(X-Y)
#     else:
#         Z = 0
#       
# for X > 6:
#     if Y <= X-5:
#         if 0.15*(X-Y) > 1.0:
#             Z = 1.0
#         else:
#             Z = 0.15*(X-Y)
#     else:
#         Z = 0
# =========================================


# Measured/calculated Eb/N0 (with ~30 dB attenuator) = 21.0 dB

# Use:
# B = Rs*(1+alpha)
# alpha = 0.3



import pprint
import time

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


from mpl_toolkits.mplot3d import axes3d, Axes3D
# import matplotlib.pyplot as plt
# import numpy as np



class DecisionMaker(object):

    def __init__(self):

        pass


    
    def generate_solutions(self):
        tic = time.time()
        record_of_parameters = {}
        
        solution_set = []
        
        # this is the collection of observed parameters, the meters, organized by path
        path_a = {'X' : 2, 'Y' : 3, 'SNR' : 10, 'dist' : 60}
        path_b = {'X' : 3, 'Y' : 1, 'SNR' :  3, 'dist' : 50}
        path_c = {'X' : 3, 'Y' : 3, 'SNR' :  4, 'dist' : 60}

        # the observed parameters, organized by individual meter
        path = ['A', 'B', 'C']
        X = [2, 4, 4]
        Y = [3, 1, 3]
        SNR = [10.0, 3.0, 4.0]
        dist = [60.0, 50.0, 60.0]
        
        # our knobs
        speed = [5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 55.0, 60.0, 65.0, 70.0, 75.0]
        modulation = ['FSK', 'GFSK', 'OOK']
        alpha = 0.3
        Rs = [2.0e3, 2.4e3, 4.8e3, 9.6e3, 19.2e3, 38.4e3, 57.6e3, 125.0e3]


        index = 0


        for i in range(3):
            
            p = path[i]
            x = X[i]
            y = Y[i]
            snr = SNR[i]
            d = dist[i]

            z = self.calculate_z(x, y)

            for j in range(len(speed)):
                t = self.calculate_time(d, speed[j])

                for k in range(len(Rs)):
                    for m in modulation:
                        b = self.calculate_ber(snr, m, Rs[k], alpha)
                        solution_set.append([z, t, b])

                        record_of_parameters[index] = {'path' : p,
                                                       'X' : x,
                                                       'Y' : y,
                                                       'Z' : z,
                                                       'T' : t,
                                                       'dist' : d,
                                                       'speed' : speed[j],
                                                       'mod' : m,
                                                       'BER' : b,
                                                       'SNR' : snr,
                                                       'bitrate' : Rs[k]}
                                                       
                        index += 1

        solution_space = np.array(solution_set).T

        max_z = np.max(solution_space[0])
        max_t = np.max(solution_space[1])
        max_b = np.max(solution_space[2])        


        pprint.pprint(solution_set)

        # this is the basic solution
        #############################################################
        scaled_z = solution_space[0] / max_z
        scaled_t = solution_space[1] / max_t
        scaled_b = solution_space[2] / max_b

        unified_solution = scaled_z - scaled_t - scaled_b
        #############################################################


        # this changes the solution 
        #############################################################
        # scaled_z = 0.3333 * solution_space[0] / max_z
        # scaled_t = 0.3333 * solution_space[1] / max_t
        # scaled_b = 0.3333 * solution_space[2] / max_b

        # unified_solution = scaled_z - scaled_t - scaled_b
        #############################################################


        # this changes the solution 
        #############################################################
        # scaled_z = 0.3333 * solution_space[0] / max_z
        # scaled_t = 1.0 * solution_space[1] / max_t
        # scaled_b = 0.3333 * solution_space[2] / max_b

        # unified_solution = scaled_z - scaled_t - scaled_b
        #############################################################


        solution = np.max(unified_solution)
        solution_index = np.where(unified_solution == solution)[0][0]

        toc1 = time.time()



        hist, bin_edges = np.histogram(unified_solution, 50)

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

        # print "Time of initial solution calculation: %f seconds" %(base_time,)
        # print "Time of alternative solution extension: %f seconds" %(extended_time,)

        print "\n\nDetails of `solution`: "
        print solution_index, solution, record_of_parameters[solution_index]


        print "\n\nAlternate `solutions`: "
        for i in alternative_solution_indices:
            print i, unified_solution[i], record_of_parameters[i]




        z_vector = []
        time_vector = []
        ber_vector = []

        for i in range(len(unified_solution)):
            z_vector.append(record_of_parameters[i]['Z'])
            time_vector.append(record_of_parameters[i]['T'])
            ber_vector.append(record_of_parameters[i]['BER'])


        # plt.rc('xtick', direction = 'out')
        # plt.rc('ytick', direction = 'out')

        # data = np.random.normal(0,1,100)

        # fig = plt.figure(figsize=(8,6), dpi=72, facecolor='w')
        # axes = plt.subplot(111)
        # # axes.axvline(np.mean(data), 0, data.max(), linewidth=2, color='red')
        # axes.hist(data, bins=50, normed=True)
        # axes.set_ylim(0, 1)
        # axes.set_xlim(-3, 3)

        # axes.spines['right'].set_color('none')
        # axes.spines['top'].set_color('none')
        # axes.xaxis.set_ticks_position('bottom')
        # axes.spines['bottom'].set_position(('data', -0.05))
        # axes.yaxis.set_ticks_position('left')
        # axes.spines['left'].set_position(('data',-3.25))

        # plt.show()

        z = solution_space[0]
        t = solution_space[1]
        b = solution_space[2]                             

        plt.rc('xtick', direction = 'out')
        plt.rc('ytick', direction = 'out')

        fig = plt.figure(figsize=(8,6), dpi=72, facecolor='w')
        axes = plt.subplot(221)
        axes.hist(z, 50, normed=True)

        axes.spines['right'].set_color('none')
        axes.spines['top'].set_color('none')
        axes.xaxis.set_ticks_position('bottom')
        axes.yaxis.set_ticks_position('left')


        fig = plt.figure(figsize=(8,6), dpi=72, facecolor='w')
        axes = plt.subplot(222)
        axes.hist(t, 50, normed=True)

        axes.spines['right'].set_color('none')
        axes.spines['top'].set_color('none')
        axes.xaxis.set_ticks_position('bottom')
        axes.yaxis.set_ticks_position('left')


        fig = plt.figure(figsize=(8,6), dpi=72, facecolor='w')
        axes = plt.subplot(223)
        axes.hist(b, 50, normed=True)

        axes.spines['right'].set_color('none')
        axes.spines['top'].set_color('none')
        axes.xaxis.set_ticks_position('bottom')
        axes.yaxis.set_ticks_position('left')

        plt.show()

        # fig = plt.figure()
        # ax = fig.add_subplot(111)
        # min_x = min(time_vector)
        # max_x = max(time_vector)
        # time_n, time_bins, time_patches = ax.hist(time_vector, 10, (min_x, max_x))
        # time_plot = plt.plot(time_bins)




        # # print ber_vector
        # fig = plt.figure()
        # ax = fig.add_subplot(111)
        # min_x = min(ber_vector)
        # max_x = max(ber_vector)
        # ber_n, ber_bins, ber_patches = ax.hist(ber_vector, 50, (min_x, max_x))
        # ber_plot = plt.plot(ber_bins)

        # z = solution_space[0]
        # t = solution_space[1]
        # b = solution_space[2]                             

        # fig = plt.figure()
        fig = plt.figure(figsize=(8,6), dpi=72, facecolor='w')

        ax = fig.add_subplot(224, projection='3d')
        # X, Y, Z = axes3d.get_test_data(0.05)
        # ax.plot_wireframe(z, t, b, rstride=10, cstride=10)
        ax.scatter(z, t, b)

        ax.set_xlabel('Z parameter')
        ax.set_ylabel('Time')
        ax.set_zlabel('BER')

        plt.show()





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


        

    def calculate_ber(self, SNR, modulation, Rs, alpha):
        """
        Calculate BER.

        """
        if modulation not in ['FSK', 'GFSK', 'OOK']:
            print "Modulation not recognized, must be one of {`FSK` | `GFSK` | `OOK`}"
            raise ValueError

        snr = 10.0**(SNR/10.0)
        bw = Rs*(1+alpha)
        EbN0 = snr*bw/Rs

        if modulation == 'FSK':
            Pb = (0.5)*np.exp((-0.5*EbN0))
        if modulation in ['GFSK', 'OOK']:
            x = np.sqrt(EbN0)
            Pb = (0.5)-(0.5)*self._erf(x/np.sqrt(2.0))

        return Pb




    def calculate_time(self, distance, speed):
        """
        Calculate time of travel.

        """
        return distance/speed




    def _erf(self, x):
        """
        Calculate error function.

        """
        # max error: 2.5e-5
        p = 0.47047
        a1 = 0.3480242
        a2 = -0.0958798
        a3 = 0.7478556

        t = 1.0 / (1 + p*x)

        erf = 1 - (a1*t + a2*t**2 + a3+t**3)*np.exp(-x**2)

        return erf


if __name__=='__main__':
    main = DecisionMaker()
    main.generate_solutions()



        # scaled_z = solution_space[0] / max_z
        # scaled_t = solution_space[1] / max_t
        # scaled_b = solution_space[2] / max_b

        # unified_solution = scaled_z - scaled_t - scaled_b











    # def plot_histogram(self, data):
    #     fig = plt.figure()
    #     ax = fig.add_subplot(111)

    #     min_x = min(data)
    #     max_x = max(data)
    #     n, bins, patches = ax.hist(data, 50, (min_x, max_x))
    #     print bins
    #     print n

    #     l = plt.plot(bins)
    #     plt.show()
        




        # print "\n\nAlternate `solutions`: "
        # for i in alternative_solution_indices:
        #     print unified_solution[i], record_of_parameters[i]
        # self.plot_histogram(unified_solution)


        # print solution
        # print solution_index

        # alternative_solution_indices = []



        # hist, bin_edges = np.histogram(unified_solution, 50)

        # # print hist
        # # print bin_edges
        # # print bin_edges[-1]
        # # print bin_edges[-2]

        
        # for i in range(len(unified_solution)):
        #     s = unified_solution[i]
        #     if s == solution:
        #         solution_index = i
        #     elif ( s <= bin_edges[-1] and s >= bin_edges[-2] ):
        #         alternative_solution_indices.append(i)
        #     else:
        #         continue


        # for i in range(len(unified_solution)):
        #     if solution == unified_solution[i]:
        #         solution_indices.append(i)
        #     else:
        #         continue
            
            
        # for i in solution_indices:
        #     print "Details of `solution`: "
        #     print record_of_parameters[i]
