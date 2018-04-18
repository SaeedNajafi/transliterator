#!/usr/bin/env bash
export PATH=$PATH:~/naacl12COPY/naacl12/util

TRAIN=~/liblinear-1.96/train

language=$1


paste ${language}.tst.dtlp.sc.base directlp/rerank.tst.out | cut -f 1-3 | rerank.py | \
    tee ${language}.tst.dtlp.sc.reranked | eval.py ${language}.tst; mcNemars.py ${language}.tst \
    ${language}.tst.dtlp.sc.{base,reranked}


sed 's/ //g' ${language}.tst.dtlp.sc.reranked > tmp
sed -e 's/#/_/g' -e 's/%/ /g' tmp >  ${language}.dtlp.sc.final # convert back to spaces and underscoress
evalDirecTL.sh ${language}.dtlp.sc.final ../../dev.xml
