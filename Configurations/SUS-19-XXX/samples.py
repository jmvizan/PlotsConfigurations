import os
import subprocess
import string
from LatinoAnalysis.Tools.commonTools import *

### Directories
  
SITE=os.uname()[1]

if  'cern' in SITE :
    treeBaseDirMC   = '/eos/cms/store/user/scodella/SUSY/Nano/'
    treeBaseDirData = '/eos/cms/store/caf/user/scodella/BTV/Nano/'

directoryBkg  = treeBaseDirMC   + 'Summer16_102X_nAODv4_Full2016v4/MCl1loose2016__MCCorr2016__susyMT2/'
directorySig  = treeBaseDirMC   + 'Summer16FS_102X_nAODv4_Full2016v4/susyGen__susyW__MCl1loose2016__MCCorr2016FS__susyMT2/'
directoryData = treeBaseDirData + 'Run2016_102X_nAODv4_Full2016v4/DATAl1loose2016__susyMT2data/'

### MC weights

XSWeight      = 'baseW'
SFweight      = 'puWeight'

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

samples['ttbar'] = {    'name'   :   getSampleFiles(directoryBkg,'TTTo2L2Nu',False,'nanoLatino_'),
                        'weight' : XSWeight+'*'+SFweight ,
                        'FilesPerJob' : 2 ,
                        }

### Signals

samples['T2tt'] = {    'name'   :   getSampleFiles(directorySig,'T2tt__mStop-400to1200',False,'nanoLatino_'),
                       'weight' : XSWeight+'*'+SFweight ,
                       'FilesPerJob' : 2 ,
                       }

### Data
       
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

