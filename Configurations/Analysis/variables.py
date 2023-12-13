# variables = {}

# Flags  
gv    = ' [GeV]'
pt    = '#font[50]{p}_{T}'
met   = pt+'^{miss}'
ptrel = pt+'^{rel}'
sll   = '#font[12]{ll}'
pll   = '('+sll+')'
mt2   = '#font[50]{m}_{T2}'
ptll  = pt+'^{'+sll+'}'

if hasattr(opt, 'batchQueue') and not hasattr(opt, 'dryRun'): ## mkShape
    overflow  = 1
    underflow = 2
else: ## mkShapeMulti
    overflow  = 2
    underflow = 1

jetEtaBins = ( int(2*float(maxJetEta)/0.1) , -float(maxJetEta), float(maxJetEta) )
# This does not work in python3
#jetEta2DBins = [ -float(maxJetEta)+edge*0.1 for edge in range(int(2*float(maxJetEta)/0.1)+1) ]
jetEta2DBins = [ edge*0.1 for edge in range(int(-float(maxJetEta)/0.1), int(float(maxJetEta)/0.1)+1) ]

if 'WorkingPoints' in opt.tag:

    discriminantDone = []

    for btagwp in bTagWorkingPoints:
        if bTagWorkingPoints[btagwp]['discriminant'] not in discriminantDone:

            discriminantBins = (20000, 0., 20.) if 'JBP' in btagwp else (11000, 0., 1.1)

            for ijet in range(nJetMax): # Bleah!!!!
                for flv in [ '0', '5' ]:
         
                    variable = 'Jet_'+bTagWorkingPoints[btagwp]['discriminant']+'_'+flv+'_'+str(ijet)
                    variables[variable]  = { 'name'  : jetDisc.replace('JETIDX', str(ijet)).replace('BTAGDISC',bTagWorkingPoints[btagwp]['discriminant']).replace('JETFLV',flv),     
                                             'range' : discriminantBins,              
                                             'xaxis' : 'Jet '+bTagWorkingPoints[btagwp]['discriminant']   
                                            }
                   
            discriminantDone.append(bTagWorkingPoints[btagwp]['discriminant'])

elif 'DataKinematics' in opt.tag:

    muJetPtBins  = ( int(maxJetPt-minJetPt), minJetPt, maxJetPt)

    variables['mujetpt']         = { 'name'  : muJetPt,
                                     'range' : muJetPtBins,
                                     'xaxis' : '#mu-jet '+pt+gv,
                                     'fold'  : overflow
                                    }

elif opt.method+'Kinematics' in opt.tag:

    variables['mujeteta']        = { 'name'  : muJetEta,
                                     'range' : jetEtaBins,
                                     'xaxis' : '#mu-jet pseudorapodity',
                                    }

    variables['muonpt']          = { 'name'  : muPt,
                                     'range' : (25, 5., 30.),
                                     'xaxis' : '#mu '+pt+gv,
                                     'fold'  : overflow
                                    }

    variables['PV']              = { 'name'  : 'npvsGood',
                                     'range' : (50, 0., 50.),
                                     'xaxis' : 'number of good PVs',
                                     'fold'  : overflow
                                    }

    for cut in cuts:

        jetPtMin, jetPtMax = float(jetPtBins[cut][0]), float(jetPtBins[cut][1])
        muJetPtBins  = ( int(jetPtMax-jetPtMin), jetPtMin, jetPtMax )

        muJetPt2DBins = [ ]
        for edge in range(int(jetPtMin), int(jetPtMax)+1):
            muJetPt2DBins.append(edge)

        variables['mujetpt_'+cut]         = { 'name'  : muJetPt,
                                              'range' : muJetPtBins,
                                              'xaxis' : '#mu-jet '+pt+gv,
                                              'cuts'  : [ cut ]
                                              }

        variables['mujetpteta_'+cut]      = { 'name'  : muJetEta+':'+muJetPt,
                                              'range' : (muJetPt2DBins, jetEta2DBins),
                                              'xaxis' : '2D #mu-jet eta:'+pt,
                                              'cuts'  : [ cut ]
                                             }

elif opt.method+'Templates' in opt.tag:

    if opt.method=='PtRel':

        if 'ForFit' in opt.tag:

            variables['ptrel'] = { 'name'  : muPtRel,
                                   'range' : ptrelRange,
                                   'xaxis' : '#mu-jet '+ptrel+gv,
                                   'fold'  : overflow
                                  }

        else:

            for btagwp in bTagWorkingPoints:
                for btagselection in [ 'Pass', 'Fail' ]:

                    variableName = '_'.join([ 'ptrel', btagwp, btagselection ])
                    discCut  = 'Jet_'+bTagWorkingPoints[btagwp]['discriminant']+'['+muJetIdx+']>='+bTagWorkingPoints[btagwp]['cut']
                    if btagselection=='Fail': discCut = discCut.replace('>=', '<')

                    variables[variableName] = { 'name'  : muPtRel,
                                                'range' : ptrelRange,
                                                'xaxis' : '#mu-jet '+ptrel+gv,
                                                'weight': discCut,
                                                'fold'  : overflow
                                               }

    elif opt.method=='System8':

        variables['ptrel'] = { 'name'  : muPtRel,
                               'range' : ptrelRange,
                               'xaxis' : '#mu-jet '+ptrel+gv,
                               'fold'  : overflow
                              }

        for btagwp in bTagWorkingPoints:

            variableName = '_'.join([ 'ptrel', btagwp ])
            discCut  = 'Jet_'+bTagWorkingPoints[btagwp]['discriminant']+'['+muJetIdx+']>='+bTagWorkingPoints[btagwp]['cut']

            variables[variableName] = { 'name'  : muPtRel,
                                        'range' : ptrelRange,
                                        'xaxis' : '#mu-jet '+ptrel+gv,
                                        'weight': discCut,
                                        'fold'  : overflow
                                       }

