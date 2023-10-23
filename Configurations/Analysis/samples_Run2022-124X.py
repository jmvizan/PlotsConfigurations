import os
import subprocess
import math
import string
from LatinoAnalysis.Tools.commonTools import *

### Generals

opt.campaign = 'Summer22'
#if 'Summer22v11' in opt.tag: opt.campaign = 'Summer22v11'
#elif 'Summer22EEv11' in opt.tag: opt.campaign = 'Summer22EEv11'
#elif 'Summer22EE' in opt.tag: opt.campaign = 'Summer22EE'
if 'Summer22EE' in opt.tag: opt.campaign = 'Summer22EE'

opt.CME = '13.6'
opt.lumi = 1. if 'Validation' in opt.tag else 26.337 if 'Summer22EE' in opt.campaign else 7.875

opt.simulationPileupFile = 'pileup_DistrWinter22_Run3_2022_LHC_Simulation_10h_2h.root'
if 'Summer22EE' in opt.campaign: opt.dataPileupFile = '/afs/cern.ch/work/s/scodella/BTagging/CMSSW_10_6_28/src/LatinoAnalysis/NanoGardener/python/data/PUweights/2022/2022EFG.root'
elif 'Summer22' in opt.campaign: opt.dataPileupFile = '/afs/cern.ch/work/s/scodella/BTagging/CMSSW_10_6_28/src/LatinoAnalysis/NanoGardener/python/data/PUweights/2022/2022CD.root'

fragTune = 'fragCP5BL'
jetEnergyUncertaintyFile = 'Summer22EEPrompt22_V1_MC_Uncertainty_AK4PFPuppi.txt' if 'Summer22EE' in opt.campaign else 'Summer22Prompt22_V1_MC_Uncertainty_AK4PFPuppi.txt'

treePrefix = ''

opt.method = 'System8' if 'System8' in opt.tag else 'PtRel'

### Process utilities

isDatacardOrPlot = hasattr(opt, 'outputDirDatacard') or hasattr(opt, 'postFit') or hasattr(opt, 'skipLNN') or hasattr(opt, 'inputDirMaxFit')
isPlot = hasattr(opt, 'postFit')
isShape = hasattr(opt, 'doHadd')
isFillShape = isShape and not opt.doHadd
opt.isShape = isShape

if isFillShape and 'MergedLight' in opt.tag:
    print 'Cannot fill shapes for', opt.tag, 'directly from trees'
    exit()

### Directories

skipTreesCheck = False if isShape or 'WorkingPoints' not in opt.tag else True

if not isDatacardOrPlot and 'WorkingPoints' not in opt.tag: 
    if skipTreesCheck:
        print 'Error: it is not allowed to fill shapes and skipping trees check!'
        exit()
    if opt.sigset=='SM' and hasattr(opt, 'doHadd') and not opt.doHadd:
        print 'Error: SM cannot be used when filling the shapes. Use Data and MC separately instead' 

SITE=os.uname()[1]
if 'cern' not in SITE and 'ifca' not in SITE and 'cloud' not in SITE: SITE = 'cern'

if 'cern' in SITE:
    treeBaseDirMC   = '/eos/cms/store/group/phys_btag/milee/BTA_addPFMuons_NanoV12/'
    treeBaseDirData = '/eos/cms/store/group/phys_btag/milee/BTA_addPFMuons_NanoV12/'
else: print 'trees for', campaign, 'campaign available only at cern'

ProductionMC   = opt.campaign
ProductionData = opt.campaign
  
directoryBkg  = treeBaseDirMC   + ProductionMC   + '/' 
directoryData = treeBaseDirData + ProductionData + '/'

### Campaign parameters

# global parameters
minJetPt  =   20.
maxJetPt  = 1400.
maxJetEta = '2.5'

campaignRunPeriod = { 'year' : '2022' }
campaignRunPeriod['period']    = '2022EFG' if 'Summer22EE' in opt.campaign else '2022CD'
campaignRunPeriod['pileup']    = opt.campaign
campaignRunPeriod['prescales'] = opt.campaign

ptrelRange = (50, 0., 4.) if opt.method=='PtRel' else (70, 0., 7.)

# triggers
triggerInfos = { 'BTagMu_AK4DiJet20_Mu5'  : { 'jetPtRange' : [  '20.',   '50.' ], 'ptAwayJet' : '20.', 'ptTriggerEmulation' :  '30.', 'jetTrigger' :  'PFJet40', 'idx' : '32', 'idxJetTrigger' : '0' },
                 'BTagMu_AK4DiJet40_Mu5'  : { 'jetPtRange' : [  '50.',  '100.' ], 'ptAwayJet' : '30.', 'ptTriggerEmulation' :  '50.', 'jetTrigger' :  'PFJet40', 'idx' : '33', 'idxJetTrigger' : '0' },
                 'BTagMu_AK4DiJet70_Mu5'  : { 'jetPtRange' : [ '100.',  '140.' ], 'ptAwayJet' : '30.', 'ptTriggerEmulation' :  '80.', 'jetTrigger' :  'PFJet60', 'idx' : '34', 'idxJetTrigger' : '1' },
                 'BTagMu_AK4DiJet110_Mu5' : { 'jetPtRange' : [ '140.',  '200.' ], 'ptAwayJet' : '30.', 'ptTriggerEmulation' : '140.', 'jetTrigger' :  'PFJet80', 'idx' : '35', 'idxJetTrigger' : '2' },
                 'BTagMu_AK4DiJet170_Mu5' : { 'jetPtRange' : [ '200.',  '320.' ], 'ptAwayJet' : '30.', 'ptTriggerEmulation' : '200.', 'jetTrigger' : 'PFJet140', 'idx' : '36', 'idxJetTrigger' : '3' },
                 'BTagMu_AK4Jet300_Mu5'   : { 'jetPtRange' : [ '320.', '1400.' ], 'ptAwayJet' : '30.', 'ptTriggerEmulation' :   '0.', 'jetTrigger' : 'PFJet260', 'idx' : '37', 'idxJetTrigger' : '5' },
                }

