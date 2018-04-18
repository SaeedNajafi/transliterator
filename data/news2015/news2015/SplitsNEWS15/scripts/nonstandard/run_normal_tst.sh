
lower=$1
PATH_TO_MODEL=$2 #../trn/enhi.align.10nBest.1order.linearChain.4 #"SPECIFY_YOUR_PATH_TO_MODEL_HERE"

#if [ 0 -eq 1 ]; then

#~/m2m-aligner-1.2/m2m-aligner --delX --alignerIn $lower.trn.*.model -i $lower.tst
#cut -f 1 $lower.tst.*.align | sed -e 's/:/|/g' | uniq > $lower.tst.words

cut -f 1 $lower.tst | sed 's/ /|/g' | sed 's/$/|/' | uniq > $lower.tst.words


~/DirecTL-p/directlp --mi $PATH_TO_MODEL  -t $lower.tst.words --outChar ' ' -a $lower.output --inChar : --nBestTest 10 --order 1 --linearChain --jointMgram 5


#fi



 
sed 's/ //g' $lower.output > tmp
sed -e 's/#/_/g' -e 's/%/ /g' tmp > $lower.output.final

if [ 0 -eq 1 ]; then # cute block comments
getTestThatHaveSuppl.py ../$lower.tst ../$lower.tst.ext.matched > tmp2
sed 's/ //g' tmp2 > tmp3
sed -e 's/#/_/g' -e 's/%/ /g' tmp3 > $lower.tst.final
convertToXML.py $lower.tst.final > tst.xml
rm tmp*

echo accuracy on words that have supplemental
evalDirecTL.sh $lower.output.final tst.xml

fi