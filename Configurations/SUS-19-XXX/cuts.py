#

massZ = '91.1876'
vetoZ = 'fabs(mll'+ctrltag+'-'+massZ+')>15.'
Zcut  = 'fabs(mll'+ctrltag+'-'+massZ+')<ZCUT'
SF    = LL+' && '+vetoZ  

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
    
if 'VetoNoiseEE' in opt.tag:

    channelCut = OC 
    if 'Zveto' in opt.tag:
        channelCut += ' && ('+DF+' || '+SF+')'
 
    EENoiseVeto0 = '(Sum$(abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139)>=1)'
    EENoiseVeto1 = '(Sum$(Jet_pt*(1.-Jet_rawFactor)<50. && abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139)>=1)'
    EENoiseVeto2 = '(Sum$(Jet_pt*(1.-Jet_rawFactor)<50. && Jet_pt>30. && abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139)>=1)'
    
    ptm = ' && ptmiss > 100. && ptmiss<=140'
    if 'MET' in opt.tag: ptm = ' && MET_pt > 100 && MET_pt < 140 ' # currently unused
      
    cuts['Veto0_Tag']             = { 'expr' : '('+channelCut+' && '+EENoiseVeto0+')', 'weight' : btagWeight1tag }
    cuts['Veto0_Tag_highptmiss']  = { 'expr' : '('+channelCut+' && '+EENoiseVeto0+' && ptmiss>=100. && ptmiss<140.)', 'weight' : btagWeight1tag }
    cuts['Veto1_Tag']             = { 'expr' : '('+channelCut+' && '+EENoiseVeto1+')', 'weight' : btagWeight1tag }
    cuts['Veto1_Tag_highptmiss']  = { 'expr' : '('+channelCut+' && '+EENoiseVeto1+' && ptmiss>=100. && ptmiss<140.)', 'weight' : btagWeight1tag }
    cuts['Veto2_Tag']             = { 'expr' : '('+channelCut+' && '+EENoiseVeto2+')', 'weight' : btagWeight1tag }
    cuts['Veto2_Tag_highptmiss']  = { 'expr' : '('+channelCut+' && '+EENoiseVeto2+' && ptmiss>=100. && ptmiss<140.)', 'weight' : btagWeight1tag }
    cuts['Veto0_Veto']            = { 'expr' : '('+channelCut+' && '+EENoiseVeto0+')', 'weight' : btagWeight0tag }
    cuts['Veto0_Veto_highptmiss'] = { 'expr' : '('+channelCut+' && '+EENoiseVeto0+' && ptmiss>=100. && ptmiss<140.)', 'weight' : btagWeight0tag }
    cuts['Veto1_Veto']            = { 'expr' : '('+channelCut+' && '+EENoiseVeto1+')', 'weight' : btagWeight0tag }
    cuts['Veto1_Veto_highptmiss'] = { 'expr' : '('+channelCut+' && '+EENoiseVeto1+' && ptmiss>=100. && ptmiss<140.)', 'weight' : btagWeight0tag }
    cuts['Veto2_Veto']            = { 'expr' : '('+channelCut+' && '+EENoiseVeto2+')', 'weight' : btagWeight0tag }
    cuts['Veto2_Veto_highptmiss'] = { 'expr' : '('+channelCut+' && '+EENoiseVeto2+' && ptmiss>=100. && ptmiss<140.)', 'weight' : btagWeight0tag }
    if 'HTF' in opt.tag:
        cuts['Veto0_Tag_HTF']             = { 'expr' : '('+OC+' && '+EENoiseVeto0+' && ' + HTForward + '>=60.'+')', 'weight' : btagWeight1tag }
        cuts['Veto0_Tag_highptmiss_HTF']  = { 'expr' : '('+OC+' && '+EENoiseVeto0+' && ptmiss>=100. && ptmiss<=140.'+' && ' + HTForward + '>=60.'+')', 'weight' : btagWeight1tag }
        cuts['Veto1_Tag_HTF']             = { 'expr' : '('+OC+' && '+EENoiseVeto1+' && ' + HTForward + '>=60.' +')', 'weight' : btagWeight1tag }
        cuts['Veto1_Tag_highptmiss_HTF']  = { 'expr' : '('+OC+' && '+EENoiseVeto1+' && ptmiss>=100. && ptmiss<=140.'+' && ' + HTForward + '>=60.'+')', 'weight' : btagWeight1tag }
        cuts['Veto2_Tag_HTF']             = { 'expr' : '('+OC+' && '+EENoiseVeto2+' && ' + HTForward + '>=60.'+')', 'weight' : btagWeight1tag }
        cuts['Veto2_Tag_highptmiss_HTF']  = { 'expr' : '('+OC+' && '+EENoiseVeto2+' && ptmiss>=100. && ptmiss<=140.'+' && ' + HTForward + '>=60.'+')', 'weight' : btagWeight1tag }
        cuts['Veto0_Veto_HTF']            = { 'expr' : '('+OC+' && '+EENoiseVeto0+' && ' + HTForward + '>=60.'+')', 'weight' : btagWeight0tag }
        cuts['Veto0_Veto_highptmiss_HTF'] = { 'expr' : '('+OC+' && '+EENoiseVeto0+' && ptmiss>=100. && ptmiss<=140.'+' && ' + HTForward + '>=60.'+')', 'weight' : btagWeight0tag }
        cuts['Veto1_Veto_HTF']            = { 'expr' : '('+OC+' && '+EENoiseVeto1+' && ' + HTForward + '>=60.'+')', 'weight' : btagWeight0tag }
        cuts['Veto1_Veto_highptmiss_HTF'] = { 'expr' : '('+OC+' && '+EENoiseVeto1+' && ptmiss>=100. && ptmiss<=140.'+' && ' + HTForward + '>=60.'+')', 'weight' : btagWeight0tag }
        cuts['Veto2_Veto_HTF']            = { 'expr' : '('+OC+' && '+EENoiseVeto2+' && ' + HTForward + '>=60.'+')', 'weight' : btagWeight0tag }
        cuts['Veto2_Veto_highptmiss_HTF'] = { 'expr' : '('+OC+' && '+EENoiseVeto2+' && ptmiss>=100. && ptmiss<=140.'+' && ' + HTForward + '>=60.'+')', 'weight' : btagWeight0tag }

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

    cuts['WW_metcut']   = '(' + OC+' && '+DF+' && nCleanJet==0 && ptmiss>=70)'
    cuts['WW_nometcut'] = '(' + OC+' && '+DF+' && nCleanJet==0)'

