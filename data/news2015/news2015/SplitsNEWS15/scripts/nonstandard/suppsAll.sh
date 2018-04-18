#!/usr/bin/env bash  

cd ~/NEWS15/

declare -A language
language=([EnBa]=enba [EnCh]=ench [EnHe]=enhe [EnHi]=enhi [EnJa]=enja [EnKa]=enka [EnKo]=enko [EnPe]=enpe [EnTa]=enta [EnTh]=enth )

for key in ${!language[@]}
do
    cd ${key}/nonstandard
    determineSupplTrnDev.py  ${language[${key}]}
    cd ../nonstandardTEST
    determineSuppl.py  ${language[${key}]}
    echo ============================================
    cd ../..
done