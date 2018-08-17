#!/bin/bash

cat MassPointList${1}.txt | while read line
do
   if [[ -n $line && "$line" != *"#"* ]]
   then
       ./runPointLimit.sh $line $2
   fi
done
