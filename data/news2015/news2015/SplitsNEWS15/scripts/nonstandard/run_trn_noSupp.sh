lower=$1

#122align.sh $lower

~/m2m-aligner-1.2/m2m-aligner -i $lower.trn   --maxX 1  --delX  
mv $lower.*.align $lower.align


touch dumby.trn.ext # empty ext file

#train_direct.sh $lower
~/DirecTL-p-3j-speedup-general/directlp -f $lower.align  --inChar : --extFeaTrain dumby.trn.ext --order 1 --linearChain  --jointMgram 5 #--tal 4 --tam 5