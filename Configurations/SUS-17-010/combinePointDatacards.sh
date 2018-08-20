#!/bin/bash

echo "Combining datacards for" $1
#
cd $1/
#
###if [[ "$1" = *"MassPoint2XXX"* ]]
if [[ "$1" = *"MassPoint2"* ]]
then
    # SR1
    combineCards.py em=./SR1_Tag_em/MT2ll/datacard.txt      sf=./SR1_Tag_sf/MT2ll/datacard.txt      > datacardSR1T.txt
    combineCards.py em=./SR1_Veto_em/MT2ll/datacard.txt     sf=./SR1_Veto_sf/MT2ll/datacard.txt     > datacardSR1V.txt
    # SR2
    combineCards.py em=./SR2_Tag_em/MT2ll/datacard.txt      sf=./SR2_Tag_sf/MT2ll/datacard.txt      > datacardSR2T.txt
    combineCards.py em=./SR2_Veto_em/MT2ll/datacard.txt     sf=./SR2_Veto_sf/MT2ll/datacard.txt     > datacardSR2V.txt
    # SR3
    #combineCards.py em=./SR3_Tag_em/MT2ll/datacard.txt      sf=./SR3_Tag_sf/MT2ll/datacard.txt      > datacardSR3T.txt
    #combineCards.py em=./SR3_Veto_em/MT2ll/datacard.txt     sf=./SR3_Veto_sf/MT2ll/datacard.txt     > datacardSR3V.txt
    # SR3 ISR
    combineCards.py em=./SR3_Tag_em/MT2llisr/datacard.txt   sf=./SR3_Tag_sf/MT2llisr/datacard.txt   > datacardSR3T.txt
    combineCards.py em=./SR3_Veto_em/MT2llisr/datacard.txt  sf=./SR3_Veto_sf/MT2llisr/datacard.txt  > datacardSR3V.txt
    #
    combineCards.py SR1=datacardSR1T.txt SR2=datacardSR2T.txt SR3=datacardSR3T.txt > datacardTag.txt 
    combineCards.py SR1=datacardSR1V.txt SR2=datacardSR2V.txt SR3=datacardSR3V.txt > datacardVeto.txt 
    #combineCards.py SR2=datacardSR2T.txt SR3=datacardSR3T.txt > datacardTag.txt 
    #combineCards.py SR2=datacardSR2V.txt SR3=datacardSR3V.txt > datacardVeto.txt 
    #
    combineCards.py Tag=datacardTag.txt Veto=datacardVeto.txt > datacardFinal.txt 
