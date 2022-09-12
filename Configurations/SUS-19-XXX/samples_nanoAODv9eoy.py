import os
import subprocess
import math
import string
from LatinoAnalysis.Tools.commonTools import *

### Generals

# luminosity info from:
# https://twiki.cern.ch/twiki/bin/view/CMS/TWikiLUM#SummaryTable
# https://twiki.cern.ch/twiki/bin/view/CMS/TWikiLUM#LumiComb (minimal correlations 2016-2018)

opt.lumi = 0.
yearstag = { }
if '2016' in opt.tag:
    if 'HIPM' not in opt.tag:
        opt.lumi += 36.33
        yearstag['2016'] = '2016HIPM-2016noHIPM'
    if '2016noHIPM' in opt.tag:
        opt.lumi += 16.81 
        yearstag['2016noHIPM'] = '2016noHIPM'
    if '2016HIPM' in opt.tag:
        opt.lumi += 19.52
        yearstag['2016HIPM'] = '2016HIPM'
    lumi_uncertainty     = '1.012'
    lumi_uncertainty_unc = '1.010'
    lumi_uncertainty_cor = '1.006'
    lumi_uncertainty_dos = '1.000'
    trigger_uncertainty  = '1.020'
if '2017' in opt.tag : 
    opt.lumi += 41.48
    yearstag['2017'] = '2017'
    lumi_uncertainty     = '1.023'
    lumi_uncertainty_unc = '1.020'
    lumi_uncertainty_cor = '1.009'
    lumi_uncertainty_dos = '1.006'
    trigger_uncertainty  = '1.020'
if '2018' in opt.tag : 
    opt.lumi += 59.83
    yearstag['2018'] = '2018'
    lumi_uncertainty     = '1.025'
    lumi_uncertainty_unc = '1.015'
    lumi_uncertainty_cor = '1.020'
    lumi_uncertainty_dos = '1.002'
    trigger_uncertainty  = '1.020'
print 'Value of lumi set to', opt.lumi

recoFlag = '_UL'

yeartag = '-'.join(yearstag.values())

nuis_jer_whole  = False if 'JRW' not in opt.tag else True
nuis_lumi_split = True
nuis_btag_split = True

treePrefix= 'nanoLatino_'

isDatacardOrPlot = hasattr(opt, 'outputDirDatacard') or hasattr(opt, 'postFit') or hasattr(opt, 'skipLNN')

### Directories

skipTreesCheck = False if len(yeartag.split('-'))==1 else True

if not isDatacardOrPlot and skipTreesCheck:
    print 'Error: it is not allowed to fill shapes and skipping trees check!'
    exit()
 
SITE=os.uname()[1]
if 'cern' not in SITE and 'ifca' not in SITE and 'cloud' not in SITE: SITE = 'cern'

if  'cern' in SITE :
    treeBaseDirSig  = '/eos/cms/store/group/phys_susy/Chargino/Nano/'
    treeBaseDirMC   = '/eos/cms/store/group/phys_susy/Chargino/Nano/'
    treeBaseDirData = '/eos/cms/store/group/phys_susy/Chargino/Nano/'
    if not skipTreesCheck:
        print 'nanoAODv9 trees for', yeartag, 'not available yet on cern'
        if not hasattr(opt, 'doHadd') or opt.doHadd:
            skipTreesCheck = True
        else:
            exit()
elif 'ifca' in SITE or 'cloud' in SITE:
    treeBaseDirSig  = '/gpfs/projects/tier3data/LatinosSkims/RunII/Nano/'
    treeBaseDirMC   = '/gpfs/projects/tier3data/LatinosSkims/RunII/Nano/'
    treeBaseDirData = '/gpfs/projects/tier3data/LatinosSkims/RunII/Nano/'

if '2016' in yeartag :
    ProductionMC   = 'Summer20UL16_106X_nAODv9_'+yeartag.replace('2016', '')+'_Full2016v8/MCSusy2016v8__MCSusyCorr2016v8'+yeartag.replace('2016', '')+'__MCSusyNomin2016v8'
    ProductionSig  = 'Summer16FS_102X_nAODv6_Full2016v6loose/hadd__susyGen__susyW__FSSusy2016v6loose__FSSusyCorr2016v6loose__FSSusyNomin2016v6loose'
    ProductionData = 'Run2016_106X_nAODv9_'+yeartag.replace('2016', '')+'_Full2016v8/DATASusy2016v8__hadd'
elif '2017' in yeartag :
    ProductionMC   = 'Summer20UL17_106X_nAODv9_Full2017v8/MCSusy2017v8__MCSusyCorr2017v8__MCSusyNomin2017v8'
    ProductionSig  = 'Fall2017FS_102X_nAODv6_Full2017v6loose/hadd__susyGen__susyW__FSSusy2017v6loose__FSSusyCorr2017v6loose__FSSusyNomin2017v6loose'
    ProductionData = 'Run2017_106X_nAODv9_Full2017v8/DATASusy2017v8__hadd'
elif '2018' in yeartag :
    ProductionMC   = 'Summer20UL18_106X_nAODv9_Full2018v8/MCSusy2018v8__MCSusyCorr2018v8__MCSusyNomin2018v8'
    ProductionSig  = 'Autumn18FS_102X_nAODv6_Full2018v6loose/hadd__susyGen__susyW__FSSusy2018v6loose__FSSusyCorr2018v6loose__FSSusyNomin2018v6loose'
    ProductionData = 'Run2018_106X_nAODv9_Full2018v8/DATASusy2018v8__hadd'

fastsimSignal = False if ('S2tt' in opt.sigset or 'SChipm' in opt.sigset) else True
signalReco = 'fast' if fastsimSignal else 'reco'
if not fastsimSignal:
    ProductionSig = ProductionMC.replace('/MCSusy', '/susyGen__susyW__MCSusy')

metnom, metsmr = 'Smear', 'Nomin'
if 'Nomin' in opt.tag:
    metnom, metsmr = 'Nomin', 'Smear'

regionName = '__susyMT2reco'+metnom+'/'
ctrltag = ''

CRs = ['SameSign', 'Fake', 'WZVal', 'WZtoWW', 'ttZ', 'ZZVal', 'FitCRWZ', 'FitCRZZ', 'Trigger3Lep']
for CR_i in CRs:
    if CR_i in opt.tag:
        regionName = regionName.replace('reco', 'ctrl') 
        ctrltag = '_'+CR_i.replace('FitCR','').replace('Val','').replace('Trigger3Lep','WZ')

directoryBkg  = treeBaseDirMC   + ProductionMC   + regionName
directorySig  = treeBaseDirSig  + ProductionSig  + regionName.replace('reco',  signalReco)
directoryData = treeBaseDirData + ProductionData + regionName.replace('Smear', 'Nomin')

if 'LeptonL2TRate' in opt.tag:
    directoryBkg  = treeBaseDirMC   + ProductionMC.split('/')[0] + '/MCSusyFakeLepton__MCSusyFakeLeptonWeight/'
    directoryData = treeBaseDirData + ProductionData.split('/')[0] + '/DATASusyFakeLepton__selSusyFake__hadd/' 
    pfHTcut = '900' if '2016' in yeartag else '1050'
    leptonL2TRateTriggers = { 'SingleMuon'     : { 'LowPt'          : '(HLT_Mu8_TrkIsoVVL  > 0)' , 
                                                   'HighPt'         : '(HLT_Mu17_TrkIsoVVL > 0)' , 
                                                   'AllPt'          : '((HLT_Mu8_TrkIsoVVL>0 && Lepton_pt[0]<25.) || (HLT_Mu17_TrkIsoVVL>0 && Lepton_pt[0]>=25.))' }, 
                              'SingleElectron' : { 'AllPt'          : '(HLT_Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0)' },
                              'JetHT'          : { 'ElectronJet40'  : '(HLT_PFJet40>0)' ,
                                                   'ElectronJet80'  : '(HLT_PFJet80>0)' ,
                                                   'ElectronJet140' : '(HLT_PFJet140>0)' ,
                                                   'ElectronJet200' : '(HLT_PFJet200>0)' ,
                                                   'ElectronJetXXX' : '(HLT_PFJet40>0 || HLT_PFJet80>0 || HLT_PFJet140>0 || HLT_PFJet200>0)',
                                                   'ElectronDiJet40': '(HLT_DiPFJetAve40>0)' ,
                                                   'ElectronDiJet80': '(HLT_DiPFJetAve80>0)' ,
                                                   'ElectronDiJetXX': '(HLT_DiPFJetAve40>0 || HLT_DiPFJetAve80>0)' ,
                                                   #'ElectronHT180'  : '(HLT_PFHT180)' ,
                                                   'ElectronHT1050' : '(HLT_PFHT'+pfHTcut+'>0)' }
                             }
    if '2017' in yeartag:
        del leptonL2TRateTriggers['JetHT']['ElectronDiJet40']
        del leptonL2TRateTriggers['JetHT']['ElectronDiJet80']
        del leptonL2TRateTriggers['JetHT']['ElectronDiJetXX']

    jethtcutlist = leptonL2TRateTriggers['JetHT'].keys()
    for jethtcut in jethtcutlist:
        leptonL2TRateTriggers['JetHT'][jethtcut.replace('Electron','Muon')] = leptonL2TRateTriggers['JetHT'][jethtcut]
            
    effectiveTriggerLuminosity = { '2016HIPM'   : { 'SingleMuonLowPt'     :     '6.585395243/19521.228351606' ,
                                                    'SingleMuonHighPt'    :   '192.124599592/19521.228351606' ,
                                                    'SingleElectronAllPt' :    '11.033890219/19521.228351606' ,
                                                    'JetHTElectronJet40'  :     '0.154935651/19521.228351606' ,
                                                    'JetHTElectronJet80'  :     '1.960876903/19521.228351606' ,
                                                    'JetHTElectronJet140' :    '16.417493997/19521.228351606' ,
                                                    'JetHTElectronJet200' :    '78.096967167/19521.228351606' ,
                                                    'JetHTElectronDiJet40':     '0.075290206/19521.228351606' ,
                                                    'JetHTElectronDiJet80':     '3.489788545/19521.228351606' ,
                                                    #'JetHTElectronHT180'  :     '/19521.228351606' ,
                                                    'JetHTElectronHT1050' : '19517.523849710/19521.228351606' },
                                   '2016noHIPM' : { 'SingleMuonLowPt'     :     '1.296837118/16812.151722311' ,
                                                    'SingleMuonHighPt'    :    '26.872793405/16812.151722311' ,
                                                    'SingleElectronAllPt' :     '3.980060594/16812.151722311' ,
                                                    'JetHTElectronJet40'  :     '0.112166353/16812.151722311' ,
                                                    'JetHTElectronJet80'  :     '0.798694930/16812.151722311' ,
                                                    'JetHTElectronJet140' :     '7.782596119/16812.151722311' ,
                                                    'JetHTElectronJet200' :    '25.758818194/16812.151722311' ,
                                                    'JetHTElectronDiJet40':     '0.026528823/16812.151722311' ,
                                                    'JetHTElectronDiJet80':     '0.737101065/16812.151722311' ,
                                                    #'JetHTElectronHT180'  :     '/16812.151722311' ,
                                                    'JetHTElectronHT1050' : '16812.151722311/16812.151722311' },
                                   '2017'       : { 'SingleMuonLowPt'     :     '2.899706509/41479.680528762' ,
                                                    'SingleMuonHighPt'    :    '65.898920913/41479.680528762' ,
                                                    'SingleElectronAllPt' :    '27.683553584/41479.680528762' ,
                                                    'JetHTElectronJet40'  :     '0.481958118/41479.680528762' ,
                                                    'JetHTElectronJet80'  :     '4.310850053/41479.680528762' ,
                                                    'JetHTElectronJet140' :    '39.867122288/41479.680528762' ,
                                                    'JetHTElectronJet200' :   '218.831880532/41479.680528762' ,
                                                    'JetHTElectronDiJet40':     '0.257374251/41479.680528762' ,
                                                    'JetHTElectronDiJet80':     '1.969395052/41479.680528762' ,
                                                    #'JetHTElectronHT180'  :     '/41479.680528762' ,
                                                    'JetHTElectronHT1050' : '41477.877399293/41479.680528762' },
                                   '2018'       : { 'SingleMuonLowPt'     :     '8.581579807/59832.475339089' ,
                                                    'SingleMuonHighPt'    :    '45.852032058/59832.475339089' ,
                                                    'SingleElectronAllPt' :    '38.917235487/59832.475339089' ,
                                                    'JetHTElectronJet40'  :     '0.240617828/59832.475339089' ,
                                                    'JetHTElectronJet80'  :     '5.150239903/59832.475339089' ,
                                                    'JetHTElectronJet140' :    '48.566444282/59832.475339089' ,
                                                    'JetHTElectronJet200' :   '209.083270897/59832.475339089' ,
                                                    'JetHTElectronDiJet40':     '0.220756537/59832.475339089' ,
                                                    'JetHTElectronDiJet80':     '5.444414187/59832.475339089' ,
                                                    #'JetHTElectronHT180'  :     '/59832.475339089' ,
                                                    'JetHTElectronHT1050' : '59827.879505586/59832.475339089' },
                                  }
    for yearkey in effectiveTriggerLuminosity:
        effectiveTriggerLuminosity[yearkey]['SingleMuonAllPt'] = '('+effectiveTriggerLuminosity[yearkey]['SingleMuonLowPt']+'*(Lepton_pt[0]<25.)+'+effectiveTriggerLuminosity[yearkey]['SingleMuonHighPt']+'*(Lepton_pt[0]>=25.))'
        effeLumiJetXXX, effeLumiDiJetXX = '(', '('
        for jethttrig in leptonL2TRateTriggers['JetHT'].keys():
            if 'Electron' in jethttrig and 'JetXX' not in jethttrig:
                jethttrigweight = leptonL2TRateTriggers['JetHT'][jethttrig]+'*('+effectiveTriggerLuminosity[yearkey]['JetHT'+jethttrig]+') + '
                if 'ElectronJet' in jethttrig: effeLumiJetXXX += jethttrigweight
                if 'ElectronDiJet' in jethttrig: effeLumiDiJetXX += jethttrigweight
        effeLumiJetXXX += ')'; effeLumiDiJetXX += ')'
        effectiveTriggerLuminosity[yearkey]['JetHTElectronJetXXX'] = effeLumiJetXXX.replace(') + )', ') )')
        effectiveTriggerLuminosity[yearkey]['JetHTElectronDiJetXX'] = effeLumiDiJetXX.replace(') + )', ') )')
        pdtrglist = effectiveTriggerLuminosity[yearkey].keys()
        for pdtrg in pdtrglist:
            if 'JetHTElectron' in pdtrg:
                effectiveTriggerLuminosity[yearkey][pdtrg.replace('Electron', 'Muon')]  = effectiveTriggerLuminosity[yearkey][pdtrg]

