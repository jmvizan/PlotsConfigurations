#

massZ = '91.1876'
vetoZ = 'fabs(mll'+ctrltag+'-'+massZ+')>15.'
Zcut  = 'fabs(mll'+ctrltag+'-'+massZ+')<ZCUT'
SF    = LL+' && '+vetoZ  

NoJets = 'Alt$(CleanJet_pt[0],0)<' +jetPtCut
HasJet = 'Alt$(CleanJet_pt[0],0)>='+jetPtCut
 
if 'Data' in opt.sigset:
    btagWeight1tag = bTagPass
    btagWeight0tag = bTagVeto
    btagWeight2tag = b2TagPass

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

if 'Trigger' in opt.tag:

    OCT = OC.replace('mll>=20. && ', '') 

    cuts['ee_denominator'] = OCT+' && '+EE
    cuts['mm_denominator'] = OCT+' && '+MM  
    cuts['em_denominator'] = OCT+' && '+DF

    if 'MET' in opt.sigset:

        cuts['ee_numerator_double'] = OCT+' && '+EE+' && Trigger_dblEl' 
        cuts['mm_numerator_double'] = OCT+' && '+MM+' && Trigger_dblMu'
        cuts['em_numerator_double'] = OCT+' && '+DF+' && Trigger_ElMu'

        cuts['ee_numerator'] = OCT+' && '+EE+' && (Trigger_dblEl || Trigger_sngEl)'
        cuts['mm_numerator'] = OCT+' && '+MM+' && (Trigger_dblMu || Trigger_sngMu)'
        cuts['em_numerator'] = OCT+' && '+DF+' && (Trigger_ElMu  || Trigger_sngEl || Trigger_sngMu)'  

    else:

        cuts['ee_numerator'] = { 'expr' : OCT+' && '+EE, 'weight' : 'TriggerEffWeight_2l' }
        cuts['mm_numerator'] = { 'expr' : OCT+' && '+MM, 'weight' : 'TriggerEffWeight_2l' }
        cuts['em_numerator'] = { 'expr' : OCT+' && '+DF, 'weight' : 'TriggerEffWeight_2l' }

if 'TwoLeptons' in opt.tag:

    cuts['TwoLep_em'] = OC+' && '+DF
    cuts['TwoLep_ee'] = OC+' && '+EE 
    cuts['TwoLep_mm'] = OC+' && '+MM
    
if 'PV35' in opt.tag:

    cuts['TwoLep_em_PVm35'] = OC+' && '+DF+' && PV_npvs<35'
    cuts['TwoLep_em_PVp35'] = OC+' && '+DF+' && PV_npvs>=35'
    cuts['TwoLep_sf_PVm35'] = OC+' && '+SF+' && PV_npvs<35'
    cuts['TwoLep_sf_PVp35'] = OC+' && '+SF+' && PV_npvs>=35'

if 'Preselection' in opt.tag:

    cuts['TwoLep_em_nometcut'] = OC+' && '+DF
    cuts['TwoLep_ee_nometcut'] = OC+' && '+EE+' && '+vetoZ
    cuts['TwoLep_mm_nometcut'] = OC+' && '+MM+' && '+vetoZ

    cuts['TwoLep_em'] = OC+' && '+DF+' && ptmiss>=80'
    cuts['TwoLep_ee'] = OC+' && '+EE+' && '+vetoZ+' && ptmiss>=80'
    cuts['TwoLep_mm'] = OC+' && '+MM+' && '+vetoZ+' && ptmiss>=80'
    
    cuts['TwoLep_em_Veto'] = { 'expr' : '('+OC+' && '+DF             +')', 'weight' : btagWeight0tag }
    cuts['TwoLep_ee_Veto'] = { 'expr' : '('+OC+' && '+EE+' && '+vetoZ+')', 'weight' : btagWeight0tag }
    cuts['TwoLep_mm_Veto'] = { 'expr' : '('+OC+' && '+MM+' && '+vetoZ+')', 'weight' : btagWeight0tag }
    
    cuts['TwoLep_em_Tag']  = { 'expr' : '('+OC+' && '+DF             +')', 'weight' : btagWeight1tag }
    cuts['TwoLep_ee_Tag']  = { 'expr' : '('+OC+' && '+EE+' && '+vetoZ+')', 'weight' : btagWeight1tag }
    cuts['TwoLep_mm_Tag']  = { 'expr' : '('+OC+' && '+MM+' && '+vetoZ+')', 'weight' : btagWeight1tag }

if 'METFix' in opt.tag:
    
    cuts['METFixEE_low_em_Veto'] = { 'expr' : '('+OC+' && '+DF             +')', 'weight' : btagWeight0tag }
    cuts['METFixEE_low_ee_Veto'] = { 'expr' : '('+OC+' && '+EE+' && '+vetoZ+')', 'weight' : btagWeight0tag }
    cuts['METFixEE_low_mm_Veto'] = { 'expr' : '('+OC+' && '+MM+' && '+vetoZ+')', 'weight' : btagWeight0tag }
    cuts['METFixEE_low_sf_Veto'] = { 'expr' : '('+OC+' && '+SF+' && '+vetoZ+')', 'weight' : btagWeight0tag }
    
    cuts['METFixEE_low_em_Tag']  = { 'expr' : '('+OC+' && '+DF             +')', 'weight' : btagWeight1tag }
    cuts['METFixEE_low_ee_Tag']  = { 'expr' : '('+OC+' && '+EE+' && '+vetoZ+')', 'weight' : btagWeight1tag }
    cuts['METFixEE_low_mm_Tag']  = { 'expr' : '('+OC+' && '+MM+' && '+vetoZ+')', 'weight' : btagWeight1tag }
    cuts['METFixEE_low_sf_Tag']  = { 'expr' : '('+OC+' && '+SF+' && '+vetoZ+')', 'weight' : btagWeight1tag }
    
    cuts['METFixEE_high_em_Veto'] = { 'expr' : '('+OC+' && '+DF             +' && ptmiss>=100 && ptmiss<140)', 'weight' : btagWeight0tag }
    cuts['METFixEE_high_ee_Veto'] = { 'expr' : '('+OC+' && '+EE+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140)', 'weight' : btagWeight0tag }
    cuts['METFixEE_high_mm_Veto'] = { 'expr' : '('+OC+' && '+MM+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140)', 'weight' : btagWeight0tag }
    cuts['METFixEE_high_sf_Veto'] = { 'expr' : '('+OC+' && '+SF+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140)', 'weight' : btagWeight0tag }
    
    cuts['METFixEE_high_em_Tag']  = { 'expr' : '('+OC+' && '+DF             +' && ptmiss>=100 && ptmiss<140)', 'weight' : btagWeight1tag }
    cuts['METFixEE_high_ee_Tag']  = { 'expr' : '('+OC+' && '+EE+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140)', 'weight' : btagWeight1tag }
    cuts['METFixEE_high_mm_Tag']  = { 'expr' : '('+OC+' && '+MM+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140)', 'weight' : btagWeight1tag }
    cuts['METFixEE_high_sf_Tag']  = { 'expr' : '('+OC+' && '+SF+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140)', 'weight' : btagWeight1tag }
    
