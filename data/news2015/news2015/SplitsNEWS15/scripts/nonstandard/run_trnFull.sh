# this script is the final version used for training the final models. Different from others that it requires jointMgram size as input

lower=$1
jointMsize=$2

#122align.sh $lower

~/m2m-aligner-1.2/m2m-aligner -i $lower.trn   --maxX 1  --delX  
mv $lower.*.align $lower.align


#train_direct.sh $lower
~/DirecTL-p-3j-speedup-general/directlp -f $lower.align  --inChar : --extFeaTrain $lower.trn.ext --order 1 --linearChain  --jointMgram $jointMsize --mo /local/chauvin1/ajstarna/$lower/$lower.FinalModel