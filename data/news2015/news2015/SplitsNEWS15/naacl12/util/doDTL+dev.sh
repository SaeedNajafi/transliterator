#!/usr/bin/env bash

# set some variables
if [ -z $3 ]
then
    maxX=2
else
    maxX=$3
fi
if [ -z $4 ]
then
    maxY=2
else
    maxY=$4
fi
if [ -z $5 ]
then
    iter="--tal 5"
elif [ $5 -gt 5 ]
then
    iter="--tal 5 --tam $5"
else
    iter="--tam 5"
fi

m2m-aligner --delX --maxX $maxX --maxY $maxY -i $1
m2m-aligner --delX --maxX $maxX --maxY $maxY --alignerIn $1.*.model -i $2
rm *.err # probably empty, and not really helpful regardless

# train-at-most (tam) parameter determined during development
directlp --inChar : --tal 5 --order 1 --linearChain --jointMgram 5 -f \
    $1.*.align -t <(cut -f 1 $2.*.align | sed -e 's/:/|/g' | uniq) -a \
    $2.out --nBestTest 10 -d $2.*.align
