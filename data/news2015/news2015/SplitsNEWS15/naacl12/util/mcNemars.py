#!/usr/bin/env python3

import optparse
from collections import defaultdict
from math import factorial, pow
from sys import argv, stderr

__author__ = 'Aditya Bhargava'
__license__ = 'FreeBSD'
__version__ = '1.0.0'
__email__ = 'aditya@cs.toronto.edu'


def errordie(msg):
    print(msg, file=stderr)
    exit()

parser = optparse.OptionParser(usage='usage: %prog GOLD BEFORE AFTER')
(options, args) = parser.parse_args()

if len(args) != 3:
    errordie('must have exactly three arguments')

def readfile(thefile):
    ret = defaultdict(list)
    with open(thefile) as filein:
        for line in filein:
            k, v = line.replace(' ', '').strip().split('\t')[0:2]
            ret[k].append(v)

    return ret

gold = readfile(args[0])
before = readfile(args[1])
after = readfile(args[2])

# do some quick checks
for entry in before:
    if entry not in gold:
        errordie("before has something gold doesn't")
    if entry not in after:
        errordie("before has something after doesn't")

for entry in after:
    if entry not in gold:
        errordie("after has something gold doesn't")
    if entry not in before:
        errordie("after has something before doesn't")

pp, pm, mp, mm = 0, 0, 0, 0
for entry in before:
    bp = before[entry][0] in gold[entry]
    ap = after[entry][0] in gold[entry]

    if bp and ap:
        pp += 1
    elif bp and not ap:
        pm += 1
    elif not bp and ap:
        mp += 1
    elif not bp and not ap:
        mm += 1



# ADAM: I am adding these divide by 0 checks

if (mp + mm == 0):
    print("mp + mm == 0")
else:
    print('Error reduction: {:.2%}'.format((mp - pm) / (mp + mm)))

if (pp + pm <= 0):
    print("pp + pm = 0")
else:
    print('Performance increase: {:.2%}'.format((mp - pm) / (pp + pm)))
#print('++ {}'.format(pp))
#print('+- {}'.format(pm))
#print('-+ {}'.format(mp))
#print('-- {}'.format(mm))

chiSquared = (pm - mp) * (pm - mp) / (pm + mp)

#print('chi squared =', chiSquared)

if chiSquared > 10.83:
    print('Significant with p < 0.001')
elif chiSquared > 6.64:
    print('Significant with p < 0.01')
elif chiSquared > 3.84:
    print('Significant with p < 0.05')
else:
    print('Not statistically significant')


# binomial is more exact than chi-squared
def choose(n, k):
    if not 0 <= k <= n:
        return 0
    if k == 0 or k == n:
        return 1
    P = k + 1
    for i in range(k + 2, n + 1):
        P *= i
    #C, rem = divmod(P, factorial(n - k))
    #assert rem = 0
    #return C
    return P / factorial(n - k)

n = mp + pm
p = 1 - pow(0.5, n) * sum(choose(n, i) for i in range(mp + 1))
print('p =', p)
