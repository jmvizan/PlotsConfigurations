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

btagAlgo = 'btagDeepB'
bTagPtCut  = '20.'
bTagEtaMax = '2.4' if ('2016' in opt.tag) else '2.5'
bTagCut = '0.6321'
btagWP  = '2016M'
if '2017' in opt.tag: 
    bTagCut = '0.4941'
    btagWP  = '2017M'
if '2018' in opt.tag: 
    bTagCut = '0.4184'
    btagWP  = '2018M'
nbjets = 'Sum$(CleanJet_pt>='+bTagPtCut+' && abs(CleanJet_eta)<'+bTagEtaMax+' && Jet_'+btagAlgo+'[CleanJet_jetIdx]>='+bTagCut+')'

# variables = {}

if 'Test' in opt.tag: 
    
    variables['nbjets']        = {  'name'  : nbjets,                    #   variable name    
                                    'range' : (  3,    0.,     3.),      #   variable range
                                    'xaxis' : 'number of b-tagged jets', #   x axis name
                                    'fold'  : 1                          #   fold overflow
                                }

if 'HighPtMissOptimisationRegion' in opt.tag: 
    
    variables['ptmissmt2ll']      = {  'name'  : 'ptmiss:mt2ll',                                             #   variable name    
                                       'range' : ([   0.,   10.,   20.,   30.,   40.,   50.,   60.,   70.,   80., 90.,  100.,  110.,  120.,  130.,  140.,  150.,  160.,  170., 180.,  190.,  200.,  210.,  220.,  230.,  240.,  250.,  260., 270.,  280.,  290.,  300.,  310.,  320.,  330.,  340.,  350., 360.,  370.,  380.,  390.,  400.,  410.,  420.,  430.,  440., 450.,  460.,  470.,  480.,  490.,  500.,  510.,  520.,  530.,  540.,  550.,  560.,  570.,  580.,  590.,  600.,  610.,  620., 630.,  640.,  650.,  660.,  670.,  680.,  690.,  700.,  710.,  720.,  730.,  740.,  750.,  760.,  770.,  780.,  790.,  800., 810.,  820.,  830.,  840.,  850.,  860.,  870.,  880.,  890.,  900.,  910.,  920.,  930.,  940.,  950.,  960.,  970.,  980., 990., 1000.],[   0.,   20.,   40.,   60.,   80.,  100.,  120.,  140.,  160.,  180.,  200.,  220.,  240.,  260.,  280.,  300.,  320.,  340.,  360.,  380.,  400.,  420.,  440.,  460.,  480.,  500.,  520.,   540.,  560.,  580.,  600.,  620.,  640.,  660.,  680.,  700.,  720.,  740.,  760.,  780.,  800.,  820.,  840.,  860.,  880.,  900.,  920.,  940.,  960.,  980., 1000., 1020., 1040., 1060.,  1080., 1100., 1120., 1140., 1160., 1180., 1200., 1220., 1240.,  1260., 1280., 1300., 1320., 1340., 1360., 1380., 1400., 1420.,  1440., 1460., 1480., 1500., 1520., 1540., 1560., 1580., 1600.,  1620., 1640., 1660., 1680., 1700., 1720., 1740., 1760., 1780.,  1800., 1820., 1840., 1860., 1880., 1900., 1920., 1940., 1960., 1980., 2000.]),  #   variable range
                                    'xaxis' : '2D #ptmiss:MT2',                                                      #   x axis name
                                    'fold'  : 1                                                                  #   fold overflow
                                    }
    variables['mt2ll']      = {  'name'  : 'mt2ll',                                             #   variable name    
                                     'range' : ([   0.,   10.,   20.,   30.,   40.,   50.,   60.,   70.,   80., 90.,  100.,  110.,  120.,  130.,  140.,  150.,  160.,  170., 180.,  190.,  200.,  210.,  220.,  230.,  240.,  250.,  260., 270.,  280.,  290.,  300.,  310.,  320.,  330.,  340.,  350., 360.,  370.,  380.,  390.,  400.,  410.,  420.,  430.,  440., 450.,  460.,  470.,  480.,  490.,  500.,  510.,  520.,  530.,  540.,  550.,  560.,  570.,  580.,  590.,  600.,  610.,  620., 630.,  640.,  650.,  660.,  670.,  680.,  690.,  700.,  710.,  720.,  730.,  740.,  750.,  760.,  770.,  780.,  790.,  800., 810.,  820.,  830.,  840.,  850.,  860.,  870.,  880.,  890.,  900.,  910.,  920.,  930.,  940.,  950.,  960.,  970.,  980., 990., 1000.],[1]),  #   variable range
                                    'xaxis' : 'MT2ll',                                                      #   x axis name
                                    'fold'  : 1                                                                  #   fold overflow
                                    }
    variables['ptmiss']      = {  'name'  : 'ptmiss',                                             #   variable name    
                                     'range' : ([   0.,   20.,   40.,   60.,   80.,  100.,  120.,  140.,  160.,  180.,  200.,  220.,  240.,  260.,  280.,  300.,  320.,  340.,  360.,  380.,  400.,  420.,  440.,  460.,  480.,  500.,  520.,   540.,  560.,  580.,  600.,  620.,  640.,  660.,  680.,  700.,  720.,  740.,  760.,  780.,  800.,  820.,  840.,  860.,  880.,  900.,  920.,  940.,  960.,  980., 1000., 1020., 1040., 1060.,  1080., 1100., 1120., 1140., 1160., 1180., 1200., 1220., 1240.,  1260., 1280., 1300., 1320., 1340., 1360., 1380., 1400., 1420.,  1440., 1460., 1480., 1500., 1520., 1540., 1560., 1580., 1600.,  1620., 1640., 1660., 1680., 1700., 1720., 1740., 1760., 1780.,  1800., 1820., 1840., 1860., 1880., 1900., 1920., 1940., 1960., 1980., 2000.],[1]),  #   variable range
                                    'xaxis' : 'ptmiss',                                                      #   x axis name
                                    'fold'  : 1                                                                  #   fold overflow
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
    
    variables['Lep1pt']        = {   'name'  : 'Lepton_pt[0]',               #   variable name    
                                     'range' : (  40,    0.,  200.),         #   variable range
                                     'xaxis' : 'leading lepton ' + pt + gv,  #   x axis name
                                     'fold'  : 1                             #   fold overflow
                                 }
    
    variables['Lep2pt']        = {   'name'  : 'Lepton_pt[1]',               #   variable name    
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

        T0 = '(Lepton_isTightElectron_cutBasedMediumPOG[0]+Lepton_isTightMuon_mediumRelIsoTight[0])'
        T1 = '(Lepton_isTightElectron_cutBasedMediumPOG[1]+Lepton_isTightMuon_mediumRelIsoTight[1])'
        T2 = '(Lepton_isTightElectron_cutBasedMediumPOG[2]+Lepton_isTightMuon_mediumRelIsoTight[2])'
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

    elif "Optim" in opt.tag and "MT2" in opt.tag:

        variables['mt2ll']         = {   'name'  : mt2ll,                  #   variable name    
                                         'range' : ([0, 20, 40, 60, 80, 100, 160, 220],[1]), # variable range
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
 
        visht = 'Lepton_pt[0]+Lepton_pt[1]+Sum$(CleanJet_pt)'
        
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
        
        variables['sumLepPt']      = {   'name'  : 'Lepton_pt[0]+Lepton_pt[1]', #   variable name    
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

            variables['deltaPhiLep']   = {  'name'  : 'acos(cos(Lepton_phi[1]-Lepton_phi[0]))', #   variable name    
                                            'range' : (  10,    0.,  3.2),     #   variable range
                                            'xaxis' : dphill,                  #   x axis name
                                            'fold'  : 1                        #   fold overflow
                                         }

            pxll = '(Lepton_pt[0]*cos(Lepton_phi[0])+Lepton_pt[1]*cos(Lepton_phi[1]))'
            pyll = '(Lepton_pt[0]*sin(Lepton_phi[0])+Lepton_pt[1]*sin(Lepton_phi[1]))'
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
