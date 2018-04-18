# this script makes a Folds directory, calls foldify.py to set up the 10 folds, and concatenates folds 0-7 into a file
# fold 8 is used by each system for its own development. fold 9 is used to train the reranker/combo. fold 7 is for each system's training

LANGUAGE=$1

mkdir Folds
cd Folds
~/naacl12/util/foldify.py $LANGUAGE < ../$LANGUAGE.full.trn
cat $LANGUAGE.{0,1,2,3,4,5,6,7}.tst | sort > $LANGUAGE.0-7.tst