if 'DYControlRegion' in opt.tag:

    DY = OC+' && '+LL+' && '+Zcut.replace('ZCUT',  '15.')
    
    cuts['DY_ee']     = { 'expr' : '(' + DY+' && '+EE+')', 'weight' : btagWeight0tag }
    cuts['DY_mm']     = { 'expr' : '(' + DY+' && '+MM+')', 'weight' : btagWeight0tag }
    cuts['DY_ee_jet'] = { 'expr' : '(' + DY+' && '+EE+' && Alt$(CleanJet_pt[1],0)>=30.)', 'weight' : btagWeight0tag }
    cuts['DY_mm_jet'] = { 'expr' : '(' + DY+' && '+MM+' && Alt$(CleanJet_pt[1],0)>=30.)', 'weight' : btagWeight0tag }

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
    cuts['VR1_Veto_em_0jet']   = '(' + OC+' && '+DF+             ' && ptmiss>=100 && ptmiss<140 && nCleanJet==0)'
    cuts['VR1_Veto_sf_0jet']   = '(' + OC+' && '+SF+             ' && ptmiss>=100 && ptmiss<140 && nCleanJet==0)'
    cuts['VR1_Veto_mm_0jet']   = '(' + OC+' && '+MM+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140 && nCleanJet==0)'
    cuts['VR1_Veto_ee_0jet']   = '(' + OC+' && '+EE+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140 && nCleanJet==0)'
    if 'More' in opt.tag:
        cuts['VR1_Veto_em_mt2']    = '(' + OC+' && '+DF+             ' && ptmiss>=100 && ptmiss<140 && mt2ll>100.)'
        cuts['VR1_Veto_mm_mt2']    = '(' + OC+' && '+MM+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140 && mt2ll>100.)'
        cuts['VR1_Veto_ee_mt2']    = '(' + OC+' && '+EE+' && '+vetoZ+' && ptmiss>=100 && ptmiss<140 && mt2ll>100.)'
        cuts['VR1_Veto_0jet']      = '(' + OC+' && ('+SF+' || '+DF+')  && ptmiss>=100 && ptmiss<140 && nCleanJet==0)'

