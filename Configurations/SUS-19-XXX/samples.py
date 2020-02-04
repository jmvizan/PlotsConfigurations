import os
import subprocess
import string
from LatinoAnalysis.Tools.commonTools import *

if '2016' in opt.tag : 
    opt.lumi = 35.9 # 35.92
elif '2017' in opt.tag : 
    opt.lumi = 41.5 # 41.53
elif '2018' in opt.tag : 
    opt.lumi = 59.7 # 59.74
print 'Value of lumi set to', opt.lumi

### Directories
  
SITE=os.uname()[1]

if  'cern' in SITE :
    treeBaseDirSig  = '/eos/cms/store/user/scodella/SUSY/Nano/'
    treeBaseDirData = '/eos/cms/store/caf/user/scodella/BTV/Nano/'
    if '2018' in opt.tag :
        treeBaseDirMC   = '/eos/cms/store/caf/user/scodella/BTV/Nano/'
    else :
        treeBaseDirMC   = '/eos/cms/store/user/scodella/SUSY/Nano/'
elif 'ifca' in SITE:
    treeBaseDirSig  = '/gpfs/projects/tier3data/LatinosSkims/RunII/Nano/'
    treeBaseDirMC   = '/gpfs/projects/tier3data/LatinosSkims/RunII/Nano/'
    treeBaseDirData = '/gpfs/projects/tier3data/LatinosSkims/RunII/Nano/'

if '2016' in opt.tag :
    ProductionMC   = 'Summer16_102X_nAODv4_Full2016v4/MCSusy2016__MCCorr2016Susy'
    ProductionSig  = 'Summer16FS_102X_nAODv4_Full2016v4/susyGen__susyW__MCSusy2016FS__MCCorr2016SusyFS'
    ProductionData = 'Run2016_102X_nAODv4_Full2016v4/DATASusy2016'
elif '2017' in opt.tag :
    ProductionMC   = 'Fall2017_102X_nAODv4_Full2017v4/MCSusy2017__MCCorr2017Susy'
    ProductionSig  = 'Fall2017FS_102X_nAODv4_Full2017v4/susyGen__susyW__MCSusy2017FS__MCCorr2017SusyFS'
    ProductionData = 'Run2017_102X_nAODv4_Full2017v4/DATASusy2017'
elif '2018' in opt.tag :
    ProductionMC   = 'Autumn18_102X_nAODv4_GTv16_Full2018v4/MCSusy2018__MCCorr2018Susy'
    ProductionSig  = 'Autumn18FS_102X_nAODv4_GTv16_Full2018v4/susyGen__susyW__MCSusy2018FS__MCCorr2018SusyFS'
    ProductionData = 'Run2018_102X_nAODv4_14Dec_Full2018v4/DATASusy2018'

regionName = '__susyMT2'

if 'SameSign' in opt.tag :
    regionName = '__susyMT2SameSign'
elif 'Fake' in opt.tag :
    regionName = '__susyMT2Fake'
elif 'WZ' in opt.tag :
    regionName = '__susyMT2WZ'
elif 'WZtoWW' in opt.tag :
    regionName = '__susyMT2WZtoWW'
elif 'ZZ' in opt.tag :
    regionName = '__susyMT2ZZ'
elif 'ttZ' in opt.tag :
    regionName = '__susyMT2ttZ'

directoryBkg  = treeBaseDirMC   + ProductionMC   + regionName + '/'
directorySig  = treeBaseDirSig  + ProductionSig  + regionName + 'FS/' 
directoryData = treeBaseDirData + ProductionData + regionName + '/'
directoryData = directoryData.replace('__susyMT2/', '__susyMT2data/')

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

