import os
import subprocess
import string
from LatinoAnalysis.Tools.commonTools import *

### Generals

if '2016' in opt.tag : 
    opt.lumi = 35.9 # 35.92
elif '2017' in opt.tag : 
    opt.lumi = 41.5 # 41.53
elif '2018' in opt.tag : 
    opt.lumi = 59.7 # 59.74
print 'Value of lumi set to', opt.lumi

treePrefix= 'nanoLatino_'

### Directories
  
SITE=os.uname()[1]

if  'cern' in SITE :
    treeBaseDirData = '/eos/cms/store/user/scodella/SUSY/Nano/'
    if '2016' in opt.tag : 
        treeBaseDirMC   = '/eos/cms/store/user/scodella/SUSY/Nano/'
    else : 
        treeBaseDirMC   = '/eos/cms/store/caf/user/scodella/BTV/Nano/'
    treeBaseDirSig  = treeBaseDirMC
elif 'ifca' in SITE or 'cloud' in SITE:
    treeBaseDirSig  = '/gpfs/projects/tier3data/LatinosSkims/RunII/Nano/'
    treeBaseDirMC   = '/gpfs/projects/tier3data/LatinosSkims/RunII/Nano/'
    treeBaseDirData = '/gpfs/projects/tier3data/LatinosSkims/RunII/Nano/'

if '2016' in opt.tag :
    ProductionMC   = 'Summer16_102X_nAODv6_Full2016v6/MCSusy2016v6__MCCorr2016Susyv6'
    ProductionSig  = 'Summer16FS_102X_nAODv6_Full2016v6/hadd__susyGen__MCSusy2016FSv6__susyW__MCCorr2016SusyFSv6'
    ProductionData = 'Run2016_102X_nAODv6_Full2016v6/DATASusy2016v6__hadd'
elif '2017' in opt.tag :
    ProductionMC   = 'Fall2017_102X_nAODv6_Full2017v6/MCSusy2017v6__MCCorr2017Susyv6'
    ProductionSig  = 'Fall2017FS_102X_nAODv6_Full2017v6/hadd__susyGen__MCSusy2017FSv6__susyW__MCCorr2017SusyFSv6'
    ProductionData = 'Run2017_102X_nAODv6_Full2017v6/DATASusy2017v6__hadd'
elif '2018' in opt.tag :
    ProductionMC   = 'Autumn18_102X_nAODv6_Full2018v6/MCSusy2018v6__MCCorr2018Susyv6'
    ProductionSig  = 'Autumn18FS_102X_nAODv6_Full2018v6/hadd__susyGen__MCSusy2018FSv6__susyW__MCCorr2018SusyFSv6'
    ProductionData = 'Run2018_102X_nAODv6_Full2018v6/DATASusy2018v6__hadd'

regionName = '__susyMT2'

if 'SameSign' in opt.tag :
    regionName = '__susyMT2SameSign'
elif 'Fake' in opt.tag :
    regionName = '__susyMT2Fake'
elif 'WZtoWW' in opt.tag :
    regionName = '__susyMT2WZtoWW'
elif 'WZ' in opt.tag :
    regionName = '__susyMT2WZ'
elif 'ZZ' in opt.tag :
    regionName = '__susyMT2ZZ'
elif 'ttZ' in opt.tag :
    regionName = '__susyMT2ttZ'

directoryBkg  = treeBaseDirMC   + ProductionMC   + regionName + '/'
directorySig  = treeBaseDirSig  + ProductionSig  + regionName + 'FS/' 
directoryData = treeBaseDirData + ProductionData + regionName + '/'
directoryData = directoryData.replace('__susyMT2/', '__susyMT2data/')

# Complex cut variables

ElectronWP = 'Lepton_isTightElectron_cutBasedMediumPOG'
if 'IP' in opt.tag:
    ElectronWP += 'IP'
elif 'EleMiniIso' in opt.tag:
    ElectronWP = 'Lepton_isTightElectron_cutBasedMediumMiniIso'
elif 'EleTightPOG' in opt.tag:
    ElectronWP = 'Lepton_isTightElectron_cutBasedTightPOG'
MuonWP     = 'Lepton_isTightMuon_mediumRelIsoTight'

ElectronSF = ElectronWP.replace('isTightElectron', 'tightElectron')
MuonSF     = MuonWP.replace('isTightMuon', 'tightMuon')

