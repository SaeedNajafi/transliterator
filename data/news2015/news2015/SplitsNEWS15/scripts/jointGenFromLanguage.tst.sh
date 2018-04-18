# this script only requires the input language as lower and upper letters (and the number of the model to be used) and will call jointGenAllSystems.tst.sh with all of its required inputs
# this script is just easier to call than the other

LOWER=$1
UPPER=$2
MODELNUM=$3
TAGS=$4 # yes or no. must match what we trained with

jointGenAllSystems.tst.sh ${LOWER}.dev ${LOWER}Dev.phraseOut ${LOWER}.dev.seq.out ${UPPER}.dev.smt.out ${LOWER} ${LOWER}.9.tst.m-mAlign.1-2.delX.1-best.conYX.align.10nBest.1order.linearChain.${MODELNUM} $TAGS
sed 's/ //g' ${LOWER}.output > tmp
sed -e 's/#/_/g' -e 's/%/ /g' tmp >  ${LOWER}.output.final # convert back to spaces and underscoress
evalDirecTL.sh ${LOWER}.output.final ../../dev.xml