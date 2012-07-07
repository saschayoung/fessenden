#!/usr/bin/env path

class Path(object):
    """
    A single path.

    A path is an object that represents a single graph edge, that is,
    it is a path between two nodes in a graph.

    A path has:
    - a name,
    - a distance,
    - a direction

    """

    def __init__(self, name, distance, direction):
        """
        Extend base class.
        
        Parameters
        ----------
        name : str
            Name of path.
        distance : float
            Distance of path.
        direction : str
            Direction of path from current location. One of
            {`left` | `right` | `straight` }.

        """
        if direction not in ['left', 'right', 'straight']:
            print "Path error, direction must be one of {`left` | `right` | `straight` }"
            raise ValueError
        self.p = {'name' : name, 'distance' : distance, 'direction' : direction}

        
