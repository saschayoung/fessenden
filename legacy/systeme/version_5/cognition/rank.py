#!/usr/bin/env python

import numpy as np


def nondominated_sort(P):
    """
    Determint pareto front of input array.

    This is based on the work by Deb.

    """
    F = []
    for p in range(len(P)):
        flag = 0
        for q in range(len(P)):
            if p == q:
                continue
            if ( (P[q][0] >= P[p][0]) and (P[q][1] <= P[p][1]) and
                 (P[q][2] <= P[p][2]) and (P[q][3] >= P[p][3]) ):
                flag = 1
                break
        if ( flag == 0 ):
            F.append(p)
    return F


def score_solution(index, soln_space):
    """
    Score solution.

    Generate a solution score based on a weighted sum.

    """
    weights = [1, 1, 1, 1]
    soln_space = np.array(soln_space).T

    Z_array = soln_space[0]
    T_array = soln_space[1]
    B_array = soln_space[2]
    G_array = soln_space[3]

    # Z is defined [0,1] -> already normalized
    # max_z = np.max(solution_space[0])
    max_t = np.max(T_array)
    max_b = np.max(B_array)
    max_g = np.max(G_array)

    # see comment above
    scaled_Z = Z_array
    scaled_T = T_array / max_t
    if max_b <= -1.0e-16:    # ber may be functionally zero, don't divide by 0
        scaled_B = B_array
    else:
        scaled_B = B_array / max_b
    scaled_G = G_array / max_g

    unified_scores = (weights[0]*scaled_Z - weights[1]*scaled_T
                     - weights[2]*scaled_B + weights[3]*scaled_G)

    score = unified_scores[index]
    return score
