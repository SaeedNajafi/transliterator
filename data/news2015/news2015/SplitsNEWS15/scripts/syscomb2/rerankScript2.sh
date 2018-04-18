#!/usr/bin/env bash
export PATH=$PATH:~/naacl12COPY/naacl12/util

language=$1
langfront=$2
langend=$3

cd suppl
for t in trn tst
do
    sed -e '/^$/d' ../${language}.$t.orig | combine.py ${langfront}ext${langend}.$t > ${language}.$t.orig.sc
    alignSupOut.sh ${language}.$t.orig.sc ${langend} ext > ../${language}.$t.orig.sc

    # don't care about the extra?
    #sed -e '/^$/d' ../${langfront}${langend}.$t.seq | combine.py ${langfront}dt${langend}.$t > ${langfront}${langend}.$t.seq.sc
    #alignSupOut.sh ${langfront}${langend}.$t.seq.sc ${langend} dt > ../${langfront}${langend}.$t.seq.sc
done

cd ..