LepId = '('+ElectronWP+'[0]+'+MuonWP+'[0]+'+ElectronWP+'[1]+'+MuonWP+'[1])==2'
LepId3 = '('+ElectronWP+'[0]+'+MuonWP+'[0]+'+ElectronWP+'[1]+'+MuonWP+'[1]+'+ElectronWP+'[2]+'+MuonWP+'[2])==3'
LepId3of4 = '('+ElectronWP+'[0]+'+MuonWP+'[0]+'+ElectronWP+'[1]+'+MuonWP+'[1]+'+ElectronWP+'[2]+'+MuonWP+'[2]+'+ElectronWP+'[3]+'+MuonWP+'[3])==3'

T0 = '('+ElectronWP+'[0]+'+MuonWP+'[0])'
T1 = '('+ElectronWP+'[1]+'+MuonWP+'[1])'
T2 = '('+ElectronWP+'[2]+'+MuonWP+'[2])'

BTAG = '(leadingPtTagged_btagDeepBM_1c>=20.)' 
VETO = '!'+BTAG

BTAG30= '(leadingPtTagged_btagDeepBM_1c>=30.)'
VETO30 = '!'+BTAG30

btagWeight1tag = 'btagWeight_1tag_btagDeepBM_1c'
btagWeight0tag = '(1.-'+btagWeight1tag+')'

ISRCut = 'CleanJet_pt[0]>150. && CleanJet_pt[0]!=leadingPtTagged_btagDeepBM_1c && acos(cos(ptmiss_phi-CleanJet_phi[0]))>2.5'
ISRCutData = ' '+ISRCut+' && '
ISRCutMC   = '&& '+ISRCut

### MET Filters

METFilters_Common = 'Flag_goodVertices*Flag_HBHENoiseFilter*Flag_HBHENoiseIsoFilter*Flag_EcalDeadCellTriggerPrimitiveFilter*Flag_BadPFMuonFilter'
if '2017' in opt.tag or '2018' in opt.tag : # Deprecated ???
    METFilters_Common += '*Flag_ecalBadCalibFilter' 
METFilters_MC     = METFilters_Common + '*Flag_globalSuperTightHalo2016Filter'
METFilters_Data   = METFilters_Common + '*Flag_globalSuperTightHalo2016Filter*Flag_eeBadScFilter'
METFilters_FS     = METFilters_Common

### Trigger Efficiencies

TriggerEff = 'TriggerEffWeight_2l'

if 'WZ' in opt.tag or 'ZZ' in opt.tag or 'ttZ' in opt.tag :
    TriggerEff = 'TriggerEffWeight_3l'

### MC weights

# generation weights

XSWeight       = 'baseW*genWeight'

# lepton weights

EleWeight      = ElectronSF+'_IdIsoSF[0]*'+ElectronSF+'_IdIsoSF[1]'
MuoWeight      = MuonSF+'_IdIsoSF[0]*'+MuonSF+'_IdIsoSF[1]'
LepWeight      = EleWeight + '*' + MuoWeight
EleWeightFS    = EleWeight.replace('IdIsoSF', 'FastSimSF')
MuoWeightFS    = MuoWeight.replace('IdIsoSF', 'FastSimSF')
LepWeightFS    = LepWeight.replace('IdIsoSF', 'FastSimSF')

# nonprompt lepton rate

#nonpromptLep = { 'rate' : '1.00', 'rateUp' : '1.50', 'rateDown' : '0.50' } 
nonpromptLep = { 'rate' : '1.08', 'rateUp' : '1.29', 'rateDown' : '0.87' } 
promptLeptons = 'Lepton_promptgenmatched[0]*Lepton_promptgenmatched[1]'
nonpromptLepSF      = '( ' + promptLeptons + ' + (1. - ' + promptLeptons + ')*' + nonpromptLep['rate']      + ')'
nonpromptLepSF_Up   = '( ' + promptLeptons + ' + (1. - ' + promptLeptons + ')*' + nonpromptLep['rateUp']    + ')'
nonpromptLepSF_Down = '( ' + promptLeptons + ' + (1. - ' + promptLeptons + ')*' + nonpromptLep['rateDown']  + ')'

# global SF weights 