directoryBkgEOY = directoryBkg.replace('Summer20UL16_106X_nAODv9_HIPM', 'Summer16_102X_nAODv6').replace('Summer20UL16_106X_nAODv9_noHIPM', 'Summer16_102X_nAODv6').replace('Summer20UL17_106X_nAODv9', 'Fall2017_102X_nAODv6').replace('Summer20UL18_106X_nAODv9', 'Autumn18_102X_nAODv6').replace('v8', 'v6loose').replace('noHIPM','').replace('HIPM','') 
if 'cern' in SITE:
    if '2016' in yeartag:
        directoryBkgEOY = directoryBkgEOY.replace('/eos/cms/store/group/phys_susy/Chargino/Nano/', '/eos/cms/store/user/scodella/SUSY/Nano/')
    elif 'EOY' in opt.sigset: 
        print 'Set directoryBkgEOY for', yeartag, 'year'
        exit()

# nuisance parameters

removeZeros = 1 if 'StatZero' in opt.tag else 0
#removeZeros = 0 if 'NoStat0' in opt.tag else 1

treeNuisances = { }
if metnom=='Nomin':
    treeNuisances['smear']        = { 'name' : metsmr,                 'onesided' : True  }
    #treeNuisances['jesTotal']  = { 'name' : 'JES',  'jetname' : 'JES', 'onesided' : False }
    #treeNuisances['unclustEn'] = { 'name' : 'MET',                     'onesided' : False }
elif metnom=='Smear':
    if not isDatacardOrPlot or not nuis_jer_whole:
        treeNuisances['jer']      = { 'name' : 'JER',  'jetname' : 'JER', 'onesided' : False }
    if not isDatacardOrPlot or nuis_jer_whole:
        treeNuisances['nosmear']  = { 'name' : metsmr,                    'onesided' : True  }
    treeNuisances['jesTotal']  = { 'name' : 'SJS',  'jetname' : 'JES', 'onesided' : False }
    treeNuisances['unclustEn'] = { 'name' : 'SMT',                     'onesided' : False }

for treeNuisance in treeNuisances:
    treeNuisances[treeNuisance]['year']     = False # ???
    treeNuisances[treeNuisance]['BkgToSig'] = True if not fastsimSignal else True # ???

treeNuisanceDirs = { }
treeNuisanceSuffix = '__hadd' if ('cern' in SITE and 'EOY' in opt.sigset) else ''
for treeNuisance in treeNuisances:
    treeNuisanceDirs[treeNuisance] = { 'Bkg' : { }, 'Sig' : { }, }
    if treeNuisance=='nosmear' or treeNuisance=='smaer':
        treeNuisanceDirs[treeNuisance]['Bkg']['Up']   = directoryBkg.replace(metnom+'/', metsmr+'/') 
        treeNuisanceDirs[treeNuisance]['Bkg']['Down'] = directoryBkg
        treeNuisanceDirs[treeNuisance]['Sig']['Up']   = directorySig.replace(metnom+'/', metsmr+'/') 
        treeNuisanceDirs[treeNuisance]['Sig']['Down'] = directorySig
    else:
        directoryBkgTemp = directoryBkg.replace(metnom+'/', treeNuisances[treeNuisance]['name']+'variation'+treeNuisanceSuffix+'/') 
        directorySigTemp = directorySig.replace(metnom+'/', treeNuisances[treeNuisance]['name']+'variation'+treeNuisanceSuffix+'/') 
        if 'jetname' in treeNuisances[treeNuisance]:
            directoryBkgTemp = directoryBkgTemp.replace('SusyNomin', 'Susy'+treeNuisances[treeNuisance]['jetname']+'variation')
            directorySigTemp = directorySigTemp.replace('SusyNomin', 'Susy'+treeNuisances[treeNuisance]['jetname']+'variation') 
        for variation in [ 'Down', 'Up' ]:
            treeNuisanceDirs[treeNuisance]['Bkg'][variation]  = directoryBkgTemp.replace('variation', variation[:2])
            treeNuisanceDirs[treeNuisance]['Sig'][variation]  = directorySigTemp.replace('variation', variation[:2])
    if 'EOY' in opt.sigset:
        treeNuisanceDirs[treeNuisance]['Bkg']['Up']   = treeNuisanceDirs[treeNuisance]['Bkg']['Up'].replace('Summer20UL16_106X_nAODv9_', 'Summer16_102X_nAODv6').replace('noHIPM', '').replace('HIPM','').replace('Summer20UL17_106X_nAODv9', 'Fall2017_102X_nAODv6').replace('Summer20UL18_106X_nAODv9', 'Autumn18_102X_nAODv6').replace('v8', 'v6loose')
        treeNuisanceDirs[treeNuisance]['Bkg']['Down'] = treeNuisanceDirs[treeNuisance]['Bkg']['Down'].replace('Summer20UL16_106X_nAODv9_', 'Summer16_102X_nAODv6').replace('noHIPM', '').replace('HIPM','').replace('Summer20UL17_106X_nAODv9', 'Fall2017_102X_nAODv6').replace('Summer20UL18_106X_nAODv9', 'Autumn18_102X_nAODv6').replace('v8', 'v6loose')
        if 'cern' in SITE:
            treeNuisanceDirs[treeNuisance]['Bkg']['Up']   = treeNuisanceDirs[treeNuisance]['Bkg']['Up'].replace('/eos/cms/store/group/phys_susy/Chargino/Nano/', '/eos/cms/store/user/scodella/SUSY/Nano/')
            treeNuisanceDirs[treeNuisance]['Bkg']['Down'] = treeNuisanceDirs[treeNuisance]['Bkg']['Down'].replace('/eos/cms/store/group/phys_susy/Chargino/Nano/', '/eos/cms/store/user/scodella/SUSY/Nano/')

globalNuisances = { }
globalNuisances['trigger'] = { 'name' : 'trigger_yeartag', 'value' : trigger_uncertainty }
if nuis_lumi_split:
    globalNuisances['lumi_unc'] = { 'name' : 'lumi_yeartag', 'value' : lumi_uncertainty_unc }
    globalNuisances['lumi_cor'] = { 'name' : 'lumi'         , 'value' : lumi_uncertainty_cor }
    if '2016' not in yeartag:
        globalNuisances['lumi_dos'] = { 'name' : 'lumi_1718', 'value' : lumi_uncertainty_dos }
else:
    globalNuisances['lumi']     = { 'name' : 'lumi_yeartag', 'value' : lumi_uncertainty }

bTagNuisances = {
    'mistag'   : { 'name' : 'mistag_yeartag',   'var' : 'l_VAR' },
    'btagFS'   : { 'name' : 'btagFS_yeartag',   'var' : 'b_VAR_fastsim' },
    'ctagFS'   : { 'name' : 'ctagFS_yeartag',   'var' : 'c_VAR_fastsim' },
    'mistagFS' : { 'name' : 'mistagFS_yeartag', 'var' : 'l_VAR_fastsim' },
}
if nuis_btag_split and 'EOY' not in opt.sigset:
    bTagNuisances['btagunc'] = { 'name' : 'btag_yeartag',     'var' : 'b_VAR_uncorrelated' }
    bTagNuisances['btagcor'] = { 'name' : 'btag',              'var' : 'b_VAR_correlated' }
else:
    bTagNuisances['btag']    = { 'name' : 'btag_yeartag',     'var' : 'b_VAR' }

# Complex cut variables

ElectronWP = 'Lepton_isTightElectron_cutBasedMediumPOG'
if 'EleTightPOG' in opt.tag:
    ElectronWP = 'Lepton_isTightElectron_cutBasedTightPOG'
MuonWP     = 'Lepton_isTightMuon_mediumRelIsoTight'

if 'TriggerLatino' in opt.tag:
    if '2016' in yeartag:
        ElectronWP = 'Lepton_isTightElectron_cut_WP_Tight80X' #'Lepton_isTightElectron_mva_90p_Iso2016'
        MuonWP     = 'Lepton_isTightMuon_cut_Tight80x'
    elif '2017' in yeartag or '2018' in yeartag:
        ElectronWP = 'Lepton_isTightElectron_cutFall17V2Iso_Tight' #'Lepton_isTightElectron_mvaFall17V2Iso_WP90'
        MuonWP     = 'Lepton_isTightMuon_cut_Tight_HWWW'
ElectronSF = ElectronWP.replace('isTightElectron', 'tightElectron')
MuonSF     = MuonWP.replace('isTightMuon', 'tightMuon')

lep0idx = '0'
lep1idx = '1'
lep2idx = '2'

nLooseLepton = 'nLepton'
nTightLepton = 'Sum$(('+ElectronWP+'+'+MuonWP+')==1)'
#nTightPromptLepton = 'Sum$((('+ElectronWP+'+'+MuonWP+')*Lepton_promptgenmatched)==1)'
nTightPromptLepton = '(('+ElectronWP+'[0]+'+MuonWP+'[0])*Lepton_promptgenmatched[0]+('+ElectronWP+'[1]+'+MuonWP+'[1])*Lepton_promptgenmatched[1])'
nTightIDLepton = '(Lepton_isTightElectron_cutBasedTightPOG[0]+(abs(Lepton_pdgId[0])==13)*Alt$(Muon_tightId[abs(Lepton_muonIdx[0])],0)+Lepton_isTightElectron_cutBasedTightPOG[1]+(abs(Lepton_pdgId[1])==13)*Alt$(Muon_tightId[abs(Lepton_muonIdx[1])],0))'

