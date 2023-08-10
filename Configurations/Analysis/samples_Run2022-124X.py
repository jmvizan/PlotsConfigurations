import os
import subprocess
import math
import string
from LatinoAnalysis.Tools.commonTools import *

### Generals

opt.method = 'System8' if 'System8' in opt.tag else 'PtRel'
opt.campaign = 'Summer22EE' if 'Summer22EE' in opt.tag else 'Summer22'
opt.CME = '13.6'
opt.lumi = 26.337 if 'Summer22EE' in opt.tag else 7.875
treePrefix= ''

isDatacardOrPlot = hasattr(opt, 'outputDirDatacard') or hasattr(opt, 'postFit') or hasattr(opt, 'skipLNN') or hasattr(opt, 'inputDirMaxFit')
isPlot = hasattr(opt, 'postFit')
isShape = hasattr(opt, 'doHadd')
isFillShape = isShape and not opt.doHadd
opt.isShape = isShape

if isFillShape and 'MergedLight' in opt.tag:
    print 'Cannot fill shapes for', opt.tag, 'directly from trees'
    exit()

### Directories

skipTreesCheck = False

if not isDatacardOrPlot: 
    if skipTreesCheck:
        print 'Error: it is not allowed to fill shapes and skipping trees check!'
        exit()
    if opt.sigset=='SM' and hasattr(opt, 'doHadd') and not opt.doHadd:
        print 'Error: SM cannot be used when filling the shapes. Use Data and MC separately instead' 

SITE=os.uname()[1]
if 'cern' not in SITE and 'ifca' not in SITE and 'cloud' not in SITE: SITE = 'cern'

if 'cern' in SITE:
    treeBaseDirMC   = '/eos/cms/store/group/phys_btag/milee/BTA/' if 'Short' not in opt.tag else '/eos/cms/store/user/scodella/BTV/'
    treeBaseDirData = '/eos/cms/store/group/phys_btag/milee/BTA/'
else: print 'trees for', campaign, 'available only at cern'

ProductionMC   = opt.campaign+'/'
ProductionData = opt.campaign+'/'

directoryBkg  = treeBaseDirMC   + ProductionMC 
directoryData = treeBaseDirData + ProductionData 

### Campaign parameters

# global parameters
minJetPt  =   20.
maxJetPt  = 1400.
maxJetEta = '2.5'

campaignRunPeriod = { 'year' : '2022' }
campaignRunPeriod['period'] = '2022EFG' if 'Summer22EE' in opt.tag else '2022CD'

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
    bTagWorkingPoints = {'DeepJetT': {'cut': '0.7217', 'discriminant': 'DeepFlavourBDisc'}, 'ParTL': {'cut': '0.0834', 'discriminant': 'ParTBDisc'}, 'ParTT': {'cut': '0.8506', 'discriminant': 'ParTBDisc'}, 'ParticleNetT': {'cut': '0.6685', 'discriminant': 'PNetBDisc'}, 'DeepJetM': {'cut': '0.3064', 'discriminant': 'DeepFlavourBDisc'}, 'DeepJetL': {'cut': '0.0575', 'discriminant': 'DeepFlavourBDisc'}, 'ParticleNetM': {'cut': '0.2421', 'discriminant': 'PNetBDisc'}, 'ParticleNetL': {'cut': '0.0462', 'discriminant': 'PNetBDisc'}, 'ParTM': {'cut': '0.4278', 'discriminant': 'ParTBDisc'}}
    #bTagWorkingPoints = {'DeepJetT': {'cut': '0.7217', 'discriminant': 'DeepFlavourBDisc'}, 'DeepJetV': {'cut': '0.8125', 'discriminant': 'DeepFlavourBDisc'}, 'DeepJetS': {'cut': '0.9498', 'discriminant': 'DeepFlavourBDisc'}, 'ParTL': {'cut': '0.0834', 'discriminant': 'ParTBDisc'}, 'ParticleNetM': {'cut': '0.2421', 'discriminant': 'PNetBDisc'}, 'ParticleNetL': {'cut': '0.0462', 'discriminant': 'PNetBDisc'}, 'ParTM': {'cut': '0.4278', 'discriminant': 'ParTBDisc'}, 'ParticleNetS': {'cut': '0.9615', 'discriminant': 'PNetBDisc'}, 'ParTS': {'cut': '0.9849', 'discriminant': 'ParTBDisc'}, 'ParTT': {'cut': '0.8506', 'discriminant': 'ParTBDisc'}, 'ParticleNetT': {'cut': '0.6685', 'discriminant': 'PNetBDisc'}, 'ParTV': {'cut': '0.9161', 'discriminant': 'ParTBDisc'}, 'ParticleNetV': {'cut': '0.7823', 'discriminant': 'PNetBDisc'}, 'DeepJetM': {'cut': '0.3064', 'discriminant': 'DeepFlavourBDisc'}, 'DeepJetL': {'cut': '0.0575', 'discriminant': 'DeepFlavourBDisc'}}
    btagAwayJetTagger, btagAwayJetDiscriminant = 'JBP', 'Bprob'
    btagAwayJetVariations = { 'Central' : '2.821',  'AwayJetDown' : '1.370' , 'AwayJetUp' : '5.129' }

