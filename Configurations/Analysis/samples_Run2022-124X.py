import os
import subprocess
import math
import string
from LatinoAnalysis.Tools.commonTools import *
from collections import OrderedDict

### Generals

opt.campaign = 'Summer22'
if 'Summer22EE' in opt.tag: opt.campaign = 'Summer22EE'

opt.CME = '13.6'
opt.lumi = 1. if 'Validation' in opt.tag else 26.337 if 'Summer22EE' in opt.campaign else 7.875

opt.simulationPileupFile = 'pileup_DistrWinter22_Run3_2022_LHC_Simulation_10h_2h.root'
if 'Summer22EE' in opt.campaign: opt.dataPileupFile = '/afs/cern.ch/work/s/scodella/BTagging/CMSSW_10_6_28/src/LatinoAnalysis/NanoGardener/python/data/PUweights/2022/2022EFG.root'
elif 'Summer22' in opt.campaign: opt.dataPileupFile = '/afs/cern.ch/work/s/scodella/BTagging/CMSSW_10_6_28/src/LatinoAnalysis/NanoGardener/python/data/PUweights/2022/2022CD.root'

fragTune = 'fragCP5BL'
jetEnergyUncertaintyFile = 'Summer22EEPrompt22_V1_MC_Uncertainty_AK4PFPuppi.txt' if 'Summer22EE' in opt.campaign else 'Winter22Run3_V2_MC_Uncertainty_AK4PFPuppi.txt'

treePrefix = ''

opt.method = 'System8' if 'System8' in opt.tag else 'PtRel'

### Process utilities

isDatacardOrPlot = hasattr(opt, 'outputDirDatacard') or hasattr(opt, 'postFit') or hasattr(opt, 'skipLNN') or hasattr(opt, 'inputDirMaxFit')
isPlot = hasattr(opt, 'postFit')
isShape = hasattr(opt, 'doHadd')
isFillShape = isShape and not opt.doHadd
opt.isShape = isShape

bIsSignal = opt.method=='PtRel' and not isPlot
if hasattr(opt, 'action') and opt.action=='plotNuisances': bIsSignal = False

if isFillShape and 'MergedLight' in opt.tag:
    print('Cannot fill shapes for', opt.tag, 'directly from trees')
    exit()

### Directories

skipTreesCheck = False if isShape or 'PtHatWeights' in opt.tag else True

if opt.sigset=='SM' and isFillShape:
    print('Error: SM cannot be used when filling the shapes. Use Data and MC separately instead') 

SITE=os.uname()[1]
if 'cern' not in SITE and 'ifca' not in SITE and 'cloud' not in SITE: SITE = 'cern'

if 'cern' in SITE:
    treeBaseDirMC   = '/eos/cms/store/group/phys_btag/milee/BTA_addPFMuons_NanoV12_fixPuppi'
    treeBaseDirData = '/eos/cms/store/group/phys_btag/milee/BTA_addPFMuons_NanoV12_fixPuppi'
else: print('trees for', campaign, 'campaign available only at cern')

ProductionMC   = opt.campaign
ProductionData = opt.campaign
  
directoryBkg  = '/'.join([ treeBaseDirMC,   ProductionMC  , '' ])
directoryData = '/'.join([ treeBaseDirData, ProductionData, '' ])

### Campaign parameters

# global parameters
minJetPt  =   20.
maxJetPt  = 1400.
maxJetEta = '2.5'
minPlotPt =   20.
maxPlotPt = 1000.

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

# b-tagging algorithms and working points

bTagAlgorithms = [ 'DeepJet', 'ParticleNet', 'ParT' ]
workingPointName = [ 'Loose', 'Medium', 'Tight', 'eXtraTight', 'eXtraeXtraTight' ]
workingPointLimit = [ 0.1, 0.01, 0.001, 0.0005, 0.0001 ]

