#!/usr/bin/env python3
'''
Sort lines of text files.

Like sort(1) but uses Python, allowing reliable UTF-8 sorting and uniquing.
Usage is:
    pysort.py [OPTION] [FILE]

FILE specifies the input text file; if it is - or unspecified, standard input
is used. The lines in the input text file are sorted according to Python's
sort() function.
'''

import optparse
from sys import stdin

__author__ = 'Aditya Bhargava'
__license__ = 'FreeBSD'
__version__ = '1.0.0'
__email__ = 'aditya@cs.toronto.edu'


parser = optparse.OptionParser(usage='usage: %prog [OPTION] FILE')
parser.add_option('-u', '--unique', dest='unique', action='store_true',
                  default=False, help='remove duplicates')

options, args = parser.parse_args()


def addLine(line):
    global lines
    if options.unique:
        lines.add(line)
    else:
        lines.append(line)

lines = set() if options.unique else []
if args:
    for arg in args:
        if arg == '-':
            for line in stdin.readlines():
                addLine(line)
        else:
            with open(arg) as input:
                for line in input:
                    addLine(line)
else:
    for line in stdin.readlines():
        addLine(line)

for line in sorted(lines):
    print(line, end='')
