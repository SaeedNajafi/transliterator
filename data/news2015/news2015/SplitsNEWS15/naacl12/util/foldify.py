#!/usr/bin/env python3
'''
Split lines of text files into folds.

Usage is:
    foldify.py [OPTIONS] BASENAME

Data is read on standard input. The lines are expected to tab-separated
input-output pairs. BASENAME specifies the prefix for the output filenames. For
example, if BASENAME is set to "data" then if producing 10 folds the output
files would be data.trn.0 to data.trn.9 and data.tst.0 to data.tst.9.

The splits are done by input, so that if there are multiple valid outputs for a
given input, the input does not accidentally appear in both the training and
test sets for a given fold. The data are split pseudorandomly, with a
hard-coded RNG seed. The default number of folds is 10; use the -h option to
see how to change this as well as the RNG seed.
'''

import optparse
import random
from collections import defaultdict
from sys import argv, stdin

__author__ = 'Aditya Bhargava'
__license__ = 'FreeBSD'
__version__ = '1.0.0'
__email__ = 'aditya@cs.toronto.edu'


def errordie(msg, exitcode):
    print(argv[0], ': error: ', msg, sep='')
    exit(exitcode)

planck = 6.626e-34
parser = optparse.OptionParser(usage='usage: %prog [OPTIONS] BASENAME')
parser.add_option('-n', '--folds', dest='folds', type='int', default=10,
                  help='number of folds')
parser.add_option('-s', '--seed', action='store', dest='seed', type='int',
                  default=planck,
                  help="RNG seed; default is Planck's constant")

(options, args) = parser.parse_args()

if len(args) == 0:
    errordie('no output file specified', 2)
elif len(args) > 1:
    errordie('too many options specified', 2)

random.seed(options.seed)

outbase = args[0]

data = defaultdict(list)
for line in stdin.readlines():
    k, v = line.strip().split('\t')
    data[k].append(v)

shuffled = list(data)
random.shuffle(shuffled)

trn, tst = [], []
for i in range(options.folds):
    trn.append([])
    tst.append([])
indices = set(k for k in range(10))
for i in range(len(shuffled)):
    j = i % options.folds
    tst[j].append(shuffled[i])
    for k in indices - {j}:
        trn[k].append(shuffled[i])

for i in range(options.folds):
    with open('{}.{}.trn'.format(outbase, i), 'w') as outp:
        for k in sorted(trn[i]):
            for v in data[k]:
                outp.write('\t'.join((k, v)) + '\n')
    with open('{}.{}.tst'.format(outbase, i), 'w') as outp:
        for k in sorted(tst[i]):
            for v in data[k]:
                outp.write('\t'.join((k, v)) + '\n')
