# Implementation of a graph class using dictionary
## Author: Shifan Mao
## Date: 11-06-16

class Graph:
    """ undirected graph data structure """
    def __init__(self, graph=None):
        if graph == None:
            graph = {}
        self.__graph = graph

    def nodes(self):
        """ return nodes of graph 
        nodes are lists objects for completeness """
        return list(self.__graph.keys())

    def edges(self):
        """ return edges of graph 
        edges are set objects for undirectness of graph """
        return self.show_edges()

    def neighbor(self,node):
        """ return neighbors, that have direct connection 
        to node """
        return self.__graph[node]
    
    def add_node(self,node):
        if node not in self.__graph:
            self.__graph[node] = []
            # NEED ADD NODE
    
    def add_edge(self,node1,node2):
        """ add connection / edge between 
        node1 and node2 """
        # add nodes if not already in graph
        if node1 not in self.nodes():
            self.add_node(node1)
        if node2 not in self.nodes():
            self.add_node(node2)

        # make connections to nodes
        self.__graph[node1].append(node2)
        self.__graph[node2].append(node1)

    def show_edges(self):
        edges = []
        for node in self.nodes():
            for neighbor in self.neighbor(node):
                if {node, neighbor} not in edges:
                    edges.append({node, neighbor})
        return edges

    def isneighbor(self,node1,node2):
        return node1 in self.nodes() and node2 in self.neighbor(node1)