pxll   = '(Lepton_pt['+lep0idx+']*cos(Lepton_phi['+lep0idx+'])+Lepton_pt['+lep1idx+']*cos(Lepton_phi['+lep1idx+']))'
pyll   = '(Lepton_pt['+lep0idx+']*sin(Lepton_phi['+lep0idx+'])+Lepton_pt['+lep1idx+']*sin(Lepton_phi['+lep1idx+']))'
pTll   = 'sqrt('+pxll+'*'+pxll+'+'+pyll+'*'+pyll+')'
phill  = 'atan('+pyll+'/'+pxll+')'
dPhill = 'acos(cos(Lepton_phi['+lep1idx+']-Lepton_phi['+lep0idx+']))'
dEtall = 'Lepton_eta['+lep1idx+']-Lepton_eta['+lep0idx+']'
dRll   = 'sqrt('+dPhill+'*'+dPhill+'+'+dEtall+'*'+dEtall+')'
ptmiss_phi = 'ptmiss_phi'+ctrltag
if 'MET' in opt.tag:
    ptmiss_phi = 'MET_phi' 
mTllptmiss       = 'sqrt(2*'+pTll+'*ptmiss*(1.-cos('+phill+'-'+ptmiss_phi+')))'
dPhillptmiss     = 'acos(cos('+phill+'-'+ptmiss_phi+'))'
dPhilep0ptmiss   = 'acos(cos(Lepton_phi['+lep0idx+']-'+ptmiss_phi+'))'
dPhilep1ptmiss   = 'acos(cos(Lepton_phi['+lep1idx+']-'+ptmiss_phi+'))'
dPhiMinlepptmiss = 'TMath::Min('+dPhilep0ptmiss+','+dPhilep1ptmiss+')'
dPhijet0ptmiss   = 'acos(cos(CleanJet_phi[0]-'+ptmiss_phi+'))'
dPhijet1ptmiss   = 'acos(cos(CleanJet_phi[1]-'+ptmiss_phi+'))'
jetrawpteenoise  = '(Jet_pt*(1.-Jet_rawFactor)*(2*(abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139)-1))'
njeteenoise      = 'Sum$(abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139)'
njeteenoise30    = 'Sum$(abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139 && Jet_pt*(1.-Jet_rawFactor)<30.)'
jetpteenoise     = '(Jet_pt*(2*(Jet_pt*(1.-Jet_rawFactor)<50. && abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139)-1))'
dPhieenoiseptmiss_pt30 = 'acos(cos(Jet_phi-'+ptmiss_phi+'))*(2.*((Jet_pt*(1.-Jet_rawFactor)<50. && Jet_pt>30. && abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139)==1)-1.)'
dPhieenoiseptmiss_pt50 = 'acos(cos(Jet_phi-'+ptmiss_phi+'))*(2.*((Jet_pt*(1.-Jet_rawFactor)<50. && Jet_pt>50. && abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139)==1)-1.)'
dPhieenoiseptmiss_pt15 = 'acos(cos(Jet_phi-'+ptmiss_phi+'))*(2.*((Jet_pt*(1.-Jet_rawFactor)<50. && Jet_pt>15. && abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139)==1)-1.)'
dPhieenoiseptmiss_hard = 'acos(cos(Jet_phi-'+ptmiss_phi+'))*(2.*((Jet_pt*(1.-Jet_rawFactor)>50. && Jet_pt>30. && abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139)==1)-1.)'
dPhieenoiseptmiss_pt30_norawcut = 'acos(cos(Jet_phi-'+ptmiss_phi+'))*(2.*((Jet_pt>30. && abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139)==1)-1.)'
dPhieenoiseptmiss_pt15_norawcut = 'acos(cos(Jet_phi-'+ptmiss_phi+'))*(2.*((Jet_pt>15. && abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139)==1)-1.)'
HTForward     = 'Sum$(Jet_pt*(abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139))'
HTForwardSoft = 'Sum$(Jet_pt*(abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139 && Jet_pt*(1.-Jet_rawFactor)<50.))'
HTRawForward  = 'Sum$(Jet_pt*(1.-Jet_rawFactor)*(abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139))'
HTRawForwardSoft = 'Sum$(Jet_pt*(1.-Jet_rawFactor)*(abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139 && Jet_pt*(1.-Jet_rawFactor)<50.))'
jetpteenoisedphi = '(Jet_pt*(2*(Jet_pt*(1.-Jet_rawFactor)<50. && abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139 && acos(cos(Jet_phi-'+ptmiss_phi+'))<0.96)-1))'

ptmissNano = 'MET_pt'
if 'Data' not in opt.sigset: # data do not have pt_nom, but it's equal to pt as the JEC in central production were the final ones
    if   metnom =='Nomin': ptmissNano = 'MET_T1_pt'
    elif metnom =='Smear': ptmissNano = 'MET_T1Smear_pt'
if 'EOY' in opt.sigset:
    ptmissNano = 'METFixEE2017_pt' if '2017' in yeartag else 'MET_pt'
    if metnom=='Nomin': ptmissNano += '_nom'
    elif metnom=='Smear': ptmissNano += '_jer'
ptmissPhiNano = ptmissNano.replace('_pt', '_phi')

ptxLep = 'Lepton_pt[abs(lepidx_WZtoWW)]*cos(Lepton_phi[abs(lepidx_WZtoWW)])'
ptyLep = 'Lepton_pt[abs(lepidx_WZtoWW)]*sin(Lepton_phi[abs(lepidx_WZtoWW)])'
chrLep = '((Lepton_pdgId[abs(lepidx_WZtoWW)]*Lepton_pdgId[abs(lep2idx_WZtoWW)])<0)'
metx_ttZ3Lep = '(ptmiss_WZtoWW*cos(ptmiss_phi_WZtoWW)+'+ptxLep.replace('lepidx', 'lep0idx')+'*'+chrLep.replace('lepidx', 'lep0idx')+'+'+ptxLep.replace('lepidx', 'lep1idx')+'*'+chrLep.replace('lepidx', 'lep1idx')+')' 
mety_ttZ3Lep = '(ptmiss_WZtoWW*sin(ptmiss_phi_WZtoWW)+'+ptyLep.replace('lepidx', 'lep0idx')+'*'+chrLep.replace('lepidx', 'lep0idx')+'+'+ptyLep.replace('lepidx', 'lep1idx')+'*'+chrLep.replace('lepidx', 'lep1idx')+')'
ptmiss_ttZ3Lep      = 'sqrt('+metx_ttZ3Lep+'*'+metx_ttZ3Lep+'+'+mety_ttZ3Lep+'*'+mety_ttZ3Lep+')'
ptmiss_phi_ttZ3Lep  = 'atan2('+mety_ttZ3Lep+', '+metx_ttZ3Lep+')' 
ptmiss_ttZLoose     = '('+ptmiss_ttZ3Lep+'*(ptmiss_WZtoWW>=0.) + ptmiss_ttZ*(ptmiss_ttZ>=0.))'
ptmiss_phi_ttZLoose = '('+ptmiss_phi_ttZ3Lep+'*(ptmiss_WZtoWW>=0.) + ptmiss_phi_ttZ*(ptmiss_ttZ>=0.))'
 
OC  = nTightLepton + '==2 && mll'+ctrltag+'>=20. && Lepton_pt[0]>=25. && Lepton_pt[1]>=20. && (Lepton_pdgId[0]*Lepton_pdgId[1])<0'
SS  = nTightLepton + '==2 && mll'+ctrltag+'>=20. && Lepton_pt[0]>=25. && Lepton_pt[1]>=20. && (Lepton_pdgId[0]*Lepton_pdgId[1])>0'
SSP = nTightLepton + '==2 && mll'+ctrltag+'>=20. && Lepton_pt[0]>=25. && Lepton_pt[1]>=20. && Lepton_pdgId[0]<0 && Lepton_pdgId[1]<0'
SSM = nTightLepton + '==2 && mll'+ctrltag+'>=20. && Lepton_pt[0]>=25. && Lepton_pt[1]>=20. && Lepton_pdgId[0]>0 && Lepton_pdgId[1]>0'

if 'SameSign' in opt.tag: OC = SS
if 'AppWJets' in opt.tag or 'WJetsCorr' in opt.sigset: OC = OC.replace('==2 && mll', '==1 && mll')
if 'TightLep' in opt.tag: OC = OC.replace('==2 && mll', '==2 && '+nTightIDLepton+'==2 && mll')
if 'TightLep' in opt.tag: OC = OC.replace('==1 && mll', '==1 && '+nTightIDLepton+'==1 && mll')

LL = 'fabs(Lepton_pdgId[0])==fabs(Lepton_pdgId[1])'
DF = 'fabs(Lepton_pdgId[0])!=fabs(Lepton_pdgId[1])'
EE = 'fabs(Lepton_pdgId[0])==11 && fabs(Lepton_pdgId[1])==11'
MM = 'fabs(Lepton_pdgId[0])==13 && fabs(Lepton_pdgId[1])==13'

T0 = '('+ElectronWP+'[0]+'+MuonWP+'[0])'
T1 = '('+ElectronWP+'[1]+'+MuonWP+'[1])'
T2 = '('+ElectronWP+'[2]+'+MuonWP+'[2])'

LepId2of3 = nLooseLepton+'==3 && ('+T0+'+'+T1+'+'+T2+')==2'

C2  = '(Lepton_pdgId[0]*Lepton_pdgId[1])'
C1  = '(Lepton_pdgId[0]*Lepton_pdgId[2])'
C0  = '(Lepton_pdgId[1]*Lepton_pdgId[2])'
OCT = '('+C2+'*'+T0+'*'+T1+'+'+C1+'*'+T0+'*'+T2+'+'+C0+'*'+T1+'*'+T2+')<0'

MET_significance = 'MET_significance'

btagAlgo   = 'deepcsv'
btagDisc   = 'btagDeepB'
bTagWP     = '_M'
if 'EOY' in opt.sigset and 'EOYWJets' not in opt.sigset:
    btagAlgo   = 'btagDeepB'
    bTagWP     = 'M'
bTagPtCut  = '20.'
if 'ptb25' in opt.tag: bTagPtCut  = '25.' 
if 'ptb30' in opt.tag: bTagPtCut  = '30.' 
jetPtCut = '20.'
if 'pt25' in opt.tag: jetPtCut = '25.'
if 'pt30' in opt.tag: jetPtCut = '30.'
bTagEtaMax = '2.4' if ('2016' in opt.tag) else '2.5'
if '2016HIPM' in yeartag: 
    bTagCut = '0.6001' 
    btagWP  = '2016'
elif '2016noHIPM' in yeartag:
    bTagCut = '0.5847' 
    btagWP  = '2016'
elif '2017' in yeartag: 
    bTagCut = '0.4506'
    btagWP  = '2017'
elif '2018' in yeartag: 
    bTagCut = '0.4168'
    btagWP  = '2018'
btagWP += bTagWP

#bTagPass = '(leadingPtTagged_'+btagAlgo+bTagWP+'_1c>='+bTagPtCut+')'
bTagPass  = '(Sum$(CleanJet_pt>='+bTagPtCut+' && abs(CleanJet_eta)<'+bTagEtaMax+' && Jet_'+btagDisc+'[CleanJet_jetIdx]>='+bTagCut+')>=1)' 
bTagVeto  = '!'+bTagPass
#b2TagPass = bTagPass.replace('leadingPt', 'trailingPt')
b2TagPass = '(Sum$(CleanJet_pt>='+bTagPtCut+' && abs(CleanJet_eta)<'+bTagEtaMax+' && Jet_'+btagDisc+'[CleanJet_jetIdx]>='+bTagCut+')>=2)'

