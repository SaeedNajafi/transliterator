# gives the wc of trn, tst, and ext files

lower=$1

wc -l $lower.trn
wc -l $lower.trn.ext
wc -l $lower.tst
wc -l $lower.tst.ext
wc -l $lower.tst.words.matched

wc -l ${lower}11.tst
wc -l ${lower}11.tst.ext

wc -l ${lower}12.tst
wc -l ${lower}12.tst.ext
