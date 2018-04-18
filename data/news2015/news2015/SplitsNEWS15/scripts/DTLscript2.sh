#!/bin/bash

M2M=~/m2m-aligner-1.2/m2m-aligner
DTL=~/DirecTL-p/directlp

# Required files
################
TRNFILE=$1
#DEVFILE=enhi.dev
TSTFILE=$2

# Development phase
###################
# First we need to align our data
$M2M --delX -i $TRNFILE
# --delX allows deletions on X side; --delY is a possibility too that can be
# tried, but do *not* enable both! Otherwise it may make an alignment by simply
# deleting both sides entirely.
# --maxX M and --maxY N tell it to use a M-N alignment. Default is 2-2.
# The default format (--inFormat news) is not as convenient for L2P; for that,
# you should use --informat l2p. NEWS format has the X and Y separated by tabs,
# with each character within X and Y separated by spaces. e.g.:
# t e s t<TAB>t e s t

#$M2M --delX --alignerIn $TRNFILE.*.model -i $DEVFILE
# Note that the above command uses *-globbing. This may be bad if there are
# multiple matches, so in that case you will need to fill in the model name
# manually. Warning applies in subsequent commands as well.

# Get some test-format data from the development set so we can examine the
# output
#cut -f 1 $DEVFILE.*.align | sed -e 's/:/|/g' | uniq > $DEVFILE.words

# Now we can run DirecTL+ using the development set to tell us how many
# iterations to use. I personally question this as the best way to determine the
# number of iterations but neither Tee nor I ever experimented with anything
# else (despite having an idea or two), so we stick with it.
#$DTL --inChar : --tal 5 --order 1 --linearChain --jointMgram 6 -f \
#    $TRNFILE.*.align -d $DEVFILE.*.align -t $DEVFILE.words -a $DEVFILE.output \
#    --nBestTest 10

# Testing phase
###############

# Merge training and development for more data

# Repeat above process using combined train/dev as well as actual testing data

$M2M --delX --alignerIn $TRNFILE.*.model -i $TSTFILE
cut -f 1 $TSTFILE.*.align | sed -e 's/:/|/g' | uniq > $TSTFILE.words

# Here you use your maximum iteration number from the development phase (--tam
# parameter):
$DTL --inChar : --tal 5 --order 1 --linearChain --jointMgram 6 -f $TRNFILE.*.align -t $TSTFILE.words -a $TSTFILE.output --nBestTest 10
