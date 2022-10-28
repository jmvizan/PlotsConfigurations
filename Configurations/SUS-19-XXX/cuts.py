#

massZ = '91.1876'
vetoZ = 'fabs(mll'+ctrltag+'-'+massZ+')>15.'
Zcut  = 'fabs(mll'+ctrltag+'-'+massZ+')<ZCUT'
SF    = LL+' && '+vetoZ  

NoJets = 'Alt$(CleanJet_pt[0],0)<' +jetPtCut
HasJet = 'Alt$(CleanJet_pt[0],0)>='+jetPtCut
 
if 'Data' in opt.sigset or 'SingleLepton' in opt.sigset: # from nAODv9 it should't matter anymore 
    btagWeightNoCut = '1.'
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

    triggerOC = OC.replace('mll'+ctrltag+'>=20. && ', '') 
    #triggerCuts = { 'none' : '', 'mll' : ' && mll>=20.',  'met' : ' && MET_pt>100.', 'all' : ' && mll>=20. && MET_pt>100.' }
    triggerCuts = { 'none' : '', 'met' : ' && MET_pt>100.', 'btag' : ' && MET_pt>100. && '+bTagPass, 'veto' : ' && MET_pt>100. && '+bTagVeto }
    if '3Lep' in opt.tag:
        triggerOC = triggerOC.replace('==2', '==3')
        for cutt in triggerCuts:
            triggerCuts[cutt] = triggerCuts[cutt].replace('mll', 'mll'+ctrltag)
    etaBins = { '_full' : '', '_cent' : ' && abs(Lepton_eta[0])<=1.2', '_forw' : ' && abs(Lepton_eta[0])>1.2 && abs(Lepton_eta[0])<=2.4' }

    fullTrigger = '(Trigger_dblEl || Trigger_dblMu || Trigger_ElMu  || Trigger_sngEl || Trigger_sngMu)'
    triggerBits = { 'ee' : { 'cut' : EE, 'double' : 'Trigger_dblEl', 'both' : '(Trigger_dblEl || Trigger_sngEl)'                 , 'full' : fullTrigger },
                    'mm' : { 'cut' : MM, 'double' : 'Trigger_dblEl', 'both' : '(Trigger_dblMu || Trigger_sngMu)'                 , 'full' : fullTrigger },
                    'em' : { 'cut' : DF, 'double' : 'Trigger_ElMu' , 'both' : '(Trigger_ElMu  || Trigger_sngEl || Trigger_sngMu)', 'full' : fullTrigger }
                   }

    for ch in triggerBits:
        for etab in etaBins:
            for cutt in triggerCuts:

                denominatorName = ch+etab+'_'+cutt
                denominatorCut  = triggerOC + ' && ' + triggerBits[ch]['cut'] + etaBins[etab] + triggerCuts[cutt]
                cuts[denominatorName] = denominatorCut
   
                if 'MET' in opt.sigset:
                    for trgbit in triggerBits[ch]:
                        if trgbit!='cut':
                            cuts[denominatorName+'_'+trgbit] = denominatorCut + ' && ' + triggerBits[ch][trgbit]

                else:
                    cuts[denominatorName+'_eff'] = { 'expr' : denominatorCut, 'weight' : 'TriggerEffWeight_2l' }

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
    
if 'VetoNoiseEE' in opt.tag and not 'HTFCut' in opt.tag:

    channelCut = OC 
    if 'Zveto' in opt.tag:
        channelCut += ' && ('+DF+' || '+SF+')'
 
    EENoiseVeto0 = '(Sum$(abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139)>=1)'
    EENoiseVeto1 = '(Sum$(Jet_pt*(1.-Jet_rawFactor)<50. && abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139)>=1)'
    EENoiseVeto2 = '(Sum$(Jet_pt*(1.-Jet_rawFactor)<50. && Jet_pt>30. && abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139)>=1)'
    
    ptm = ' ptmiss>=100. && ptmiss<140 '
    if 'MET' in opt.tag: ptm = ptm.replace('ptmiss', 'MET_pt')

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

