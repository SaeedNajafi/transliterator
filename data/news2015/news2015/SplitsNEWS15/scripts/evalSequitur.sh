# this script will take an output sequitur file, then convert it as needed to get the relevant fields, convert to XML format, then run the news_eval code against the given testfile

# path to scripts
CONVERT=~/NEWS15/scripts/convertToXML.py
EVAL=~/NEWS15/eval/news_evaluation.py

INPUTFILE=$1
TESTFILE=$2

# get rid of spaces on outputs (not anymore)
cut -f 1,4 $INPUTFILE > tmp
python3 $CONVERT tmp > tmp.xml
python $EVAL -i tmp.xml -t $TESTFILE 
rm tmp*