#!/usr/bin/env python


import networkx as nx
import numpy as np


class KnowledgeBase(object):
    def __init__(self):
        self.current_location = 0

        

        # Radio
        # =================================================================
        self.default_radio_profile = {'power': 17,
                                      'frequency' : 434e6,
                                      'data_rate' : 4.8e3,
                                      'modulation' : "gfsk"}
        self.current_radio_profile = None
        # =================================================================


        # Route
        # =================================================================
        self.route = nx.DiGraph()
        self.node_coordinates = {'1' : (17.0, 17.0), '2' : (17.0, 26.5),
                                 '3' : (17.0, 68.5), '4' : (17.0, 78.0),
                                 '5' : (45.0, 78.0), '6' : (45.0, 17.0),
                                 '7' : (17.0, 17.0), '8' : ( 7.0, 36.0),
                                 '9' : (27.0, 36.0)}
        
                            
        # weight alternative path higher to begin with to discourage
        # its use on first pass
        self.weighted_edge_connections = [(1,2,0),
                                          (2,3,1),
                                          (2,8,1), (8,3,0), 
                                          (2,9,0), (9,3,0),
                                          (3,4,0),
                                          (4,5,0),
                                          (5,6,0),
                                          (6,7,0)]

        self.current_node = None
        self.last_node = []
        self.next_node = None

        self.current_edge = None
        self.last_edge = []
        self.next_edge = None
        # =================================================================



    def build_route(self):
        for n in self.node_coordinates:
            self.route.add_node(int(n), coords=self.node_coordinates[n])
        self.route.add_weighted_edges_from(self.weighted_edge_connections)

        
    def get_start_node(self):
        return self.route.nodes()[0]


    def get_next_node(self, node):
        if node == 7:
            return 1
        next = self.route.successors(node)
        if len(next) == 1:
            return next[0]
        elif len(next) > 1:
            return self._choose_next_node(node, next)
        else: 
            print "Route().get_next_node(node) error"
            print "for node=%d, self.route.successors(node) is %s" %(node, str(next))


    def _choose_next_node(self, current_node, next_nodes):
        path = []
        weight = []
        for n in next_nodes:
            path.append((current_node, n))
        for p in path:
            weight.append(self.route[p[0]][p[1]]['weight'])
        weight = np.array([weight])
        return next_nodes[np.argmin(weight)]


    def set_edge_weight(self, edge, weight):
        if edge == (7,1):
            pass
        else:
            self.route[edge[0]][edge[1]]['weight'] = weight

    def set_current_node(self, node):
        self.current_node = node

    def set_last_node(self, node):
        self.last_node.append(node)

    def set_next_node(self, node):
        self.next_node = node

    def set_current_edge(self, edge):
        self.current_edge = edge

    def set_last_edge(self, edge):
        self.last_edge.append(edge)

    def set_next_edge(self, edge):
        self.next_edge = edge




    def get_state(self):
        """
        Get current state of knowledge base.
        
        Returns
        -------
        out : dict
            Dictionary containing names and values of all data currently in
            database.
        """
        return {'current_location' : self.current_location,
                'default_radio_profile' : self.default_radio_profile,
                'current_radio_profile' : self.current_radio_profile,
                'node_coordinates' : self.node_coordinates,
                'weighted_edge_connections' : self.weighted_edge_connections,
                # 'initial_edge_weights' : self.initial_edge_weights,
                'current_node' : self.current_node,
                'last_node' : self.last_node,
                'next_node' : self.next_node,
                'current_edge' : self.current_edge,
                'last_edge' : self.last_edge, 
                'next_edge' : self.next_edge}







    def route_debug(self):
        print "Nodes: ", self.route.nodes()
        print "Edges: ", self.route.edges()
        for e in self.route.edges():
            print "%s['weight']: %f" %(str(e), self.route[e[0]][e[1]]['weight'])

    



if __name__=='__main__':
    kb = KnowledgeBase()
    state = kb.get_state()
    print state


    


        # node_coordinates = kb_state['node_coordinates']
        # weighted_edge_connections = kb_state['weighted_edge_connections']

                            
