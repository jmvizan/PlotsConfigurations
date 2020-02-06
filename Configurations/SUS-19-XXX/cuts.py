# cuts

#

massZ = '91.1876'
vetoZ = 'fabs(mll-'+massZ+')>15.'
Zcut  = 'fabs(mZ-'+massZ+')<ZCUT'

LepId = '(Lepton_isTightElectron_cutBasedMediumPOG[0]+Lepton_isTightMuon_mediumRelIsoTight[0]+Lepton_isTightElectron_cutBasedMediumPOG[1]+Lepton_isTightMuon_mediumRelIsoTight[1])==2'
OC = LepId + ' && mll>=20. && Lepton_pt[0]>=25. && Lepton_pt[1]>=20. && (Lepton_pdgId[0]*Lepton_pdgId[1]<0)'
SF = 'fabs(Lepton_pdgId[0])==fabs(Lepton_pdgId[1]) && '+vetoZ
DF = 'fabs(Lepton_pdgId[0])!=fabs(Lepton_pdgId[1])'
EE = SF+' && fabs(Lepton_pdgId[0])==11'
MM = SF+' && fabs(Lepton_pdgId[0])==13'

btagAlgo = 'btagDeepB'
btagWP   = '2016M'
btagCut  = '0.6321'
btagEtaMax = '2.4'
"""
BTAG = '((CleanJet_pt[0]>=20. && fabs(CleanJet_eta[0])<2.4 && Jet_'+btagAlgo+'[CleanJet_jetIdx[0]]>='+btagCut+') || \
         (CleanJet_pt[1]>=20. && fabs(CleanJet_eta[1])<2.4 && Jet_'+btagAlgo+'[CleanJet_jetIdx[1]]>='+btagCut+') || \
         (CleanJet_pt[2]>=20. && fabs(CleanJet_eta[2])<2.4 && Jet_'+btagAlgo+'[CleanJet_jetIdx[2]]>='+btagCut+') || \
         (CleanJet_pt[3]>=20. && fabs(CleanJet_eta[3])<2.4 && Jet_'+btagAlgo+'[CleanJet_jetIdx[3]]>='+btagCut+') || \
         (CleanJet_pt[4]>=20. && fabs(CleanJet_eta[4])<2.4 && Jet_'+btagAlgo+'[CleanJet_jetIdx[4]]>='+btagCut+') || \
         (CleanJet_pt[5]>=20. && fabs(CleanJet_eta[5])<2.4 && Jet_'+btagAlgo+'[CleanJet_jetIdx[5]]>='+btagCut+') || \
         (CleanJet_pt[6]>=20. && fabs(CleanJet_eta[6])<2.4 && Jet_'+btagAlgo+'[CleanJet_jetIdx[6]]>='+btagCut+') || \
         (CleanJet_pt[7]>=20. && fabs(CleanJet_eta[7])<2.4 && Jet_'+btagAlgo+'[CleanJet_jetIdx[7]]>='+btagCut+') || \
         (CleanJet_pt[8]>=20. && fabs(CleanJet_eta[8])<2.4 && Jet_'+btagAlgo+'[CleanJet_jetIdx[8]]>='+btagCut+') || \
         (CleanJet_pt[9]>=20. && fabs(CleanJet_eta[9])<2.4 && Jet_'+btagAlgo+'[CleanJet_jetIdx[9]]>='+btagCut+') || \
         (CleanJet_pt[5]>=20. && fabs(CleanJet_eta[5])<2.4 && Jet_'+btagAlgo+'[CleanJet_jetIdx[5]]>='+btagCut+'))'
"""
BTAG = '(leadingPtTagged>=20.)' 
VETO = '!'+BTAG

BTAG30= '(leadingPtTagged>=30.)'
VETO30 = '!'+BTAG30

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
    cuts['TwoLep_em_Tag'] = '(' + OC+' && '+DF+' && ptmiss>=80)*btagWeight_1tag'
    cuts['TwoLep_em_Veto'] = '(' + OC+' && '+DF+' && ptmiss>=80)*(1.-btagWeight_1tag)'

