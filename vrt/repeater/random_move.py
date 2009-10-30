#!/usr/bin/env python

import math
import random

def range_random(base, upperbound):
    random.seed()
    scale = upperbound - base
    return((random.random()*scale)+base)

def random_move(coordinates, magnitude = 0.0006):
    if coordinates == None:
        coordinates = get_random_coord()

    #Convert string coordinates to list of floats
    coordinates = coordinates.strip('[]\n')
    coordinates = coordinates.split(',')

    coordinates[0] = float(coordinates[0])
    coordinates[1] = float(coordinates[1])

    #come up with random angle
    angle = range_random(0,2*math.pi)
    cosine = math.cos(angle)
    sine = math.sin(angle)

    #break up into components based on magnitude
    vert = magnitude*sine
    hori = magnitude*cosine

    #add components to old values
    vert = coordinates[0] + vert
    hori = coordinates[1] + hori

    #convert back to string with 15 places after decimal
    vert_string = "%.15f" % vert
    hori_string = "%.15f" % hori

    #glue parts together (longitude first) seperated by comma 
    result = vert_string + ',' + hori_string
    
    return result
##################################################################
def get_random_coord():
    long_base = 80.38097990274007
    long_upper = 80.39682877540427
    lat_base = 37.2242687061976
    lat_upper = 37.2311454410083
    longitude = range_random(long_base, long_upper)
    latitude = range_random(lat_base, lat_upper)
    longitude = -1 * longitude
    result = [longitude, latitude]
    result = str(result)
    result = result.split(" ")
    result = "".join(result)
    result.strip("[]")
    return result

if __name__ == '__main__':
    start = get_random_coord()
    print ("Start: ", start)
    moved = random_move(start)
    print ("After Move: ", moved)
    
