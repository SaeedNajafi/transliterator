#!/usr/bin/env bash  

cd ~/NEWS15/

declare -A language
language=([ArEn]=aren [ChEn]=chen [EnBa]=enba [EnCh]=ench [EnHe]=enhe [EnHi]=enhi [EnJa]=enja [EnKa]=enka [EnKo]=enko [EnPe]=enpe [EnTa]=enta [EnTh]=enth [JnJk]=jnjk [ThEn]=then )

for key in ${!language[@]}
do
    cd ${key}/Folds
    setUpJointDirectory.sh ${language[${key}]} ${key}
    cd ../..
#    echo ${key} ${language[${key}]}   
done