if 'VetoNoiseEE' in opt.tag and not 'More' in opt.tag:

    channelCut = OC 
    if 'Zveto' in opt.tag:
        channelCut += ' && ('+DF+' || '+SF+')'
 
    EENoiseVeto0 = '(Sum$(abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139)>=1)'
    EENoiseVeto1 = '(Sum$(Jet_pt*(1.-Jet_rawFactor)<50. && abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139)>=1)'
    EENoiseVeto2 = '(Sum$(Jet_pt*(1.-Jet_rawFactor)<50. && Jet_pt>30. && abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139)>=1)'
    
    ptm = ' ptmiss>=100. && ptmiss<140 '
    if 'MET' in opt.tag: 
        ptm = ' && MET_pt>=100 && MET_pt<140 '

    if 'Zpeak' not in opt.tag:      
        cuts['Veto0_Tag']             = { 'expr' : '('+channelCut+' && '+EENoiseVeto0+')', 'weight' : btagWeight1tag }
        cuts['Veto0_Tag_highptmiss']  = { 'expr' : '('+channelCut+' && '+EENoiseVeto0+' && '+ptm+')', 'weight' : btagWeight1tag }
        cuts['Veto1_Tag']             = { 'expr' : '('+channelCut+' && '+EENoiseVeto1+')', 'weight' : btagWeight1tag }
        cuts['Veto1_Tag_highptmiss']  = { 'expr' : '('+channelCut+' && '+EENoiseVeto1+' && '+ptm+')', 'weight' : btagWeight1tag }
        cuts['Veto2_Tag']             = { 'expr' : '('+channelCut+' && '+EENoiseVeto2+')', 'weight' : btagWeight1tag }
        cuts['Veto2_Tag_highptmiss']  = { 'expr' : '('+channelCut+' && '+EENoiseVeto2+' && '+ptm+')', 'weight' : btagWeight1tag }
        cuts['Veto0_Veto']            = { 'expr' : '('+channelCut+' && '+EENoiseVeto0+')', 'weight' : btagWeight0tag }
        cuts['Veto0_Veto_highptmiss'] = { 'expr' : '('+channelCut+' && '+EENoiseVeto0+' && '+ptm+')', 'weight' : btagWeight0tag }
        cuts['Veto1_Veto']            = { 'expr' : '('+channelCut+' && '+EENoiseVeto1+')', 'weight' : btagWeight0tag }
        cuts['Veto1_Veto_highptmiss'] = { 'expr' : '('+channelCut+' && '+EENoiseVeto1+' && '+ptm+')', 'weight' : btagWeight0tag }
        cuts['Veto2_Veto']            = { 'expr' : '('+channelCut+' && '+EENoiseVeto2+')', 'weight' : btagWeight0tag }
        cuts['Veto2_Veto_highptmiss'] = { 'expr' : '('+channelCut+' && '+EENoiseVeto2+' && '+ptm+')', 'weight' : btagWeight0tag }
    elif 'ZpeakValid' in opt.tag:
        cuts['Veto0_Valid_Zpeak'] = { 'expr' : '('+OC+' && '+LL+' && '+Zcut.replace('ZCUT',  '15.')+' && '+EENoiseVeto0+' && '+ptm+')', 'weight' : btagWeight0tag }
        cuts['Veto1_Valid_Zpeak'] = { 'expr' : '('+OC+' && '+LL+' && '+Zcut.replace('ZCUT',  '15.')+' && '+EENoiseVeto1+' && '+ptm+')', 'weight' : btagWeight0tag }
        cuts['Veto2_Valid_Zpeak'] = { 'expr' : '('+OC+' && '+LL+' && '+Zcut.replace('ZCUT',  '15.')+' && '+EENoiseVeto2+' && '+ptm+')', 'weight' : btagWeight0tag }
    if 'HTF' in opt.tag:
        cuts['Veto0_Tag_HTF']             = { 'expr' : '('+OC+' && '+EENoiseVeto0+' && ' + HTForward + '>=60.'+')', 'weight' : btagWeight1tag }
        cuts['Veto0_Tag_highptmiss_HTF']  = { 'expr' : '('+OC+' && '+EENoiseVeto0+' && '+ptm+' && ' + HTForward + '>=60.'+')', 'weight' : btagWeight1tag }
        cuts['Veto1_Tag_HTF']             = { 'expr' : '('+OC+' && '+EENoiseVeto1+' && ' + HTForward + '>=60.' +')', 'weight' : btagWeight1tag }
        cuts['Veto1_Tag_highptmiss_HTF']  = { 'expr' : '('+OC+' && '+EENoiseVeto1+' && '+ptm+' && ' + HTForward + '>=60.'+')', 'weight' : btagWeight1tag }
        cuts['Veto2_Tag_HTF']             = { 'expr' : '('+OC+' && '+EENoiseVeto2+' && ' + HTForward + '>=60.'+')', 'weight' : btagWeight1tag }
        cuts['Veto2_Tag_highptmiss_HTF']  = { 'expr' : '('+OC+' && '+EENoiseVeto2+' && '+ptm+' && ' + HTForward + '>=60.'+')', 'weight' : btagWeight1tag }
        cuts['Veto0_Veto_HTF']            = { 'expr' : '('+OC+' && '+EENoiseVeto0+' && ' + HTForward + '>=60.'+')', 'weight' : btagWeight0tag }
        cuts['Veto0_Veto_highptmiss_HTF'] = { 'expr' : '('+OC+' && '+EENoiseVeto0+' && '+ptm+' && ' + HTForward + '>=60.'+')', 'weight' : btagWeight0tag }
        cuts['Veto1_Veto_HTF']            = { 'expr' : '('+OC+' && '+EENoiseVeto1+' && ' + HTForward + '>=60.'+')', 'weight' : btagWeight0tag }
        cuts['Veto1_Veto_highptmiss_HTF'] = { 'expr' : '('+OC+' && '+EENoiseVeto1+' && '+ptm+' && ' + HTForward + '>=60.'+')', 'weight' : btagWeight0tag }
        cuts['Veto2_Veto_HTF']            = { 'expr' : '('+OC+' && '+EENoiseVeto2+' && ' + HTForward + '>=60.'+')', 'weight' : btagWeight0tag }
        cuts['Veto2_Veto_highptmiss_HTF'] = { 'expr' : '('+OC+' && '+EENoiseVeto2+' && '+ptm+' && ' + HTForward + '>=60.'+')', 'weight' : btagWeight0tag }

