lower=$1
outName=$2

#122align.sh $lower

~/m2m-aligner-1.2/m2m-aligner -i $lower.trn  --delX  
mv $lower.*.align $lower.align


#train_direct.sh $lower
~/DirecTL-p/directlp -f $lower.align  --inChar : --order 1 --linearChain  --jointMgram 5 --mo /local/chauvin1/ajstarna/$lower/$lower.${outName}Model