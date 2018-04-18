# this script will take a language name as input, prints the trnPlusDev file with just sources and no spaces.
# useful for then calculating overlap with test files and for caluculating avergae size of sources

input=$1 # e.g enhe

sed 's/   / % /g' $input.dev | cut -f 1 > tmp
sed 's/ //g' tmp > $input.dev.sourcesNoSpaces
rm tmp

wc -l -m $input.dev.sourcesNoSpaces