# b-tagging algorithms
if opt.campaign=='Summer22':
    bTagWorkingPoints = {'DeepJetT': {'cut': '0.7183', 'discriminant': 'DeepFlavourBDisc'}, 'ParticleNetVT': {'cut': '0.7862', 'discriminant': 'PNetBDisc'}, 'ParTL': {'cut': '0.0849', 'discriminant': 'ParTBDisc'}, 'ParticleNetM': {'cut': '0.245', 'discriminant': 'PNetBDisc'}, 'ParticleNetL': {'cut': '0.047', 'discriminant': 'PNetBDisc'}, 'ParTM': {'cut': '0.4319', 'discriminant': 'ParTBDisc'}, 'ParTT': {'cut': '0.8482', 'discriminant': 'ParTBDisc'}, 'ParticleNetT': {'cut': '0.6734', 'discriminant': 'PNetBDisc'}, 'DeepJetM': {'cut': '0.3086', 'discriminant': 'DeepFlavourBDisc'}, 'DeepJetL': {'cut': '0.0583', 'discriminant': 'DeepFlavourBDisc'}, 'ParticleNetVVT': {'cut': '0.961', 'discriminant': 'PNetBDisc'}, 'ParTVVT': {'cut': '0.9874', 'discriminant': 'ParTBDisc'}, 'ParTVT': {'cut': '0.9151', 'discriminant': 'ParTBDisc'}, 'DeepJetVVT': {'cut': '0.9512', 'discriminant': 'DeepFlavourBDisc'}, 'DeepJetVT': {'cut': '0.8111', 'discriminant': 'DeepFlavourBDisc'}}
    btagAwayJetTagger, btagAwayJetDiscriminant = 'JBP', 'Bprob'
    btagAwayJetVariations = { 'AwayJetTag' : '2.866',  'AwayJetDown' : '1.397' , 'AwayJetUp' : '5.196' }

elif opt.campaign=='Summer22EE':
    bTagWorkingPoints = {'DeepJetT': {'cut': '0.73', 'discriminant': 'DeepFlavourBDisc'}, 'ParticleNetVT': {'cut': '0.8033', 'discriminant': 'PNetBDisc'}, 'ParTL': {'cut': '0.0897', 'discriminant': 'ParTBDisc'}, 'ParticleNetM': {'cut': '0.2605', 'discriminant': 'PNetBDisc'}, 'ParticleNetL': {'cut': '0.0499', 'discriminant': 'PNetBDisc'}, 'ParTM': {'cut': '0.451', 'discriminant': 'ParTBDisc'}, 'ParTT': {'cut': '0.8604', 'discriminant': 'ParTBDisc'}, 'ParticleNetT': {'cut': '0.6915', 'discriminant': 'PNetBDisc'}, 'DeepJetM': {'cut': '0.3196', 'discriminant': 'DeepFlavourBDisc'}, 'DeepJetL': {'cut': '0.0614', 'discriminant': 'DeepFlavourBDisc'}, 'ParticleNetVVT': {'cut': '0.9664', 'discriminant': 'PNetBDisc'}, 'ParTVVT': {'cut': '0.9893', 'discriminant': 'ParTBDisc'}, 'ParTVT': {'cut': '0.9234', 'discriminant': 'ParTBDisc'}, 'DeepJetVVT': {'cut': '0.9542', 'discriminant': 'DeepFlavourBDisc'}, 'DeepJetVT': {'cut': '0.8184', 'discriminant': 'DeepFlavourBDisc'}}
    btagAwayJetTagger, btagAwayJetDiscriminant = 'JBP', 'Bprob'
    btagAwayJetVariations = { 'AwayJetTag' : '3.057',  'AwayJetDown' : '1.492' , 'AwayJetUp' : '5.481' }

#elif opt.campaign=='Summer22v11':
#    bTagWorkingPoints = {'DeepJetM': {'cut': '0.303', 'discriminant': 'DeepFlavourBDisc'}, 'DeepJetT': {'cut': '0.7559', 'discriminant': 'DeepFlavourBDisc'}, 'DeepJetVVT': {'cut': '0.9659', 'discriminant': 'DeepFlavourBDisc'}, 'DeepJetVT': {'cut': '0.8531', 'discriminant': 'DeepFlavourBDisc'}, 'DeepJetL': {'cut': '0.0474', 'discriminant': 'DeepFlavourBDisc'}}
#    btagAwayJetTagger, btagAwayJetDiscriminant = 'JBP', 'Bprob'
#    btagAwayJetVariations = { 'AwayJetTag' : '2.866',  'AwayJetDown' : '1.397' , 'AwayJetUp' : '5.196' }
#
#elif opt.campaign=='Summer22EEv11':
#    bTagWorkingPoints = {'DeepJetM': {'cut': '0.3179', 'discriminant': 'DeepFlavourBDisc'}, 'DeepJetT': {'cut': '0.7696', 'discriminant': 'DeepFlavourBDisc'}, 'DeepJetVVT': {'cut': '0.9683', 'discriminant': 'DeepFlavourBDisc'}, 'DeepJetVT': {'cut': '0.8594', 'discriminant': 'DeepFlavourBDisc'}, 'DeepJetL': {'cut': '0.0492', 'discriminant': 'DeepFlavourBDisc'}}
#    btagAwayJetTagger, btagAwayJetDiscriminant = 'JBP', 'Bprob'
#    btagAwayJetVariations = { 'AwayJetTag' : '3.057',  'AwayJetDown' : '1.492' , 'AwayJetUp' : '5.481' }

