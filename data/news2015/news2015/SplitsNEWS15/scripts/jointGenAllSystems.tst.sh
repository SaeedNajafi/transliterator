# this script needs the sequitur output for  dev set, and the dev set itself. Also requires the MODEL from training (seqSuppJointGen.train.sh)
#    it will set up and do leis dtl training using seuitur output as supplemental data and give the output

DEV=$1
DTLDEV=$2
SEQDEV=$3
SMTDEV=$4
LANGUAGE=$5 # e.g. enhe
MODEL=$6
TAGS=$7

if [ $TAGS == yes ]; then
    PREPARESCRIPT=~/NEWS15/scripts/prepareSystemOutputForAlignmentNewScript.py
else
   PREPARESCRIPT=~/NEWS15/scripts/prepareSystemOutputForAlignment.py
fi


# first get the Sequitur output in a pperared format for m2m
cut -f 1,2 $DTLDEV > tmp
$PREPARESCRIPT tmp 1 > $LANGUAGE.dev.dtl.prepared

cut -f 1,4 $SEQDEV > tmp
$PREPARESCRIPT tmp 2 > $LANGUAGE.dev.seq.prepared

cut -f 2,3 $SMTDEV > tmp
$PREPARESCRIPT tmp 3 > $LANGUAGE.dev.smt.prepared
rm tmp


# now align the holdout set and the sequitur output

M2M=~/m2m-aligner-1.2/m2m-aligner

$M2M --delX --maxX 1 -i $DEV --maxY 2
$M2M --delX --maxX 1 -i $LANGUAGE.dev.dtl.prepared --maxY 2
$M2M --delX --maxX 1 -i $LANGUAGE.dev.seq.prepared --maxY 2
$M2M --delX --maxX 1 -i $LANGUAGE.dev.smt.prepared --maxY 2



# now get the aligned Sequitur output as supplemental data like Lei's .ext files
~/NEWS15/scripts/setUpExtSystems.py $LANGUAGE.dev.dtl.prepared.*.align $LANGUAGE.dev.seq.prepared.*.align $LANGUAGE.dev.smt.prepared.*.align > $LANGUAGE.dev.ext


# get the testing file sources ready to input to dtl
cut -f 1 $DEV.m*.align | uniq > $DEV.words

# need to match the supple data so each line corresponds to the line in the aligned source
~/NEWS15/scripts/matchSuppWithSource.py $DEV.words $LANGUAGE.dev.ext > $LANGUAGE.dev.ext.matched

# now test using lei's dtl
~/DirecTL-p-3j-speedup-general/directlp --mi $MODEL  -t $DEV.words --outChar ' ' -a $LANGUAGE.output --inChar : --extFeaTest $LANGUAGE.dev.ext.matched --nBestTest 10 --order 1 --linearChain --jointMgram 6


