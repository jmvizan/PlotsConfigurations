#!/bin/bash

echo "Performing MaxLikelihoodFit for " $1
#
cd /afs/cern.ch/work/s/scodella/Stop/CodeDevelopment/CMSSW_7_4_7/src/
#cd /afs/cern.ch/work/s/scodella/Stop/CMSSW_7_4_7/src/
eval `scramv1 runtime -sh`
cd -
#
cd $1/
#
if [[ -z $2 || "$2" = *"asimov"* ]]
then
    echo "     fit to asimov datasets"
    combine -M MaxLikelihoodFit -t -1 --expectSignal 0 --robustFit 1 --saveShapes --saveWithUncertainties -n "_asimov" -d datacardFinal.txt
    mv mlfit.root mlfit_asimov.root
    rm  *.mH120.root
    $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py mlfit_asimov.root -A -a -f latex --histogram pulls_asimov.root > pulls_asimov.tex
fi
#
if [[ -z $2 || "$2" = *"data"* ]]
then
    echo "     fit to data"
    combine -M MaxLikelihoodFit --robustFit 1 --saveOverallShapes --saveWithUncertainties -n "_data_checkJR" -d datacardFinal.txt
    #combine -M MaxLikelihoodFit --cminM2StorageLevel 1 datacardFinal.txt 
    #mv mlfit.root mlfit_data_nomt2ll.root
    rm  *.mH120.root
    #$CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py mlfit_data.root -A -a -f latex --histogram pulls_data.root > pulls_data_all.tex
    #$CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py mlfit_data.root -f latex --histogram pulls_data.root > pulls_data.tex
    #combine -M Asymptotic  -d datacardFinal.txt
    #mv higgsCombineTest.Asymptotic.mH120.root datacardFinal.root
fi
#
cd -

