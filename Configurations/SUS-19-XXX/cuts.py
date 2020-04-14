# cuts

#

massZ = '91.1876'
vetoZ = 'fabs(mll-'+massZ+')>15.'
Zcut  = 'fabs(mll-'+massZ+')<ZCUT'

OC = LepId + ' && mll>=20. && Lepton_pt[0]>=25. && Lepton_pt[1]>=20. && (Lepton_pdgId[0]*Lepton_pdgId[1]<0)'
SF = 'fabs(Lepton_pdgId[0])==fabs(Lepton_pdgId[1]) && '+vetoZ
DF = 'fabs(Lepton_pdgId[0])!=fabs(Lepton_pdgId[1])'
EE = SF+' && fabs(Lepton_pdgId[0])==11'
MM = SF+' && fabs(Lepton_pdgId[0])==13'

#cuts = {}

if opt.tag=='btagefficiencies':

    jetKinSelection = 'CleanJet_pt>=20. && abs(CleanJet_eta)<'+btagEtaMax
    jetTagSelection = 'Jet_'+btagAlgo+'[CleanJet_jetIdx]>='+btagCut
    cuts['taggablejets_b'] = jetKinSelection+' && abs(Jet_hadronFlavour[CleanJet_jetIdx])==5'
    cuts['taggablejets_c'] = jetKinSelection+' && abs(Jet_hadronFlavour[CleanJet_jetIdx])==4'
    cuts['taggablejets_l'] = jetKinSelection+' && abs(Jet_hadronFlavour[CleanJet_jetIdx])<4 '
    cuts[btagAlgo+'_'+btagWP+'_b']  = jetKinSelection+' && abs(Jet_hadronFlavour[CleanJet_jetIdx])==5 && '+jetTagSelection
    cuts[btagAlgo+'_'+btagWP+'_c']  = jetKinSelection+' && abs(Jet_hadronFlavour[CleanJet_jetIdx])==4 && '+jetTagSelection
    cuts[btagAlgo+'_'+btagWP+'_l']  = jetKinSelection+' && abs(Jet_hadronFlavour[CleanJet_jetIdx])<4  && '+jetTagSelection

if 'Test' in opt.tag:

    cuts['TwoLep_em'] = OC+' && '+DF+' && ptmiss>=80'
    cuts['TwoLep_em_Tag'] = '(' + OC+' && '+DF+' && ptmiss>=80)*'+btagWeight1tag
    cuts['TwoLep_em_Veto'] = '(' + OC+' && '+DF+' && ptmiss>=80)*'+btagWeight0tag

if 'TwoLeptons' in opt.tag:

    cuts['TwoLep_em'] = OC+' && '+DF
    cuts['TwoLep_ee'] = OC+' && fabs(Lepton_pdgId[0])==11 && fabs(Lepton_pdgId[1])==11' 
    cuts['TwoLep_mm'] = OC+' && fabs(Lepton_pdgId[0])==13 && fabs(Lepton_pdgId[1])==13'

if 'Preselection' in opt.tag:

    cuts['TwoLep_em_nometcut'] = OC+' && '+DF
    cuts['TwoLep_ee_nometcut'] = OC+' && '+EE
    cuts['TwoLep_mm_nometcut'] = OC+' && '+MM

    cuts['TwoLep_em'] = OC+' && '+DF+' && ptmiss>=80'
    cuts['TwoLep_ee'] = OC+' && '+EE+' && ptmiss>=80'
    cuts['TwoLep_mm'] = OC+' && '+MM+' && ptmiss>=80'

if 'TopControlRegion' in opt.tag:

    if 'Data' in opt.sigset:
        cuts['Top_em'] = '(' + OC+' && '+DF+' && ptmiss>=20) && '+BTAG 
        cuts['Top_ee'] = '(' + OC+' && '+EE+' && ptmiss>=50) && '+BTAG 
        cuts['Top_mm'] = '(' + OC+' && '+MM+' && ptmiss>=50) && '+BTAG 

    else: #if 'Backgrounds' in opt.sigset:
        cuts['Top_em'] = '(' + OC+' && '+DF+' && ptmiss>=20)*'+btagWeight1tag
        cuts['Top_ee'] = '(' + OC+' && '+EE+' && ptmiss>=50)*'+btagWeight1tag
        cuts['Top_mm'] = '(' + OC+' && '+MM+' && ptmiss>=50)*'+btagWeight1tag

