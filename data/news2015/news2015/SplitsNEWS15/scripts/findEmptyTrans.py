''' this script looks through a dtl output file and finds if there was an empty translit '''

import sys

with open(sys.argv[1], 'r') as file:
    count = 1
    for line in file:
        source, trans = line.split('\t')
        if trans == '\n' or trans.replace(' ', '') == 'n':
            print("empty trans on line {0}: {1}".format(count, line.strip()))
        count += 1
