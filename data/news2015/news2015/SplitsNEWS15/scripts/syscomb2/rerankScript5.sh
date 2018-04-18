#!/usr/bin/env bash
export PATH=$PATH:~/naacl12COPY/naacl12/util

TRAIN=~/liblinear-1.96/train

language=$1

# Below, when I refer to best C values, I use D for the denominator. D is the
# number of QIDs in the training set. I show the command in each case to find
# the value.
cd original
cut -d# -f 1 rerank.trn | rr2svm.py > pair.trn

# during dev we found the best C = 8/D
# to find D do:
tail -n 1 rerank.trn | cut -d ' ' -f 2 | cut -d ':' -f 2
# D = 25211, so C = 0.0003173218039744556
# ADAM: D = 2621, so C = 0.0030522701
$TRAIN -c 0.00305227012 pair.trn model
llnrpredictr.py rerank.tst model > rerank.tst.out

#cd ../directlp
#cut -d# -f 1 rerank.trn | rr2svm.py > pair.trn

# during dev we found the best C = 4/D
# to find D do:
#tail -n 1 rerank.trn | cut -d ' ' -f 2 | cut -d ':' -f 2
# D = 25211, so C = 0.0001586609019872278 ADAM: D = 2621
#$TRAIN -c 0.00305227012 pair.trn model
#llnrpredictr.py rerank.tst model > rerank.tst.out

cd ..
# Get the results
paste ${language}.tst.orig.sc.base original/rerank.tst.out | cut -f 1-3 | rerank.py | \
    tee ${language}.tst.orig.sc.reranked | eval.py ${language}.tst; mcNemars.py ${language}.tst \
    ${language}.tst.orig.sc.{base,reranked}

#Word accuracy: 50.05%
#Character accuracy: 82.20%
#Oracly re-ranked word accuracy: 84.40%
#Total words: 2801
#Error reduction: 8.26%
#Performance increase: 9.87%
#Significant with p < 0.001
#p = 1.5761048022255864e-10
# NOTE: a bit weaker than in the paper

#paste ${language}.tst.dtlp.sc.base directlp/rerank.tst.out | cut -f 1-3 | rerank.py | \
#    tee ${language}.tst.dtlp.sc.reranked | eval.py ${language}.tst; mcNemars.py ${language}.tst \
#    ${language}.tst.dtlp.sc.{base,reranked}
#Word accuracy: 49.66%
#Character accuracy: 81.68%
#Oracly re-ranked word accuracy: 78.22%
#Total words: 2801
#Error reduction: 2.22%
#Performance increase: 2.35%
#Not statistically significant
#p = 0.027047248378120115
# NOTE: a bit weaker than in the paper



# ADAM
# evaluate results for NEWS results

#echo "NEWS results for dtl reranked"
#sed 's/ //g' ${language}.tst.dtlp.sc.reranked > tmp
#sed -e 's/#/_/g' -e 's/%/ /g' tmp >  ${language}.dtlp.sc.final # convert back to spaces and underscoress
#evalDirecTL.sh ${language}.dtlp.sc.final ../../dev.xml

echo "NEWS results for orig reranked"
sed 's/ //g' ${language}.tst.orig.sc.reranked > tmp
sed -e 's/#/_/g' -e 's/%/ /g' tmp >  ${language}.orig.sc.final # convert back to spaces and underscoress
evalDirecTL.sh ${language}.orig.sc.final ../../dev.xml