if 'WWControlRegion' in opt.tag:

    cuts['WW_metcut'] = '(' + OC+' && '+DF+' && ptmiss>=70 && nCleanJet==0)'
    cuts['WW_nometcut'] = '(' + OC+' && '+DF+' && nCleanJet==0)'

if 'DYControlRegion' in opt.tag:

    DY = 'fabs(Lepton_pdgId[0])==fabs(Lepton_pdgId[1]) && ' + Zcut.replace('ZCUT',  '15.')

    if 'Data' in opt.sigset:
        cuts['DY_ee'] = '(' + OC+' && '+DY+' && fabs(Lepton_pdgId[0])==11) && '+VETO
        cuts['DY_mm'] = '(' + OC+' && '+DY+' && fabs(Lepton_pdgId[0])==13) && '+VETO

    else: #if 'Backgrounds' in opt.sigset:
        cuts['DY_ee'] = '(' + OC+' && '+DY+' && fabs(Lepton_pdgId[0])==11)*'+btagWeight0tag
        cuts['DY_mm'] = '(' + OC+' && '+DY+' && fabs(Lepton_pdgId[0])==13)*'+btagWeight0tag

if 'HighPtMissControlRegion' in opt.tag:

    if 'Data' in opt.sigset:
        cuts['VR1_Tag_em']   = OC+' && '+DF+' && ptmiss>=100 && ptmiss<140 && '+BTAG
        cuts['VR1_Veto_em']  = OC+' && '+DF+' && ptmiss>=100 && ptmiss<140 && '+VETO
        cuts['VR1_Tag_sf']   = OC+' && '+SF+' && ptmiss>=100 && ptmiss<140 && '+BTAG
        cuts['VR1_Veto_sf']  = OC+' && '+SF+' && ptmiss>=100 && ptmiss<140 && '+VETO

    else:
        cuts['VR1_Tag_em']   = '(' + OC+' && '+DF+' && ptmiss>=100 && ptmiss<140)*'+btagWeight1tag
        cuts['VR1_Veto_em']  = '(' + OC+' && '+DF+' && ptmiss>=100 && ptmiss<140)*'+btagWeight0tag
        cuts['VR1_Tag_sf']   = '(' + OC+' && '+SF+' && ptmiss>=100 && ptmiss<140)*'+btagWeight1tag
        cuts['VR1_Veto_sf']  = '(' + OC+' && '+SF+' && ptmiss>=100 && ptmiss<140)*'+btagWeight0tag

if 'TopValidationRegion' in opt.tag:

    if 'Data' in opt.sigset:
        cuts['VR1_Tag_em']   = OC+' && '+DF+' && ptmiss>=100 && ptmiss<140 && '+BTAG
        cuts['VR1_Tag_jets'] = OC+' && ('+SF+' || '+DF+') && ptmiss>=100 && ptmiss<140 && CleanJet_pt[1]>=30. && '+BTAG

    else:
        cuts['VR1_Tag_em']   = '(' + OC+' && '+DF+' && ptmiss>=100 && ptmiss<140)*'+btagWeight1tag
        cuts['VR1_Tag_jets'] = '(' + OC+' && ('+SF+' || '+DF+') && ptmiss>=100 && ptmiss<140 && CleanJet_pt[1]>=30.)*'+btagWeight1tag

if 'WWValidationRegion' in opt.tag and 'WZtoWWValidationRegion' not in opt.tag:

    if 'Data' in opt.sigset:
        cuts['VR1_Veto_em']   = OC+' && '+DF+' && ptmiss>=100 && ptmiss<140 && '+VETO
        cuts['VR1_Veto_0jet'] = OC+' && ('+SF+' || '+DF+') && ptmiss>=100 && ptmiss<140 && nCleanJet==0'

    else:
        cuts['VR1_Veto_em']   = '(' + OC+' && '+DF+' && ptmiss>=100 && ptmiss<140)*'+btagWeight0tag
        cuts['VR1_Veto_0jet'] = '(' + OC+' && ('+SF+' || '+DF+') && ptmiss>=100 && ptmiss<140 && nCleanJet==0)'