if 'SameSignValidationRegion' in opt.tag:

    cuts['SS_ptmiss']            = { 'expr' : '('+SSM+' && ptmiss'+ctrltag+'>=0  )', 'weight' : btagWeight1tag }
    cuts['SS_ptmiss-100to140']   = { 'expr' : '('+SS +' && ptmiss'+ctrltag+'>=100 && ptmiss'+ctrltag+'<140)', 'weight' : btagWeight1tag }
    cuts['SS_ptmiss-140']        = { 'expr' : '('+SS +' && ptmiss'+ctrltag+'>=140)', 'weight' : btagWeight1tag }
    cuts['SS_ptmiss-160']        = { 'expr' : '('+SS +' && ptmiss'+ctrltag+'>=160)', 'weight' : btagWeight1tag }
    cuts['SS_ptmiss-160_plus']   = { 'expr' : '('+SSP+' && ptmiss'+ctrltag+'>=160)', 'weight' : btagWeight1tag }
    cuts['SS_ptmiss-160_minus']  = { 'expr' : '('+SSM+' && ptmiss'+ctrltag+'>=160)', 'weight' : btagWeight1tag }

if 'FakeValidationRegion' in opt.tag:
    
    Fake = LepId2of3 + ' && ' + OCT

    cuts['Fake']                   = { 'expr' : '('+Fake+' && ptmiss'+ctrltag+'>=0  )', 'weight' : btagWeight1tag }
    cuts['Fake_ptmiss-100to140']   = { 'expr' : '('+Fake+' && ptmiss'+ctrltag+'>=100 && ptmiss'+ctrltag+'<140)', 'weight' : btagWeight1tag }
    cuts['Fake_ptmiss-140']        = { 'expr' : '('+Fake+' && ptmiss'+ctrltag+'>=140)', 'weight' : btagWeight1tag }
    cuts['Fake_ptmiss-160']        = { 'expr' : '('+Fake+' && ptmiss'+ctrltag+'>=160)', 'weight' : btagWeight1tag }

if 'WZValidationRegion' in opt.tag or 'WZtoWWValidationRegion' in opt.tag:

    WZselection = nLooseLepton+'==3 && ' + nTightLepton + '==3 && deltaMassZ'+ctrltag+'<ZCUT && ptmiss'+ctrltag+'>=METCUT'

    if 'WZValidationRegion' in opt.tag:

        cuts['WZ_3Lep_ptmiss-140']  = { 'expr' : '(' + WZselection.replace('ZCUT', '999.').replace('METCUT', '140') + ')', 'weight' : btagWeight0tag }
        cuts['WZ_3LepZ_ptmiss-140'] = { 'expr' : '(' + WZselection.replace('ZCUT',  '15.').replace('METCUT', '140') + ')', 'weight' : btagWeight0tag }
        cuts['WZ_3Lep_ptmiss-160']  = { 'expr' : '(' + WZselection.replace('ZCUT', '999.').replace('METCUT', '160') + ')', 'weight' : btagWeight0tag }
        cuts['WZ_3LepZ_ptmiss-160'] = { 'expr' : '(' + WZselection.replace('ZCUT',  '15.').replace('METCUT', '160') + ')', 'weight' : btagWeight0tag }

    elif 'WZtoWWValidationRegion' in opt.tag:

        cuts['WZtoWW_Zcut10_ptmiss-140'] = { 'expr' : '('+WZselection.replace('ZCUT','10.').replace('METCUT','140')+')', 'weight' : btagWeight0tag }
        cuts['WZtoWW_Zcut15_ptmiss-140'] = { 'expr' : '('+WZselection.replace('ZCUT','15.').replace('METCUT','140')+')', 'weight' : btagWeight0tag }
        cuts['WZtoWW_Zcut10_ptmiss-160'] = { 'expr' : '('+WZselection.replace('ZCUT','10.').replace('METCUT','160')+')', 'weight' : btagWeight0tag }
        cuts['WZtoWW_Zcut15_ptmiss-160'] = { 'expr' : '('+WZselection.replace('ZCUT','15.').replace('METCUT','160')+')', 'weight' : btagWeight0tag }

