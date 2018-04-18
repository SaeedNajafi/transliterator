#!/usr/bin/env python3 
''' this is used to print out a 1 for each row in a file. needed to give a dumby rank to syscomb output for additional reranking '''


import sys

with open(sys.argv[1], 'r') as file:
    for line in file:
        print(1)