if opt.campaign=='Summer22':
    bTagWorkingPoints = {'DeepJetT': {'cut': '0.7183', 'discriminant': 'DeepFlavourBDisc'}, 'ParticleNetXT': {'cut': '0.7862', 'discriminant': 'PNetBDisc'}, 'ParTL': {'cut': '0.0849', 'discriminant': 'ParTBDisc'}, 'ParticleNetM': {'cut': '0.245', 'discriminant': 'PNetBDisc'}, 'ParticleNetL': {'cut': '0.047', 'discriminant': 'PNetBDisc'}, 'ParTM': {'cut': '0.4319', 'discriminant': 'ParTBDisc'}, 'ParTT': {'cut': '0.8482', 'discriminant': 'ParTBDisc'}, 'ParticleNetT': {'cut': '0.6734', 'discriminant': 'PNetBDisc'}, 'DeepJetM': {'cut': '0.3086', 'discriminant': 'DeepFlavourBDisc'}, 'DeepJetL': {'cut': '0.0583', 'discriminant': 'DeepFlavourBDisc'}, 'ParticleNetXXT': {'cut': '0.961', 'discriminant': 'PNetBDisc'}, 'ParTXXT': {'cut': '0.9874', 'discriminant': 'ParTBDisc'}, 'ParTXT': {'cut': '0.9151', 'discriminant': 'ParTBDisc'}, 'DeepJetXXT': {'cut': '0.9512', 'discriminant': 'DeepFlavourBDisc'}, 'DeepJetXT': {'cut': '0.8111', 'discriminant': 'DeepFlavourBDisc'}}
    btagAwayJetTagger, btagAwayJetDiscriminant = 'JBP', 'Bprob'
    btagAwayJetVariations = { 'AwayJetTag' : '2.866',  'AwayJetDown' : '1.397' , 'AwayJetUp' : '5.196' }

elif opt.campaign=='Summer22EE':
    bTagWorkingPoints = {'DeepJetT': {'cut': '0.73', 'discriminant': 'DeepFlavourBDisc'}, 'ParticleNetXT': {'cut': '0.8033', 'discriminant': 'PNetBDisc'}, 'ParTL': {'cut': '0.0897', 'discriminant': 'ParTBDisc'}, 'ParticleNetM': {'cut': '0.2605', 'discriminant': 'PNetBDisc'}, 'ParticleNetL': {'cut': '0.0499', 'discriminant': 'PNetBDisc'}, 'ParTM': {'cut': '0.451', 'discriminant': 'ParTBDisc'}, 'ParTT': {'cut': '0.8604', 'discriminant': 'ParTBDisc'}, 'ParticleNetT': {'cut': '0.6915', 'discriminant': 'PNetBDisc'}, 'DeepJetM': {'cut': '0.3196', 'discriminant': 'DeepFlavourBDisc'}, 'DeepJetL': {'cut': '0.0614', 'discriminant': 'DeepFlavourBDisc'}, 'ParticleNetXXT': {'cut': '0.9664', 'discriminant': 'PNetBDisc'}, 'ParTXXT': {'cut': '0.9893', 'discriminant': 'ParTBDisc'}, 'ParTXT': {'cut': '0.9234', 'discriminant': 'ParTBDisc'}, 'DeepJetXXT': {'cut': '0.9542', 'discriminant': 'DeepFlavourBDisc'}, 'DeepJetXT': {'cut': '0.8184', 'discriminant': 'DeepFlavourBDisc'}}
    btagAwayJetTagger, btagAwayJetDiscriminant = 'JBP', 'Bprob'
    btagAwayJetVariations = { 'AwayJetTag' : '3.057',  'AwayJetDown' : '1.492' , 'AwayJetUp' : '5.481' }

if 'WorkingPoints' in opt.tag:
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
           if ptbin in 'Pt'+opt.tag.split('JetPtVeto')[1].split('_')[0]:
               ptBinToRemove.append(ptbin)
        elif ptbin not in 'Pt'+opt.tag.split('JetPt')[1].split('_')[0]:
           ptBinToRemove.append(ptbin)
    for ptbin in ptBinToRemove:
        del jetPtBins[ptbin]

# systematics

