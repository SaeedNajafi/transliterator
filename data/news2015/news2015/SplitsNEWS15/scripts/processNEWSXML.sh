# this script is used to convert the XML NEWS data into txt files and split the full training set into a small and holdout set to train the reranker


DEVXML=$1
TRNXML=$2
BASENAME=$3

~/NEWS15/scripts/processNEWSXML.py $DEVXML > $BASENAME.dev
~/NEWS15/scripts/processNEWSXML.py $TRNXML > $BASENAME.full.trn
python3 ~/NEWS15/scripts/makeHoldOutSet.py $BASENAME < $BASENAME.full.trn