#!/usr/bin/env python




import networkx as nx
import numpy as np

class Route(object):
    """
    Route definition.

    """
    def __init__(self, knowledge_base, lock):
        self.kb = knowledge_base
        self.lock = lock
        self.graph = nx.DiGraph()



    def build_route(self):
        kb_state = self.kb.get_state()
        node_coordinates = kb_state['node_coordinates']
        weighted_edge_connections = kb_state['weighted_edge_connections']
        # initial_edge_weights = kb_state['initial_edge_weights']
                            
        for n in node_coordinates:
            self.graph.add_node(int(n), coords=node_coordinates[n])
        self.graph.add_weighted_edges_from(weighted_edge_connections)



    def get_shortest_path(self):
        return nx.shortest_path(self.graph, 1, 7)


    def get_start_node(self):
        return self.graph.nodes()[0]


    def get_next_node(self, node):
        if node == 7:
            return 1
        next = self.graph.successors(node)
        if len(next) == 1:
            # print next[0]
            return next[0]
        elif len(next) > 1:
            return self._choose_next_node(node, next)
        else: 
            print "Route().get_next_node(node) error"
            print "for node=%d, self.graph.successors(node) is %s" %(node, str(next))
        

    # this is where the path choice algorithm currently is
    def _choose_next_node(self, current_node, next_nodes):
        path = []
        weight = []
        for n in next_nodes:
            path.append((current_node, n))
        for p in path:
            weight.append(self.graph[p[0]][p[1]]['weight'])
        weight = np.array([weight])
        return next_nodes[np.argmin(weight)]
    


    def set_edge_weight(self, edge, weight):
        if edge == (7,1):
            pass
        else:
            self.graph[edge[0]][edge[1]]['weight'] = weight











    def debug(self):
        print "Nodes: ", self.graph.nodes()
        print "Edges: ", self.graph.edges()
        for e in self.graph.edges():
            print "%s['weight']: %f" %(str(e), self.graph[e[0]][e[1]]['weight'])




            

if __name__=='__main__':

    from threading import Lock
    
    from knowledge_base import KnowledgeBase
    
    kb = KnowledgeBase()
    lock = Lock()

    main = Route(kb, lock)
    main.build_route()
    main.debug()







        # print "Shortest path from 1 to 7: ", nx.shortest_path(self.graph, 1, 7)
        # for n in nx.shortest_path(self.graph, 1, 7):
        #     print self.graph.successors(n)
        # for n in nx.shortest_path(self.graph, 1, 7):
        #     print self.get_next_node(n)
        # for e in self.graph.edges():
        #     print "self.graph[e[0]][e[1]]: ", self.graph[e[0]][e[1]]





        # e = self.graph.edges()
        # for i in range(len(e)):
        #     self.graph[e[i][0]][e[i][1]]['value'] = initial_edge_weights[i]



    # print "starting node: ", main.get_start_node()
    # print "next node: ", main.get_next_node(main.get_start_node())
    # print "get_next_node(7): ", main.get_next_node(7)






# import numpy as np
# import matplotlib
# import matplotlib.pyplot as plt



# x = np.array([17.0, 17.0, 17.0, 17.0, 45.0, 45.0, 17.0, 07.0])
# y = np.array([17.0, 26.5, 68.5, 78.0, 78.0, 17.0, 17.0, 36.0])


# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.plot(x, y, 'o')
# plt.show()



#         for i in range(len(self.n)):
#             self.full_graph.add_node(i+1, coords = (self.n[i][0], self.n[i][1]))
            
#         self.full_graph.add_nodes_from(self.n)
        
#         self.full_graph.add_edges_from(self.e)
        
#         # for n i self.full_graph.nodes():

#         print "Nodes: ", self.full_graph.nodes()
#         print "Edges: ", self.full_graph.edges()
#         print "Shortest path from 1 to 7: ", nx.shortest_path(self.full_graph, 1, 7)










#         self.n = [(17.0, 17.0),
#                   (17.0, 26.5),
#                   (17.0, 68.5),
#                   (17.0, 78.0),
#                   (45.0, 78.0),
#                   (45.0, 17.0),
#                   (17.0, 17.0),
#                   (36.0, 7.0),
#                   (59.0, 7.0),
#                   (36.0, 27.0),
#                   (59.0, 27.0)]
#         self.first_path = [1, 2, 3, 4, 5, 6, 7]


#     def build_full_graph(self):






# if __name__=='__main__':
#     fp = FlightPath()
#     fp.build_full_graph()











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
