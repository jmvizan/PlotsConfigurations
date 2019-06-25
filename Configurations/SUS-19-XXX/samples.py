import os
import subprocess
import string
from LatinoAnalysis.Tools.commonTools import *

### Directories
  
SITE=os.uname()[1]

if  'cern' in SITE :
    treeBaseDirMC   = '/eos/cms/store/user/scodella/SUSY/Nano/'
    treeBaseDirData = '/eos/cms/store/caf/user/scodella/BTV/Nano/'

directoryBkg  = treeBaseDirMC   + 'Summer16_102X_nAODv4_Full2016v4/MCl1loose2016__MCCorr2016__susyMT2__btagPerEvent/'
directorySig  = treeBaseDirMC   + 'Summer16FS_102X_nAODv4_Full2016v4/susyGen__susyW__MCl1loose2016__MCCorr2016FS__susyMT2__btagPerEvent/'
directoryData = treeBaseDirData + 'Run2016_102X_nAODv4_Full2016v4/DATAl1loose2016__susyMT2data__btagPerEventData/'

### MC weights

XSWeight      = 'baseW'
SFweight      = 'puWeight*btagWeight'

### Filters



### Data info

DataRun = [ 
            ['B','Run2016B-Nano14Dec2018_ver2-v1'],
            ['C','Run2016C-Nano14Dec2018-v1'] ,
            ['D','Run2016D-Nano14Dec2018-v1'] ,
            ['E','Run2016E-Nano14Dec2018-v1'] ,
            ['F','Run2016F-Nano14Dec2018-v1'] ,
            ['G','Run2016G-Nano14Dec2018-v1'] ,
            ['H','Run2016H-Nano14Dec2018-v1'] 
          ]

DataSets = ['MuonEG','DoubleMuon','SingleMuon','DoubleEG','SingleElectron']

DataTrig = {
            'MuonEG'         : 'Trigger_ElMu' ,
            'DoubleMuon'     : '!Trigger_ElMu && Trigger_dblMu' ,
            'SingleMuon'     : '!Trigger_ElMu && !Trigger_dblMu && Trigger_sngMu' ,
            'DoubleEG'       : '!Trigger_ElMu && !Trigger_dblMu && !Trigger_sngMu && Trigger_dblEl' ,
            'SingleElectron' : '!Trigger_ElMu && !Trigger_dblMu && !Trigger_sngMu && !Trigger_dblEl && Trigger_sngEl' ,
           }

### Backgrounds

