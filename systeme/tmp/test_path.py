#!/usr/bin/env python


class Path(object):
    """
    A single path.

    A path is an object that represents a single graph edge, that is,
    it is a path between two nodes in a graph.

    A path has:
    - a name,
    - an explored value,
    - a distance,
    - a direction
    - a start node,
    - an end node,
    - a direction,
    - targets,
    - anti_targets
    - an iteration

    """


    def __init__(self):
        self.name = ''
        self.explored = False
        self.distance = 0
        self.start_node = 0
        self.end_node = 0
        self.direction = ''
        self.targets = 0
        self.anti_targets = 0
        self.iteration = 0


    def set_name(self, name):
        """
        Set name of path.

        Parameters
        ----------
        name : str
            Name of path.

        """
        self.name = name


    def set_explored(self):
        """
        Set path explored `True`.

        """
        self.explored = True
        

    def set_distance(self, distance):
        """
        Set distance of path.

        
        Parameters
        ----------
        distance : float
            Distance of path, in inches.

        """

        self.distance = distance


    def set_start_node(self, start_node):
        """
        Set node at beginning of path.

        Parameters
        ----------
        start_node : int
            Node at beginning of path.

        """

        self.start_node = start_node

    def set_end_node(self, end_node):
        """
        Set node at end of path.

        Parameters
        ----------
        end_node : int
            Node at end of path.

        """
        self.end_node = end_node
    

    def set_direction(self, direction):
        """
        Set direction to turn for path.

        Parameters
        ----------
        direction : str
            Direction to turn for path. One of
            {`left` | `right` | `straight` | `n/a` }.

        """
        self.direction = direction


    def set_targets(self, targets):
        """
        Set number of targets.

        Parameters
        ----------
        targets : int
            Number of targets on path.

        """
        self.targets = targets


    def set_anti_targets(self, anti_targets):
        """
        Set number of anti-targets.

        Parameters
        ----------
        anti_targets : int
            Number of anti-targets on path.

        """
        self.anti_targets = anti_targets


    def set_iteration(self, iteration):
        """
        Set iteration.

        Parameters
        ----------
        iteration : int
            Number of passes through full route/graph.

        """
        self.iteration = iteration







    def get_path(self):
        """
        Get full path information.

        Returns
        -------
        out : dict
            Dictionary containing all attributes of path.

        """
        out = {'name' : self.name,
               'explored' : self.explored,
               'distance' : self.distance,
               'start_node' : self.start_node,
               'end_node' : self.end_node,
               'direction' : self.direction,
               'targets' : self.targets,
               'anti_targets' : self.anti_targets,
               'iteration' : self.iteration}

        return out







    # def get_name(self):
    #     """
    #     Get name of path.

    #     Returns
    #     -------
    #     name : str
    #         Name of path.

    #     """
    #     return self.name

        
    # def get_explored(self):
    #     """
    #     Get path explored value.

    #     Returns
    #     -------
    #     out : bool
    #         Whether path has been explored before.

    #     """
    #     return self.explored


    # def get_distance(self):
    #     """
    #     Get distance of path.

        
    #     Returns
    #     -------
    #     distance : float
    #         Distance of path, in inches.

    #     """

    #     return self.distance
        

    # def get_start_node(self):
    #     """
    #     Get node at beginning of path.

    #     Returns
    #     -------
    #     start_node : int
    #         Node at beginning of path.

    #     """

    #     return self.start_node

    # def get_end_node(self):
    #     """
    #     Get node at end of path.

    #     Returns
    #     -------
    #     end_node : int
    #         Node at end of path.

    #     """
    #     return self.end_node
    

    # def get_direction(self):
    #     """
    #     Get direction to turn for path.

    #     Returns
    #     -------
    #     direction : str
    #         Direction to turn for path. One of
    #         {`left` | `right` | `straight` | `n/a` }.

    #     """
    #     return self.direction


    # def get_targets(self):
    #     """
    #     Get number of targets.

    #     Returns
    #     -------
    #     targets : int
    #         Number of targets on path.

    #     """
    #     return self.targets


    # def get_anti_targets(self):
    #     """
    #     Get number of anti-targets.

    #     Returns
    #     -------
    #     anti_targets : int
    #         Number of anti-targets on path.

    #     """
    #     return self.anti_targets


    # def get_iteration(self):
    #     """
    #     Get iteration.

    #     Returns
    #     -------
    #     iteration : int
    #         Number of passes through full route/graph.

    #     """
    #     return self.iteration