btagWeight1tag = 'btagWeight_1tag_'+btagAlgo+bTagWP+'_1c'
if 'pt25' in opt.tag: btagWeight1tag += '_Pt25'
if 'pt30' in opt.tag: btagWeight1tag += '_Pt30'
btagWeight0tag = '(1.-'+btagWeight1tag+')'
if 'TrigBTag' in opt.tag:
    if 'HighPtMissControlRegion' not in opt.tag and 'HighPtMissValidationRegion' not in opt.tag:
        print 'TrigBTag option only implemented for HighPtMissControlRegion and HighPtMissValidationRegion tags' 
        exit()
    btagWeightNoCut = 'triggerWeight'
    btagWeight1tag += '*triggerWeightBTag'
    btagWeight0tag += '*triggerWeightVeto'
else:
    btagWeightNoCut = '1.'
btagWeight2tag = btagWeight1tag.replace('_1tag_', '_2tag_')

ISRCut     = 'CleanJet_pt[0]>150. && CleanJet_pt[0]!=leadingPtTagged_'+btagAlgo+bTagWP+'_1c && acos(cos(ptmiss_phi-CleanJet_phi[0]))>2.5'
ISRCutData = ' '+ISRCut+' && '
ISRCutMC   = '&& '+ISRCut

### MET Filters 

# https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2#UL_data (checked on may20)
METFilters_Common = 'Flag_goodVertices*Flag_globalSuperTightHalo2016Filter*Flag_HBHENoiseFilter*Flag_HBHENoiseIsoFilter*Flag_EcalDeadCellTriggerPrimitiveFilter*Flag_BadPFMuonFilter*Flag_BadPFMuonDzFilter'

if '2017' in opt.tag or '2018' in opt.tag :
    METFilters_Common += '*Flag_ecalBadCalibFilter'
    if 'noisyhits' in opt.tag: METFilters_Common += '*Flag_hfNoisyHitsFilter'
METFilters_MC   = METFilters_Common
METFilters_Data = METFilters_Common + '*Flag_eeBadScFilter'
METFilters_FS   = METFilters_Common

if 'EOY' in opt.sigset:
    METFilters_Common = 'Flag_goodVertices*Flag_HBHENoiseFilter*Flag_HBHENoiseIsoFilter*Flag_EcalDeadCellTriggerPrimitiveFilter*Flag_BadPFMuonFilter'
    if '2017' in opt.tag or '2018' in opt.tag :
        METFilters_Common += '*Flag_ecalBadCalibFilterV2'
    METFilters_MC   = METFilters_Common + '*Flag_globalSuperTightHalo2016Filter'
    METFilters_Data = METFilters_Common + '*Flag_globalSuperTightHalo2016Filter*Flag_eeBadScFilter'
    METFilters_FS   = METFilters_Common

### EE Noise in 2017 and HEM Issue in 2018

DataQualityCuts = ''
if 'VetoesUL' in opt.tag: DataQualityCuts = 'EENoiseHTHEM'
elif 'VetoesEOY' in opt.tag: DataQualityCuts = 'EENoiseDPhiHEM'
else:
    if 'EENoise30' in opt.tag: DataQualityCuts += 'EENoise30'
    elif 'EENoiseHT' in opt.tag: DataQualityCuts += 'EENoiseHT'
    elif 'EENoiseDPhiHard' in opt.tag: DataQualityCuts += 'EENoiseDPhiHard'
    elif 'EENoiseDPhiSoftPt50' in opt.tag: DataQualityCuts += 'EENoiseDPhiSoftPt50'
    elif 'EENoiseDPhiSoft' in opt.tag: DataQualityCuts += 'EENoiseDPhiSoft'
    elif 'EENoiseDPhi' in opt.tag: DataQualityCuts += 'EENoiseDPhi'
    if 'HEM20' in opt.tag: DataQualityCuts += 'HEM20'
    elif 'HEM' in opt.tag: DataQualityCuts += 'HEM'

VetoEENoise, VetoHEMdata, VetoHEMmc  = '1.', '1.', '1.'
if '2017' in yeartag and 'EENoise' in DataQualityCuts:
    VetoEENoise = '(Sum$(Jet_pt*(1.-Jet_rawFactor)<50. && Jet_pt>30. && abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139)==0)'
    if 'EENoise30' in DataQualityCuts:
        VetoEENoise = '(Sum$(Jet_pt*(1.-Jet_rawFactor)<30. && Jet_pt>30. && abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139)==0)'
        #VetoEENoise = '('+njeteenoise30+'==0)'
    elif 'EENoiseHT' in DataQualityCuts:
        VetoEENoise = '('+HTForwardSoft+'<60.)'
    elif 'EENoiseDPhiHard' in DataQualityCuts:
        if 'UL' in recoFlag:
            VetoEENoise = '(Sum$('+dPhieenoiseptmiss_hard+'>2.560)==0)'
        else:
            VetoEENoise = '(Sum$('+dPhieenoiseptmiss_hard+'>1.257)==0)'
    elif 'EENoiseDPhiSoftPt50' in DataQualityCuts:
        VetoEENoise = '(Sum$('+dPhieenoiseptmiss_pt50+'>0. && '+dPhieenoiseptmiss_pt50+'<0.96)==0)'
    elif 'EENoiseDPhiSoft' in DataQualityCuts:
        VetoEENoise = '(Sum$('+dPhieenoiseptmiss_pt30+'>0. && '+dPhieenoiseptmiss_pt30+'<0.96)==0)'
    elif 'EENoiseDPhi' in DataQualityCuts:
        VetoEENoise = '(Sum$('+dPhieenoiseptmiss_hard+'>1.257)==0 && Sum$('+dPhieenoiseptmiss_pt50+'>0. && '+dPhieenoiseptmiss_pt50+'<0.96)==0)'
    #if 'Veto' in DataQualityCuts:
    #    #VetoEENoise = '(1. - '+VetoEENoise+')'
    #    VetoEENoise = '(Sum$(Jet_pt*(1.-Jet_rawFactor)<50. && Jet_pt>30. && abs(Jet_eta)>2.650 && abs(Jet_eta)<3.139)>=1)'

elif '2018' in yeartag and 'HEM' in DataQualityCuts:
    hemPtCut    = '20.' if 'HEM20' in DataQualityCuts else '30.' 
    VetoHEMele  = '(Sum$(Electron_pt>'+hemPtCut+' && Electron_eta>-3.0 && Electron_eta<-1.4 && Electron_phi>-1.57 && Electron_phi<-0.87)==0)'
    VetoHEMjet  = '(Sum$(Jet_pt>'+hemPtCut+' && Jet_eta>-3.2 && Jet_eta<-1.2 && Jet_phi>-1.77 && Jet_phi<-0.67)==0)'
    VetoHEM     = '('+VetoHEMele+' && '+VetoHEMjet+')'
    VetoHEMdata = '(run<319077 || '+VetoHEM+')'
    VetoHEMmc   = '('+VetoHEM+' + (1.-'+VetoHEM+')*0.35225285)'

### Trigger Efficiencies

TriggerEff = 'TriggerEffWeight_2l' if ('Trigger' not in opt.tag and 'LeptonL2TRate' not in opt.tag) else '1.'

if 'WZtoWW' in opt.tag or 'WZVal' in opt.tag or 'ZZVal' in opt.tag or 'ttZ' in opt.tag or 'FitCRZZ' in opt.tag or 'FitCRWZ' in opt.tag:
    TriggerEff = 'TriggerEffWeight_3l' if 'TrigLatino' in opt.tag else '1.'

### MC weights

# generation weights

XSWeight       = 'baseW*genWeight'

# lepton weights

allweights  = ['Extra', 'IdIso','Reco', 'Tot', 'FastSim']
LepWeight = { 
    'Ele' : {'base' : [ElectronSF]},
    'Muo' : {'base' : [MuonSF]},
    'Lep' : {'base' : [ElectronSF, MuonSF]}
}
for lep_i in LepWeight:
    for weight_i in allweights:
        if weight_i == 'Reco' :
            if 'EOY' in opt.sigset and '2016' in yeartag: 
                LepRecoSF  = '((abs(Lepton_pdgId[LEPIDX])==13)+(Lepton_RecoSF[LEPIDX]*(abs(Lepton_pdgId[LEPIDX])==11)))'
                LepWeight[lep_i][weight_i] = LepRecoSF.replace('LEPIDX', '0') + '*' + LepRecoSF.replace('LEPIDX', '1')
            else: 
                LepWeight[lep_i][weight_i] = 'Lepton_' + weight_i + 'SF[0]*Lepton_' + weight_i + 'SF[1]'
        else:
            LepWeight[lep_i][weight_i] = LepWeight[lep_i]['base'][0] + '_' + weight_i + 'SF[0]*'+LepWeight[lep_i]['base'][0] + '_' + weight_i + 'SF[1]'
            if lep_i == 'Lep': LepWeight[lep_i][weight_i] += '*'+LepWeight[lep_i]['base'][1] + '_' + weight_i + 'SF[0]*'+LepWeight[lep_i]['base'][1] + '_' + weight_i + 'SF[1]'
        
leptonSF = {}
allweights.remove('Tot')
if 'EOY' in opt.sigset: allweights.remove('Extra')
for lep_i in ['Lep']:
    for weight_i in allweights:
        lepW_i = LepWeight[lep_i][weight_i]
        if weight_i == 'FastSim': leptonSF["leptonIdIsoFS"] = { 'type' : 'lnN', 'weight' : '1.04' }
        else: leptonSF[lep_i.lower()+weight_i] = {'type' : 'shape', 'weight' : [lepW_i.replace('SF[', 'SF_Up[')+'/('+lepW_i+')', lepW_i.replace('SF[', 'SF_Down[')+'/('+lepW_i+')']}

# nonprompt lepton rate TODO?:

if   '2016HIPM'   in yeartag: nonpromptLep = { 'rate' : '1.07', 'rateUp' : '1.16', 'rateDown' : '0.97' } 
elif '2016noHIPM' in yeartag: nonpromptLep = { 'rate' : '1.09', 'rateUp' : '1.30', 'rateDown' : '0.91' } 
elif '2017'       in yeartag: nonpromptLep = { 'rate' : '1.38', 'rateUp' : '1.46', 'rateDown' : '1.29' } 
elif '2018'       in yeartag: nonpromptLep = { 'rate' : '1.28', 'rateUp' : '1.37', 'rateDown' : '1.21' } 
if 'nonpromptSF' in opt.tag: # To check that mismodelling doesnt change much the limits (EOY values)
    if   '2016' in yeartag: nonpromptLep = { 'rate' : '1.00', 'rateUp' : '1.23', 'rateDown' : '0.77' } 
    elif '2017' in yeartag: nonpromptLep = { 'rate' : '1.00', 'rateUp' : '1.48', 'rateDown' : '0.52' } 
    elif '2018' in yeartag: nonpromptLep = { 'rate' : '1.00', 'rateUp' : '1.30', 'rateDown' : '0.70' } 

if 'SameSign' in opt.tag or 'AppWJets' in opt.tag or 'LeptonL2TRate' in opt.tag:
    nonpromptLepSF      = '1.'
    nonpromptLepSF_Up   = '1.'
    nonpromptLepSF_Down = '1.'
else:
    promptLeptons = 'Lepton_promptgenmatched[0]*Lepton_promptgenmatched[1]'
    nonpromptLepSF      = '( ' + promptLeptons + ' + (1. - ' + promptLeptons + ')*' + nonpromptLep['rate']      + ')'
    nonpromptLepSF_Up   = '( ' + promptLeptons + ' + (1. - ' + promptLeptons + ')*' + nonpromptLep['rateUp']    + ')'
    nonpromptLepSF_Down = '( ' + promptLeptons + ' + (1. - ' + promptLeptons + ')*' + nonpromptLep['rateDown']  + ')'

# global SF weights 
if 'EOY' in opt.sigset or 'TestExtra' in opt.tag:
    SFweightCommon = 'puWeight*' + TriggerEff + '*' + LepWeight['Lep']['Reco'] + '*' + LepWeight['Lep']['IdIso'] + '*' + nonpromptLepSF
else:
    SFweightCommon = 'puWeight*' + TriggerEff + '*' + LepWeight['Lep']['Tot'] + '*' + nonpromptLepSF

if '2016' in yeartag or '2017' in yeartag: 
    SFweightCommon += '*PrefireWeight'
