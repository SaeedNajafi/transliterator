
lower=$1
PATH_TO_MODEL=$2 #../trn/enhi.align.10nBest.1order.linearChain.4 #"SPECIFY_YOUR_PATH_TO_MODEL_HERE"


#noSupp=$3


#cut -f 1 $lower.tst | sed 's/ /|/g' | sed 's/$/|/' | uniq > $lower.tst.words

#matchSuppWithSource.py $lower.tst.words $lower.tst.ext > $lower.tst.ext.matched
#getWordsThatHaveSuppl.py $lower.tst.words $lower.tst.ext.matched > $lower.tst.words.matched


sort $lower.tst.ext  > $lower.tst.ext.matched
cut -f 1 $lower.tst.ext.matched > $lower.tst.words.matched


#if [ $noSupp -eq 1 ]; then
#    echo noSupp test on all words with dummy
#    paste $lower.tst.words  $lower.tst.words >  $lower.tst.ext.matched
#    cp $lower.tst.words $lower.tst.words.matched
#    ~/DirecTL-p-3j-speedup-general/directlp --mi $PATH_TO_MODEL  -t $lower.tst.words.matched --outChar ' ' -a $lower.output --inChar : --nBestTest 10 --order 1 --linearChain --jointMgram 5


#else
~/DirecTL-p-3j-speedup-general/directlp --mi $PATH_TO_MODEL  -t $lower.tst.words.matched --outChar ' ' -a $lower.output --inChar : --extFeaTest $lower.tst.ext.matched --nBestTest 10 --order 1 --linearChain --jointMgram 5

#fi




sed 's/ //g' $lower.output > tmp
sed -e 's/#/_/g' -e 's/%/ /g' tmp > $lower.output.final

getTestThatHaveSuppl.py $lower.tst $lower.tst.ext.matched > tmp2
sed 's/ //g' tmp2 > tmp3
sed -e 's/#/_/g' -e 's/%/ /g' tmp3 > $lower.tst.final
convertToXML.py $lower.tst.final > tst.xml
rm tmp*

echo accuracy on words that have supplemental
evalDirecTL.sh $lower.output.final tst.xml