if 'VetoNoiseEE' in opt.tag and 'HTFCut' in opt.tag:

    channelCut = OC
    if 'Zveto' in opt.tag:
        channelCut += ' && ('+DF+' || '+SF+')'

    EENoiseVeto0 = '(Sum$(abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139)>=1)'
    EENoiseVeto1 = '(Sum$(Jet_pt*(1.-Jet_rawFactor)<50. && abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139)>=1)'
    EENoiseVeto2 = '(Sum$(Jet_pt*(1.-Jet_rawFactor)<50. && Jet_pt>30. && abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139)>=1)'

    ptm = ' ptmiss>=100. && ptmiss<140 '
    if 'MET' in opt.tag: ptm = ptm.replace('ptmiss', 'MET_pt')

    cuts['Veto0_Tag_HTFCut']             = { 'expr' : '('+OC+' && '+EENoiseVeto0+' && ' + HTForward + '<60.'+')', 'weight' : btagWeight1tag }
    cuts['Veto0_Tag_highptmiss_HTFCut']  = { 'expr' : '('+OC+' && '+EENoiseVeto0+' && '+ptm+' && ' + HTForward + '<60.'+')', 'weight' : btagWeight1tag }
    cuts['Veto1_Tag_HTFCut']             = { 'expr' : '('+OC+' && '+EENoiseVeto1+' && ' + HTForward + '<60.' +')', 'weight' : btagWeight1tag }
    cuts['Veto1_Tag_highptmiss_HTFCut']  = { 'expr' : '('+OC+' && '+EENoiseVeto1+' && '+ptm+' && ' + HTForward + '<60.'+')', 'weight' : btagWeight1tag }
    cuts['Veto2_Tag_HTFCut']             = { 'expr' : '('+OC+' && '+EENoiseVeto2+' && ' + HTForward + '<60.'+')', 'weight' : btagWeight1tag }
    cuts['Veto2_Tag_highptmiss_HTFcut']  = { 'expr' : '('+OC+' && '+EENoiseVeto2+' && '+ptm+' && ' + HTForward + '<60.'+')', 'weight' : btagWeight1tag }
    cuts['Veto0_Veto_HTFCut']            = { 'expr' : '('+OC+' && '+EENoiseVeto0+' && ' + HTForward + '<60.'+')', 'weight' : btagWeight0tag }
    cuts['Veto0_Veto_highptmiss_HTFCut'] = { 'expr' : '('+OC+' && '+EENoiseVeto0+' && '+ptm+' && ' + HTForward + '<60.'+')', 'weight' : btagWeight0tag }
    cuts['Veto1_Veto_HTFCut']            = { 'expr' : '('+OC+' && '+EENoiseVeto1+' && ' + HTForward + '<60.'+')', 'weight' : btagWeight0tag }
    cuts['Veto1_Veto_highptmiss_HTFCut'] = { 'expr' : '('+OC+' && '+EENoiseVeto1+' && '+ptm+' && ' + HTForward + '<60.'+')', 'weight' : btagWeight0tag }
    cuts['Veto2_Veto_HTFCut']            = { 'expr' : '('+OC+' && '+EENoiseVeto2+' && ' + HTForward + '<60.'+')', 'weight' : btagWeight0tag }
    cuts['Veto2_Veto_highptmiss_HTFCut'] = { 'expr' : '('+OC+' && '+EENoiseVeto2+' && '+ptm+' && ' + HTForward + '<60.'+')', 'weight' : btagWeight0tag }

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
    if 'Latino' in opt.tag:
        print "im doing latinos"
        cuts['WW_Latino_em']   = '(' + OC+' && '+DF+' && '+pTll+'>30 && '+NoJets+' &&  ptmiss>=20 && mll>20) '
        cuts['WW_Latino_sf']   = '(' + OC+' && '+SF+' && '+pTll+'>30 && '+NoJets+' && ' +vetoZ+' && ptmiss>=20 && mll>40) '
    else:
        cuts['WW_metcut']   = '(' + OC+' && '+DF+' && '+NoJets+' && ptmiss>=70)'
        cuts['WW_nometcut'] = '(' + OC+' && '+DF+' && '+NoJets+')'

