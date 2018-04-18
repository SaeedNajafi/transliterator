# final script for the test submission. tests on 2011 and 2012 test sets
# usage: run_tstFull.sh enba enba.align.sdfsdfsf.14 6
# note: jointMsize must match that used for training this language


lower=$1
PATH_TO_MODEL=$2 #../trn/enhi.align.10nBest.1order.linearChain.4 #"SPECIFY_YOUR_PATH_TO_MODEL_HERE"

jointMsize=$3

#if [ 0 -eq 1 ]; then

#cut -f 1 ${lower}11.tst | sed 's/ /|/g' | sed 's/$/|/' | uniq > ${lower}11.tst.words
#cut -f 1 ${lower}12.tst | sed 's/ /|/g' | sed 's/$/|/' | uniq > ${lower}12.tst.words


sort ${lower}11.tst.ext  > ${lower}11.tst.ext.matched
cut -f 1 ${lower}11.tst.ext.matched > ${lower}11.tst.words.matched


sort ${lower}12.tst.ext  > ${lower}12.tst.ext.matched
cut -f 1 ${lower}12.tst.ext.matched > ${lower}12.tst.words.matched

#matchSuppWithSource.py ${lower}11.tst.words ${lower}11.tst.ext | sort  > ${lower}11.tst.ext.matched
#getWordsThatHaveSuppl.py ${lower}11.tst.words ${lower}11.tst.ext.matched  > ${lower}11.tst.words.matched.nosort

#matchSuppWithSource.py ${lower}12.tst.words ${lower}12.tst.ext | sort > ${lower}12.tst.ext.matched
#getWordsThatHaveSuppl.py ${lower}12.tst.words ${lower}12.tst.ext.matched  > ${lower}12.tst.words.matched.nosort


~/DirecTL-p-3j-speedup-general/directlp --mi $PATH_TO_MODEL  -t ${lower}11.tst.words.matched --outChar ' ' -a ${lower}11.output --inChar : --extFeaTest ${lower}11.tst.ext.matched --nBestTest 10 --order 1 --linearChain --jointMgram $jointMsize

~/DirecTL-p-3j-speedup-general/directlp --mi $PATH_TO_MODEL  -t ${lower}12.tst.words.matched --outChar ' ' -a ${lower}12.output --inChar : --extFeaTest ${lower}12.tst.ext.matched --nBestTest 10 --order 1 --linearChain --jointMgram $jointMsize





#fi




sed 's/ //g' ${lower}11.output > tmp
sed -e 's/#/_/g' -e 's/%/ /g' tmp > ${lower}11.output.final

sed 's/ //g' ${lower}12.output > tmp
sed -e 's/#/_/g' -e 's/%/ /g' tmp > ${lower}12.output.final


rm tmp*



