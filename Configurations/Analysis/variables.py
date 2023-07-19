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

if 'WorkingPoints' in opt.tag:

    discriminantDone = []

    for btagwp in bTagWorkingPoints:
        if bTagWorkingPoints[btagwp]['discriminant'] not in discriminantDone:

            for ijet in range(20): # Bleah!!!!
                for flv in [ '0', '5' ]:
 
                    goodJet = '(('+str(ijet)+'<nJet)*(Alt$(Jet_pT['+str(ijet)+'],0.)>=30.)*(abs(Alt$(Jet_eta['+str(ijet)+'],5.))<'+maxJetEta+')*(Alt$(Jet_hadronFlavour['+str(ijet)+'],-1)=='+flv+')*(Alt$(Jet_tightID['+str(ijet)+'],0)==1))'
                    jetDisc = '(999999.*(!('+goodJet+')) + '+goodJet+'*(Alt$(Jet_'+bTagWorkingPoints[btagwp]['discriminant']+'['+str(ijet)+'],999999.)))'         
         
                    variable = 'Jet_'+bTagWorkingPoints[btagwp]['discriminant']+'_'+flv+'_'+str(ijet)
                    variables[variable]  = { 'name'  : jetDisc,     
                                             'range' : (11000, 0., 1.1),              
                                             'xaxis' : 'Jet '+bTagWorkingPoints[btagwp]['discriminant']   
                                            }
                   
            discriminantDone.append(bTagWorkingPoints[btagwp]['discriminant'])

