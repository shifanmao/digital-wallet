#!/usr/bin/python

import sys
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout

def train(input_batch):
    """ Make Network of Users based on Transaction History """
    G = nx.Graph()
    print('Step # 0: Start loading trans. history from '+input_batch+' ...')

    with open(input_batch) as f:
        next(f)

        for i, l in enumerate(f):
            if i > 5e3:
                break

            row = l.split(',')
            id1 = row[1]
            id2 = row[2]
            G.add_edge(id1,id2)
    print ' Finished loading trans. history for a total of #', i+1, ' transactions'

    # Make a drawing
    graphs = list(nx.connected_component_subgraphs(G))
    Gc = max(nx.connected_component_subgraphs(G), key=len)
    print ' Number of connected subgraphs = ', len(graphs)
    print ' Number of nodes of largest connected graph = ', len(Gc)

    pos=nx.random_layout(Gc)
    nx.draw_networkx_nodes(Gc,pos,node_color='b',node_size=100,alpha=0.5)
    nx.draw_networkx_edges(Gc,pos,width=1.0,alpha=0.5)
    plt.axis('off')
    plt.savefig("network.png")


def main(input_batch):
    """ specify train and test files                                                                                                                   
    training data comes from transaction history and
    test data are new transactions, which need classification trusted/untrusted """

    """ load transaction history """
    G = train(input_batch)

if __name__ == "__main__":
    if len(sys.argv[1:]):
        input_batch = sys.argv[1:]
    else:
        print(' Inputs not specified, turn to default file ... ')
        input_batch = '../paymo_input/batch_payment.txt'
    main(input_batch)