if '2017' in yeartag and 'EENoise' in DataQualityCuts:
    SFweightCommon += '*' + VetoEENoise
if '2018' in yeartag and 'HEM' in DataQualityCuts: 
    SFweightCommon += '*' + VetoHEMmc
SFweight       = SFweightCommon + '*' + METFilters_MC
SFweightFS     = SFweightCommon + '*' + METFilters_FS + '*' + LepWeight['Lep']['FastSim'] + '*isrW'
    
### Special weights

# background cross section uncertainties and normalization scale factors

normBackgrounds = {}

if 'WWSF' in opt.tag and "PseudoData" not in opt.tag:
    if '2016HIPM' in opt.tag:
        normBackgrounds['WW']      = { 'nojet'   : { 'scalefactor' : { '1.142' : '0.191' }, 'cuts' : [ '_NoJet', '_Veto' ], 'selection' : '(nCleanJet==0)' } }
    elif '2016noHIPM' in opt.tag:
        normBackgrounds['WW']      = { 'nojet'   : { 'scalefactor' : { '1.416' : '0.189' }, 'cuts' : [ '_NoJet', '_Veto' ], 'selection' : '(nCleanJet==0)' } }
    elif '2017' in opt.tag:
        normBackgrounds['WW']      = { 'nojet'   : { 'scalefactor' : { '1.333' : '0.140' }, 'cuts' : [ '_NoJet', '_Veto' ], 'selection' : '(nCleanJet==0)' } }
    elif '2018' in opt.tag:
        normBackgrounds['WW']      = { 'nojet'   : { 'scalefactor' : { '1.395' : '0.167' }, 'cuts' : [ '_NoJet', '_Veto' ], 'selection' : '(nCleanJet==0)' } }

if 'WJetsCorr' in opt.sigset:

    if '2016HIPM' in opt.tag:
        normBackgrounds['WJetsCorr']      = { 'nojet'   : { 'scalefactor' : { '1.00' : '0.' }, 'cuts' : [ '_NoJet', '_Veto' ], 'selection' : '(nCleanJet==0)' }, 
                                              'notag'   : { 'scalefactor' : { '1.14' : '0.' }, 'cuts' : [ '_NoTag', '_Veto' ], 'selection' : '(nCleanJet>=1)' } }
    elif '2016noHIPM' in opt.tag:
        normBackgrounds['WJetsCorr']      = { 'nojet'   : { 'scalefactor' : { '1.00' : '0.' }, 'cuts' : [ '_NoJet', '_Veto' ], 'selection' : '(nCleanJet==0)' },
                                              'notag'   : { 'scalefactor' : { '1.14' : '0.' }, 'cuts' : [ '_NoTag', '_Veto' ], 'selection' : '(nCleanJet>=1)' } }
    elif '2017' in opt.tag:
        normBackgrounds['WJetsCorr']      = { 'nojet'   : { 'scalefactor' : { '1.17' : '0.' }, 'cuts' : [ '_NoJet', '_Veto' ], 'selection' : '(nCleanJet==0)' },
                                              'notag'   : { 'scalefactor' : { '1.24' : '0.' }, 'cuts' : [ '_NoTag', '_Veto' ], 'selection' : '(nCleanJet>=1)' } }
    elif '2018' in opt.tag:
        normBackgrounds['WJetsCorr']      = { 'nojet'   : { 'scalefactor' : { '1.34' : '0.' }, 'cuts' : [ '_NoJet', '_Veto' ], 'selection' : '(nCleanJet==0)' },
                                              'notag'   : { 'scalefactor' : { '1.25' : '0.' }, 'cuts' : [ '_NoTag', '_Veto' ], 'selection' : '(nCleanJet>=1)' } }

if 'SignalRegions' in opt.tag or 'BackSF' in opt.tag:

    normBackgrounds['STtW']      = { 'all'   : { 'scalefactor' : { '1.00' : '0.10' }, 'selection' : '1.' } }
    normBackgrounds['ttW']       = { 'all'   : { 'scalefactor' : { '1.00' : '0.50' }, 'selection' : '1.' } } 
    normBackgrounds['Higgs']     = { 'all'   : { 'scalefactor' : { '1.00' : '0.50' }, 'selection' : '1.' } } 
    normBackgrounds['VZ']        = { 'all'   : { 'scalefactor' : { '1.00' : '0.50' }, 'selection' : '1.' } } 
    normBackgrounds['VVV']       = { 'all'   : { 'scalefactor' : { '1.00' : '0.50' }, 'selection' : '1.' } } 
    normBackgrounds['DY']        = { 'all'   : { 'scalefactor' : { '1.00' : '0.50' }, 'selection' : '1.' } }
    normBackgrounds['ttSemilep'] = { 'all'   : { 'scalefactor' : { '1.00' : '0.50' }, 'selection' : '1.' } }

    if 'BackSF' in opt.tag: # To be updated to UL if one wants to use them

        if '2016' in yeartag:
            normBackgrounds['WZ']        = { 'all'   : { 'scalefactor' : { '0.86' : '0.08' }, 'selection' : '1.' } }
            normBackgrounds['ttZ']       = { 'all'   : { 'scalefactor' : { '1.29' : '0.28' }, 'selection' : '1.' } }
            normBackgrounds['ZZTo2L2Nu'] = { 'nojet' : { 'scalefactor' : { '1.13' : '0.31' }, 'cuts' : [ '_NoJet', '_Veto' ],         'selection' : '(nCleanJet==0)' },
                                             'notag' : { 'scalefactor' : { '1.25' : '0.23' }, 'cuts' : [ '_NoTag', '_Tag', '_Veto' ], 'selection' : '(nCleanJet>=1)' },
                                           }
            if 'kZZmass' in opt.tag:
                normBackgrounds['ZZTo2L2Nu']['nojet']['scalefactor'] = { '1.00' : '0.27' }
                normBackgrounds['ZZTo2L2Nu']['notag']['scalefactor'] = { '1.12' : '0.20' }
                #normBackgrounds['ZZTo2L2Nu']['veto']['scalefactor'] = { '1.08' : '0.16' }
            elif 'kZZpt' in opt.tag:
                normBackgrounds['ZZTo2L2Nu']['nojet']['scalefactor'] = { '0.91' : '0.25' }
                normBackgrounds['ZZTo2L2Nu']['notag']['scalefactor'] = { '0.85' : '0.16' }
            elif 'kZZdphi' in opt.tag: 
                normBackgrounds['ZZTo2L2Nu']['nojet']['scalefactor'] = { '1.00' : '0.27' } 
                normBackgrounds['ZZTo2L2Nu']['notag']['scalefactor'] = { '1.13' : '0.21' } 

        elif '2017' in yeartag:
            normBackgrounds['WZ']        = { 'all'   : { 'scalefactor' : { '1.04' : '0.08' }, 'selection' : '1.' } }
            normBackgrounds['ttZ']       = { 'all'   : { 'scalefactor' : { '1.45' : '0.27' }, 'selection' : '1.' } }
            normBackgrounds['ZZTo2L2Nu'] = { 'nojet' : { 'scalefactor' : { '0.83' : '0.25' }, 'cuts' : [ '_NoJet', '_Veto' ],         'selection' : '(nCleanJet==0)' },  
                                             'notag' : { 'scalefactor' : { '0.94' : '0.18' }, 'cuts' : [ '_NoTag', '_Tag', '_Veto' ], 'selection' : '(nCleanJet>=1)' },
                                           }
            if 'kZZmass' in opt.tag:
                normBackgrounds['ZZTo2L2Nu']['nojet']['scalefactor'] = { '0.74' : '0.22' }
                normBackgrounds['ZZTo2L2Nu']['notag']['scalefactor'] = { '0.84' : '0.16' }
                #normBackgrounds['ZZTo2L2Nu']['veto']['scalefactor'] = { '0.81' : '0.13' }
            elif 'kZZpt' in opt.tag: 
                normBackgrounds['ZZTo2L2Nu']['nojet']['scalefactor'] = { '0.68' : '0.20' }
                normBackgrounds['ZZTo2L2Nu']['notag']['scalefactor'] = { '0.66' : '0.12' }
            elif 'kZZdphi' in opt.tag:
                normBackgrounds['ZZTo2L2Nu']['nojet']['scalefactor'] = { '0.74' : '0.22' } 
                normBackgrounds['ZZTo2L2Nu']['notag']['scalefactor'] = { '0.86' : '0.16' }        

        elif '2018' in yeartag:
            normBackgrounds['WZ']        = { 'all'   : { 'scalefactor' : { '0.86' : '0.06' }, 'selection' : '1.' } }
            normBackgrounds['ttZ']       = { 'all'   : { 'scalefactor' : { '1.43' : '0.22' }, 'selection' : '1.' } }
            normBackgrounds['ZZTo2L2Nu'] = { 'nojet' : { 'scalefactor' : { '1.08' : '0.23' }, 'cuts' : [ '_NoJet', '_Veto' ],         'selection' : '(nCleanJet==0)' },
                                             'notag' : { 'scalefactor' : { '0.83' : '0.14' }, 'cuts' : [ '_NoTag', '_Tag', '_Veto' ], 'selection' : '(nCleanJet>=1)' },
                                           }
            if 'kZZmass' in opt.tag:   
                normBackgrounds['ZZTo2L2Nu']['nojet']['scalefactor'] = { '0.95' : '0.20' }
                normBackgrounds['ZZTo2L2Nu']['notag']['scalefactor'] = { '0.75' : '0.13' }
                #normBackgrounds['ZZTo2L2Nu']['veto']['scalefactor'] = { '0.81' : '0.11' }
            elif 'kZZpt' in opt.tag:
                normBackgrounds['ZZTo2L2Nu']['nojet']['scalefactor'] = { '0.88' : '0.19' }
                normBackgrounds['ZZTo2L2Nu']['notag']['scalefactor'] = { '0.58' : '0.10' }
            elif 'kZZdphi' in opt.tag:
                normBackgrounds['ZZTo2L2Nu']['nojet']['scalefactor'] = { '0.96' : '0.20' }
                normBackgrounds['ZZTo2L2Nu']['notag']['scalefactor'] = { '0.76' : '0.13' }

        if 'BackSF' in opt.tag: 
            if 'ZZValidationRegion' in opt.tag or 'ttZValidationRegion' in opt.tag or 'WZValidationRegion' in opt.tag or 'WZtoWWValidationRegion' in opt.tag or 'DYValidationRegion' in opt.tag:
                normBackgrounds['ZZTo2L2Nu']['nojet']['cuts'] = [ 'ptmiss-160' ]
                normBackgrounds['ZZTo2L2Nu']['notag']['cuts'] = [ 'ptmiss-160' ]
                normBackgrounds['ZZTo2L2Nu']['nojet']['selection'] = '(nCleanJet==0 && ptmiss'+ctrltag+'>=160.)'
                normBackgrounds['ZZTo2L2Nu']['notag']['selection'] = '(nCleanJet>=1 && ptmiss'+ctrltag+'>=160.)'
                normBackgrounds['ZZTo4L'] = normBackgrounds['ZZTo2L2Nu']
                normBackgrounds['ttZ']['all']['cuts'] = [ 'ptmiss-160' ] 
                normBackgrounds['ttZ']['all']['selection'] = '(ptmiss'+ctrltag+'>=160.)'
                normBackgrounds['WZ']['all']['cuts'] = [ 'ptmiss-160' ]
                normBackgrounds['WZ']['all']['selection'] = '(ptmiss'+ctrltag+'>=160.)'

# top pt reweighting

Top_pTrw = '(TMath::Sqrt( TMath::Exp(0.0615-0.0005*topGenPt) * TMath::Exp(0.0615-0.0005*antitopGenPt) ) )'
centralTopPt = Top_pTrw 
systematicTopPt = '1.'

### Data info

