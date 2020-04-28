# variables
    
# Flags  
gv   = ' [GeV]'
pt   = '#font[50]{p}_{T}'
met  = pt+'^{miss}'
sll  = '#font[12]{ll}'
pll  = '('+sll+')'
mt2  = '#font[50]{m}_{T2}'
ptll = pt+'^{'+sll+'}'
dphill = '#Delta#phi(lep1,lep2)'

# Complex variables

sumLeptonPt = 'Lepton_pt['+lep0idx+']+Lepton_pt['+lep1idx+']'

nbjets = 'Sum$(CleanJet_pt>='+bTagPtCut+' && abs(CleanJet_eta)<'+bTagEtaMax+' && Jet_'+btagAlgo+'[CleanJet_jetIdx]>='+bTagCut+')'

# variables = {}

if 'Test' in opt.tag: 
    
    variables['nbjets']        = {  'name'  : nbjets,                    #   variable name    
                                    'range' : (  3,    0.,     3.),      #   variable range
                                    'xaxis' : 'number of b-tagged jets', #   x axis name
                                    'fold'  : 1                          #   fold overflow
                                }

if 'btagefficiencies' in opt.tag: 
    
    variables['jetpteta']      = {  'name'  : 'abs(Jet_eta):Jet_pt',                                             #   variable name    
                                    'range' : ([20, 30, 40, 50, 60, 70, 80, 100, 120, 150, 200, 250, 400, 1000],[0.,0.2,0.4,0.8,1.2,1.6,2.0,2.5]),  #   variable range
                                    'xaxis' : '2D eta:#pt',                                                      #   x axis name
                                    'fold'  : 1                                                                  #   fold overflow
                                    }
                                   
    variables['jetpt']  = { 'name'  : 'Jet_pt',                              #   variable name    
                            'range' : ([20, 30, 40, 50, 60, 70, 80, 100, 120, 150, 200, 250, 400, 1000],[1]), #   variable range
                            'xaxis' : 'jet'+pt+gv,                           #   x axis name
                            'fold'  : 1                                      #   fold overflow
                            } 
    
    variables['jeteta'] = { 'name'  : 'abs(Jet_eta)',              #   variable name    
                            'range' : ([0.,0.2,0.4,0.8,1.2,1.6,2.0,2.5],[1]),  #   variable range
                            'xaxis' : 'jet pseudorapodity',        #   x axis name
                            } 
                            
if 'Preselection' in opt.tag or 'ControlRegion' in opt.tag or 'Baseline' in opt.tag or 'TwoLeptons' in opt.tag:

    variables['ptmiss']        = {  'name'  : 'ptmiss',                #   variable name    
                                    'range' : (  40,    0.,  400.),    #   variable range
                                    'xaxis' : met + gv,                #   x axis name
                                    'fold'  : 1                        #   fold overflow
                                }
    
    variables['njets']         = {  'name'  : 'nCleanJet',             #   variable name    
                                    'range' : (  6,    0.,     6.),    #   variable range
                                    'xaxis' : 'number of jets',        #   x axis name
                                    'fold'  : 1                        #   fold overflow
                                }
    
    variables['nbjets']        = {  'name'  : nbjets,                    #   variable name    
                                    'range' : (  3,    0.,     3.),      #   variable range
                                    'xaxis' : 'number of b-tagged jets', #   x axis name
                                    'fold'  : 1                          #   fold overflow
                                }
    
    variables['mt2ll']         = {   'name'  : 'mt2ll',                #   variable name    
                                     'range' : (  20,    0.,  200.),   #   variable range
                                     'xaxis' : mt2 + pll + gv,         #   x axis name
                                     'fold'  : 1                       #   fold overflow
                                 }
    
    variables['jetpt']         = {   'name'  : 'CleanJet_pt',          #   variable name    
                                     'range' : (  40,    0.,  200.),   #   variable range
                                     'xaxis' : 'jet ' + pt + gv,       #   x axis name
                                     'fold'  : 1                       #   fold overflow
                                 }
    
    variables['Lep1pt']        = {   'name'  : 'Lepton_pt['+lep0idx+']',     #   variable name    
                                     'range' : (  40,    0.,  200.),         #   variable range
                                     'xaxis' : 'leading lepton ' + pt + gv,  #   x axis name
                                     'fold'  : 1                             #   fold overflow
                                 }
    
    variables['Lep2pt']        = {   'name'  : 'Lepton_pt['+lep1idx+']',     #   variable name    
                                     'range' : (  40,    0.,  200.),         #   variable range
                                     'xaxis' : 'trailing lepton ' + pt + gv, #   x axis name
                                     'fold'  : 1                             #   fold overflow
                                 }

    if 'TwoLeptons' in opt.tag:
    
        variables['mll']         = {   'name'  : 'mll',                #   variable name    
                                       'range' : ( 100,    0.,  200.), #   variable range
                                       'xaxis' : 'm' + pll + gv,       #   x axis name
                                       'fold'  : 1                     #   fold overflow
                                   }

