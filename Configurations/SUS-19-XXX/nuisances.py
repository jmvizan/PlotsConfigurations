### nuisances

### general parameters

if len(yearstag.keys())!=1:
    print 'WARNING: nuisances.py cannot be used on multiple years'
    exit()

for key in yearstag:
    year = '_' + key
    yearstaglist = yearstag[key].split('-')

### nuisances = {}
 
### statistical uncertainty

nuisances['stat']  = {
              'type'  : 'auto',   # Use the following if you want to apply the automatic combine MC stat nuisances.
              'maxPoiss'  : '10',     # Number of threshold events for Poisson modelling
              'includeSignal'  : '1', # Include MC stat nuisances on signal processes (1=True, 0=False)
              'removeZeros' : removeZeros,
              'samples' : {}
             }

### global lnN (luminosity and trigger)

for globalNuisance in globalNuisances:

    nuisances[globalNuisance]  = {
                   'name'  : globalNuisances[globalNuisance]['name'].replace('_yeartag', year.replace('noHIPM','').replace('HIPM','')), # Bleah!
                   'samples'  : { },
                   'type'  : 'lnN',
    }
    for sample in samples.keys():
        if not samples[sample]['isDATA']:
            nuisances[globalNuisance]['samples'][sample] = globalNuisances[globalNuisance]['value']

# background cross section and scale factor uncertainties

for background in normBackgroundNuisances:
    if background in samples:

        scalefactorFromData = False

        for region in normBackgroundNuisances[background]:
            nuisancename = normBackgroundNuisances[background][region]['name']
            nuisances[nuisancename]  = {
                'name'    : nuisancename+year.replace('noHIPM','').replace('HIPM',''), 
                'samples' : normBackgroundNuisances[background][region]['samples'],
                'cuts'    : normBackgroundNuisances[background][region]['cuts'], 
                'type'    : normBackgroundNuisances[background][region]['type'],
            }
            if 'kind' in normBackgroundNuisances[background][region]:
                nuisances[nuisancename]['kind'] = normBackgroundNuisances[background][region]['kind']
            scalefactorFromData = normBackgroundNuisances[background][region]['scalefactorFromData']  

        if scalefactorFromData: # Remove gloabl lnN uncertainties for backgrounds normalized on data
            for globalNuisance in globalNuisances: 
                if background in nuisances[globalNuisance]['samples']:
                    del nuisances[globalNuisance]['samples'][background]

### shapes

# lepton reco, id, iso, fastsim

for scalefactor in leptonSF:

    nuisances[scalefactor]  = {
        'name'  : scalefactor+year,
        'samples'  : { },
    }
    nuisances[scalefactor]['type'] = leptonSF[scalefactor]['type']   
    if leptonSF[scalefactor]['type']=='shape':
        nuisances[scalefactor]['kind'] = 'weight'   
    for sample in samples.keys():
        if not samples[sample]['isDATA']:
            if 'FS' not in scalefactor or samples[sample]['isFastsim']:
                if ('nanoAODv6' not in opt.samplesFile and 'EOY' not in sample and (not samples[sample]['isFastsim'] or 'SigV6' not in opt.tag )) or 'Extra' not in scalefactor:
                    nuisances[scalefactor]['samples'][sample] = leptonSF[scalefactor]['weight']

# b-tagging scale factors

btagWeight1tagSyst = btagWeight1tag if 'TrigBTag' not in opt.tag else btagWeight1tag.replace('*triggerWeightBTag', '') # Bleah!!!
bSelections = { '1b' : { 'weight' : btagWeight1tagSyst+'_syst/'+btagWeight1tagSyst,
                         'cuts'   : [ '_Tag', 'SS_', 'Fake', 'ttZ', '1tag', '2tag' ] },
                '0b' : { 'weight' : '(1.-'+btagWeight1tagSyst+'_syst)/(1.-'+btagWeight1tagSyst+')',
                         'cuts'   : [ '_Veto', 'SSV_', '_NoTag', 'WZ_', 'WZtoWW_', 'ZZ', 'Zpeak' ] },
               }