if 'SameSignValidationRegion' in opt.tag:

    SS = LepId + ' && mll>=20. && Lepton_pt[0]>=25. && Lepton_pt[1]>=20. && (Lepton_pdgId[0]*Lepton_pdgId[1]>0)'

    if 'Data' in opt.sigset:
        cuts['SS_ptmiss-100to140']  = SS+' && ptmiss>=100 && ptmiss<140 && '       +BTAG
        cuts['SS_ptmiss-140']       = SS+' && ptmiss>=140 && '                     +BTAG
        cuts['SS_ptmiss-140_plus']  = SS+' && ptmiss>=140 && Lepton_pdgId[0]<0 && '+BTAG
        cuts['SS_ptmiss-140_minus'] = SS+' && ptmiss>=140 && Lepton_pdgId[0]>0 && '+BTAG

    else:
        cuts['SS_ptmiss-100to140']   = '('+SS+' && ptmiss>=100 && ptmiss<140)*(btagWeight1tag)'
        cuts['SS_ptmiss-140']        = '('+SS+' && ptmiss>=140)*(btagWeight1tag)'
        cuts['SS_ptmiss-140_plus']   = '('+SS+' && ptmiss>=140 && Lepton_pdgId[0]<0)*(btagWeight1tag)'
        cuts['SS_ptmiss-140_minus']  = '('+SS+' && ptmiss>=140 && Lepton_pdgId[0]>0)*(btagWeight1tag)'

if 'FakeValidationRegion' in opt.tag:

    LepId2of3 = '('+T0+'+'+T1+'+'+T2+')==2'

    C2 = '(Lepton_pdgId[0]*Lepton_pdgId[1])'
    C1 = '(Lepton_pdgId[0]*Lepton_pdgId[2])'
    C0 = '(Lepton_pdgId[1]*Lepton_pdgId[2])'
    OCT = '('+C2+'*'+T0+'*'+T1+'+'+C1+'*'+T0+'*'+T2+'+'+C0+'*'+T1+'*'+T2+')<0'
    
    Fake = 'nLeptons==3 && ' + LepId2of3 + ' && ' + OCT + ' && Lepton_pt[2]>=20.'

    if 'Data' in opt.sigset:
        cuts['Fake_ptmiss-100to140']  = Fake+' && ptmiss>=100 && ptmiss<140 && '       +BTAG
        cuts['Fake_ptmiss-140']       = Fake+' && ptmiss>=140 && '                     +BTAG

    else:
        cuts['Fake_ptmiss-100to140']   = '('+Fake+' && ptmiss>=100 && ptmiss<140)*(btagWeight1tag)'
        cuts['Fake_ptmiss-140']        = '('+Fake+' && ptmiss>=140)*(btagWeight1tag)'

if 'WZValidationRegion' in opt.tag or 'WZtoWWValidationRegion' in opt.tag:

    WZselection = 'nLepton==3 && Lepton_pt[2]>=20. && ' + LepId3 + ' && deltaMassZ<ZCUT && ptmiss>=140'

    if 'WZValidationRegion' in opt.tag:

        if 'Data' in opt.sigset:
            cuts['WZ_3Lep']  = WZselection.replace('ZCUT', '999.') + ' && ' + VETO
            cuts['WZ_3LepZ'] = WZselection.replace('ZCUT',  '15.') + ' && ' + VETO

        else:
            cuts['WZ_3Lep']  = '(' + WZselection.replace('ZCUT', '999.') + ')*'+btagWeight0tag
            cuts['WZ_3LepZ'] = '(' + WZselection.replace('ZCUT',  '15.') + ')*'+btagWeight0tag

    elif 'WZtoWWValidationRegion' in opt.tag:

        if 'Data' in opt.sigset:
            cuts['WZtoWW_Zcut10'] = WZselection.replace('ZCUT', '10.') + ' && ' + VETO
            cuts['WZtoWW_Zcut15'] = WZselection.replace('ZCUT', '15.') + ' && ' + VETO

        else:
            cuts['WZtoWW_Zcut10'] = '(' + WZselection.replace('ZCUT',  '10.') + ')*'+btagWeight0tag
            cuts['WZtoWW_Zcut15'] = '(' + WZselection.replace('ZCUT',  '15.') + ')*'+btagWeight0tag