if 'DYControlRegion' in opt.tag:

    DY = OC+' && '+LL+' && '+Zcut.replace('ZCUT',  '15.')
    
    cuts['DY_ee']     = { 'expr' : '(' + DY+' && '+EE+')', 'weight' : btagWeight0tag }
    cuts['DY_mm']     = { 'expr' : '(' + DY+' && '+MM+')', 'weight' : btagWeight0tag }
    cuts['DY_NoJet_ee'] = { 'expr' : '(' + DY+' && '+EE+' && '+NoJets+')', 'weight' : btagWeight0tag }
    cuts['DY_NoJet_mm'] = { 'expr' : '(' + DY+' && '+MM+' && '+NoJets+')', 'weight' : btagWeight0tag }

if 'DYMeasurements' in opt.tag:

    DY = OC+' && '+LL+' && mll>=60. && mll<=140.'

    cuts['DY_ee']       = { 'expr' : '(' + DY+' && '+EE+')', 'weight' : btagWeight0tag }
    cuts['DY_mm']       = { 'expr' : '(' + DY+' && '+MM+')', 'weight' : btagWeight0tag }
    cuts['DY_ee_nojet'] = { 'expr' : '(' + DY+' && '+EE+' && Alt$(CleanJet_pt[0],0)<30.)', 'weight' : btagWeight0tag }
    cuts['DY_mm_nojet'] = { 'expr' : '(' + DY+' && '+MM+' && Alt$(CleanJet_pt[0],0)<30.)', 'weight' : btagWeight0tag }
    cuts['DY_ee_nomet'] = { 'expr' : '(' + DY+' && '+EE+' && ptmiss<30.)', 'weight' : btagWeight0tag }
    cuts['DY_ee_nomet'] = { 'expr' : '(' + DY+' && '+EE+' && ptmiss<30.)', 'weight' : btagWeight0tag }
    cuts['DY_ee_cuts']  = { 'expr' : '(' + DY+' && '+EE+' && ptmiss<30. && Alt$(CleanJet_pt[0],0)<30.)', 'weight' : btagWeight0tag }
    cuts['DY_ee_cuts']  = { 'expr' : '(' + DY+' && '+EE+' && ptmiss<30. && Alt$(CleanJet_pt[0],0)<30.)', 'weight' : btagWeight0tag }

if 'DYtauControlRegion' in opt.tag:

    DYtau = OC+' && '+DF+' && '+Zcut.replace('ZCUT',  '15.')

    cuts['DY_em']     = { 'expr' : '(' + DYtau+')', 'weight' : btagWeight0tag }
    cuts['DY_NoJet_em'] = { 'expr' : '(' + DYtau+' && '+NoJets+')', 'weight' : btagWeight0tag }

if 'DYDarkMatterControlRegion' in opt.tag:

    DY = OC+' && '+LL+' && '+Zcut.replace('ZCUT',  '15.')

    cuts['DY_ee_puppi'] = '(' + DY+' && '+EE+') && Alt$(CleanJet_pt[1],0)>=30. && PuppiMET_pt>=50.'
    cuts['DY_mm_puppi'] = '(' + DY+' && '+MM+') && Alt$(CleanJet_pt[1],0)>=30. && PuppiMET_pt>=50.'
    cuts['DY_ee_pfmet'] = '(' + DY+' && '+EE+') && Alt$(CleanJet_pt[1],0)>=30. && ptmiss>=50.'
    cuts['DY_mm_pfmet'] = '(' + DY+' && '+MM+') && Alt$(CleanJet_pt[1],0)>=30. && ptmiss>=50.'

