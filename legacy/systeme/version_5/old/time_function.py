#!/usr/bin/env python


import numpy as np


class TimeObjective(object):
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











# import matplotlib
# import matplotlib.pyplot as plt


# z1 = np.polyfit(power, t_total, 2)
# p1 = np.poly1d(z1)
# xp1 = np.linspace(25, 75, 100)

# z2 = np.polyfit(power, t_total, 3)
# p2 = np.poly1d(z2)
# xp2 = np.linspace(25, 75, 100)

# z3 = np.polyfit(power, t_total, 4)
# p3 = np.poly1d(z3)
# xp3 = np.linspace(25, 75, 100)

# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.plot(power, t_total, 'o', xp1, p1(xp1), '-', xp2, p2(xp2), '--', xp3, p3(xp3), '-.')


# z1 = np.polyfit(power, unit_t, 2)
# p1 = np.poly1d(z1)
# xp1 = np.linspace(25, 75, 100)

# z2 = np.polyfit(power, unit_t, 3)
# p2 = np.poly1d(z2)
# xp2 = np.linspace(25, 75, 100)

# z3 = np.polyfit(power, unit_t, 4)
# p3 = np.poly1d(z3)
# xp3 = np.linspace(25, 75, 100)

# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.plot(power, unit_t, 'o', xp1, p1(xp1), '-', xp2, p2(xp2), '--', xp3, p3(xp3), '-.')

# plt.show()