csvSystematics = OrderedDict()
csvSystematics['central'] = 'Final'
for variation in [ 'Up', 'Down' ]:
    csvSystematics[variation.lower()]                   = 'Final'+variation
    csvSystematics[variation.lower()+'_statistic']      = 'Statistics'+variation
    csvSystematics[variation.lower()+'_jetaway']        = 'AwayJet'+variation
    csvSystematics[variation.lower()+'_mupt']           = 'MuPt'+variation
    csvSystematics[variation.lower()+'_mudr']           = 'MuDR'+variation
    csvSystematics[variation.lower()+'_jes']            = 'JEU'+variation
    csvSystematics[variation.lower()+'_pileup']         = 'pileup'+variation
    csvSystematics[variation.lower()+'_gluonsplitting'] = 'gluonSplitting'+variation
    csvSystematics[variation.lower()+'_bfragmentation'] = 'bfragmentation'+variation
    csvSystematics[variation.lower()+'_bdecays']        = 'bdecays'+variation
    csvSystematics[variation.lower()+'_btempcorr']      = 'CorrB'+variation
    csvSystematics[variation.lower()+'_cjets']          = 'cjets'+variation
    csvSystematics[variation.lower()+'_l2c']            = 'lightCharmRatio'+variation
    csvSystematics[variation.lower()+'_ltempcorr']      = 'CorrL'+variation

systematicVariations = [ '' ]

if 'Templates' in opt.tag:
    systematicVariations.extend([ 'MuPtUp', 'MuPtDown', 'MuDRUp', 'MuDRDown' ])
    if ('Validation' not in opt.tag and ('SM' in opt.sigset or 'MC' in opt.sigset) and ('ForFit' not in opt.tag or '_nuisSelections' in opt.tag)) or '_selJEU' in opt.tag: 
        systematicVariations.extend([ 'JEUUp', 'JEUDown' ])
    if 'Light' not in opt.tag:
        systematicVariations.insert(1, 'AwayJetDown')
        systematicVariations.insert(1, 'AwayJetUp')

systematicNuisances = []

applyBFragmentation = 1

if 'NoPU' not in opt.tag and 'Validation' not in opt.tag: systematicNuisances.append('pileup')
systematicNuisances.append('gluonSplitting')
if applyBFragmentation>=1: systematicNuisances.append('bfragmentation')
systematicNuisances.append('bdecay')
if opt.method=='PtRel': systematicNuisances.append('lightCharmRatio')

if 'Templates' in opt.tag and 'ForFit' in opt.tag and '_nuisSelections' in opt.tag: 
    if '_noselrefit' in opt.tag or '_norefit' in opt.tag: systematicVariations = [ 'JEUUp', 'JEUDown' ]
    for nuisance in systematicNuisances:
        systematicVariations.append(nuisance+'Up')
        systematicVariations.append(nuisance+'Down')

# Template corrections

templateTreatments = [ 'corr', 'nuis', 'syst' ]
bTemplateCorrector = {}
for btagWP in bTagWorkingPoints: bTemplateCorrector[btagWP] = 'ParTT' if 'DeepJet' in btagWP else 'DeepJetT'

if 'PtRelTemplates' in opt.tag and 'ForFit' in opt.tag:
    
   templateTreatmentFlag = opt.tag.split('Templates')[1].split('2D')[0].split('ForFit')[0]

   templateCorrectionNuisances = {}   
   if 'Nuis' in templateTreatmentFlag:
       for flavour in templateTreatmentFlag.split('Nuis')[1].split('Syst')[0]:
           templateCorrectionNuisances['Corr'+flavour] = flavour.lower()+'jets'

   if 'Syst' in templateTreatmentFlag and 'nocorrrefit' not in opt.tag and 'norefit' not in opt.tag:
       for flavour in templateTreatmentFlag.split('Syst')[1]:
           systematicVariations.append('Corr'+flavour) 

if '_sel' in opt.tag:
    selectionToRemove = []
    for tagoption in opt.tag.split('_'):
        if 'sel' in tagoption:
            for selection in systematicVariations:
               sel = 'Central' if selection=='' else selection
               if 'veto' in tagoption:
                   if sel in tagoption: selectionToRemove.append(selection)
               elif sel not in tagoption: selectionToRemove.append(selection)
            for nuisance in systematicNuisances:
                for variation in [ 'Up', 'Down' ]:
                    if nuisance+variation in tagoption: systematicVariations.append(nuisance+variation)
    for selection in selectionToRemove:
        systematicVariations.remove(selection)

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
                        'Jet'    : [ 'Jet' ]
                       }

