#!/usr/bin/env python




import pprint

# import networkx as nx
# import numpy as np



class Route(object):

    def __init__(self):

        self.nodes = {}
        self.edges = {}


        self.initial_node = 0
        self.terminal_node = 0
        
        # self.current_node = None
        # self.last_node = None
        # self.next_node = None





    def add_nodes(self, node_list):
        """
        Add nodes to the route graph.

        Parameters
        ----------
        node_list : list
            List of nodes in route. Each element in the list tuple,
            where the first element of the tuple is the name of the
            node, and the second element is a tuple containing the X,Y
            coordinates of the node.

        Examples
        --------
        >>> route = Route()
        >>> node_list = [(1, (17.0, 17.0)), (2, (17.0, 26.5), (3, (17.0, 68.5)))]
        >>> route.add_nodes(node_list)
        
        """
        for i in range(len(node_list)):
            self.nodes[node_list[i][0]] = node_list[i][1]


    def set_initial_node(self, node):
        self.initial_node = node


    def set_terminal_node(self, node):
        self.terminal_node = node


    def add_edges(self):
        """
        Add edges.

        This function is a complete hack for the moment, until I can
        figure out how to dynamically create the structure I need, as
        shown below.

        """

        self.edges = {
            1 : {2 : {None : {'weight' : 10, 'MOT' : None, 'RF' : None},},},
            2 : {3 : {None : {'weight' : 10, 'MOT' : None, 'RF' : None},
                      8    : {'weight' : 0,  'MOT' : None, 'RF' : None},
                      9    : {'weight' : 0,  'MOT' : None, 'RF' : None},},},
            3 : {4 : {None : {'weight' : 10, 'MOT' : None, 'RF' : None},},},
            4 : {5 : {None : {'weight' : 10, 'MOT' : None, 'RF' : None},},},
            5 : {6 : {None : {'weight' : 10, 'MOT' : None, 'RF' : None},},},
            6 : {7 : {None : {'weight' : 10, 'MOT' : None, 'RF' : None},},},
            }



        

    def get_nodes(self):
        """
        Get a list of the nodes in the route graph.

        Returns
        -------
        out : list
            List of the nodes in the route graph.

        Examples
        --------
        >>> route = Route()
        >>> node_list = [(1, (17.0, 17.0)), (2, (17.0, 26.5)), (3, (17.0, 68.5))]
        >>> route.add_nodes(node_list)
        >>> route.get_nodes()
        [1, 2, 3]

        """
        return list(self.nodes.__iter__())
    



    def get_edges(self):
        """
        Get a list of the edges in the route graph.

        Returns
        -------
        out : list
            List of the edges in the route graph.


        See Also
        --------
        update_edge_list

        Examples
        --------
        >>> route = Route()
        >>> route.add_edges()
        >>> route.update_edge_list()
        >>> route.get_edges()
        [(1, 2), (2, 3, None), (2, 3, 8), (2, 3, 9), (3, 4), (4, 5), (5, 6), (6, 7)]

        """
        return self.edge_list



    def update_edge_list(self):
        """
        Make (or update) an edge list.

        This function generates a list of the edges in the route graph.
        
        Notes
        -----
        Each element in the edge_list is a n-tuple representing the
        edge (or super-edge, a path made up of multiple edges). For
        n==2, the edge is a direct path from the first element of the
        2-tuple to the second element. For n>2, the super-edge
        precedes from the first element of the n-tuple to the second
        element, via the third element. an n-tuple where the third
        element is `None` indicates that the path is a direct path
        with no iteremediate nodes.
        
        """
        self.edge_list = []

        for i in self.edges:
            l = list(self.edges[i].__iter__())
            
            if len(self.edges[i][l[0]]) == 1:
                self.edge_list.append((i, l[0]))

            else:
                for j in self.edges[i][l[0]]:
                    self.edge_list.append((i, l[0], j))


    def number_of_successors(self, node):
        """
        Return the number of successor nodes to node `node`.

        Parameters
        ----------
        node : int
            Node name or reference identifier,

        Returns
        -------
        out : int
            Number of successor nodes to node `node`.

        Examples
        --------
        >>> route = Route()
        >>> route.add_edges()
        >>> route.update_edge_list()
        >>> route.number_of_successors(2)
        3
        >>> route.number_of_successors(5)
        1
        
        """

        l = list(self.edges[node].__iter__())
        return len(self.edges[node][l[0]])




    def get_next_node(self, node):
        """
        Return the single successor node to node `node`.

        
        Parameters
        ----------
        node : int
            Node name or reference identifier,

        Returns
        -------
        out : int
            Number of successor nodes to node `node`.

        Raises
        ------
        ValueError
            If `node` has more than one successor.
        KeyError
            If `node` not in nodes.

        Examples
        --------
        >>> route = Route()
        >>> nodes = [(1, (17.0, 17.0)), (2, (17.0, 26.5)), (3, (17.0, 68.5)),(4, (17.0, 78.0)),(5, (45.0, 78.0)),
        ... (6, (45.0, 17.0)),(7, (17.0, 17.0)),(8, ( 7.0, 36.0)),(9, (27.0, 36.0))]
        >>> route.add_nodes(nodes)
        >>> route.set_initial_node(1)
        >>> route.set_terminal_node(7)
        >>> route.add_edges()
        >>> route.update_edge_list()
        >>> route.get_next_node(3)
        4

        """
        if node == self.terminal_node:
            return self.initial_node

        if node not in self.nodes:
            print "Node %d not in graph." %(node,)
            raise KeyError

        if self.number_of_successors(node) != 1:
            print "Node %d has more than one successor." %(node,)
            raise ValueError

        return list(self.edges[node].__iter__())[0]



    def get_multiple_successors(self, node):
        """
        Return the multiple possible successor nodes to `node`.

        Parameters
        ----------
        node : int
            Node name or reference identifier,

        Returns
        -------
        out : ???
            ???
        
        




if __name__=='__main__':
    DOCTEST = True

    if DOCTEST:
        import doctest
        doctest.testmod()
    else:
        route = Route()
        nodes = [(1, (17.0, 17.0)), 
                 (2, (17.0, 26.5)),
                 (3, (17.0, 68.5)),
                 (4, (17.0, 78.0)),
                 (5, (45.0, 78.0)),
                 (6, (45.0, 17.0)),
                 (7, (17.0, 17.0)),
                 (8, ( 7.0, 36.0)),
                 (9, (27.0, 36.0))]

        route.add_nodes(nodes)
        route.set_initial_node(1)
        route.set_terminal_node(7)

        route.add_edges()
        route.update_edge_list()

        print route.get_next_node(3)

    # print route.number_of_successors(2)
    # print route.number_of_successors(5)

    # route.add_nodes(nodes)
    # route.add_edges()

    # route.get_edges()
    # print route.get_nodes()



    # nodes = [(1, (17.0, 17.0)), 
    #          (2, (17.0, 26.5)),
    #          (3, (17.0, 68.5))]


    

    # def debug(self):
    #     pprint.pprint(self.nodes)
        


    # nodes = [(1, (17.0, 17.0)), 
    #          (2, (17.0, 26.5)),
    #          (3, (17.0, 68.5)),
    #          (4, (17.0, 78.0)),
    #          (5, (45.0, 78.0)),
    #          (6, (45.0, 17.0)),
    #          (7, (17.0, 17.0)),
    #          (8, ( 7.0, 36.0)),
    #          (9, (27.0, 36.0))]


    # def run(self):
    #     print self.edges[2][3].keys()
    #     tmp = []
        
    #     for i in self.edges[2][3].keys():
    #         tmp.append((self.edges[2][3][i]['weight'],i))
    #     # tmp.sort()
    #     tmp.sort(key=lambda x: x[0])

    #     print tmp
    #     print tmp[-1]
    #     # print tmp.sort()

    #     # pprint.pprint(self.nodes)
    #     # pprint.pprint(self.edges)

    #     # print self.nodes
    #     # print self.nodes[1]['coords']
    #     # pprint.pprint(self.edges)
    #     # pprint.pprint(list(self.edges.__iter__()))
    #     # pprint.pprint(list(self.edges[2].__iter__()))
    #     # pprint.pprint(list(self.edges[2][3].__iter__()))
    #     # print list(self.nodes.__iter__())



        # self.edges = {
        #     1 : {2 : {None : {'weight' : 10, 'MOT' : None, 'RF' : None},},},
        #     2 : {3 : {None : {'weight' : 10, 'MOT' : None, 'RF' : None},
        #               8    : {'weight' : 0,  'MOT' : None, 'RF' : None},
        #               9    : {'weight' : 0,  'MOT' : None, 'RF' : None},},},
        #     4 : {5 : {None : {'weight' : 10, 'MOT' : None, 'RF' : None},},},
        #     5 : {6 : {None : {'weight' : 10, 'MOT' : None, 'RF' : None},},},
        #     6 : {7 : {None : {'weight' : 10, 'MOT' : None, 'RF' : None},},},
        #     }


    # route.run()




        # self.nodes = {1 : {'coords' : (17.0, 17.0)},
        #               2 : {'coords' : (17.0, 26.5)},
        #               3 : {'coords' : (17.0, 68.5)},
        #               4 : {'coords' : (17.0, 78.0)},
        #               5 : {'coords' : (45.0, 78.0)},
        #               6 : {'coords' : (45.0, 17.0)},
        #               7 : {'coords' : (17.0, 17.0)},
        #               8 : {'coords' : ( 7.0, 36.0)},
        #               9 : {'coords' : (27.0, 36.0)}}


        # self.edges = [
        #     {'start' : 1, 'intermediate' : None, 'end' : 2, 'weight' : 10, 'MOT' : None, 'RF' : None},
        #     {'start' : 2, 'intermediate' : None, 'end' : 3, 'weight' : 10, 'MOT' : None, 'RF' : None},
        #     {'start' : 2, 'intermediate' : (8,), 'end' : 3, 'weight' : 10, 'MOT' : None, 'RF' : None},
        #     {'start' : 2, 'intermediate' : (9,), 'end' : 3, 'weight' : 10, 'MOT' : None, 'RF' : None},
        #     {'start' : 4, 'intermediate' : None, 'end' : 5, 'weight' : 10, 'MOT' : None, 'RF' : None},
        #     {'start' : 5, 'intermediate' : None, 'end' : 6, 'weight' : 10, 'MOT' : None, 'RF' : None},
        #     {'start' : 6, 'intermediate' : None, 'end' : 7, 'weight' : 10, 'MOT' : None, 'RF' : None}]
            

        # self.edges = [
        #     {'start' : 1, 'intermediate' : None, 'end' : 2, 'weight' : 10, 'MOT' : None, 'RF' : None},
        #     {'start' : 2, 'intermediate' : None, 'end' : 3, 'weight' : 10, 'MOT' : None, 'RF' : None},
        #     {'start' : 2, 'intermediate' : (8,), 'end' : 3, 'weight' : 10, 'MOT' : None, 'RF' : None},
        #     {'start' : 2, 'intermediate' : (9,), 'end' : 3, 'weight' : 10, 'MOT' : None, 'RF' : None},
        #     {'start' : 4, 'intermediate' : None, 'end' : 5, 'weight' : 10, 'MOT' : None, 'RF' : None},
        #     {'start' : 5, 'intermediate' : None, 'end' : 6, 'weight' : 10, 'MOT' : None, 'RF' : None},
        #     {'start' : 6, 'intermediate' : None, 'end' : 7, 'weight' : 10, 'MOT' : None, 'RF' : None}]


        # self.nodes = [ {'name' : 1, 'coords' : (17.0, 17.0)},
        #                {'name' : 2, 'coords' : (17.0, 26.5)},
        #                {'name' : 3, 'coords' : (17.0, 68.5)},
        #                {'name' : 4, 'coords' : (17.0, 78.0)},
        #                {'name' : 5, 'coords' : (45.0, 78.0)},
        #                {'name' : 6, 'coords' : (45.0, 17.0)},
        #                {'name' : 7, 'coords' : (17.0, 17.0)},
        #                {'name' : 8, 'coords' : ( 7.0, 36.0)},
        #                {'name' : 9, 'coords' : (27.0, 36.0)}]


        # self.node_coordinates = {'1' : (17.0, 17.0), '2' : (17.0, 26.5),
        #                          '3' : (17.0, 68.5), '4' : (17.0, 78.0),
        #                          '5' : (45.0, 78.0), '6' : (45.0, 17.0),
        #                          '7' : (17.0, 17.0), '8' : ( 7.0, 36.0),
        #                          '9' : (27.0, 36.0)}

        # self.primary_edges = [(1,2,10),
        #                       (2,3,10),
        #                       (3,4,10),
        #                       (4,5,10),
        #                       (5,6,10),
        #                       (6,7,10)]

        # self.alternate_edges = [(2,8,3),
        #                         (2,9,3)]

        # for n in self.node_coordinates:
        #     self.route.add_node(int(n), coords=self.node_coordinates[n])

        # self.route.add_weighted_edges_from(self.primary_edges)

        # # self.route.add_path([2,8,3], weight=0)



        # self.route = nx.MultiDiGraph()
        
        # self.node_coordinates = {'1' : (17.0, 17.0), '2' : (17.0, 26.5),
        #                          '3' : (17.0, 68.5), '4' : (17.0, 78.0),
        #                          '5' : (45.0, 78.0), '6' : (45.0, 17.0),
        #                          '7' : (17.0, 17.0), '8' : ( 7.0, 36.0),
        #                          '9' : (27.0, 36.0)}

        # self.primary_edges = [(1,2,10),
        #                       (2,3,10),
        #                       (3,4,10),
        #                       (4,5,10),
        #                       (5,6,10),
        #                       (6,7,10)]

        # self.alternate_edges = [(2,8,3),
        #                         (2,9,3)]

        # for n in self.node_coordinates:
        #     self.route.add_node(int(n), coords=self.node_coordinates[n])

        # self.route.add_weighted_edges_from(self.primary_edges)

        # # self.route.add_path([2,8,3], weight=0)





        # print self.route.adjacency_list()

        # self.coordinates = [(17.0, 17.0),
        #                     (17.0, 26.5),
        #                     (17.0, 68.5),
        #                     (17.0, 78.0),
        #                     (45.0, 78.0),
        #                     (45.0, 17.0),
        #                     (17.0, 17.0),
        #                     ( 7.0, 36.0),
        #                     (27.0, 36.0)]


        






















        # self.paths = {'1' : [1, 2],
        #               '2' : [2, 3],
        #               '3' : [3, 4],
        #               '4' : [4, 5],
        #               '5' : [5, 6],
        #               '6' : [6. 7],
        #               '7' : [2, 8, 10, 3],
        #               '8' : [2, 9, 11, 3]}

 
        # self.paths = [[1, 2],
        #               [2, 3],
        #               [3, 4],
        #               [4, 5],
        #               [5, 6],
        #               [6. 7],
        #               [2, 8, 10, 3],
        #               [2, 9, 11, 3]]
    

    


        # self.coordinates = {'1' : (17.0, 17.0), '2' : (17.0, 26.5),
        #                     '3' : (17.0, 68.5), '4' : (17.0, 78.0),
        #                     '5' : (45.0, 78.0), '6' : (45.0, 17.0),
        #                     '7' : (17.0, 17.0), '8' : ( 7.0, 36.0),
        #                     '9' : (27.0, 36.0)}


    
    

        # """
        # time, MOT
        # rf, RF
        # targets, X
        # weight = f(MOT, RF, X)
        # """
