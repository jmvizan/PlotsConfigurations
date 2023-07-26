import os
import subprocess
import math
import string
from LatinoAnalysis.Tools.commonTools import *

### Generals

opt.method = 'System8' if 'System8' in opt.tag else 'PtRel'
opt.campaign = 'Summer22EE' if 'Summer22EE' in opt.tag else 'Summer22'
opt.CME = '13.6'
opt.lumi = 1. if 'Summer22EE' in opt.tag else 1.
treePrefix= ''

isDatacardOrPlot = hasattr(opt, 'outputDirDatacard') or hasattr(opt, 'postFit') or hasattr(opt, 'skipLNN') or hasattr(opt, 'inputDirMaxFit')
isPlot = hasattr(opt, 'postFit')

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
    treeBaseDirMC   = '/eos/cms/store/group/phys_btag/milee/BTA/'
    treeBaseDirData = '/eos/cms/store/group/phys_btag/milee/BTA/'
else: print 'trees for', campaign, 'available only at cern'

ProductionMC   = opt.campaign+'/'
ProductionData = opt.campaign+'/'

directoryBkg  = treeBaseDirMC   + ProductionMC 
directoryData = treeBaseDirData + ProductionData 

### Nuisance parameters

treeNuisances = { }

globalNuisances = { }

bTagNuisances = { }

### Campaign parameters

# jet range
minJetPt  =   20.
maxJetPt  = 1400.
maxJetEta = '2.5'

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
    btagAwayJetTagger, btagAwayJetDiscriminant = 'JBP', 'Bprob'
    btagAwayJetVariations = { 'Central' : '2.821',  'AwayJetDown' : '1.370' , 'AwayJetUp' : '5.129' }

elif opt.campaign=='Summer22EE':
    bTagWorkingPoints = {'DeepJetT': {'cut': '0.7134', 'discriminant': 'DeepFlavourBDisc'}, 'ParTL': {'cut': '0.0828', 'discriminant': 'ParTBDisc'}, 'ParTT': {'cut': '0.8443', 'discriminant': 'ParTBDisc'}, 'ParticleNetT': {'cut': '0.6651', 'discriminant': 'PNetBDisc'}, 'DeepJetM': {'cut': '0.3033', 'discriminant': 'DeepFlavourBDisc'}, 'DeepJetL': {'cut': '0.057', 'discriminant': 'DeepFlavourBDisc'}, 'ParticleNetM': {'cut': '0.2386', 'discriminant': 'PNetBDisc'}, 'ParticleNetL': {'cut': '0.0458', 'discriminant': 'PNetBDisc'}, 'ParTM': {'cut': '0.4244', 'discriminant': 'ParTBDisc'}}
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

# samples for kinematic weights
kinematicWeightsMap = { 'QCDMu'  : [ 'QCDMu', 'bjets', 'light' ],
                        'IncQCD' : [ 'IncQCD' ],
                        'JetHT'  : [ 'JetHT' ]
                       }

### Complex variables

# Event
goodPV = 'PV_chi2<100.'

# Working points

goodJetForDisc = '((JETIDX<nJet)*(Alt$(Jet_pT[JETIDX],0.)>=30.)*(abs(Alt$(Jet_eta[JETIDX],5.))<'+maxJetEta+')*(Alt$(Jet_hadronFlavour[JETIDX],-1)==JETFLV)*(Alt$(Jet_tightID[JETIDX],0)==1))'
jetDisc = '(999999.*(!('+goodJetForDisc+')) + '+goodJetForDisc+'*(Alt$(Jet_BTAGDISC[JETIDX],999999.)))'