if 'HighPtMissControlRegion' in opt.tag or 'HighPtMissValidationRegion' in opt.tag:

    if not hasattr(opt, 'outputDirDatacard'):

        cuts['VR1_em']   = { 'expr' : OC+' && '+DF+' && ptmiss'+ctrltag+'>=100 && ptmiss'+ctrltag+'<140', 'weight' : btagWeightNoCut }
        cuts['VR1_sf']   = { 'expr' : OC+' && '+SF+' && ptmiss'+ctrltag+'>=100 && ptmiss'+ctrltag+'<140', 'weight' : btagWeightNoCut }

        cuts['VR1_Veto_em']  = { 'expr' : OC+' && '+DF+' && ptmiss'+ctrltag+'>=100 && ptmiss'+ctrltag+'<140', 'weight' : btagWeight0tag }
        cuts['VR1_Veto_sf']  = { 'expr' : OC+' && '+SF+' && ptmiss'+ctrltag+'>=100 && ptmiss'+ctrltag+'<140', 'weight' : btagWeight0tag }

    cuts['VR1_Tag_em']   = { 'expr' : OC+' && '+DF+' && ptmiss'+ctrltag+'>=100 && ptmiss'+ctrltag+'<140', 'weight' : btagWeight1tag }
    cuts['VR1_Tag_sf']   = { 'expr' : OC+' && '+SF+' && ptmiss'+ctrltag+'>=100 && ptmiss'+ctrltag+'<140', 'weight' : btagWeight1tag }

    cuts['VR1_NoTag_em']  = { 'expr' : OC+' && '+DF+' && ptmiss'+ctrltag+'>=100 && ptmiss'+ctrltag+'<140 && '+HasJet, 'weight' : btagWeight0tag }
    cuts['VR1_NoTag_sf']  = { 'expr' : OC+' && '+SF+' && ptmiss'+ctrltag+'>=100 && ptmiss'+ctrltag+'<140 && '+HasJet, 'weight' : btagWeight0tag }
    cuts['VR1_NoJet_em']  = { 'expr' : OC+' && '+DF+' && ptmiss'+ctrltag+'>=100 && ptmiss'+ctrltag+'<140 && '+NoJets, 'weight' : btagWeight0tag }
    cuts['VR1_NoJet_sf']  = { 'expr' : OC+' && '+SF+' && ptmiss'+ctrltag+'>=100 && ptmiss'+ctrltag+'<140 && '+NoJets, 'weight' : btagWeight0tag }

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

if 'LeptonL2TRate' in opt.tag:

    mTLep1MET = 'sqrt(2*Lepton_pt[0]*MET_pt*(1.-cos(Lepton_phi[0]-MET_phi)))'
    hadronCut = 'nCleanJet>=1 && CleanJet_pt[0]>25. && sqrt((Lepton_eta[0]-CleanJet_eta[0])*(Lepton_eta[0]-CleanJet_eta[0])+acos(cos(Lepton_phi[0]-CleanJet_phi[0]))*acos(cos(Lepton_phi[0]-CleanJet_phi[0])))>1.'
    LeptonL2TRateSelection = nLooseLepton+'==1 && MET_pt<20. && '+mTLep1MET+'<20. && '+hadronCut+' && Lepton_pt[0]>=20. && abs(Lepton_eta[0])<2.4'

    tightIDcut = nTightLepton+'==1'
    if 'TightLep' in opt.tag: tightIDcut += ' && (Lepton_isTightElectron_cutBasedTightPOG[0]+(abs(Lepton_pdgId[0])==13)*Alt$(Muon_tightId[abs(Lepton_muonIdx[0])],0))==1' 

    for dataSet in leptonL2TRateTriggers:
        for ptrange in leptonL2TRateTriggers[dataSet]:
            leptonIdCut = 'fabs(Lepton_pdgId[0])==11' if (dataSet=='SingleElectron' or 'Electron' in ptrange) else 'fabs(Lepton_pdgId[0])==13'
            triggerCut = leptonL2TRateTriggers[dataSet][ptrange]
            effLumi = '*'+effectiveTriggerLuminosity[yeartag][dataSet+ptrange] if 'EWK' in opt.sigset else ''
            cuts[dataSet+ptrange+'Loose'] = { 'expr' : LeptonL2TRateSelection+' && '+leptonIdCut+' && '+triggerCut,                  'weight' : btagWeight0tag+effLumi }
            cuts[dataSet+ptrange+'Tight'] = { 'expr' : LeptonL2TRateSelection+' && '+leptonIdCut+' && '+triggerCut+' && '+tightIDcut,'weight' : btagWeight0tag+effLumi }

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

