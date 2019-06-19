# cuts

#cuts = {}

OC = 'Lepton_pt[0]>=25. && Lepton_pt[1]>=20. && (Lepton_pdgId[0]*Lepton_pdgId[1]<0)'
SF = 'fabs(Lepton_pdgId[0])==fabs(Lepton_pdgId[1])'
DF = 'fabs(Lepton_pdgId[0])!=fabs(Lepton_pdgId[1])'

btagAlgo = 'btagDeepB'
btagWP = '0.6321'
"""
BTAG = '((CleanJet_pt[0]>=20. && fabs(CleanJet_eta[0])<2.4 && Jet_'+btagAlgo+'[CleanJet_jetIdx[0]]>='+btagWP+') || \
         (CleanJet_pt[1]>=20. && fabs(CleanJet_eta[1])<2.4 && Jet_'+btagAlgo+'[CleanJet_jetIdx[1]]>='+btagWP+') || \
         (CleanJet_pt[2]>=20. && fabs(CleanJet_eta[2])<2.4 && Jet_'+btagAlgo+'[CleanJet_jetIdx[2]]>='+btagWP+') || \
         (CleanJet_pt[3]>=20. && fabs(CleanJet_eta[3])<2.4 && Jet_'+btagAlgo+'[CleanJet_jetIdx[3]]>='+btagWP+') || \
         (CleanJet_pt[4]>=20. && fabs(CleanJet_eta[4])<2.4 && Jet_'+btagAlgo+'[CleanJet_jetIdx[4]]>='+btagWP+') || \
         (CleanJet_pt[5]>=20. && fabs(CleanJet_eta[5])<2.4 && Jet_'+btagAlgo+'[CleanJet_jetIdx[5]]>='+btagWP+') || \
         (CleanJet_pt[6]>=20. && fabs(CleanJet_eta[6])<2.4 && Jet_'+btagAlgo+'[CleanJet_jetIdx[6]]>='+btagWP+') || \
         (CleanJet_pt[7]>=20. && fabs(CleanJet_eta[7])<2.4 && Jet_'+btagAlgo+'[CleanJet_jetIdx[7]]>='+btagWP+') || \
         (CleanJet_pt[8]>=20. && fabs(CleanJet_eta[8])<2.4 && Jet_'+btagAlgo+'[CleanJet_jetIdx[8]]>='+btagWP+') || \
         (CleanJet_pt[9]>=20. && fabs(CleanJet_eta[9])<2.4 && Jet_'+btagAlgo+'[CleanJet_jetIdx[9]]>='+btagWP+') || \
         (CleanJet_pt[5]>=20. && fabs(CleanJet_eta[5])<2.4 && Jet_'+btagAlgo+'[CleanJet_jetIdx[5]]>='+btagWP+'))'
"""
BTAG = 'leadingPtTagged>=20.' 


cuts['VR1_Tag_em']   = OC+' && '+DF+' && ptmiss>=100 && ptmiss<140 && '+BTAG
cuts['VR1_Veto_em']  = OC+' && '+DF+' && ptmiss>=100 && ptmiss<140 && !'+BTAG

cuts['VR1_Tag_sf']   = OC+' && '+SF+' && ptmiss>=100 && ptmiss<140 && '+BTAG
cuts['VR1_Veto_sf']  = OC+' && '+SF+' && ptmiss>=100 && ptmiss<140 && !'+BTAG

cuts['SR1_Tag_em']   = OC+' && '+DF+' && ptmiss>=140 && ptmiss<200 && '+BTAG
cuts['SR1_Veto_em']  = OC+' && '+DF+' && ptmiss>=140 && ptmiss<200 && !'+BTAG

cuts['SR1_Tag_sf']   = OC+' && '+SF+' && ptmiss>=140 && ptmiss<200 && '+BTAG
cuts['SR1_Veto_sf']  = OC+' && '+SF+' && ptmiss>=140 && ptmiss<200 && !'+BTAG

cuts['SR2_Tag_em']   = OC+' && '+DF+' && ptmiss>=200 && ptmiss<300 && '+BTAG
cuts['SR2_Veto_em']  = OC+' && '+DF+' && ptmiss>=200 && ptmiss<300 && !'+BTAG

cuts['SR2_Tag_sf']   = OC+' && '+SF+' && ptmiss>=200 && ptmiss<300 && '+BTAG
cuts['SR2_Veto_sf']  = OC+' && '+SF+' && ptmiss>=200 && ptmiss<300 && !'+BTAG

cuts['SR3_Tag_em']   = OC+' && '+DF+' && ptmiss>=300 && '+BTAG
cuts['SR3_Veto_em']  = OC+' && '+DF+' && ptmiss>=300 && !'+BTAG

cuts['SR3_Tag_sf']   = OC+' && '+SF+' && ptmiss>=300 && '+BTAG
cuts['SR3_Veto_sf']  = OC+' && '+SF+' && ptmiss>=300 && !'+BTAG