elif opt.campaign=='Summer22EE':
    bTagWorkingPoints = {'DeepJetT': {'cut': '0.7134', 'discriminant': 'DeepFlavourBDisc'}, 'ParTL': {'cut': '0.0828', 'discriminant': 'ParTBDisc'}, 'ParTT': {'cut': '0.8443', 'discriminant': 'ParTBDisc'}, 'ParticleNetT': {'cut': '0.6651', 'discriminant': 'PNetBDisc'}, 'DeepJetM': {'cut': '0.3033', 'discriminant': 'DeepFlavourBDisc'}, 'DeepJetL': {'cut': '0.057', 'discriminant': 'DeepFlavourBDisc'}, 'ParticleNetM': {'cut': '0.2386', 'discriminant': 'PNetBDisc'}, 'ParticleNetL': {'cut': '0.0458', 'discriminant': 'PNetBDisc'}, 'ParTM': {'cut': '0.4244', 'discriminant': 'ParTBDisc'}}
    #bTagWorkingPoints = {'DeepJetT': {'cut': '0.7134', 'discriminant': 'DeepFlavourBDisc'}, 'DeepJetV': {'cut': '0.8067', 'discriminant': 'DeepFlavourBDisc'}, 'DeepJetS': {'cut': '0.9483', 'discriminant': 'DeepFlavourBDisc'}, 'ParTL': {'cut': '0.0828', 'discriminant': 'ParTBDisc'}, 'ParticleNetM': {'cut': '0.2386', 'discriminant': 'PNetBDisc'}, 'ParticleNetL': {'cut': '0.0458', 'discriminant': 'PNetBDisc'}, 'ParTM': {'cut': '0.4244', 'discriminant': 'ParTBDisc'}, 'ParticleNetS': {'cut': '0.9571', 'discriminant': 'PNetBDisc'}, 'ParTS': {'cut': '0.9864', 'discriminant': 'ParTBDisc'}, 'ParTT': {'cut': '0.8443', 'discriminant': 'ParTBDisc'}, 'ParticleNetT': {'cut': '0.6651', 'discriminant': 'PNetBDisc'}, 'ParTV': {'cut': '0.9117', 'discriminant': 'ParTBDisc'}, 'ParticleNetV': {'cut': '0.7789', 'discriminant': 'PNetBDisc'}, 'DeepJetM': {'cut': '0.3033', 'discriminant': 'DeepFlavourBDisc'}, 'DeepJetL': {'cut': '0.057', 'discriminant': 'DeepFlavourBDisc'}}
    btagAwayJetTagger, btagAwayJetDiscriminant = 'JBP', 'Bprob'
    btagAwayJetVariations = { 'Central' : '2.831',  'AwayJetDown' : '1.371' , 'AwayJetUp' : '5.129' }

if 'WorkingPoints' in opt.tag:
    bTagWorkingPoints[btagAwayJetTagger+'L'] = {'cut': btagAwayJetVariations['AwayJetDown'], 'discriminant': btagAwayJetDiscriminant}
    bTagWorkingPoints[btagAwayJetTagger+'M'] = {'cut': btagAwayJetVariations['Central']    , 'discriminant': btagAwayJetDiscriminant}
    bTagWorkingPoints[btagAwayJetTagger+'T'] = {'cut': btagAwayJetVariations['AwayJetUp']  , 'discriminant': btagAwayJetDiscriminant}

if '_btag' in opt.tag:
    btagWPToRemove = []
    for btagwp in bTagWorkingPoints:
        if opt.tag.split('_btag')[1].split('_')[0] not in btagwp:
           btagWPToRemove.append(btagwp)
    for btagwp in btagWPToRemove:
        del bTagWorkingPoints[btagwp]

