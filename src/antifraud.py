#!/usr/bin/python

""" Fraud Detection Using Social-network Information
Author: Shifan Mao
Date: 11-06-16 """

import sys
import networkx as nx
import numpy as np
# from graph import Graph

""" 
example of executing this script
python ./src/antifraud.py ./paymo_input/batch_payment.txt ./paymo_input/stream_payment.txt ./paymo_output/output1.txt ./paymo_output/output2.txt ./paymo_output/output3.txt
"""

def train(input_batch):
    """ Make Network of Users based on Transaction History """
    G = nx.Graph()
    print('Step # 0: Start loading trans. history from '+input_batch+' ...')

    with open(input_batch) as f:
        next(f)

        for i, l in enumerate(f):
            row = l.split(',')
            id1,id2 = row[1:3]
            G.add_edge(id1,id2)
    print ' Finished loading trans. history for a total of #', i+1, ' transactions'
    return G

def test(input_stream,output_out1,G,feat=1):
    """ 
    Feature 1. Display Warning if Not Friends (degree 1 connection)
    Feature 2. Display Warning if Not Friends of Friends (degree 2 connection)
    Feature 3. Display Warning if Outside of Fourth-degree Friends (degree> 4 connection)
    """
    if (feat in [1,2,3]):
        print "Implementing Feature #%d..." %1
    else:
        raise ValueError('Feature not specified, need to choose feature no. from 1, 2, and 3')
    
    fout1 = open(output_out1, 'w')
    with open(input_stream) as f:
        next(f)
        for i, l in enumerate(f):
            row = l.split(',')
            id1,id2 = row[1:3]
            
            if (i%1e5==0):
                print " Processing Line #%d..." %i
            result = 'unverified\n'
            if (feat==1):
                if G.has_edge(id1,id2):
                    result = 'trusted\n'
            else:
                has_nodes = ((id1 in G) and (id2 in G))
                if (has_nodes):
                    has_path = nx.has_path(G,id1,id2)
                    if (has_path):
#                        path_length,path = nx.bidirectional_dijkstra(G,id1,id2)
                        path_length = nx.shortest_path_length(G,source=id1,target=id2)
                        
                        if (feat==2):
                            if (path_length<=2):
                                result = 'trusted\n'
                        elif (feat==3):
                            if (path_length<=4):
                                result = 'trusted\n'
            fout1.write(result)
    fout1.close()
    print "Implementing Feature #%d... for total of %d transactions" %(feat,i+1)

def main(input_batch, input_stream, output_out1, output_out2, output_out3):
    """ specify train and test files
    training data comes from transaction history and
    test data are new transactions, which need classification trusted/untrusted """

    """ load transaction history """
    G = train(input_batch)
    
    """ test with new transactions """
    test(input_stream,output_out1,G,feat=1)
    test(input_stream,output_out2,G,feat=2)
    test(input_stream,output_out3,G,feat=3)

if __name__ == "__main__":
    try:
        input_batch, input_stream, output_out1, output_out2, output_out3 = sys.argv[1:]
    except:
        print(' Inputs and outputs not specified, turn to default files ... ')
        input_batch = '../paymo_input/batch_payment.txt'
        input_stream = '../paymo_input/stream_payment.txt'

        output_out1 = '../paymo_output/output1.txt'
        output_out2 = '../paymo_output/output2.txt'
        output_out3 = '../paymo_output/output3.txt'        
    main(input_batch, input_stream, output_out1, output_out2, output_out3)
