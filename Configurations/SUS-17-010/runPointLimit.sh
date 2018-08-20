#!/bin/bash

echo "Computing limit for " $1
#
cd Datacards$2/MassPoint$1/
#
#combine -M Asymptotic  --run blind -n $1 -d datacardFinal.txt
#mv higgsCombine$1.Asymptotic.mH120.root datacardFinalBlind.root
#
#combine -M Asymptotic  --run expected -n $1 -d datacardFinal.txt
#mv higgsCombine$1.Asymptotic.mH120.root datacardFinalExpected.root
#
combine -M Asymptotic  -n $1 -d datacardFinal.txt
mv higgsCombine$1.Asymptotic.mH120.root datacardFinal.root
#
cd -