# jet pt bins
if 'ProdFine' in opt.tag:
    jetPtBins = { 'Pt20to30'    : [   '20.',   '30.' ], 'Pt30to40'     : [   '30.',   '40.' ], 'Pt40to50'    : [   '40.',   '50.' ], 'Pt50to60'     : [   '50.',   '60.' ], 
                  'Pt60to70'    : [   '60.',   '70.' ], 'Pt70to80'     : [   '70.',   '80.' ], 'Pt80to100'   : [   '80.',  '100.' ], 'Pt100to120'   : [  '100.',  '120.' ], 
                  'Pt120to140'  : [  '120.',  '140.' ], 'Pt140to160'   : [  '140.',  '160.' ], 'Pt160to200'  : [  '160.',  '200.' ], 'Pt200to260'   : [  '200.',  '260.' ], 
                  'Pt260to300'  : [  '260.',  '300.' ], 'Pt300to320'   : [  '300.',  '320.' ], 'Pt320to400'  : [  '320.',  '400.' ], 'Pt400to500'   : [  '400.',  '500.' ], 
                  'Pt500to600'  : [  '500.',  '600.' ], 'Pt600to800'   : [  '600.',  '800.' ], 'Pt800to1000' : [  '800.', '1000.' ], 'Pt1000to1400' : [ '1000.', '1400.' ], 
                 }
elif 'ProdRun2' in opt.tag:
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

# muon kinematics bins
  
if 'PtRel' in opt.method:
    muonKinBins = { 'Bin1' : { 'range' : [ str(minJetPt),         '30.' ], 'pt' : [ '5.', '6.', '8.' ], 'dr' : [ '0.20', '0.15', '999.' ] },
                    'Bin2' : { 'range' : [         '30.',         '80.' ], 'pt' : [ '5.', '6.', '8.' ], 'dr' : [ '0.15', '0.12', '999.' ] },
                    'Bin3' : { 'range' : [         '80.', str(maxJetPt) ], 'pt' : [ '5.', '6.', '8.' ], 'dr' : [ '0.12', '0.09', '999.' ] } }

elif 'System8' in opt.method:
    muonKinBins = { 'Bin1' : { 'range' : [ str(minJetPt), str(maxJetPt) ], 'pt' : [ '5.', '6.', '8.' ], 'dr' : [ '0.40', '0.30', '999.' ] } }

# pt-hat safety thresholds

if 'Light' not in opt.tag:
    pthatThresholds = {  20. :  60.,  30. :  85.,  50. : 120.,  80. : 160., 120. : 220., 
                        170. : 320., 300. : 440., 470. : 620., 600. : 720., 800. : 920. }
else:
    #pthatThresholds = {  30. : 200.,  50. : 200.,  80. : 200., 120. : 250., 170. : 340., 300. : 520. }
    pthatThresholds = {  80. : 200., 120. : 250., 170. : 340., 300. : 520. }

# kinematic weights setting
kinematicWeightsMap = { 'QCDMu'  : [ 'QCDMu', 'bjets', 'light' ],
                        'QCD'    : [ 'QCD' ],
                        'JetHT'  : [ 'JetHT' ]
                       }

### Complex variables

# event
nJetMax = 20
goodPV  = 'PV_chi2<100.' # No nPV so far in the trees

# working points
goodJetForDisc = '((JETIDX<nJet)*(Alt$(Jet_pT[JETIDX],0.)>=30.)*(abs(Alt$(Jet_eta[JETIDX],5.))<'+maxJetEta+')*(Alt$(Jet_hadronFlavour[JETIDX],-1)==JETFLV)*(Alt$(Jet_tightID[JETIDX],0)==1))'
jetDisc = '(999999.*(!('+goodJetForDisc+')) + '+goodJetForDisc+'*(Alt$(Jet_BTAGDISC[JETIDX],999999.)))'

# kinematic weights
jetKinematicWeight = '*'.join([ x+'[JETIDX]' for x in opt.tag.split(':') if opt.method not in x ]) if ':' in opt.tag else '1.'

# mu-jet
jetPt    = 'Jet_pT'
jetSel   = 'Jet_tightID==1 && abs(Jet_eta)<='+maxJetEta+' && '+jetPt+'>='+str(minJetPt)
muSel    = 'PFMuon_GoodQuality>=2 && PFMuon_pt>5. && abs(PFMuon_eta)<2.4 && PFMuon_IdxJet>=0'
muJetEvt = 'Sum$('+muSel+')==1'
muPt     = 'Sum$(('+muSel+')*PFMuon_pt)'
muEta    = 'Sum$(('+muSel+')*PFMuon_eta)'
muPhi    = 'Sum$(('+muSel+')*PFMuon_phi)'
muPtRel  = 'Sum$(('+muSel+')*PFMuon_ptrel)'
muJetIdx = 'Sum$(('+muSel+')*PFMuon_IdxJet)'
muJetPt  = jetPt+'['+muJetIdx+']'
muJetEta = 'Jet_eta['+muJetIdx+']'
muJetPhi = 'Jet_phi['+muJetIdx+']'
muJetSel = muJetIdx+'>=0 && Jet_tightID['+muJetIdx+']==1 && abs('+muJetEta+')<='+maxJetEta
muJetDR  = 'sqrt(acos(cos('+muPhi+'-'+muJetPhi+'))*acos(cos('+muPhi+'-'+muJetPhi+'))+('+muEta+'-'+muJetEta+')*('+muEta+'-'+muJetEta+'))'
muJetKinematicWeight = jetKinematicWeight.replace('JETIDX',muJetIdx)

