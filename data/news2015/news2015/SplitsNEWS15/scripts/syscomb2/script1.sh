#!/usr/bin/env bash
export PATH=$PATH:~/naacl12COPY/naacl12/util

language=$1
langfront=$2
langend=$3

cat ../$language.9.tst | sed -e 's/_/#/g' -e 's/   / % /g' >  $language.trn # the trn set is the training for the reranker, ie the holdOut set
cat ../../$language.dev | sed -e 's/_/#/g' -e 's/   / % /g'  > $language.tst # and the tst set is actually the NEWS dev set
cat ../${language}9.phraseOut | sed -e 's/_/#/g' -e 's/ /%/g' > ${language}.trn.dtlp
cat ../${language}.9.tst.seq.out | sed -e 's/_/#/g' -e 's/ /%/g' > ${language}.trn.seq
cat ../${language}Dev.phraseOut | sed -e 's/_/#/g' -e 's/ /%/g' > ${language}.tst.dtlp
cat ../${language}.dev.seq.out | sed -e 's/_/#/g' -e 's/ /%/g' > ${language}.tst.seq

cut -f 1,4 ${language}.trn.seq | sed -e '/^$/d' | getTop1.py > ${language}.trn.seq.top1
cut -f 1,4 ${language}.tst.seq | sed -e '/^$/d' | getTop1.py > ${language}.tst.seq.top1
cut -f 1,2 ${language}.trn.dtlp | sed -e 's/[|_]//g' -e '/^$/d' | getTop1.py > \
    ${language}.trn.dtlp.top1
cut -f 1,2 ${language}.tst.dtlp | sed -e 's/[|_]//g' -e '/^$/d' | getTop1.py > \
    ${language}.tst.dtlp.top1

mkdir suppl; cd suppl
declare -A sups
sups=([dtlp]=dt [seq]=sq)
for sup in ${!sups[@]}
do
    getSupplemental.py ../${language}.trn.$sup.top1 < ../${language}.trn | pysort.py -u | \
        tee ${langfront}${sups[$sup]}${langend}.trn | cut -f 2,3 | pysort.py -u > \
        ${sups[$sup]}${langend}.trn
    getSupplemental.py ../${language}.tst.$sup.top1 < ../${language}.tst | pysort.py -u | \
        tee ${langfront}${sups[$sup]}${langend}.tst | cut -f 2,3 | pysort.py -u > \
        ${sups[$sup]}${langend}.tst
    ~/m2m-aligner-1.2/m2m-aligner --delX -i ${sups[$sup]}${langend}.trn
done
#rm ??${langend}.{trn,tst} *.align!(.model) # not useful


cd ..