SFweightCommon = 'puWeight*' + TriggerEff + '*' + LepWeight + '*' + nonpromptLepSF
if '2016' in opt.tag or '2017' in opt.tag: 
    SFweightCommon += '*PrefireWeight'
SFweight       = SFweightCommon + '*' + METFilters_MC
SFweightFS     = SFweightCommon + '*' + METFilters_FS + '*' + LepWeightFS + '*isrW'

### Special weights

# background cross section uncertainties and normalization scale factors

normBackgrounds = {
    #'ttbar' : { 'all'   : { 'scalefactor' : { '1.00' : '0.10' }, 'cuts' : [], 'selections' : { '_All'   : '1.' } } },
    'tW'    : { 'all'   : { 'scalefactor' : { '1.00' : '0.10' }, 'cuts' : [], 'selections' : { '_All'   : '1.' } } },
    #'WW'    : { 'all'   : { 'scalefactor' : { '1.00' : '0.10' }, 'cuts' : [], 'selections' : { '_All'   : '1.' } } },
    'ttW'   : { 'all'   : { 'scalefactor' : { '1.00' : '0.50' }, 'cuts' : [], 'selections' : { '_All'   : '1.' } } },
    'VZ'    : { 'all'   : { 'scalefactor' : { '1.00' : '0.50' }, 'cuts' : [], 'selections' : { '_All'   : '1.' } } },
    'VVV'   : { 'all'   : { 'scalefactor' : { '1.00' : '0.50' }, 'cuts' : [], 'selections' : { '_All'   : '1.' } } },
    'WZ'    : { 'all'   : { 'scalefactor' : { '0.97' : '0.09' }, 'cuts' : [], 'selections' : { '_All'   : '1.' } } },
    'ttZ'   : { 'all'   : { 'scalefactor' : { '1.44' : '0.36' }, 'cuts' : [], 'selections' : { '_All'   : '1.' } } },
    'ZZ'    : { 'nojet' : { 'scalefactor' : { '0.74' : '0.19' }, 'cuts' : [], 'selections' : { '_NoJet' : '(nCleanJet==0)' } },  
                'notag' : { 'scalefactor' : { '1.21' : '0.17' }, 'cuts' : [], 'selections' : { '_NoTag' : '((nCleanJet>=1)*(leadingPtTagged<20.))',
                                                                                               '_Tag'   : '(leadingPtTagged>=20.)'  } },   
                'veto'  : { 'scalefactor' : { '1.06' : '0.12' }, 'cuts' : [], 'selections' : { '_Veto'  : '(leadingPtTagged<20.)' } }, }, 
    'DY'    : { 'nojet' : { 'scalefactor' : { '1.00' : '1.00' }, 'cuts' : [], 'selections' : { '_NoJet' : '(nCleanJet==0)' } },
                'notag' : { 'scalefactor' : { '1.00' : '0.32' }, 'cuts' : [], 'selections' : { '_NoTag' : '((nCleanJet>=1)*(leadingPtTagged<20.))',
                                                                                               '_Tag'   : '(leadingPtTagged>=20.)',
                                                                                               '_Veto'  : '(leadingPtTagged<20.)' } }, },
}

# top pt reweighting

Top_pTrw = '(TMath::Sqrt( TMath::Exp(0.0615-0.0005*topGenPt) * TMath::Exp(0.0615-0.0005*antitopGenPt) ) )'
centralTopPt = Top_pTrw 
systematicTopPt = '1.'

### Data info

