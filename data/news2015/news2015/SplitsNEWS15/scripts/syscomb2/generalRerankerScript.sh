# this script runs all the necessary scripts to do system combination of dtl and sequitur
# should be ran from a directory within the Folds directory of a language
# expects to find an m2m model two directories up


# the inputs are the paths from the current directory to the corresponding sets                                                                                                   
# the actual sets we working with                                                                                                                                                 
trainset=$1
testset=$2

# the outputs on those sets from the original system                                                                                                                              
trainoriginal=$3
testoriginal=$4
#originalcoords=$5 # the coordinates of the answers from these files (examples for dtl = 1,2 and seq = 1,4)                                                                        

# the outputs on those sets from the system we will use to rerank the origial with                                                                                                
trainextra=$5
testextra=$6
extracoords=$7

# the language pair we are working with (for example enhe)                                                                                                                        
language=$8 # e.g. enko

languagefront=$9 #en
languageend=${10} # ko
needalign=${11} # "yes" or "no" (yes if sequitur or smt i think, no if original system is dtl)
features=${12} # "scores" or "all" (which features to use for featurizer)



echo STARTTING SCRIPT 1
rerankScript1.sh ${trainset} ${testset} ${trainoriginal} ${testoriginal} ${trainextra} ${testextra} ${extracoords} ${language} ${languagefront} ${languageend}



echo STARTTING SCRIPT 2
rerankScript2.sh ${language} ${languagefront} ${languageend}

if [ $needalign == "yes" ]; then 
    echo STARTTING SCRIPT 3
    rerankScript3.sh ${language} 
fi



echo STARTTING SCRIPT 4
rerankScript4.sh ${language} ${features}

echo STARTTING SCRIPT 5
rerankScript5.sh ${language}
