#!/usr/bin/env python3

from collections import defaultdict
from optparse import OptionParser
from sys import argv, stdin


def errordie(msg):
    print(argv[0], ': error: ', msg, sep='')
    exit()

parser = OptionParser(usage='usage: %prog SUPPL_CORPUS < BASE_CORPUS')

(options, args) = parser.parse_args()

if len(args) != 1:
    errordie('must have only one argument')
else:
    SUPFILE = args[0]

baseData = defaultdict(set)
for line in stdin.readlines():
    k, v = line.strip().split('\t')
    baseData[k].add(v)

supData = defaultdict(set)
with open(SUPFILE) as inp:
    for line in inp:
        k, v = line.strip().split('\t')
        supData[k].add(v)

bset = set(baseData.keys())
sset = set(supData.keys())

common = bset & sset
for baseIn in sorted(common):
    for suppl in sorted(supData[baseIn]):
        for baseOut in sorted(baseData[baseIn]):
            print(baseIn, suppl, baseOut, sep='\t')
