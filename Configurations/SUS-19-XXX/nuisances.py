### nuisances

### general parameters
if '2016' in opt.tag : 
    year = '_2016'
    lumi_uncertainty    = '1.025'
    trigger_uncertainty = '1.020'
elif '2017' in opt.tag : 
    year = '_2017'
    lumi_uncertainty = '1.023'
    trigger_uncertainty = '1.020'
elif '2018' in opt.tag : 
    year = '_2018'
    lumi_uncertainty = '1.025'
    trigger_uncertainty = '1.020'

### nuisances = {}
 
### statistical uncertainty

nuisances['stat']  = {
              'type'  : 'auto',   # Use the following if you want to apply the automatic combine MC stat nuisances.
              'maxPoiss'  : '10',     # Number of threshold events for Poisson modelling
              'includeSignal'  : '1', # Include MC stat nuisances on signal processes (1=True, 0=False)
              'samples' : {}
             }

### lnN

# luminosity -> https://twiki.cern.ch/twiki/bin/view/CMS/TWikiLUM#TabLum

nuisances['lumi']  = {
               'name'  : 'lumi_13TeV'+year,
               'samples'  : { },
               'type'  : 'lnN',
}
for sample in samples.keys():
    if not samples[sample]['isDATA']:
        nuisances['lumi']  ['samples'][sample] = lumi_uncertainty 

# trigger

nuisances['trigger']  = {
               'name'  : 'trigger'+year,
               'samples'  : { },
               'type'  : 'lnN',
}
for sample in samples.keys():
    if not samples[sample]['isDATA']:
        nuisances['trigger']  ['samples'][sample] = trigger_uncertainty

# background cross section and scale factor uncertainties

if 'SignalRegions' in opt.tag:
    for background in normBackgrounds:
        if background in samples:

            scalefactorFromData = True

            for region in normBackgrounds[background]:
                nuisancename = 'norm'+background+region
                scalefactor = normBackgrounds[background][region]['scalefactor'].keys()[0]
                scalefactorerror = normBackgrounds[background][region]['scalefactor'][scalefactor]
                nuisances[nuisancename]  = {
                    'name'    : nuisancename+year, 
                    'samples' : { background : str(1.+float(scalefactorerror)/float(scalefactor)) },
                    'cuts'    : normBackgrounds[background][region]['cuts'], 
                    'type'    : 'lnN',
                }
                if region=='all' and scalefactor=='1.00':
                    scalefactorFromData = False

            if scalefactorFromData:
            
                if background in nuisances['lumi']['samples']:
                    del nuisances['lumi']['samples'][background]
            
                if background in nuisances['trigger']['samples']:
                    del nuisances['trigger']['samples'][background]

### shapes

# lepton reco, id, iso, fastsim

for scalefactor in leptonSF:

    nuisances[scalefactor]  = {
        'name'  : scalefactor+year,
        'samples'  : { },
        'kind'  : 'weight',
        'type'  : 'shape',
    }
    for sample in samples.keys():
        if not samples[sample]['isDATA']:
            if 'FS' not in scalefactor or samples[sample]['isFastsim']:
                nuisances[scalefactor]['samples'][sample] = leptonSF[scalefactor]

# b-tagging scale factors

weight1b = btagWeight1tag+'_syst/'+btagWeight1tag
weight0b = '(1.-'+btagWeight1tag+'_syst)/(1.-'+btagWeight1tag+')'

btagSF = {
    'btag1b'     : [ weight1b.replace('syst', 'b_up'),         weight1b.replace('syst', 'b_down') ],
    'btag0b'     : [ weight0b.replace('syst', 'b_up'),         weight0b.replace('syst', 'b_down') ],
    'mistag1b'   : [ weight1b.replace('syst', 'l_up'),         weight1b.replace('syst', 'l_down') ],
    'mistag0b'   : [ weight0b.replace('syst', 'l_up'),         weight0b.replace('syst', 'l_down') ],
    'btag1bFS'   : [ weight1b.replace('syst', 'b_up_fastsim'), weight1b.replace('syst', 'b_down_fastsim') ],
    'btag0bFS'   : [ weight0b.replace('syst', 'b_up_fastsim'), weight0b.replace('syst', 'b_down_fastsim') ],
    'ctag1bFS'   : [ weight1b.replace('syst', 'c_up_fastsim'), weight1b.replace('syst', 'c_down_fastsim') ],
    'ctag0bFS'   : [ weight0b.replace('syst', 'c_up_fastsim'), weight0b.replace('syst', 'c_down_fastsim') ],
    'mistag1bFS' : [ weight1b.replace('syst', 'l_up_fastsim'), weight1b.replace('syst', 'l_down_fastsim') ],
    'mistag0bFS' : [ weight0b.replace('syst', 'l_up_fastsim'), weight0b.replace('syst', 'l_down_fastsim') ],
}

