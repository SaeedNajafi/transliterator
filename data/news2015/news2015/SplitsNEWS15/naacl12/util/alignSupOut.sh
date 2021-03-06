#!/usr/bin/env bash

file=$1
shift
out=$1
shift
i=4
let j=$i+$#
for sup in $@
do
    cut -f $i,$j $file > $file.$sup$out
    ~/m2m-aligner-1.2/m2m-aligner --pScore --errorInFile --delX --sepInChar '' --alignerIn \
        $sup$out.*.model -i $file.$sup$out > /dev/null
    let i+=1
done

rm *.err # not useful
sed -i -e 's/NO ALIGNMENT \t/NALGN\tNALGN\tNULL\tNULL/' $file.*.align

for sup in $@
do
    paste $file.$sup$out $file.$sup$out.*.align | sed -e \
        '/^NULL\t/s/NALGN/NULL/g' | cut -f 3,4,6 > $file.$sup$out.tmp
done

cut -f 1-3 $file | paste - $file.*.tmp
rm *.tmp
