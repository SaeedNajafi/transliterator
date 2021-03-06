#!/usr/bin/env python3 

''' 
   this script takes a test set and a train+dev set (each as one column of source words) and calculates how many
   words from the test set are in the train+dev set
   ./<this>.py trn.txt tst.txt 
'''

import sys

dataTrn = set()
with open(sys.argv[1], 'r') as trnFile:
    for line in trnFile:
            source = line.strip()
            #print("adding source {0}".format(source))
            dataTrn.add(source)


testSize = 0
overlap = 0
with open(sys.argv[2], 'r') as tstFile:
    for line in tstFile:
        testSize += 1
        source = line.strip()
        if source in dataTrn:
            overlap += 1

print("size of overlap with train set = {0} / {1} = {2}".format(overlap, testSize, float(overlap)/testSize))