for scalefactor in btagSF:
    nuisances[scalefactor]  = {
        'name'  : scalefactor.replace('0', '').replace('1', '') +year,
        'samples'  : { },
        'kind'  : 'weight',
        'type'  : 'shape',
        'cuts'  : [ ]           
    }
    for sample in samples.keys():
        if not samples[sample]['isDATA']:
            if 'FS' not in scalefactor or samples[sample]['isFastsim']:
                nuisances[scalefactor]['samples'][sample] = btagSF[scalefactor]
    for cut in cuts.keys():
        if ('1b' in scalefactor and '_Tag' in cut) or ('0b' in scalefactor and ('_Veto' in cut or '_NoTag' in cut)):
            nuisances[scalefactor]['cuts'].append(cut)

# pileup

nuisances['pileup']  = {
    'name'  : 'pileup', # inelastic cross section correlated through the years
    'samples'  : { },
    'kind'  : 'weight',
    'type'  : 'shape',
}
for sample in samples.keys():
    if not samples[sample]['isDATA']:
        nuisances['pileup']['samples'][sample] = [ 'puWeightUp/puWeight', 'puWeightDown/puWeight' ] 

# ECAL prefiring
"""
if '2016' in opt.tag or '2017' in opt.tag: 
    nuisances['prefiring']  = {
        'name'  : 'prefiring'+year, 
        'samples'  : { },
        'kind'  : 'weight',
        'type'  : 'shape',
    }
    for sample in samples.keys():
        if not samples[sample]['isDATA']:
            nuisances['pileup']['samples'][sample] = [ 'PrefireWeight_Up/PrefireWeight', 'PrefireWeight_Down/PrefireWeight' ] 
"""
# nonprompt lepton rate

nuisances['nonpromptLep']  = {
    'name'  : 'nonpromptLep'+year, 
    'samples'  : { },
    'kind'  : 'weight',
    'type'  : 'shape',
}
for sample in samples.keys():
    if not samples[sample]['isDATA']:
        nuisances['nonpromptLep']['samples'][sample] = [ nonpromptLepSF_Up+'/'+nonpromptLepSF, nonpromptLepSF_Down+'/'+nonpromptLepSF ] 

# top pt reweighting

nuisances['toppt']  = {
    'name'  : 'toppt', # assuming the mismodeling is correlated through the years 
    'samples'  : { 'ttbar' : [ systematicTopPt+'/'+centralTopPt, '1.' ] },
    'kind'  : 'weight',
    'type'  : 'shape',
}

# isr fastsim

nuisances['isrFS']  = {
    'name'  : 'isrFS', # assuming the mismodeling is correlated through the years 
    'samples'  : { },
    'kind'  : 'weight',
    'type'  : 'shape',
}
for sample in samples.keys():
    if 'isrObservable' in samples[sample]:
            if samples[sample]['isrObservable']=='njetISR':
                isrWeight = [ '0.5*(3.*isrW-1.)', '0.5*(isrW+1.)/isrW' ]
            elif samples[sample]['isrObservable']=='ptISR':
                isrWeight = [ '(2.*isrW-1.)/isrW', '1./isrW' ]
            else:
                print 'ERROR: no isrW implementation for model', model
            nuisances['isrFS']['samples'][sample] = isrWeight

### mt2ll backgrounds (special case for shape uncertainties)

# mt2ll top and WW

mt2llRegions = ['SR1_', 'SR2_', 'SR3_']
mt2llBins = ['Bin4', 'Bin5', 'Bin6', 'Bin7']
mt2llEdges = ['60.', '80.', '100.', '120.', '999999999.']
mt2llSystematics = [0.05, 0.10, 0.20, 0.30]

