#!/bin/bash

echo "Producing impacts plot for " $1
#
cd /afs/cern.ch/work/s/scodella/Stop/CodeDevelopment/CMSSW_7_4_7/src/
eval `scramv1 runtime -sh`
cd -
#
cd $1/
#
text2workspace.py datacardFinal.txt  -m 125
$CMSSW_BASE/src/CombineHarvester/CombineTools/scripts/combineTool.py -M Impacts -d datacardFinal.root -m 125 --doInitialFit --robustFit 1
$CMSSW_BASE/src/CombineHarvester/CombineTools/scripts/combineTool.py -M Impacts -d datacardFinal.root -m 125 --robustFit 1 --doFits --parallel 10
$CMSSW_BASE/src/CombineHarvester/CombineTools/scripts/combineTool.py -M Impacts -d datacardFinal.root -m 125 -o impacts.json
$CMSSW_BASE/src/CombineHarvester/CombineTools/scripts/plotImpacts.py -i impacts.json -o impacts
#
cd -

