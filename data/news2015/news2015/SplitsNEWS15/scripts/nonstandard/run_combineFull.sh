# this script is used once the normal system and the joint system are done.
# run from the normal directory
# the normal DTL outputs are expected to be in the normal directory where this is called from. Up one level is the nonstandardTEST directory
# with the joint output. 
# this script will combine the outputs for the 11 and 12 tests sets, when possible using the joint system and then normal to fill in the gaps

lower=$1


#cut -f 1,2 ${lower}11.answers.phraseOut | sed 's/ //g'  > tmp
#sed -e 's/#/_/g' -e 's/%/ /g' tmp > ${lower}11.output.final
cut -f 1,2 ${lower}11.answers.phraseOut  > ${lower}11.output.final
getOutputFromJoint.py ${lower}11.output.final ../${lower}11.output.final >  ${lower}11.outputWithJoint.final

#cut -f 1,2 ${lower}12.answers.phraseOut | sed 's/ //g'  > tmp
#sed -e 's/#/_/g' -e 's/%/ /g' tmp > ${lower}12.output.final
cut -f 1,2 ${lower}12.answers.phraseOut  > ${lower}12.output.final
getOutputFromJoint.py ${lower}12.output.final ../${lower}12.output.final >  ${lower}12.outputWithJoint.final


#rm tmp*

