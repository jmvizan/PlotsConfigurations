# cuts

#

massZ = '91.1876'
vetoZ = 'fabs(mll-'+massZ+')>15.'

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

    DY = 'fabs(Lepton_pdgId[0])==fabs(Lepton_pdgId[1]) && !('+vetoZ+')'

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
        cuts['VR1_Tag_sf']   = OC+' && ('+SF+' || '+DF+') && ptmiss>=100 && ptmiss<140 && CleanJet_pt[1]>=30. && '+BTAG

    else:
        cuts['VR1_Tag_em']   = '(' + OC+' && '+DF+' && ptmiss>=100 && ptmiss<140)*btagWeight_1tag'
        cuts['VR1_Tag_sf']   = '(' + OC+' && ('+SF+' || '+DF+') && ptmiss>=100 && ptmiss<140 && CleanJet_pt[1]>=30.)*btagWeight_1tag'

if 'WWValidationRegion' in opt.tag:

    if 'Data' in opt.sigset:
        cuts['VR1_Veto_em']  = OC+' && '+DF+' && ptmiss>=100 && ptmiss<140 && '+VETO
        cuts['VR1_Veto_sf']  = OC+' && ('+SF+' || '+DF+') && ptmiss>=100 && ptmiss<140 && nCleanJet==0'

    else:
        cuts['VR1_Veto_em']  = '(' + OC+' && '+DF+' && ptmiss>=100 && ptmiss<140)*(1.-btagWeight_1tag)'
        cuts['VR1_Veto_sf']  = '(' + OC+' && ('+SF+' || '+DF+') && ptmiss>=100 && ptmiss<140 && nCleanJet==0)'

if 'StopSignalRegions' in opt.tag:
    
    if 'Data' in opt.sigset:
        cuts['SR1_Tag_em']   = OC+' && '+DF+' && ptmiss>=140 && ptmiss<200 && '+BTAG
        cuts['SR1_Veto_em']  = OC+' && '+DF+' && ptmiss>=140 && ptmiss<200 && '+VETO
    
        cuts['SR1_Tag_sf']   = OC+' && '+SF+' && ptmiss>=140 && ptmiss<200 && '+BTAG
        cuts['SR1_Veto_sf']  = OC+' && '+SF+' && ptmiss>=140 && ptmiss<200 && '+VETO
    
        cuts['SR2_Tag_em']   = OC+' && '+DF+' && ptmiss>=200 && ptmiss<300 && '+BTAG
        cuts['SR2_Veto_em']  = OC+' && '+DF+' && ptmiss>=200 && ptmiss<300 && '+VETO
    
        cuts['SR2_Tag_sf']   = OC+' && '+SF+' && ptmiss>=200 && ptmiss<300 && '+BTAG
        cuts['SR2_Veto_sf']  = OC+' && '+SF+' && ptmiss>=200 && ptmiss<300 && '+VETO
    
        cuts['SR3_Tag_em']   = OC+' && '+DF+' && ptmiss>=300 && '+BTAG
        cuts['SR3_Veto_em']  = OC+' && '+DF+' && ptmiss>=300 && '+VETO
    
        cuts['SR3_Tag_sf']   = OC+' && '+SF+' && ptmiss>=300 && '+BTAG
        cuts['SR3_Veto_sf']  = OC+' && '+SF+' && ptmiss>=300 && '+VETO

    else:
        cuts['SR1_Tag_em']   = '(' + OC+' && '+DF+' && ptmiss>=140 && ptmiss<200)*btagWeight_1tag'
        cuts['SR1_Veto_em']  = '(' + OC+' && '+DF+' && ptmiss>=140 && ptmiss<200)*(1.-btagWeight_1tag)'

        cuts['SR1_Tag_sf']   = '(' + OC+' && '+SF+' && ptmiss>=140 && ptmiss<200)*btagWeight_1tag'
        cuts['SR1_Veto_sf']  = '(' + OC+' && '+SF+' && ptmiss>=140 && ptmiss<200)*(1.-btagWeight_1tag)'

        cuts['SR2_Tag_em']   = '(' + OC+' && '+DF+' && ptmiss>=200 && ptmiss<300)*btagWeight_1tag'
        cuts['SR2_Veto_em']  = '(' + OC+' && '+DF+' && ptmiss>=200 && ptmiss<300)*(1.-btagWeight_1tag)'

        cuts['SR2_Tag_sf']   = '(' + OC+' && '+SF+' && ptmiss>=200 && ptmiss<300)*btagWeight_1tag'
        cuts['SR2_Veto_sf']  = '(' + OC+' && '+SF+' && ptmiss>=200 && ptmiss<300)*(1.-btagWeight_1tag)'

        cuts['SR3_Tag_em']   = '(' + OC+' && '+DF+' && ptmiss>=300)*btagWeight_1tag'
        cuts['SR3_Veto_em']  = '(' + OC+' && '+DF+' && ptmiss>=300)*(1.-btagWeight_1tag)'

        cuts['SR3_Tag_sf']   = '(' + OC+' && '+SF+' && ptmiss>=300)*btagWeight_1tag'
        cuts['SR3_Veto_sf']  = '(' + OC+' && '+SF+' && ptmiss>=300)*(1.-btagWeight_1tag)'