### Complex variables

# event
nJetMax = 20
goodPV  = 'PV_chi2<100.' # No nPV so far in the trees

# working points
jetPt   = 'Jet_pT'
if 'RawPt'   in opt.tag: jetPt = 'Jet_uncorrpt'
if 'JEUDown' in opt.tag: jetPt = 'jetEnDown'
elif 'JEUUp' in opt.tag: jetPt = 'jetEnUp'
goodJetForDisc = '((JETIDX<nJet)*(Alt$('+jetPt+'[JETIDX],0.)>=30.)*(abs(Alt$(Jet_eta[JETIDX],5.))<'+maxJetEta+')*(Alt$(Jet_hadronFlavour[JETIDX],-1)==JETFLV)*(Alt$(Jet_tightID[JETIDX],0)==1))'
jetDisc = '(999999.*(!('+goodJetForDisc+')) + '+goodJetForDisc+'*(Alt$(Jet_BTAGDISC[JETIDX],999999.)))'

# kinematic weights
jetKinematicWeight = '1.'
if '.' in opt.tag:
    jetKinematicWeightList = []
    for x in opt.tag.split('.'):
        if opt.method not in x: jetKinematicWeightList.append('Alt$('+x+'[JETIDX],1.)')
    jetKinematicWeight = '*'.join(jetKinematicWeightList)
