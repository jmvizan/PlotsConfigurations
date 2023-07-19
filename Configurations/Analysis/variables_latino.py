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

if 'DataKinematics' in opt.tag: 

    muJetPtBins  = ( int(maxJetPt-minJetPt), minJetPt, maxJetPt)

    variables['mujetpt']         = { 'name'  : 'muJet_pt',
                                     'range' : muJetPtBins,
                                     'xaxis' : '#mu-jet '+pt+gv,
                                     'fold'  : overflow
                                    }

elif opt.method+'Kinematics' in opt.tag:

    muJetEtaBins = ( int(2*float(maxJetEta)/0.1) , -float(maxJetEta), float(maxJetEta))
    
    muJetEta2DBins = [ ]
    for edge in range(int(2*float(maxJetEta)/0.1)+1):
        muJetEta2DBins.append(-float(maxJetEta)+edge*0.1)

    variables['mujeteta']        = { 'name'  : 'muJet_eta',
                                     'range' : muJetEtaBins,
                                     'xaxis' : '#mu-jet pseudorapodity',
                                    }

    variables['muonpt']          = { 'name'  : 'Muon_pt[muJet_muon]',
                                     'range' : (25, 5., 30.),
                                     'xaxis' : '#mu '+pt+gv,
                                     'fold'  : overflow
                                    }

    variables['PV']              = { 'name'  : 'PV_npvsGood',
                                     'range' : (50, 0., 50.),
                                     'xaxis' : 'nPV',
                                     'fold'  : overflow
                                    } 

    for cut in cuts:

        jetPtMin, jetPtMax = float(jetPtBins[cut][0]), float(jetPtBins[cut][1])
        muJetPtBins  = ( int(jetPtMax-jetPtMin), jetPtMin, jetPtMax)

        muJetPt2DBins = [ ]
        for edge in range(int(jetPtMin), int(jetPtMax)+1):
            muJetPt2DBins.append(edge)

        variables['mujetpt_'+cut]         = { 'name'  : 'muJet_pt',
                                              'range' : muJetPtBins,
                                              'xaxis' : '#mu-jet '+pt+gv,
                                              'fold'  : overflow,
                                              'cuts'  : [ cut ]
                                              }

        variables['mujetpteta_'+cut]      = { 'name'  : 'muJet_eta:muJet_pt',                                                
                                              'range' : (muJetPt2DBins, muJetEta2DBins),
                                              'xaxis' : '2D #mu-jet eta:'+pt,   
                                              'fold'  : overflow,
                                              'cuts'  : [ cut ]          
                                             }

elif opt.method+'Templates' in opt.tag:

        ptrelRange = (50, 0., 4.) if opt.method=='PtRel' else (70, 0., 7.)

        variables['ptrel']       = { 'name'  : 'muJet_ptrel',
                                     'range' : ptrelRange,
                                     'xaxis' : '#mu-jet '+ptrel+gv,
                                     'fold'  : overflow
                                    }