if 'Preselection' in opt.tag:

    cuts['TwoLep_em'] = OC+' && '+DF+' && ptmiss>=80'
    cuts['TwoLep_ee'] = OC+' && '+EE+' && ptmiss>=80'
    cuts['TwoLep_mm'] = OC+' && '+MM+' && ptmiss>=80'

if 'TopControlRegion' in opt.tag:

    if 'Data' in opt.sigset:
        cuts['Top_em'] = '(' + OC+' && '+DF+' && ptmiss>=20) && '+BTAG 
        cuts['Top_ee'] = '(' + OC+' && '+EE+' && ptmiss>=50) && '+BTAG 
        cuts['Top_mm'] = '(' + OC+' && '+MM+' && ptmiss>=50) && '+BTAG 

    else: #if 'Backgrounds' in opt.sigset:
        cuts['Top_em'] = '(' + OC+' && '+DF+' && ptmiss>=20)*btagWeight_1tag'
        cuts['Top_ee'] = '(' + OC+' && '+EE+' && ptmiss>=50)*btagWeight_1tag'
        cuts['Top_mm'] = '(' + OC+' && '+MM+' && ptmiss>=50)*btagWeight_1tag'

if 'WWControlRegion' in opt.tag:

    cuts['WW_metcut'] = '(' + OC+' && '+DF+' && ptmiss>=70 && nCleanJet==0)'
    cuts['WW_nometcut'] = '(' + OC+' && '+DF+' && nCleanJet==0)'

if 'DYControlRegion' in opt.tag:

    DY = 'fabs(Lepton_pdgId[0])==fabs(Lepton_pdgId[1]) && ' + Zcut.replace('ZCUT',  '15.')

    if 'Data' in opt.sigset:
        cuts['DY_ee'] = '(' + OC+' && '+DY+' && fabs(Lepton_pdgId[0])==11) && '+VETO
        cuts['DY_mm'] = '(' + OC+' && '+DY+' && fabs(Lepton_pdgId[0])==13) && '+VETO

    else: #if 'Backgrounds' in opt.sigset:
        cuts['DY_ee'] = '(' + OC+' && '+DY+' && fabs(Lepton_pdgId[0])==11)*(1.-btagWeight_1tag)'
        cuts['DY_mm'] = '(' + OC+' && '+DY+' && fabs(Lepton_pdgId[0])==13)*(1.-btagWeight_1tag)'

if 'HighPtMissControlRegion' in opt.tag:

    if 'Data' in opt.sigset:
        cuts['VR1_Tag_em']   = OC+' && '+DF+' && ptmiss>=100 && ptmiss<140 && '+BTAG
        cuts['VR1_Veto_em']  = OC+' && '+DF+' && ptmiss>=100 && ptmiss<140 && '+VETO
        cuts['VR1_Tag_sf']   = OC+' && '+SF+' && ptmiss>=100 && ptmiss<140 && '+BTAG
        cuts['VR1_Veto_sf']  = OC+' && '+SF+' && ptmiss>=100 && ptmiss<140 && '+VETO

    else:
        cuts['VR1_Tag_em']   = '(' + OC+' && '+DF+' && ptmiss>=100 && ptmiss<140)*btagWeight_1tag'
        cuts['VR1_Veto_em']  = '(' + OC+' && '+DF+' && ptmiss>=100 && ptmiss<140)*(1.-btagWeight_1tag)'
        cuts['VR1_Tag_sf']   = '(' + OC+' && '+SF+' && ptmiss>=100 && ptmiss<140)*btagWeight_1tag'
        cuts['VR1_Veto_sf']  = '(' + OC+' && '+SF+' && ptmiss>=100 && ptmiss<140)*(1.-btagWeight_1tag)'

if 'TopValidationRegion' in opt.tag:

    if 'Data' in opt.sigset:
        cuts['VR1_Tag_em']   = OC+' && '+DF+' && ptmiss>=100 && ptmiss<140 && '+BTAG
        cuts['VR1_Tag_jets'] = OC+' && ('+SF+' || '+DF+') && ptmiss>=100 && ptmiss<140 && CleanJet_pt[1]>=30. && '+BTAG

    else:
        cuts['VR1_Tag_em']   = '(' + OC+' && '+DF+' && ptmiss>=100 && ptmiss<140)*btagWeight_1tag'
        cuts['VR1_Tag_jets'] = '(' + OC+' && ('+SF+' || '+DF+') && ptmiss>=100 && ptmiss<140 && CleanJet_pt[1]>=30.)*btagWeight_1tag'