# This does not work in python3
#jetKinematicWeight = '*'.join([ 'Alt$('+x+'[JETIDX],1.)' for x in opt.tag.split('.') if opt.method not in x ]) if '.' in opt.tag else '1.'

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
    #awayJetCand = [ '('+str(ijet)+'<nJet && Alt$(Jet_tightID['+str(ijet)+'],0)==1 && abs(Alt$(Jet_eta['+str(ijet)+'],5.))<='+maxJetEta+' && '+str(ijet)+'!='+muJetIdx+' && Alt$('+jetPt+'['+str(ijet)+'],0.)>=AWAYJETPTCUT && Alt$(Jet_'+btagAwayJetDiscriminant+'['+str(ijet)+'],-9999999.)>=-999999. && Sum$('+jetSel+' && '+jetPt+'!='+muJetPt+' && '+jetPt+'>'+jetPt+'['+str(ijet)+'])==0)' for ijet in range(5) ]
    awayJetCand = []
    for ijet in range(5):
        awayJetCand.append( '('+str(ijet)+'<nJet && Alt$(Jet_tightID['+str(ijet)+'],0)==1 && abs(Alt$(Jet_eta['+str(ijet)+'],5.))<='+maxJetEta+' && '+str(ijet)+'!='+muJetIdx+' && Alt$('+jetPt+'['+str(ijet)+'],0.)>=AWAYJETPTCUT && Alt$(Jet_'+btagAwayJetDiscriminant+'['+str(ijet)+'],-9999999.)>=-999999. && Sum$('+jetSel+' && '+jetPt+'!='+muJetPt+' && '+jetPt+'>'+jetPt+'['+str(ijet)+'])==0)' )
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
        qcdMuPtHatBins = {'80to120': {'ext': '', 'xSec': '2536000*0.03807', 'events': '24335108', 'weight': '3.96733476589'}, '170to300': {'ext': '', 'xSec': '114200*0.06781', 'events': '36811617', 'weight': '0.210365711455'}, '300to470': {'ext': '', 'xSec': '7678*0.09136', 'events': '30226277', 'weight': '0.0232070287717'}, '600to800': {'ext': '', 'xSec': '180.6*0.1176', 'events': '16990662', 'weight': '0.00125001368399'}, '800to1000': {'ext': '', 'xSec': '30.89*0.1278', 'events': '39259978', 'weight': '0.000100553851558'}, '120to170': {'ext': '', 'xSec': '444900*0.05214', 'events': '18670083', 'weight': '1.24247364085'}, '50to80': {'ext': '', 'xSec': '15710000*0.0221', 'events': '40877766', 'weight': '8.49339467328'}, '30to50': {'ext': '', 'xSec': '114100000*0.01303', 'events': '30122969', 'weight': '49.3551283076'}, '470to600': {'ext': '', 'xSec': '630.3*0.1062', 'events': '18567007', 'weight': '0.00360520465146'}, '15to20': {'ext': '', 'xSec': '907100000*0.0032', 'events': '4355208', 'weight': '666.493999827'}, '20to30': {'ext': '', 'xSec': '420500000*0.00599', 'events': '30156471', 'weight': '83.5241961833'}, '1000': {'ext': '', 'xSec': '9.935*0.1341', 'events': '13705539', 'weight': '9.72076691037e-05'}}
        qcdPtHatBins = {'80to120': {'ext': '', 'xSec': '2762530*1', 'events': '29962336', 'weight': '92.2000874698'}, '170to300': {'ext': '', 'xSec': '19204300', 'events': '28753694', 'weight': '667.889837041'}, '300to470': {'ext': '', 'xSec': '7823', 'events': '56915763', 'weight': '0.137448741573'}, '600to800': {'ext': '', 'xSec': '186.9', 'events': '65874236', 'weight': '0.0028372245562'}, '1000to1400': {'ext': '', 'xSec': '9.4183', 'events': '20214043', 'weight': '0.000465928562633'}, '800to1000': {'ext': '', 'xSec': '32.293', 'events': '40661892', 'weight': '0.000794183408878'}, '120to170': {'ext': '', 'xSec': '471100', 'events': '29386831', 'weight': '16.0309902078'}, '1400to1800': {'ext': '', 'xSec': '0.84265', 'events': '6220780', 'weight': '0.000135457289922'}, '1800to2400': {'ext': '', 'xSec': '0.114943', 'events': '2796944', 'weight': '4.1095924695e-05'}, '2400to3200': {'ext': '', 'xSec': '0.00682981', 'events': '1874178', 'weight': '3.64416293436e-06'}, '3200': {'ext': '', 'xSec': '0.000165445', 'events': '100000', 'weight': '1.65445e-06'}, '50to80': {'ext': '', 'xSec': '19204300', 'events': '19963206', 'weight': '961.984763369'}, '30to50': {'ext': '', 'xSec': '114100000', 'events': '3883200', 'weight': '29382.9831067'}, '470to600': {'ext': '', 'xSec': '648.2', 'events': '26594326', 'weight': '0.0243736201474'}, '15to30': {'ext': '', 'xSec': '1327600000', 'events': '1149000', 'weight': '1155439.51262'}}
 
    elif opt.campaign=='Summer22EE':
        qcdMuPtHatBins = {'80to120': {'ext': '', 'xSec': '2536000*0.03807', 'events': '86940145', 'weight': '1.11048261997'}, '170to300': {'ext': '', 'xSec': '114200*0.06781', 'events': '107479889', 'weight': '0.0720497766796'}, '300to470': {'ext': '', 'xSec': '7678*0.09136', 'events': '101648281', 'weight': '0.00690087498873'}, '600to800': {'ext': '', 'xSec': '180.6*0.1176', 'events': '72565100', 'weight': '0.000292682846162'}, '800to1000': {'ext': '', 'xSec': '30.89*0.1278', 'events': '128437072', 'weight': '3.07367797983e-05'}, '120to170': {'ext': '', 'xSec': '444900*0.05214', 'events': '70443255', 'weight': '0.329301733715'}, '50to80': {'ext': '', 'xSec': '15710000*0.0221', 'events': '39483803', 'weight': '8.79325124786'}, '30to50': {'ext': '', 'xSec': '114100000*0.01303', 'events': '101098844', 'weight': '14.7056379794'}, '470to600': {'ext': '', 'xSec': '630.3*0.1062', 'events': '71197091', 'weight': '0.000940176895711'}, '15to20': {'ext': '', 'xSec': '907100000*0.0032', 'events': '16043927', 'weight': '180.923286425'}, '20to30': {'ext': '', 'xSec': '420500000*0.00599', 'events': '75762116', 'weight': '33.2461015212'}, '1000': {'ext': '', 'xSec': '9.935*0.1341', 'events': '45503506', 'weight': '2.92786999753e-05'}}
        qcdPtHatBins = {'80to120': {'ext': '', 'xSec': '2762530*1', 'events': '28629379', 'weight': '96.49283695605133'}, '170to300': {'ext': '', 'xSec': '19204300', 'events': '31822560', 'weight': '603.4806753447868'}, '300to470': {'ext': '', 'xSec': '7823', 'events': '64232868', 'weight': '0.12179122999770149'}, '600to800': {'ext': '', 'xSec': '186.9', 'events': '65747546', 'weight': '0.002842691649662483'}, '1000to1400': {'ext': '', 'xSec': '9.4183', 'events': '23710401', 'weight': '0.00039722229919266237'}, '800to1000': {'ext': '', 'xSec': '32.293', 'events': '43945702', 'weight': '0.0007348386424683806'}, '120to170': {'ext': '', 'xSec': '471100', 'events': '30572539', 'weight': '15.409253382586249'}, '1400to1800': {'ext': '', 'xSec': '0.84265', 'events': '8317538', 'weight': '0.0001013100270777242'}, '1800to2400': {'ext': '', 'xSec': '0.114943', 'events': '4484970', 'weight': '2.5628488038938946e-05'}, '2400to3200': {'ext': '', 'xSec': '0.00682981', 'events': '2389431', 'weight': '2.858341588436745e-06'}, '3200': {'ext': '', 'xSec': '0.000165445', 'events': '1241939', 'weight': '1.332150773910796e-07'}, '50to80': {'ext': '', 'xSec': '19204300', 'events': '19392712', 'weight': '990.284391373419'}, '30to50': {'ext': '', 'xSec': '114100000', 'events': '4802915', 'weight': '23756.40626577818'}, '470to600': {'ext': '', 'xSec': '648.2', 'events': '29381124', 'weight': '0.02206178361317967'}, '15to30': {'ext': '', 'xSec': '1327600000', 'events': '4491551', 'weight': '295577.1848076533'}}

    if 'Validation' in opt.tag:
        for pthatbin in list(qcdMuPtHatBins.keys()):
            if pthatbin!='80to120': del qcdMuPtHatBins[pthatbin]
        for pthatbin in list(qcdPtHatBins.keys()):
            if pthatbin!='80to120': del qcdPtHatBins[pthatbin]

    if 'WorkingPoints' in opt.tag or 'PtHatWeights' in opt.tag or 'Light' in opt.tag:

        nPtHatBins = len(list(qcdPtHatBins.keys()))        

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

        nPtHatBins = len(list(qcdMuPtHatBins.keys()))

        qcdMuTrees = []
        for pth in qcdMuPtHatBins:
            ptHatTrees = getSampleFiles(directoryBkg+qcdMuName.replace('PTHATBIN',pth)+qcdMuPtHatBins[pth]['ext']+'/','',True,treePrefix,skipTreesCheck)
            if 'PtHatWeights' in opt.tag: samples['QCDMu_'+pth] = { 'name' : ptHatTrees }
            else: qcdMuTrees += ptHatTrees

        if opt.method+'Kinematics' in opt.tag or 'DataKinematics' in opt.tag:
            samples['QCDMu'] = { 'name' : qcdMuTrees, 'weight'   : muJetKinematicWeight               , 'isSignal' : 0 }

        elif opt.method+'Templates' in opt.tag:
            samples['bjets'] = { 'name' : qcdMuTrees, 'weight'   : muJetKinematicWeight+'*'+muJetFromB, 'isSignal' : bIsSignal }
            if 'PtRel' in opt.method:
                if '2D' not in opt.tag: samples['cjets'] = { 'name' : qcdMuTrees, 'weight'   : muJetKinematicWeight+'*'+muJetFromC, 'isSignal' : 0 }
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

