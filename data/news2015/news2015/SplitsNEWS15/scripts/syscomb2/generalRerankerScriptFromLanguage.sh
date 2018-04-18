# this script will clal the general reranker script.
# requires as input the language as lower, front, end, and UPPER
# as well as the system for original and the system to use for reranking


# generalRerankerScriptFromLanguage.sh enhe en he EnHe dtl smt holdout scores

language=$1 # e.g. enko
languagefront=$2 #en 
languageend=$3 # ko
UPPER=$4 # EnKo 

orig=$5 # either dtl, seq, or smt, (OR directory where previous outputs are)
extra=$6 # either dtl, seq, or smt

train=$7 # either "holdout" or "full" (holdout corresponds to 9.tst)
features=$8 # either "scores" or "all"
needalign="no" # seems to be working fine with no alignments... hmmm

if [ $train == "holdout" ]; then
    trainset=../${language}.9.tst
    testset=../../${language}.dev
else
    trainset=../../${language}.full.trn
    testset=../../${language}.dev
fi



## now figure out which system and train set is used for original

if [ $orig == "dtl" ]; then
    
    testoriginal=../${language}Dev.phraseOut

    if [ $train == "holdout" ]; then
	trainoriginal=../${language}9.phraseOut
    else
	trainoriginal=../${language}All.phraseOut
    fi

else

    if [ $orig == "seq" ]; then

	testoriginal=../${language}.dev.seq.out

	if [ $train == "holdout" ]; then
	    trainoriginal=../${language}.9.tst.seq.out
	else
	    trainoriginal=../${language}.all.seq.out
	fi


    else 
        if [ $orig == "smt" ]; then
	    testoriginal=../${UPPER}.dev.smt.out
	    if [ $train == "holdout" ]; then
		trainoriginal=../${UPPER}.9.tst.smt.out
	    else
		trainoriginal=../${UPPER}.all.smt.out
	    fi

	else # orig is already a reranked system and is the name of a directory 
	    # make the directory called like DTLrerankedSeq and inside have the files named as below
	    testoriginal=../${orig}/${language}.dev.reranked.out
	    if [ $train == "holdout" ]; then
		trainoriginal=../${orig}/${language}.9.tst.reranked.out
	    else
		trainoriginal=../${orig}/${language}.all.reranked.out
	    fi


	fi
    fi
fi



## now figure out which system and train set is used for extra


if [ $extra == "dtl" ]; then
    
    testextra=../${language}Dev.phraseOut
    extracoords=1,2
    if [ $train == "holdout" ]; then
	trainextra=../${language}9.phraseOut
    else
	trainextra=../${language}All.phraseOut
    fi

else

    if [ $extra == "seq" ]; then

	testextra=../${language}.dev.seq.out
	extracoords=1,4
	if [ $train == "holdout" ]; then
	    trainextra=../${language}.9.tst.seq.out
	else
	    trainextra=../${language}.all.seq.out
	fi


    else # extra = smt
	testextra=../${UPPER}.dev.smt.out
	extracoords=2,3
	if [ $train == "holdout" ]; then
	    trainextra=../${UPPER}.9.tst.smt.out
	else
	    trainextra=../${UPPER}.all.smt.out
	fi

    fi
fi

echo generalRerankerScript.sh $trainset $testset $trainoriginal $testoriginal $trainextra $testextra $extracoords $language $languagefront $languageend $needalign $features
generalRerankerScript.sh $trainset $testset $trainoriginal $testoriginal $trainextra $testextra $extracoords $language $languagefront $languageend $needalign $features