fi
#
###if [[ "$1" = *"MassPoint"* ]]
if [[ "$1" = *"MassPointChi"* ]]
then
    # SR1
    combineCards.py em=./SR1_Tag_em/MT2ll/datacard.txt      sf=./SR1_Tag_sf/MT2ll/datacard.txt      > datacardSR1T.txt
    combineCards.py em=./SR1_NoTag_em/MT2ll/datacard.txt    sf=./SR1_NoTag_sf/MT2ll/datacard.txt    > datacardSR1J.txt
    combineCards.py em=./SR1_NoJet_em/MT2ll/datacard.txt    sf=./SR1_NoJet_sf/MT2ll/datacard.txt    > datacardSR10.txt
    #combineCards.py em=./SR1_Veto_em/MT2ll/datacard.txt     sf=./SR1_Veto_sf/MT2ll/datacard.txt     > datacardSR1V.txt
    # SR2
    combineCards.py em=./SR2_Tag_em/MT2ll/datacard.txt      sf=./SR2_Tag_sf/MT2ll/datacard.txt      > datacardSR2T.txt
    combineCards.py em=./SR2_NoTag_em/MT2ll/datacard.txt    sf=./SR2_NoTag_sf/MT2ll/datacard.txt    > datacardSR2J.txt
    combineCards.py em=./SR2_NoJet_em/MT2ll/datacard.txt    sf=./SR2_NoJet_sf/MT2ll/datacard.txt    > datacardSR20.txt
    #combineCards.py em=./SR2_Veto_em/MT2ll/datacard.txt     sf=./SR2_Veto_sf/MT2ll/datacard.txt     > datacardSR2V.txt
    # SR3
    combineCards.py em=./SR3_Tag_em/MT2ll/datacard.txt      sf=./SR3_Tag_sf/MT2ll/datacard.txt      > datacardSR3T.txt
    combineCards.py em=./SR3_Veto_em/MT2ll/datacard.txt     sf=./SR3_Veto_sf/MT2ll/datacard.txt     > datacardSR3V.txt
    #combineCards.py em=./SR3_NoTag_em/MT2ll/datacard.txt    sf=./SR3_NoTag_sf/MT2ll/datacard.txt    > datacardSR3J.txt
    #combineCards.py em=./SR3_NoJet_em/MT2ll/datacard.txt    sf=./SR3_NoJet_sf/MT2ll/datacard.txt    > datacardSR30.txt
    #
    #combineCards.py SR1=datacardSR1T.txt SR2=datacardSR2T.txt SR3=datacardSR3T.txt > datacardTag.txt 
    #combineCards.py SR1=datacardSR1J.txt SR2=datacardSR2J.txt SR3=datacardSR3V.txt > datacardNoTag.txt 
    #combineCards.py SR1=datacardSR10.txt SR2=datacardSR20.txt > datacardNoJet.txt
    #
    combineCards.py Tag=datacardSR1T.txt NoTag=datacardSR1J.txt NoJet=datacardSR10.txt > datacardSR1.txt 
    #combineCards.py Tag=./SR1_Tag_em/MT2ll/datacard.txt NoTag=./SR1_NoTag_em/MT2ll/datacard.txt NoJet=./SR1_NoJet_em/MT2ll/datacard.txt > datacardFinal.txt
    combineCards.py Tag=datacardSR2T.txt NoTag=datacardSR2J.txt NoJet=datacardSR20.txt > datacardSR2.txt 
    #combineCards.py Tag=datacardSR3T.txt NoTag=datacardSR3J.txt NoJet=datacardSR30.txt > datacardSR3.txt
    #combineCards.py Tag=datacardSR1T.txt Veto=datacardSR1V.txt                         > datacardSR1.txt 
    #combineCards.py Tag=datacardSR2T.txt Veto=datacardSR2V.txt                         > datacardSR2.txt 
    combineCards.py Tag=datacardSR3T.txt Veto=datacardSR3V.txt                         > datacardSR3.txt  
    #
    #combineCards.py Tag=datacardTag.txt NoTag=datacardNoTag.txt NoJet=datacardNoJet.txt > datacardFinal.txt 
    combineCards.py SR1=datacardSR1.txt SR2=datacardSR2.txt SR3=datacardSR3.txt > datacardFinal.txt 
    #combineCards.py SR1=datacardSR1.txt SR2=datacardSR2.txt > datacardFinal.txt
    #combineCards.py SR3=datacardSR2.txt > datacardFinal.txt
    # em
    #combineCards.py Tag=./SR1_Tag_em/MT2ll/datacard.txt NoTag=./SR1_NoTag_em/MT2ll/datacard.txt NoJet=./SR1_NoJet_em/MT2ll/datacard.txt > datacardFinal.txt #PPdatacardSR1em.txt
    #combineCards.py Tag=./SR2_Tag_em/MT2ll/datacard.txt NoTag=./SR2_NoTag_em/MT2ll/datacard.txt NoJet=./SR2_NoJet_em/MT2ll/datacard.txt > datacardFinal.txt #PPdatacardSR2em.txt
    #combineCards.py Tag=./SR3_Tag_em/MT2ll/datacard.txt Veto=./SR3_Veto_em/MT2ll/datacard.txt > datacardSR3em.txt
    # sf
    #combineCards.py Tag=./SR1_Tag_sf/MT2ll/datacard.txt NoTag=./SR1_NoTag_sf/MT2ll/datacard.txt NoJet=./SR1_NoJet_sf/MT2ll/datacard.txt > datacardFinal.txt #PPdatacardSR1sf.txt
    #combineCards.py Tag=./SR2_Tag_sf/MT2ll/datacard.txt NoTag=./SR2_NoTag_sf/MT2ll/datacard.txt NoJet=./SR2_NoJet_sf/MT2ll/datacard.txt > datacardFinal.txt #PPdatacardSR2sf.txt
    #combineCards.py Tag=./SR3_Tag_sf/MT2ll/datacard.txt Veto=./SR3_Veto_sf/MT2ll/datacard.txt > datacardSR3sf.txt
    # 
    #combineCards.py SR1=datacardSR1em.txt SR2=datacardSR2em.txt SR3=datacardSR3em.txt > datacardEM.txt
    #combineCards.py SR1=datacardSR1em.txt > datacardFinal.txt 
    #combineCards.py SR1=datacardSR1sf.txt SR2=datacardSR2sf.txt SR3=datacardSR3sf.txt > datacardSF.txt
    #
    #combineCards.py em=datacardEM.txt sf=datacardSF.txt > datacardFinal.txt 
    #
    # ll
    #combineCards.py Tag=./SR1_Tag_ll/MT2ll/datacard.txt NoTag=./SR1_NoTag_ll/MT2ll/datacard.txt NoJet=./SR1_NoJet_ll/MT2ll/datacard.txt > datacardSR1ll.txt
    #combineCards.py Tag=./SR2_Tag_ll/MT2ll/datacard.txt NoTag=./SR2_NoTag_ll/MT2ll/datacard.txt NoJet=./SR2_NoJet_ll/MT2ll/datacard.txt > datacardSR2ll.txt
    #combineCards.py Tag=./SR3_Tag_ll/MT2ll/datacard.txt Veto=./SR3_Veto_ll/MT2ll/datacard.txt > datacardSR3ll.txt
    #combineCards.py SR1=datacardSR1ll.txt SR2=datacardSR2ll.txt SR3=datacardSR3ll.txt > datacardFinal.txt
    #
fi
