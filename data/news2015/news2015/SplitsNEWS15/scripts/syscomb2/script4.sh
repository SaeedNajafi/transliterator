#!/usr/bin/env bash
export PATH=$PATH:~/naacl12COPY/naacl12/util

TRAIN=~/liblinear-1.96/train

language=$1

mkdir sequitur directlp

# about 1h and ~13GiB of RAM
featurizer.py -n ${language}.trn ${language}.trn.seq.sc sequitur/rerank.trn /dev/null \
    ${language}.tst.seq.sc sequitur/rerank.tst

echo "first featurizing done"

# ditto
featurizer.py ${language}.trn ${language}.trn.dtlp.sc directlp/rerank.trn /dev/null \
    ${language}.tst.dtlp.sc directlp/rerank.tst
