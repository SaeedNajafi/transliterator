# this script runs all the necessary scripts to do system combination of dtl and sequitur
# should be ran from a directory within the Folds directory of a language
# expects to find an m2m model two directories up

language=$1 # enko
languagefront=$2 #en
languageend=$3 # ko

script1.sh ${language} ${languagefront} ${languageend}
script2.sh ${languagefront} ${languageend}
script3.sh ${language}
script4B.sh ${language}
script5.sh ${language}