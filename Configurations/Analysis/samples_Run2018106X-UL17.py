import os
import subprocess
import math
import string
from LatinoAnalysis.Tools.commonTools import *

### Generals

opt.method = 'System8' if 'System8' in opt.tag else 'PtRel'
opt.campaign = 'UL17nano'
opt.CME = '13'
opt.lumi = 41.48
treePrefix= 'nanoLatino_'

isDatacardOrPlot = hasattr(opt, 'outputDirDatacard') or hasattr(opt, 'postFit') or hasattr(opt, 'skipLNN') or hasattr(opt, 'inputDirMaxFit')
isPlot = hasattr(opt, 'postFit')

### Directories

skipTreesCheck = False

if not isDatacardOrPlot: 
    if skipTreesCheck:
        print('Error: it is not allowed to fill shapes and skipping trees check!')
        exit()
    if opt.sigset=='SM' and hasattr(opt, 'doHadd') and not opt.doHadd:
        print('Error: SM cannot be used when filling the shapes. Use Data and MC separately instead') 

SITE=os.uname()[1]
if 'cern' not in SITE and 'ifca' not in SITE and 'cloud' not in SITE: SITE = 'cern'

if 'cern' in SITE:
    treeBaseDirMC   = '/eos/cms/store/group/phys_btag/performance/Nano/'
    treeBaseDirData = '/eos/cms/store/group/phys_btag/performance/Nano/'
else: print('trees for', campaign, 'available only at cern')

ProductionMC   = 'Summer20UL17_106X_nAODv9_Full2017v8/btvperfMC__btvperfWeights/'
ProductionData = 'Run2017_106X_nAODv9_Full2017v8/btvperfData__hadd/'

directoryBkg  = treeBaseDirMC   + ProductionMC 
directoryData = treeBaseDirData + ProductionData 

### Nuisance parameters

treeNuisances = { }

globalNuisances = { }

bTagNuisances = { }

### Campaign parameters

minJetPt  =   20.
maxJetPt  = 1400.
maxJetEta = '2.5'

triggerInfos = { 'BTagMu_AK4DiJet20_Mu5'  : { 'jetPtRange' : [  '20.',   '50.' ], 'ptAwayJet' : '20.', 'ptTriggerEmulation' :  '30.', 'jetTrigger' :  'PFJet40' },
                 'BTagMu_AK4DiJet40_Mu5'  : { 'jetPtRange' : [  '50.',  '100.' ], 'ptAwayJet' : '30.', 'ptTriggerEmulation' :  '50.', 'jetTrigger' :  'PFJet40' },
                 'BTagMu_AK4DiJet70_Mu5'  : { 'jetPtRange' : [ '100.',  '140.' ], 'ptAwayJet' : '30.', 'ptTriggerEmulation' :  '80.', 'jetTrigger' :  'PFJet60' },
                 'BTagMu_AK4DiJet110_Mu5' : { 'jetPtRange' : [ '140.',  '200.' ], 'ptAwayJet' : '30.', 'ptTriggerEmulation' : '140.', 'jetTrigger' :  'PFJet80' },
                 'BTagMu_AK4DiJet170_Mu5' : { 'jetPtRange' : [ '200.',  '320.' ], 'ptAwayJet' : '30.', 'ptTriggerEmulation' : '200.', 'jetTrigger' : 'PFJet140' },
                 'BTagMu_AK4Jet300_Mu5'   : { 'jetPtRange' : [ '320.', '1400.' ], 'ptAwayJet' : '30.', 'ptTriggerEmulation' :   '0.', 'jetTrigger' : 'PFJet260' },
                }

bTagWorkingPoints = { 'DeepCSVL' : { 'discriminant' : 'btagDeepB'     , 'cut' : '0.1355' },
                      'DeepCSVM' : { 'discriminant' : 'btagDeepB'     , 'cut' : '0.4506' },
                      'DeepCSVT' : { 'discriminant' : 'btagDeepB'     , 'cut' : '0.7738' },
	              'DeepJetL' : { 'discriminant' : 'btagDeepFlavB' , 'cut' : '0.0532' },  
                      'DeepJetM' : { 'discriminant' : 'btagDeepFlavB' , 'cut' : '0.3040' },
                      'DeepJetT' : { 'discriminant' : 'btagDeepFlavB' , 'cut' : '0.7476' },
                     }

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

kinematicWeightsMap = { 'QCDMu'  : [ 'QCDMu', 'bjets', 'light' ],
                        'IncQCD' : [ 'IncQCD' ],
                        'JetHT'  : [ 'JetHT' ]
                       }

### Complex variables

jetPt    = 'Jet_pt' if 'Data' in opt.sigset else 'Jet_pt_nom'
jetSel   = 'Jet_jetId>=2 && (Jet_puId>=4 || '+jetPt+'>=50.) && abs(Jet_eta)<='+maxJetEta
muJetSel = 'muJet_idx>=0 && Jet_jetId[muJet_idx]>=2 && (Jet_puId[muJet_idx]>=4 || muJet_pt>=50.) && abs(muJet_eta)<='+maxJetEta

awayDeltaPhi = 'acos(cos(Jet_phi-muJet_phi))'
awayDeltaEta = '(Jet_eta-muJet_eta)'
awayDeltaR   = 'sqrt('+awayDeltaPhi+'*'+awayDeltaPhi+'+'+awayDeltaEta+'*'+awayDeltaEta+')'

