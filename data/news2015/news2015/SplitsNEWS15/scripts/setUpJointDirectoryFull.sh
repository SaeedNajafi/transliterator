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

sed -e 's/_/#/g' -e 's/   / % /g' ../$LOWER.full.trn > $dirName/$LOWER.full.trn
sed -e 's/_/#/g' -e 's/   / % /g' ../$LOWER.dev >  $dirName/$LOWER.dev 
sed -e 's/_/#/g' -e 's/ /%/g' ${LOWER}All.phraseOut > $dirName/${LOWER}All.phraseOut 
sed -e 's/_/#/g' -e 's/ /%/g' ${LOWER}Dev.phraseOut > $dirName/${LOWER}Dev.phraseOut  
sed -e 's/_/#/g' -e 's/ /%/g' $LOWER.all.seq.out > $dirName/$LOWER.all.seq.out  
sed -e 's/_/#/g' -e 's/ /%/g' $LOWER.dev.seq.out > $dirName/$LOWER.dev.seq.out 
sed -e 's/_/#/g' -e 's/ /%/g' $UPPER.all.smt.out > $dirName/$UPPER.all.smt.out 
sed -e 's/_/#/g' -e 's/ /%/g' $UPPER.dev.smt.out > $dirName/$UPPER.dev.smt.out 