#!/usr/bin/env python3 

''' 
    this script will take an aligned source word file (like .word) and a file with supplemental translits (.ext)
    it prints out only the suppl sources that occur in the source words (I guess it isn't in the source words due to m2m failure for that word?)
    this script is needed before running lei's dtl since the ext file and word file are expecting to match up
'''

import sys

data = set()
with open(sys.argv[1], 'r') as sourceFile:
    for sourceLine in sourceFile:
            source = sourceLine.strip()
            #print("adding source {0}".format(source))
            data.add(source)

with open(sys.argv[2], 'r') as extFile:
    for extLine in extFile:
        extSource = extLine.split('\t')[0] 
        if extSource in data:
            print(extLine.strip())
        #else:
        #    print(extLine.strip() + " not in data!")

