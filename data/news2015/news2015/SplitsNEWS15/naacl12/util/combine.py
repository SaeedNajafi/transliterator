#!/usr/bin/env python3

from collections import defaultdict
from optparse import OptionParser
from sys import argv, stdin


def errordie(msg, exitcode):
    print(argv[0], ': error: ', msg, sep='')
    exit(exitcode)

parser = OptionParser(usage='usage: %prog INSUPOUT1 INSUPOUT2 ... < SYSOUT')

(options, args) = parser.parse_args()

if len(args) == 0:
    errordie('no input-supplemental-output file(s) specified', 2)

allsupdata = []
for insupoutfile in args:
    insupdata = defaultdict(list)
    with open(insupoutfile) as inp:
        for line in inp:
            inData, sup = line.strip().split('\t')[:2]
            incln = inData.replace(' ', '')
            if sup not in insupdata[incln]:
                insupdata[incln].append(sup)
    allsupdata.append(insupdata)

data = defaultdict(list)
for line in stdin.readlines():
    k, f1, f2, f3 = line.strip().split('\t')
    try:
        r, s, v = int(f1), f2, f3  # Sequitur
    except ValueError:
        v, r, s = f1, int(f2), f3  # DirecTL+
    data[''.join(c for c in k if c not in '|_')].append((k, v, s))

for incln in data:
    for inData, out, sc in data[incln]:
        line = '\t'.join((inData, out, sc)) + '\t'
        outcln = ''.join(c for c in out if c not in '|_')
        insome = False
        for insupdata in allsupdata:
            if insupdata[incln]:
                for sup in insupdata[incln]:
                    insome = True
                    if ' ' in sup:
                        line += sup
                    else:
                        line += ' '.join(sup)
                    break
            else:
                line += 'NULL'
            line += '\t'

        if insome:
            if not outcln:  # can't remember what this is for
                print(line + '_')
            else:
                print(line + ' '.join(outcln))
