
### aliases = { }

## Trigger efficiencies

if recoFlag=='_UL' and 'TrigLatino' not in opt.tag and 'Trigger' not in opt.tag:

    leptonFlag = '_3Lep' if 'TriggerEffWeight_3lXXX' in TriggerEff else '' # and 'TriggerEffWeight_2l' in TriggerEff: # Too low stat for 3Lep
    triggerEfficiencyFile = os.getenv('PWD')+'/Data/'+yeartag+'/TriggerEfficiencies_UL'+yeartag+leptonFlag+'.root'
    triggerPtBins = 'Leptonpt1pt2' # [20, 25, 30, 40, 50, 70, 100, 150, 200]
    #triggerPtBins = 'Leptonpt1pt2bis' # [20, 30, 40, 60, 100, 160, 200]
    triggerEtaBins = 'split' if ('TrigEta' in opt.tag or 'TrigBTagEta' in opt.tag) else 'merged'
  
    aliases['triggerWeight'] = {
            'linesToAdd': [ 'gSystem->AddIncludePath("-I%s/src/");' % os.getenv('CMSSW_RELEASE_BASE'), '.L '+os.getenv('PWD')+'/triggerWeightReader.cc+' ],
            'class': 'TriggerWeightReader',
            'args': ( triggerEfficiencyFile, triggerPtBins, triggerEtaBins, 'met' ),
            'samples': [ ]
    }
    if 'TrigBTag' in opt.tag:
        aliases['triggerWeightBTag'] = {
                'linesToAdd': [ 'gSystem->AddIncludePath("-I%s/src/");' % os.getenv('CMSSW_RELEASE_BASE'), '.L '+os.getenv('PWD')+'/triggerWeightReader.cc+' ],
                'class': 'TriggerWeightReader',
                'args': ( triggerEfficiencyFile, triggerPtBins, triggerEtaBins, 'btag' ),
                'samples': [ ]
        }
        aliases['triggerWeightVeto'] = {
                'linesToAdd': [ 'gSystem->AddIncludePath("-I%s/src/");' % os.getenv('CMSSW_RELEASE_BASE'), '.L '+os.getenv('PWD')+'/triggerWeightReader.cc+' ],
                'class': 'TriggerWeightReader',
                'args': ( triggerEfficiencyFile, triggerPtBins, triggerEtaBins, 'veto' ),
                'samples': [ ]
        }
    for sample in samples:
        if not samples[sample]['isDATA']:
            aliases['triggerWeight']['samples'].append(sample)
            trW = 'triggerWeight[1]' if 'TriggerEffWeight_2l' in TriggerEff else '1.' # Too low stat for 3Lep
            if 'TrigBTag' in opt.tag:
                aliases['triggerWeightBTag']['samples'].append(sample)
                aliases['triggerWeightVeto']['samples'].append(sample)
                trW = '1.'
            samples[sample]['weight'] = samples[sample]['weight'].replace(TriggerEff, trW)

## Signal anlges

signalSamples = []
for sample in samples:
    if samples[sample]['isSignal']:
        signalSamples.append(sample)

if 'SignalStudies' in opt.tag and len(signalSamples)>0:
 
    aliases['decayAngleCME'] = {
            'linesToAdd': [ 'gSystem->AddIncludePath("-I%s/src/");' % os.getenv('CMSSW_RELEASE_BASE'), '.L '+os.getenv('PWD')+'/decayAngleCME.cc+' ],
            'class': 'DecayAngleCME',
            'args': ( ),
            'samples': signalSamples
    }

## Lepton LooseToTight Rates

if recoFlag=='_UL':

    if 'WJetsCorr' in samples:

        wpFlag = 'Tight' if 'TightLep' in opt.tag else ''
        leptonL2TRateFile = os.getenv('PWD')+'/Data/'+yeartag+'/'+wpFlag+'LeptonL2TRate.root'

        aliases['leptonL2TWeight'] = {
                'linesToAdd': [ 'gSystem->AddIncludePath("-I%s/src/");' % os.getenv('CMSSW_RELEASE_BASE'), '.L '+os.getenv('PWD')+'/leptonL2TWeightReader.cc+' ],
                'class': 'LeptonL2TWeightReader',
                'args': ( leptonL2TRateFile, 'mediumRelIsoTight', 'cutBasedMediumPOG'),
                'samples': [ ]
        }
        aliases['leptonL2TWeight']['samples'].append('WJetsCorr')
        samples['WJetsCorr']['weight'] += '*leptonL2TWeight'
 
## FastSim lepton scale factors

if 'FSv6' in opt.tag: 
    fastsimLeptonScaleFactorFile = os.getenv('PWD')+'/Data/'+yeartag.replace('noHIPM','').replace('HIPM','')+'/fastsimLeptonWeights.root'
elif 'T2' in opt.sigset:
    fastsimLeptonScaleFactorFile = os.getenv('PWD')+'/Data/'+yeartag+'/fastsimLeptonWeights_UL_ttbar__all.root'
else:
    fastsimLeptonScaleFactorFile = os.getenv('PWD')+'/Data/'+yeartag+'/fastsimLeptonWeights_UL_DY.root'
fastsimMuonScaleFactorHisto = 'Muo_tight_fullsim'
fastsimElectronScaleFactorHisto = 'Ele_tight_fullsim'

if 'nanoAODv9' in opt.samplesFile: 
    LepWeightFS = LepWeight['Lep']['FastSim']
    if 'TestExtraV8' in opt.tag: LepWeight = LepWeight['Lep']['IdIso']
    if 'TestExtraV6' in opt.tag: EleWeight = LepWeight['Lep']['IdIso']