# mu-jet
jetPt    = 'Jet_pT'
jetSel   = 'Jet_tightID==1 && abs(Jet_eta)<='+maxJetEta
muSel    = 'PFMuon_GoodQuality>=2 && PFMuon_pt>5. && abs(PFMuon_eta)<2.4 && PFMuon_IdxJet>=0'
muJetEvt = 'Sum$('+muSel+')==1'
muPt     = 'Sum$(('+muSel+')*PFMuon_pt)'
muPtRel  = 'Sum$(('+muSel+')*PFMuon_ptrel)'
muJetIdx = 'Sum$(('+muSel+')*PFMuon_IdxJet)'
muJetPt  = jetPt+'['+muJetIdx+']'
muJetEta = 'Jet_eta['+muJetIdx+']'
muJetSel = muJetIdx+'>=0 && Jet_tightID['+muJetIdx+']==1 && abs('+muJetEta+')<='+maxJetEta

# Trigger
bitIdx     = 'int(triggerIdx/32)'
triggerCut = '( BitTrigger['+bitIdx+'] & ( 1 << (triggerIdx - '+bitIdx+'*32) ) )>0'

# light jets
lightJetSel = '((JETIDX<nJet)*(Alt$(Jet_tightID[JETIDX],0)==1)*(abs(Alt$(Jet_eta[JETIDX],5.))<'+maxJetEta+')*(Alt$('+jetPt+'[JETIDX],-1.)>=PTMIN)*(Alt$('+jetPt+'[JETIDX],999999.)<PTMAX)*(Alt$(Jet_'+btagAwayJetDiscriminant+'[JETIDX],999.)<'+btagAwayJetVariations['AwayJetDown']+')*(Sum$(PFMuon_GoodQuality>=1 && PFMuon_IdxJet==JETIDX)==0))'
lightJetPt  = 'Alt$('+jetPt+'[JETIDX],-999.)' #'(-999.*(!('+lightJetSel+')) + '+lightJetSel+'*(Alt$('+jetPt+'[JETIDX],-999.)))'
lightJetEta = 'Alt$(Jet_eta[JETIDX],-999.)'   #'(-999.*(!('+lightJetSel+')) + '+lightJetSel+'*(Alt$(Jet_eta[JETIDX],-999.)))'

# Away jet
awayDeltaPhi = 'acos(cos(Jet_phi-Jet_phi['+muJetIdx+']))'
awayDeltaEta = '(Jet_eta-Jet_eta['+muJetIdx+'])'
awayDeltaR   = 'sqrt('+awayDeltaPhi+'*'+awayDeltaPhi+'+'+awayDeltaEta+'*'+awayDeltaEta+')'

awayJet = 'Sum$('+jetSel+' && '+jetPt+'>=AWAYJETPTCUT && '+awayDeltaR+'>AWAYDRCUT && Jet_BTAGDISC>BTAGAWAYJETCUT)'

if 'PtRel' in opt.method:

    awayJetCut = awayJet.replace('AWAYDRCUT', '1.5')+'==1'
    awayJetCut = awayJetCut.replace('BTAGDISC>BTAGAWAYJETCUT', btagAwayJetDiscriminant+'>'+btagAwayJetVariations['Central'])

elif 'System8' in opt.method:

    awayJetCut = awayJet.replace('AWAYDRCUT', '0.05')+'>=1'

    isTaggedLeadingJet  = jetPt+'=='+jetPt+'[0] && Jet_'+btagAwayJetDiscriminant+'>-999999.'
    isTaggedTrailingJet = isTaggedLeadingJet.replace('[0]','[1]')
    muJetIsLeadingJet = muJetPt+'==Jet_pt[0]'
    isTaggedAwayJet = '( ('+isTaggedLeadingJet+') || ('+isTaggedTrailingJet+' && '+muJetIsLeadingJet+') )'
    awayJetCut = awayJetCut.replace('Jet_BTAGDISC>BTAGAWAYJETCUT', isTaggedAwayJet)

### Weights and filters

## MET Filters 

# https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2#UL_data (checked on may20)

METFilters_Common = 'Flag_goodVertices*Flag_globalSuperTightHalo2016Filter*Flag_HBHENoiseFilter*Flag_HBHENoiseIsoFilter*Flag_EcalDeadCellTriggerPrimitiveFilter*Flag_BadPFMuonFilter*Flag_BadPFMuonDzFilter*Flag_ecalBadCalibFilter'


