#!/usr/bin/env python3

from collections import defaultdict
from sys import stdin


data = defaultdict(list)
for line in stdin.readlines():
    stuff = line.replace('|', '').replace('_', '').split()
    inp, outp, score = stuff[0:3]
    score = float(score)
    data[inp].append((outp, score))

for inp in data:
    maxscore = data[inp][0][1]
    minscore = data[inp][-1][1]
    diff = maxscore - minscore
    for outp, score in data[inp]:
        print(inp, outp, (score - minscore) / diff, sep='\t')