for scalefactor in bTagNuisances:
    for bsel in bSelections:
        nuisances[scalefactor+bsel]  = {
            'name'  : bTagNuisances[scalefactor]['name'].replace('_yeartag', year),
            'samples'  : { },
            'kind'  : 'weight',
            'type'  : 'shape',
            'cuts'  : [ ]           
        }
        bselweight = bSelections[bsel]['weight']
        scafactvar = bTagNuisances[scalefactor]['var']
        for sample in samples.keys():
            if not samples[sample]['isDATA']:
                if 'FS' not in scalefactor or samples[sample]['isFastsim']:
                    if ('EOY' not in sample and not samples[sample]['isFastsim']) or scalefactor!='btagcor': 
                        nuisances[scalefactor+bsel]['samples'][sample] = [ bselweight.replace('syst', scafactvar.replace('VAR', 'up'  )),
                                                                           bselweight.replace('syst', scafactvar.replace('VAR', 'down')) ]
        for cut in cuts.keys():
            for bselcut in bSelections[bsel]['cuts']:
                if bselcut in cut:
                    nuisances[scalefactor+bsel]['cuts'].append(cut)
                    break

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

if '2016' in opt.tag or '2017' in opt.tag: 
    nuisances['prefiring']  = {
        'name'  : 'prefiring'+year, 
        'samples'  : { },
        'kind'  : 'weight',
        'type'  : 'shape',
    }
    for sample in samples.keys():
        if not samples[sample]['isDATA']:
            nuisances['prefiring']['samples'][sample] = [ 'PrefireWeight_Up/PrefireWeight', 'PrefireWeight_Down/PrefireWeight' ] 

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

if 'ttbar' in samples:
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

mt2llRegions = [ ]
for cut in cuts:
    ptmissCut = cut.split('_')[0]+'_'
    if ('SR' in ptmissCut or 'VR1' in ptmissCut) and ptmissCut not in mt2llRegions:
        mt2llRegions.append(ptmissCut)

# mt2ll top and WW

addMT2Shapes = 'SignalRegions' in opt.tag

if addMT2Shapes:

    mt2llweightUp = '(1. - 0.75*(mt2ll'+ctrltag+'>=370))'
    mt2llweightDo = '1.'

    nuisancekey = 'WZbin'
    nuisances[nuisancekey]  = {
        'name'  : nuisancekey+year.replace('noHIPM','').replace('HIPM',''),
        'samples'  : { 'WZ' : [ mt2llweightUp, mt2llweightDo] },
        'OneSided' : True,
        'kind'  : 'weight',
        'type'  : 'shape'
    }

    mt2llweightUp = '(1. + 0.2*(mt2ll>=100.)*(mt2ll<160.) + 0.4*(mt2ll>=160.)*(mt2ll<240.) + 0.5*(mt2ll>=240))'
    mt2llweightDo = '1.'

    for mt2llregion in mt2llRegions:
        if 'VR1' in mt2llregion: continue

        if isShape or hasattr(opt, 'groups') or hasattr(opt,'skipLNN') or '_WWShapeCorr' not in opt.tag:

            nuisancekey = 'WWshape_'+mt2llregion
            nuisances[nuisancekey]  = {
                'name'  : nuisancekey+year.replace('noHIPM','').replace('HIPM',''),
                'samples'  : { 'ttbar' : [ mt2llweightUp, mt2llweightDo],
                               'STtW'  : [ mt2llweightUp, mt2llweightDo],
                               'WW'    : [ mt2llweightUp, mt2llweightDo] },
                'OneSided' : True,
                'kind'  : 'weight',
                'type'  : 'shape',
                'cuts'  : [ ]
            } 

            for cut in cuts.keys():
                if mt2llregion in cut:
                    nuisances[nuisancekey]['cuts'].append(cut)

        if isShape or hasattr(opt, 'groups') or hasattr(opt,'skipLNN') or '_WWShapeCorr' in opt.tag:

            binList = []
            if 'Stop' in opt.tag: binList.extend([ 'Bin6', 'Bin7' ])
            elif 'Merge' not in opt.tag: binList.extend([ 'Bin6', 'Bin7', 'Bin8' , 'Bin9' ])
            else: 
                if 'SR1' in mt2llregion: binList.extend([ 'Bin6', 'Bin7' ])
                elif 'SR2' in mt2llregion: binList.extend([ 'Bin6', 'Bin7', 'Bin8' ])
                elif 'SR3' in mt2llregion: binList.extend([ 'Bin6', 'Bin7', 'Bin8' ])
                elif 'SR4' in mt2llregion: binList.extend([ 'Bin6', 'Bin7', 'Bin8', 'Bin9' ])

            for ibin in binList:
                nuisancekey = 'WWshape_'+ibin+'_'+mt2llregion
                nuisances[nuisancekey]  = {
                    'name'  : nuisancekey+year.replace('noHIPM','').replace('HIPM',''),
                    'samples'  : { 'ttbar' : [ mt2llweightUp, mt2llweightDo],
                                   'STtW'  : [ mt2llweightUp, mt2llweightDo],
                                   'WW'    : [ mt2llweightUp, mt2llweightDo] },
                    'OneSided' : True,
                    'kind'  : 'weight',
                    'type'  : 'shape',
                    'cuts'  : [ ]
                }

                for cut in cuts.keys():
                    if mt2llregion in cut:
                        nuisances[nuisancekey]['cuts'].append(cut)