### Data

if 'SM' in opt.sigset or 'Data' in opt.sigset:

    dataSetName = 'BTagMu' if 'Light' not in opt.tag else 'JetMET'

    runPeriods = {}
    if 'Summer22EE' in opt.campaign:
        if dataSetName=='BTagMu':
            runPeriods['Run2022E'] = { 'subdir' : dataSetName + 'Run2022E-22Sep2023-v1' }
            runPeriods['Run2022F'] = { 'subdir' : dataSetName + 'Run2022F-22Sep2023-v2' }
            runPeriods['Run2022G'] = { 'subdir' : dataSetName + 'Run2022G-22Sep2023-v1' }
        else:  
            runPeriods['Run2022E'] = { 'subdir' : dataSetName + 'Run2022E-22Sep2023-v1' }
            runPeriods['Run2022F'] = { 'subdir' : dataSetName + 'Run2022F-22Sep2023-v2' }
            runPeriods['Run2022G'] = { 'subdir' : dataSetName + 'Run2022G-22Sep2023-v2' }
    elif 'Summer22' in opt.campaign:
        if dataSetName=='BTagMu':
            runPeriods['Run2022C'] = { 'subdir' : dataSetName + 'Run2022C-22Sep2023-v1' }
            runPeriods['Run2022D'] = { 'subdir' : dataSetName + 'Run2022D-22Sep2023-v1' }
        else:
            runPeriods['Run2022c'] = { 'subdir' : 'JetHT'     + 'Run2022C-22Sep2023'    }
            runPeriods['Run2022C'] = { 'subdir' : dataSetName + 'Run2022C-22Sep2023-v1' }
            runPeriods['Run2022D'] = { 'subdir' : dataSetName + 'Run2022D-22Sep2023-v1' }
        if 'RunC' in opt.tag: del runPeriods['Run2022D']
        if 'RunD' in opt.tag: del runPeriods['Run2022C']

    dataTrees = [ ]
    for runPeriod in runPeriods:
  
        dataDir = '/'.join([ directoryData, runPeriods[runPeriod]['subdir'], '' ]) 
        dataTrees += getSampleFiles(dataDir,  '', True, treePrefix, skipTreesCheck)
 
    dataName = 'DATA' if dataSetName=='BTagMu' else 'Jet'
    samples[dataName]  = { 'name'      : dataTrees ,
                           'weight'    : '1.' ,
                           'isData'    : ['all'] ,
                           'treeType'  : 'Data' ,
                           'isSignal'  : 0 ,
                           'isDATA'    : 1 ,
                           'isFastsim' : 0 ,
                           'split'     : 'AsMuchAsPossible',
                           'JobsPerSample' : 20*len(list(runPeriods.keys())) if 'Light' in opt.tag else 8*len(list(runPeriods.keys()))
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

### getCampaignParameters for python3

if hasattr(opt, 'getCampaignParameters') and opt.getCampaignParameters:

    opt.minPlotPt = minPlotPt
    opt.maxPlotPt = maxPlotPt
    opt.maxJetEta = float(maxJetEta)
    opt.bTagAlgorithms = bTagAlgorithms
    opt.btagWPs = list(bTagWorkingPoints.keys())
    opt.ptBins = list(jetPtBins.keys())

    opt.Selections = []
    for selection in systematicVariations:
        sel = 'Central' if selection=='' else selection
        if 'vetosel' in opt.option:
            if sel in opt.option: continue
        elif 'sel' in opt.option and sel not in opt.option: continue
        opt.Selections.append(selection)
    opt.systematicNuisances = systematicNuisances

    if opt.action=='ptHatWeights':
        opt.samples = samples
        opt.qcdMuPtHatBins = qcdMuPtHatBins
        opt.qcdPtHatBins = qcdPtHatBins

    elif opt.action=='workingPoints':
        opt.workingPointName = workingPointName
        opt.workingPointLimit = workingPointLimit
        opt.samples = samples
        opt.nJetMax = nJetMax
        opt.bTagWorkingPoints = bTagWorkingPoints
 
    elif opt.action=='frameworkValidation':                     
        opt.samples = list(samples.keys())
        opt.triggerInfos = triggerInfos                                                                                                                                                                              
    elif opt.action=='kinematicWeights': 
        opt.jetPtBins = jetPtBins         
        opt.minJetPt  = minJetPt
        opt.maxJetPt  = maxJetPt

    elif opt.action=='ptRelInput' or opt.action=='shapesForFit':
        opt.templateTreatments = templateTreatments
        opt.bTemplateCorrector = bTemplateCorrector

    elif opt.action=='storeBTagScaleFactors':
        opt.csvSystematics = csvSystematics

