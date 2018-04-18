#!/usr/bin/env python3

# script to anyalyze how many sources only have a single supplemental or multi

import sys

lower = sys.argv[1]

trn = lower + ".trn.ext"
dev = lower + ".tst.ext.matched"

def analyze(fileName, lower, name, totalLines):
    print(lower, name)
    with open(fileName, 'r') as file:
        totalSupps = 0
        numOneSuppers = 0 # the number of sources which only have a single supplemental
        numMultiSuppers = 0
        suppDict  = {}
        for line in file:
            supps = line.strip().split("\t")[1:]
            numSupps = len(supps)
            if numSupps == 1:
                numOneSuppers +=1
            else:
                numMultiSuppers += 1

            totalSupps += numSupps
            if numSupps in suppDict:
                suppDict[numSupps] += 1
            else:
                suppDict[numSupps] = 1

                
        #print(fileName)
        #print("Total number of supplemental translits = {0}, and the number of sources with a single supplemental = {1}".format(totalSupps,numOneSuppers))
        #print(suppDict)
        print("Number of single supplemental = {0}".format(numOneSuppers))
        print("Number of multiple supplemental = {0}".format(numMultiSuppers))
        print("Total number of supplementals = {0}".format(totalSupps))
        print("Average number of supplemental for those with supplemental = {0}".format(float(totalSupps)/(numOneSuppers + numMultiSuppers)))
        print("Average number of supplemental for all sources = {0}".format(float(totalSupps)/(totalLines)))

        print("")



with open(lower + ".trn", 'r') as trnFile:
    trnLines = 0
    for line in trnFile:
        trnLines +=1

with open(lower + ".tst", 'r') as devFile:
    devLines = 0
    for line in devFile:
        devLines +=1



analyze(dev, lower, "dev", devLines)
analyze(trn, lower, "train", trnLines) 
