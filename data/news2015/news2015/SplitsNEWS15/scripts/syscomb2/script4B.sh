#!/usr/bin/env bash
export PATH=$PATH:~/naacl12COPY/naacl12/util

TRAIN=~/liblinear-1.96/train

language=$1

mkdir sequitur directlp

# about 1h and ~13GiB of RAM
#featurizer.py -c -C -t -l -L -j -n -N ${language}.trn ${language}.trn.seq.sc sequitur/rerank.trn /dev/null \
#    ${language}.tst.seq.sc sequitur/rerank.tst

echo "first featurizing done"

# ditto
# turning off all features that aren't related to score
# so no -s or -d (wonder if should use -M for MRR)
featurizer.py -c -C -t -l -L -j -n -N ${language}.trn ${language}.trn.dtlp.sc directlp/rerank.trn /dev/null \
    ${language}.tst.dtlp.sc directlp/rerank.tst
