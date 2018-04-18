#!/usr/bin/env python3 

''' this script will take as input a language name (e.g enhi) and will use all other aligned languages for supplemental data
    and place them on a line similar to lei's .ext file
'''

import sys

languages = ['enba', 'ench', 'enhe', 'enhi', 'enja', 'enka', 'enko', 'enpe', 'enta', 'enth']

thisLanguage = sys.argv[1]

languages.remove(thisLanguage) # no supplemental data for this language itself


ending = sys.argv[2] # either trn or tst

# this function fills a dictionary with keys for each source word and values for each supplemental transliteration across languages
def processData(ending):
    data = {}
    for language in languages:
        with open(language + "." +  ending + ".m-mAlign.1-2.delX.1-best.conYX.align", 'r') as file:
            for line in file:
                source, trans = line.strip().split('\t')
                if not source in data:
                    data[source] = [trans] # the first suppl for this source
                else:
                    # otherwise, the source has already been seen before
                    data[source].append(trans)
    return data


data = processData(ending)
for source in sorted(data):
    print("\t".join([source] + data[source]))