for mt2llregion in mt2llRegions: 
    for mt2llbin in range(len(mt2llBins)):

        mt2llsystname = mt2llregion + mt2llBins[mt2llbin]
        mt2llweightUp = '(mt2ll>='+mt2llEdges[mt2llbin]+' && mt2ll<'+mt2llEdges[mt2llbin+1]+') ? '+str(1.+mt2llSystematics[mt2llbin])+' : 1.'  
        mt2llweightDo = '(mt2ll>='+mt2llEdges[mt2llbin]+' && mt2ll<'+mt2llEdges[mt2llbin+1]+') ? '+str(1.-mt2llSystematics[mt2llbin])+' : 1.'  
        
        nuisances['Top_'+mt2llsystname]  = {
            'name'  : 'Top_'+mt2llsystname+year,
            'samples'  : { 
                'ttbar' : [ mt2llweightUp, mt2llweightDo],
                'STtW'  : [ mt2llweightUp, mt2llweightDo],
                'tW'    : [ mt2llweightUp, mt2llweightDo], # backward compatibility for background names
            },
            'kind'  : 'weight',
            'type'  : 'shape',
            'cuts'  : [ ]           
        }
        
        nuisances['WW_'+mt2llsystname]  = {
            'name'  : 'WW_'+mt2llsystname+year,
            'samples'  : { 
                'WW' : [ mt2llweightUp, mt2llweightDo],
            },
            'kind'  : 'weight',
            'type'  : 'shape',
            'cuts'  : [ ]           
        }

        for cut in cuts.keys():
            if mt2llregion in cut:
                nuisances['Top_'+mt2llsystname]['cuts'].append(cut)
                nuisances['WW_' +mt2llsystname]['cuts'].append(cut)

# mt2ll DY (from control regions)
 
# mt2ll ZZ (from k-factors)

# mt2ll signal
if '__susyMT2reco' not in directorySig:
    nuisances['ptmissfastsim']  = {
        'name'  : 'ptmissfastsim', # mismodeling correlated through the years?
        'samples'  : { },
        'kind'  : 'tree',
        'type'  : 'shape',
        'folderUp':   directorySig.replace('__susyMT2fast', '__susyMT2reco'),
        'folderDown': directorySig.replace('__susyMT2fast', '__susyMT2genm').replace('Smear', 'Nomin'),
    }
    for sample in samples.keys():
        if samples[sample]['isFastsim']:
            nuisances['ptmissfastsim']['samples'][sample] = ['1.', '1.']

### LHE weights

# LHE scale variation weights (w_var / w_nominal)
# [0] is muR=0.50000E+00 muF=0.50000E+00
# [1] is muR=0.50000E+00 muF=0.10000E+01
# [2] is muR=0.50000E+00 muF=0.20000E+01
# [3] is muR=0.10000E+01 muF=0.50000E+00
# [4] is muR=0.10000E+01 muF=0.10000E+01
# [5] is muR=0.10000E+01 muF=0.20000E+01
# [6] is muR=0.20000E+01 muF=0.50000E+00
# [7] is muR=0.20000E+01 muF=0.10000E+01
# [8] is muR=0.20000E+01 muF=0.20000E+01

#variations = ['LHEScaleWeight[%d]' % i for i in [0, 1, 3, 5, 7, 8]]
"""
nuisances['QCDscale'] = {
    'name': 'QCDscale', # Scales correlated through the years?
    #'kind': 'weight_envelope',
    'kind': 'weight',
    'type': 'shape',
    'samples': { },
}
for sample in samples.keys():
    if not samples[sample]['isDATA']:
        nuisances['QCDscale']['samples'][sample] = [ 'LHEScaleWeight[8]', 'LHEScaleWeight[0]' ] 
"""
### JES, JER and MET

for treeNuisance in treeNuisances:

    for mcType in treeNuisanceDirs[treeNuisance]:
        if 'Down' not in treeNuisanceDirs[treeNuisance][mcType] or 'Up' not in treeNuisanceDirs[treeNuisance][mcType]:
            print 'nuisance warning: missing trees for', treeNuisance, mcType, 'variations'
        else:

            mcTypeName = '_'+mcTpye if (mcType=='FS' and not treeNuisances[treeNuisance]['MCtoFS']) else ''
            yearCorr = '' if treeNuisances[treeNuisance]['year'] else year # correlated through the years?

            nuisances[treeNuisance+mcType] = {
                'name': treeNuisance+mcTypeName+yearCorr, 
                'kind': 'tree',
                'type': 'shape',
                'samples': { },
                'folderDown': treeNuisanceDirs[treeNuisance][mcType]['Down'],
                'folderUp':   treeNuisanceDirs[treeNuisance][mcType]['Up'],
            }
            for sample in samples.keys():
                if not samples[sample]['isDATA']:
                    if (mcType=='MC' and not samples[sample]['isFastsim']) or (mcType=='FS' and samples[sample]['isFastsim']):
                        nuisances[treeNuisance+mcType]['samples'][sample] = ['1.', '1.']

            if len(nuisances[treeNuisance+mcType]['samples'].keys())==0:
                del nuisances[treeNuisance+mcType]