if '2016' in opt.tag or '2017' in opt.tag :

    if '2016' in opt.tag :
        DataRun = [ 
            ['B','Run2016B-Nano25Oct2019_ver2-v1'],
            ['C','Run2016C-Nano25Oct2019-v1'] ,
            ['D','Run2016D-Nano25Oct2019-v1'] ,
            ['E','Run2016E-Nano25Oct2019-v1'] ,
            ['F','Run2016F-Nano25Oct2019-v1'] ,
            ['G','Run2016G-Nano25Oct2019-v1'] ,
            ['H','Run2016H-Nano25Oct2019-v1'] 
        ]
    elif '2017' in opt.tag :
        DataRun = [ 
            ['B','Run2017B-Nano25Oct2019-v1'],
            ['C','Run2017C-Nano25Oct2019-v1'],
            ['D','Run2017D-Nano25Oct2019-v1'],
            ['E','Run2017E-Nano25Oct2019-v1'],
            ['F','Run2017F-Nano25Oct2019-v1'],
        ]

    DataSets = ['MuonEG','DoubleMuon','SingleMuon','DoubleEG','SingleElectron']

    DataTrig = {
        'MuonEG'         : 'Trigger_ElMu' ,
        'DoubleMuon'     : '!Trigger_ElMu && Trigger_dblMu' ,
        'SingleMuon'     : '!Trigger_ElMu && !Trigger_dblMu && Trigger_sngMu' ,
        'DoubleEG'       : '!Trigger_ElMu && !Trigger_dblMu && !Trigger_sngMu && Trigger_dblEl' ,
        'SingleElectron' : '!Trigger_ElMu && !Trigger_dblMu && !Trigger_sngMu && !Trigger_dblEl && Trigger_sngEl' ,
    }

elif '2018' in opt.tag :

    DataRun = [ 
        ['A','Run2018A-Nano25Oct2019-v1'] ,
        ['B','Run2018B-Nano25Oct2019-v1'] ,
        ['C','Run2018C-Nano25Oct2019-v1'] ,
        ['D','Run2018D-Nano25Oct2019_ver2-v1'] ,
    ]

    DataSets = ['MuonEG','DoubleMuon','SingleMuon','EGamma']

    DataTrig = {
        'MuonEG'         : 'Trigger_ElMu' ,
        'DoubleMuon'     : '!Trigger_ElMu && Trigger_dblMu' ,
        'SingleMuon'     : '!Trigger_ElMu && !Trigger_dblMu && Trigger_sngMu' ,
        'EGamma'         : '!Trigger_ElMu && !Trigger_dblMu && !Trigger_sngMu && (Trigger_sngEl || Trigger_dblEl)' ,
    }



### Backgrounds

