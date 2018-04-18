#!/usr/bin/env bash
export PATH=$PATH:~/naacl12COPY/naacl12/util

language=$1

# Not quite done yet; Sequitur provides no structure in the output so to make
# things more fair we use m2m-aligner to give us some input-output alignments to
# use

# if sequitur is the original system then we should call this...

for t in trn tst
do
    cut -f 1,2 ${language}.$t.orig.sc | space.py > ${language}.$t.orig.sc.${language}
    ~/m2m-aligner-1.2/m2m-aligner --delX  --pScore  --alignerIn ../../${language}.full.trn.*.model \
        -i ${language}.$t.orig.sc.${language} --errorInFile
    sed -i -e 's/NO ALIGNMENT \t/NALGN\tNALGN\tNULL\tNULL/' *.align
    cut -f 1,2,4 ${language}.$t.orig.*.align | sed -e 's/://g' > \
        ${language}.$t.orig.sc.${language}
    paste ${language}.$t.orig.sc ${language}.$t.orig.sc.${language} > tmp
    mv tmp ${language}.$t.orig.sc
    rm *.${language}*
done

# Base accuracies:


# ADAM: I added the sed here to get rid of spaces. how did it work before without that...?

# Orig accuracy
#cut -f 1,2 ${language}.tst.orig.sc | sed -e 's/ //g' | tee ${language}.tst.orig.sc.base | eval.py ${language}.tst
#Word accuracy: 45.56%
#Phoneme accuracy: 79.02%
#Oracly re-ranked word accuracy: 84.40%
#Total words: 2801

# DirecTL+

#cut -f 1,2 ${language}.tst.dtlp.sc | sed -e 's/[|_]//g' | tee ${language}.tst.dtlp.sc.base \
#    | eval.py ${language}.tst
#Word accuracy: 48.52%
#Phoneme accuracy: 81.45%
#Oracly re-ranked word accuracy: 78.22%
#Total words: 2801
#
# NOTE: the difference in results compared to those reported in the paper is
# due to a different data split. Stupid random number generators/seeds :'(
