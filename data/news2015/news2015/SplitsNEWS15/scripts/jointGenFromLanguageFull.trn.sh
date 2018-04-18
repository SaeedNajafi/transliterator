# this script only requires the input language as lower and upper letters and will call jointGenAllSystems.sh with all of its required inputs
# this script is just easier to call than the other

LOWER=$1
UPPER=$2
TAGS=$3

jointGenAllSystems.trn.sh $LOWER.full.trn ${LOWER}All.phraseOut $LOWER.all.seq.out $UPPER.all.smt.out $LOWER $TAGS