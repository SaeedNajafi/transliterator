# this script is used once the normal system and the joint system are done.
# run from the normal directory

lower=$1


sed 's/ //g' $lower.output > tmp
sed -e 's/#/_/g' -e 's/%/ /g' tmp > $lower.output.final

getOutputFromJoint.py $lower.output ../$lower.output > tmp2
sed 's/ //g' tmp2 > tmp3
sed -e 's/#/_/g' -e 's/%/ /g' tmp3 > $lower.outputWithJoint.final

rm tmp*

echo accuracy of base DTL
evalDirecTL.sh $lower.output.final ../../dev.xml

echo accuracy of base DTL With Joint Help
evalDirecTL.sh $lower.outputWithJoint.final ../../dev.xml