EleWeight      = 'Lepton_tightElectron_cutBasedMediumPOG_IdIsoSF[0]*Lepton_tightElectron_cutBasedMediumPOG_IdIsoSF[1]'
MuoWeight      = 'Lepton_tightMuon_mediumRelIsoTight_IdIsoSF[0]*Lepton_tightMuon_mediumRelIsoTight_IdIsoSF[1]'
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
            ['B','Run2016B-Nano14Dec2018_ver2-v1'],
            ['C','Run2016C-Nano14Dec2018-v1'] ,
            ['D','Run2016D-Nano14Dec2018-v1'] ,
            ['E','Run2016E-Nano14Dec2018-v1'] ,
            ['F','Run2016F-Nano14Dec2018-v1'] ,
            ['G','Run2016G-Nano14Dec2018-v1'] ,
            ['H','Run2016H-Nano14Dec2018-v1'] 
        ]
    elif '2017' in opt.tag :
        DataRun = [ 
            ['B','Run2017B-Nano14Dec2018-v1'],
            ['C','Run2017C-Nano14Dec2018-v1'],
            ['D','Run2017D-Nano14Dec2018-v1'],
            ['E','Run2017E-Nano14Dec2018-v1'],
            ['F','Run2017F-Nano14Dec2018-v1'],
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
        ['A','Run2018A-Nano14Dec2018-v1'] ,
        ['B','Run2018B-Nano14Dec2018-v1'] ,
        ['C','Run2018C-Nano14Dec2018-v1'] ,
        ['D','Run2018D-Nano14Dec2018_ver2-v1'] ,
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

    samples['ttbar'] = {    'name'   : getSampleFiles(directoryBkg,'TTTo2L2Nu',False,'nanoLatino_'),
                            'weight' : XSWeight+'*'+SFweight+'*'+centralTopPt ,
                            'FilesPerJob' : 2 ,
                        }

    if 'btagefficiencies' in opt.tag:

        samples['T2tt'] = { 'name'   : getSampleFiles(directorySig,'T2tt__mStop-400to1200',False,'nanoLatino_'),
                            'weight' : XSWeight+'*'+SFweight ,
                            'FilesPerJob' : 2 ,
                            }

    if 'btagefficiencies' not in opt.tag and 'Test' not in opt.tag:
    
        tWext = ''
        if '2018' in opt.tag : 
            tWext = '_ext1'
        samples['tW']    = {    'name'   :   getSampleFiles(directoryBkg,'ST_tW_antitop'+tWext,False,'nanoLatino_') +
                                             getSampleFiles(directoryBkg,'ST_tW_top'+tWext,    False,'nanoLatino_'),
                                'weight' : XSWeight+'*'+SFweight ,
                                'FilesPerJob' : 2 ,
                                }

        ttZext = ''
        if '2016' in opt.tag : 
            ttZext = '_ext2'
        samples['ttZ']   = {    'name'   :   getSampleFiles(directoryBkg,'TTZToLLNuNu_M-10'+ttZext,False,'nanoLatino_') + 
                                             getSampleFiles(directoryBkg,'TTZToQQ',                False,'nanoLatino_'),
                                'weight' : XSWeight+'*'+SFweight ,
                                'FilesPerJob' : 2 ,
                                }
        
        samples['ttW']   = {    'name'   :   getSampleFiles(directoryBkg,'TTWJetsToLNu',False,'nanoLatino_') +
                                getSampleFiles(directoryBkg,'TTWJetsToQQ',False,'nanoLatino_'), 
                                'weight' : XSWeight+'*'+SFweight ,
                                'FilesPerJob' : 2 ,
                                }

        if '2018' not in opt.tag : 
            samples['WW']    = {    'name'   :   getSampleFiles(directoryBkg,'WWTo2L2Nu',           False,'nanoLatino_'),
                                    'weight' : XSWeight+'*'+SFweight ,
                                    'FilesPerJob' : 2 ,
                                }
            if '2016' in opt.tag : 
                samples['WW']['name'] += getSampleFiles(directoryBkg,'GluGluWWTo2L2Nu_MCFM',False,'nanoLatino_') 
            elif '2017' in opt.tag : 
                samples['WW']['name'] += getSampleFiles(directoryBkg,'GluGluToWWToENEN',False,'nanoLatino_') \
                                         + getSampleFiles(directoryBkg,'GluGluToWWToENTN',False,'nanoLatino_') \
                                         + getSampleFiles(directoryBkg,'GluGluToWWToMNEN',False,'nanoLatino_') \
                                         + getSampleFiles(directoryBkg,'GluGluToWWToMNMN',False,'nanoLatino_') \
                                         + getSampleFiles(directoryBkg,'GluGluToWWToMNTN',False,'nanoLatino_') \
                                         + getSampleFiles(directoryBkg,'GluGluToWWToTNMN',False,'nanoLatino_') \
                                         + getSampleFiles(directoryBkg,'GluGluToWWToTNTN',False,'nanoLatino_') 
        elif '2018' in opt.tag : 
            samples['WW']    = {    'name'   :   getSampleFiles(directoryBkg,'GluGluToWWToENMN',False,'nanoLatino_') +
                                                 getSampleFiles(directoryBkg,'GluGluToWWToENTN',False,'nanoLatino_') +
                                                 getSampleFiles(directoryBkg,'GluGluToWWToMNMN',False,'nanoLatino_') +
                                                 getSampleFiles(directoryBkg,'GluGluToWWToMNTN',False,'nanoLatino_') +
                                                 getSampleFiles(directoryBkg,'GluGluToWWToTNMN',False,'nanoLatino_') +
                                                 getSampleFiles(directoryBkg,'GluGluToWWToTNTN',False,'nanoLatino_'),
                                    'weight' : XSWeight+'*'+SFweight ,
                                    'FilesPerJob' : 2 ,
                                }
            
        WZext = ''
        if '2016' in opt.tag : 
            WZext = '_ext1'
        samples['WZ']    = {    'name'   :   getSampleFiles(directoryBkg,'WZTo3LNu'+WZext,False,'nanoLatino_'),
                                'weight' : XSWeight+'*'+SFweight ,
                                'FilesPerJob' : 2 ,
                                }

        ZZext = ''
        if '2016' in opt.tag : 
            ZZext = '_ext1'
        elif '2018' in opt.tag : 
            ZZext = '_ext2'
        samples['ZZ']    = {    'name'   :   getSampleFiles(directoryBkg,'ZZTo2L2Nu'+ZZext,False,'nanoLatino_') +
                                getSampleFiles(directoryBkg,'ggZZ2e2n',False,'nanoLatino_') +
                                getSampleFiles(directoryBkg,'ggZZ2m2n',False,'nanoLatino_'),
                                'weight' : XSWeight+'*'+SFweight ,
                                'FilesPerJob' : 2 ,
                                }

        DYM50ext = ''
        DYMlow = 'M-4to50'    
        if '2016' in opt.tag : 
            DYM50ext = '_ext1'
            DYMlow = 'M-5to50'   
        samples['DY']    = {    'name'   :   getSampleFiles(directoryBkg,'DYJetsToLL_M-10to50-LO',        False,'nanoLatino_') +
                                #getSampleFiles(directoryBkg,'DYJetsToLL_'+DYMlow+'_HT-70to100', False,'nanoLatino_') +
                                getSampleFiles(directoryBkg,'DYJetsToLL_'+DYMlow+'_HT-100to200',False,'nanoLatino_') +
                                getSampleFiles(directoryBkg,'DYJetsToLL_'+DYMlow+'_HT-200to400',False,'nanoLatino_') +
                                getSampleFiles(directoryBkg,'DYJetsToLL_'+DYMlow+'_HT-400to600',False,'nanoLatino_') +
                                #getSampleFiles(directoryBkg,'DYJetsToLL_'+DYMlow+'_HT-600toinf',False,'nanoLatino_') +
                                getSampleFiles(directoryBkg,'DYJetsToLL_M-50-LO'+DYM50ext,   False,'nanoLatino_') +
                                #getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-70to100',    False,'nanoLatino_') +
                                getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-100to200',   False,'nanoLatino_') +
                                getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-200to400',   False,'nanoLatino_') +
                                getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-400to600',   False,'nanoLatino_') +
                                getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-600to800',   False,'nanoLatino_') +
                                getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-800to1200',  False,'nanoLatino_'), # +
                                #getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-1200to2500', False,'nanoLatino_') +
                                #getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-2500toinf',  False,'nanoLatino_') ,
                                'weight' : XSWeight+'*'+SFweight ,
                                'FilesPerJob' : 2 ,
                                } 
        if '2016' in opt.tag : 
            samples['DY']['name'] += getSampleFiles(directoryBkg,'DYJetsToLL_'+DYMlow+'_HT-70to100',False,'nanoLatino_') 
            samples['DY']['name'] += getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-70to100',False,'nanoLatino_')
            samples['DY']['name'] += getSampleFiles(directoryBkg,'DYJetsToLL_'+DYMlow+'_HT-600toinf',False,'nanoLatino_') 
            samples['DY']['name'] += getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-2500toinf',False,'nanoLatino_') 
        else :
            if '2017' in opt.tag : 
                samples['DY']['name'] += getSampleFiles(directoryBkg,'DYJetsToLL_'+DYMlow+'_HT-600toInf',False,'nanoLatino_') 
            samples['DY']['name'] += getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-2500toInf',False,'nanoLatino_')
        if '2018' not in opt.tag : 
            samples['DY']['name'] += getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-1200to2500',False,'nanoLatino_') 
        if '2016' in opt.tag : 
            addSampleWeight(samples,'DY','DYJetsToLL_M-10to50-LO',  'LHE_HT<70.0')
            addSampleWeight(samples,'DY','DYJetsToLL_M-50-LO_ext1', 'LHE_HT<70.0')
        else :
            addSampleWeight(samples,'DY','DYJetsToLL_M-10to50-LO',  'LHE_HT<100.0')
            addSampleWeight(samples,'DY','DYJetsToLL_M-50-LO_ext1', 'LHE_HT<100.0')
        
        ggHWWgen = ''
        if '2016' in opt.tag : 
            ggHWWgen = 'AMCNLO'
        ggHTText = ''
        if '2017' in opt.tag : 
            ggHTText = '_ext1'
        samples['HWW']   = {    'name'   :   getSampleFiles(directoryBkg,'GluGluHToWWTo2L2Nu'+ggHWWgen+'_M125',False,'nanoLatino_') + 
                                #getSampleFiles(directoryBkg,'GluGluHToTauTau_M125'+ggHTText,                  False,'nanoLatino_') + 
                                getSampleFiles(directoryBkg,'VBFHToWWTo2L2Nu_M125',                            False,'nanoLatino_') + 
                                #getSampleFiles(directoryBkg,'HWplusJ_HToWW_M125',                              False,'nanoLatino_') + 
                                getSampleFiles(directoryBkg,'HWminusJ_HToWW_M125',                             False,'nanoLatino_') ,
                                'weight' : XSWeight+'*'+SFweight ,
                                'FilesPerJob' : 2 ,
                                }
        if '2018' not in opt.tag : 
            samples['HWW']['name'] += getSampleFiles(directoryBkg,'GluGluHToTauTau_M125'+ggHTText,False,'nanoLatino_')
        if '2017' not in opt.tag : 
            samples['HWW']['name'] += getSampleFiles(directoryBkg,'HWplusJ_HToWW_M125',False,'nanoLatino_') 

        if '2018' not in opt.tag : 
            samples['VZ']    = {    'name'   :   getSampleFiles(directoryBkg,'WZTo2L2Q',False,'nanoLatino_') + 
                                    getSampleFiles(directoryBkg,'ZZTo2L2Q',False,'nanoLatino_'),
                                    'weight' : XSWeight+'*'+SFweight ,
                                    'FilesPerJob' : 2 ,
                                    }
        
        samples['VVV']   = {    'name'   :   getSampleFiles(directoryBkg,'WWW',False,'nanoLatino_') + 
                                getSampleFiles(directoryBkg,'WWZ',False,'nanoLatino_') + 
                                getSampleFiles(directoryBkg,'WZZ',False,'nanoLatino_') +
                                getSampleFiles(directoryBkg,'ZZZ',False,'nanoLatino_'),
                                'weight' : XSWeight+'*'+SFweight ,
                                'FilesPerJob' : 2 ,
                                }
        
        if 'ZZ' in opt.tag or 'ttZ' in opt.tag :
            
            ZZ4Lext = ''
            if '2017' in opt.tag : 
                ZZ4Lext = '_ext1'
            elif '2018' in opt.tag : 
                ZZ4Lext = '_ext2'
            samples['ZZTo4L']   = {    'name'   :   getSampleFiles(directoryBkg,'ZZTo4L'+ZZ4Lext, False,'nanoLatino_') + 
                                       getSampleFiles(directoryBkg,'ggZZ4e',              False,'nanoLatino_') +
                                       #getSampleFiles(directoryBkg,'ggZZ4m',              False,'nanoLatino_') +
                                       getSampleFiles(directoryBkg,'ggZZ4t',              False,'nanoLatino_') +
                                       getSampleFiles(directoryBkg,'ggZZ2e2m',            False,'nanoLatino_') +
                                       getSampleFiles(directoryBkg,'ggZZ2e2t',            False,'nanoLatino_') +
                                       getSampleFiles(directoryBkg,'ggZZ2m2t',            False,'nanoLatino_'), # +
                                       #getSampleFiles(directoryBkg,'qqHToZZTo4L_M125',    False,'nanoLatino_') +
                                       #getSampleFiles(directoryBkg,'GluGluHToZZTo4L_M125',False,'nanoLatino_'),
                                       'weight' : XSWeight+'*'+SFweight ,
                                       'FilesPerJob' : 2 ,
                                       }
            if '2017' not in opt.tag : 
                samples['ZZTo4L']['name'] += getSampleFiles(directoryBkg,'ggZZ4m',False,'nanoLatino_')
            if '2016' in opt.tag : 
                samples['ZZTo4L']['name'] += getSampleFiles(directoryBkg,'qqHToZZTo4L_M125',False,'nanoLatino_')
                samples['ZZTo4L']['name'] += getSampleFiles(directoryBkg,'GluGluHToZZTo4L_M125',False,'nanoLatino_')

if 'Backgrounds' in opt.sigset and opt.sigset not in 'Backgrounds':

    sampleToRemove = [ ] 

    for sample in samples:
        if sample not in opt.sigset:
            sampleToRemove.append(sample)

    for sample in sampleToRemove:
        del samples[sample]

### Data

if 'SM' in opt.sigset or 'Data' in opt.sigset:

    samples['DATA']  = {   'name': [ ] ,    
                           'weight' : '1.', 
                           'weights' : [ ],
                           'isData': ['all'],                            
                           'FilesPerJob' : 20 ,
                       }

    for Run in DataRun :
        for DataSet in DataSets :
            FileTarget = getSampleFiles(directoryData,DataSet+'_'+Run[1],True,'nanoLatino_')
            for iFile in FileTarget:
                #print(iFile)
                samples['DATA']['name'].append(iFile)
                samples['DATA']['weights'].append(DataTrig[DataSet]+'*'+METFilters_Data)

### Signals

#exec(open(opt.signalMassPointsFile).read())
exec(open('./signalMassPoints.py').read())

for model in signalMassPoints:
    if model in opt.sigset:
        # v4 patch... 
        BranchingRatio = '(0.10497000068426132)' if (model=='TChipmWW') else '(1.)'
        if ('TChipm' in model): BranchingRatio = BranchingRatio.replace(')', '/1000.)')
        for massPoint in signalMassPoints[model]:
            if massPointInSignalSet(massPoint, opt.sigset):

                # v4 patch... 
                XSWeight       = 'baseW*genWeight'
                if '2017' in opt.tag or '2018' in opt.tag : 
                    if 'T2tt__mStop-400to1200' in signalMassPoints[model][massPoint]['massPointDataset'] :

                        stopTerm = massPoint.split('_')[1]
                        stopMass = int(stopTerm.replace('mS-', ''))
                        if stopMass<735:
                            XSWeight = '0.00192*genWeight'
                        else:
                            XSWeight = '1000.*Xsec*genWeight/30000.'

                samples[massPoint] = { 'name'   : getSampleFiles(directorySig,signalMassPoints[model][massPoint]['massPointDataset'],False,'nanoLatino_'),
                                       'weight' : BranchingRatio+'*'+XSWeight+'*'+SFweightFS+'*'+signalMassPoints[model][massPoint]['massPointCut'] ,
                                       'FilesPerJob' : 2 ,
                                       'fastsim' : 1.
                                   }
                