if 'DYchecks' in opt.tag:

    if 'nojets' in opt.tag:
        cuts['lowMll_sf_nojetcut']  = OC + ' && ' + LL + ' && PuppiMET_pt> 50' 
        cuts['lowMll_ee_nojetcut']  = OC + ' && ' + EE + ' && PuppiMET_pt> 50 '  
        cuts['lowMll_mm_nojetcut']  = OC + ' && ' + MM + ' && PuppiMET_pt> 50 '   
        cuts['highMll_sf_nojetcut'] = OC + ' && ' + LL + ' && PuppiMET_pt> 50 && mll>=76 && mll<106'
        cuts['highMll_ee_nojetcut'] = OC + ' && ' + EE + ' && PuppiMET_pt> 50 && mll>=76 && mll<106'
        cuts['highMll_mm_nojetcut'] = OC + ' && ' + MM + ' && PuppiMET_pt> 50 && mll>=76 && mll<106' 
        cuts['lowMll_sf_noMETcut_nojetcut']  = OC + ' && ' + LL   
        cuts['lowMll_ee_noMETcut_nojetcut']  = OC + ' && ' + EE   
        cuts['lowMll_mm_noMETcut_nojetcut']  = OC + ' && ' + MM    
        cuts['highMll_sf_noMETcut_nojetcut'] = OC + ' && ' + LL + ' && mll>=76 && mll<106'
        cuts['highMll_ee_noMETcut_nojetcut'] = OC + ' && ' + EE + ' && mll>=76 && mll<106' 
        cuts['highMll_mm_noMETcut_nojetcut'] = OC + ' && ' + MM + ' && mll>=76 && mll<106'
        
    else: 
        cuts['lowMll_sf']  = { 'expr' : '(' + OC + ' && ' + LL + ' && Alt$(CleanJet_pt[1],0)>=30.)', 'weight' : btagWeight1tag }
        cuts['lowMll_ee']  = { 'expr' : '(' + OC + ' && ' + EE + ' && Alt$(CleanJet_pt[1],0)>=30. && PuppiMET_pt> 50)', 'weight' : btagWeight1tag }
        cuts['lowMll_mm']  = { 'expr' : '(' + OC + ' && ' + MM + ' && Alt$(CleanJet_pt[1],0)>=30. && PuppiMET_pt> 50)', 'weight' : btagWeight1tag }
        cuts['highMll_sf'] = { 'expr' : '(' + OC + ' && ' + LL + ' && Alt$(CleanJet_pt[1],0)>=30. && mll>=76 && mll<106)', 'weight' : btagWeight1tag }
        cuts['highMll_ee'] = { 'expr' : '(' + OC + ' && ' + EE + ' && Alt$(CleanJet_pt[1],0)>=30. && PuppiMET_pt> 50 &&  mll>=76 && mll<106)', 'weight' : btagWeight1tag }
        cuts['highMll_mm'] = { 'expr' : '(' + OC + ' && ' + MM + ' && Alt$(CleanJet_pt[1],0)>=30. &&  PuppiMET_pt> 50 && mll>=76 && mll<106)', 'weight' : btagWeight1tag }
        cuts['lowMll_ee_noMETcut']  = { 'expr' : '(' + OC + ' && ' + EE + ' && Alt$(CleanJet_pt[1],0)>=30.)', 'weight' : btagWeight1tag }
        cuts['lowMll_mm_noMETcut']  = { 'expr' : '(' + OC + ' && ' + MM + ' && Alt$(CleanJet_pt[1],0)>=30.)', 'weight' : btagWeight1tag }
        cuts['highMll_ee_noMETcut'] = { 'expr' : '(' + OC + ' && ' + EE + ' && Alt$(CleanJet_pt[1],0)>=30. &&  mll>=76 && mll<106)', 'weight' : btagWeight1tag }
        cuts['highMll_mm_noMETcut'] = { 'expr' : '(' + OC + ' && ' + MM + ' && Alt$(CleanJet_pt[1],0)>=30. &&  mll>=76 && mll<106)', 'weight' : btagWeight1tag }
        
if 'TopControlRegion' in opt.tag:

    cuts['Top_em'] = { 'expr' : '(' + OC+' && '+DF+' && ptmiss>=20)', 'weight' : btagWeight1tag }
    cuts['Top_ee'] = { 'expr' : '(' + OC+' && '+EE+' && '+vetoZ+' && ptmiss>=50)', 'weight' : btagWeight1tag }
    cuts['Top_mm'] = { 'expr' : '(' + OC+' && '+MM+' && '+vetoZ+' && ptmiss>=50)', 'weight' : btagWeight1tag }
    cuts['Top_cr'] = { 'expr' : '(' + OC+' && (('+DF+') || ('+SF+'))  && ptmiss>=50  && CleanJet_pt[1]>=30.)', 'weight' : btagWeight1tag }
    cuts['Top_hm'] = { 'expr' : '(' + OC+' && (('+DF+') || ('+SF+'))  && MET_significance>12  && CleanJet_pt[1]>=30. && '+dPhijet0ptmiss+'>0.64 && '+dPhijet1ptmiss+'>0.25)', 'weight' : btagWeight1tag }

if 'HMControlRegion' in opt.tag:

    cuts['Top_em'] = { 'expr' : '(' + OC+' && '+DF+' && MET_significance>12  && CleanJet_pt[1]>=30. && '+dPhijet0ptmiss+'>0.64 && '+dPhijet1ptmiss+'>0.25)', 'weight' : btagWeight1tag }
    cuts['Top_sf'] = { 'expr' : '(' + OC+' && '+SF+' && MET_significance>12  && CleanJet_pt[1]>=30. && '+dPhijet0ptmiss+'>0.64 && '+dPhijet1ptmiss+'>0.25)', 'weight' : btagWeight1tag }
    cuts['Top_hm'] = { 'expr' : '(' + OC+' && (('+DF+') || ('+SF+'))  && MET_significance>12  && CleanJet_pt[1]>=30. && '+dPhijet0ptmiss+'>0.64 && '+dPhijet1ptmiss+'>0.25)', 'weight' : btagWeight1tag }
    
if 'WWControlRegion' in opt.tag:

    cuts['WW_metcut']   = '(' + OC+' && '+DF+' && '+NoJets+' && ptmiss>=70)'
    cuts['WW_nometcut'] = '(' + OC+' && '+DF+' && '+NoJets+')'

if 'DYControlRegion' in opt.tag:

    DY = OC+' && '+LL+' && '+Zcut.replace('ZCUT',  '15.')
    
    cuts['DY_ee']     = { 'expr' : '(' + DY+' && '+EE+')', 'weight' : btagWeight0tag }
    cuts['DY_mm']     = { 'expr' : '(' + DY+' && '+MM+')', 'weight' : btagWeight0tag }
    cuts['DY_ee_jet'] = { 'expr' : '(' + DY+' && '+EE+' && '+NoJets+')', 'weight' : btagWeight0tag }
    cuts['DY_mm_jet'] = { 'expr' : '(' + DY+' && '+MM+' && '+NoJets+')', 'weight' : btagWeight0tag }

if 'DYtauControlRegion' in opt.tag:

    DYtau = OC+' && '+DF+' && '+Zcut.replace('ZCUT',  '15.')

    cuts['DY_em']     = { 'expr' : '(' + DYtau+')', 'weight' : btagWeight0tag }
    cuts['DY_em_jet'] = { 'expr' : '(' + DYtau+' && '+NoJets+')', 'weight' : btagWeight0tag }

if 'DYDarkMatterControlRegion' in opt.tag:

    DY = OC+' && '+LL+' && '+Zcut.replace('ZCUT',  '15.')

    cuts['DY_ee_puppi'] = '(' + DY+' && '+EE+') && Alt$(CleanJet_pt[1],0)>=30. && PuppiMET_pt>=50.'
    cuts['DY_mm_puppi'] = '(' + DY+' && '+MM+') && Alt$(CleanJet_pt[1],0)>=30. && PuppiMET_pt>=50.'
    cuts['DY_ee_pfmet'] = '(' + DY+' && '+EE+') && Alt$(CleanJet_pt[1],0)>=30. && ptmiss>=50.'
    cuts['DY_mm_pfmet'] = '(' + DY+' && '+MM+') && Alt$(CleanJet_pt[1],0)>=30. && ptmiss>=50.'

