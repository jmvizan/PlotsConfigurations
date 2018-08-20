#!/bin/bash

export WORKDIRECTORY=$PWD

cat MassPointList${1}.txt | while read line
do
   if [[ -n $line && "$line" != *"#"* ]]
   then
       qsub ./runPointLimitGrbatch.sh $line $WORKDIRECTORY $2
   fi
done
