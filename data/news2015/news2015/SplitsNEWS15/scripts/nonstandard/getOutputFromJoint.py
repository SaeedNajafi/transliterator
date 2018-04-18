#!/usr/bin/env python3

''' this script takes a normal dtl output file and a joint dtl output file.
    when there is an output from the joint system (i.e. when that input has suppl data), that output is printed out,
    otherwise, the normal dtl's output is printed
    in effect, this uses the joint system when possible, and the normal system otherwise.

    usage:  getOutputFromJoint.py dtl.output joint.output > combined.output
'''


import sys

jointDict = dict() # the outputs for the joint system

with open(sys.argv[2], 'r') as extFile:
    for line in extFile:
        try:
            source, trans  = line.strip().split('\t')[0], line.strip().split('\t')[1] 
        except:
            #print("problem with line: {0}".format(line.strip()))
            continue
        if source in jointDict:
            jointDict[source].append(trans)
        else:
            jointDict[source] = [trans]



normalDict = dict() # the outputs for the normal system

with open(sys.argv[1], 'r') as extFile:
    for line in extFile:
        try:
            source, trans  = line.strip().split('\t')
        except:
            #print("problem with line: {0}".format(line.strip()))
            continue
        if source in normalDict:
            normalDict[source].append(trans)
        else:
            normalDict[source] = [trans]


for source in sorted(normalDict):
    if source in jointDict:
        # use the joint output
        for output in jointDict[source]:
            print("\t".join([source, output]))
    else:
        # use the normal output
        for output in normalDict[source]:
            print("\t".join([source, output]))
