#!/bin/bash

M2M=~/m2m-aligner-1.2/m2m-aligner


# Required files
################
TRNFILE=$1
SEQFILE=$2

$M2M --delX --maxX 1 -i $TRNFILE --maxY 2
# the joint generating direcTL requires maxX == 1

$M2M --delX --maxX 1 -i $SEQFILE --maxY 2