if 'WorkingPoints' in opt.tag: # and 'v11' not in opt.campaign:
    bTagWorkingPoints[btagAwayJetTagger+'L'] = {'cut': btagAwayJetVariations['AwayJetDown'], 'discriminant': btagAwayJetDiscriminant}
    bTagWorkingPoints[btagAwayJetTagger+'M'] = {'cut': btagAwayJetVariations['AwayJetTag'] , 'discriminant': btagAwayJetDiscriminant}
    bTagWorkingPoints[btagAwayJetTagger+'T'] = {'cut': btagAwayJetVariations['AwayJetUp']  , 'discriminant': btagAwayJetDiscriminant}

if 'PtRelTemplates' in opt.tag:
    if btagAwayJetTagger+'T' not in bTagWorkingPoints:
        bTagWorkingPoints[btagAwayJetTagger+'T'] = {'cut': btagAwayJetVariations['AwayJetUp']  , 'discriminant': btagAwayJetDiscriminant}

if 'btag' in opt.tag:
    btagWPToRemove = []
    for btagwp in bTagWorkingPoints:
        if 'btagveto' in opt.tag:
           if opt.tag.split('btagveto')[1].split('_')[0] in btagwp:
               btagWPToRemove.append(btagwp)
        elif opt.tag.split('btag')[1].split('_')[0] not in btagwp:
           btagWPToRemove.append(btagwp)
    for btagwp in btagWPToRemove:
        del bTagWorkingPoints[btagwp]

# jet pt bins
if 'ProdFine' in opt.tag or 'Validation' in opt.tag:
    jetPtBins = { 'Pt20to30'    : [   '20.',   '30.' ], 'Pt30to40'     : [   '30.',   '40.' ], 'Pt40to50'    : [   '40.',   '50.' ], 'Pt50to60'     : [   '50.',   '60.' ], 
                  'Pt60to70'    : [   '60.',   '70.' ], 'Pt70to80'     : [   '70.',   '80.' ], 'Pt80to100'   : [   '80.',  '100.' ], 'Pt100to120'   : [  '100.',  '120.' ], 
                  'Pt120to140'  : [  '120.',  '140.' ], 'Pt140to160'   : [  '140.',  '160.' ], 'Pt160to200'  : [  '160.',  '200.' ], 'Pt200to260'   : [  '200.',  '260.' ], 
                  'Pt260to300'  : [  '260.',  '300.' ], 'Pt300to320'   : [  '300.',  '320.' ], 'Pt320to400'  : [  '320.',  '400.' ], 'Pt400to500'   : [  '400.',  '500.' ], 
                  'Pt500to600'  : [  '500.',  '600.' ], 'Pt600to800'   : [  '600.',  '800.' ], 'Pt800to1000' : [  '800.', '1000.' ], 'Pt1000to1400' : [ '1000.', '1400.' ], 
                 }
elif 'ProdRun2' in opt.tag or ('Templates' in opt.tag and 'Prod' not in opt.tag):
    jetPtBins = { 'Pt20to30'    : [   '20.',   '30.' ], 'Pt30to50'     : [   '30.',   '50.' ], 'Pt50to70'    : [   '50.',   '70.' ], 'Pt70to100'    : [   '70.',  '100.' ], 
                  'Pt100to140'  : [  '100.',  '140.' ], 'Pt140to200'   : [  '140.',  '200.' ], 'Pt200to300'  : [  '200.',  '300.' ], 'Pt300to600'   : [  '300.',  '600.' ], 
                  'Pt600to1000' : [  '600.', '1000.' ], 'Pt1000to1400' : [ '1000.', '1400.' ], 
                 }
elif opt.method+'Data' in opt.tag:
    jetPtBins = { }
    for trigger in triggerInfos:
        jetPtBins[trigger] = [ str(minJetPt), str(maxJetPt) ] 
else: 
    jetPtBins = { }
    for trigger in triggerInfos:
        jetPtBins[trigger] = triggerInfos[trigger]['jetPtRange']

if 'JetPt' in opt.tag:
    ptBinToRemove = []
    for ptbin in jetPtBins:
        if 'JetPtVeto' in opt.tag:
           if ptbin in opt.tag.split('JetPtVeto')[1].split('_')[0]:
               ptBinToRemove.append(ptbin)
        elif ptbin not in opt.tag.split('JetPt')[1].split('_')[0]:
           ptBinToRemove.append(ptbin)
    for ptbin in ptBinToRemove:
        del jetPtBins[ptbin]

# systematics

systematicVariations = [ '' ]

