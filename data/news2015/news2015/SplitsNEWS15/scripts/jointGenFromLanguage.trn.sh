# this script only requires the input language as lower and upper letters and will call jointGenAllSystems.sh with all of its required inputs
# this script is just easier to call than the other

LOWER=$1
UPPER=$2
TAGS=$3 # yes or no

echo jointGenAllSystems.trn.sh $LOWER.9.tst ${LOWER}9.phraseOut $LOWER.9.tst.seq.out $UPPER.9.tst.smt.out $LOWER $TAGS
jointGenAllSystems.trn.sh $LOWER.9.tst ${LOWER}9.phraseOut $LOWER.9.tst.seq.out $UPPER.9.tst.smt.out $LOWER $TAGS