if '2016' in yeartag or '2017' in yeartag :

    if '2016HIPM' in yeartag :
        DataRun = [ 
            ['B','Run2016B-ver2_HIPM_UL2016-v1'],
            ['C','Run2016C_HIPM_UL2016-v1'],
            ['D','Run2016D_HIPM_UL2016-v1'],
            ['E','Run2016E_HIPM_UL2016-v1'],
            ['F','Run2016F_HIPM_UL2016-v1']
        ]
    elif '2016noHIPM' in yeartag :
        DataRun = [
            ['F','Run2016F_UL2016-v1'],
            ['G','Run2016G_UL2016-v1'],
            ['H','Run2016H_UL2016-v1']
        ]
    elif '2017' in yeartag :
        DataRun = [ 
            ['B','Run2017B-UL2017_MiniAODv2_NanoAODv9-v1'],
            ['C','Run2017C-UL2017_MiniAODv2_NanoAODv9-v1'],
            ['D','Run2017D-UL2017_MiniAODv2_NanoAODv9-v1'],
            ['E','Run2017E-UL2017_MiniAODv2_NanoAODv9-v1'],
            ['F','Run2017F-UL2017_MiniAODv2_NanoAODv9-v1'],
        ]

    DataSets = ['MuonEG','DoubleMuon','SingleMuon','DoubleEG','SingleElectron']

    DataTrig = {
        'MuonEG'         : '(Trigger_ElMu)' ,
        'DoubleMuon'     : '(!Trigger_ElMu && Trigger_dblMu)' ,
        'SingleMuon'     : '(!Trigger_ElMu && !Trigger_dblMu && Trigger_sngMu)' ,
        'DoubleEG'       : '(!Trigger_ElMu && !Trigger_dblMu && !Trigger_sngMu && Trigger_dblEl)' ,
        'SingleElectron' : '(!Trigger_ElMu && !Trigger_dblMu && !Trigger_sngMu && !Trigger_dblEl && Trigger_sngEl)' ,
    }

elif '2018' in yeartag :

    DataRun = [ 
        ['A','Run2018A-UL2018_MiniAODv2_NanoAODv9-v1'] ,
        ['B','Run2018B-UL2018_MiniAODv2_NanoAODv9-v1'] ,
        ['C','Run2018C-UL2018_MiniAODv2_NanoAODv9-v1'] ,
        ['D','Run2018D-UL2018_MiniAODv2_NanoAODv9-v1'] ,
    ]

    if '2018AB' in opt.tag :
        DataRun.remove( ['C','Run2018C-UL2018_MiniAODv2_NanoAODv9-v1'] )
        DataRun.remove( ['D','Run2018D-UL2018_MiniAODv2_NanoAODv9-v1'] )

    if '2018CD' in opt.tag :
        DataRun.remove( ['A','Run2018A-UL2018_MiniAODv2_NanoAODv9-v1'] )
        DataRun.remove( ['B','Run2018B-UL2018_MiniAODv2_NanoAODv9-v1'] )

    DataSets = ['MuonEG','DoubleMuon','SingleMuon','EGamma']

    DataTrig = {
        'MuonEG'         : '(Trigger_ElMu)' ,
        'DoubleMuon'     : '(!Trigger_ElMu && Trigger_dblMu)' ,
        'SingleMuon'     : '(!Trigger_ElMu && !Trigger_dblMu && Trigger_sngMu)' ,
        'EGamma'         : '(!Trigger_ElMu && !Trigger_dblMu && !Trigger_sngMu && (Trigger_sngEl || Trigger_dblEl))' ,
    }

### Backgrounds

if 'EWK' in opt.sigset:

    ewkSFweight = SFweight.replace('*PrefireWeight','').replace('*Lepton_tightElectron_cutBasedMediumPOG_TotSF[1]','').replace('*Lepton_tightMuon_mediumRelIsoTight_TotSF[1]','')

    samples['ttbar'] = {    'name'   : getSampleFiles(directoryBkg,'TTTo2L2Nu'       ,False,treePrefix,skipTreesCheck) + 
                                       getSampleFiles(directoryBkg,'TTToSemiLeptonic',False,treePrefix,skipTreesCheck) ,
                            'weight' : XSWeight+'*'+ewkSFweight ,
                        }

    

    samples['DY'] = { 'name'   : getSampleFiles(directoryBkg,'DYJetsToLL_M-10to50-LO', False,treePrefix,skipTreesCheck) +
                                 getSampleFiles(directoryBkg,'DYJetsToLL_M-50-LO'    , False,treePrefix,skipTreesCheck) ,
                      'weight' : XSWeight+'*'+ewkSFweight ,
                     }

    samples['WJetsToLNu'] = { 'name' : getSampleFiles(directoryBkg,'WJetsToLNu-LO'   , False,treePrefix,skipTreesCheck),
                              'weight' : XSWeight+'*'+ewkSFweight+'*(genWeight<20.)' ,
                              #'isControlSample' : 1,
                             }

