#!/usr/bin/env python

import networkx as nx


class FlightPath(object):
    def __init__(self):
        self.full_graph = nx.DiGraph()
        self.n = [(17.0, 17.0),
                  (17.0, 26.5),
                  (17.0, 68.5),
                  (17.0, 78.0),
                  (45.0, 78.0),
                  (45.0, 17.0),
                  (17.0, 17.0),
                  (36.0, 7.0),
                  (59.0, 7.0),
                  (36.0, 27.0),
                  (59.0, 27.0)]
        self.e = [(1,2),(2,3),(3,4),(4,5),
                  (5,6),(6,7),(2,8),(2,10),
                  (8,9),(10,11),(9,3),(11,3)]
        self.first_path = [1, 2, 3, 4, 5, 6, 7]


    def build_full_graph(self):
        for i in range(len(self.n)):
            self.full_graph.add_node(i+1, coords = (self.n[i][0], self.n[i][1]))
            
        # self.full_graph.add_nodes_from(self.n)
        
        self.full_graph.add_edges_from(self.e)
        
        # for n i self.full_graph.nodes():

        # print "Nodes: ", self.full_graph.nodes()
        # print "Edges: ", self.full_graph.edges()







if __name__=='__main__':
    fp = FlightPath()
    fp.build_full_graph()











        # self.n = [(1, coords = (17.0, 17.0)),
        #           (2, coords = (17.0, 26.5)),
        #           (3, coords = (17.0, 68.5)),
        #           (4, coords = (17.0, 78.0)),
        #           (5, coords = (45.0, 78.0)),
        #           (6, coords = (45.0, 17.0)),
        #           (7, coords = (17.0, 17.0)),
        #           (8, coords = (36.0, 7.0)),
        #           (9, coords = (59.0, 7.0)),
        #           (10, coords = (36.0, 27.0)),
        #           (11, coords = (59.0, 27.0))]

                  














        # e = [(1,2,9.5),
        #      (2,3,42),
        #      (3,4,9.5),
        #      (4,5,28),
        #      (5,6,61),
        #      (6,7,28),
        #      (2,8,13.4),
        #      (2,10,13.4),
        #      (8,9,23),
        #      (10,11,23),
        #      (9,3,13.4),
        #      (11,3,13.4)]
        # self.full_graph.add_weighted_edges_from
