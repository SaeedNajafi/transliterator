#!/bin/bash

g2p.py -t $1 -d 10% -n $1.model.1 -e UTF-8
for (( i=2; i<=$2; i++ ))
do
    g2p.py -t $1 -d 10% -r -m $1.model.$((i-1)) -n $1.model.$i -e UTF-8
done
cut -f 1 $3 | sed -e 's/ //g' | uniq | g2p.py -m $1.model.$2 -a - -e UTF-8 \
    --variants-number=10 | sed -e 's/ //g' > $(basename $3).out
