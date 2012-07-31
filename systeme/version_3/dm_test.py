#!/usr/bin/env python

from cognition.new_decision_making import DecisionMaker
from route.new_path import Path

path_a = Path(name='A', distance=62.0, direction='left')
path_b = Path(name='B', distance=48.0, direction='straight')
path_c = Path(name='C', distance=87.5, direction='right')

path_a.previous_meters['X'] = 5
path_a.previous_meters['Y'] = 1
path_a.previous_meters['RSSI'] = 300

path_b.previous_meters['X'] = 3
path_b.previous_meters['Y'] = 0
path_b.previous_meters['RSSI'] = 300

path_c.previous_meters['X'] = 5
path_c.previous_meters['Y'] = 2
path_c.previous_meters['RSSI'] = 300

dm = DecisionMaker()
choice = dm.generate_solutions([path_a, path_b, path_c])

print choice

for p in [path_a, path_b, path_c]:
    print p.name
    print p.solution_parameters
