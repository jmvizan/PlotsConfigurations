#!/bin/bash

echo "Combining datacards for" $1
#
cd $1/
#
combineCards.py em=./SR1_Tag_em/mt2ll/datacard.txt   sf=./SR1_Tag_sf/mt2ll/datacard.txt  > datacardSR1T.txt
combineCards.py em=./SR1_Veto_em/mt2ll/datacard.txt  sf=./SR1_Veto_sf/mt2ll/datacard.txt > datacardSR1V.txt
#
combineCards.py em=./SR2_Tag_em/mt2ll/datacard.txt   sf=./SR2_Tag_sf/mt2ll/datacard.txt  > datacardSR2T.txt
combineCards.py em=./SR2_Veto_em/mt2ll/datacard.txt  sf=./SR2_Veto_sf/mt2ll/datacard.txt > datacardSR2V.txt
#
combineCards.py em=./SR3_Tag_em/mt2ll/datacard.txt   sf=./SR3_Tag_sf/mt2ll/datacard.txt  > datacardSR3T.txt
combineCards.py em=./SR3_Veto_em/mt2ll/datacard.txt  sf=./SR3_Veto_sf/mt2ll/datacard.txt > datacardSR3V.txt
#
combineCards.py Tag=datacardSR1T.txt Veto=datacardSR1V.txt > datacardSR1.txt 
combineCards.py Tag=datacardSR2T.txt Veto=datacardSR2V.txt > datacardSR2.txt 
combineCards.py Tag=datacardSR3T.txt Veto=datacardSR3V.txt > datacardSR3.txt 
#
combineCards.py SR1=datacardSR1.txt SR2=datacardSR2.txt SR3=datacardSR3.txt > datacardFinal.txt
# 
cd -