if 'ttZValidationRegion' in opt.tag or 'ZZValidationRegion' in opt.tag:

    sel4Lep = 'nLepton==4 && Lepton_pt[3]>=20. && ' + LepId3of4

    if 'ttZValidationRegion' in opt.tag:

        ttZselection = sel4Lep + ' && deltaMassZ<10. && nCleanJet>=2 && CleanJet_pt[1]>=20.'

        if 'Data' in opt.sigset:
            cuts['ttZ']            = ttZselection + ' && '                + BTAG
            cuts['ttZ_ptmiss-140'] = ttZselection + ' && ptmiss>=140 && ' + BTAG

        else:
            cuts['ttZ']            = '(' + ttZselection +                ')*(btagWeight1tag)'
            cuts['ttZ_ptmiss-140'] = '(' + ttZselection + ' && ptmiss>=140)*(btagWeight1tag)'

    elif 'ZZValidationRegion' in opt.tag:

        if 'Data' in opt.sigset:
            cuts['ZZ']            = sel4Lep + ' && '                + VETO
            cuts['ZZ_ptmiss-140'] = sel4Lep + ' && ptmiss>=140 && ' + VETO

        else:
            cuts['ZZ']            = '(' + sel4Lep +                ')*'+btagWeight0tag
            cuts['ZZ_ptmiss-140'] = '(' + sel4Lep + ' && ptmiss>=140)*'+btagWeight0tag

if 'DYValidationRegion' in opt.tag:

    DY = OC + ' && fabs(Lepton_pdgId[0])==fabs(Lepton_pdgId[1]) && ' + Zcut.replace('ZCUT',  '15.')

    if 'Data' in opt.sigset:
        cuts['ZZ_ptmiss-100to140']       = DY + ' && ptmiss>=100 && ptmiss<140 && ' + VETO
        cuts['ZZ_ptmiss-140']            = DY + ' && ptmiss>=140 && '               + VETO
        cuts['ZZ_ptmiss-100to140_nojet'] = DY + ' && ptmiss>=100 && ptmiss<140 && nCleanJet==0'
        cuts['ZZ_ptmiss-140_nojet']      = DY + ' && ptmiss>=140 && nCleanJet==0'            
        
    else:
        cuts['ZZ_ptmiss-100to140']       = '(' + DY + ' && ptmiss>=100 && ptmiss<140)*'+btagWeight0tag
        cuts['ZZ_ptmiss-140']            = '(' + DY + ' && ptmiss>=140)' +          '*'+btagWeight0tag
        cuts['ZZ_ptmiss-100to140_nojet'] = '(' + DY + ' && ptmiss>=100 && ptmiss<140 && nCleanJet==0)'
        cuts['ZZ_ptmiss-140_nojet']      = '(' + DY + ' && ptmiss>=140 && nCleanJet==0)' 

