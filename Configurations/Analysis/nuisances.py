### nuisances = {}

# statistical uncertainty

nuisances['stat']  = { 'type'          : 'auto', # Use the following if you want to apply the automatic combine MC stat nuisances.
                       'maxPoiss'      : '10',   # Number of threshold events for Poisson modelling
                       'includeSignal' : '1',    # Include MC stat nuisances on signal processes (1=True, 0=False)
                       'samples'       : {}
                      }

if 'Templates' in opt.tag:

    # pileup
    if 'pileup' in systematicNuisances:
        nuisances['pileup']  = { 'name'  : 'pileup',
                                 'samples'  : { },
                                 'kind'  : 'weight',
                                 'type'  : 'shape'
                                }

        for sample in samples.keys():
            if not samples[sample]['isDATA']:
                nuisances['pileup']['samples'][sample] = [ 'pileupWeight[2]/pileupWeight[1]', 'pileupWeight[0]/pileupWeight[1]' ]

    # b specific nuisances
    if 'bjets' in samples:

        # gluon splitting
        if 'gluonSplitting' in systematicNuisances:
            nuisances['gluonSplitting']  = { 'name'  : 'gluonSplitting',
                                             'samples'  : { 'bjets' : [ '1.5*'+isGluonSplitting+'+(!('+isGluonSplitting+'))', '0.5*'+isGluonSplitting+'+(!('+isGluonSplitting+'))' ] },
                                             'kind'  : 'weight',
                                             'type'  : 'shape'
                                            }

        # b hadron fragmentation
        if 'bfragmentation' in systematicNuisances:
            nuisances['bfragmentation']  = { 'name'  : 'bfragmentation',
                                             'samples'  : { 'bjets' : [ 'bHadronWeight[2]/bHadronWeight[1]', 'bHadronWeight[0]/bHadronWeight[1]' ] },
                                             'kind'  : 'weight',
                                             'type'  : 'shape'
                                            }

        # b semileptonic decays' br
        if 'bdecay' in systematicNuisances:
            nuisances['bdecay']  = { 'name'  : 'bdecay',
                                     'samples'  : { 'bjets' : [ 'bHadronWeight[4]', 'bHadronWeight[3]' ] },
                                     'kind'  : 'weight',
                                     'type'  : 'shape'
                                    }

    # ptrel specific nuisances
    if 'PtRel' in opt.method:

        # light specific nuisances
        if 'ljets' in samples and 'lightCharmRatio' in systematicNuisances:

            # light to charm ratio
            if 'ForFit' not in opt.tag:

                nuisances['lightCharmRatio'] = { 'name'  : 'lightCharmRatio',
                                                 'samples'  : { 'ljets' : '1.3', },
                                                 'type'  : 'lnN'
                                                }

            elif '2D' in opt.tag: 

                nuisances['lightCharmRatio'] = { 'name'  : 'lightCharmRatio',
                                                 'samples'  : { 'ljets' : [ '1.', '1.' ] },
                                                 'type'  : 'shape',
                                                 'kind'  : 'weight'
                                                }

        # nuisances for PtRel fits
        if 'ForFit' in opt.tag:

            # JEU
            if  '_nojeu' not in opt.tag:

                nuisances['JEU']  = { 'name'  : 'JEU',
                                      'samples'  : { },
                                      'cuts'  : [],
                                      'kind'  : 'weight',
                                      'type'  : 'shape'
                                     }

                for sample in samples.keys():
                    if not samples[sample]['isDATA']:
                        nuisances['JEU']['samples'][sample] = [ 1., 1. ]

                for cut in cuts:
                    if len(cut.split('_'))==3 or (len(cut.split('_'))==4 and ('Corr' in cut.split('_')[3] or cut.split('_')[3].replace('Up','').replace('Down','') in systematicNuisances)):
                        nuisances['JEU']['cuts'].append(cut)

            # template corrections
            for nuisance in templateCorrectionNuisances:

                nuisances[nuisance]  = { 'name'  : nuisance,
                                         'samples'  : { templateCorrectionNuisances[nuisance] : [ 1., 1. ] },
                                         'kind'  : 'weight',
                                         'type'  : 'shape'
                                        }

            # decouple nuisances in simultaneous fits to all selections 
            if '_mergedSelections' in opt.tag and '_nuisSelections' in opt.tag:
                for selection in systematicVariations:
                    nuisance = selection.replace('Up','').replace('Down','')
                    if nuisance in nuisances and nuisance in systematicNuisances:
                        nuisances[nuisance]['cuts'] = []
                        for cut in cuts:
                            if nuisance not in cut:
                                nuisances[nuisance]['cuts'].append(cut)
                        
            # rate parameters
            for cut in cuts:
                for sample in samples:
                    if not samples[sample]['isDATA']:

                        if sample=='bjets' and '_nobRP' in opt.tag: continue

                        nuisances[sample+'_'+cut]  = { 'name'    : sample+'_'+cut,
                                                       'type'    : 'rateParam',
                                                       'samples' : { sample : '1.' },
                                                       'cuts'    : [ cut ]
                                                      }

                        if 'AwayJet888' not in cut or 'Pass' in cut or not samples[sample]['isSignal'] or '_NoAwayJetBond' in opt.tag:
   
                            nuisances[sample+'_'+cut]['limits'] = '[0.01,20]'

                        else:

                            fileIn = ROOT.TFile(opt.inputFile, 'READ')

                            nuisances[sample+'_'+cut]['bond'] = {}
                            nuisances[sample+'_'+cut]['bond'][cut] = {}

                            for variable in variables:
                                if 'cuts' not in variables[variable] or cut in variables[variable]['cuts']:

                                    awayJetFailCut   = cut
                                    awayJetPassCut   = cut.replace('Fail','Pass')
                                    muonJetFailCut   = cut.replace('_AwayJetUp','').replace('_AwayJetDown','')
                                    muonJetPassCut   = muonJetFailCut.replace('Fail','Pass')

                                    awayJetFailHisto = fileIn.Get(awayJetFailCut+'/'+variable+'/histo_'+sample)
                                    awayJetPassHisto = fileIn.Get(awayJetPassCut+'/'+variable+'/histo_'+sample)
                                    muonJetFailHisto = fileIn.Get(muonJetFailCut+'/'+variable+'/histo_'+sample)   
                                    muonJetPassHisto = fileIn.Get(muonJetPassCut+'/'+variable+'/histo_'+sample)                            

                                    awayJetFailYield = awayJetFailHisto.Integral()
                                    awayJetPassYield = awayJetPassHisto.Integral()
                                    muonJetFailYield = muonJetFailHisto.Integral()
                                    muonJetPassYield = muonJetPassHisto.Integral()
  
                                    awayJetFailRelativeYield = awayJetFailYield/(awayJetFailYield+awayJetPassYield)
                                    awayJetPassRelativeYield = awayJetPassYield/(awayJetFailYield+awayJetPassYield)
                                    muonJetFailRelativeYield = muonJetFailYield/(muonJetFailYield+muonJetPassYield)
                                    muonJetPassRelativeYield = muonJetPassYield/(muonJetFailYield+muonJetPassYield)
 
                                    differencePassRelativeYields = str(muonJetPassRelativeYield-awayJetPassRelativeYield)
                                    muonJetFailFactor = '(@1/@0)*'+str(muonJetFailRelativeYield)
                                    awayJetFailFactor = '@2/'+str(awayJetFailRelativeYield)

                                    bond_formula = '(('+differencePassRelativeYields+'+'+muonJetFailFactor+')*'+awayJetFailFactor+') '
                                    bond_parameters = ','.join([ sample+'_'+muonJetPassCut, sample+'_'+muonJetFailCut, sample+'_'+awayJetPassCut  ])

                                    nuisances[sample+'_'+cut]['bond'][cut][variable] = { bond_formula : bond_parameters }

                            fileIn.Close()


