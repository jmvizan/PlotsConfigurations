#!/bin/bash

echo "Combining datacards for" $1
#
cd $1/
#
if [[ "$1" = *"MassPoint2"* ]]
then
    # SR2
    combineCards.py em=./SR2_Tag_em/MT2ll/datacard.txt      sf=./SR2_Tag_sf/MT2ll/datacard.txt      > datacardSR2T.txt
    #combineCards.py em=./SR2_Veto_em/MT2ll/datacard.txt     sf=./SR2_Veto_sf/MT2ll/datacard.txt     > datacardSR2V.txt
    #
    combineCards.py em=./SR1_Tag_em/MT2ll/datacard.txt      sf=./SR1_Tag_sf/MT2ll/datacard.txt      > datacardSR1T.txt
    combineCards.py em=./SR3_Tag_em/MT2ll/datacard.txt      sf=./SR3_Tag_sf/MT2ll/datacard.txt      > datacardSR3T.txt
    #
    #combineCards.py Tag=datacardSR2T.txt Veto=datacardSR2V.txt > datacardFinal.txt
    #
    combineCards.py SR1=datacardSR1T.txt SR2=datacardSR2T.txt SR3=datacardSR3T.txt > datacardFinal.txt
    #
fi
#
if [[ "$1" = *"MassPointChi"* ]]
then
    # SR2
    combineCards.py em=./SR2_Tag_em/MT2ll/datacard.txt      sf=./SR2_Tag_sf/MT2ll/datacard.txt      > datacardSR2T.txt
    combineCards.py em=./SR2_NoTag_em/MT2ll/datacard.txt    sf=./SR2_NoTag_sf/MT2ll/datacard.txt    > datacardSR2J.txt
    combineCards.py em=./SR2_NoJet_em/MT2ll/datacard.txt    sf=./SR2_NoJet_sf/MT2ll/datacard.txt    > datacardSR20.txt
    #
    combineCards.py Tag=datacardSR2T.txt NoTag=datacardSR2J.txt NoJet=datacardSR20.txt > datacardFinal.txt
    #
fi