# mt2ll top and WW SUS-17-010 style
#mt2llBins = [ ]
#mt2llNuisances = False
#if not isDatacardOrPlot or mt2llNuisances:
#    if 'Optim' not in opt.tag or 'MT2' not in opt.tag:
#        mt2llBins = ['Bin4', 'Bin5', 'Bin6', 'Bin7']
#        mt2llEdges = ['60.', '80.', '100.', '120.', '999999999.']
#        mt2llSystematics = [0.05, 0.10, 0.20, 0.30]
#    elif 'High' in opt.tag and 'Extra' in opt.tag:
#        mt2llBins = ['Bin6', 'Bin7', 'Bin8', 'Bin9' ]
#        mt2llEdges = ['100.', '160.', '240.', '370.', '999999999.']
#        mt2llSystematics = [0.20, 0.30, 0.30, 0.30] # placeholders    
#    elif 'High' in opt.tag:
#        mt2llBins = ['Bin6', 'Bin7', 'Bin8' ]     
#        mt2llEdges = ['100.', '160.', '370.', '999999999.']
#        mt2llSystematics = [0.20, 0.30, 0.30] # placeholders     
#    else:
#        mt2llBins = ['Bin6', 'Bin7' ]
#        mt2llEdges = ['100.', '160.', '999999999.']
#        mt2llSystematics = [0.20, 0.30] # placeholders            
#
#for mt2llregion in mt2llRegions: 
#    if 'VR1' in mt2llregion: continue
#    for mt2llbin in range(len(mt2llBins)):
#
#        mt2llsystname = mt2llregion + mt2llBins[mt2llbin]
#        mt2llweightUp = '(mt2ll>='+mt2llEdges[mt2llbin]+' && mt2ll<'+mt2llEdges[mt2llbin+1]+') ? '+str(1.+mt2llSystematics[mt2llbin])+' : 1.'  
#        mt2llweightDo = '(mt2ll>='+mt2llEdges[mt2llbin]+' && mt2ll<'+mt2llEdges[mt2llbin+1]+') ? '+str(1.-mt2llSystematics[mt2llbin])+' : 1.'  
#        
#        nuisances['Top_'+mt2llsystname]  = {
#            'name'  : 'Top_'+mt2llsystname+year,
#            'samples'  : { 
#                'ttbar' : [ mt2llweightUp, mt2llweightDo],
#                'STtW'  : [ mt2llweightUp, mt2llweightDo],
#                'tW'    : [ mt2llweightUp, mt2llweightDo], # backward compatibility for background names
#            },
#            'kind'  : 'weight',
#            'type'  : 'shape',
#            'cuts'  : [ ]           
#        }
#        
#        nuisances['WW_'+mt2llsystname]  = {
#            'name'  : 'WW_'+mt2llsystname+year,
#            'samples'  : { 
#                'WW' : [ mt2llweightUp, mt2llweightDo],
#            },
#            'kind'  : 'weight',
#            'type'  : 'shape',
#            'cuts'  : [ ]           
#        }
#
#        for cut in cuts.keys():
#            if mt2llregion in cut:
#                nuisances['Top_'+mt2llsystname]['cuts'].append(cut)
#                nuisances['WW_' +mt2llsystname]['cuts'].append(cut)

