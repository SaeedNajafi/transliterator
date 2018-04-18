lower=$1 # e.g. enhi

~/DirecTL-p-3j-speedup-general/directlp -f $lower.align  --inChar : --extFeaTrain $lower.trn.ext --order 1 --linearChain  --jointMgram 5 #--tal 4 --tam 5