if 'StopSignalRegions' in opt.tag:
    if 'Data' in opt.sigset:
        isrcut=''
        btagcut=BTAG
        vetocut=VETO
        if 'ISR' in opt.tag:
            isrcut= ISRCutData
        if 'pt30' in opt.tag:
            btagcut=BTAG30
            vetocut=VETO30
        cuts['SR1_Tag_em']   = OC+' && '+DF+' && ptmiss>=140 && ptmiss<200 && '+btagcut
        cuts['SR1_Veto_em']  = OC+' && '+DF+' && ptmiss>=140 && ptmiss<200 && '+vetocut
    
        cuts['SR1_Tag_sf']   = OC+' && '+SF+' && ptmiss>=140 && ptmiss<200 && '+btagcut
        cuts['SR1_Veto_sf']  = OC+' && '+SF+' && ptmiss>=140 && ptmiss<200 && '+vetocut
    
        cuts['SR2_Tag_em']   = OC+' && '+DF+' && ptmiss>=200 && ptmiss<300 && '+btagcut
        cuts['SR2_Veto_em']  = OC+' && '+DF+' && ptmiss>=200 && ptmiss<300 && '+vetocut
    
        cuts['SR2_Tag_sf']   = OC+' && '+SF+' && ptmiss>=200 && ptmiss<300 && '+btagcut
        cuts['SR2_Veto_sf']  = OC+' && '+SF+' && ptmiss>=200 && ptmiss<300 && '+vetocut
    
        cuts['SR3_Tag_em']   = OC+' && '+DF+' && ptmiss>=300 && '+isrcut+btagcut
        cuts['SR3_Veto_em']  = OC+' && '+DF+' && ptmiss>=300 && '+isrcut+vetocut
    
        cuts['SR3_Tag_sf']   = OC+' && '+SF+' && ptmiss>=300 && '+isrcut+btagcut
        cuts['SR3_Veto_sf']  = OC+' && '+SF+' && ptmiss>=300 && '+isrcut+vetocut   

    else:
        isrcut= ' '
        btagcut=' '
        vetocut=' '
        if "ISR" in opt.tag:
            isrcut=ISRCutMC
        if "pt30" in opt.tag:
            btagcut=' && '+BTAG30
            vetocut=' && '+VETO30
        
        cuts['SR1_Tag_em']   = '(' + OC+' && '+DF+' && ptmiss>=140 && ptmiss<200'+btagcut+')*'+btagWeight1tag
        cuts['SR1_Veto_em']  = '(' + OC+' && '+DF+' && ptmiss>=140 && ptmiss<200'+vetocut+')*'+btagWeight0tag

        cuts['SR1_Tag_sf']   = '(' + OC+' && '+SF+' && ptmiss>=140 && ptmiss<200'+btagcut+')*'+btagWeight1tag
        cuts['SR1_Veto_sf']  = '(' + OC+' && '+SF+' && ptmiss>=140 && ptmiss<200'+vetocut+')*'+btagWeight0tag

        cuts['SR2_Tag_em']   = '(' + OC+' && '+DF+' && ptmiss>=200 && ptmiss<300'+btagcut+')*'+btagWeight1tag
        cuts['SR2_Veto_em']  = '(' + OC+' && '+DF+' && ptmiss>=200 && ptmiss<300'+vetocut+')*'+btagWeight0tag

        cuts['SR2_Tag_sf']   = '(' + OC+' && '+SF+' && ptmiss>=200 && ptmiss<300'+btagcut+')*'+btagWeight1tag
        cuts['SR2_Veto_sf']  = '(' + OC+' && '+SF+' && ptmiss>=200 && ptmiss<300'+vetocut+')*'+btagWeight0tag

        cuts['SR3_Tag_em']   = '(' + OC+' && '+DF+' && ptmiss>=300'+isrcut+btagcut+')*'+btagWeight1tag
        cuts['SR3_Veto_em']  = '(' + OC+' && '+DF+' && ptmiss>=300'+isrcut+vetocut+')*'+btagWeight0tag

        cuts['SR3_Tag_sf']   = '(' + OC+' && '+SF+' && ptmiss>=300'+isrcut+btagcut+')*'+btagWeight1tag
        cuts['SR3_Veto_sf']  = '(' + OC+' && '+SF+' && ptmiss>=300'+isrcut+vetocut+')*'+btagWeight0tag
        
            
                


