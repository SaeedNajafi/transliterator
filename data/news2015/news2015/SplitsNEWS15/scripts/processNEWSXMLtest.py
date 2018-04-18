#!/usr/bin/env python3

from optparse import OptionParser
from os import path
from string import punctuation
from sys import argv
from xml.etree import ElementTree

import re


def errordie(msg):
    print(path.basename(argv[0]), ': error: ', msg, sep = '')
    exit()

parser = OptionParser(usage = 'usage: %prog [options args] DATA.xml')
parser.add_option('-p', '--handle-punctuation', action='store_true',
                  dest='handlepunc', default=False, help=
                  'Process the punctuation (specific to Hindi data)')

(options, args) = parser.parse_args()

if len(args) == 0:
    errordie('no XML file specified')
elif len(args) == 1:
    datafile = args[0]
elif len(args) > 1:
    errordie('too many arguments')

smartReplace = [(re.compile('/'), ' '),
                (re.compile(',([^ ])'), r', \1'),
                (re.compile('_'), '#'),
                (re.compile('[' + re.sub("['#^-]", '', punctuation) + ']'), '')
               ]

tree = ElementTree.parse(datafile)
corpus = tree.getroot()
for tlset in corpus:
    id = tlset.get('ID')
    src = tlset[0].text.strip()
    if options.handlepunc:
        for cre, sub in smartReplace:
            src = cre.sub(sub, src)

    for s in src.split(' '):
        print(id, s, sep = '\t')
