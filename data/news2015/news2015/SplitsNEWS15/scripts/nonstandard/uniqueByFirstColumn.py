#!/usr/bin/env python3 

''' this script can be called on a NEWS txt file and will print out only those lines where the first column
    hasn't been seen already. i.e. a uniq for source words
'''

import sys

data = set() # to keep track of sources seen
with open(sys.argv[1], 'r') as file:
    for line in file:
        source = line.strip().split('\t')[0]
        if source in data:
            continue
        else:
            data.add(source)
            print(line.strip())