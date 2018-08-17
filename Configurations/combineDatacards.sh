#!/bin/bash

cat MassPointList${1}.txt | while read line
do
   if [[ -n $line && "$line" != *"#"* ]]
   then
      ./combinePointDatacards.sh Datacards$2/MassPoint$line
   fi
done