if 'SM' in opt.sigset or 'Backgrounds' in opt.sigset:

    ttbarFlag = '_PSWeights' if ('2017' in opt.tag) else ''
    samples['ttbar'] = {    'name'   : getSampleFiles(directoryBkg,'TTTo2L2Nu'+ttbarFlag,False,treePrefix),
                            'weight' : XSWeight+'*'+SFweight+'*'+centralTopPt ,
                            'FilesPerJob' : 2 ,
                        }

    if 'btagefficiencies' in opt.tag:

        samples['T2tt'] = { 'name'   : getSampleFiles(directorySig,'T2tt__mStop-400to1200',False,treePrefix),
                            'weight' : XSWeight+'*'+SFweight ,
                            'FilesPerJob' : 2 ,
                            }

    if 'btagefficiencies' not in opt.tag and 'Test' not in opt.tag:
    
        tWext = '_ext1' if ('2018' in opt.tag) else ''
        samples['tW']    = {    'name'   :   getSampleFiles(directoryBkg,'ST_tW_antitop'+tWext,False,treePrefix) +
                                             getSampleFiles(directoryBkg,'ST_tW_top'+tWext,    False,treePrefix),
                                'weight' : XSWeight+'*'+SFweight ,
                                'FilesPerJob' : 2 ,
                            }

        ttZToLLext = '_ext3' if ('2016' in opt.tag) else ''
        ttZToQQext = '_ext1' if ('2017' in opt.tag) else ''
        samples['ttZ']   = {    'name'   :   getSampleFiles(directoryBkg,'TTZToLLNuNu_M-10'+ttZToLLext,False,treePrefix) + 
                                             getSampleFiles(directoryBkg,'TTZToQQ'         +ttZToQQext,False,treePrefix),
                                'weight' : XSWeight+'*'+SFweight ,
                                'FilesPerJob' : 2 ,
                                }
        
        ttWToLLext = ''
        if ('2016' in opt.tag): ttWToLLext = '_ext2'
        if ('2017' in opt.tag): ttWToLLext = '_newpmx'
        samples['ttW']   = {    'name'   :   getSampleFiles(directoryBkg,'TTWJetsToLNu'+ttWToLLext,False,treePrefix) +
                                getSampleFiles(directoryBkg,'TTWJetsToQQ',False,treePrefix), 
                                'weight' : XSWeight+'*'+SFweight ,
                                'FilesPerJob' : 2 ,
                                'suppressNegative':['all'],
                                'suppressNegativeNuisances' :['all'],
                                }

         
        samples['WW']    = {    'name'   :   getSampleFiles(directoryBkg,'WWTo2L2Nu',           False,treePrefix),
                                'weight' : XSWeight+'*'+SFweight ,
                                'FilesPerJob' : 2 ,
        }
        if '2016' in opt.tag : 
            samples['WW']['name'] += getSampleFiles(directoryBkg,'GluGluWWTo2L2Nu_MCFM',False,treePrefix) 
        else : 
            samples['WW']['name'] += getSampleFiles(directoryBkg,'GluGluToWWToENEN',False,treePrefix) \
                                   + getSampleFiles(directoryBkg,'GluGluToWWToENMN',False,treePrefix) \
                                   + getSampleFiles(directoryBkg,'GluGluToWWToENTN',False,treePrefix) \
                                   + getSampleFiles(directoryBkg,'GluGluToWWToMNEN',False,treePrefix) \
                                   + getSampleFiles(directoryBkg,'GluGluToWWToMNMN',False,treePrefix) \
                                   + getSampleFiles(directoryBkg,'GluGluToWWToMNTN',False,treePrefix) \
                                   + getSampleFiles(directoryBkg,'GluGluToWWToTNEN',False,treePrefix) \
                                   + getSampleFiles(directoryBkg,'GluGluToWWToTNMN',False,treePrefix) \
                                   + getSampleFiles(directoryBkg,'GluGluToWWToTNTN',False,treePrefix)

        WZext = '_ext1' if ('2018' in opt.tag) else ''
        samples['WZ']    = {    'name'   :   getSampleFiles(directoryBkg,'WZTo3LNu'+WZext,False,treePrefix),
                                'weight' : XSWeight+'*'+SFweight ,
                                'FilesPerJob' : 2 ,
                                }

        ZZext = ''
        if '2016' in opt.tag : 
            ZZext = '_ext1'
        elif '2018' in opt.tag : 
            ZZext = '_ext2'
        samples['ZZ']    = {    'name'   : getSampleFiles(directoryBkg,'ZZTo2L2Nu'+ZZext,False,treePrefix) +
                                           getSampleFiles(directoryBkg,'ggZZ2e2n',       False,treePrefix) +
                                           getSampleFiles(directoryBkg,'ggZZ2m2n',       False,treePrefix),
                                'weight' : XSWeight+'*'+SFweight ,
                                'suppressNegative':['all'],
                                'suppressNegativeNuisances' :['all'],
                                'FilesPerJob' : 2 ,
                                }

        DYM10ext = '_ext1' if ('2016' not in opt.tag) else ''
        DYMlow = 'M-5to50' if ('2016' in opt.tag) else 'M-4to50' 
        DYMlowHT70ext, DYMlowHT100ext, DYMlowHT200ext, DYMlowHT400ext, DYMlowHT600ext = '', '', '', '', '' 
        if '2016' in opt.tag:
            DYMlowHT100ext = '_ext1'
            DYMlowHT200ext = '_ext1'
            DYMlowHT400ext = '_ext1'
            DYMlowHT600ext = '_ext1'
        DYM50ext = '_ext2' if ('2016' in opt.tag) else ''
        DYMhighHT70ext = ''
        DYMhighHT100ext = '_ext1' if ('2018' not in opt.tag) else ''
        DYMhighHT200ext = '_ext1' if ('2016' in opt.tag) else ''
        DYMhighHT400ext = '_ext1' if ('2018' not in opt.tag) else ''
        DYMhighHT600ext = '_newpmx' if ('2017' in opt.tag) else ''
        DYMhighHT800ext = '_newpmx' if ('2017' in opt.tag) else ''
        DYMhighHT1200ext = '' 
        DYMhighHT2500ext = '_newpmx' if ('2017' in opt.tag) else ''
        samples['DY']    = {    'name'   :   getSampleFiles(directoryBkg,'DYJetsToLL_M-10to50-LO'+DYM10ext,        False,treePrefix) +
                                #getSampleFiles(directoryBkg,'DYJetsToLL_'+DYMlow+'_HT-70to100'+DYMlowHT70ext, False,treePrefix) +
                                getSampleFiles(directoryBkg,'DYJetsToLL_'+DYMlow+'_HT-100to200'+DYMlowHT100ext,False,treePrefix) +
                                getSampleFiles(directoryBkg,'DYJetsToLL_'+DYMlow+'_HT-200to400'+DYMlowHT200ext,False,treePrefix) +
                                getSampleFiles(directoryBkg,'DYJetsToLL_'+DYMlow+'_HT-400to600'+DYMlowHT400ext,False,treePrefix) +
                                getSampleFiles(directoryBkg,'DYJetsToLL_'+DYMlow+'_HT-600toInf'+DYMlowHT600ext,False,treePrefix) +
                                getSampleFiles(directoryBkg,'DYJetsToLL_M-50-LO'+DYM50ext,   False,treePrefix) +
                                getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-70to100'+DYMhighHT70ext,    False,treePrefix) +
                                getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-100to200'+DYMhighHT100ext,   False,treePrefix) +
                                getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-200to400'+DYMhighHT200ext,   False,treePrefix) +
                                getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-400to600'+DYMhighHT400ext,   False,treePrefix) +
                                getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-600to800'+DYMhighHT600ext,   False,treePrefix) +
                                getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-800to1200'+DYMhighHT800ext,  False,treePrefix) +
                                getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-1200to2500'+DYMhighHT1200ext, False,treePrefix) +
                                getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-2500toInf'+DYMhighHT2500ext,  False,treePrefix) ,
                                'weight' : XSWeight+'*'+SFweight ,
                                'FilesPerJob' : 2 ,
                                } 
        if '2016' in opt.tag : 
            samples['DY']['name'] += getSampleFiles(directoryBkg,'DYJetsToLL_'+DYMlow+'_HT-70to100',False,treePrefix)
            addSampleWeight(samples,'DY','DYJetsToLL_M-10to50-LO',  'LHE_HT<70.0')
        else :
            addSampleWeight(samples,'DY','DYJetsToLL_M-10to50-LO',  'LHE_HT<100.0')
        addSampleWeight(samples,'DY','DYJetsToLL_M-50-LO_ext1', 'LHE_HT<70.0')
        
        ggHWWgen = 'AMCNLO'  if ('2016' in opt.tag) else ''
        ggHTText = '_newpmx' if ('2017' in opt.tag) else ''
        samples['HWW']   = {    'name'   :   getSampleFiles(directoryBkg,'GluGluHToWWTo2L2Nu'+ggHWWgen+'_M125',False,treePrefix) + 
                                             getSampleFiles(directoryBkg,'GluGluHToTauTau_M125'+ggHTText,      False,treePrefix) + 
                                             getSampleFiles(directoryBkg,'VBFHToWWTo2L2Nu_M125',               False,treePrefix) + 
                                             getSampleFiles(directoryBkg,'VBFHToTauTau_M125',                  False,treePrefix) + 
                                             getSampleFiles(directoryBkg,'HWplusJ_HToWW_M125',                 False,treePrefix) +  
                                             getSampleFiles(directoryBkg,'HWplusJ_HToTauTau_M125',             False,treePrefix) + 
                                             getSampleFiles(directoryBkg,'HWminusJ_HToWW_M125',                False,treePrefix) + 
                                             getSampleFiles(directoryBkg,'HWminusJ_HToTauTau_M125',            False,treePrefix) ,
                                'weight' : XSWeight+'*'+SFweight ,
                                'suppressNegative':['all'],
                                'suppressNegativeNuisances' :['all'],
                                'FilesPerJob' : 2 ,
                                }

        samples['VZ']    = {    'name'   :   getSampleFiles(directoryBkg,'WZTo2L2Q',False,treePrefix) + 
                                             getSampleFiles(directoryBkg,'ZZTo2L2Q',False,treePrefix),
                                'weight' : XSWeight+'*'+SFweight ,
                                'suppressNegative':['all'],
                                'suppressNegativeNuisances' :['all'],
                                'FilesPerJob' : 2 ,
        }
        
        samples['VVV']   = {    'name'   :   getSampleFiles(directoryBkg,'WWW',False,treePrefix) + 
                                             getSampleFiles(directoryBkg,'WWZ',False,treePrefix) + 
                                             getSampleFiles(directoryBkg,'WZZ',False,treePrefix) +
                                             getSampleFiles(directoryBkg,'ZZZ',False,treePrefix) +
                                             getSampleFiles(directoryBkg,'WWG',False,treePrefix),
                                'weight' : XSWeight+'*'+SFweight ,
                                'FilesPerJob' : 2 ,
                                }
        
        if 'ZZ' in opt.tag or 'ttZ' in opt.tag or 'WZValidationRegion' in opt.tag or 'WZtoWWValidationRegion' in opt.tag:
            
            ZZ4Lext = '_ext2' if ('2018' in opt.tag) else '_ext1'
            samples['ZZTo4L']   = {    'name'   :   getSampleFiles(directoryBkg,'ZZTo4L'+ZZ4Lext, False,treePrefix) + 
                                       getSampleFiles(directoryBkg,'ggZZ4e',              False,treePrefix) +
                                       getSampleFiles(directoryBkg,'ggZZ4m',              False,treePrefix) +
                                       getSampleFiles(directoryBkg,'ggZZ4t',              False,treePrefix) +
                                       getSampleFiles(directoryBkg,'ggZZ2e2m',            False,treePrefix) +
                                       getSampleFiles(directoryBkg,'ggZZ2e2t',            False,treePrefix) +
                                       getSampleFiles(directoryBkg,'ggZZ2m2t',            False,treePrefix) +
                                       getSampleFiles(directoryBkg,'VBFHToZZTo4L_M125',   False,treePrefix) +
                                       getSampleFiles(directoryBkg,'GluGluHToZZTo4L_M125',False,treePrefix),
                                       'weight' : XSWeight+'*'+SFweight ,
                                       'FilesPerJob' : 2 ,
                                   }

        if 'SameSignValidationRegion' in opt.tag:
    
            ttSemilepFlag = '_ext3' if ('2018' in opt.tag) else ''
            samples['ttSemilep'] = { 'name'   : getSampleFiles(directoryBkg,'TTToSemiLeptonic'+ttSemilepFlag,False,treePrefix),
                                     'weight' : XSWeight+'*'+SFweight ,
                                     'FilesPerJob' : 2 ,
                                    }