if 'HighPtMissControlRegion' in opt.tag or 'HighPtMissValidationRegion' in opt.tag:

    cuts['VR1_Tag_em']   = { 'expr' : OC+' && '+DF+' && ptmiss>=100 && ptmiss<140', 'weight' : btagWeight1tag }
    cuts['VR1_Veto_em']  = { 'expr' : OC+' && '+DF+' && ptmiss>=100 && ptmiss<140', 'weight' : btagWeight0tag }
    cuts['VR1_Tag_sf']   = { 'expr' : OC+' && '+SF+' && ptmiss>=100 && ptmiss<140', 'weight' : btagWeight1tag }
    cuts['VR1_Veto_sf']  = { 'expr' : OC+' && '+SF+' && ptmiss>=100 && ptmiss<140', 'weight' : btagWeight0tag }

    cuts['VR1_NoTag_em']  = { 'expr' : OC+' && '+DF+' && ptmiss>=100 && ptmiss<140 && '+HasJet, 'weight' : btagWeight0tag }
    cuts['VR1_NoTag_sf']  = { 'expr' : OC+' && '+SF+' && ptmiss>=100 && ptmiss<140 && '+HasJet, 'weight' : btagWeight0tag }
    cuts['VR1_NoJet_em']  = { 'expr' : OC+' && '+DF+' && ptmiss>=100 && ptmiss<140 && '+NoJets, 'weight' : btagWeight0tag }
    cuts['VR1_NoJet_sf']  = { 'expr' : OC+' && '+SF+' && ptmiss>=100 && ptmiss<140 && '+NoJets, 'weight' : btagWeight0tag }

if 'JetSelectionRegions' in opt.tag: # To optimize jet selections 

    cuts['VR1_Veto_em']  = { 'expr' : OC+' && '+DF+' && ptmiss>=100 && ptmiss<140', 'weight' : btagWeight0tag }
    cuts['VR1_Veto_sf']  = { 'expr' : OC+' && '+SF+' && ptmiss>=100 && ptmiss<140', 'weight' : btagWeight0tag }
    cuts['SR1_Veto_em']  = { 'expr' : OC+' && '+DF+' && ptmiss>=140 && ptmiss<220', 'weight' : btagWeight0tag }
    cuts['SR1_Veto_sf']  = { 'expr' : OC+' && '+SF+' && ptmiss>=140 && ptmiss<220', 'weight' : btagWeight0tag }
    cuts['SR2_Veto_em']  = { 'expr' : OC+' && '+DF+' && ptmiss>=220 && ptmiss<280', 'weight' : btagWeight0tag }
    cuts['SR2_Veto_sf']  = { 'expr' : OC+' && '+SF+' && ptmiss>=220 && ptmiss<280', 'weight' : btagWeight0tag }
    cuts['SR3_Veto_em']  = { 'expr' : OC+' && '+DF+' && ptmiss>=280 && ptmiss<380', 'weight' : btagWeight0tag }
    cuts['SR3_Veto_sf']  = { 'expr' : OC+' && '+SF+' && ptmiss>=280 && ptmiss<380', 'weight' : btagWeight0tag }
    cuts['SR4_Veto_em']  = { 'expr' : OC+' && '+DF+' && ptmiss>=380',               'weight' : btagWeight0tag }
    cuts['SR4_Veto_sf']  = { 'expr' : OC+' && '+SF+' && ptmiss>=380',               'weight' : btagWeight0tag }

if 'LatinoControlRegion' in opt.tag:

    cuts['Top_em'] = { 'expr' : '('+OC+' && '+DF+' && ptmiss>=20 && mll<76 && '          +pTll+'>30 && '+dRll+'<2.5 && '+mTllptmiss+'>40)', 'weight' : btagWeight1tag }
    cuts['WW_em']  = { 'expr' : '('+OC+' && '+DF+' && ptmiss>=20 && mll>76 && '          +pTll+'>30 && '+dRll+'<2.5 && '+mTllptmiss+'>40)', 'weight' : btagWeight0tag }
    cuts['Top_sf'] = { 'expr' : '('+OC+' && '+SF+' && ptmiss>=50 && mll>25 && mll<76 && '+pTll+'>30 && '+dRll+'<2.5 && '+mTllptmiss+'>40)', 'weight' : btagWeight1tag }
    cuts['DY_sf']  = { 'expr' : '('+OC+' && '+LL+' && ptmiss>=50 && '+Zcut.replace('ZCUT','15')+'&& '+pTll+'>30 && '+dRll+'<2.5 && '+mTllptmiss+'>40)', 'weight' : btagWeight0tag }

if 'HighPtMissOptimisationRegion' in opt.tag:

    cuts['VR1_Tag_em']   = { 'expr' : '(' + OC+' && '+DF+' && ptmiss>=100)', 'weight' : btagWeight1tag }
    cuts['VR1_Veto_em']  = { 'expr' : '(' + OC+' && '+DF+' && ptmiss>=100)', 'weight' : btagWeight0tag }
    cuts['VR1_Tag_sf']   = { 'expr' : '(' + OC+' && '+SF+' && ptmiss>=100)', 'weight' : btagWeight1tag }
    cuts['VR1_Veto_sf']  = { 'expr' : '(' + OC+' && '+SF+' && ptmiss>=100)', 'weight' : btagWeight0tag }

if 'TopValidationRegion' in opt.tag:

    cuts['VR1_Tag_em']        = { 'expr' : '(' + OC+' && '+DF+             ' && ptmiss>=100 && ptmiss<140)', 'weight' : btagWeight1tag }
    cuts['VR1_Tag_sf']        = { 'expr' : '(' + OC+' && '+SF+             ' && ptmiss>=100 && ptmiss<140)', 'weight' : btagWeight1tag }
    cuts['VR1_Tag_mm']        = { 'expr' : '(' + OC+' && '+MM+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140)', 'weight' : btagWeight1tag }
    cuts['VR1_Tag_ee']        = { 'expr' : '(' + OC+' && '+EE+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140)', 'weight' : btagWeight1tag }
    cuts['VR1_Tag_em_jets']   = { 'expr' : '(' + OC+' && '+DF+             ' && ptmiss>=100 && ptmiss<140 && CleanJet_pt[1]>=30.)', 'weight' : btagWeight1tag }
    cuts['VR1_Tag_sf_jets']   = { 'expr' : '(' + OC+' && '+SF+             ' && ptmiss>=100 && ptmiss<140 && CleanJet_pt[1]>=30.)', 'weight' : btagWeight1tag }
    cuts['VR1_Tag_mm_jets']   = { 'expr' : '(' + OC+' && '+MM+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140 && CleanJet_pt[1]>=30.)', 'weight' : btagWeight1tag }
    cuts['VR1_Tag_ee_jets']   = { 'expr' : '(' + OC+' && '+EE+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140 && CleanJet_pt[1]>=30.)', 'weight' : btagWeight1tag }
    if 'More' in opt.tag:
        cuts['VR1_Tag_em_mt2']    = { 'expr' : '(' + OC+' && '+DF+             ' && ptmiss>=100 && ptmiss<140 && mt2ll>100.         )', 'weight' : btagWeight1tag }
        cuts['VR1_Tag_mm_mt2']    = { 'expr' : '(' + OC+' && '+MM+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140 && mt2ll>100.         )', 'weight' : btagWeight1tag }
        cuts['VR1_Tag_ee_mt2']    = { 'expr' : '(' + OC+' && '+EE+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140 && mt2ll>100.         )', 'weight' : btagWeight1tag }
        cuts['VR1_Tag_jets']      = { 'expr' : '(' + OC+' && ('+SF+' || '+DF+')  && ptmiss>=100 && ptmiss<140 && CleanJet_pt[1]>=30.)', 'weight' : btagWeight1tag }
        
