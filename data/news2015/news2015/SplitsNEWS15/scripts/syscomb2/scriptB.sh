#!/usr/bin/env bash
export PATH=$PATH:~/naacl12COPY/naacl12/util

langfront=$1
langend=$2

cd suppl
for t in trn tst
do
    sed -e '/^$/d' ../${langfront}${langend}.$t.dtlp | combine.py ${langfront}sq${langend}.$t > ${langfront}${langend}.$t.dtlp.sc
    alignSupOut.sh ${langfront}${langend}.$t.dtlp.sc ${langend} sq > ../${langfront}${langend}.$t.dtlp.sc

    sed -e '/^$/d' ../${langfront}${langend}.$t.seq | combine.py ${langfront}dt${langend}.$t > ${langfront}${langend}.$t.seq.sc
    alignSupOut.sh ${langfront}${langend}.$t.seq.sc ${langend} dt > ../${langfront}${langend}.$t.seq.sc

    sed -e '/^$/d' ../${langfront}${langend}.$t.joint | combine.py ${langfront}dt${langend}.$t > ${langfront}${langend}.$t.seq.sc
    alignSupOut.sh ${langfront}${langend}.$t.seq.sc ${langend} dt > ../${langfront}${langend}.$t.seq.sc

done

cd ..