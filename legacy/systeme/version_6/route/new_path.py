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
        # self.has_been_explored = False
        self.has_been_explored = True

        self.Lp = 90
        self.d_prop = 10


        self.meters = {}

        self.current_knobs = {'Modulation' : 'fsk',
                              'Rs' : 0,
                              'EIRP' : 0,
                              'Speed' : 0}

        self.current_meters = {'X' : 0,
                               'Y' : 0,
                               'RSSI' : 0}


        self.solution_as_observed = {'Z' : 0,
                                     'T' : 0,
                                     'B' : 0,
                                     'G' : 0}

        self.solution_as_implemented = {'Z' : 0,
                                        'T' : 0,
                                        'B' : 0,
                                        'G' : 0}
        
        self.previous_knobs = {'Modulation' : '',
                               'Rs' : 0,
                               'EIRP' : 0,
                               'Speed' : 0}

        self.previous_meters = {'X' : 0,
                                'Y' : 0,
                                'RSSI' : 0}



    def update_knobs(self):
        """
        Update knob settings.

        This function copies the current knob settings into
        previous_knobs and resets current_knobs.

        """
        self.previous_knobs = self.current_knobs
        self.current_knobs = {'Modulation' : 'fsk',
                              'Rs' : 0,
                              'EIRP' : 0,
                              'Speed' : 0}



    def update_meters(self):
        """
        Update meter settings.

        This function copies the current meter settings into
        previous_meters and resets current_meters.

        """
        self.previous_meters = self.current_meters
        self.current_meters = {'X' : 0,
                               'Y' : 0,
                               'RSSI' : 0}






















        # self.iteration = 0

        # self.solution_parameters = {}

        
        # self.solution_as_implemented = {'Z' : 0,
        #                                 'T' : 0,
        #                                 'B' : 0,
        #                                 'G' : 0}

        # self.solution_as_observed = {'Z' : 0,
        #                              'T' : 0,
        #                              'B' : 0,
        #                              'G' : 0}

        # self.solution_effectiveness = 0

        # self.previous_meters = {'X' : 0,
        #                         'Y' : 0,
        #                         'RSSI' : 0}

        
        # self.current_meters = {'X' : 0,
        #                        'Y' : 0,
        #                        'RSSI' : 0}
                               
        # self.previous_knobs = {'Modulation' : '',
        #                        'Rs' : 0,
        #                        'EIRP' : 0,
        #                        'Speed' : 0}

        # self.current_knobs = {'Modulation' : 'fsk',
        #                       'Rs' : 0,
        #                       'EIRP' : 0,
        #                       'Speed' : 0}
