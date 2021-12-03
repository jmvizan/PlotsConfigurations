
### aliases = { }

## Trigger efficiencies

if recoFlag=='_UL' and 'Trig' in opt.tag and 'Trigger' not in opt.tag and 'TriggerEffWeight_2l' in TriggerEff: # Too low stat for 3Lep

    leptonFlag = '_3Lep' if 'TriggerEffWeight_3l' in TriggerEff else ''
    triggerEfficiencyFile = os.getenv('PWD')+'/Data/'+yeartag+'/TriggerEfficiencies_UL'+yeartag+leptonFlag+'.root'
    triggerPtBins = 'Leptonpt1pt2' # [20, 25, 30, 40, 50, 70, 100, 150, 200]
    #triggerPtBins = 'Leptonpt1pt2bis' # [20, 30, 40, 60, 100, 160, 200]
    triggerEtaBins = 'split' if ('TrigEta' in opt.tag or 'TrigBTagEta' in opt.tag) else 'merged'
   
    trW = 'triggerWeight' 
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
        trW = '1.'
    for sample in samples:
        if not samples[sample]['isDATA']:
            aliases['triggerWeight']['samples'].append(sample)
            if 'TrigBTag' in opt.tag:
                aliases['triggerWeightBTag']['samples'].append(sample)
                aliases['triggerWeightVeto']['samples'].append(sample)
            samples[sample]['weight'] = samples[sample]['weight'].replace(TriggerEff, trW)
     
## FastSim lepton scale factors

fastsimLeptonScaleFactorFile = os.getenv('PWD')+'/Data/'+yeartag+'/fastsimLeptonWeights.root' # TODO switch to UL scale factors when FastSim available
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

if 'nanoAODv8' in opt.samplesFile or 'TestExtraV8' in opt.tag:
        
    if "noweights" in opt.tag.lower(): 
        print "no additional lepton weights being applied"
    else:
        AdditionalElectronScaleFactorFile = os.getenv('PWD')+'/Data/'+yeartag+'/AdditionalSF_'+yeartag+'Ele.root'
        AdditionalMuonScaleFactorFile     = os.getenv('PWD')+'/Data/'+yeartag+'/AdditionalSF_'+yeartag+'Muon.root'
        aliases['additionalLeptonWeight'] = {
            'linesToAdd': [ 'gSystem->AddIncludePath("-I%s/src/");' % os.getenv('CMSSW_RELEASE_BASE'), '.L '+os.getenv('PWD')+'/additionalLeptonWeightReader.cc+' ],
            'class': 'AdditionalLeptonWeightReader',
            'args': ( AdditionalMuonScaleFactorFile , AdditionalElectronScaleFactorFile, "hSFDataMC_central" ),
            'samples': [ ]
        }
        for sample in samples:
            if  not samples[sample]['isDATA']:
                aliases['additionalLeptonWeight']['samples'].append(sample)
                samples[sample]['weight'] = samples[sample]['weight'].replace(LepWeight, LepWeight+'*additionalLeptonWeight')
    
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