# mt2ll DY (from control regions)
 
# mt2ll ZZ (from k-factors)

# mt2ll signal
if signalReco=='fast' and fastsimMetType!='reco': 
    if fastsimMetType=='average' or not isFillShape:
        nuisances['ptmissfastsim']  = {
            'name'  : 'ptmissfastsim', # mismodeling correlated through the years?
            'samples'  : { },
            'kind'  : 'tree',
            'type'  : 'shape',
            'folderUp':   directorySig.replace('__susyMT2fast', '__susyMT2reco'),
            'folderDown': directorySig.replace('__susyMT2fast', '__susyMT2genm').replace('Smear', 'Nomin'),
        }
        if fastsimMetType=='acceptance': nuisances['ptmissfastsim']['extremes'] = [ '_reco', '_gen' ]
        for sample in samples.keys():
            if samples[sample]['isFastsim']:
                nuisances['ptmissfastsim']['samples'][sample] = ['1.', '1.']

### QCD scale and PDFs

nuisances['qcdScale'] = {
    'name': 'qcdScale', # Scales correlated through the years?
    'kind': 'weight_envelope',
    'type': 'shape',
    'samples': { },
    'cuts' : [ ],
}

nuisances['pdf'] = {
    'name': 'pdf', # PDFs correlated through the years?
    'kind': 'weight_envelope',
    'type': 'shape',
    'samples': { },
    'cuts' : [ ],
}

for yeartomerge in yearstaglist:

    theoryRecoFlag = recoFlag+'SigV6' if ('SigV6' in opt.tag or 'EOY' in opt.sigset) else recoFlag
    exec(open('./Data/theoryNormalizations/theoryNormalizations'+theoryRecoFlag+'_'+yeartomerge+'.py').read())

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

    for sample in samples.keys():
        if not samples[sample]['isDATA']:
            if sample=='minor':
                nuisances['qcdScale']['samples'][sample] = []
                nuisances['pdf']['samples'][sample] = []
                continue
            elif sample not in theoryNormalizations:
                print 'Nuisance warning: sample', sample, 'not in theoryNormalizations'
                continue
            if theoryNormalizations[sample]['qcdScaleStatus']==3:
                qcdScaleVariations = [ ]
                for i in [0, 1, 3, 5, 7, 8]:
                    qcdScaleVariations.append('LHEScaleWeight['+str(i)+']/'+str(theoryNormalizations[sample]['qcdScale'][i]))
                nuisances['qcdScale']['samples'][sample] = qcdScaleVariations
            if not samples[sample]['isSignal'] and theoryNormalizations[sample]['pdfStatus']==3:
                pdfVariations = [ ] 
                for i in range(len(theoryNormalizations[sample]['pdf'])):                              
                    pdfVariations.append('LHEPdfWeight['+str(i)+']/'+str(theoryNormalizations[sample]['pdf'][i]))
                nuisances['pdf']['samples'][sample] = qcdScaleVariations

