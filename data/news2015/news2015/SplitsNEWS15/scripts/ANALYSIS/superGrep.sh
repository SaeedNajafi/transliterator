echo train source
echo train target
echo dev source
echo dev target
echo
echo spaces
cut -f 1 *.full.trn | grep "   "  | wc -l
cut -f 2 *.full.trn | grep "   "  | wc -l
cut -f 1 *.dev | grep "   "  | wc -l
cut -f 2 *.dev | grep "   "  | wc -l
echo

echo underscore
cut -f 1 *.full.trn | grep " _ "  | wc -l
cut -f 2 *.full.trn | grep " _ "  | wc -l
cut -f 1 *.dev | grep " _ "  | wc -l
cut -f 2 *.dev | grep " _ "  | wc -l
#grep " _ " *.full.trn | wc -l
#grep " _ " *.dev | wc -l
echo

echo ampersand
cut -f 1 *.full.trn | grep " & "  | wc -l
cut -f 2 *.full.trn | grep " & "  | wc -l
cut -f 1 *.dev | grep " & "  | wc -l
cut -f 2 *.dev | grep " & "  | wc -l
#grep " & " *.full.trn | wc -l
#grep " & " *.dev | wc -l
echo

echo hash
cut -f 1 *.full.trn | grep " # "  | wc -l
cut -f 2 *.full.trn | grep " # "  | wc -l
cut -f 1 *.dev | grep " # "  | wc -l
cut -f 2 *.dev | grep " # "  | wc -l
#grep " # " *.full.trn | wc -l
#grep " # " *.dev | wc -l
echo

echo apost
cut -f 1 *.full.trn | grep " ' "  | wc -l
cut -f 2 *.full.trn | grep " ' "  | wc -l
cut -f 1 *.dev | grep " ' "  | wc -l
cut -f 2 *.dev | grep " ' "  | wc -l
#grep " ' " *.full.trn | wc -l
#grep " ' " *.dev | wc -l
echo

echo comma
cut -f 1 *.full.trn | grep " , "  | wc -l
cut -f 2 *.full.trn | grep " , "  | wc -l
cut -f 1 *.dev | grep " , "  | wc -l
cut -f 2 *.dev | grep " , "  | wc -l
#grep " , " *.full.trn | wc -l
#grep " , " *.dev | wc -l
echo

echo period
cut -f 1 *.full.trn | grep " \. "  | wc -l
cut -f 2 *.full.trn | grep " \. "  | wc -l
cut -f 1 *.dev | grep " \. "  | wc -l
cut -f 2 *.dev | grep " \. "  | wc -l
#grep " \. " *.full.trn | wc -l
#grep " \. " *.dev | wc -l
echo

echo ==================================
echo
echo test 11
echo test 12
echo

echo spaces
grep " " *11.tst | wc -l
grep " " *12.tst | wc -l
echo

echo underscore
grep "_" *11.tst | wc -l
grep "_" *12.tst | wc -l
echo

echo ampersand
grep "&" *11.tst | wc -l
grep "&" *12.tst | wc -l
echo

echo hash
grep "#" *11.tst | wc -l
grep "#" *12.tst | wc -l
echo

echo apost
grep "'" *11.tst | wc -l
grep "'" *12.tst | wc -l
echo

echo comma
grep "," *11.tst | wc -l
grep "," *12.tst | wc -l

echo
echo period
grep "\." *11.tst | wc -l
grep "\." *12.tst | wc -l
echo