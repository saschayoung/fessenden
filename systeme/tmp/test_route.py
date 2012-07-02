#!/usr/bin/env python


from test_path import Path

class Route(object):
    """
    A route is a graph, with nodes, edges, and paths. 

    Nodes are points, effectively graph nodes.  Edges are paired
    nodes, a start point and end point.  Paths are the important part
    of this, a traversal from start to end where we are interested in
    the results, and can make choices. Paths are actual objects. An
    edge does not necessarily have any paths.
    
    """

    def __init__(self):
        self.graph = {1: {'end' : 2, 'paths' : 3},
                      2: {'end' : 1, 'paths' : 0}}


        # self.nodes = [1, 2, 3, 4]
        # self.edges = [(1,2), (2, 3), (3, 4), (4, 1)]
        # self.number_of_paths = [0, , 0, 0]
        self.paths = {}
        

    def build_route(self):
        a = Path()
        a.set_name('a')
        a.set_distance(60.0)
        a.set_start_node(2)
        a.set_end_node(3)
        a.set_direction('left')
        self.paths['a'] = a.get_path()

        b = Path()
        b.set_name('b')
        b.set_distance(50.0)
        b.set_start_node(2)
        b.set_end_node(3)
        b.set_direction('straight')
        self.paths['b'] = b.get_path()

        c = Path()
        c.set_name('c')
        c.set_distance(60.0)
        c.set_start_node(2)
        c.set_end_node(3)
        c.set_direction('right')
        self.paths['c'] = c.get_path()




    






if __name__=='__main__':
    main = Route()
    main.build_route()