# away jet
awayDeltaPhi = 'acos(cos(Jet_phi-Jet_phi['+muJetIdx+']))'
awayDeltaEta = '(Jet_eta-Jet_eta['+muJetIdx+'])'
awayDeltaR   = 'sqrt('+awayDeltaPhi+'*'+awayDeltaPhi+'+'+awayDeltaEta+'*'+awayDeltaEta+')'

if 'PtRel' in opt.method:
    awayJetNCut     = 'Sum$('+jetSel+' && '+awayDeltaR+'>1.5 && Jet_'+btagAwayJetDiscriminant+'>='+btagAwayJetVariations['Central']+')==1'
    awayJetPtCut    = 'Sum$('+jetSel+' && '+awayDeltaR+'>1.5 && Jet_'+btagAwayJetDiscriminant+'>='+btagAwayJetVariations['Central']+' && '+jetPt+'>=AWAYJETPTCUT)==1'
    awayJetLightCut = 'Sum$('+jetSel+' && '+awayDeltaR.replace(muJetIdx,'JETIDX')+'>1.5 && '+jetPt+'>=AWAYJETPTCUT)>=1'
    awayJetCut      = awayJetNCut+' && '+awayJetPtCut

elif 'System8' in opt.method: # Not sure System8 does really this
    isTaggedLeadingJet  = jetPt+'=='+jetPt+'[0] && Jet_'+btagAwayJetDiscriminant+'>=-999999.'
    isTaggedTrailingJet = isTaggedLeadingJet.replace('[0]','[1]')
    muJetIsLeadingJet = muJetPt+'=='+jetPt+'[0]'
    isTaggedAwayJet = '( ('+isTaggedLeadingJet+') || ('+isTaggedTrailingJet+' && '+muJetIsLeadingJet+') )'
    awayJetCut = 'Sum$('+jetSel+' && '+jetPt+'>=AWAYJETPTCUT && '+awayDeltaR+'>0.05 && '+isTaggedAwayJet+')>=1'

# trigger
bitIdx      = 'int(triggerIdx/32)'
triggerCut  = '( BitTrigger['+bitIdx+'] & ( 1 << (triggerIdx - '+bitIdx+'*32) ) )>0'
triggerEmul = 'Sum$('+jetSel+' && '+awayDeltaR+'>0.05 && '+jetPt+'>=TRGEMULJETPTCUT)>=1' 

# light jets
lightJetSel = '((JETIDX<nJet)*(Alt$(Jet_tightID[JETIDX],0)==1)*(abs(Alt$(Jet_eta[JETIDX],5.))<'+maxJetEta+')*(Alt$('+jetPt+'[JETIDX],-1.)>=PTMIN)*(Alt$('+jetPt+'[JETIDX],999999.)<PTMAX)*(Sum$(PFMuon_GoodQuality>=1 && PFMuon_IdxJet==JETIDX)==0)*(Sum$(Jet_tightID==1 && '+jetPt+'!='+jetPt+'[JETIDX] && Jet_'+btagAwayJetDiscriminant+'>='+btagAwayJetVariations['AwayJetDown']+')==0))'
lightJetPt  = 'Alt$('+jetPt+'[JETIDX],-999.)'
lightJetEta = 'Alt$(Jet_eta[JETIDX],-999.)'

