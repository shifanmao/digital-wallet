#!/usr/bin/python

""" Fraud Detection Using Social-network Information
Author: Shifan Mao
Date: 11-06-16 """

import sys
import networkx as nx
import numpy as np
# from graph import Graph

def train(input_batch):
    """ Make Network of Users based on Transaction History """
    G = nx.Graph()
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
    """ 
    Feature 1. Display Warning if Not Friends (degree 1 connection)
    Feature 2. Display Warning if Not Friends of Friends (degree 2 connection)
    Feature 3. Display Warning if Outside of Fourth-degree Friends (degree> 4 connection)
    """
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
            
            result = 'unverified\n'
            if (deg==1):
                if G.has_edge(id1,id2):
                    result = 'trusted\n'
            else:
                has_nodes = ((id1 in G) and (id2 in G))
                if (has_nodes):
                    has_path = nx.has_path(G,id1,id2)
                    if (has_path):
                        path_length = len(nx.bidirectional_dijkstra(G,id1,id2))
                        if (deg==2):
                            if (path_length==2):
                                result = 'trusted\n'
                        elif (deg==4):  
                            if (path_length<=4):
                                result = 'trusted\n'
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
    
    """ load transaction history """
    G = train(input_batch)
    
    """ test with new transactions """
    test(input_stream,output_out1,G,deg=1)
    test(input_stream,output_out2,G,deg=2)
    test(input_stream,output_out3,G,deg=4)

if __name__ == "__main__":
    # example of executing this script
    # python ./src/antifraud.py ./paymo_input/batch_payment.txt ./paymo_input/stream_payment.txt ./paymo_output/output1.txt ./paymo_output/output2.txt ./paymo_output/output3.txt
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
