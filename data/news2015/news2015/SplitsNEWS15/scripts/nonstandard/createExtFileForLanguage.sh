#!/usr/bin/env bash

export PATH=$PATH:~/naacl12COPY/naacl12/util



# this script will set up the current directory (within a language directory) for the supplemental joint system. 
# note that it uses the ful training set ***

lower=$1 # e.g. enhe
UPPER=$2 # EnHe
back=$3 # he


cp  ../$lower.full.trn  $lower.trn.noprocessing # the noprocessing files are used when finding supplemental data for getSupp.py script
cp  ../$lower.dev  $lower.tst.noprocessing

# the process are used when using dtl since _ and spaces are weird
sed -e 's/ _ / # /g' -e 's/   / % /g' $lower.trn.noprocessing > $lower.trn
sed -e 's/ _ / # /g' -e 's/   / % /g' $lower.tst.noprocessing > $lower.tst




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
    getSupplemental.py ~/naacl12COPY/naacl12/data/$sup < ../$lower.tst.noprocessing | pysort.py -u | tee \
        en${sups[$sup]}$back.tst | cut -f 1,2 | sed -e 's/ _ / # /g' -e 's/   / % /g' | pysort.py -u > en${sups[$sup]}.tst
    ~/m2m-aligner-1.2/m2m-aligner --maxX 1 --delX -i en${sups[$sup]}.trn
    ~/m2m-aligner-1.2/m2m-aligner --maxX 1 --delX -i en${sups[$sup]}.tst
done

setUpExtTranslits.py $lower trn > ../$lower.trn.ext
setUpExtTranslits.py $lower tst > ../$lower.tst.ext

cd ..

