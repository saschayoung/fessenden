#!/usr/bin/env python

import random
import numpy as np

def range_random(base, upperbound):
    random.seed()
    scale = upperbound - base
    return((random.random()*scale)+base)

def random_move(coordinates, direction = -1, magnitude = 0.0006):
    if coordinates == None:
        coordinates = get_random_coord()

#     #Convert string coordinates to list of floats
#     coordinates = coordinates.strip('[]\n')
#     coordinates = coordinates.split(',')

#     coordinates[0] = float(coordinates[0])
#     coordinates[1] = float(coordinates[1])

    #come up with random angle
    #direction = 1 -> go north east
    #direction = 2 -> go north west
    #direction = 3 -> go south west
    #direction = 4 -> go south east
    #otherwise -> go where ever
    direction = int(direction)

    angle_start = np.pi/2*(direction-1)
    angle_end = np.pi/2*direction

    if (direction < 1) or (direction > 4):
        angle_start = 0
        angle_end = 2*np.pi

    angle = range_random(angle_start,angle_end)
    cosine = np.cos(angle)
    sine = np.sin(angle)

    #break up into components based on magnitude
    vert = magnitude*sine
    hori = magnitude*cosine

    #add components to old values
    vert = coordinates[0] + vert
    hori = coordinates[1] + hori

#     #convert back to string with 15 places after decimal
#     vert_string = "%.15f" % vert
#     hori_string = "%.15f" % hori

#     #glue parts together (longitude first) seperated by comma 
#     result = vert_string + ',' + hori_string

    result = [vert,hori]
    
    return result

def directed_move(start, finish, magnitude = 0.0006):
    delta_x = finish[0]-start[0]
    delta_y = finish[1]-start[1]

    angle = np.arctan2(delta_y,delta_x)

    x_move = magnitude*np.cos(angle)
    y_move = magnitude*np.sin(angle)

    #random part
    max_rand = magnitude/10

    x_rand = range_random(-1*max_rand, max_rand)
    y_rand = range_random(-1*max_rand, max_rand)

    x_move += x_rand
    y_move += y_rand

    new_x = start[0] + x_rand + x_move
    new_y = start[1] + y_rand + y_move

    return [new_x, new_y]

def get_random_coord():
    long_base = np.float64(-77.03784581934387)
    long_upper = np.float64(-77.13004625000904)
    lat_base = np.float64(38.7928657357599)
    lat_upper = np.float64(38.85000638965948)
    longitude = range_random(long_base, long_upper)
    latitude = range_random(lat_base, lat_upper)
#     longitude = -1 * longitude
    result = [longitude,latitude]
#     result = ["%.15f"%k for k in result]
#     result = ",".join(result)
#     result.strip()
    return result

if __name__ == '__main__':
    start = get_random_coord()
    finish = get_random_coord()
    print "Start:\t\t", start
    print "Finish:\t\t", finish
    moved = directed_move(start,finish)
    print "After Move:\t", moved
    