if 'Templates' in opt.tag:
    systematicVariations.extend([ 'MuPtUp', 'MuPtDown', 'MuDRUp', 'MuDRDown' ])
    if 'Validation' not in opt.tag and ('SM' in opt.sigset or 'MC' in opt.sigset): systematicVariations.extend([ 'JEUUp', 'JEUDown' ])
    if 'Light' not in opt.tag:
        systematicVariations.insert(1, 'AwayJetDown')
        systematicVariations.insert(1, 'AwayJetUp')

    if 'JEU' in opt.tag and 'Data' in opt.sigset:
        print 'No need to run JEU variations on data'
        exit()

applyBFragmentation = 1

# muon kinematics selection
  
if 'PtRel' in opt.method:
    muonKinBins = { 'Bin1' : { 'range' : [ str(minJetPt),         '30.' ], 'pt' : [ '5.', '6.', '8.' ], 'dr' : [ '0.20', '0.15', '999.' ] },
                    'Bin2' : { 'range' : [         '30.',         '80.' ], 'pt' : [ '5.', '6.', '8.' ], 'dr' : [ '0.15', '0.12', '999.' ] },
                    'Bin3' : { 'range' : [         '80.', str(maxJetPt) ], 'pt' : [ '5.', '6.', '8.' ], 'dr' : [ '0.12', '0.09', '999.' ] } }

elif 'System8' in opt.method:
    muonKinBins = { 'Bin1' : { 'range' : [ str(minJetPt), str(maxJetPt) ], 'pt' : [ '5.', '6.', '8.' ], 'dr' : [ '0.40', '0.30', '999.' ] } }

muonKinSelection = 'Central'
for systvar in systematicVariations:
    if 'Mu' in systvar and systvar in opt.tag: muonKinSelection = systvar

# pt-hat safety thresholds

if 'Light' not in opt.tag:
    pthatThresholds = {  20. :  60.,  30. :  85.,  50. : 120.,  80. : 160., 120. : 220., 
                        170. : 320., 300. : 440., 470. : 620., 600. : 720., 800. : 920. }
else:
    #pthatThresholds = {  30. : 200.,  50. : 200.,  80. : 200., 120. : 250., 170. : 340., 300. : 520. }
    pthatThresholds = {  80. : 200., 120. : 250., 170. : 340., 300. : 520. }

# kinematic weights setting
kinematicWeightsMap = { 'QCDMu'  : [ 'QCDMu', 'bjets', 'cjets', 'ljets', 'light' ],
                        'QCD'    : [ 'QCD' ],
                        'JetMET' : [ 'JetMET' ]
                       }

### Complex variables

# event
nJetMax = 20
goodPV  = 'PV_chi2<100.' # No nPV so far in the trees

# working points
jetPt   = 'Jet_pT'
if 'JEUDown' in opt.tag: jetPt = 'jetEnDown'
elif 'JEUUp' in opt.tag: jetPt = 'jetEnUp'
goodJetForDisc = '((JETIDX<nJet)*(Alt$('+jetPt+'[JETIDX],0.)>=30.)*(abs(Alt$(Jet_eta[JETIDX],5.))<'+maxJetEta+')*(Alt$(Jet_hadronFlavour[JETIDX],-1)==JETFLV)*(Alt$(Jet_tightID[JETIDX],0)==1))'
jetDisc = '(999999.*(!('+goodJetForDisc+')) + '+goodJetForDisc+'*(Alt$(Jet_BTAGDISC[JETIDX],999999.)))'

# kinematic weights
jetKinematicWeight = '*'.join([ 'Alt$('+x+'[JETIDX],1.)' for x in opt.tag.split('.') if opt.method not in x ]) if '.' in opt.tag else '1.'

# mu-jet
jetSel      = 'Jet_tightID==1 && abs(Jet_eta)<='+maxJetEta+' && '+jetPt+'>='+str(minJetPt)
#  muSel       = 'PFMuon_GoodQuality>=2 && PFMuon_pt>5. && abs(PFMuon_eta)<2.4 && PFMuon_IdxJet>=0'
#  muJetEvt    = 'Sum$('+muSel+')==1'
#  muPt        = 'Sum$(('+muSel+')*PFMuon_pt)'
#  muEta       = 'Sum$(('+muSel+')*PFMuon_eta)'
#  muPhi       = 'Sum$(('+muSel+')*PFMuon_phi)'
#  muPtRel     = 'Sum$(('+muSel+')*PFMuon_ptrel)'
#  muJetIdx    = 'Sum$(('+muSel+')*PFMuon_IdxJet)'
muJetEvt    = 'muonJetFinder[0]>=0'
muIdx       = 'abs(muonJetFinder[0])'
muPt        = 'PFMuon_pt['+muIdx+']'
muEta       = 'PFMuon_eta['+muIdx+']'
muPhi       = 'PFMuon_phi['+muIdx+']'
muPtRel     = 'PFMuon_ptrel['+muIdx+']'
muJetIdx    = 'abs(muonJetFinder[1])'
muJetPt     = jetPt+'['+muJetIdx+']'
muJetEta    = 'Jet_eta['+muJetIdx+']'
muJetPhi    = 'Jet_phi['+muJetIdx+']'
muJetSel    = muJetIdx+'>=0 && Jet_tightID['+muJetIdx+']==1 && abs('+muJetEta+')<='+maxJetEta
muJetDR     = 'sqrt(acos(cos('+muPhi+'-'+muJetPhi+'))*acos(cos('+muPhi+'-'+muJetPhi+'))+('+muEta+'-'+muJetEta+')*('+muEta+'-'+muJetEta+'))'
muJetKinematicWeight = jetKinematicWeight.replace('JETIDX',muJetIdx)