aliases['fastsimLeptonWeight'] = {
        'linesToAdd': [ 'gSystem->AddIncludePath("-I%s/src/");' % os.getenv('CMSSW_RELEASE_BASE'), '.L '+os.getenv('PWD')+'/fastsimLeptonWeightReader.cc+' ],
        'class': 'FastsimLeptonWeightReader',
        'args': ( fastsimLeptonScaleFactorFile, fastsimMuonScaleFactorHisto, fastsimElectronScaleFactorHisto ),
        'samples': [ ]
} 
for sample in samples:
    if 'isFastsim' in samples[sample] and samples[sample]['isFastsim']:
        aliases['fastsimLeptonWeight']['samples'].append(sample)
        samples[sample]['weight'] = samples[sample]['weight'].replace(LepWeightFS, 'fastsimLeptonWeight')

## d_xy/d_z/noLostHits scale factors

if 'nanoAODv9' in opt.samplesFile and 'ExtraV1' not in opt.tag:

    additionalSFDir = os.getenv('PWD')+'/../../../LatinoAnalysis/NanoGardener/python/data/scale_factor/Full'+yeartag.replace('noHIPM','').replace('HIPM','')+'v8/'       
    AdditionalElectronScaleFactorFile = additionalSFDir+'AdditionalSF_'+yeartag.replace('2016','2016_')+'Ele_v2.root'
    AdditionalMuonScaleFactorFile     = additionalSFDir+'AdditionalSF_'+yeartag.replace('2016','2016_')+'Muon.root'
    aliases['additionalLeptonWeight'] = {
        'linesToAdd': [ 'gSystem->AddIncludePath("-I%s/src/");' % os.getenv('CMSSW_RELEASE_BASE'), '.L '+os.getenv('PWD')+'/additionalLeptonWeightReader.cc+' ],
        'class': 'AdditionalLeptonWeightReader',
        'args': ( AdditionalMuonScaleFactorFile , AdditionalElectronScaleFactorFile, "hSFDataMC_central" ),
        'samples': [ ]
    }
    for sample in samples:
        if not samples[sample]['isDATA']:
            aliases['additionalLeptonWeight']['samples'].append(sample)
            samples[sample]['weight'] += '*additionalLeptonWeight[1]'
    
elif 'nanoAODv6' in opt.samplesFile or 'TestExtraV6' in opt.tag:

    if '2016' in opt.tag:
        zerohitElectronRootFile = 'Full2016v2/ElectronScaleFactors_Run2016_SUSY.root'
    elif '2017' in opt.tag:
        zerohitElectronRootFile = 'Full2017/ElectronScaleFactors_Run2017_SUSY.root'
    elif '2018' in opt.tag:
        zerohitElectronRootFile = 'Full2018/ElectronScaleFactors_Run2018_SUSY.root'
    
    zerohitElectronScaleFactorFile = os.getenv('CMSSW_BASE')+'/src/LatinoAnalysis/NanoGardener/python/data/scale_factor/'+zerohitElectronRootFile
    zerohitElectronScaleFactorHisto = 'Run'+yeartag+'_ConvIHit0'

    aliases['zerohitLeptonWeight'] = {
        'linesToAdd': [ 'gSystem->AddIncludePath("-I%s/src/");' % os.getenv('CMSSW_RELEASE_BASE'), '.L '+os.getenv('PWD')+'/zerohitLeptonWeightReader.cc+' ],
        'class': 'ZeroHitLeptonWeightReader',
        'args': ( zerohitElectronScaleFactorFile , zerohitElectronScaleFactorHisto ),
        'samples': [ ]
    }

    for sample in samples:
        if not samples[sample]['isDATA']:
            aliases['zerohitLeptonWeight']['samples'].append(sample)
            samples[sample]['weight'] = samples[sample]['weight'].replace(EleWeight, EleWeight+'*zerohitLeptonWeight')

if 'SearchRegionKinematics' in opt.tag:

    aliases['btagWeightNtag'] = {
        'linesToAdd': [ 'gSystem->AddIncludePath("-I%s/src/");' % os.getenv('CMSSW_RELEASE_BASE'), '.L '+os.getenv('PWD')+'/btagWeightNtag.cc+' ],
        'class': 'BTagWeightNtag',
        'args': ( btagDisc, btagAlgo+bTagWP, float(bTagCut), float(bTagEtaMax) ),
        'samples': [ ]
    }
    for sample in samples:
        if not samples[sample]['isDATA']:
            aliases['btagWeightNtag']['samples'].append(sample)

## jet PU ID

if recoFlag=='_UL' and 'JPUW' in opt.tag:

    jetPUIDfile = os.getenv('PWD')+'/Data/PUID_106XTraining_ULRun2_EffSFandUncties_v1.root'
    jetPUIDhisto = 'UL'
    if '2016HIPM' in yeartag: jetPUIDhisto += '2016APV'
    elif '2016noHIPM' in yeartag: jetPUIDhisto += '2016'
    else: jetPUIDhisto += yeartag
    jetPUIDhisto += '_L'

    aliases['jetPUIDweight'] = {
        'linesToAdd': [ 'gSystem->AddIncludePath("-I%s/src/");' % os.getenv('CMSSW_RELEASE_BASE'), '.L '+os.getenv('PWD')+'/jetPUIDWeightReader.cc+' ],
        'class': 'JetPUIDWeightReader',
        'args': ( jetPUIDfile , jetPUIDhisto, float(bTagCut)),
        'samples': [ ]
    }
    for sample in samples:
        if not samples[sample]['isDATA']:
            aliases['jetPUIDweight']['samples'].append(sample)
            #samples[sample]['weight'] += '*jetPUIDweight'