if 'Validation' in opt.tag or 'Signal' in opt.tag:

    mt2ll = 'mt2ll'

    if 'FakeValidationRegion' in opt.tag:
        mt2ll = T0+'*mt2llfake0+'+T1+'*mt2llfake1+'+T2+'*mt2llfake2'

    if 'StudyHighMT2' in opt.tag:
 
        variables['mt2ll']         = {   'name'  : mt2ll,                  #   variable name    
                                         'range' : (  40,    0.,  800.),   # variable range
                                         'xaxis' : mt2 + pll + gv,         #   x axis name
                                         'fold'  : 1                       #   fold overflow
                                     }

    elif 'HighMT2' in opt.tag:

        variables['mt2ll']         = {   'name'  : mt2ll,                  #   variable name    
                                         'range' : ([0, 20, 40, 60, 80, 100, 120, 250 , 450, 650],[1]), # variable range
                                         'xaxis' : mt2 + pll + gv,         #   x axis name
                                         'fold'  : 1                       #   fold overflow
                                     }

    else:
    
        variables['mt2ll']         = {   'name'  : mt2ll,                  #   variable name    
                                         'range' : (   7,    0.,  140.),   #   variable range
                                         'xaxis' : mt2 + pll + gv,         #   x axis name
                                         'fold'  : 1                       #   fold overflow
                                     }

    if 'StudyVisHT' in opt.tag:
 
        visht = sumLeptonPt+'+Sum$(CleanJet_pt)'
        
        variables['visht']         = {   'name'  : visht,                  #   variable name    
                                         'range' : ( 120,    0., 3000.),   #   variable range
                                         'xaxis' : 'visht' + gv,           #   x axis name
                                         'fold'  : 1                       #   fold overflow
                                     }
        
        variables['ht']            = {   'name'  : 'Sum$(CleanJet_pt)',    #   variable name    
                                         'range' : ( 120,    0., 3000.),   #   variable range
                                         'xaxis' : 'ht' + gv,              #   x axis name
                                         'fold'  : 1                       #   fold overflow
                                     }
        
        variables['sumLepPt']      = {   'name'  : sumLeptonPt,            #   variable name    
                                         'range' : ( 120,    0., 3000.),   #   variable range
                                         'xaxis' : 'sumleppt' + gv,        #   x axis name
                                         'fold'  : 1                       #   fold overflow
                                     }
    
        variables['njets']         = {  'name'  : 'nCleanJet',             #   variable name    
                                        'range' : (  6,    0.,     6.),    #   variable range
                                        'xaxis' : 'number of jets',        #   x axis name
                                        'fold'  : 1                        #   fold overflow
                                    }

    if 'ttZValidationRegion' in opt.tag or 'ZZValidationRegion' in opt.tag or 'DYValidationRegion' in opt.tag: 

        variables['ptmiss']        = {  'name'  : 'ptmiss',                #   variable name    
                                        'range' : (  20,    0.,  400.),    #   variable range                             
                                        'xaxis' : met + gv,                #   x axis name
                                        'fold'  : 1                        #   fold overflow
                                     }

        if 'DYValidationRegion' in opt.tag:   

            variables['deltaPhiLep']   = {  'name'  : 'acos(cos(Lepton_phi['+lep1idx+']-Lepton_phi['+lep0idx+']))', #   variable name    
                                            'range' : (  10,    0.,  3.2),     #   variable range
                                            'xaxis' : dphill,                  #   x axis name
                                            'fold'  : 1                        #   fold overflow
                                         }

            pxll = '(Lepton_pt['+lep0idx+']*cos(Lepton_phi['+lep0idx+'])+Lepton_pt['+lep1idx+']*cos(Lepton_phi['+lep1idx+']))'
            pyll = '(Lepton_pt['+lep0idx+']*sin(Lepton_phi['+lep0idx+'])+Lepton_pt['+lep1idx+']*sin(Lepton_phi['+lep1idx+']))'
            pTll = 'sqrt('+pxll+'*'+pxll+'+'+pyll+'*'+pyll+')'

            variables['ptll']          = {  'name'  : pTll,                    #   variable name    
                                            'range' : ([20, 30, 40, 50, 60, 70, 80, 100, 120, 150, 200, 250, 300, 400, 500, 1000],[1]), #   variable range
                                            'xaxis' : ptll + gv,               #   x axis name
                                            'fold'  : 1                        #   fold overflow
                                         } 

        if 'ZZValidationRegion' in opt.tag: 
    
            variables['njets']         = {  'name'  : 'nCleanJet',             #   variable name    
                                            'range' : (  6,    0.,     6.),    #   variable range
                                            'xaxis' : 'number of jets',        #   x axis name
                                            'fold'  : 1                        #   fold overflow
                                         } 
    
            variables['jets']          = {  'name'  : 'nCleanJet>0',           #   variable name    
                                            'range' : (  2,    0.,     2.),    #   variable range
                                            'xaxis' : 'number of jets',        #   x axis name
                                            'fold'  : 1                        #   fold overflow
                                         }
