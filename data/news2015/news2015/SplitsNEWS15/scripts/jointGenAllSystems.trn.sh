# this script needs the 3 system outputs for holdout along with the holdout set itself.
#    it will set up and do leis dtl training using system output as supplemental data 
# if want to use this without one of the systems, make an empty file called null or something, and pass that in. The emptiness will propgate through
# and the .ext file will only include the other two systems


HOLDOUT=$1
DTLHOLDOUT=$2
SEQHOLDOUT=$3
SMTHOLDOUT=$4
LANGUAGE=$5 # e.g. "enhe"

TAGS=$6 # yes or no

#echo $SEQHOLDOUT


if [ $TAGS == yes ]; then
    PREPARESCRIPT=~/NEWS15/scripts/prepareSystemOutputForAlignmentNewScript.py
else
   PREPARESCRIPT=~/NEWS15/scripts/prepareSystemOutputForAlignment.py
fi

# first get the system outputs in a prepared format for m2m
cut -f 1,2 $DTLHOLDOUT > tmp
$PREPARESCRIPT tmp 1 > $LANGUAGE.holdOut.dtl.prepared

cut -f 1,4 $SEQHOLDOUT > tmp
$PREPARESCRIPT tmp 2 > $LANGUAGE.holdOut.seq.prepared

cut -f 2,3 $SMTHOLDOUT > tmp
$PREPARESCRIPT  tmp 3 > $LANGUAGE.holdOut.smt.prepared
rm tmp

# now align the holdout set and the system outputs

M2M=~/m2m-aligner-1.2/m2m-aligner

$M2M --delX --maxX 1 -i $HOLDOUT --maxY 2
$M2M --delX --maxX 1 -i $LANGUAGE.holdOut.dtl.prepared --maxY 2
$M2M --delX --maxX 1 -i $LANGUAGE.holdOut.seq.prepared --maxY 2
$M2M --delX --maxX 1 -i $LANGUAGE.holdOut.smt.prepared --maxY 2


# now get the aligned system output as supplemental data like Lei's .ext files
~/NEWS15/scripts/setUpExtSystems.py $LANGUAGE.holdOut.dtl.prepared.*.align  $LANGUAGE.holdOut.seq.prepared.*.align  $LANGUAGE.holdOut.smt.prepared.*.align  > $LANGUAGE.holdOut.ext  

# now train using lei's dtl
~/DirecTL-p-3j-speedup-general/directlp -f $HOLDOUT.m*.align --inChar : --extFeaTrain $LANGUAGE.holdOut.ext --order 1 --linearChain  --jointMgram 6 