if 'WWValidationRegion' in opt.tag and 'WZtoWWValidationRegion' not in opt.tag:

    cuts['VR1_Veto_em']        = { 'expr' : '(' + OC+' && '+DF+             ' && ptmiss>=100 && ptmiss<140)', 'weight' : btagWeight0tag }
    cuts['VR1_Veto_sf']        = { 'expr' : '(' + OC+' && '+SF+             ' && ptmiss>=100 && ptmiss<140)', 'weight' : btagWeight0tag }
    cuts['VR1_Veto_mm']        = { 'expr' : '(' + OC+' && '+MM+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140)', 'weight' : btagWeight0tag }
    cuts['VR1_Veto_ee']        = { 'expr' : '(' + OC+' && '+EE+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140)', 'weight' : btagWeight0tag }
    cuts['VR1_Veto_em_0jet']   = '(' + OC+' && '+DF+             ' && ptmiss>=100 && ptmiss<140 && '+NoJets+')'
    cuts['VR1_Veto_sf_0jet']   = '(' + OC+' && '+SF+             ' && ptmiss>=100 && ptmiss<140 && '+NoJets+')'
    cuts['VR1_Veto_mm_0jet']   = '(' + OC+' && '+MM+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140 && '+NoJets+')'
    cuts['VR1_Veto_ee_0jet']   = '(' + OC+' && '+EE+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140 && '+NoJets+')'
    if 'More' in opt.tag:
        cuts['VR1_Veto_em_mt2']    = '(' + OC+' && '+DF+             ' && ptmiss>=100 && ptmiss<140 && mt2ll>100.)'
        cuts['VR1_Veto_mm_mt2']    = '(' + OC+' && '+MM+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140 && mt2ll>100.)'
        cuts['VR1_Veto_ee_mt2']    = '(' + OC+' && '+EE+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140 && mt2ll>100.)'
        cuts['VR1_Veto_0jet']      = '(' + OC+' && ('+SF+' || '+DF+')  && ptmiss>=100 && ptmiss<140 && '+NoJets+')'

if 'SameSignValidationRegion' in opt.tag:

    cuts['SS_ptmiss']            = { 'expr' : '('+SSM+' && ptmiss'+ctrltag+'>=0  )', 'weight' : btagWeight1tag }
    cuts['SS_ptmiss_100to140']   = { 'expr' : '('+SS +' && ptmiss'+ctrltag+'>=100 && ptmiss'+ctrltag+'<140)', 'weight' : btagWeight1tag }
    cuts['SS_ptmiss_140']        = { 'expr' : '('+SS +' && ptmiss'+ctrltag+'>=140)', 'weight' : btagWeight1tag }
    cuts['SS_ptmiss_160']        = { 'expr' : '('+SS +' && ptmiss'+ctrltag+'>=160)', 'weight' : btagWeight1tag }
    cuts['SS_ptmiss_160_plus']   = { 'expr' : '('+SSP+' && ptmiss'+ctrltag+'>=160)', 'weight' : btagWeight1tag }
    cuts['SS_ptmiss_160_minus']  = { 'expr' : '('+SSM+' && ptmiss'+ctrltag+'>=160)', 'weight' : btagWeight1tag }

if 'FakeValidationRegion' in opt.tag:
    
    Fake = LepId2of3 + ' && ' + OCT

    cuts['Fake']                   = { 'expr' : '('+Fake+' && ptmiss'+ctrltag+'>=0  )', 'weight' : btagWeight1tag }
    cuts['Fake_ptmiss_100to140']   = { 'expr' : '('+Fake+' && ptmiss'+ctrltag+'>=100 && ptmiss'+ctrltag+'<140)', 'weight' : btagWeight1tag }
    cuts['Fake_ptmiss_140']        = { 'expr' : '('+Fake+' && ptmiss'+ctrltag+'>=140)', 'weight' : btagWeight1tag }
    cuts['Fake_ptmiss_160']        = { 'expr' : '('+Fake+' && ptmiss'+ctrltag+'>=160)', 'weight' : btagWeight1tag }

if 'WZValidationRegion' in opt.tag or 'WZtoWWValidationRegion' in opt.tag:

    WZselection = nLooseLepton+'==3 && ' + nTightLepton + '==3 && deltaMassZ'+ctrltag+'<ZCUT && ptmiss'+ctrltag+'>=METCUT'

    if 'WZValidationRegion' in opt.tag:

        cuts['WZ_3Lep']             = { 'expr' : '(' + WZselection.replace('ZCUT', '999.').replace('METCUT',   '0') + ')', 'weight' : btagWeight0tag }
        cuts['WZ_3LepZ']            = { 'expr' : '(' + WZselection.replace('ZCUT',  '15.').replace('METCUT',   '0') + ')', 'weight' : btagWeight0tag }
        cuts['WZ_3Lep_ptmiss-140']  = { 'expr' : '(' + WZselection.replace('ZCUT', '999.').replace('METCUT', '140') + ')', 'weight' : btagWeight0tag }
        cuts['WZ_3LepZ_ptmiss-140'] = { 'expr' : '(' + WZselection.replace('ZCUT',  '15.').replace('METCUT', '140') + ')', 'weight' : btagWeight0tag }
        cuts['WZ_3Lep_ptmiss-160']  = { 'expr' : '(' + WZselection.replace('ZCUT', '999.').replace('METCUT', '160') + ')', 'weight' : btagWeight0tag }
        cuts['WZ_3LepZ_ptmiss-160'] = { 'expr' : '(' + WZselection.replace('ZCUT',  '15.').replace('METCUT', '160') + ')', 'weight' : btagWeight0tag }

    elif 'WZtoWWValidationRegion' in opt.tag:

        cuts['WZtoWW_Zcut10']            = { 'expr' : '('+WZselection.replace('ZCUT','10.').replace('METCUT',  '0')+')', 'weight' : btagWeight0tag }
        cuts['WZtoWW_Zcut15']            = { 'expr' : '('+WZselection.replace('ZCUT','15.').replace('METCUT',  '0')+')', 'weight' : btagWeight0tag }
        cuts['WZtoWW_Zcut10_ptmiss-140'] = { 'expr' : '('+WZselection.replace('ZCUT','10.').replace('METCUT','140')+')', 'weight' : btagWeight0tag }
        cuts['WZtoWW_Zcut15_ptmiss-140'] = { 'expr' : '('+WZselection.replace('ZCUT','15.').replace('METCUT','140')+')', 'weight' : btagWeight0tag }
        cuts['WZtoWW_Zcut10_ptmiss-160'] = { 'expr' : '('+WZselection.replace('ZCUT','10.').replace('METCUT','160')+')', 'weight' : btagWeight0tag }
        cuts['WZtoWW_Zcut15_ptmiss-160'] = { 'expr' : '('+WZselection.replace('ZCUT','15.').replace('METCUT','160')+')', 'weight' : btagWeight0tag }