# away jet
awayDeltaPhi = 'acos(cos(Jet_phi-Jet_phi['+muJetIdx+']))'
awayDeltaEta = '(Jet_eta-Jet_eta['+muJetIdx+'])'
awayDeltaR   = 'sqrt('+awayDeltaPhi+'*'+awayDeltaPhi+'+'+awayDeltaEta+'*'+awayDeltaEta+')'

awayJetTagSelection = 'AwayJetTag'
for systvar in systematicVariations:
    if 'AwayJet' in systvar and systvar in opt.tag: awayJetTagSelection = systvar

if 'PtRel' in opt.method:
    awayJetNCut     = 'Sum$('+jetSel+' && '+awayDeltaR+'>1.5 && Jet_'+btagAwayJetDiscriminant+'>='+btagAwayJetVariations[awayJetTagSelection]+')==1'
    awayJetPtCut    = 'Sum$('+jetSel+' && '+awayDeltaR+'>1.5 && Jet_'+btagAwayJetDiscriminant+'>='+btagAwayJetVariations[awayJetTagSelection]+' && '+jetPt+'>=AWAYJETPTCUT)==1'
    awayJetLightCut = 'Sum$('+jetSel+' && '+awayDeltaR.replace(muJetIdx,'JETIDX')+'>1.5 && '+jetPt+'>=AWAYJETPTCUT)>=1'
    awayJetCut      = awayJetNCut+' && '+awayJetPtCut

elif 'System8' in opt.method: # Not sure System8 does really this
    #awayJetCut = 'Sum$('+jetSel+' && '+jetPt+'>=AWAYJETPTCUT && '+awayDeltaR+'>0.05 && Jet_'+btagAwayJetDiscriminant+'>=-999999.)>=1'
    awayJetCand = [ '('+str(ijet)+'<nJet && Alt$(Jet_tightID['+str(ijet)+'],0)==1 && abs(Alt$(Jet_eta['+str(ijet)+'],5.))<='+maxJetEta+' && '+str(ijet)+'!='+muJetIdx+' && Alt$('+jetPt+'['+str(ijet)+'],0.)>=AWAYJETPTCUT && Alt$(Jet_'+btagAwayJetDiscriminant+'['+str(ijet)+'],-9999999.)>=-999999. && Sum$('+jetSel+' && '+jetPt+'!='+muJetPt+' && '+jetPt+'>'+jetPt+'['+str(ijet)+'])==0)' for ijet in range(5) ]
    awayJetCut = '('+' || '.join(awayJetCand )+')'   

# trigger
bitIdx      = 'int(triggerIdx/32)'
triggerCut  = '( BitTrigger['+bitIdx+'] & ( 1 << (triggerIdx - '+bitIdx+'*32) ) )>0'
triggerEmul = 'Sum$('+jetSel+' && '+awayDeltaR+'>0.05 && '+jetPt+'>=TRGEMULJETPTCUT)>=1' 

# light jets
lightJetSel = '((JETIDX<nJet)*(Alt$(Jet_tightID[JETIDX],0)==1)*(abs(Alt$(Jet_eta[JETIDX],5.))<'+maxJetEta+')*(Alt$('+jetPt+'[JETIDX],-1.)>=PTMIN)*(Alt$('+jetPt+'[JETIDX],999999.)<PTMAX)*(Sum$(PFMuon_GoodQuality>=1 && PFMuon_IdxJet==JETIDX)==0)*(Sum$(Jet_tightID==1 && '+jetPt+'!='+jetPt+'[JETIDX] && Jet_'+btagAwayJetDiscriminant+'>='+btagAwayJetVariations['AwayJetDown']+')==0))'
lightJetPt     = 'Alt$('+jetPt+'[JETIDX],-999.)'
lightJetEta    = 'Alt$(Jet_eta[JETIDX],-999.)'

# light tracks
nLightTrkMax  = 50
trackJetIdx   = 'TrkInc_jetIdx'
trakPt        = 'TrkInc_pt'
trackJetDR    = muJetDR.replace(muJetIdx,'JETIDX').replace(muPhi,'TrkInc_phi[TRKIDX]').replace(muEta,'TrkInc_eta[TRKIDX]')
lightTrkPtRel = 'Alt$(TrkInc_ptrel[TRKIDX],-999.)'
lightTrkSel   = '((TRKIDX<nTrkInc)*(Alt$('+trackJetIdx+'[TRKIDX],-1)>=0)*(Alt$('+trakPt+'[TRKIDX],0.)>TRKPTCUT)*(abs(Alt$(TrkInc_eta[TRKIDX],5.))<2.4)*('+trackJetDR+'<TRKDRCUT))'
nLightTrkJet  = 'Sum$('+trackJetIdx+'==JETIDX && '+trakPt+'>TRKPTCUT && abs(TrkInc_eta)<2.4 && '+trackJetDR.replace('[TRKIDX]','')+'<TRKDRCUT)'