for cut in cuts: # TODO: Why only in the signal regions? 
    if 'SR' in cut.split('_')[0]: #or 'SM' in opt.sigset:
        nuisances['qcdScale']['cuts'].append(cut)
        nuisances['pdf']['cuts'].append(cut)

### JES, JER and MET

for treeNuisance in treeNuisances:

    for mcType in treeNuisanceDirs[treeNuisance]:
        if 'Down' not in treeNuisanceDirs[treeNuisance][mcType] or 'Up' not in treeNuisanceDirs[treeNuisance][mcType]:
            print 'nuisance warning: missing trees for', treeNuisance, mcType, 'variations'
        else:

            mcTypeName = '_FS' if (mcType=='Sig' and not treeNuisances[treeNuisance]['BkgToSig']) else ''
            yearCorr = '' if treeNuisances[treeNuisance]['year'] else year # not correlated through the years?

            nuisances[treeNuisance+mcType] = {
                'name': treeNuisance+mcTypeName+yearCorr, 
                'kind': 'tree',
                'type': 'shape',
                'OneSided' : treeNuisances[treeNuisance]['onesided'],
                'synchronized' : False,
                'samples': { },
                'folderDown': treeNuisanceDirs[treeNuisance][mcType]['Down'],
                'folderUp':   treeNuisanceDirs[treeNuisance][mcType]['Up'],
            }
            for sample in samples.keys():
                if not samples[sample]['isDATA'] and not ('NoDY' in opt.tag and treeNuisance=='jer' and '2017' in year and sample=='DY'):
                    if (mcType=='Bkg' and not samples[sample]['isSignal']) or (mcType=='Sig' and samples[sample]['isSignal']):
                        nuisances[treeNuisance+mcType]['samples'][sample] = ['1.', '1.']

            if len(nuisances[treeNuisance+mcType]['samples'].keys())==0:
                del nuisances[treeNuisance+mcType]

    if hasattr(opt, 'cardList') and treeNuisances[treeNuisance]['BkgToSig']:
        if treeNuisance+'Bkg' in nuisances and treeNuisance+'Sig' in nuisances:
            nuisances[treeNuisance+'Bkg']['samples'].update(nuisances[treeNuisance+'Sig']['samples']) 
            del nuisances[treeNuisance+'Sig']

### rate parameters
rateparameters = {
    'Topnorm' :  { 
        'samples' : [ 'ttbar', 'tW', 'STtW' ],
        'subcuts' : [ '' ],
    },
    'NoJetRate_JetBack' : {
        'samples' : [ 'ttbar', 'tW', 'STtW', 'ttW', 'ttZ' ],
        'subcuts' : [ '_NoJet_' ],
        'limits'  : '[0.5,1.5]',
    },
    'JetRate_JetBack' : {
        'samples'  : [ 'ttbar', 'tW', 'STtW', 'ttW', 'ttZ' ],
        'subcuts'  : [ '_NoTag_' ],
        'bondrate' : 'NoJetRate_JetBack',
    }
}
if '_NoWWRate' not in opt.tag: 
    rateparameters['WWnorm'] = {
        'samples' : [ 'WW' ],
        'subcuts' : [ '' ],
    }
    rateparameters['NoJetRate_DibosonBack'] = {
        'samples' : [ 'WW', 'WZ' ],
        'subcuts' : [ '_NoJet_' ],
        'limits'  : '[0.7,1.3]'
    }
    rateparameters['JetRate_DibosonBack'] = {
        'samples' : [ 'WW', 'WZ' ],
        'subcuts' : [ '_NoTag_' ],
        'bondrate' : 'NoJetRate_DibosonBack',
    }

