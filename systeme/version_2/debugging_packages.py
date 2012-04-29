#!/usr/bin/env python

import numpy as np
    
from knowledge_base import KnowledgeBase
from motion.simple_motion import SimpleMotion
    
kb = KnowledgeBase()

def move_from_here_to_there(here, there):
    coords = kb.get_state()['node_coordinates']
    src = coords[str(here)]
    dst = coords[str(there)]
    print "src: ", src
    print "dst: ", dst
    angle = np.arctan2(dst[0] - src[0], dst[1] - src[1]) * 180/np.pi

    print "angle: ", angle




nodes = [1, 2, 3, 4, 5, 6, 7]
for i in range(len(nodes) - 1):
    move_from_here_to_there(i+1,i+2)
    