# generation weights
muJetFromB    = '(Jet_hadronFlavour['+muJetIdx+']==5)'
muJetFromC    = '(Jet_hadronFlavour['+muJetIdx+']==4)'
muJetFromL    = '(Jet_hadronFlavour['+muJetIdx+']<4)'
muJetNotFromB = '(Jet_hadronFlavour['+muJetIdx+']!=5)'

# gluon splitting
BHadronDeltaR    = 'sqrt(acos(cos(BHadron_phi-Jet_phi['+muJetIdx+']))*acos(cos(BHadron_phi-Jet_phi['+muJetIdx+']))+(BHadron_eta-Jet_eta['+muJetIdx+'])*(BHadron_eta-Jet_eta['+muJetIdx+']))'
isGluonSplitting = '(Sum$('+BHadronDeltaR+'<=0.4 && BHadron_hasBdaughter==0)>=2)' 

### MC

if 'SM' in opt.sigset or 'MC' in opt.sigset:

    qcdMuName = 'QCD_PT-PTHATBIN_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8'
    qcdName   = 'QCD_PT-PTHATBIN_TuneCP5_13p6TeV_pythia8'
    ttbarName = 'TTto4Q_TuneCP5_13p6TeV_powheg-pythia8'

    if opt.campaign=='Summer22':
        qcdMuPtHatBins = {'80to120': {'ext': '', 'xSec': '2536000*0.03807', 'events': '25037792', 'weight': '3.85599177435'}, '170to300': {'ext': '', 'xSec': '114200*0.06781', 'events': '36140731', 'weight': '0.214270762813'}, '300to470': {'ext': '', 'xSec': '7678*0.09136', 'events': '30002342', 'weight': '0.0233802441156'}, '600to800': {'ext': '', 'xSec': '180.6*0.1176', 'events': '19989674', 'weight': '0.00106247655665'}, '800to1000': {'ext': '', 'xSec': '30.89*0.1278', 'events': '39062066', 'weight': '0.000101063318054'}, '120to170': {'ext': '', 'xSec': '444900*0.05214', 'events': '18849346', 'weight': '1.23065733952'}, '50to80': {'ext': '', 'xSec': '15710000*0.0221', 'events': '40249032', 'weight': '8.62607080836'}, '30to50': {'ext': '', 'xSec': '114100000*0.01303', 'events': '30177962', 'weight': '49.2651889481'}, '470to600': {'ext': '', 'xSec': '630.3*0.1062', 'events': '17697354', 'weight': '0.00378236543158'}, '15to20': {'ext': '', 'xSec': '907100000*0.0032', 'events': '4529335', 'weight': '640.871121257'}, '20to30': {'ext': '', 'xSec': '420500000*0.00599', 'events': '29845469', 'weight': '84.3945524863'}, '1000': {'ext': '', 'xSec': '9.935*0.1341', 'events': '14214939', 'weight': '9.37241798927e-05'}}
        qcdPtHatBins = {'80to120': {'ext': '', 'xSec': '2762530*1', 'events': '30322655', 'weight': '91.1044893661'}, '170to300': {'ext': '', 'xSec': '19204300', 'events': '29279427', 'weight': '655.897398539'}, '300to470': {'ext': '', 'xSec': '7823', 'events': '57643751', 'weight': '0.135712889329'}, '600to800': {'ext': '', 'xSec': '186.9', 'events': '69239419', 'weight': '0.00269932940945'}, '1000to1400': {'ext': '', 'xSec': '9.4183', 'events': '20179760', 'weight': '0.000466720119565'}, '800to1000': {'ext': '', 'xSec': '32.293', 'events': '40198975', 'weight': '0.000803328940601'}, '120to170': {'ext': '', 'xSec': '471100', 'events': '30337885', 'weight': '15.5284391117'}, '1400to1800': {'ext': '', 'xSec': '0.84265', 'events': '6022016', 'weight': '0.000139928223372'}, '1800to2400': {'ext': '', 'xSec': '0.114943', 'events': '3269659', 'weight': '3.51544304773e-05'}, '2400to3200': {'ext': '', 'xSec': '0.00682981', 'events': '1991557', 'weight': '3.42938213669e-06'}, '3200': {'ext': '', 'xSec': '0.000165445', 'events': '720008', 'weight': '2.29782169087e-07'}, '50to80': {'ext': '', 'xSec': '19204300', 'events': '19859107', 'weight': '967.027369358'}, '30to50': {'ext': '', 'xSec': '114100000', 'events': '1189766', 'weight': '95901.2108263'}, '470to600': {'ext': '', 'xSec': '648.2', 'events': '27946458', 'weight': '0.0231943525723'}, '15to30': {'ext': '', 'xSec': '1327600000', 'events': '1149000', 'weight': '1155439.51262'}}

 
    elif opt.campaign=='Summer22EE':
        qcdMuPtHatBins = {'80to120': {'ext': '', 'xSec': '2536000*0.03807', 'events': '87607597', 'weight': '1.10202223672'}, '170to300': {'ext': '', 'xSec': '114200*0.06781', 'events': '108082012', 'weight': '0.0716483886329'}, '300to470': {'ext': '', 'xSec': '7678*0.09136', 'events': '103244272', 'weight': '0.0067941985198'}, '600to800': {'ext': '', 'xSec': '180.6*0.1176', 'events': '73223619', 'weight': '0.000290050673404'}, '800to1000': {'ext': '', 'xSec': '30.89*0.1278', 'events': '126511164', 'weight': '3.12046927337e-05'}, '120to170': {'ext': '', 'xSec': '444900*0.05214', 'events': '70757973', 'weight': '0.327837062263'}, '50to80': {'ext': '', 'xSec': '15710000*0.0221', 'events': '40955399', 'weight': '8.47729502037'}, '30to50': {'ext': '', 'xSec': '114100000*0.01303', 'events': '102915690', 'weight': '14.446028589'}, '470to600': {'ext': '', 'xSec': '630.3*0.1062', 'events': '72085714', 'weight': '0.000928587042919'}, '15to20': {'ext': '', 'xSec': '907100000*0.0032', 'events': '16191725', 'weight': '179.271819402'}, '20to30': {'ext': '', 'xSec': '420500000*0.00599', 'events': '97331894', 'weight': '25.8784135034'}, '1000': {'ext': '', 'xSec': '9.935*0.1341', 'events': '47539649', 'weight': '2.80246810405e-05'}}
        qcdPtHatBins = {'15to30': {'ext': '', 'xSec': '1327600000', 'events': '3998528', 'weight': '332022.184164'}, '30to50': {'ext': '', 'xSec': '114100000', 'events': '2425246', 'weight': '47046.7738118'}, '80to120': {'ext': '', 'xSec': '2762530*1', 'events': '29586146', 'weight': '93.3724182933'}, '170to300': {'ext': '', 'xSec': '19204300', 'events': '28601371', 'weight': '671.44683379'}, '300to470': {'ext': '', 'xSec': '7823', 'events': '53611420', 'weight': '0.14592040278'}, '600to800': {'ext': '', 'xSec': '186.9', 'events': '69768259', 'weight': '0.0026788686242'}, '1000to1400': {'ext': '', 'xSec': '9.4183', 'events': '22769295', 'weight': '0.000413640387197'}, '800to1000': {'ext': '', 'xSec': '32.293', 'events': '44147575', 'weight': '0.000731478456065'}, '120to170': {'ext': '', 'xSec': '471100', 'events': '31689138', 'weight': '14.866292671'}, '1400to1800': {'ext': '', 'xSec': '0.84265', 'events': '7216187', 'weight': '0.000116772195621'}, '1800to2400': {'ext': '', 'xSec': '0.114943', 'events': '3979678', 'weight': '2.88824874776e-05'}, '470to600': {'ext': '', 'xSec': '648.2', 'events': '27755516', 'weight': '0.0233539163891'}, '3200': {'ext': '', 'xSec': '0.000165445', 'events': '1011673', 'weight': '1.63536043761e-07'}, '50to80': {'ext': '', 'xSec': '19204300', 'events': '19940303', 'weight': '963.089678226'}, '2400to3200': {'ext': '', 'xSec': '0.00682981', 'events': '2238313', 'weight': '3.05132034706e-06'}}

    if 'Validation' in opt.tag:
        for pthatbin in qcdMuPtHatBins.keys():
            if pthatbin!='80to120': del qcdMuPtHatBins[pthatbin]
        for pthatbin in qcdPtHatBins.keys():
            if pthatbin!='80to120': del qcdPtHatBins[pthatbin]

    if 'WorkingPoints' in opt.tag or 'PtHatWeights' in opt.tag or 'Light' in opt.tag:

        nPtHatBins = len(qcdPtHatBins.keys())        

        qcdTrees = []
        for pth in qcdPtHatBins:
            if pth=='80to120' or 'WorkingPoints' not in opt.tag:
                ptHatTrees = getSampleFiles(directoryBkg+qcdName.replace('PTHATBIN',pth)+qcdPtHatBins[pth]['ext']+'/','',True,treePrefix,skipTreesCheck)
                if 'PtHatWeights' in opt.tag: samples['QCD_'+pth] = { 'name' : ptHatTrees }
                else: qcdTrees += ptHatTrees

        if 'WorkingPoints' in opt.tag or 'Light' in opt.tag:
            samples['QCD']   = { 'name' : qcdTrees, 'weight' : '1.', 'isSignal' : 0 }
            #if 'WorkingPoints' in opt.tag:
            #    samples['ttbar'] = { 'name' : getSampleFiles(directoryBkg+ttbarName+'/',ttbarName,True,treePrefix,skipTreesCheck), 'weight' : '1.', 'isSignal' : 0 }

        if 'PtHatWeights' not in opt.tag and 'Validation' not in opt.tag:
            for sample in samples:
                for pth in qcdPtHatBins:
                    addSampleWeight(samples, sample, qcdName.replace('PTHATBIN',pth).split('_',1)[-1], qcdPtHatBins[pth]['weight'])

    if 'PtHatWeights' in opt.tag or opt.method+'Kinematics' in opt.tag or 'DataKinematics' in opt.tag or opt.method+'Templates' in opt.tag:

        nPtHatBins = len(qcdMuPtHatBins.keys())

        qcdMuTrees = []
        for pth in qcdMuPtHatBins:
            ptHatTrees = getSampleFiles(directoryBkg+qcdMuName.replace('PTHATBIN',pth)+qcdMuPtHatBins[pth]['ext']+'/','',True,treePrefix,skipTreesCheck)
            if 'PtHatWeights' in opt.tag: samples['QCDMu_'+pth] = { 'name' : ptHatTrees }
            else: qcdMuTrees += ptHatTrees

        if opt.method+'Kinematics' in opt.tag or 'DataKinematics' in opt.tag:
            samples['QCDMu'] = { 'name' : qcdMuTrees, 'weight'   : muJetKinematicWeight               , 'isSignal' : 0 }

        elif opt.method+'Templates' in opt.tag:
            samples['bjets'] = { 'name' : qcdMuTrees, 'weight'   : muJetKinematicWeight+'*'+muJetFromB, 'isSignal' : 1 }
            if 'PtRel' in opt.method:
                samples['cjets'] = { 'name' : qcdMuTrees, 'weight'   : muJetKinematicWeight+'*'+muJetFromC, 'isSignal' : 0 }
                samples['ljets'] = { 'name' : qcdMuTrees, 'weight'   : muJetKinematicWeight+'*'+muJetFromL, 'isSignal' : 0 }
            elif 'System8' in opt.method:
                samples['light'] = { 'name' : qcdMuTrees, 'weight'   : muJetKinematicWeight+'*'+muJetNotFromB, 'isSignal' : 0 }

        if 'PtHatWeights' not in opt.tag and 'Validation' not in opt.tag:
            for sample in samples:
                for pth in qcdMuPtHatBins:
                    addSampleWeight(samples, sample, qcdMuName.replace('PTHATBIN',pth).split('_',1)[-1], qcdMuPtHatBins[pth]['weight'])

