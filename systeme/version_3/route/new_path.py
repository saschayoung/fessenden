#!/usr/bin/env path

class Path(object):
    """
    A single path.

    A path is an object that represents a single graph edge, that is,
    it is a path between two nodes in a graph.

    A path has:
    - a name,
    - a distance,
    - a direction,
    - a has_been_explored value
    
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
        
        # these are static values, characteristic of the path
        self.name = name
        self.distance = distance
        self.direction = direction

        # this should only be false until the bath has been explored,
        # then `True` thereafter
        self.has_been_explored = False

        self.solution_parameters = {}

        
        self.solution_as_implemented = {'Z' : '',
                                        'T' : '',
                                        'B' : '',
                                        'G' : ''}

        self.solution_as_observed = {'Z' : '',
                                     'T' : '',
                                     'B' : '',
                                     'G' : ''}

        self.solution_effectiveness = 0

        self.previous_meters = {'X' : '',
                                'Y' : '',
                                'RSSI' : ''}

        
        self.current_meters = {'X' : '',
                               'Y' : '',
                               'RSSI' : ''}
                               
        self.previous_knobs = {'Modulation' : '',
                               'Rs' : '',
                               'EIRP' : '',
                               'Speed' : ''}

        self.current_knobs = {'Modulation' : '',
                              'Rs' : '',
                              'EIRP' : '',
                              'Speed' : ''}

    
        
