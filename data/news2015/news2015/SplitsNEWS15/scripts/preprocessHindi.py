#!/usr/bin/env python3 

''' this script is based off of Aditya's "getNEWS.py" script found in his reranker code in the data directory.
    attempting to preprocess hindi for the NEWS task
    takes the name of the file to preprocess as argv[1] and prints out the preprocessed stuff
'''

from collections import defaultdict
import sys



withAndWO = re.compile("['_^]")
smartReplace = [(re.compile('/'), ' '),
                (re.compile(',([^ ])'), r', \1'),
                (re.compile('[' + withAndWO.sub('', re.sub('-', '',
                                                           punctuation)) +
                            ']'), '')]
hindi = [(re.compile(chr(0x0958)), chr(0x0915) + chr(0x093C)),
         (re.compile(chr(0x0959)), chr(0x0916) + chr(0x093C)),
         (re.compile(chr(0x095A)), chr(0x0917) + chr(0x093C)),
         (re.compile(chr(0x095B)), chr(0x091C) + chr(0x093C)),
         (re.compile(chr(0x095C)), chr(0x0921) + chr(0x093C)),
         (re.compile(chr(0x095D)), chr(0x0922) + chr(0x093C)),
         (re.compile(chr(0x095E)), chr(0x092E) + chr(0x093C)),
         (re.compile(chr(0x095F)), chr(0x092F) + chr(0x093C))]



handlepunc = lang == 'Hi' and options.handlepunc
hindistuff = lang == 'Hi' and options.hindi


transliterations = defaultdict(set)

with open(sys.argv[1], 'r') as file:
    for line in file:
        src, trans = line.strip().split('\t')
        #src = tlset[0].text.strip().lower()
        if handlepunc:
            for cre, sub in smartReplace:
                src = cre.sub(sub, src)
                trans = cre.sub(sub, trans)

        srcs = src.split(' ')
        if hindistuff:
            for cre, sub in hindi:
                trans = cre.sub(sub, trans)
        trans = trg.split(' ')
                if not options.nospacemm or len(srcs) == len(trgs):
                    if options.splitwords:
                        for s, t in zip(srcs, trgs):
                            transliterations[s].add(t)
                            if handlepunc:
                                snew = withAndWO.sub('', s)
                                tnew = withAndWO.sub('', t)
                                transliterations[snew].add(tnew)
                    else:
                        transliterations[src].add(trg)
                        if handlepunc:
                            srcnew = withAndWO.sub('', src)
                            trgnew = withAndWO.sub('', trg)
                            transliterations[srcnew].add(trgnew)

    with open('En' + lang, 'w') as outp:
        print(lang, len(transliterations), sep='\t')
        for entry in sorted(transliterations):
            for transliteration in sorted(transliterations[entry]):
                outp.write('\t'.join([' '.join(entry),
                                      ' '.join(transliteration)]) + '\n')

