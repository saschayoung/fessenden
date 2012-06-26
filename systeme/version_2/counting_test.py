#!/usr/bin/env python

import numpy as np

a = np.array([0, 0, 5, 5,  0,  0,  1,  5, 5, 4, 0])
print a


a[a!=5] = 0
print a

j = 0
for i in range(len(a)-1):
    if a[i] == 0 and a[i+1] == 5:
        j += 1

print j