if 'CharginoSignalRegions' in opt.tag:

    nojetcutSR1 = 'nCleanJet==0'
    jetscutSR1  = 'nCleanJet>0'
    nojetcutSR2 = nojetcutSR1
    jetscutSR2  = jetscutSR1
    isrcut=''

    if 'VisHTv1' in opt.tag:
        visht = '(Lepton_pt[0]+Lepton_pt[1]+Sum$(CleanJet_pt))'
        nojetcutSR1 = visht+'<200'
        jetscutSR1  = visht+'>=200'
        nojetcutSR2 = visht+'<300'
        jetscutSR2  = visht+'>=300'
    elif 'VisHTv2' in opt.tag:
        visht = '(Sum$(CleanJet_pt))'
        nojetcutSR1 = visht+'<50'
        jetscutSR1  = visht+'>=50'
        nojetcutSR2 = visht+'<50'
        jetscutSR2  = visht+'>=50'
    elif 'VisHTv3' in opt.tag:
        visht = '(Lepton_pt[0]+Lepton_pt[1])'
        nojetcutSR1 = visht+'<100'
        jetscutSR1  = visht+'>=100'
        nojetcutSR2 = visht+'<100'
        jetscutSR2  = visht+'>=100'
  
    if 'Data' in opt.sigset:
        if 'ISR' in opt.tag:     isrcut= ISRCutData
        cuts['SR1_Tag_em']   = OC+' && '+DF+' && ptmiss>=140 && ptmiss<200 && '+BTAG
        cuts['SR1_NoTag_em'] = OC+' && '+DF+' && ptmiss>=140 && ptmiss<200 && '+jetscutSR1+' && '+VETO
        cuts['SR1_NoJet_em'] = OC+' && '+DF+' && ptmiss>=140 && ptmiss<200 && '+nojetcutSR1+' && '+VETO
    
        cuts['SR1_Tag_sf']   = OC+' && '+SF+' && ptmiss>=140 && ptmiss<200 && '+BTAG
        cuts['SR1_NoTag_sf'] = OC+' && '+SF+' && ptmiss>=140 && ptmiss<200 && '+jetscutSR1+' && '+VETO
        cuts['SR1_NoJet_sf'] = OC+' && '+SF+' && ptmiss>=140 && ptmiss<200 && '+nojetcutSR1+' && '+VETO
    
        cuts['SR2_Tag_em']   = OC+' && '+DF+' && ptmiss>=200 && ptmiss<300 && '+BTAG
        cuts['SR2_NoTag_em'] = OC+' && '+DF+' && ptmiss>=200 && ptmiss<300 && '+jetscutSR2+' && '+VETO
        cuts['SR2_NoJet_em'] = OC+' && '+DF+' && ptmiss>=200 && ptmiss<300 && '+nojetcutSR2+' && '+VETO
    
        cuts['SR2_Tag_sf']   = OC+' && '+SF+' && ptmiss>=200 && ptmiss<300 && '+BTAG
        cuts['SR2_NoTag_sf'] = OC+' && '+SF+' && ptmiss>=200 && ptmiss<300 && '+jetscutSR2+' && '+VETO
        cuts['SR2_NoJet_sf'] = OC+' && '+SF+' && ptmiss>=200 && ptmiss<300 && '+nojetcutSR2+' && '+VETO
    
        cuts['SR3_Tag_em']   = OC+' && '+DF+' && ptmiss>=300 && '+isrcut+BTAG
        cuts['SR3_Veto_em']  = OC+' && '+DF+' && ptmiss>=300 && '+isrcut+VETO
    
        cuts['SR3_Tag_sf']   = OC+' && '+SF+' && ptmiss>=300 && '+isrcut+BTAG
        cuts['SR3_Veto_sf']  = OC+' && '+SF+' && ptmiss>=300 && '+isrcut+VETO

    else:
        if "ISR" in opt.tag:   isrcut=ISRCutMC
        cuts['SR1_Tag_em']   = '(' + OC+' && '+DF+' && ptmiss>=140 && ptmiss<200)*'+btagWeight1tag
        cuts['SR1_NoTag_em'] = '(' + OC+' && '+DF+' && ptmiss>=140 && ptmiss<200 && '+jetscutSR1+')*'+btagWeight0tag
        cuts['SR1_NoJet_em'] = '(' + OC+' && '+DF+' && ptmiss>=140 && ptmiss<200 && '+nojetcutSR1+')*'+btagWeight0tag

        cuts['SR1_Tag_sf']   = '(' + OC+' && '+SF+' && ptmiss>=140 && ptmiss<200)*'+btagWeight1tag
        cuts['SR1_NoTag_sf'] = '(' + OC+' && '+SF+' && ptmiss>=140 && ptmiss<200 && '+jetscutSR1+')*'+btagWeight0tag
        cuts['SR1_NoJet_sf'] = '(' + OC+' && '+SF+' && ptmiss>=140 && ptmiss<200 && '+nojetcutSR1+')*'+btagWeight0tag

        cuts['SR2_Tag_em']   = '(' + OC+' && '+DF+' && ptmiss>=200 && ptmiss<300)*'+btagWeight1tag
        cuts['SR2_NoTag_em'] = '(' + OC+' && '+DF+' && ptmiss>=200 && ptmiss<300 && '+jetscutSR2+')*'+btagWeight0tag
        cuts['SR2_NoJet_em'] = '(' + OC+' && '+DF+' && ptmiss>=200 && ptmiss<300 && '+nojetcutSR2+')*'+btagWeight0tag
        
        cuts['SR2_Tag_sf']   = '(' + OC+' && '+SF+' && ptmiss>=200 && ptmiss<300)*'+btagWeight1tag
        cuts['SR2_NoTag_sf'] = '(' + OC+' && '+SF+' && ptmiss>=200 && ptmiss<300 && '+jetscutSR2+')*'+btagWeight0tag
        cuts['SR2_NoJet_sf'] = '(' + OC+' && '+SF+' && ptmiss>=200 && ptmiss<300 && '+nojetcutSR2+')*'+btagWeight0tag

        cuts['SR3_Tag_em']   = '(' + OC+' && '+DF+' && ptmiss>=300'+isrcut+')*'+btagWeight1tag
        cuts['SR3_Veto_em']  = '(' + OC+' && '+DF+' && ptmiss>=300'+isrcut+')*'+btagWeight0tag

        cuts['SR3_Tag_sf']   = '(' + OC+' && '+SF+' && ptmiss>=300'+isrcut+')*'+btagWeight1tag
        cuts['SR3_Veto_sf']  = '(' + OC+' && '+SF+' && ptmiss>=300'+isrcut+')*'+btagWeight0tag

