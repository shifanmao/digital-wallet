#!/usr/bin/python

""" Fraud Detection Using Social-network Information
Author: Shifan Mao
Date: 11-06-16 """

import sys
import networkx as nx
import numpy as np
from graph import Graph

def train(input_batch):
    """ Make Network of Users based on Transaction History """
    num_lines = sum(1 for line in open(input_batch))
    
    G = nx.Graph()
#    G = Graph()  # Alternatively, use custom Graph specified in graph.py
    print('Step # 0: Start loading trans. history from '+input_batch+' ...')

    with open(input_batch) as f:
        next(f)

        for i, l in enumerate(f):
            row = l.split(',')
            id1 = row[1]
            id2 = row[2]
            G.add_edge(id1,id2)
    print ' Finished loading trans. history for a total of #', i+1, ' transactions'
    return G

def test(input_stream,output_out1,G,deg=1):
    num_lines = sum(1 for line in open(input_stream))

    ### Feature 1. Display Warning if Not Friends (degree 1 connection)
    if (deg==1):
        print('Step # 1: Implementing Feature # 1 ...')
    elif (deg==2):
        print('Step # 2: Implementing Feature # 2 ...')
    elif (deg==3):
        print('Step # 3: Implementing Feature # 3 ...')
    else:
        print(' Feature Not Specified ')
    
    fout1 = open(output_out1, 'w')
    with open(input_stream) as f:
        next(f)
        for i, l in enumerate(f):
            row = l.split(',')
            id1 = row[1]
            id2 = row[2]
            
            if (deg==1):  # check if users are neighbors
                if G.has_edge(id1,id2):
                    result = 'trusted\n'
                else:
                    result = 'untrusted\n'
            else:
                # to be implemented

#                if nx.has_path(G,id1,id2):
#                if len(nx.shortest_path(G,id1,id2))==2:
                result = 'untrusted\n'

            fout1.write(result)
    fout1.close()
    
    if (deg==1):
        print ' Finished Implementing Feature # 1 for total of #', i+1, ' transactions'
    elif (deg==2):
        print ' Finished Implementing Feature # 2 for total of #', i+1, ' transactions'    
    elif (deg==3):
        print ' Finished Implementing Feature # 3 for total of #', i+1, ' transactions'    

def main(input_batch, input_stream, output_out1, output_out2, output_out3):
    """ specify train and test files
    training data comes from transaction history and
    test data are new transactions, which need classification trusted/untrusted """

    ## Examples of inputs
    # input_batch = '../paymo_input/batch_payment.txt'
    # input_stream = '../paymo_input/stream_payment.txt'

    ## Examples of outputs
    # output_out1 = '../paymo_output/output1.txt'
    # output_out2 = '../paymo_output/output2.txt'
    # output_out3 = '../paymo_output/output3.txt'
    
    """ load transaction history """
    G = train(input_batch)
    
    """ test with new transactions """
    test(input_stream,output_out1,G,deg=1)
    test(input_stream,output_out2,G,deg=1)
    test(input_stream,output_out3,G,deg=1)

if __name__ == "__main__":
    # example of executing this script
    # python ./src/antifraud.py ./paymo_input/batch_payment.txt ./paymo_input/stream_payment.txt ./paymo_output/output1.txt ./paymo_output/output2.txt ./paymo_output/output3.txt
    input_batch = sys.argv[1]
    input_stream = sys.argv[2]
    output_out1 = sys.argv[3]
    output_out2 = sys.argv[4]
    output_out3 = sys.argv[5]
    main(input_batch, input_stream, output_out1, output_out2, output_out3)