if 'SM' in opt.sigset or 'Backgrounds' in opt.sigset:

    samples['ttbar'] = {    'name'   : getSampleFiles(directoryBkg,'TTTo2L2Nu',False,treePrefix,skipTreesCheck),
                            'weight' : XSWeight+'*'+SFweight+'*'+centralTopPt ,
                        }

    if 'btagefficiencies' in opt.tag:

        samples['T2tt'] = { 'name'   : getSampleFiles(directorySig,'T2tt__mStop-400to1200',False,treePrefix,skipTreesCheck),
                            'weight' : XSWeight+'*'+SFweightFS ,
                            }

    if 'btagefficiencies' not in opt.tag and 'TEST' not in opt.tag:
    
        samples['STtW']    = {    'name'   : getSampleFiles(directoryBkg,'ST_tW_top_nohad',    False,treePrefix,skipTreesCheck) +
                                             getSampleFiles(directoryBkg,'ST_tW_antitop_nohad',False,treePrefix,skipTreesCheck),
                                  'weight' : XSWeight+'*'+SFweight ,
                             }

        samples['ttZ']   = {    'name'   : getSampleFiles(directoryBkg,'TTZToLLNuNu_M-10',False,treePrefix,skipTreesCheck) + 
                                           getSampleFiles(directoryBkg,'TTZToQQ'         ,False,treePrefix,skipTreesCheck),
                                'weight' : XSWeight+'*'+SFweight ,
                                }

        samples['ttW']   = {    'name'   : getSampleFiles(directoryBkg,'TTWJetsToLNu',False,treePrefix,skipTreesCheck) +
                                           getSampleFiles(directoryBkg,'TTWJetsToQQ',False,treePrefix,skipTreesCheck), 
                                'weight' : XSWeight+'*'+SFweight ,
                             }
         
        samples['WW']    = {    'name'   :   getSampleFiles(directoryBkg,'WWTo2L2Nu',           False,treePrefix,skipTreesCheck) + 
                                             getSampleFiles(directoryBkg,'GluGluToWWToENEN',False,treePrefix,skipTreesCheck) + 
                                             getSampleFiles(directoryBkg,'GluGluToWWToENMN',False,treePrefix,skipTreesCheck) +
                                             getSampleFiles(directoryBkg,'GluGluToWWToENTN',False,treePrefix,skipTreesCheck) +
                                             getSampleFiles(directoryBkg,'GluGluToWWToMNEN',False,treePrefix,skipTreesCheck) +
                                             getSampleFiles(directoryBkg,'GluGluToWWToMNMN',False,treePrefix,skipTreesCheck) +
                                             getSampleFiles(directoryBkg,'GluGluToWWToMNTN',False,treePrefix,skipTreesCheck) +
                                             getSampleFiles(directoryBkg,'GluGluToWWToTNEN',False,treePrefix,skipTreesCheck) +
                                             getSampleFiles(directoryBkg,'GluGluToWWToTNMN',False,treePrefix,skipTreesCheck) +
                                             getSampleFiles(directoryBkg,'GluGluToWWToTNTN',False,treePrefix,skipTreesCheck),
                                'weight' : XSWeight+'*'+SFweight ,
                            }

        WZext = ''#'_mllmin01' # placeholder TODO: change it when final datasets available
        if '2016HIPM' in yeartag and 'EOY' in opt.tag:
            samples['EOYVZ']  = { 'name'   : getSampleFiles(directoryBkgEOY,'WZTo3LNu'+WZext,False,treePrefix,skipTreesCheck),
                                  'weight' : XSWeight+'*'+SFweight ,
                                  }
        if '2016HIPM' not in yeartag or (isDatacardOrPlot and skipTreesCheck and len(yeartag.split('-'))>1):
            samples['WZ'] = { 'name'   : getSampleFiles(directoryBkg,'WZTo3LNu'+WZext,False,treePrefix,skipTreesCheck),
                              'weight' : XSWeight+'*'+SFweight ,
                             }
        #if '_mllmin01' in WZext: # not processed in nAODv9
        #    addSampleWeight(samples,'WZ','WZTo3LNu'+WZext, '4.42965/(58.59*0.601644)') # Wrong gridpack: mll>4 not mll>0.1

        samples['ZZTo2L2Nu']  = {  'name'   : getSampleFiles(directoryBkg,'ZZTo2L2Nu', False,treePrefix,skipTreesCheck), # +
                                              #getSampleFiles(directoryBkg,'ggZZ2e2n', False,treePrefix,skipTreesCheck) +
                                              #getSampleFiles(directoryBkg,'ggZZ2m2n', False,treePrefix,skipTreesCheck),  
                                   'weight' : XSWeight+'*'+SFweight ,
                                 }
        if '2016HIPM' in yeartag and 'EOY' in opt.tag:
            samples['EOYVZ']['name'] +=  getSampleFiles(directoryBkgEOY,'ggZZ2e2n', False,treePrefix,skipTreesCheck)
            samples['EOYVZ']['name'] +=  getSampleFiles(directoryBkgEOY,'ggZZ2m2n', False,treePrefix,skipTreesCheck)
        elif '2016HIPM' not in yeartag:
            samples['ZZTo2L2Nu']['name'] += getSampleFiles(directoryBkg,'ggZZ2e2n', False,treePrefix,skipTreesCheck)  
            samples['ZZTo2L2Nu']['name'] += getSampleFiles(directoryBkg,'ggZZ2m2n', False,treePrefix,skipTreesCheck)  
        
        addSampleWeight(samples,'ZZTo2L2Nu','ZZTo2L2Nu', '9.738e-01/6.008e-01') # From GenXSecAnalyzer: EOY mll>40 / UL mll>4

        # TODO missing HT binned samples
        samples['DY'] = { 'name' :   #getSampleFiles(directoryBkg,'DYJetsToLL_M-10to50-LO'       , False,treePrefix,skipTreesCheck) +
                                     #getSampleFiles(directoryBkg,'DYJetsToLL_M-4to50_HT-70to100' , False,treePrefix,skipTreesCheck) +
                                     #getSampleFiles(directoryBkg,'DYJetsToLL_M-4to50_HT-100to200', False,treePrefix,skipTreesCheck) +
                                     #getSampleFiles(directoryBkg,'DYJetsToLL_M-4to50_HT-200to400', False,treePrefix,skipTreesCheck) +
                                     #getSampleFiles(directoryBkg,'DYJetsToLL_M-4to50_HT-400to600', False,treePrefix,skipTreesCheck) +
                                     #getSampleFiles(directoryBkg,'DYJetsToLL_M-4to50_HT-600toInf', False,treePrefix,skipTreesCheck) +
                                     #getSampleFiles(directoryBkg,'DYJetsToLL_M-50-LO'           , False,treePrefix,skipTreesCheck) +
                                     getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-70to100'   , False,treePrefix,skipTreesCheck) +
                                     getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-100to200'  , False,treePrefix,skipTreesCheck) +
                                     getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-200to400'  , False,treePrefix,skipTreesCheck) +
                                     getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-400to600'  , False,treePrefix,skipTreesCheck) + 
                                     getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-600to800'  , False,treePrefix,skipTreesCheck) +
                                     getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-800to1200' , False,treePrefix,skipTreesCheck) +
                                     getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-1200to2500', False,treePrefix,skipTreesCheck) +
                                     getSampleFiles(directoryBkg,'DYJetsToLL_M-50_HT-2500toInf' , False,treePrefix,skipTreesCheck) ,
                          'weight' : XSWeight+'*'+SFweight ,
                        }  

        if '2016' in yeartag and 'EOY' in opt.tag:
            samples['EOYDrellYan'] = { 'name'   : getSampleFiles(directoryBkgEOY,'DYJetsToLL_M-10to50-LO' , False,treePrefix,skipTreesCheck),
                                       'weight' : XSWeight+'*'+SFweight ,
                                   }
            if '2016noHIPM' in yeartag: 
                samples['EOYDrellYan']['name'] += getSampleFiles(directoryBkgEOY,'DYJetsToLL_M-50-LO_ext2', False,treePrefix,skipTreesCheck)
                addSampleWeight(samples,'EOYDrellYan','DYJetsToLL_M-50-LO_ext2', 'LHE_HT<70.0')

        if '2016HIPM' in yeartag or '2017' in yeartag or '2018' in yeartag:
            if '2017' in yeartag or '2018' in yeartag:
                samples['DY']['name'] += getSampleFiles(directoryBkg,'DYJetsToLL_M-10to50-LO'       , False,treePrefix,skipTreesCheck)
            samples['DY']['name'] += getSampleFiles(directoryBkg,'DYJetsToLL_M-50-LO'           , False,treePrefix,skipTreesCheck)
            addSampleWeight(samples,'DY','DYJetsToLL_M-50-LO', 'LHE_HT<70.0')

        #addSampleWeight(samples,'DY','DYJetsToLL_M-10to50-LO',  'LHE_HT<70.0') # TODO uncomment when DY M-4to50 samples available
        #addSampleWeight(samples,'DY','DYJetsToLL_M-50-LO', 'LHE_HT<70.0')i     # TODO uncomment when DY M-50-LO samples available for all years

        # TODO missing
        samples['Higgs']   = {  'name'   : getSampleFiles(directoryBkg,'GluGluHToTauTau_M125'   , False,treePrefix,skipTreesCheck) + 
                                           getSampleFiles(directoryBkg,'GluGluHToWWTo2L2Nu_M125', False,treePrefix,skipTreesCheck) + 
                                           getSampleFiles(directoryBkg,'VBFHToWWTo2L2Nu_M125'   , False,treePrefix,skipTreesCheck), #+
                                           #getSampleFiles(directoryBkg,'VBFHToTauTau_M125'      , False,treePrefix,skipTreesCheck) + 
                                           #getSampleFiles(directoryBkg,'HWplusJ_HToWW_M125'     , False,treePrefix,skipTreesCheck) +  
                                           #getSampleFiles(directoryBkg,'HWplusJ_HToTauTau_M125' , False,treePrefix,skipTreesCheck) + 
                                           #getSampleFiles(directoryBkg,'HWminusJ_HToWW_M125'    , False,treePrefix,skipTreesCheck) + 
                                           #getSampleFiles(directoryBkg,'HWminusJ_HToTauTau_M125', False,treePrefix,skipTreesCheck) ,
                                'weight' : XSWeight+'*'+SFweight ,
                               }

        if '2016HIPM' not in yeartag:
            samples['Higgs']['name'] += getSampleFiles(directoryBkg,'HWminusJ_HToTauTau_M125', False,treePrefix,skipTreesCheck)
            samples['Higgs']['name'] += getSampleFiles(directoryBkg,'HWplusJ_HToTauTau_M125' , False,treePrefix,skipTreesCheck)
            samples['Higgs']['name'] += getSampleFiles(directoryBkg,'VBFHToTauTau_M125'      , False,treePrefix,skipTreesCheck)
            
        if 'EOY' in opt.tag: 
            samples['EOYH']   = {  'name'   : getSampleFiles(directoryBkgEOY,'HWplusJ_HToWW_M125'  , False,treePrefix,skipTreesCheck) +
                                              getSampleFiles(directoryBkgEOY,'HWminusJ_HToWW_M125' , False,treePrefix,skipTreesCheck),
                                   'weight' : XSWeight+'*'+SFweight ,
                                   }
            if '2016HIPM' in yeartag:
                samples['EOYH']['name'] += getSampleFiles(directoryBkgEOY,'HWminusJ_HToTauTau_M125', False,treePrefix,skipTreesCheck)
                samples['EOYH']['name'] += getSampleFiles(directoryBkgEOY,'HWplusJ_HToTauTau_M125'     , False,treePrefix,skipTreesCheck)
                samples['EOYH']['name'] += getSampleFiles(directoryBkgEOY,'VBFHToTauTau_M125'      , False,treePrefix,skipTreesCheck)

        if 'EOY' not in opt.tag: # Missing WZ for HIPM and 2017 -> negligible backgrounds, will be added when full UL availble
            samples['VZ'] = { 'name'   : getSampleFiles(directoryBkg,'WZTo2L2Q',False,treePrefix,skipTreesCheck) +
                                         getSampleFiles(directoryBkg,'ZZTo2L2Q',False,treePrefix,skipTreesCheck) ,
                              'weight' : XSWeight+'*'+SFweight
                             }
        if 'EOY' in opt.tag:
            samples['EOYQQ']    = {    'name'   :   getSampleFiles(directoryBkgEOY,'WZTo2L2Q',False,treePrefix,skipTreesCheck) + 
                                                    getSampleFiles(directoryBkgEOY,'ZZTo2L2Q',False,treePrefix,skipTreesCheck) ,
                                       'weight' : XSWeight+'*'+SFweight
                                   }
        
        samples['VVV']   = {    'name'   :   getSampleFiles(directoryBkg,'WWW',False,treePrefix,skipTreesCheck) + 
                                             getSampleFiles(directoryBkg,'WWZ',False,treePrefix,skipTreesCheck) + 
                                             getSampleFiles(directoryBkg,'WZZ',False,treePrefix,skipTreesCheck) + 
                                             getSampleFiles(directoryBkg,'ZZZ',False,treePrefix,skipTreesCheck) +
                                             getSampleFiles(directoryBkg,'WWG',False,treePrefix,skipTreesCheck), 
                                'weight' : XSWeight+'*'+SFweight ,
                                }

        if 'ZZValidationRegion' in opt.tag or 'ttZ' in opt.tag or 'WZValidationRegion' in opt.tag or 'WZtoWWValidationRegion' in opt.tag or 'FitCRWZ' in opt.tag or 'FitCRZZ' in opt.tag or ('FitCR' in opt.tag and isDatacardOrPlot) or 'TheoryNormalizations' in opt.tag:
        
            samples['ZZTo4L']   = {    'name'  :    #getSampleFiles(directoryBkg.replace('reco', 'ctrl'),'ZZTo4L'              , False,treePrefix,skipTreesCheck) +
                                                    getSampleFiles(directoryBkg.replace('reco', 'ctrl'),'ggZZ2e2m'            , False,treePrefix,skipTreesCheck) +
                                                    getSampleFiles(directoryBkg.replace('reco', 'ctrl'),'ggZZ2e2t'            , False,treePrefix,skipTreesCheck) +
                                                    getSampleFiles(directoryBkg.replace('reco', 'ctrl'),'ggZZ2m2t'            , False,treePrefix,skipTreesCheck) + 
                                                    getSampleFiles(directoryBkg.replace('reco', 'ctrl'),'ggZZ4e'              , False,treePrefix,skipTreesCheck) +
                                                    #getSampleFiles(directoryBkg.replace('reco', 'ctrl'),'ggZZ4m'              , False,treePrefix,skipTreesCheck) +
                                                    getSampleFiles(directoryBkg.replace('reco', 'ctrl'),'ggZZ4t'              , False,treePrefix,skipTreesCheck),# +
                                                    #getSampleFiles(directoryBkg.replace('reco', 'ctrl'),'VBFHToZZTo4L_M125'   , False,treePrefix,skipTreesCheck) +
                                                    #getSampleFiles(directoryBkg.replace('reco', 'ctrl'),'GluGluHToZZTo4L_M125', False,treePrefix,skipTreesCheck),
                                       'weight' : XSWeight+'*'+SFweight ,
                                       'JobsPerSample' : 6,
                                       'isControlSample' : 1,
                                   }
     
            missingZZ4L = { '2016HIPM'   : [ 'ZZTo4L', 'ggZZ4m', 'VBFHToZZTo4L_M125', 'GluGluHToZZTo4L_M125' ],
                            '2016noHIPM' : [ 'ZZTo4L'                                                        ], 
                            '2017'       : [                                                                 ],
                            '2018'       : [                                                                 ] } 
                                       
            for yyeeaarr in missingZZ4L:
                if yyeeaarr in yeartag:
                    for addingZZ4L in [ 'ZZTo4L', 'ggZZ4m', 'VBFHToZZTo4L_M125', 'GluGluHToZZTo4L_M125' ]:
                        if addingZZ4L not in missingZZ4L[yyeeaarr]:
                            samples['ZZTo4L']['name'] += getSampleFiles(directoryBkg.replace('reco', 'ctrl'), addingZZ4L, False,treePrefix,skipTreesCheck)
            
            del missingZZ4L['2017']
            del missingZZ4L['2018']
            
            if 'EOY' in opt.tag:
                for yyeeaarr in missingZZ4L:
                    if yyeeaarr in yeartag:
                        firstMissingZZ4L = missingZZ4L[yyeeaarr][0]
                        ZZ4Lstr = '' 
                        if '2016' in yeartag and 'ZZTo4L' in firstMissingZZ4L: ZZ4Lstr+='_ext1'

                        samples['EOYZZ4L']   = { 'name'   : getSampleFiles(directoryBkgEOY,firstMissingZZ4L+ZZ4Lstr,False,treePrefix,skipTreesCheck),
                                                 'weight' : XSWeight+'*'+SFweight ,
                                                  'isControlSample' : 1,
                                                }
 
                        for addingZZ4L in missingZZ4L[yyeeaarr]:
                            if addingZZ4L!=firstMissingZZ4L:
                                samples['EOYZZ4L']['name'] += getSampleFiles(directoryBkgEOY.replace('reco', 'ctrl'), addingZZ4L, False,treePrefix,skipTreesCheck)

            for kZZvariable in [ 'kZZmass', 'kZZdphi', 'kZZpt' ]:
                if kZZvariable in opt.tag:  
                    addSampleWeight(samples,'ZZTo4L','ZZTo4L'+ZZ4Lext, kZZvariable.replace('kZZ', 'kZZ_'))

        nameWJets = 'WJetsToLNu'
        if 'SameSignValidationRegion' in opt.tag or 'DYMeasurements' in opt.tag or 'WJets' in opt.sigset:
            
            if 'WJetsCorr' in opt.sigset: nameWJets = 'WJetsCorr'

            samples[nameWJets] = { 'name' : getSampleFiles(directoryBkg,'WJetsToLNu-LO'          , False,treePrefix,skipTreesCheck) +
                                            getSampleFiles(directoryBkg,'WJetsToLNu_HT70_100'    , False,treePrefix,skipTreesCheck) +
                                            getSampleFiles(directoryBkg,'WJetsToLNu_HT100_200'   , False,treePrefix,skipTreesCheck) +
                                            getSampleFiles(directoryBkg,'WJetsToLNu_HT200_400'   , False,treePrefix,skipTreesCheck) +
                                            getSampleFiles(directoryBkg,'WJetsToLNu_HT400_600'   , False,treePrefix,skipTreesCheck) +
                                            getSampleFiles(directoryBkg,'WJetsToLNu_HT600_800'   , False,treePrefix,skipTreesCheck) +
                                            getSampleFiles(directoryBkg,'WJetsToLNu_HT800_1200'  , False,treePrefix,skipTreesCheck) +
                                            getSampleFiles(directoryBkg,'WJetsToLNu_HT1200_2500' , False,treePrefix,skipTreesCheck) +
                                            getSampleFiles(directoryBkg,'WJetsToLNu_HT2500_inf'  , False,treePrefix,skipTreesCheck),
                                   'weight' : XSWeight+'*'+SFweight.replace('*' + nonpromptLepSF, '') ,
                                   #'isControlSample' : 1,
                                  }
            addSampleWeight(samples,nameWJets,'WJetsToLNu-LO', '(LHE_HT<70.0)*(genWeight<20.)')

            if 'AppWJetsSplit' in opt.tag:

                samples['WJetsPrompt'] = {}
                samples['WJetsFake'] = {}
                for samkey in samples['WJetsToLNu']:
                    samples['WJetsPrompt'][samkey] = samples['WJetsToLNu'][samkey]
                    samples['WJetsFake'][samkey] = samples['WJetsToLNu'][samkey]

                samples['WJetsPrompt']['weight'] += '*'+nTightPromptLepton
                samples['WJetsFake']['weight'] += '*(1.-'+nTightPromptLepton+')'

                del samples['WJetsToLNu']

        #if 'SameSignValidationRegion' in opt.tag:
    
        samples['ttSemilep'] = { 'name'   : getSampleFiles(directoryBkg,'TTToSemiLeptonic', False,treePrefix,skipTreesCheck),
                                 'weight' : XSWeight+'*'+SFweight ,
                                 #'isControlSample' : 1,
                                }