METFilters_MC   = METFilters_Common
METFilters_Data = METFilters_Common + '*Flag_eeBadScFilter'

## Trigger Efficiencies

TriggerEff = '(1.)'

## MC weights

# generation weights

XSWeight      = 'baseW*genWeight'

muJetFromB    = '(Jet_hadronFlavour['+muJetIdx+']==5)'
muJetFromC    = '(Jet_hadronFlavour['+muJetIdx+']==4)'
muJetFromL    = '(Jet_hadronFlavour['+muJetIdx+']<4)'
muJetNotFromB = '(Jet_hadronFlavour['+muJetIdx+']!=5)'

# lepton weights
        
leptonSF = {}

# global SF weights 

SFweight      = 'puWeight*' + TriggerEff + '*' + METFilters_MC
    
## Special weights

### MC cross section uncertainties and normalization scale factors

normBackgrounds = {}

### MC

if 'SM' in opt.sigset or 'MC' in opt.sigset:

    qcdMuTrees, qcdTrees = [], []
    qcdMuName = 'QCD_PT-PTHATBIN_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8'
    qcdName = 'QCD_PT-PTHATBIN_TuneCP5_13p6TeV_pythia8'

    if opt.campaign=='Summer22':
        qcdMuPtHatBins = {'15to20': {'xSec': '892600000*0.00328', 'events': '987', 'weight': '2966289.76697'}}
        qcdPtHatBins = {'80to120': {'xSec': '2762530*1', 'events': '1168834', 'weight': '2363.49216399'}}
    elif opt.campaign=='Summer22EE':
        qcdMuPtHatBins = {}
        qcdPtHatBins = {'80to120': {'xSec': '2762530*1', 'events': '29920690', 'weight': '92.3284188968'}}

    for pth in qcdMuPtHatBins:
        qcdMuTrees += getSampleFiles(directoryBkg+qcdMuName.replace('PTHATBIN',pth)+'/',qcdMuName.replace('PTHATBIN',pth),True,treePrefix,skipTreesCheck)

    for pth in qcdPtHatBins:
        if pth=='80to120' or 'WorkingPoints' not in opt.tag:
            qcdTrees += getSampleFiles(directoryBkg+qcdName.replace('PTHATBIN',pth)+'/',qcdName.replace('PTHATBIN',pth),True,treePrefix,skipTreesCheck)

    if opt.method+'Kinematics' in opt.tag or 'DataKinematics' in opt.tag:
        samples['QCDMu'] = { 'name'     : qcdMuTrees, 'weight'   : '1.', 'isSignal' : 0 }

    elif opt.method+'Templates' in opt.tag:
        samples['bjets'] = { 'name'     : qcdMuTrees, 'weight'   : '1.*'+muJetFromB,    'isSignal' : 1 }
        samples['light'] = { 'name'     : qcdMuTrees, 'weight'   : '1.*'+muJetNotFromB, 'isSignal' : 0 }

    if 'WorkingPoints' in opt.tag or (opt.method=='PtRel' and ('LightKinematics' in opt.tag or 'LightTemplates' in opt.tag)):
        samples['QCD'] = { 'name'     : qcdTrees , 'weight'   : '1.', 'isSignal' : 0 }

    for sample in samples:
        if sample=='QCDMu' or sample=='bjets' or sample=='light':
            for pth in qcdMuPtHatBins:
                addSampleWeight(samples, sample, qcdMuName.replace('PTHATBIN',pth), qcdMuPtHatBins[pth]['weight'])
        elif sample=='QCD':
            for pth in qcdPtHatBins:
                addSampleWeight(samples, sample, qcdName.replace('PTHATBIN',pth), qcdPtHatBins[pth]['weight'])

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
 
for sample in samples:
    if 'FilesPerJob' not in samples[sample]:
        ntrees = len(samples[sample]['name']) 
        multFactor = 6 if 'JobsPerSample' not in samples[sample] else int(samples[sample]['JobsPerSample'])
        samples[sample]['FilesPerJob'] = int(math.ceil(float(ntrees)/multFactor))

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



