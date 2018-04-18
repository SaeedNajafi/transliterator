''' script to read in a file from std and split it for holdout. The argument is the name of the output files.
    every 10th item is in the holdout set 
    Make sure to use python3, I think because of character encodings'''

import sys
from collections import defaultdict

outName = sys.argv[1]

trnFile = outName + '.small.trn'
holdOutFile = outName + '.holdOut'

data = defaultdict(list)

try:
    for line in sys.stdin.readlines():
        k, v = line.strip().split('\t')
        data[k].append(v)
except KeyboardInterrupt:
    exit()


with open(trnFile, 'w') as trn:
    with open(holdOutFile, 'w') as holdOut:
        sourceCount = 0
        for source in sorted(data.keys()):
            if sourceCount % 10 == 0:
                out = holdOut
            else:
                out = trn

            for target in data[source]:
                out.write("{}\t{}\n".format(source,target))
            sourceCount += 1