if 'SameSignVetoValidationRegion' in opt.tag:

    cuts['SSV_ptmiss']            = { 'expr' : '('+SSM+' && ptmiss'+ctrltag+'>=0  )', 'weight' : btagWeight0tag }
    cuts['SSV_ptmiss_100to140']   = { 'expr' : '('+SS +' && ptmiss'+ctrltag+'>=100 && ptmiss'+ctrltag+'<140)', 'weight' : btagWeight0tag }
    cuts['SSV_ptmiss_140']        = { 'expr' : '('+SS +' && ptmiss'+ctrltag+'>=140)', 'weight' : btagWeight0tag }
    cuts['SSV_ptmiss_160']        = { 'expr' : '('+SS +' && ptmiss'+ctrltag+'>=160)', 'weight' : btagWeight0tag }
    cuts['SSV_ptmiss_160_plus']   = { 'expr' : '('+SSP+' && ptmiss'+ctrltag+'>=160)', 'weight' : btagWeight0tag }
    cuts['SSV_ptmiss_160_minus']  = { 'expr' : '('+SSM+' && ptmiss'+ctrltag+'>=160)', 'weight' : btagWeight0tag }

if 'FakeValidationRegion' in opt.tag:
    
    Fake = LepId2of3 + ' && ' + OCT

    cuts['Fake']                   = { 'expr' : '('+Fake+' && ptmiss'+ctrltag+'>=0  )', 'weight' : btagWeight1tag }
    cuts['Fake_ptmiss_100to140']   = { 'expr' : '('+Fake+' && ptmiss'+ctrltag+'>=100 && ptmiss'+ctrltag+'<140)', 'weight' : btagWeight1tag }
    cuts['Fake_ptmiss_140']        = { 'expr' : '('+Fake+' && ptmiss'+ctrltag+'>=140)', 'weight' : btagWeight1tag }
    cuts['Fake_ptmiss_160']        = { 'expr' : '('+Fake+' && ptmiss'+ctrltag+'>=160)', 'weight' : btagWeight1tag }

if 'WZValidationRegion' in opt.tag or 'WZtoWWValidationRegion' in opt.tag:

    WZselection = nLooseLepton+'==3 && ' + nTightLepton + '==3 && deltaMassZ'+ctrltag+'<ZCUT && ptmiss'+ctrltag+'>=METCUT'

    if 'WZValidationRegion' in opt.tag:

        if 'WZValidationRegionZLeps' in opt.tag:
            WZselection += ' && (mt2llfake0+mt2llfake1+mt2llfake2-mt2ll_WZ)>0.'

        cuts['WZ_3Lep_']            = { 'expr' : '(' + WZselection.replace('ZCUT', '999.').replace('METCUT',   '0') + ')', 'weight' : btagWeight0tag }
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

        cuts['ttZ_Zcut10']            = { 'expr' : '(' + ttZselection.replace('METCUT',   '0') + ')', 'weight' : btagWeight1tag }
        cuts['ttZ_Zcut10_ptmiss-140'] = { 'expr' : '(' + ttZselection.replace('METCUT', '140') + ')', 'weight' : btagWeight1tag }
        cuts['ttZ_Zcut10_ptmiss-160'] = { 'expr' : '(' + ttZselection.replace('METCUT', '160') + ')', 'weight' : btagWeight1tag }

        ttZselectionLarge = ttZselection.replace('deltaMassZ'+ctrltag+'<10.', 'deltaMassZ'+ctrltag+'<15.')

        cuts['ttZ_Zcut15']            = { 'expr' : '(' + ttZselectionLarge.replace('METCUT',   '0') + ')', 'weight' : btagWeight1tag }
        cuts['ttZ_Zcut15_ptmiss-140'] = { 'expr' : '(' + ttZselectionLarge.replace('METCUT', '140') + ')', 'weight' : btagWeight1tag }
        cuts['ttZ_Zcut15_ptmiss-160'] = { 'expr' : '(' + ttZselectionLarge.replace('METCUT', '160') + ')', 'weight' : btagWeight1tag }

    elif 'ZZValidationRegion' in opt.tag:

        ZZselection = sel4Lep + ' && deltaMassZ'+ctrltag+'<15. && ptmiss'+ctrltag+'>=METCUT'

        cuts['ZZ']            = { 'expr' : '(' + ZZselection.replace('METCUT',   '0') + ')', 'weight' : btagWeight0tag }
        cuts['ZZ_ptmiss-140'] = { 'expr' : '(' + ZZselection.replace('METCUT', '140') + ')', 'weight' : btagWeight0tag }
        cuts['ZZ_ptmiss-160'] = { 'expr' : '(' + ZZselection.replace('METCUT', '160') + ')', 'weight' : btagWeight0tag }