if 'WWValidationRegion' in opt.tag:

    if 'Data' in opt.sigset:
        cuts['VR1_Veto_em']   = OC+' && '+DF+' && ptmiss>=100 && ptmiss<140 && '+VETO
        cuts['VR1_Veto_0jet'] = OC+' && ('+SF+' || '+DF+') && ptmiss>=100 && ptmiss<140 && nCleanJet==0'

    else:
        cuts['VR1_Veto_em']   = '(' + OC+' && '+DF+' && ptmiss>=100 && ptmiss<140)*(1.-btagWeight_1tag)'
        cuts['VR1_Veto_0jet'] = '(' + OC+' && ('+SF+' || '+DF+') && ptmiss>=100 && ptmiss<140 && nCleanJet==0)'

if 'SameSignValidationRegion' in opt.tag:

    SS = LepId + ' && mll>=20. && Lepton_pt[0]>=25. && Lepton_pt[1]>=20. && (Lepton_pdgId[0]*Lepton_pdgId[1]>0)'

    if 'Data' in opt.sigset:
        cuts['SS_ptmiss-100to140']  = SS+' && ptmiss>=100 && ptmiss<140 && '       +BTAG
        cuts['SS_ptmiss-140']       = SS+' && ptmiss>=140 && '                     +BTAG
        cuts['SS_ptmiss-140_plus']  = SS+' && ptmiss>=140 && Lepton_pdgId[0]<0 && '+BTAG
        cuts['SS_ptmiss-140_minus'] = SS+' && ptmiss>=140 && Lepton_pdgId[0]>0 && '+BTAG

    else:
        cuts['SS_ptmiss-100to140']   = '('+SS+' && ptmiss>=100 && ptmiss<140)*(btagWeight_1tag)'
        cuts['SS_ptmiss-140']        = '('+SS+' && ptmiss>=140)*(btagWeight_1tag)'
        cuts['SS_ptmiss-140_plus']   = '('+SS+' && ptmiss>=140 && Lepton_pdgId[0]<0)*(btagWeight_1tag)'
        cuts['SS_ptmiss-140_minus']  = '('+SS+' && ptmiss>=140 && Lepton_pdgId[0]>0)*(btagWeight_1tag)'

if 'FakeValidationRegion' in opt.tag:

    T0 = '(Lepton_isTightElectron_cutBasedMediumPOG[0]+Lepton_isTightMuon_mediumRelIsoTight[0])'
    T1 = '(Lepton_isTightElectron_cutBasedMediumPOG[1]+Lepton_isTightMuon_mediumRelIsoTight[1])'
    T2 = '(Lepton_isTightElectron_cutBasedMediumPOG[2]+Lepton_isTightMuon_mediumRelIsoTight[2])'
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
        cuts['Fake_ptmiss-100to140']   = '('+Fake+' && ptmiss>=100 && ptmiss<140)*(btagWeight_1tag)'
        cuts['Fake_ptmiss-140']        = '('+Fake+' && ptmiss>=140)*(btagWeight_1tag)'

