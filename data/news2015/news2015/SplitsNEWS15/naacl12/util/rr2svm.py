#!/usr/bin/env python3
'''Converts an SVMrank-style reranking problem into a libsvm-style SVM binary
classification problem.'''

from collections import defaultdict
from sys import stdin, stderr

__author__ = 'Aditya Bhargava'
__license__ = 'FreeBSD'
__version__ = '1.0.0'
__email__ = 'aditya@cs.toronto.edu'


def subtract(d1, d2):
    thefeats = set(d1) | set(d2)
    maxFeat = max(thefeats)
    ret = defaultdict(float)
    for feat in thefeats:
        val = d1[feat] - d2[feat]
        if val or feat == maxFeat:
            ret[feat] = val

    return ret


def process(q):
    for i, q_i in enumerate(query):
        for j, q_j in enumerate(query[i + 1:], i + 1):
            if q_i[0] > q_j[0]:
                print('1 ', end='')
                sub = subtract(q_i[2], q_j[2])
                for feat in sorted(sub):
                    print('{}:{:.8g} '.format(feat, round(sub[feat], 8)),
                          end='')
                print()
                #print('# {} {} {}'.format(q_i[1], i + 1, j + 1))
            elif q_i[0] < q_j[0]:
                print('-1 ', end='')
                sub = subtract(q_i[2], q_j[2])
                for feat in sorted(sub):
                    print('{}:{:.8g} '.format(feat, round(sub[feat], 8)),
                          end='')
                print()
                #print('# {} {} {}'.format(q_i[1], i, j))

query = []
line = stdin.readline()
linecount = 0
while line:
    line = line.split('#')[0].strip()
    linecount += 1
    #if linecount % 1000 == 0:
        #print(linecount, file = stderr)
    stuff = line.strip().split(' ')
    qid = int(stuff[1].split(':')[1])
    feats = defaultdict(float)

    for text in stuff[2:]:
        f, v = text.split(':')
        feats[int(f)] = float(v)

    if not len(query) or qid == query[-1][1]:
        query.append((int(stuff[0]), qid, feats))
    else:
        process(query)
        query = []
        query.append((int(stuff[0]), qid, feats))

    line = stdin.readline()

process(query)