if 'Backgrounds' in opt.sigset and opt.sigset not in 'Backgrounds' and 'Backgrounds-' not in opt.sigset:

    sampleToRemove = [ ] 

    for sample in samples:
        if 'Veto' in opt.sigset:
            if sample in opt.sigset:
                sampleToRemove.append(sample)
        elif sample not in opt.sigset:
            sampleToRemove.append(sample)

    for sample in sampleToRemove:
        del samples[sample]

for sample in samples:
    samples[sample]['isSignal']  = 0
    samples[sample]['isDATA']    = 0
    samples[sample]['isFastsim'] = 0

### Data

if 'SM' in opt.sigset or 'Data' in opt.sigset:

    samples['DATA']  = {   'name': [ ] ,    
                           'weight' : '1.', 
                           'weights' : [ ],
                           'isData': ['all'],                            
                           'FilesPerJob' : 20 ,
                           'isSignal'  : 0,
                           'isDATA'    : 1, 
                           'isFastsim' : 0
                       }

    for Run in DataRun :
        for DataSet in DataSets :
            FileTarget = getSampleFiles(directoryData,DataSet+'_'+Run[1],True,treePrefix)
            for iFile in FileTarget:
                samples['DATA']['name'].append(iFile)
                samples['DATA']['weights'].append(DataTrig[DataSet]+'*'+METFilters_Data)

### Signals

exec(open('./signalMassPoints.py').read())

for model in signalMassPoints:
    if model in opt.sigset:
        for massPoint in signalMassPoints[model]:
            if massPointInSignalSet(massPoint, opt.sigset):

                samples[massPoint] = { 'name'   : getSampleFiles(directorySig,signalMassPoints[model][massPoint]['massPointDataset'],False,treePrefix),
                                       'weight' : XSWeight+'*'+SFweightFS+'*'+signalMassPoints[model][massPoint]['massPointCut'] ,
                                       'FilesPerJob' : 2 ,
                                       'suppressNegative':['all'],
                                       'suppressNegativeNuisances' :['all'],
                                       'suppressZeroTreeNuisances' : ['all'],
                                       'isSignal'  : 1,
                                       'isDATA'    : 0, 
                                       'isFastsim' : 1
                                   }
                