if 'ttZValidationRegion' in opt.tag or 'ZZValidationRegion' in opt.tag:

    sel4Lep = nLooseLepton+'==4 && ' + nTightLepton + '>=3'

    if 'ttZValidationRegion' in opt.tag:

        ttZselection = sel4Lep + ' && deltaMassZ'+ctrltag+'<10. && ptmiss'+ctrltag+'>=METCUT && nCleanJet>=2 && CleanJet_pt[1]>='+jetPtCut

        cuts['ttZ']            = { 'expr' : '(' + ttZselection.replace('METCUT',   '0') + ')', 'weight' : btagWeight1tag }
        cuts['ttZ_ptmiss-140'] = { 'expr' : '(' + ttZselection.replace('METCUT', '140') + ')', 'weight' : btagWeight1tag }
        cuts['ttZ_ptmiss-160'] = { 'expr' : '(' + ttZselection.replace('METCUT', '160') + ')', 'weight' : btagWeight1tag }

    elif 'ZZValidationRegion' in opt.tag:

        ZZselection = sel4Lep + ' && deltaMassZ'+ctrltag+'<15. && ptmiss'+ctrltag+'>=METCUT'

        cuts['ZZ']            = { 'expr' : '(' + ZZselection.replace('METCUT',   '0') + ')', 'weight' : btagWeight0tag }
        cuts['ZZ_ptmiss-140'] = { 'expr' : '(' + ZZselection.replace('METCUT', '140') + ')', 'weight' : btagWeight0tag }
        cuts['ZZ_ptmiss-160'] = { 'expr' : '(' + ZZselection.replace('METCUT', '160') + ')', 'weight' : btagWeight0tag }

if 'ttZNormalization' in opt.tag or 'FitCRttZ' in opt.tag:

    ttZcommon = 'deltaMassZ_ctrltag<10. && deltaMassZ_ctrltag>=0. && ptmiss_ctrltag>=0.'
    if 'Z15' in opt.tag:
        ttZcommon = ttZcommon.replace('deltaMassZ_ctrltag<10.', 'deltaMassZ_ctrltag<15.')
    ttZ3Lep = nLooseLepton+'==3 && '+ttZcommon.replace('_ctrltag', '_WZtoWW' )
    ttZ4Lep = nLooseLepton+'==4 && '+ttZcommon.replace('_ctrltag', '_ttZ')
    ptmissTTZ3Lep = ptmissNano
    ptmissTTZ4Lep = ptmissNano
    if 'AddZ' in opt.tag:
        ptmissTTZ3Lep = ptmiss_ttZ3Lep 
        ptmissTTZ4Lep = 'ptmiss_ttZ'
    if 'FitCRttZ' not in opt.tag:
        ttZ3Lep += ' && '+ptmissTTZ3Lep+'>=METCUT'
        ttZ4Lep += ' && '+ptmissTTZ4Lep+'>=METCUT'
    ttZselectionLoose = nTightLepton+'>=3 && (('+ ttZ3Lep + ') || (' + ttZ4Lep + ')) && nCleanJet>=2 && Alt$(CleanJet_pt[1],0)>='+jetPtCut   
    btagweightmixtag = '(('+btagWeight2tag+')*('+nLooseLepton+'==3) + ('+btagWeight1tag+')*('+nLooseLepton+'==4))'

    if 'ttZNormalization' in opt.tag:

        #cuts['ttZ_3Lep_loose']                = { 'expr' : '(' + ttZ3Lep.replace('METCUT', '0') + ')' }
        #cuts['ttZ_3Lep_loose1tag']            = { 'expr' : '(' + ttZ3Lep.replace('METCUT', '0') + ')',   'weight' : btagWeight1tag }
        #cuts['ttZ_3Lep_loose2tag']            = { 'expr' : '(' + ttZ3Lep.replace('METCUT', '0') + ')',   'weight' : btagWeight2tag }
        #cuts['ttZ_3Lep_ptmiss-100_loose']     = { 'expr' : '(' + ttZ3Lep.replace('METCUT', '100') + ')' }  
        #cuts['ttZ_3Lep_ptmiss-100_loose1tag'] = { 'expr' : '(' + ttZ3Lep.replace('METCUT', '100') + ')', 'weight' : btagWeight1tag }
        #cuts['ttZ_3Lep_ptmiss-100_loose2tag'] = { 'expr' : '(' + ttZ3Lep.replace('METCUT', '100') + ')', 'weight' : btagWeight2tag }
        #cuts['ttZ_3Lep_ptmiss-160_loose']     = { 'expr' : '(' + ttZ3Lep.replace('METCUT', '160') + ')' }  
        #cuts['ttZ_3Lep_ptmiss-160_loose1tag'] = { 'expr' : '(' + ttZ3Lep.replace('METCUT', '160') + ')', 'weight' : btagWeight1tag }
        #cuts['ttZ_3Lep_ptmiss-160_loose2tag'] = { 'expr' : '(' + ttZ3Lep.replace('METCUT', '160') + ')', 'weight' : btagWeight2tag }

        #cuts['ttZ_4Lep_loose']                = { 'expr' : '(' + ttZ4Lep.replace('METCUT', '0') + ')' }  
        #cuts['ttZ_4Lep_loose1tag']            = { 'expr' : '(' + ttZ4Lep.replace('METCUT', '0') + ')',   'weight' : btagWeight1tag }
        #cuts['ttZ_4Lep_loose2tag']            = { 'expr' : '(' + ttZ4Lep.replace('METCUT', '0') + ')',   'weight' : btagWeight2tag }
        #cuts['ttZ_4Lep_ptmiss-100_loose']     = { 'expr' : '(' + ttZ4Lep.replace('METCUT', '100') + ')' }
        #cuts['ttZ_4Lep_ptmiss-100_loose1tag'] = { 'expr' : '(' + ttZ4Lep.replace('METCUT', '100') + ')', 'weight' : btagWeight1tag }
        #cuts['ttZ_4Lep_ptmiss-100_loose2tag'] = { 'expr' : '(' + ttZ4Lep.replace('METCUT', '100') + ')', 'weight' : btagWeight2tag }
        #cuts['ttZ_4Lep_ptmiss-160_loose']     = { 'expr' : '(' + ttZ4Lep.replace('METCUT', '160') + ')' }
        #cuts['ttZ_4Lep_ptmiss-160_loose1tag'] = { 'expr' : '(' + ttZ4Lep.replace('METCUT', '160') + ')', 'weight' : btagWeight1tag }
        #cuts['ttZ_4Lep_ptmiss-160_loose2tag'] = { 'expr' : '(' + ttZ4Lep.replace('METCUT', '160') + ')', 'weight' : btagWeight2tag }

        #cuts['ttZ_loose']                = { 'expr' : '(' + ttZselectionLoose.replace('METCUT', '0') + ')' } 
        #cuts['ttZ_loose1tag']            = { 'expr' : '(' + ttZselectionLoose.replace('METCUT', '0') + ')',   'weight' : btagWeight1tag }
        #cuts['ttZ_loose2tag']            = { 'expr' : '(' + ttZselectionLoose.replace('METCUT', '0') + ')',   'weight' : btagWeight2tag }
        #cuts['ttZ_ptmiss-100_loose']     = { 'expr' : '(' + ttZselectionLoose.replace('METCUT', '100') + ')' } 
        #cuts['ttZ_ptmiss-100_loose1tag'] = { 'expr' : '(' + ttZselectionLoose.replace('METCUT', '100') + ')', 'weight' : btagWeight1tag }
        #cuts['ttZ_ptmiss-100_loose2tag'] = { 'expr' : '(' + ttZselectionLoose.replace('METCUT', '100') + ')', 'weight' : btagWeight2tag }
        #cuts['ttZ_ptmiss-160_loose']     = { 'expr' : '(' + ttZselectionLoose.replace('METCUT', '160') + ')' }
        #cuts['ttZ_ptmiss-160_loose1tag'] = { 'expr' : '(' + ttZselectionLoose.replace('METCUT', '160') + ')', 'weight' : btagWeight1tag }
        #cuts['ttZ_ptmiss-160_loose2tag'] = { 'expr' : '(' + ttZselectionLoose.replace('METCUT', '160') + ')', 'weight' : btagWeight2tag }

        cuts['ttZ_loosemixtag']            = { 'expr' : '(' + ttZselectionLoose.replace('METCUT', '0') + ')',   'weight' : btagweightmixtag } 
        cuts['ttZ_ptmiss-100_loosemixtag'] = { 'expr' : '(' + ttZselectionLoose.replace('METCUT', '100') + ')', 'weight' : btagweightmixtag }
        cuts['ttZ_ptmiss-160_loosemixtag'] = { 'expr' : '(' + ttZselectionLoose.replace('METCUT', '160') + ')', 'weight' : btagweightmixtag }

