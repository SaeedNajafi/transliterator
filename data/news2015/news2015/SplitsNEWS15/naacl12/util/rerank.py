#!/usr/bin/env python3
'''Reranks a set of inputs and outputs according to a score.'''

from collections import defaultdict
from operator import itemgetter
from sys import stdin

__author__ = 'Aditya Bhargava'
__license__ = 'FreeBSD'
__version__ = '1.0.0'
__email__ = 'aditya@cs.toronto.edu'


data = defaultdict(list)
enlist = []
for line in stdin.readlines():
    line = line.strip()
    en, ph, score = line.split('\t')[0:3]
    if score == 'NULL':
        score = '-inf'
    score = float(score)
    data[en].append((line, score))
    if en not in enlist:
        enlist.append(en)

for en in enlist:
    data[en] = sorted(data[en], key=itemgetter(1), reverse=True)
    for line, score in data[en]:
        print(line)