# apply background scale factors
 
try:
    normBackgrounds
except NameError:
    normBackgrounds = None
   
if 'SignalRegions' in opt.tag and normBackgrounds is not None:
        
    for background in normBackgrounds:
        if background in samples:
            for region in normBackgrounds[background]:
                
                selections = [ ] 

                regionScaleFactor = normBackgrounds[background][region]['scalefactor'].keys()[0]

                for selection in normBackgrounds[background][region]['selections']:

                    usedSelection = False

                    for cut in cuts:
                        if selection=='_All' or selection in cut: 
                            normBackgrounds[background][region]['cuts'].append(cut)
                            usedSelection = True

                    if usedSelection:

                        selections.append(selection)

                        #if float(regionScaleFactor)!=1.:
                        #
                        #    selectionCut = normBackgrounds[background][region]['selections'][selection]
                        #    selectionWeight = '(!'+selectionCut+')+'+selectionCut+'*'+regionScaleFactor
                        #    samples[background]['weight'] += '*('+selectionWeight+')'
                
                if selections and float(regionScaleFactor)!=1.:

                    regionCut = '1.'

                    if len(selections)==1:
                        regionCut = normBackgrounds[background][region]['selections'][selections[0]]
                    else:
                        if '_Tag' in selections and '_NoTag' in selections and '_NoJet' not in selections:
                            regionCut = 'nCleanJet>=1'
                        elif '_Tag' in selections and '_Veto' in selections:
                            regionCut = '1.'

                    # Patches for ZZ veto
                    if '_Tag' in selections and '_Veto' not in selections and '_NoTag' not in selections:
                        regionCut = 'nCleanJet>=1'
                    if '_Veto' in selections and '_Tag' not in selections:
                        regionCut = 'nCleanJet==0'
                        regionScaleFactor = normBackgrounds[background]['nojet']['scalefactor'].keys()[0]

                    regionWeight = '(!'+regionCut+')+('+regionCut+')*'+regionScaleFactor
                    samples[background]['weight'] += '*('+regionWeight+')'
                    