if 'DYValidationRegion' in opt.tag:

    DY = OC + ' && ' + LL + ' && ' + Zcut.replace('ZCUT',  '15.')

    cuts['Zpeak_ptmiss-100to140']       = { 'expr' : '(' + DY + ' && ptmiss>=100 && ptmiss<140)', 'weight' : btagWeight0tag }
    cuts['Zpeak_ptmiss-140']            = { 'expr' : '(' + DY + ' && ptmiss>=140)', 'weight' : btagWeight0tag }
    cuts['Zpeak_ptmiss-160']            = { 'expr' : '(' + DY + ' && ptmiss>=160)', 'weight' : btagWeight0tag }
    cuts['Zpeak_ptmiss-100to140_nojet'] = '(' + DY + ' && ptmiss>=100 && ptmiss<140 && '+NoJets+')'
    cuts['Zpeak_ptmiss-140_nojet']      = '(' + DY + ' && ptmiss>=140 && '+NoJets+')' 
    cuts['Zpeak_ptmiss-160_nojet']      = '(' + DY + ' && ptmiss>=160 && '+NoJets+')' 

if 'SignalRegion' in opt.tag:

    nojetcutSR1 = NoJets
    jetscutSR1  = HasJet
    nojetcutSR2 = nojetcutSR1
    jetscutSR2  = jetscutSR1

    if 'VisHT' in opt.tag:
        if 'VisHTv1' in opt.tag:
            visht = '('+sumLeptonPt+'+Sum$(CleanJet_pt))'
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
            visht = '('+sumLeptonPt+')'
            nojetcutSR1 = visht+'<100'
            jetscutSR1  = visht+'>=100'
            nojetcutSR2 = visht+'<100'
            jetscutSR2  = visht+'>=100'

    splitjets=False  
    if 'CharginoSignalRegions' in opt.tag or 'TChipmWWSignalRegions' in opt.tag or 'VisHT' in opt.tag: splitjets=True

    ptmiss_cuts={"SR1": ' && ptmiss>=140 && ptmiss<200 ',
                 "SR2": ' && ptmiss>=200 && ptmiss<300 ',
                 "SR3": ' && ptmiss>=300 '}
    if 'Optim' in opt.tag and 'Ptm' in opt.tag:
        ptmiss_cuts={"SR1": ' && ptmiss>=160 && ptmiss<220 ',
                     "SR2": ' && ptmiss>=220 && ptmiss<280 ',
                     "SR3": ' && ptmiss>=280 && ptmiss<380 ',
                     "SR4": ' && ptmiss>=380 '}
        if 'TChipmWWSignalRegions' in opt.tag:
            ptmiss_cuts['SR1'] = ptmiss_cuts['SR1'].replace('ptmiss>=160', 'ptmiss>=140')

    for SR in ptmiss_cuts:

        isrcut = ''
        doISR  = False
        if "ISR" in opt. tag:
            if "ISR4" in opt.tag:
                if SR in ["SR4"]: doISR = True
            else:
                if SR in ["SR3","SR4"]:
                    doISR = True

        if doISR: isrcut=' && '+ISRCut

        if splitjets is True:
            if   SR == "SR1":
                jetscut  = ' && '+jetscutSR1
                nojetcut = ' && '+nojetcutSR1
            elif SR == "SR2":
                jetscut  = ' && '+jetscutSR2
                nojetcut = ' && '+nojetcutSR2

        btagcut=''
        vetocut=''

        cuts[SR+'_Tag_em' ]  = { 'expr' : '(' + OC+' && '+DF+ptmiss_cuts[SR]+isrcut+btagcut+')', 'weight' : btagWeight1tag }
        cuts[SR+'_Tag_sf' ]  = { 'expr' : '(' + OC+' && '+SF+ptmiss_cuts[SR]+isrcut+btagcut+')', 'weight' : btagWeight1tag }
        
        if splitjets is True and SR in ["SR1","SR2"]:
            cuts[SR+'_NoTag_em'] = { 'expr' : '(' + OC+' && '+DF+ptmiss_cuts[SR]+isrcut+vetocut+jetscut +')', 'weight' : btagWeight0tag }
            cuts[SR+'_NoTag_sf'] = { 'expr' : '(' + OC+' && '+SF+ptmiss_cuts[SR]+isrcut+vetocut+jetscut +')', 'weight' : btagWeight0tag }
            
            cuts[SR+'_NoJet_em'] = { 'expr' : '(' + OC+' && '+DF+ptmiss_cuts[SR]+isrcut+vetocut+nojetcut+')', 'weight' : btagWeight0tag }
            cuts[SR+'_NoJet_sf'] = { 'expr' : '(' + OC+' && '+SF+ptmiss_cuts[SR]+isrcut+vetocut+nojetcut+')', 'weight' : btagWeight0tag }
            
        else:
            cuts[SR+'_Veto_em']  = { 'expr' : '(' + OC+' && '+DF+ptmiss_cuts[SR]+isrcut+vetocut+')', 'weight' : btagWeight0tag }
            cuts[SR+'_Veto_sf']  = { 'expr' : '(' + OC+' && '+SF+ptmiss_cuts[SR]+isrcut+vetocut+')', 'weight' : btagWeight0tag }
    
# Add cuts for control regions to be added in the fit