if 'SM' in opt.sigset or 'Backgrounds' in opt.sigset:

    samples['ttbar'] = {    'name'   :   getSampleFiles(directoryBkg,'TTTo2L2Nu',False,'nanoLatino_'),
                            'weight' : XSWeight+'*'+SFweight ,
                            'FilesPerJob' : 2 ,
                        }
    
    samples['tW']    = {    'name'   :   getSampleFiles(directoryBkg,'ST_tW_antitop',False,'nanoLatino_') +
                            getSampleFiles(directoryBkg,'ST_tW_top',    False,'nanoLatino_'),
                            'weight' : XSWeight+'*'+SFweight ,
                            'FilesPerJob' : 2 ,
                        }
    
    samples['ttZ']   = {    'name'   :   getSampleFiles(directoryBkg,'TTZToLLNuNu_M-10_ext2',False,'nanoLatino_') + 
                            getSampleFiles(directoryBkg,'TTZToQQ',              False,'nanoLatino_'),
                            'weight' : XSWeight+'*'+SFweight ,
                            'FilesPerJob' : 2 ,
                        }

    samples['ttW']   = {    'name'   :   getSampleFiles(directoryBkg,'TTWJetsToLNu',False,'nanoLatino_') +
                            getSampleFiles(directoryBkg,'TTWJetsToQQ',False,'nanoLatino_'), 
                            'weight' : XSWeight+'*'+SFweight ,
                            'FilesPerJob' : 2 ,
                        }

    samples['WW']    = {    'name'   :   getSampleFiles(directoryBkg,'WWTo2L2Nu',           False,'nanoLatino_') + 
                            getSampleFiles(directoryBkg,'GluGluWWTo2L2Nu_MCFM',False,'nanoLatino_'),
                            'weight' : XSWeight+'*'+SFweight ,
                            'FilesPerJob' : 2 ,
                        }
    
    samples['WZ']    = {    'name'   :   getSampleFiles(directoryBkg,'WZTo3LNu_ext1',False,'nanoLatino_'),
                            'weight' : XSWeight+'*'+SFweight ,
                            'FilesPerJob' : 2 ,
                        }
    
    samples['ZZ']    = {    'name'   :   getSampleFiles(directoryBkg,'ZZTo2L2Nu_ext1',False,'nanoLatino_') +
                            getSampleFiles(directoryBkg,'ggZZ2e2n',False,'nanoLatino_') +
                            getSampleFiles(directoryBkg,'ggZZ2m2n',False,'nanoLatino_'),
                            'weight' : XSWeight+'*'+SFweight ,
                            'FilesPerJob' : 2 ,
                        }

    samples['DY']    = {    'name'   :   getSampleFiles(directoryBkg,'DYJetsToLL_M-10to50-LO',        False,'nanoLatino_') +
                            getSampleFiles(directoryBkg,'DYJetsToLL_M-5to50_HT-70to100', False,'nanoLatino_') +
                            getSampleFiles(directoryBkg,'DYJetsToLL_M-5to50_HT-100to200',False,'nanoLatino_') +
                            getSampleFiles(directoryBkg,'DYJetsToLL_M-5to50_HT-200to400',False,'nanoLatino_') +
                            getSampleFiles(directoryBkg,'DYJetsToLL_M-5to50_HT-400to600',False,'nanoLatino_') +
                            getSampleFiles(directoryBkg,'DYJetsToLL_M-5to50_HT-600toinf',False,'nanoLatino_') +
                            getSampleFiles(directoryBkg,'DYJetsToLL_M-50-LO_ext1',       False,'nanoLatino_') +
                            getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-70to100',    False,'nanoLatino_') +
                            getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-100to200',   False,'nanoLatino_') +
                            getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-200to400',   False,'nanoLatino_') +
                            getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-400to600',   False,'nanoLatino_') +
                            getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-600to800',   False,'nanoLatino_') +
                            getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-800to1200',  False,'nanoLatino_') +
                            getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-1200to2500', False,'nanoLatino_') +
                            getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-2500toinf',  False,'nanoLatino_') ,
                            'weight' : XSWeight+'*'+SFweight ,
                            'FilesPerJob' : 2 ,
                        }

    samples['HWW']   = {    'name'   :   getSampleFiles(directoryBkg,'GluGluHToWWTo2L2NuAMCNLO_M125',False,'nanoLatino_') + 
                            getSampleFiles(directoryBkg,'GluGluHToTauTau_M125',         False,'nanoLatino_') + 
                            getSampleFiles(directoryBkg,'VBFHToWWTo2L2Nu_M125',         False,'nanoLatino_') + 
                            getSampleFiles(directoryBkg,'HWminusJ_HToWW_M125',          False,'nanoLatino_') + 
                            getSampleFiles(directoryBkg,'HWplusJ_HToWW_M125',           False,'nanoLatino_'),
                            'weight' : XSWeight+'*'+SFweight ,
                            'FilesPerJob' : 2 ,
                        }
    
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

    if 'ControlRegion-ZZ' in opt.tag:
        
        samples['ZZTo4L']   = {    'name'   :   getSampleFiles(directoryBkg,'ZZTo4L',              False,'nanoLatino_') + 
                                   getSampleFiles(directoryBkg,'ggZZ4e',              False,'nanoLatino_') +
                                   getSampleFiles(directoryBkg,'ggZZ4m',              False,'nanoLatino_') +
                                   getSampleFiles(directoryBkg,'ggZZ4t',              False,'nanoLatino_') +
                                   getSampleFiles(directoryBkg,'ggZZ2e2m',            False,'nanoLatino_') +
                                   getSampleFiles(directoryBkg,'ggZZ2e2t',            False,'nanoLatino_') +
                                   getSampleFiles(directoryBkg,'ggZZ2m2t',            False,'nanoLatino_') +
                                   getSampleFiles(directoryBkg,'qqHToZZTo4L_M125',    False,'nanoLatino_') +
                                   getSampleFiles(directoryBkg,'GluGluHToZZTo4L_M125',False,'nanoLatino_'),
                                   'weight' : XSWeight+'*'+SFweight ,
                                   'FilesPerJob' : 2 ,
                               }
        
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
                samples['DATA']['weights'].append(DataTrig[DataSet])

### Signals

#exec(open(opt.signalMassPointsFile).read())
exec(open('./signalMassPoints.py').read())

signalSet = opt.sigset.replace('SM-', '')
signalSet = signalSet.replace('Backgrounds-', '')
signalSet = signalSet.replace('Data-', '')

for model in signalMassPoints:
    if model in signalSet:
        for massPoint in signalMassPoints[model]:
            if signalSet in massPoint:

                samples[massPoint] = { 'name'   : getSampleFiles(directorySig,signalMassPoints[model][massPoint]['massPointDataset'],False,'nanoLatino_'),
                                       'weight' : XSWeight+'*'+SFweight+'*'+signalMassPoints[model][massPoint]['massPointCut'] ,
                                       'FilesPerJob' : 2 ,
                                   }
                
