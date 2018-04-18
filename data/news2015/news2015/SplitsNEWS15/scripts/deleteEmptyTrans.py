#!/usr/bin/env python3 

''' this script will look through a dtl output file and if there is a transliteration
    that is empty, remove that line. Otherwise print out
'''

import sys

with open(sys.argv[1], 'r') as file:
    for line in file:
        source, trans = line.split('\t')
        if trans == '\n' or trans.replace(' ', '') == 'n':
            #print("empty trans on line {0}: {1}".format(count, line.strip()))
            continue # don't print an empty trans
        print(line.strip()) # print the line
