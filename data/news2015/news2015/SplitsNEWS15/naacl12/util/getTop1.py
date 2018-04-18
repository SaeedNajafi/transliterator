#!/usr/bin/env python3

from collections import Counter
from sys import stdin


printed = Counter()
for line in stdin.readlines():
    k, v = line.strip().split()
    if not printed[k]:
        print(' '.join(k), ' '.join(v), sep='\t')
        printed[k] = 1
