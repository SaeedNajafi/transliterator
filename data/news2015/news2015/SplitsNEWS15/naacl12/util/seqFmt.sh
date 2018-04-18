#!/usr/bin/env bash

cut -f 1 $1 | sed -e 's/ //g' | paste - <(cut -f 2 $1) > $(basename $1).seqfmt
