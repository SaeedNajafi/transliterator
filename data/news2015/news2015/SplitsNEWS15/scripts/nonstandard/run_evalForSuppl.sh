# this script is run fromthe normal directory after the normal dtl has been ran. Evaluates and gives results for the normal dtl
# system on just the subset of dev which has suppl data

lower=$1


sed 's/ //g' $lower.output > tmp
sed -e 's/#/_/g' -e 's/%/ /g' tmp > $lower.output.final

getTestThatHaveSuppl.py ../$lower.tst ../$lower.tst.ext.matched > tmp2
sed 's/ //g' tmp2 > tmp3
sed -e 's/#/_/g' -e 's/%/ /g' tmp3 > $lower.tst.final
convertToXML.py $lower.tst.final > tst.xml
rm tmp*

echo accuracy on words that have supplemental
evalDirecTL.sh $lower.output.final tst.xml