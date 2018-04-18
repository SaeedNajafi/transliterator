#!/usr/bin/env bash

export PATH=$PATH:~/naacl12COPY/naacl12/util


lower=$1 # e.g. enhe
UPPER=$2 # EnHe
back=$3 # he


cp  ../$lower.trnPlusDev  $lower.trn.noprocessing # the noprocessing files are used when finding supplemental data for getSUpp.py script
sed 's/./ &/g;s/^ //'  ../${lower}11.tst >  ${lower}11.tst.noprocessing
sed 's/./ &/g;s/^ //'  ../${lower}12.tst >  ${lower}12.tst.noprocessing

# the process are used when using dtl since _ and spaces are weird
sed -e 's/ _ / # /g' -e 's/   / % /g' $lower.trn.noprocessing > $lower.trn
sed -e 's/ _ / # /g' -e 's/   / % /g' ${lower}11.tst.noprocessing > ${lower}11.tst
sed -e 's/ _ / # /g' -e 's/   / % /g' ${lower}12.tst.noprocessing > ${lower}12.tst

#if [ 0 -eq 1 ]; then

mkdir suppl; cd suppl
# NOTE: the set of supplemental corpora varies per base data set; this file is
# for EnJa, and if you wanted to do another set, make sure to adjust
# appropriately, e.g. for EnTh replace "[EnTh]=th" with "[EnJa]=ja"
# You will also want to change the "ja" bits inside the loop to "th"
# It might be easiest to compare this file with the corresponding README for the
# CELEX experiments to see how what the appropriate changes would be
declare -A sups
sups=([EnBa]=ba [EnCh]=ch [EnHe]=he [EnHi]=hi [EnJa]=ja [EnKa]=ka [EnKo]=ko [EnPe]=pe \
    [EnTa]=ta [EnTh]=th)
for sup in ${!sups[@]}
do
    if [ $sup == $UPPER ]; then
	continue # don't get supplemental data from itself
	
    fi
    getSupplemental.py ~/naacl12COPY/naacl12/data/$sup < ../$lower.trn.noprocessing | pysort.py -u | tee \
        en${sups[$sup]}$back.trn | cut -f 1,2 | sed -e 's/ _ / # /g' -e 's/   / % /g' | pysort.py -u > en${sups[$sup]}.trn
    getSupplementalTESTSET.py ~/naacl12COPY/naacl12/data/$sup < ../${lower}11.tst.noprocessing | pysort.py -u | tee \
        | sed -e 's/ _ / # /g' -e 's/   / % /g' | pysort.py -u > en${sups[$sup]}.tst11
    getSupplementalTESTSET.py ~/naacl12COPY/naacl12/data/$sup < ../${lower}12.tst.noprocessing | pysort.py -u | tee \
        | sed -e 's/ _ / # /g' -e 's/   / % /g' | pysort.py -u > en${sups[$sup]}.tst12

    ~/m2m-aligner-1.2/m2m-aligner --maxX 1 --delX -i en${sups[$sup]}.trn
    ~/m2m-aligner-1.2/m2m-aligner --maxX 1 --delX -i en${sups[$sup]}.tst11
    ~/m2m-aligner-1.2/m2m-aligner --maxX 1 --delX -i en${sups[$sup]}.tst12
done

setUpExtTranslits.py $lower trn > ../$lower.trn.ext
setUpExtTranslits.py $lower tst11 > ../${lower}11.tst.ext
setUpExtTranslits.py $lower tst12 > ../${lower}12.tst.ext

cd ..

#fi