if 'WZValidationRegion' in opt.tag or 'WZtoWWValidationRegion' in opt.tag:

    LepId3 = '(Lepton_isTightElectron_cutBasedMediumPOG[0]+Lepton_isTightMuon_mediumRelIsoTight[0]+Lepton_isTightElectron_cutBasedMediumPOG[1]+Lepton_isTightMuon_mediumRelIsoTight[1]+Lepton_isTightElectron_cutBasedMediumPOG[2]+Lepton_isTightMuon_mediumRelIsoTight[2])==3'
    Zcut = 'fabs(mZ-'+massZ+')<ZCUT'

    WZselection = 'nLepton==3 && Lepton_pt[2]>=20. && ' + LepId3 + ' && ' + Zcut + ' && ptmiss>=140'

    if 'WZValidationRegion' in opt.tag:

        if 'Data' in opt.sigset:
            cuts['WZ_3Lep']  = WZselection.replace('ZCUT', '999.') + ' && ' + VETO
            cuts['WZ_3LepZ'] = WZselection.replace('ZCUT',  '15.') + ' && ' + VETO

        else:
            cuts['WZ_3Lep']  = '(' + WZselection.replace('ZCUT', '999.') + ')*(1.-btagWeight_1tag)'
            cuts['WZ_3LepZ'] = '(' + WZselection.replace('ZCUT',  '15.') + ')*(1.-btagWeight_1tag)'

    elif 'WZtoWWValidationRegion' in opt.tag:

        if 'Data' in opt.sigset:
            cuts['WZtoWW'] = WZselection.replace('ZCUT', '10.') + ' && ' + VETO

        else:
            cuts['WZtoWW'] = '(' + WZselection.replace('ZCUT',  '10.') + ')*(1.-btagWeight_1tag)'

if 'ttZValidationRegion' in opt.tag or 'ZZValidationRegion' in opt.tag:

    LepId3of4 = '(Lepton_isTightElectron_cutBasedMediumPOG[0]+Lepton_isTightMuon_mediumRelIsoTight[0]+Lepton_isTightElectron_cutBasedMediumPOG[1]+Lepton_isTightMuon_mediumRelIsoTight[1]+Lepton_isTightElectron_cutBasedMediumPOG[2]+Lepton_isTightMuon_mediumRelIsoTight[2]+Lepton_isTightElectron_cutBasedMediumPOG[3]+Lepton_isTightMuon_mediumRelIsoTight[3])==3'

    sel4Lep = 'nLepton==4 && Lepton_pt[3]>=20. && ' + LepId3of4

    if 'ttZValidationRegion' in opt.tag:

        ttZselection = sel4Lep + ' && ' + Zcut.replace('ZCUT',  '10.') + ' && nCleanJet>=2 && CleanJet_pt[1]>=20.'

        if 'Data' in opt.sigset:
            cuts['ttZ']            = ttZselection + ' && '                + BTAG
            cuts['ttZ_ptmiss-140'] = ttZselection + ' && ptmiss>=140 && ' + BTAG

        else:
            cuts['ttZ']            = '(' + ttZselection +                ')*(btagWeight_1tag)'
            cuts['ttZ_ptmiss-140'] = '(' + ttZselection + ' && ptmiss>=140)*(btagWeight_1tag)'

    elif 'ZZValidationRegion' in opt.tag:

        if 'Data' in opt.sigset:
            cuts['ZZ']            = sel4Lep + ' && '                + VETO
            cuts['ZZ_ptmiss-140'] = sel4Lep + ' && ptmiss>=140 && ' + VETO

        else:
            cuts['ZZ']            = '(' + sel4Lep +                ')*(1.-btagWeight_1tag)'
            cuts['ZZ_ptmiss-140'] = '(' + sel4Lep + ' && ptmiss>=140)*(1.-btagWeight_1tag)'

if 'DYValidationRegion' in opt.tag:

    DY = OC + ' && fabs(Lepton_pdgId[0])==fabs(Lepton_pdgId[1]) && ' + Zcut.replace('ZCUT',  '15.')

    if 'Data' in opt.sigset:
        cuts['ZZ_ptmiss-100to140']       = DY + ' && ptmiss>=100 && ptmiss<140 && ' + VETO
        cuts['ZZ_ptmiss-140']            = DY + ' && ptmiss>=140 && '               + VETO
        cuts['ZZ_ptmiss-100to140_nojet'] = DY + ' && ptmiss>=100 && ptmiss<140 && nCleanJet==0'
        cuts['ZZ_ptmiss-140_nojet']      = DY + ' && ptmiss>=140 && nCleanJet==0'            
        
    else:
        cuts['ZZ_ptmiss-100to140']       = '(' + DY + ' && ptmiss>=100 && ptmiss<140)*(1.-btagWeight_1tag)'
        cuts['ZZ_ptmiss-140']            = '(' + DY + ' && ptmiss>=140)' +          '*(1.-btagWeight_1tag)'
        cuts['ZZ_ptmiss-100to140_nojet'] = '(' + DY + ' && ptmiss>=100 && ptmiss<140 && nCleanJet==0)'
        cuts['ZZ_ptmiss-140_nojet']      = '(' + DY + ' && ptmiss>=140 && nCleanJet==0)' 