if 'FitCR' in opt.tag:
    backgroundCRs = { 'ttZ' : { 'samples' : [ 'ttZ' ],
                                'regions' : { '_Tag_' : [ '_NoTag_', '_Veto_', '_Tag_' ] }, },
                      'WZ'  : { 'samples' : [ 'WZ' ],  
                                'regions' : { '_Veto_' : [ '_Veto_', '_Tag_' ] , '_NoTag_' : [ '_NoTag_', '_Tag_' ], '_NoJet_' : [ '_NoJet_' ] }, },
                      'ZZ'  : { 'samples' : [ 'ZZTo2L2Nu', 'ZZTo4L' ],
                                'regions' : { '_Veto_' : [ '_Veto_', '_Tag_' ] , '_NoTag_' : [ '_NoTag_', '_Tag_' ], '_NoJet_' : [ '_NoJet_' ] }, },
                    }
    for controlregion in backgroundCRs:
        for sample in backgroundCRs[controlregion]['samples']:
            for rateparam in rateparameters.keys():
                if sample in rateparameters[rateparam]['samples']: 
                    rateparameters[rateparam]['samples'].remove(sample)
        for region in backgroundCRs[controlregion]['regions']:
            useRegion = False
            for cut in cuts:
                if region in cut:
                    useRegion = True
                    continue
            if useRegion:
                rateparameters['CR'+region+controlregion] = { }
                rateparameters['CR'+region+controlregion]['samples'] = backgroundCRs[controlregion]['samples']
                rateparameters['CR'+region+controlregion]['subcuts'] = backgroundCRs[controlregion]['regions'][region]
                rateparameters['CR'+region+controlregion]['limits'] = '[0.3,1.7]'

if hasattr(opt, 'outputDirDatacard'):
    for mt2llregion in mt2llRegions: 
        for rateparam in rateparameters: 
            
            if 'CR_' in rateparam:
                useControlRegion = False            
                for cut in cuts:
                    if mt2llregion in cut and rateparam.split('_')[1]==cut.split('_')[1]:
                        useControlRegion = True
                        continue
                if not useControlRegion: continue

            rateparamname = rateparam + '_' + mt2llregion
            
            for sample in rateparameters[rateparam]['samples']:

                if sample not in samples: continue # backward compatibility for background names

                isControlSample = True if ('isControlSample' in samples[sample] and samples[sample]['isControlSample']==1) else False

                initialValue = '1.00' if 'initval' not in rateparameters[rateparam].keys() else rateparameters[rateparam]['initval']

                nuisances[sample+rateparamname]  = {
                    'name'  : rateparamname+year,
                    'samples'  : { sample : initialValue },
                    'type'  : 'rateParam',
                    'cuts'  : [ ] 
                }
                
                if 'limits' in rateparameters[rateparam].keys():
                    nuisances[sample+rateparamname]['limits'] = rateparameters[rateparam]['limits'] 
                    
                for cut in cuts.keys():
                    if (mt2llregion in cut and not isControlSample) or (mt2llregion.replace('SR', 'CR').replace('VR1', 'CR0') in cut and 'CR_' in rateparam and rateparam.split('_')[2]==cut.split('_')[2]):
                        for subcut in rateparameters[rateparam]['subcuts']:
                            if subcut in cut:
                                nuisances[sample+rateparamname]['cuts'].append(cut)
                        
                if 'bondrate' in rateparameters[rateparam].keys():
                                
                    fileIn = ROOT.TFile(opt.inputFile, "READ")

                    nuisances[sample+rateparamname]['bond'] = {}

                    for cut in nuisances[sample+rateparamname]['cuts']:

                        nuisances[sample+rateparamname]['bond'][cut] = {}

                        for variable in variables.keys():
                            if 'cuts' in variables[variable] and cut not in variables[variable]['cuts']: continue

                            histoB = fileIn.Get(cut+'/'+variable+'/histo_'+sample)
                            cutB = rateparameters[rateparam]['subcuts'][0]
                            cutA = rateparameters[rateparameters[rateparam]['bondrate']]['subcuts'][0]
                            cutA = rateparameters[rateparameters[rateparam]['bondrate']]['subcuts'][0]
                            histoA = fileIn.Get(cut.replace(cutB, cutA)+'/'+variable+'/histo_'+sample)
                            yieldB = '%-.4f' % histoB.Integral()
                            yieldA = '%-.4f' % histoA.Integral()
            
                            bond_formula = '1+'+yieldA+'/'+yieldB+'*(1.-@0)' 
                            bond_parameters = rateparameters[rateparam]['bondrate']+'_'+mt2llregion+year
                            
                            nuisances[sample+rateparamname]['bond'][cut][variable] =  { bond_formula : bond_parameters }

                    fileIn.Close()