# Common MC keys

for sample in samples:

    samples[sample]['isDATA']    = 0
    samples[sample]['isFastsim'] = 0
    samples[sample]['treeType']  = 'MC'
    samples[sample]['suppressNegative']          = ['all']
    samples[sample]['suppressNegativeNuisances'] = ['all']
    samples[sample]['suppressZeroTreeNuisances'] = ['all']
    samples[sample]['split'] = 'AsMuchAsPossible'
    samples[sample]['JobsPerSample'] = 20*nPtHatBins if 'Light' in opt.tag else 8*nPtHatBins
    if isPlot or opt.method!='PtRel': samples[sample]['isSignal']  = 0

### Data

if 'SM' in opt.sigset or 'Data' in opt.sigset:

    dataName = 'BTagMu' if opt.method+'Kinematics' in opt.tag or opt.method+'Templates' in opt.tag or 'DataKinematics' in opt.tag else 'JetMET'

    runPeriods = {}
    if 'Summer22EE' in opt.campaign:
        #runPeriods['Run2022E'] = { 'subdir' : dataName + 'Run2022E-27Jun2023-v1'  }
        runPeriods['Run2022F'] = { 'subdir' : dataName + 'Run2022F-PromptReco-v1' }
        runPeriods['Run2022G'] = { 'subdir' : dataName + 'Run2022F-PromptReco-v1' }
    elif 'Summer22' in opt.campaign:
        if dataName=='BTagMu':
            runPeriods['Run2022C'] = { 'subdir' : dataName + 'Run2022C-27Jun2023-v2' }
            runPeriods['Run2022D'] = { 'subdir' : dataName + 'Run2022C-27Jun2023-v1' }
        else:
            runPeriods['Run2022C'] = { 'subdir' : dataName + 'Run2022C-27Jun2023-v1' }
            runPeriods['Run2022D'] = { 'subdir' : dataName + 'Run2022C-27Jun2023-v2' }

    dataTrees = [ ]
    for runPeriod in runPeriods:
  
        sampleName = ''
        dataDir = '/'.join([ directoryData, runPeriods[runPeriod]['subdir'], '' ]) 
        dataTrees += getSampleFiles(dataDir,  sampleName, True, treePrefix, skipTreesCheck)
 
    if dataName=='BTagMu': dataName = 'DATA'
    samples[dataName]  = { 'name'      : dataTrees ,
                           'weight'    : '1.' ,
                           'isData'    : ['all'] ,
                           'treeType'  : 'Data' ,
                           'isSignal'  : 0 ,
                           'isDATA'    : 1 ,
                           'isFastsim' : 0 ,
                           'split'     : 'AsMuchAsPossible',
                           'JobsPerSample' : 20*len(runPeriods.keys()) if 'Light' in opt.tag else 8*len(runPeriods.keys())
                          }
     
