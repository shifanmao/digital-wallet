#!/usr/bin/python

""" Transaction Fraud Detection Using Social-network Information
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

def train(input_batch, feat=None):
    """ Make Network of Users based on Transaction History """
    G = nx.Graph()

    with open(input_batch) as f:
        next(f)  # skip header
        for i, l in enumerate(f):
            row = l.split(',')
            id1,id2 = row[1:3]
            G.add_edge(id1,id2)

            if (feat==4):
                pass # new feature, to be implemented
    return G

def test(input_stream,output_out,G,feat=1):
    """ 
    Feature 1. Display Warning if Not Friends (degree 1 connection)
    Feature 2. Display Warning if Not Friends of Friends (degree 2 connection)
    Feature 3. Display Warning if Outside of Fourth-degree Friends (degree> 4 connection)
    """
    if (feat not in [1,2,3]):
        raise ValueError('Feature not specified, need to choose feature no. from 1, 2, 3, or 4')

    fout = open(output_out, 'w')
    with open(input_stream) as f:
        next(f)  #skip header
        for i, l in enumerate(f):
            row = l.split(',')
            id1,id2 = row[1:3]
            
            result = 'unverified\n'
            if (feat==1):
                if G.has_edge(id1,id2):
                    result = 'trusted\n'
            else:
                has_nodes = ((id1 in G) and (id2 in G))
                if (has_nodes):
                    has_path = nx.has_path(G,id1,id2)
                    if (has_path):
                        path_length = nx.shortest_path_length(G,source=id1,target=id2)
                        
                        if (feat==2):
                            if (path_length<=2):
                                result = 'trusted\n'
                        elif (feat==3):
                            if (path_length<=4):
                                result = 'trusted\n'
            fout.write(result)
    fout.close()

def main(input_batch, input_stream, output_out1, output_out2, output_out3):
    """ specify train and test files
    training data comes from transaction history and
    test data are new transactions, which need classification trusted/untrusted """

    outputs = [output_out1,output_out2,output_out3]
    for feature in [1,2,3]:
        output = outputs[feature-1]
        
        """ load transaction history """
        G = train(input_batch, feat=feature)

        """ test with new transactions """
        test(input_stream,output,G,feat=feature)

if __name__ == "__main__":
    try:
        input_batch, input_stream, output_out1, output_out2, output_out3 = sys.argv[1:]
    except:
        input_batch = '../paymo_input/batch_payment.txt'
        input_stream = '../paymo_input/stream_payment.txt'

        output_out1 = '../paymo_output/output1.txt'
        output_out2 = '../paymo_output/output2.txt'
        output_out3 = '../paymo_output/output3.txt'
    main(input_batch, input_stream, \
         output_out1, output_out2, output_out3)
