#!/usr/bin/env python3

# script to anyalyze how many sources only have a single supplemental or multi

import sys

lower = sys.argv[1]

test11 = lower + "11.tst.ext"
test12 = lower + "12.tst.ext"



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
        #print("Total number of supplemental translits = {0}, and the number of sources with a single supplemental = {1}\n".format(totalSupps,numOneSuppers))
        #print(suppDict)
        print("Number of single supplemental = {0}".format(numOneSuppers))
        print("Number of multiple supplemental = {0}".format(numMultiSuppers))
        print("Total number of supplementals = {0}".format(totalSupps))

        print("Average number of supplemental for those with supplemental = {0}".format(float(totalSupps)/(numOneSuppers + numMultiSuppers)))
        print("Average number of supplemental for all sources = {0}".format(float(totalSupps)/(totalLines)))

        print("")

with open(lower + "11.tst", 'r') as file:
    test11Lines = 0
    for line in file:
        test11Lines +=1

with open(lower + "12.tst", 'r') as file:
    test12Lines = 0
    for line in file:
        test12Lines +=1


analyze(test11, lower, "test11", test11Lines)
analyze(test12, lower, "test12", test12Lines)  