if 'StopSignalRegions' in opt.tag:
    if 'Data' in opt.sigset:
        isrcut=''
        btagcut=BTAG
        vetocut=VETO
        if 'ISR' in opt.tag:
            isrcut= ' CleanJet_pt[0]>150. && CleanJet_pt[0]!=leadingPtTagged && acos(cos(MET_phi-CleanJet_phi[0]))>2.5 && '
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
            isrcut='&& CleanJet_pt[0]>150. && CleanJet_pt[0]!=leadingPtTagged && acos(cos(MET_phi-CleanJet_phi[0]))>2.5 '
        if "pt30" in opt.tag:
            btagcut=' && '+BTAG30
            vetocut=' && '+VETO30
        
        cuts['SR1_Tag_em']   = '(' + OC+' && '+DF+' && ptmiss>=140 && ptmiss<200'+btagcut+')*btagWeight_1tag'
        cuts['SR1_Veto_em']  = '(' + OC+' && '+DF+' && ptmiss>=140 && ptmiss<200'+vetocut+')*(1.-btagWeight_1tag)'

        cuts['SR1_Tag_sf']   = '(' + OC+' && '+SF+' && ptmiss>=140 && ptmiss<200'+btagcut+')*btagWeight_1tag'
        cuts['SR1_Veto_sf']  = '(' + OC+' && '+SF+' && ptmiss>=140 && ptmiss<200'+vetocut+')*(1.-btagWeight_1tag)'

        cuts['SR2_Tag_em']   = '(' + OC+' && '+DF+' && ptmiss>=200 && ptmiss<300'+btagcut+')*btagWeight_1tag'
        cuts['SR2_Veto_em']  = '(' + OC+' && '+DF+' && ptmiss>=200 && ptmiss<300'+vetocut+')*(1.-btagWeight_1tag)'

        cuts['SR2_Tag_sf']   = '(' + OC+' && '+SF+' && ptmiss>=200 && ptmiss<300'+btagcut+')*btagWeight_1tag'
        cuts['SR2_Veto_sf']  = '(' + OC+' && '+SF+' && ptmiss>=200 && ptmiss<300'+vetocut+')*(1.-btagWeight_1tag)'

        cuts['SR3_Tag_em']   = '(' + OC+' && '+DF+' && ptmiss>=300'+isrcut+btagcut+')*btagWeight_1tag'
        cuts['SR3_Veto_em']  = '(' + OC+' && '+DF+' && ptmiss>=300'+isrcut+vetocut+')*(1.-btagWeight_1tag)'

        cuts['SR3_Tag_sf']   = '(' + OC+' && '+SF+' && ptmiss>=300'+isrcut+btagcut+')*btagWeight_1tag'
        cuts['SR3_Veto_sf']  = '(' + OC+' && '+SF+' && ptmiss>=300'+isrcut+vetocut+')*(1.-btagWeight_1tag)'
        
            
                


