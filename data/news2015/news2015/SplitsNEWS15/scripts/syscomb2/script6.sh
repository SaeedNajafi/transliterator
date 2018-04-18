#!/usr/bin/env bash
export PATH=$PATH:~/naacl12COPY/naacl12/util


language=$1

# Now we do the linear combination baseline. Since the linear weight is not a
# hyperparameter we don't need to worry about finding the parameter during
# development and can do it directly on the training set here.
for t in trn tst
do
    for s in seq dtlp
    do
        cut -f 1-3 ${language}.$t.$s.sc | sed 's/ //g' | scale.py > ${language}.$t.$s.scaled
    done
done

#for f in $(seq 0 0.01 1)
#do
#    linComb.py ${language}.trn.seq.scaled ${language}.trn.dtlp.scaled $f | eval.py ${language}.trn
#done
# Best value of lambda is 0.49, so let's use it:



linComb.py ${language}.tst.seq.scaled ${language}.tst.dtlp.scaled 0.49 | tee ${language}.tst.lc | \
    eval.py ${language}.tst; mcNemars.py ${language}.tst ${language}.tst.seq.sc ${language}.tst.lc; \
    mcNemars.py ${language}.tst ${language}.tst.dtlp.sc ${language}.tst.lc
#Word accuracy: 50.37%
#Character accuracy: 82.23%
#Oracly re-ranked word accuracy: 87.22%
#Total words: 2801
#Performance increase: 10.58%
#Significant with p < 0.001
#p = 1.61393121089759e-12
#Error reduction: 3.61%
#Performance increase: 3.83%
#Significant with p < 0.001
#p = 0.000297285799665592
#NOTE: Better ERR for Sequitur and slightly worse (but still significant) for
#      DTL+ than in the paper