awayJet = 'Sum$('+jetSel+' && '+jetPt+'>=AWAYJETPTCUT && '+awayDeltaR+'>AWAYDRCUT && Jet_BTAGDISC>BTAGAWAYJETCUT)'

btagAwayJetVariations = { 'Central' : '0.8838',  'AwayJetDown' : '0.5803' , 'AwayJetUp' : '0.9693' }

if 'PtRel' in opt.method:

    awayJetCut = awayJet.replace('AWAYDRCUT', '1.5')+'==1'
    awayJetCut = awayJetCut.replace('BTAGDISC>BTAGAWAYJETCUT', 'btagCSVV2>'+btagAwayJetVariations['Central'])

elif 'System8' in opt.method:

    awayJetCut = awayJet.replace('AWAYDRCUT', '0.05')+'>=1'

    isTaggedLeadingJet = jetPt+'=='+jetPt+'[0] && Jet_btagCSVV2>-999999.'
    isTaggedTrailingJet = jetPt+'=='+jetPt+'[1] && Jet_btagCSVV2>-999999.'
    muJetIsLeadingJet = 'muJet_pt==Jet_pt[0]'
    isTaggedAwayJet = '( ('+isTaggedLeadingJet+') || ('+isTaggedTrailingJet+' && '+muJetIsLeadingJet+') )'
    awayJetCut = awayJetCut.replace('Jet_BTAGDISC>BTAGAWAYJETCUT', isTaggedAwayJet)

### Weights and filters

## MET Filters 

# https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2#UL_data (checked on may20)

METFilters_Common = 'Flag_goodVertices*Flag_globalSuperTightHalo2016Filter*Flag_HBHENoiseFilter*Flag_HBHENoiseIsoFilter*Flag_EcalDeadCellTriggerPrimitiveFilter*Flag_BadPFMuonFilter*Flag_BadPFMuonDzFilter*Flag_ecalBadCalibFilter'

if 'noisyhits' in opt.tag: METFilters_Common += '*Flag_hfNoisyHitsFilter'

METFilters_MC   = METFilters_Common
METFilters_Data = METFilters_Common + '*Flag_eeBadScFilter'

## HEM Issue in 2018

DataQualityCuts = ''
if 'VetoesUL' in opt.tag: DataQualityCuts = 'EENoiseHTHEM'

VetoEENoise = '('+HTForwardSoft+'<60.)' if 'EENoiseHT' in DataQualityCuts else '1.'

## Trigger Efficiencies

TriggerEff = '(1.)'

## MC weights

# generation weights

XSWeight      = 'baseW*genWeight'

muJetFromB    = '(abs(Jet_hadronFlavour[abs(muJet_idx)])==5)'
muJetFromC    = '(abs(Jet_hadronFlavour[abs(muJet_idx)])==4)'
muJetFromL    = '(abs(Jet_hadronFlavour[abs(muJet_idx)])<4)'
muJetNotFromB = '(abs(Jet_hadronFlavour[abs(muJet_idx)])!=5)'

# lepton weights
        
leptonSF = {}

# global SF weights 

SFweight      = 'puWeight*' + TriggerEff + '*' + VetoEENoise + '*' + METFilters_MC
    
## Special weights

### MC cross section uncertainties and normalization scale factors

normBackgrounds = {}

### MC

if 'SM' in opt.sigset or 'MC' in opt.sigset:

    qcdmuTrees = [ ]
    ptHatEdges = [ '20', '30', '50', '80', '120', '170', '300', '470', '600', '800', '1000', 'Inf' ]
    for pth in range(len(ptHatEdges)-1):
        qcdmuTrees += getSampleFiles(directoryBkg,'QCD_Pt-'+ptHatEdges[pth]+'to'+ptHatEdges[pth+1]+'_MuEnrichedPt5',True,treePrefix,skipTreesCheck)

    if opt.method+'Kinematics' in opt.tag or 'DataKinematics' in opt.tag:

        samples['QCDMu'] = { 'name'     : qcdmuTrees ,
                             'weight'   : XSWeight+'*'+SFweight ,
                             'isSignal' : 0 ,
                             'split'    : 'AsMuchAsPossible'
                            }  

    elif opt.method+'Templates' in opt.tag:

        samples['bjets'] = { 'name'     : qcdmuTrees ,
                             'weight'   : XSWeight+'*'+SFweight+'*'+muJetFromB ,
                             'isSignal' : 1 ,
                             'split'    : 'AsMuchAsPossible'
                            }
    
        samples['light'] = { 'name'     : qcdmuTrees ,
                             'weight'   : XSWeight+'*'+SFweight+'*'+muJetNotFromB ,
                             'isSignal' : 0 ,
                             'split'    : 'AsMuchAsPossible'
                            }

    if 'PtRelKinematics' in opt.tag or 'PtRelLightTemplates' in opt.tag:

        print('Trees for light template corrections not yet available')

# Common MC keys

for sample in samples:

    samples[sample]['isDATA']    = 0
    samples[sample]['isFastsim'] = 0
    samples[sample]['treeType']  = 'MC'
    samples[sample]['suppressNegative']          = ['all']
    samples[sample]['suppressNegativeNuisances'] = ['all']
    samples[sample]['suppressZeroTreeNuisances'] = ['all']
    samples[sample]['JobsPerSample'] = 20
    if isPlot or opt.method!='PtRel': samples[sample]['isSignal']  = 0

### Data

if 'SM' in opt.sigset or 'Data' in opt.sigset:

    runPeriods = [ 'Run2017B', 'Run2017C', 'Run2017D', 'Run2017E', 'Run2017F' ]

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