### rate parameters

rateparameters = {
    'Topnorm' :  { 
        'samples' : [ 'ttbar', 'tW', 'STtW' ],
        'subcut'  : '',
    },
    'WWnorm'  : {
        'samples' : [ 'WW' ],
        'subcut'  : '',
    },
    'NoJetRate_JetBack' : {
        'samples' : [ 'ttbar', 'tW', 'STtW', 'ttW', 'ttZ' ],
        'subcut'  : '_NoJet_',
        'limits'  : '[0.5,1.5]',
    },
    'JetRate_JetBack' : {
        'samples'  : [ 'ttbar', 'tW', 'STtW', 'ttW', 'ttZ' ],
        'subcut'   : '_NoTag_',
        'bondrate' : 'NoJetRate_JetBack',
    },
    'NoJetRate_DibosonBack' : {
        'samples' : [ 'WW', 'WZ' ],
        'subcut'  : '_NoJet_',
        'limits'  : '[0.7,1.3]'
    },
    'JetRate_DibosonBack' : {
        'samples' : [ 'WW', 'WZ' ],
        'subcut'  : '_NoTag_',
        'bondrate' : 'NoJetRate_DibosonBack',
    },
}

if hasattr(opt, 'inputFile'):
    for mt2llregion in mt2llRegions: 
        for rateparam in rateparameters: 
            
            rateparamname = rateparam + '_' + mt2llregion
            
            for sample in rateparameters[rateparam]['samples']:

                if sample not in samples: continue # backward compatibility for background names

                nuisances[sample+rateparamname]  = {
                    'name'  : rateparamname+year,
                    'samples'  : { sample : '1.00' },
                    'type'  : 'rateParam',
                    'cuts'  : [ ] 
                }
                
                if 'limits' in rateparameters[rateparam].keys():
                    nuisances[sample+rateparamname]['limits'] = rateparameters[rateparam]['limits'] 
                    
                for cut in cuts.keys():
                    if mt2llregion in cut and rateparameters[rateparam]['subcut'] in  cut:

                        nuisances[sample+rateparamname]['cuts'].append(cut)
                        
                if 'bondrate' in rateparameters[rateparam].keys():
                                
                    fileIn = ROOT.TFile(opt.inputFile, "READ")

                    nuisances[sample+rateparamname]['bond'] = {}

                    for cut in nuisances[sample+rateparamname]['cuts']:

                        nuisances[sample+rateparamname]['bond'][cut] = {}

                        for variable in variables.keys():

                            histoB = fileIn.Get(cut+'/'+variable+'/histo_'+sample)
                            cutB = rateparameters[rateparam]['subcut']
                            cutA = rateparameters[rateparameters[rateparam]['bondrate']]['subcut']
                            histoA = fileIn.Get(cut.replace(cutB, cutA)+'/'+variable+'/histo_'+sample)
                            yieldB = '%-.4f' % histoB.Integral()
                            yieldA = '%-.4f' % histoA.Integral()
            
                            bond_formula = '1+'+yieldA+'/'+yieldB+'*(1.-@0)' 
                            bond_parameters = rateparameters[rateparam]['bondrate']+'_'+mt2llregion+year
                            
                            nuisances[sample+rateparamname]['bond'][cut][variable] =  { bond_formula : bond_parameters }

                    fileIn.Close()

### Nasty tricks ...

nuisanceToRemove = [ ]  

if 'ValidationRegion' in opt.tag:

    pass
    #for nuisance in nuisances:
    #    #if 'kind' not in nuisances[nuisance]:
    #    #    nuisanceToRemove.append(nuisance)
    #    #elif nuisances[nuisance]['kind']!='tree' and 'pileup' not in nuisance:
    #    if 'jer' not in nuisance: # 
    #        nuisanceToRemove.append(nuisance)

elif 'ControlRegion' in opt.tag or 'TwoLeptons' in opt.tag or 'Preselection' in opt.tag:

    for nuisance in nuisances:
        #if nuisance!='stat' and nuisance!='lumi': # example ...
        if 'jer' not in nuisance: # 
            nuisanceToRemove.append(nuisance)
            
elif 'SignalRegion' not in opt.tag:

    for nuisance in nuisances:
        if 'lumi' not in nuisance: 
            nuisanceToRemove.append(nuisance)

for nuisance in nuisanceToRemove:
    del nuisances[nuisance]

