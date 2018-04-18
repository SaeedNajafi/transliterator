# this script will take a language lower and upper name
# setUpJointDirectory.sh aren ArEn
# makes a directory and copies the needed files into that directory for joint generation
# call this script from a Folds directory

LOWER=$1
UPPER=$2
dirName=$3

mkdir $dirName
#cp  $LOWER.9.tst ../$LOWER.dev ${LOWER}9.phraseOut ${LOWER}Dev.phraseOut  $LOWER.9.tst.seq.out  $LOWER.dev.seq.out $UPPER.9.tst.smt.out $UPPER.dev.smt.out JointDTLSeqSMT

# note: I changed this later to handle spaces and underscores and made the new directory 2. Many of the languages aren't affected

sed -e 's/_/#/g' -e 's/   / % /g' $LOWER.9.tst > $dirName/$LOWER.9.tst
sed -e 's/_/#/g' -e 's/   / % /g' ../$LOWER.dev >  $dirName/$LOWER.dev 
sed -e 's/_/#/g' -e 's/ /%/g' ${LOWER}9.phraseOut > $dirName/${LOWER}9.phraseOut 
sed -e 's/_/#/g' -e 's/ /%/g' ${LOWER}Dev.phraseOut > $dirName/${LOWER}Dev.phraseOut  
sed -e 's/_/#/g' -e 's/ /%/g' $LOWER.9.tst.seq.out > $dirName/$LOWER.9.tst.seq.out  
sed -e 's/_/#/g' -e 's/ /%/g' $LOWER.dev.seq.out > $dirName/$LOWER.dev.seq.out 
sed -e 's/_/#/g' -e 's/ /%/g' $UPPER.9.tst.smt.out > $dirName/$UPPER.9.tst.smt.out 
sed -e 's/_/#/g' -e 's/ /%/g' $UPPER.dev.smt.out > $dirName/$UPPER.dev.smt.out 