if 'CharginoSignalRegions' in opt.tag:

    if 'Data' in opt.sigset:
        cuts['SR1_Tag_em']   = OC+' && '+DF+' && ptmiss>=140 && ptmiss<200 && '+BTAG
        cuts['SR1_NoTag_em'] = OC+' && '+DF+' && ptmiss>=140 && ptmiss<200 && nCleanJet>0 && '+VETO
        cuts['SR1_NoJet_em'] = OC+' && '+DF+' && ptmiss>=140 && ptmiss<200 && nCleanJet==0'
    
        cuts['SR1_Tag_sf']   = OC+' && '+SF+' && ptmiss>=140 && ptmiss<200 && '+BTAG
        cuts['SR1_NoTag_sf'] = OC+' && '+SF+' && ptmiss>=140 && ptmiss<200 && nCleanJet>0 && '+VETO
        cuts['SR1_NoJet_sf'] = OC+' && '+SF+' && ptmiss>=140 && ptmiss<200 && nCleanJet==0'
    
        cuts['SR2_Tag_em']   = OC+' && '+DF+' && ptmiss>=200 && ptmiss<300 && '+BTAG
        cuts['SR2_NoTag_em'] = OC+' && '+DF+' && ptmiss>=200 && ptmiss<300 && nCleanJet>0 && '+VETO
        cuts['SR2_NoJet_em'] = OC+' && '+DF+' && ptmiss>=200 && ptmiss<300 && nCleanJet==0'
    
        cuts['SR2_Tag_sf']   = OC+' && '+SF+' && ptmiss>=200 && ptmiss<300 && '+BTAG
        cuts['SR2_NoTag_sf'] = OC+' && '+SF+' && ptmiss>=200 && ptmiss<300 && nCleanJet>0 && '+VETO
        cuts['SR2_NoJet_sf'] = OC+' && '+SF+' && ptmiss>=200 && ptmiss<300 && nCleanJet==0'
    
        cuts['SR3_Tag_em']   = OC+' && '+DF+' && ptmiss>=300 && '+BTAG
        cuts['SR3_Veto_em']  = OC+' && '+DF+' && ptmiss>=300 && '+VETO
    
        cuts['SR3_Tag_sf']   = OC+' && '+SF+' && ptmiss>=300 && '+BTAG
        cuts['SR3_Veto_sf']  = OC+' && '+SF+' && ptmiss>=300 && '+VETO

    else:
        cuts['SR1_Tag_em']   = '(' + OC+' && '+DF+' && ptmiss>=140 && ptmiss<200)*btagWeight_1tag'
        cuts['SR1_NoTag_em'] = '(' + OC+' && '+DF+' && ptmiss>=140 && ptmiss<200 && nCleanJet>0)*(1.-btagWeight_1tag)'
        cuts['SR1_NoJet_em'] = '(' + OC+' && '+DF+' && ptmiss>=140 && ptmiss<200 && nCleanJet==0)'

        cuts['SR1_Tag_sf']   = '(' + OC+' && '+SF+' && ptmiss>=140 && ptmiss<200)*btagWeight_1tag'
        cuts['SR1_NoTag_sf'] = '(' + OC+' && '+SF+' && ptmiss>=140 && ptmiss<200 && nCleanJet>0)*(1.-btagWeight_1tag)'
        cuts['SR1_NoJet_sf'] = '(' + OC+' && '+SF+' && ptmiss>=140 && ptmiss<200 && nCleanJet==0)'

        cuts['SR2_Tag_em']   = '(' + OC+' && '+DF+' && ptmiss>=200 && ptmiss<300)*btagWeight_1tag'
        cuts['SR2_NoTag_em'] = '(' + OC+' && '+DF+' && ptmiss>=200 && ptmiss<300 && nCleanJet>0)*(1.-btagWeight_1tag)'
        cuts['SR2_NoJet_em'] = '(' + OC+' && '+DF+' && ptmiss>=200 && ptmiss<300 && nCleanJet==0)'

        cuts['SR2_Tag_sf']   = '(' + OC+' && '+SF+' && ptmiss>=200 && ptmiss<300)*btagWeight_1tag'
        cuts['SR2_NoTag_sf'] = '(' + OC+' && '+SF+' && ptmiss>=200 && ptmiss<300 && nCleanJet>0)*(1.-btagWeight_1tag)'
        cuts['SR2_NoJet_sf'] = '(' + OC+' && '+SF+' && ptmiss>=200 && ptmiss<300 && nCleanJet==0)'

        cuts['SR3_Tag_em']   = '(' + OC+' && '+DF+' && ptmiss>=300)*btagWeight_1tag'
        cuts['SR3_Veto_em']  = '(' + OC+' && '+DF+' && ptmiss>=300)*(1.-btagWeight_1tag)'

        cuts['SR3_Tag_sf']   = '(' + OC+' && '+SF+' && ptmiss>=300)*btagWeight_1tag'
        cuts['SR3_Veto_sf']  = '(' + OC+' && '+SF+' && ptmiss>=300)*(1.-btagWeight_1tag)'

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

                    regionWeight = '(!'+regionCut+')+'+regionCut+'*'+regionScaleFactor
                    samples[background]['weight'] += '*('+regionWeight+')'
                    