if 'ttZNormalization' in opt.tag or 'FitCRttZ' in opt.tag:

    ttZcommon = 'deltaMassZ_ctrltag<15. && deltaMassZ_ctrltag>=0. && ptmiss_ctrltag>=0.'
    if 'Z10' in opt.tag:
        ttZcommon = ttZcommon.replace('deltaMassZ_ctrltag<15.', 'deltaMassZ_ctrltag<10.')
    ttZ3Lep = nLooseLepton+'==3 && '+ttZcommon.replace('_ctrltag', '_WZtoWW' )
    ttZ4Lep = nLooseLepton+'==4 && '+ttZcommon.replace('_ctrltag', '_ttZ')
    ptmissTTZ3Lep = ptmissNano if 'NoZ' in opt.tag else ptmiss_ttZ3Lep
    ptmissTTZ4Lep = ptmissNano if 'NoZ' in opt.tag else 'ptmiss_ttZ'
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

    if 'Paper2016' in opt.tag or 'METBins2016' in opt.tag:
        ptmiss_cuts={"SR1": ' && ptmiss>=140 && ptmiss<200 ',
                     "SR2": ' && ptmiss>=200 && ptmiss<300 ',
                     "SR3": ' && ptmiss>=300 '}
    else:
        ptmiss_cuts={"SR1": ' && ptmiss>=160 && ptmiss<220 ',
                     "SR2": ' && ptmiss>=220 && ptmiss<280 ',
                     "SR3": ' && ptmiss>=280 && ptmiss<380 ',
                     "SR4": ' && ptmiss>=380 '}
        if 'TChipmWWSignalRegions' in opt.tag:
            ptmiss_cuts['SR1'] = ptmiss_cuts['SR1'].replace('ptmiss>=160', 'ptmiss>=140')

    SRlist = ptmiss_cuts.keys()
    for sr in SRlist:
        if '_no'+sr in opt.tag:
            del ptmiss_cuts[sr]

    isrRegions = [ ]
    if 'StopSignalRegions' in opt.tag: 
        if 'NoISR' not in opt.tag: 
            if 'ISR4' not in opt.tag: isrRegions.append('SR3')
            isrRegions.append('SR4')
    elif 'CharginoSignalRegions' in opt.tag or 'TChipmWWSignalRegions' in opt.tag:
        if 'ISR' in opt.tag:
            if 'ISR4' not in opt.tag: isrRegions.append('SR3')
            isrRegions.append('SR4') 

    for SR in ptmiss_cuts:

        isrcut = ''
        if SR in isrRegions: isrcut=' && '+ISRCut

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

    isStrictDatacardOrPlot = 'FitCRWZ' not in opt.tag and 'FitCRttZ' not in opt.tag and 'FitCRZZ' not in opt.tag

    for cut in cuts:
        if 'SR' in cut or 'VR1' in cut:

            if not isStrictDatacardOrPlot:
                cutToRemove.append(cut)

            if '_em' in cut: continue # Use only sf channel to avoid double counting

            crcut = cut.replace('SR', 'CR').replace('VR1', 'CR0')
            exprcut = cuts[cut]['expr']
            exprcut = exprcut.replace(' && '+DF, '')
            exprcut = exprcut.replace(' && '+SF, '')

            if '_Tag_' in cut and ('FitCRttZ' in opt.tag or isStrictDatacardOrPlot):

                if isDatacardOrPlot: # Ugly, but in this case these variables are not used
                    ttZselectionLoose = ''
                    btagweightmixtag = '1.'

                exprCR = exprcut.replace('ptmiss_phi', ptmiss_phi_ttZLoose)
                exprCR = exprCR.replace('ptmiss>', ptmiss_ttZLoose+'>')
                exprCR = exprCR.replace('ptmiss<', ptmiss_ttZLoose+'<')
                exprCR = exprCR.replace(OC, ttZselectionLoose)
                crcuts[crcut.replace('_sf', '_ttZ')] = { 'expr' : exprCR, 'weight' : btagweightmixtag }

            if '_Tag_' not in cut and ('FitCRWZ' in opt.tag or isStrictDatacardOrPlot):
             
                exprCR = exprcut.replace(OC, nLooseLepton+'==3 && ' + nTightLepton + '==3 && deltaMassZ_WZ<999. && ptmiss_WZ>=0.')
                exprCR = exprCR.replace('ptmiss>', 'ptmiss_WZ>')
                exprCR = exprCR.replace('ptmiss<', 'ptmiss_WZ<')
                exprCR = exprCR.replace('ptmiss_phi', 'ptmiss_phi_WZ')
                crcuts[crcut.replace('_sf', '_WZ')] = { 'expr' : exprCR, 'weight' : cuts[cut]['weight'] }

            if '_Tag_' not in cut and ('FitCRZZ' in opt.tag or isStrictDatacardOrPlot): 

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
    if opt.postFit!='n' and 'Fit' not in opt.postFit:
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