elif 'Light' in opt.tag:

    for cut in cuts:

        ptbin = cut
        lightJetWeight  = cuts[cut]['lightJetWeight']
        cutNLightTrkJet = cuts[cut]['cutNLightTrkJet']

        if 'LightKinematics' in opt.tag:

            jetPtMin, jetPtMax = float(jetPtBins[ptbin][0]), float(jetPtBins[ptbin][1])
            lightJetPtBins  = ( int(jetPtMax-jetPtMin), jetPtMin, jetPtMax )

            lightJetPt2DBins = [ edge for edge in range(int(jetPtMin), int(jetPtMax)+1) ]

            jetMax = 1 if 'MergedLight' in opt.tag else nJetMax

            for ijet in range(jetMax): # Bleah!!!!

                jetFlag = '_'+str(ijet) if 'MergedLight' not in opt.tag else ''
                jetKinWeight = jetKinematicWeight.replace('JETIDX',str(ijet))
                jetWeight = jetKinWeight+'*'+lightJetSel.replace('JETIDX',str(ijet)).replace('PTMIN',jetPtBins[ptbin][0]).replace('PTMAX',jetPtBins[ptbin][1])+'*'+lightJetWeight.replace('JETIDX',str(ijet))+'*('+cutNLightTrkJet.replace('JETIDX',str(ijet))+'>=1)'

                cutLightJetEta = lightJetEta.replace('JETIDX',str(ijet))
                cutLightJetPt  = lightJetPt.replace( 'JETIDX',str(ijet))

                variables['lightjeteta_'+cut+jetFlag] = { 'name'  : cutLightJetEta,
                                                          'range' : jetEtaBins,
                                                          'xaxis' : 'light jet pseudorapodity',
                                                          'weight': jetWeight,
                                                          'cuts'  : [ cut ],
                                                         }

                variables['lightjetpt_'+cut+jetFlag]    = { 'name'  : cutLightJetPt,
                                                            'range' : lightJetPtBins,
                                                            'xaxis' : 'light jet '+pt+gv,
                                                            'cuts'  : [ cut ],
                                                            'weight': jetWeight
                                                           }

                variables['lightjetpteta_'+cut+jetFlag] = { 'name'  : cutLightJetEta+':'+cutLightJetPt,
                                                            'range' : (lightJetPt2DBins, jetEta2DBins),
                                                            'xaxis' : '2D light jet eta:'+pt,
                                                            'cuts'  : [ cut ],
                                                            'weight': jetWeight
                                                           }

        elif 'LightTemplates' in opt.tag:

            cutLightTrkJetSel = cuts[cut]['cutLightTrkJetSel']
            trkMax = 1 if 'MergedLight' in opt.tag else nLightTrkMax

            for itrk in range(trkMax): # Re-Bleah!!!!

                trkFlag = '_'+str(itrk) if 'MergedLight' not in opt.tag else ''
                jetKinWeight = jetKinematicWeight.replace('JETIDX',trackJetIdx+'['+str(itrk)+']')
                jetWeight = jetKinWeight+'*'+lightJetSel.replace('JETIDX',trackJetIdx+'['+str(itrk)+']').replace('PTMIN',jetPtBins[ptbin][0]).replace('PTMAX',jetPtBins[ptbin][1])+'*'+lightJetWeight.replace('JETIDX',trackJetIdx+'['+str(itrk)+']')+'*('+cutNLightTrkJet.replace('JETIDX',trackJetIdx+'['+str(itrk)+']')+'>=1)'
                trkWeight = jetWeight+'*'+cutLightTrkJetSel.replace('TRKIDX',str(itrk)).replace('JETIDX',trackJetIdx+'['+str(itrk)+']')+'/'+cutNLightTrkJet.replace('JETIDX',trackJetIdx+'['+str(itrk)+']')
                
                variables['ptrel_'+cut+trkFlag] = { 'name'  : lightTrkPtRel.replace('TRKIDX',str(itrk)),
                                                    'range' : ptrelRange,
                                                    'xaxis' : 'light jet '+ptrel+gv,
                                                    'weight': trkWeight,
                                                    'cuts'  : [ cut ],
                                                    'fold'  : overflow
                                                   }