if 'ttZValidationRegion' in opt.tag or 'ZZValidationRegion' in opt.tag:

    sel4Lep = nLooseLepton+'==4 && ' + nTightLepton + '>=3'

    if 'ttZValidationRegion' in opt.tag:

        ttZselection = sel4Lep + ' && deltaMassZ'+ctrltag+'<10. && ptmiss'+ctrltag+'>=METCUT && nCleanJet>=2 && CleanJet_pt[1]>=20.'

        cuts['ttZ']            = { 'expr' : '(' + ttZselection.replace('METCUT',   '0') + ')', 'weight' : btagWeight1tag }
        cuts['ttZ_ptmiss-140'] = { 'expr' : '(' + ttZselection.replace('METCUT', '140') + ')', 'weight' : btagWeight1tag }
        cuts['ttZ_ptmiss-160'] = { 'expr' : '(' + ttZselection.replace('METCUT', '160') + ')', 'weight' : btagWeight1tag }

    elif 'ZZValidationRegion' in opt.tag:

        ZZselection = sel4Lep + ' && deltaMassZ'+ctrltag+'<15. && ptmiss'+ctrltag+'>=METCUT'

        cuts['ZZ']            = { 'expr' : '(' + ZZselection.replace('METCUT',   '0') + ')', 'weight' : btagWeight0tag }
        cuts['ZZ_ptmiss-140'] = { 'expr' : '(' + ZZselection.replace('METCUT', '140') + ')', 'weight' : btagWeight0tag }
        cuts['ZZ_ptmiss-160'] = { 'expr' : '(' + ZZselection.replace('METCUT', '160') + ')', 'weight' : btagWeight0tag }

if 'ttZNormalization' in opt.tag:

    ttZcommon = nTightLepton+'>=3 && deltaMassZ_ctrltag<10. && '+ptmissNano+'>=METCUT && nCleanJet>=2 && Alt$(CleanJet_pt[1],0)>=20.'
    ttZ3Lep = nLooseLepton+'==3 && '+ttZcommon.replace('_ctrltag', '_WZ')
    ttZ4Lep = nLooseLepton+'==4 && '+ttZcommon.replace('_ctrltag', '_ttZ') 
    ttZselectionLoose = '(('+ ttZ3Lep + ') || (' + ttZ4Lep + '))'   

    cuts['ttZ_ptmiss-160_loose1tag'] = { 'expr' : '(' + ttZselectionLoose.replace('METCUT', '160') + ')', 'weight' : btagWeight1tag }
    cuts['ttZ_ptmiss-160_loose2tag'] = { 'expr' : '(' + ttZselectionLoose.replace('METCUT', '160') + ')', 'weight' : btagWeight2tag }

if 'DYValidationRegion' in opt.tag:

    DY = OC + ' && ' + LL + ' && ' + Zcut.replace('ZCUT',  '15.')

    cuts['Zpeak_ptmiss-100to140']       = { 'expr' : '(' + DY + ' && ptmiss>=100 && ptmiss<140)', 'weight' : btagWeight0tag }
    cuts['Zpeak_ptmiss-140']            = { 'expr' : '(' + DY + ' && ptmiss>=140)', 'weight' : btagWeight0tag }
    cuts['Zpeak_ptmiss-160']            = { 'expr' : '(' + DY + ' && ptmiss>=160)', 'weight' : btagWeight0tag }
    cuts['Zpeak_ptmiss-100to140_nojet'] = '(' + DY + ' && ptmiss>=100 && ptmiss<140 && nCleanJet==0)'
    cuts['Zpeak_ptmiss-140_nojet']      = '(' + DY + ' && ptmiss>=140 && nCleanJet==0)' 
    cuts['Zpeak_ptmiss-160_nojet']      = '(' + DY + ' && ptmiss>=160 && nCleanJet==0)' 

if 'SignalRegion' in opt.tag:

    nojetcutSR1 = 'nCleanJet==0'
    jetscutSR1  = 'nCleanJet>0'
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
    if 'CharginoSignalRegions' in opt.tag or 'VisHT' in opt.tag: splitjets=True

    ptmiss_cuts={"SR1": ' && ptmiss>=140 && ptmiss<200 ',
                 "SR2": ' && ptmiss>=200 && ptmiss<300 ',
                 "SR3": ' && ptmiss>=300 '}
    if 'Optim' in opt.tag and 'Ptm' in opt.tag:
        ptmiss_cuts={"SR1": ' && ptmiss>=160 && ptmiss<220 ',
                     "SR2": ' && ptmiss>=220 && ptmiss<280 ',
                     "SR3": ' && ptmiss>=280 && ptmiss<380 ',
                     "SR4": ' && ptmiss>=380 '}

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
                    