### Files per job

removeFromSplit = []
 
for sample in samples:
    if 'FilesPerJob' not in samples[sample]:
        ntrees = len(samples[sample]['name']) 
        multFactor = 6 if 'JobsPerSample' not in samples[sample] else int(samples[sample]['JobsPerSample'])
        filesPerJob = int(math.ceil(float(ntrees)/multFactor))
        if filesPerJob>1: samples[sample]['FilesPerJob'] = filesPerJob
        else: removeFromSplit.append(sample)

for sample in removeFromSplit:
    del samples[sample]['split']

### Cleaning

if opt.sigset.split('-')[0] not in [ 'SM', 'MC', 'Data' ]:

    sampleToRemove = [ ]

    shortset = opt.sigset.split('-')[0]

    for sample in samples:
        if 'Veto' in shortset:
            if sample in shortset:
                sampleToRemove.append(sample)
        elif sample not in shortset: # Be sure this sample's name is not substring of other samples' names
            sampleToRemove.append(sample)

    for sample in sampleToRemove:
        del samples[sample]

### Nasty clean up for eos

if 'cern' in SITE:
    for sample in samples:
        for ifile in range(len(samples[sample]['name'])):
            samples[sample]['name'][ifile] = samples[sample]['name'][ifile].replace('root://eoscms.cern.ch/', '')