if 'SignalRegion' in opt.tag or 'ValidationRegion' in opt.tag:

    for sample in samples:

        cutToRemove = [ ]

        for cut in cuts:
            if (('SR' in cut or 'VR1' in cut) and 'isControlSample' in samples[sample] and samples[sample]['isControlSample']==1) or ('CR' in cut and samples[sample]['isSignal']==1):
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

            exclusiveSelection = True

            for region in normBackgrounds[background]:

                if 'exclusiveSelection' in normBackgrounds[background][region] and not normBackgrounds[background][region]['exclusiveSelection']: 
                    exclusiveSelection = False

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

            if len(normBackgroundNuisances[background].keys())>0:

                if not exclusiveSelection and hasattr(opt, 'doHadd') and not opt.doHadd:
                    # Tricky because we can't define a weight for one sample and one cut!
                    # We need to run only on the background to which the SF apply. For other samples, L673 saves us!
                    for othersample in samples:
                        if othersample!=background:
                            print 'Error: scale factors for', background, 'do not have exclusive selection: please run on this sample separately!'
                            exit()

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
                            if exclusiveSelection:
                                samples[background]['weight'] += '*'+regionWeight
                            else:
                                for cut in cuts:                       
                                    if cut in normBackgroundNuisances[background][region]['cuts']:
                                        if 'weight' in cuts[cut]:
                                            cuts[cut]['weight'] += '*'+regionWeight           
                                        else:
                                            cuts[cut]['weight'] = regionWeight

                        normBackgroundNuisances[background][region]['type'] = nuisanceType
   
                        if nuisanceType=='lnN':

                            normBackgroundNuisances[background][region]['samples'] = { background : str(1.+scaleFactorRelativeError) }
                         
                        else:
 
                            regionWeightUp   = '((!'+regionCut+')+('+regionCut+')*'+str(1.+scaleFactorRelativeError)+')'
                            regionWeightDown = '((!'+regionCut+')+('+regionCut+')*'+str(1.-scaleFactorRelativeError)+')' 

                            normBackgroundNuisances[background][region]['kind'] = 'weight'
                            normBackgroundNuisances[background][region]['samples'] = { background : [ regionWeightUp, regionWeightDown ] }
   