# light tracks
nLightTrkMax  = 50
trackJetIdx   = 'TrkInc_jetIdx'
trakPt        = 'TrkInc_pt'
trackJetDR    = muJetDR.replace(muJetIdx,'JETIDX').replace(muPhi,'TrkInc_phi[TRKIDX]').replace(muEta,'TrkInc_eta[TRKIDX]')
lightTrkPtRel = 'Alt$(TrkInc_ptrel[TRKIDX],-999.)'
lightTrkSel   = '((TRKIDX<nTrkInc)*('+trackJetIdx+'[TRKIDX]>=0)*(Alt$('+trakPt+'[TRKIDX],0.)>TRKPTCUT)*(abs(Alt$(TrkInc_eta[TRKIDX],5.))<2.4)*('+trackJetDR+'<TRKDRCUT))'
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
        qcdMuPtHatBins = {'15to20': {'ext': '', 'xSec': '892600000*0.00328', 'events': '987', 'weight': '2966289.76697'}}
        qcdPtHatBins = {'80to120': {'ext': '_ext1', 'xSec': '2762530*1', 'events': '29798700', 'weight': '92.7063932319'}}

    elif opt.campaign=='Summer22EE':
        qcdMuPtHatBins = {}
        qcdPtHatBins = {'80to120': {'xSec': '2762530*1', 'events': '29920690', 'weight': '92.3284188968', 'ext' : ''}}

    if 'WorkingPoints' in opt.tag or 'PtHatWeights' in opt.tag or 'Light' in opt.tag:

        qcdTrees = []
        for pth in qcdPtHatBins:
            if pth=='80to120' or 'WorkingPoints' not in opt.tag:
                ptHatTrees = getSampleFiles(directoryBkg+qcdName.replace('PTHATBIN',pth)+qcdPtHatBins[pth]['ext']+'/',qcdName.replace('PTHATBIN',pth),True,treePrefix,skipTreesCheck)
                if 'PtHatWeights' in opt.tag: samples['QCD_'+pth] = { 'name' : ptHatTrees }
                else: qcdTrees += ptHatTrees

        if 'WorkingPoints' in opt.tag or 'Light' in opt.tag:
            samples['QCD']   = { 'name' : qcdTrees, 'weight' : '1.', 'isSignal' : 0 }
            if 'WorkingPoints' in opt.tag:
                samples['ttbar'] = { 'name' : getSampleFiles(directoryBkg+ttbarName+'/',ttbarName,True,treePrefix,skipTreesCheck), 'weight' : '1.', 'isSignal' : 0 }

        for sample in samples:
            for treeName in samples[sample]['name']:
                for pth in qcdPtHatBins:
                    if qcdName.replace('PTHATBIN',pth) in treeName.split('/')[-1]:
                        addSampleWeight(samples, sample, treeName.split('/')[-1].split('_',1)[-1].replace('.root',''), qcdPtHatBins[pth]['weight'])

    else:

        qcdMuTrees = []
        for pth in qcdMuPtHatBins:
            ptHatTrees = getSampleFiles(directoryBkg+qcdMuName.replace('PTHATBIN',pth)+qcdMuPtHatBins[pth]['ext']+'/',qcdMuName.replace('PTHATBIN',pth),True,treePrefix,skipTreesCheck)
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

        for sample in samples:
            for treeName in samples[sample]['name']:
                for pth in qcdMuPtHatBins:
                    if qcdMuName.replace('PTHATBIN',pth) in treeName.split('/')[-1]:
                        addSampleWeight(samples, sample, treeName.split('/')[-1].split('_',1)[-1].replace('.root',''), qcdMuPtHatBins[pth]['weight'])

# Common MC keys

for sample in samples:

    samples[sample]['isDATA']    = 0
    samples[sample]['isFastsim'] = 0
    samples[sample]['treeType']  = 'MC'
    samples[sample]['suppressNegative']          = ['all']
    samples[sample]['suppressNegativeNuisances'] = ['all']
    samples[sample]['suppressZeroTreeNuisances'] = ['all']
    samples[sample]['split'] = 'AsMuchAsPossible'
    samples[sample]['JobsPerSample'] = 20
    if isPlot or opt.method!='PtRel': samples[sample]['isSignal']  = 0

### Data

if 'SM' in opt.sigset or 'Data' in opt.sigset:

    runPeriods = [ 'Run2017B', 'Run2017C', 'Run2017D', 'Run2017E', 'Run2017F' ]

    if opt.method+'Kinematics' in opt.tag or opt.method+'Templates' in opt.tag or 'DataKinematics' in opt.tag:
    
        btagTrees = [ ]
        for runPeriod in runPeriods:
            btagTrees += getSampleFiles(directoryData,'BTagMu_'+runPeriod,True,treePrefix,skipTreesCheck)
 
        samples['DATA']  = { 'name'      : btagTrees ,
                             'weight'    : METFilters_Data+'*'+VetoEENoise ,
                             'isData'    : ['all'] ,
                             'treeType'  : 'Data' ,
                             'isSignal'  : 0 ,
                             'isDATA'    : 1 ,
                             'isFastsim' : 0 ,
                             'split'     : 'AsMuchAsPossible'
                            }
     
    if opt.method=='PtRel' and ('LightKinematics' in opt.tag or 'LightTemplates' in opt.tag):
        pass

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



