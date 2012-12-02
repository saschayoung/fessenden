#!/usr/bin/env python

import time

import numpy as np


import policy

from obj_func import ObjectiveFunctions
from rank import nondominated_sort, score_solution


WRITE_FILES = True


class DecisionMaker(object):

    def __init__(self):
        self.objfunc = ObjectiveFunctions()
        

    def solution(self, paths, iteration):
        """
        Generate a UMDDM solution.

        """
        knobs = {'possible_rotor_power' : [25.0, 30.0, 35.0, 40.0, 45.0, 50.0,
                                           55.0, 60.0, 65.0, 70.0, 75.0, 80.0],
                 'possible_Rs' : [2.0e3, 2.4e3, 4.8e3, 9.6e3, 19.2e3, 38.4e3, 57.6e3, 125.0e3],
                 'possible_EIRP' : [8.0, 11.0, 14.0, 17.0]}

        names = ['A', 'B', 'C']
        dist = []
        X = []
        Y = []
        Noise = []
        Lp = []
        d_prop = []

        soln_space = []
        param_space = []

        for p in paths:
            dist.append(p.distance)
            X.append(p.meters['X'])
            Y.append(p.meters['Y'])
            Noise.append(p.meters['Noise'])
            Lp.append(p.Lp)
            d_prop.append(p.d_prop)

        for i in range(3):
            name = names[i]
            x = X[i]
            y = Y[i]
            noise = Noise[i]
            d = dist[i]

            Z = self.objfunc.calculate_z_score(x, y)

            for j in range(len(knobs['possible_rotor_power'])):
                rotor_power = knobs['possible_rotor_power'][j]
                T = self.objfunc.calculate_time(rotor_power, d)


                for k in range(len(knobs['possible_Rs'])):
                    Rs = knobs['possible_Rs'][k]

                    for m in range(len(knobs['possible_EIRP'])):
                        EIRP = knobs['possible_EIRP'][m]
                        B = self.objfunc.calculate_ber(EIRP, Rs, noise, Lp[i])
                        G = self.objfunc.calculate_packet_delivery(Rs, T, d_prop[i])

                        soln = [Z, T, B, G]
                        soln_space.append(ref_soln)
                        
                        params = {'name' : name,
                                  'dist' : d,
                                  'X' : x,
                                  'Y' : y,
                                  'Noise' : noise,
                                  'rotor_power' : rotor_power,
                                  'EIRP' : EIRP,
                                  'Rs' : Rs,
                                  'Lp': Lp[i],
                                  'd_prop' : d_prop[i],
                                  'Z' : Z, 
                                  'T' : T,
                                  'B' : B,
                                  'G' : G}

                        param_space.append(params)

        front = nondominated_sort(ref_soln_space)

        if len(front) == 0:
            print "No nondominated values, throwing error."
            raise ValueError

        if WRITE_FILES:
            self.write_files(iteration, soln_space, param_space)

        if len(front) == 1:
            return param_space[front[0]], ref_soln_space[front[0]]
        else:
            rand_idx = random.randint(0,len(front)-1)
            idx = front[rand_idx]
            counter = 0
            while  (param_space[idx]['Z'] < policy.min_z) or (param_space[idx]['B'] > policy.max_ber):
                rand_idx = random.randint(0,len(front)-1)
                idx = front[rand_idx]
                counter += 1
                if counter == 100:
                    break
            solution_score = score_solution(idx, ref_soln_space)
            return solution_score, param_space[idx], ref_soln_space[idx], idx


    def write_files(self, iteration, soln_space, param_space):
        """
        Write solution data to files.

        """
        f = open('../data_files/full_soln_space_' + str(iteration), 'wt')
        for s in ref_soln_space:
            f.write(str(s) + "\n")
        f.close()

        f = open('../data_files/full_param_space_' + str(iteration), 'wt')
        for p in param_space:
            f.write(str(p) + "\n")
        f.close()

        f = open('../data_files/nondom_sort_results_' + str(iteration), 'wt')
        f.write(str(front) + "\n")
        f.close()


    def choose_path(self, paths):
        """
        Determine which path to take.

        This function implements decision making as necessary. This is
        only used to generate a choice in ``Explore'' mode. For
        ``Exploit'' mode, this function returns ``-1'', to indicate
        that the AVEP should use the decision making module.
        
        Parameters
        ----------
        paths : list
            List of path objects.

        Returns
        -------
        out : int
            Path which to take, indicated by index of element in `paths`
            representing appropriate path choice. Choice

        """
        has_been_explored = []
        for p in paths:
            has_been_explored.append(p.has_been_explored)
        if False in has_been_explored:
            return has_been_explored.index(False)
        else:
            return -1




if __name__=='__main__':
    main = DecisionMaker()
    main.test(8,0)
    
