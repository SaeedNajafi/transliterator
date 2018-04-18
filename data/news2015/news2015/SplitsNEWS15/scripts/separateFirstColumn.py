#!/usr/bin/env python3 

''' this script will take an input file in argv[1] that looks like
    adam    A D A M
    and add spaces between all chars in the first column so it looks like
    a d a m    A D A M
    printed to stdout
'''


import sys

with open(sys.argv[1], 'r') as file:
    for line in file:
        left, right = line.strip().split('\t')
        left = " ".join(left)
        print("\t".join([left, right]))