if 'FitCR' in opt.tag and ('FitCRWZ' in opt.tag or 'FitCRttZ' in opt.tag or 'FitCRZZ' in opt.tag or isDatacardOrPlot):

    crcuts = { } 
    cutToRemove = [ ] 

    for cut in cuts:
        if 'SR' in cut:

            if not isDatacardOrPlot:
                cutToRemove.append(cut)

            if '_em' in cut: continue # Use only sf channel to avoid double counting

            crcut = cut.replace('SR', 'CR')
            exprcut = cuts[cut]['expr']
            exprcut = exprcut.replace(' && '+DF, '')
            exprcut = exprcut.replace(' && '+SF, '')

            if '_Tag_' in cut and ('FitCRttZ' in opt.tag or isDatacardOrPlot):

                if isDatacardOrPlot: # Ugly, but in this case these variables are not used
                    ttZselectionLoose = ''
                    btagweightmixtag = '1.'

                exprCR = exprcut.replace('ptmiss_phi', ptmiss_phi_ttZLoose)
                exprCR = exprCR.replace('ptmiss>', ptmiss_ttZLoose+'>')
                exprCR = exprCR.replace('ptmiss<', ptmiss_ttZLoose+'<')
                exprCR = exprCR.replace(OC, ttZselectionLoose)
                crcuts[crcut.replace('_sf', '_ttZ')] = { 'expr' : exprCR, 'weight' : btagweightmixtag }

            if '_Tag_' not in cut and ('FitCRWZ' in opt.tag or isDatacardOrPlot):
             
                exprCR = exprcut.replace(OC, nLooseLepton+'==3 && ' + nTightLepton + '==3 && deltaMassZ_WZ<10. && ptmiss_WZ>=0.')
                exprCR = exprCR.replace('ptmiss>', 'ptmiss_WZ>')
                exprCR = exprCR.replace('ptmiss<', 'ptmiss_WZ<')
                exprCR = exprCR.replace('ptmiss_phi', 'ptmiss_phi_WZ')
                crcuts[crcut.replace('_sf', '_WZ')] = { 'expr' : exprCR, 'weight' : cuts[cut]['weight'] }

            if '_Tag_' not in cut and ('FitCRZZ' in opt.tag or isDatacardOrPlot): 

                exprCR = exprcut.replace(OC, nLooseLepton+'==4 && ' + nTightLepton + '>=3 && deltaMassZ_ZZ<15. && ptmiss_ZZ>=0.')
                exprCR = exprCR.replace('ptmiss>', 'ptmiss_ZZ>')
                exprCR = exprCR.replace('ptmiss<', 'ptmiss_ZZ<')                  
                exprCR = exprCR.replace('ptmiss_phi', 'ptmiss_phi_ZZ')
                crcuts[crcut.replace('_sf', '_ZZ')] = { 'expr' : exprCR, 'weight' : cuts[cut]['weight'] } 

    for cut in cutToRemove:
        del cuts[cut]

    for cut in crcuts:
        cuts[cut] = crcuts[cut]

# To keep track of mkShapes without Multi

if hasattr(opt, 'batchQueue') and not hasattr(opt, 'dryRun'):

    cutList = [ ]
    for cut in cuts.keys(): cutList.append(cut)

    for cut in cutList:

        if 'expr' in cuts[cut]:
	    expr = cuts[cut]['expr']	
            del cuts[cut]['expr']

            if 'weight' in cuts[cut]:
                expr = '('+expr+')*'+cuts[cut]['weight']
                del cuts[cut]['weight']

        cuts[cut] = expr

# For postfit plots

if hasattr(opt, 'postFit'):
    if opt.postFit!='n':
        if opt.tag!=opt.inputFile.split('/')[2]+opt.inputFile.split('/')[3]:
            
            cutList = [ ]
            for cut in cuts.keys(): cutList.append(cut)

            yearcut = '_'+opt.tag.replace(opt.inputFile.split('/')[3], '')

            for cut in cutList:

                cuts[cut+yearcut] = { }
                for key in cuts[cut]: 
                    cuts[cut+yearcut][key] = cuts[cut][key]
            
                del cuts[cut]

# For structure and plot cfg files

if 'SignalRegion' in opt.tag:

    for sample in samples:

        cutToRemove = [ ]

        for cut in cuts:
            if ('SR' in cut and 'isControlSample' in samples[sample] and samples[sample]['isControlSample']==1) or ('CR' in cut and samples[sample]['isSignal']==1):
                cutToRemove.append(cut)

        if len(cutToRemove)>0:
            samples[sample]['removeFromCuts'] = cutToRemove

# Apply background scale factors
 
try:
    normBackgrounds
except NameError:
    normBackgrounds = None

normBackgroundNuisances = { }

if normBackgrounds is not None:
        
    for background in normBackgrounds:
        if background in samples:

            normBackgroundNuisances[background] = { }

            for region in normBackgrounds[background]:

                cutList = [ ]
                if 'cuts' not in normBackgrounds[background][region]:
                    cutList = cuts.keys()
                else:
                    for cut in cuts:
                        for cutsegment in normBackgrounds[background][region]['cuts']:
                            if cutsegment in cut:
                                cutList.append(cut)
                                break

                if len(cutList)>0:

                    scaleFactor = normBackgrounds[background][region]['scalefactor'].keys()[0]

                    normBackgroundNuisances[background][region] = { }

                    normBackgroundNuisances[background][region]['name'] = 'norm'+background+region 
                    normBackgroundNuisances[background][region]['cuts'] = cutList
                    normBackgroundNuisances[background][region]['scalefactorFromData'] = False if (region=='all' and scaleFactor=='1.00') else True

            for region in normBackgrounds[background]:    
                if region in normBackgroundNuisances[background]:

                    scaleFactor = normBackgrounds[background][region]['scalefactor'].keys()[0]  
                    scaleFactorError = normBackgrounds[background][region]['scalefactor'][scaleFactor]
                    scaleFactorRelativeError = float(scaleFactorError)/float(scaleFactor)                    

                    regionCut = normBackgrounds[background][region]['selection']
                    regionWeight = scaleFactor if regionCut=='1.' else '((!'+regionCut+')+('+regionCut+')*'+scaleFactor+')'

                    nuisanceType = 'lnN'
                    for cut in normBackgroundNuisances[background][region]['cuts']:
                        for otherregion in normBackgroundNuisances[background]:
                            if otherregion!=region and cut in normBackgroundNuisances[background][otherregion]['cuts']:
                                nuisanceType = 'shape'

                    if normBackgroundNuisances[background][region]['scalefactorFromData']:
                        samples[background]['weight'] += '*'+regionWeight

                    normBackgroundNuisances[background][region]['type'] = nuisanceType

                    if nuisanceType=='lnN':

                        normBackgroundNuisances[background][region]['samples'] = { background : str(1.+scaleFactorRelativeError) }
                      
                    else:

                        regionWeightUp   = '((!'+regionCut+')+('+regionCut+')*'+str(1.+scaleFactorRelativeError)+')'
                        regionWeightDown = '((!'+regionCut+')+('+regionCut+')*'+str(1.-scaleFactorRelativeError)+')' 

                        normBackgroundNuisances[background][region]['kind'] = 'weight'
                        normBackgroundNuisances[background][region]['samples'] = { background : [ regionWeightUp, regionWeightDown ] }



