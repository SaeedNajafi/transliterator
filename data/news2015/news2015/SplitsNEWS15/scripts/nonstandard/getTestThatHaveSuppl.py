#!/usr/bin/env python3

''' this script takes a tst file and a file with a subset of these word with supplemental data.
    It prints out those words that have at least one supplemental '''

import sys

extSet = set()
with open(sys.argv[2], 'r') as extFile:
    for line in extFile:
        source = line.strip().split('\t')[0]
        source = source.replace('|', '')
        #print("adding source = {0}".format(source))
        extSet.add(source)


with open(sys.argv[1], 'r') as tstFile:
    for line in tstFile:
        source = line.strip().split('\t')[0]
        source = source.replace(' ', '')
        if source in extSet:
            print(line.strip())
        #else:
        #    print("source not in ext: {0}".format(source))