### Cleaning 

nuisanceToRemove = [ ]

for nuisance in nuisances:

    if 'cuts' in nuisances[nuisance]:
        if len(nuisances[nuisance]['cuts'])==0:
            nuisanceToRemove.append(nuisance)

    if nuisance!='stat' and nuisance not in nuisanceToRemove and 'samples' in nuisances[nuisance]:
        if len(nuisances[nuisance]['samples'])==0:
            nuisanceToRemove.append(nuisance)

    if '_noTreeNuisances' in opt.tag:
        if nuisance not in nuisanceToRemove and 'kind' in nuisances[nuisance] and nuisances[nuisance]['kind']=='tree':
            nuisanceToRemove.append(nuisance)

    if '_noShapeNuisances' in opt.tag:
        if nuisance not in nuisanceToRemove and 'type' in nuisances[nuisance] and nuisances[nuisance]['type']=='shape':
            nuisanceToRemove.append(nuisance)

    if '_nolnNNuisances' in opt.tag:
        if nuisance not in nuisanceToRemove and 'type' in nuisances[nuisance] and nuisances[nuisance]['type']=='lnN':
            nuisanceToRemove.append(nuisance)

for nuisance in nuisanceToRemove:
    del nuisances[nuisance]

### Nasty tricks ...

nuisanceToRemove = [ ]  

if 'SignalRegion' in opt.tag or 'ValidationRegion' in opt.tag or 'ttZNormalization' in opt.tag or 'SearchRegion' in opt.tag:

    if ('nanoAODv6' in opt.samplesFile and 'ctrl' in regionName and 'cern' in SITE): 
 
        if hasattr(opt, 'batchSplit'): # Remove only when running shapes, so can make shapes in gridui and plots+datacards in lxplus
            for nuisance in nuisances:
                if 'jesTotal' in nuisance or 'unclustEn' in nuisance: 
                    nuisanceToRemove.append(nuisance)
        
    if 'SignalRegion' not in opt.tag:
        for nuisance in nuisances:
            if nuisance!='stat' and 'norm' in nuisances[nuisance]['name']:
                nuisanceToRemove.append(nuisance)

else:

    for nuisance in nuisances:
        if nuisance!='stat' and 'lumi' not in nuisance: # example ...
            nuisanceToRemove.append(nuisance)

for nuisance in nuisanceToRemove:
    del nuisances[nuisance]

if len(yearstaglist)>1:
  
   nuisanceToRemove = [ ]

   for nuisance in nuisances:
       if 'WWshape' in nuisance or 'WZbin' in nuisance: continue
       if 'type' in nuisances[nuisance] and nuisances[nuisance]['type']=='shape':
           if year in nuisances[nuisance]['name']:
               nuisanceToRemove.append(nuisance)

   for nuisance in nuisanceToRemove:

       for ytag in yearstaglist:
           nuisances[nuisance+'_'+ytag] = nuisances[nuisance].copy()
           nuisances[nuisance+'_'+ytag]['name'] = nuisances[nuisance+'_'+ytag]['name'].replace(year, '_'+ytag)

       del nuisances[nuisance]


   #for nuisance in sorted (nuisances.keys()):
   #    print nuisance
   #    if nuisance!='stat':
   #       print '             ', nuisances[nuisance]['name']

   #exit()