if 'Backgrounds' in opt.sigset and opt.sigset not in 'Backgrounds' and 'Backgrounds-' not in opt.sigset:

    sampleToRemove = [ ] 

    for sample in samples:
        if 'Veto' in opt.sigset:
            if sample in opt.sigset:
                sampleToRemove.append(sample)
            if 'EOY' in sample: 
                sampleToRemove.append(sample)
        elif 'EOYWJets' in opt.sigset:
            if sample!='EOYWJets':
                sampleToRemove.append(sample)
        elif 'BackgroundsEOY'==opt.sigset:
            if 'EOY' not in sample:
                sampleToRemove.append(sample)
            if sample=='EOYWJets':
                sampleToRemove.append(sample)
        elif 'BackgroundsWJets' in opt.sigset:
            if sample!=nameWJets and sample!='WJetsPrompt' and sample!='WJetsFake':
                sampleToRemove.append(sample)
        elif 'Backgrounds'+sample!= opt.sigset:
            sampleToRemove.append(sample)

    for sample in sampleToRemove:
        del samples[sample]
for sample in samples:
    samples[sample]['isSignal']  = 0
    samples[sample]['isDATA']    = 0
    samples[sample]['isFastsim'] = 0
    samples[sample]['suppressNegative'] = ['all']
    samples[sample]['suppressNegativeNuisances'] = ['all']
    samples[sample]['suppressZeroTreeNuisances'] = ['all']

### Data

if 'SM' in opt.sigset or 'Data' in opt.sigset:

    samples['DATA']  = {   'name': [ ] ,    
                           'weight' : METFilters_Data+'*'+VetoHEMdata+'*'+VetoEENoise, 
                           'weights' : [ ],
                           'isData': ['all'],
                           'isSignal'  : 0,
                           'isDATA'    : 1, 
                           'isFastsim' : 0
                       }
    v1v2samples = { 'SingleMuon'     : ['Run2018B','Run2018C'],
                    'DoubleMuon'     : ['Run2016G_UL2016', 'Run2018D'],
                    'DoubleEG'       : ['Run2016B-ver2_HIPM']
              }

    v1v3samples = { 'EGamma' : ['Run2018D'] }
    
    for Run in DataRun :
        for DataSet in DataSets :
            datasetName = DataSet+'_'+Run[1]
            for v1v2sample in v1v2samples:
                if DataSet != v1v2sample: continue
                for v1v2run in v1v2samples[v1v2sample]:
                    if v1v2run in Run[1]: datasetName = datasetName.replace('-v1', '-v2') 
            if DataSet in v1v3samples:
                for v1v3run in v1v3samples[DataSet]:
                    if v1v3run in Run[1]: datasetName = datasetName.replace('-v1', '-v3')

            FileTarget = getSampleFiles(directoryData,datasetName,True,treePrefix,skipTreesCheck)
            for iFile in FileTarget:
                samples['DATA']['name'].append(iFile)
                samples['DATA']['weights'].append(DataTrig[DataSet])

elif 'MET' in opt.sigset:

    if 'cern' in SITE: 
        print 'MET datasets not available on lxplus, please use gridui' 

    metTriggers = ''
    if '2016' in yeartag:
        metTriggers = '(HLT_PFMET300 > 0 || HLT_MET200 > 0 || HLT_PFHT300_PFMET110 > 0 || HLT_PFMET170_HBHECleaned > 0 || HLT_PFMETNoMu120_PFMHTNoMu120_IDTight > 0 || HLT_PFMET120_PFMHT120_IDTight > 0)'
    elif '2017' in yeartag:
        metTriggers = '( HLT_PFMETNoMu120_PFMHTNoMu120_IDTight > 0 || HLT_PFMET120_PFMHT120_IDTight > 0 || HLT_PFHT500_PFMET100_PFMHT100_IDTight > 0 || HLT_PFHT700_PFMET85_PFMHT85_IDTight > 0 || HLT_PFHT800_PFMET75_PFMHT75_IDTight > 0)'
    elif '2018' in yeartag:
        metTriggers = '(HLT_PFMET200_HBHECleaned > 0 || HLT_PFMET200_HBHE_BeamHaloCleaned > 0 || HLT_PFMETTypeOne200_HBHE_BeamHaloCleaned > 0 || HLT_PFMETNoMu120_PFMHTNoMu120_IDTight > 0 || HLT_PFMET120_PFMHT120_IDTight > 0 || HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60 > 0 || HLT_PFMET120_PFMHT120_IDTight_PFHT60 > 0 || HLT_PFHT500_PFMET100_PFMHT100_IDTight > 0 || HLT_PFHT700_PFMET85_PFMHT85_IDTight > 0 || HLT_PFHT800_PFMET75_PFMHT75_IDTight > 0)'

    samples['MET']  = {   'name': [ ] ,
                           'weight' : METFilters_Data+'*'+VetoHEMdata+'*'+VetoEENoise,
                           'weights' : [ ],
                           'isData': ['all'],
                           'isSignal'  : 0,
                           'isDATA'    : 1,
                           'isFastsim' : 0
                       }

    directoryMET = directoryData#.split('__hadd')[0]+'__hadd/'
    if 'TriggerLatino' in opt.tag: 
        directoryMET = directoryMET.replace('DATASusy', 'DATALatino')
        print 'Trees for latino working points not available yet in nAODv9'
        exit()

    for Run in DataRun :
        datasetName = 'MET_'+Run[1]
        if 'Run2016F_UL2016' in Run[1]: datasetName = datasetName.replace('-v1', '-v2')
        if 'Run2018A-UL2018' in Run[1]: datasetName = datasetName.replace('-v1', '-v2')
        if 'Run2018B-UL2018' in Run[1]: datasetName = datasetName.replace('-v1', '-v2')
        FileTarget = getSampleFiles(directoryMET,datasetName,True,treePrefix,skipTreesCheck)
        for iFile in FileTarget:
            samples['MET']['name'].append(iFile)
            samples['MET']['weights'].append( '('+metTriggers+')' )
    
elif 'LeptonL2TRateJetHT' in opt.tag and 'JetHT' in opt.sigset:

    samples['JetHT']  = { 'name': [ ] ,
                          'weight' : METFilters_Data+'*'+VetoHEMdata+'*'+VetoEENoise,
                          'weights' : [ ],
                          'isData': ['all'],
                          'isSignal'  : 0,
                          'isDATA'    : 1,
                          'isFastsim' : 0
                         }

    verSamples = { '_HIPM' : '-v2', 'Run2018A' : '-v2', 'Run2018C' : '_GT36-v1', 'Run2018D' : '-v2'}

    del leptonL2TRateTriggers['SingleElectron']
    del leptonL2TRateTriggers['SingleMuon']

    triggerPath = ''
    for ptrange in leptonL2TRateTriggers['JetHT']:
        if triggerPath!='': triggerPath += ' || '
        triggerPath += leptonL2TRateTriggers['JetHT'][ptrange]

    for Run in DataRun :

        datasetName = 'JetHT_'+Run[1]
        for verrun in verSamples:
            if verrun in Run[1]: datasetName = datasetName.replace('-v1', verSamples[verrun])

        FileTarget = getSampleFiles(directoryData,datasetName,True,treePrefix,skipTreesCheck)
        for iFile in FileTarget:
            samples['JetHT']['name'].append(iFile)
            samples['JetHT']['weights'].append( '('+triggerPath+')' )


elif 'LeptonL2TRate' in opt.tag and 'Single' in opt.sigset:
 
    verSamples = { 'SingleMuon'     :  { 'Run2018A' : '-v2', 'Run2018B' : '_GT36-v1', 'Run2018C' : '_GT36-v1', '_HIPM' : '-v2' },
                   'SingleElectron' :  { '_HIPM'    : '-v2' },
                   'EGamma'         :  { 'Run2018D' : '-v3' },
                  }

    if 'SingleLepton' not in opt.sigset:
        if 'SingleElectron' in opt.sigset: del leptonL2TRateTriggers['SingleMuon']
        if 'SingleMuon' in opt.sigset: del leptonL2TRateTriggers['SingleElectron']
    del leptonL2TRateTriggers['JetHT']

    for DataSet in DataSets :
        if DataSet=='SingleMuon' or DataSet=='SingleElectron' or DataSet=='EGamma':

            dataName = DataSet if DataSet!='EGamma' else 'SingleElectron'

            if dataName not in leptonL2TRateTriggers.keys(): continue

            samples[dataName]  = { 'name': [ ] ,
                                   'weight' : METFilters_Data+'*'+VetoHEMdata+'*'+VetoEENoise,
                                   'weights' : [ ],
                                   'isData': ['all'],
                                   'isSignal'  : 0,
                                   'isDATA'    : 1,
                                   'isFastsim' : 0
                                  }

            triggerPath = ''
            for ptrange in leptonL2TRateTriggers[dataName]:
                if triggerPath!='': triggerPath += ' || '
                triggerPath += leptonL2TRateTriggers[dataName][ptrange]

            for Run in DataRun :   

                if DataSet=='SingleElectron' and 'Run2017B' in Run[1]: continue

                datasetName = DataSet+'_'+Run[1]
                if DataSet in verSamples:
                    for verrun in verSamples[DataSet]:
                        if verrun in Run[1]: datasetName = datasetName.replace('-v1', verSamples[DataSet][verrun])

                FileTarget = getSampleFiles(directoryData,datasetName,True,treePrefix,skipTreesCheck)
                for iFile in FileTarget:
                    samples[dataName]['name'].append(iFile)
                    samples[dataName]['weights'].append( '('+triggerPath+')' )

### Files per job
 
for sample in samples:
    if 'FilesPerJob' not in samples[sample]:
        ntrees = len(samples[sample]['name']) 
        multFactor = 6 if 'JobsPerSample' not in samples[sample] else int(samples[sample]['JobsPerSample'])
        samples[sample]['FilesPerJob'] = int(math.ceil(float(ntrees)/multFactor))

### Signals

exec(open('./signalMassPoints.py').read())

for model in signalMassPoints:
    if model in opt.sigset.replace('EOY', ''):

        isrObservable = 'ptISR' if ('T2' not in model and 'S2' not in model and '2016' in opt.tag) else 'njetISR'

        for massPoint in signalMassPoints[model]:
            if massPointInSignalSet(massPoint, opt.sigset.replace('EOY', '')):

                samples[massPoint] = { 'name'   : getSampleFiles(directorySig,signalMassPoints[model][massPoint]['massPointDataset'],False,treePrefix,skipTreesCheck),
                                       'FilesPerJob' : 2 ,
                                       'suppressNegative':['all'],
                                       'suppressNegativeNuisances' :['all'],
                                       'suppressZeroTreeNuisances' : ['all'],
                                       'isrObservable' : isrObservable,
                                       'isSignal'  : 1,
                                       'isDATA'    : 0,
                                     }
                  
                if fastsimSignal:
                    samples[massPoint]['weight']    = XSWeight+'*'+SFweightFS+'*'+signalMassPoints[model][massPoint]['massPointCut']
                    samples[massPoint]['isFastsim'] = 1
                else:
                    samples[massPoint]['weight']    = XSWeight+'*'+SFweight+'*isrW*'+signalMassPoints[model][massPoint]['massPointCut']
                    samples[massPoint]['isFastsim'] = 0

            
