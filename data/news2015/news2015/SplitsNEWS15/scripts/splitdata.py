#!/usr/bin/env python3
'''
Split lines in text file into training, development, and test sets.

Usage is:
    splitdata.py [OPTION] [BASENAME]

Data is read on standard input. The lines are expected to tab-separated
input-output pairs. If BASENAME is specified, it is used to prefix the output
filenames (for example, if BASENAME is set to "data" then the three output
files would be data.trn, data.dev, and data.tst). If it is unspecified, the
three output files are simply trn, dev, and tst.

The splits are done by input, so that if there are multiple valid outputs for a
given input, the input does not accidentally appear in two sets. The data are
assigned to the sets pseudorandomly, with a hard-coded RNG seed. The default
training/development/test split is 80/10/10; use the -h option to see how to
change this as well as the RNG seed. (Note that the actual fraction used is the
reciprocal of the command-line option, so if you want 1/5 of the data for a
particular set, the command-line option should be 5.)
'''

import optparse, random
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
parser = optparse.OptionParser(usage='usage: %prog [OPTION] [BASENAME]')
parser.add_option('-t', '--test', dest='test', type='int', default=10,
                  help='fraction of data for testing; 0 to disable')
parser.add_option('-d', '--dev', dest='dev', type='int', default=10,
                  help='fraction of data for development; 0 to disable')
parser.add_option('-s', '--seed', action='store', dest='seed', type='int',
                  default=planck, help="RNG seed; default is Planck's "
                  "constant")

(options, args) = parser.parse_args()

outbase = ''
if len(args) == 1:
    outbase = args[0] + '.'
elif len(args) > 1:
    errordie('too many options specified', 2)

random.seed(options.seed)

trnfile = outbase + 'trn'
tstfile = outbase + 'tst'
devfile = outbase + 'dev'

data = defaultdict(list)
try:
    for line in stdin.readlines():
        k, v = line.strip().split('\t')
        data[k].append(v)
except KeyboardInterrupt:
    exit()

total = len(data)
testsize = round(total / options.test) if options.test else 0
devsize = round(total / options.dev) if options.dev else 0

testset = sorted(random.sample(list(data), testsize))
if testset:
    with open(tstfile, 'w') as op:
        for k in testset:
            for v in data[k]:
                op.write('\t'.join((k, v)) + '\n')
            del data[k]

devset = sorted(random.sample(list(data), devsize))
if devset:
    with open(devfile, 'w') as op:
        for k in devset:
            for v in data[k]:
                op.write('\t'.join((k, v)) + '\n')
            del data[k]

with open(trnfile, 'w') as op:
    for k in sorted(data):
        for v in data[k]:
            op.write('\t'.join((k, v)) + '\n')
