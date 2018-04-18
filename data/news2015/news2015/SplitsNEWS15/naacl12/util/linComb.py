#!/usr/bin/env python3

from collections import defaultdict
from sys import argv, stdin


def readData(filein):
    data = defaultdict(lambda: defaultdict(float))
    for line in filein:
        inp, outp, score = line.split()
        # Use max() because the same output may show up multiple times
        data[inp][outp] = max(data[inp][outp], float(score))

    return data

with open(argv[1]) as inp:
    data1 = readData(inp)
with open(argv[2]) as inp:
    data2 = readData(inp)

l = float(argv[3])
c = 1.0 - l

for inp in data1:
    combined = []
    for outp in set(data1[inp]) | set(data2[inp]):
        combined.append((outp, l * data1[inp][outp] + c * data2[inp][outp]))

    for outp, score in sorted(combined, key=lambda t: t[1], reverse=True):
        print(inp, outp, score, sep='\t')
