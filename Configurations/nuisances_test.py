"""
# lnN

nuisances['lumiMoriond17']  = {
    'name'  : 'lumiMoriond17', 
    'samples'  : {
        #https://twiki.cern.ch/twiki/bin/view/CMS/TWikiLUM#CurRec
        'T'                             : '1.025',
        #'03_ZZ'                            : '1.025',
        '04_TTTo2L2Nu'                     : '1.025',
        '06_WW'                            : '1.025',
        '05_ST'                            : '1.025',
        '09_TTW'                           : '1.025',
        #'10_TTZ'                           : '1.025',
        #'07_ZJetsHT_DYcorr'                : '1.025',
        #'02_WZTo3LNu'                      : '1.025',
        '11_HWW'                           : '1.025',
        '13_VVV'                           : '1.025',
        },
    'type'  : 'lnN',
    }

nuisances['normWZ']  = {
    'name'  : 'normWZ', 
    'samples'  : {
        '02_WZTo3LNu'                      : '1.09', # 0.97 +/- 0.09
        },
    'type'  : 'lnN',
    }

nuisances['normTTZ']  = {
    'name'  : 'normTTZ', 
    'samples'  : {
        '10_TTZ'                           : '1.25', # 1.44 +/- 0.36
        },
    'type'  : 'lnN',
    'type'  : 'lnN',
    }

nuisances['normZZnojet']  = {
    'name'  : 'normZZnojet', 
    'samples'  : {
        '03_ZZ'                            : '1.26', # 0.74 +/- 0.19
        },
    'cuts'  : {
        'NoJet' : '1.00',
        },
    'type'  : 'lnN',
    }

nuisances['normZZjet']  = {
    'name'  : 'normZZjet', 
    'samples'  : {
        '03_ZZ'                            : '1.14', # 1.21 +/- 0.17
        },
    'cuts'  : {
        'Tag'   : '1.00',
        'NoTag' : '1.00',
        },
    'type'  : 'lnN',
    }

nuisances['normZZveto']  = {
    'name'  : 'normZZveto', 
    'samples'  : {
        '03_ZZ'                            : '1.12', # 1.06 +/- 0.12
        },
    'cuts'  : {
        'Veto' : '1.00',
        },
    'type'  : 'lnN',
    }

nuisances['normDY']  = {
    'name'  : 'normDY', 
    'samples'  : {
        '07_ZJetsHT_DYcorr'                         : '1.32',
        },
    'cuts'  : {
        'Veto'  : '1.00',
        'NoTag' : '1.00',
        'Tag'   : '1.00',
        },
    'type'  : 'lnN',
    }

nuisances['DYshape']  = {
    'name'  : 'DYshape', 
    'samples'  : {
        '07_ZJetsHT_DYcorr'                         : '1.',
        },
    'cuts'  : {
        'Veto'  : '1.00',
        'NoTag' : '1.00',
        'NoJet' : '1.00',
        'Tag'   : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['ZZshape']  = {
    'name'  : 'ZZshape', 
    'samples'  : {
        '03_ZZ'                                    : '1.',
        },
    'cuts'  : {
        'Veto' : '1.00',
        'NoJet' : '1.00',
        'NoTag' : '1.00',
        'Tag' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['DYnojet']  = {
    'name'  : 'DYnojet', 
    'samples'  : {
        '07_ZJetsHT_DYcorr'                         : '4.',
        },
    'cuts'  : {
        'NoJet' : '1.00',
        },
    'type'  : 'lnN',
    }

nuisances['normTTbar']  = {
    'name'  : 'normTTbar', 
    'samples'  : {
        '04_TTTo2L2Nu'                     : '1.1',
        },
    'type'  : 'lnN',
    }

#nuisances['normWW']  = {
#    'name'  : 'normWW', 
#    'samples'  : {
#        '06_WW'                            : '1.1',
#        },
#    'type'  : 'lnN',
#    }

nuisances['normTW']  = {
    'name'  : 'normTW', 
    'samples'  : {
        '05_ST'                            : '1.1',
        },
    'type'  : 'lnN',
    }

nuisances['normTTW']  = {
    'name'  : 'normTTW', 
    'samples'  : {
        '09_TTW'                           : '1.5',
        },
    'type'  : 'lnN',
    }

nuisances['normHWW']  = {
    'name'  : 'normHWW', 
    'samples'  : {
        '11_HWW'                           : '1.5',
        },
    'type'  : 'lnN',
    }

nuisances['normVVV']  = {
    'name'  : 'normVVV', 
    'samples'  : {
        '13_VVV'                           : '1.5',
        },
    'type'  : 'lnN',
    }

# Shape

nuisances['Reco']  = {
    'name'  : 'Reco', 
    'samples'  : {
        'T'                             : '1.',
        '03_ZZ'                            : '1.',
        '04_TTTo2L2Nu'                     : '1.',
        '06_WW'                            : '1.',
        '05_ST'                            : '1.',
        '09_TTW'                           : '1.',
        '10_TTZ'                          : '1.',
        '07_ZJetsHT_DYcorr'                         : '1.',
        '02_WZTo3LNu'                      : '1.',
        '11_HWW'                           : '1.',
        '13_VVV'                           : '1.',
        },
    'type'  : 'shape',
    }

nuisances['Idiso']  = {
    'name'  : 'Idiso', 
    'samples'  : {
        'T'                             : '1.',
        '03_ZZ'                            : '1.',
        '04_TTTo2L2Nu'                     : '1.',
        '06_WW'                            : '1.',
        '05_ST'                            : '1.',
        '09_TTW'                           : '1.',
        '10_TTZ'                          : '1.',
        '07_ZJetsHT_DYcorr'                         : '1.',
        '02_WZTo3LNu'                      : '1.',
        '11_HWW'                           : '1.',
        '13_VVV'                           : '1.',
        },
    'type'  : 'shape',
    }

#nuisances['Idisoele']  = {
#    'name'  : 'Idisoele', 
#    'samples'  : {
#        'T'                             : '1.',
#        '03_ZZ'                            : '1.',
#        '04_TTTo2L2Nu'                     : '1.',
#        '06_WW'                            : '1.',
#        '05_ST'                            : '1.',
#        '09_TTW'                           : '1.',
#        '10_TTZ'                          : '1.',
#        '07_ZJetsHT_DYcorr'                         : '1.',
#        '02_WZTo3LNu'                      : '1.',
#        '11_HWW'                           : '1.',
#        '13_VVV'                           : '1.',
#        },
#    'type'  : 'shape',
#    }

#nuisances['Idisomu']  = {
#    'name'  : 'Idisomu', 
#    'samples'  : {
#        'T'                             : '1.',
#        '03_ZZ'                            : '1.',
#        '04_TTTo2L2Nu'                     : '1.',
#        '06_WW'                            : '1.',
#        '05_ST'                            : '1.',
#        '09_TTW'                           : '1.',
#        '10_TTZ'                          : '1.',
#        '07_ZJetsHT_DYcorr'                         : '1.',
#        '02_WZTo3LNu'                      : '1.',
#        '11_HWW'                           : '1.',
#        '13_VVV'                           : '1.',
#        },
#    'type'  : 'shape',
#    }

nuisances['Fastsim']  = {
    'name'  : 'Fastsim', 
    'samples'  : {
        'T'                             : '1.',
        },
    'type'  : 'shape',
    }

#nuisances['Trigger']  = {
#    'name'  : 'Trigger', 
#    'samples'  : {
#        'T'                             : '1.',
#        '03_ZZ'                            : '1.',
#        '04_TTTo2L2Nu'                     : '1.',
#        '06_WW'                            : '1.',
#        '05_ST'                            : '1.',
#        '09_TTW'                           : '1.',
#        '10_TTZ'                          : '1.',
#        '07_ZJetsHT_DYcorr'                         : '1.',
#        '02_WZTo3LNu'                      : '1.',
#        '11_HWW'                           : '1.',
#        '13_VVV'                           : '1.',
#        },
#    'type'  : 'shape',
#    }

nuisances['Trigger']  = {
    'name'  : 'Trigger', 
    'samples'  : {
        'T'                             : '1.02',
        #'03_ZZ'                            : '1.02',
        '04_TTTo2L2Nu'                     : '1.02',
        '06_WW'                            : '1.02',
        '05_ST'                            : '1.02',
        '09_TTW'                           : '1.02',
        #'10_TTZ'                           : '1.02',
        #'07_ZJetsHT_DYcorr'                         : '1.02',
        #'02_WZTo3LNu'                      : '1.02',
        '11_HWW'                           : '1.02',
        '13_VVV'                           : '1.02',
        },
    'type'  : 'lnN',
    }

nuisances['Btag']  = {
    'name'  : 'Btag', 
    'samples'  : {
        'T'                             : '1.',
        '03_ZZ'                            : '1.',
        '04_TTTo2L2Nu'                     : '1.',
        '06_WW'                            : '1.',
        '05_ST'                            : '1.',
        '09_TTW'                           : '1.',
        '10_TTZ'                          : '1.',
        '07_ZJetsHT_DYcorr'                         : '1.',
        '02_WZTo3LNu'                      : '1.',
        '11_HWW'                           : '1.',
        '13_VVV'                           : '1.',
        },
    'type'  : 'shape',
    }

nuisances['BtagFS']  = {
    'name'  : 'BtagFS', 
    'samples'  : {
        'T'                             : '1.',
        },
    'type'  : 'shape',
    }

nuisances['Pileup']  = {
    'name'  : 'Pileup', 
    'samples'  : {
        'T'                             : '1.',
        },
    'type'  : 'shape',
    }

nuisances['Metfastsim']  = {
    'name'  : 'Metfastsim', 
    'samples'  : {
        'T'                             : '1.',
        },
    'type'  : 'shape',
    }

nuisances['Isrnjet']  = {
    'name'  : 'Isrnjet', 
    'samples'  : {
        'T'                             : '1.',
        },
    'type'  : 'shape',
    }

nuisances['JES']  = {
    'name'  : 'JES', 
    'samples'  : {
        'T'                             : '1.',
        '03_ZZ'                            : '1.',
        '04_TTTo2L2Nu'                     : '1.',
        '06_WW'                            : '1.',
        '05_ST'                            : '1.',
        '09_TTW'                           : '1.',
        '10_TTZ'                           : '1.',
        '07_ZJetsHT_DYcorr'                         : '1.',
        '02_WZTo3LNu'                      : '1.',
        '11_HWW'                           : '1.',
        '13_VVV'                           : '1.',
        },
    'type'  : 'shape',
    }

nuisances['MET']  = {
    'name'  : 'MET', 
    'samples'  : {
        'T'                             : '1.',
        '03_ZZ'                            : '1.',
        '04_TTTo2L2Nu'                     : '1.',
        '06_WW'                            : '1.',
        '05_ST'                            : '1.',
        '09_TTW'                           : '1.',
        '10_TTZ'                           : '1.',
        '07_ZJetsHT_DYcorr'                         : '1.',
        '02_WZTo3LNu'                      : '1.',
        '11_HWW'                           : '1.',
        '13_VVV'                           : '1.',
        },
    'type'  : 'shape',
    }

#

nuisances['Q2']  = {
    'name'  : 'Q2', 
    'samples'  : {
        '03_ZZ'                            : '1.',
        '04_TTTo2L2Nu'                     : '1.',
        '06_WW'                            : '1.',
        #'05_ST'                            : '1.',
        '09_TTW'                           : '1.',
        '10_TTZ'                           : '1.',
        '07_ZJetsHT_DYcorr'                       : '1.',
        '02_WZTo3LNu'                      : '1.',
        '11_HWW'                           : '1.',
        '13_VVV'                           : '1.',
        },
    'type'  : 'shape',
    }

nuisances['PDF']  = {
    'name'  : 'PDF', 
    'samples'  : {
        '03_ZZ'                            : '1.',
        '04_TTTo2L2Nu'                     : '1.',
        '06_WW'                            : '1.',
        #'05_ST'                            : '1.',
        '09_TTW'                           : '1.',
        '10_TTZ'                           : '1.',
        '07_ZJetsHT_DYcorr'                       : '1.',
        '02_WZTo3LNu'                      : '1.',
        '11_HWW'                           : '1.',
        '13_VVV'                           : '1.',
        },
    'type'  : 'shape',
    }



#

nuisances['Toppt']  = {
    'name'  : 'Toppt', 
    'samples'  : {
        '04_TTTo2L2Nu'                      : '1.',
        },
    'type'  : 'shape',
    }

nuisances['Fake']  = {
    'name'  : 'Fake', 
    'samples'  : {
        '03_ZZ'                            : '1.',
        '04_TTTo2L2Nu'                     : '1.',
        '06_WW'                            : '1.',
        '05_ST'                            : '1.',
        '09_TTW'                           : '1.',
        '10_TTZ'                           : '1.',
        '07_ZJetsHT_DYcorr'                       : '1.',
        '02_WZTo3LNu'                      : '1.',
        '11_HWW'                           : '1.',
        '13_VVV'                           : '1.',
        },
    'type'  : 'shape',
    }
"""
# Stat

nuisances['stat']  = {
    # apply to the following samples: name of samples here must match keys in samples.py
    'samples'  : {
        
        'T'            : {
            'typeStat' : 'bbb',
            },
        
        '04_TTTo2L2Nu': {
            'typeStat' : 'bbb',
            },  
        '05_ST': {
            'typeStat' : 'bbb',
            },  
        '06_WW': {
            'typeStat' : 'bbb',
            }, 
        '03_ZZ': {
            'typeStat' : 'bbb',
            },
        '09_TTW': {
            'typeStat' : 'bbb',
            }, 
        '10_TTZ': {
            'typeStat' : 'bbb',
            },  
        '07_ZJetsHT_DYcorr': {
            'typeStat' : 'bbb',
            }, 
        '02_WZTo3LNu': {
            'typeStat' : 'bbb',
            },  
        '11_HWW': {
            'typeStat' : 'bbb',
            },   
        '13_VVV': {
            'typeStat' : 'bbb',
            },                                
        },
    'type'  : 'shape'
    }

# MT2ll correlate regions
"""
nuisances['MT2llBinWWSR1']  = {
    'name'  : 'MT2llBinWWSR1',  
    'samples'  : {
        '06_WW' : '1.00',
        },
    'cuts'  : {
        'SR1_' : {'Bin4': '0.05', 'Bin5': '0.10', 'Bin6': '0.20', 'Bin7': '0.30', },
        },
    'type'  : 'shape',
    }

nuisances['MT2llBinWWSR2']  = {
    'name'  : 'MT2llBinWWSR2',  
    'samples'  : {
        '06_WW' : '1.00',
        },
    'cuts'  : {
        'SR2_' : {'Bin4': '0.05', 'Bin5': '0.10', 'Bin6': '0.20', 'Bin7': '0.30', },
        },
    'type'  : 'shape',
    }

nuisances['MT2llBinWWSR3']  = {
    'name'  : 'MT2llBinWWSR3',  
    'samples'  : {
        '06_WW' : '1.00',
        },
    'cuts'  : {
        'SR3_' : {'Bin4': '0.05', 'Bin5': '0.10', 'Bin6': '0.20', 'Bin7': '0.30', },
        },
    'type'  : 'shape',
    }

nuisances['MT2llBinTopSR1']  = {
    'name'  : 'MT2llBinTopSR1',  
    'samples'  : {
        '04_TTTo2L2Nu' : '1.00',
        '05_ST' : '1.00',
        },
    'cuts'  : {
        'SR1_' : {'Bin4': '0.05', 'Bin5': '0.10', 'Bin6': '0.20', 'Bin7': '0.30', },
        },
    'type'  : 'shape',
    }

nuisances['MT2llBinTopSR2']  = {
    'name'  : 'MT2llBinTopSR2',  
    'samples'  : {
        '04_TTTo2L2Nu' : '1.00',
        '05_ST' : '1.00',
        },
    'cuts'  : {
        'SR2_' : {'Bin4': '0.05', 'Bin5': '0.10', 'Bin6': '0.20', 'Bin7': '0.30', },
        },
    'type'  : 'shape',
    }

nuisances['MT2llBinTopSR3']  = {
    'name'  : 'MT2llBinTopSR3',  
    'samples'  : {
        '04_TTTo2L2Nu' : '1.00',
        '05_ST' : '1.00',
        },
    'cuts'  : {
        'SR3_' : {'Bin4': '0.05', 'Bin5': '0.10', 'Bin6': '0.20', 'Bin7': '0.30', },
        },
    'type'  : 'shape',
    }
"""

# rateParam ttbar

nuisances['Topnorm_SR1']  = {
    'name'  : 'Topnorm_SR1',
    'samples'  : {
        '04_TTTo2L2Nu' : '1.00',
        '05_ST' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR1_Tag' : '1.00',
        'SR1_Veto' : '1.00',
        'SR1_NoTag' : '1.00',
        'SR1_NoJet' : '1.00',
        },
    }

nuisances['Topnorm_SR2']  = {
    'name'  : 'Topnorm_SR2',
    'samples'  : {
        '04_TTTo2L2Nu' : '1.00',
        '05_ST' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR2_Tag' : '1.00',
        'SR2_Veto' : '1.00',
        'SR2_NoTag' : '1.00',
        'SR2_NoJet' : '1.00',
        },
    }

nuisances['Topnorm_SR3']  = {
    'name'  : 'Topnorm_SR3',
    'samples'  : {
        '04_TTTo2L2Nu' : '1.00',
        '05_ST' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR3_Tag' : '1.00',
        'SR3_Veto' : '1.00',
        'SR3_NoTag' : '1.00',
        'SR3_NoJet' : '1.00',
        },
    }

# rateParam WW

nuisances['WWnorm_SR1']  = {
    'name'  : 'WWnorm_SR1',
    'samples'  : {
        '06_WW' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR1_Tag' : '1.00',
        'SR1_Veto' : '1.00',
        'SR1_NoTag' : '1.00',
        'SR1_NoJet' : '1.00',
        },
    }

nuisances['WWnorm_SR2']  = {
    'name'  : 'WWnorm_SR2',
    'samples'  : {
        '06_WW' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR2_Tag' : '1.00',
        'SR2_Veto' : '1.00',
        'SR2_NoTag' : '1.00',
        'SR2_NoJet' : '1.00',
        },
    }

nuisances['WWnorm_SR3']  = {
    'name'  : 'WWnorm_SR3',
    'samples'  : {
        '06_WW' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR3_Tag' : '1.00',
        'SR3_Veto' : '1.00',
        'SR3_NoTag' : '1.00',
        'SR3_NoJet' : '1.00',
        },
    }

# Specific for 3Reg 

# SR1
nuisances['JetRate_JetBack_SR1']  = {
    'name'  : 'JetRate_JetBack_SR1',
    'samples'  : {
        '04_TTTo2L2Nu'                    : '1.',
        '05_ST'                           : '1.',
        '09_TTW'                          : '1.',
        '10_TTZ'                          : '1.',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR1_NoTag' : '1.00',
        },
    }

nuisances['JetRate_DibosonBack_SR1']  = {
    'name'  : 'JetRate_DibosonBack_SR1',
    'samples'  : {
        '06_WW'                            : '1.',
        '02_WZTo3LNu'                      : '1.',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR1_NoTag' : '1.00',
        },
    }

nuisances['NoJetRate_JetBack_SR1']  = {
    'name'  : 'NoJetRate_JetBack_SR1',
    'samples'  : {
        '04_TTTo2L2Nu'                    : '1.',
        '05_ST'                           : '1.',
        '09_TTW'                          : '1.',
        '10_TTZ'                          : '1.',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR1_NoJet' : '1.00',
        },
    }

nuisances['NoJetRate_DibosonBack_SR1']  = {
    'name'  : 'NoJetRate_DibosonBack_SR1',
    'samples'  : {
        '06_WW'                            : '1.',
        '02_WZTo3LNu'                      : '1.',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR1_NoJet' : '1.00',
        },
    }

#SR2
nuisances['JetRate_JetBack_SR2']  = {
    'name'  : 'JetRate_JetBack_SR2',
    'samples'  : {
        '04_TTTo2L2Nu'                    : '1.',
        '05_ST'                           : '1.',
        '09_TTW'                          : '1.',
        '10_TTZ'                          : '1.',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR2_NoTag' : '1.00',
        },
    }

nuisances['JetRate_DibosonBack_SR2']  = {
    'name'  : 'JetRate_DibosonBack_SR2',
    'samples'  : {
        '06_WW'                            : '1.',
        '02_WZTo3LNu'                      : '1.',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR2_NoTag' : '1.00',
        },
    }

nuisances['NoJetRate_JetBack_SR2']  = {
    'name'  : 'NoJetRate_JetBack_SR2',
    'samples'  : {
        '04_TTTo2L2Nu'                    : '1.',
        '05_ST'                           : '1.',
        '09_TTW'                          : '1.',
        '10_TTZ'                          : '1.',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR2_NoJet' : '1.00',
        },
    }

nuisances['NoJetRate_DibosonBack_SR2']  = {
    'name'  : 'NoJetRate_DibosonBack_SR2',
    'samples'  : {
        '06_WW'                            : '1.',
        '02_WZTo3LNu'                      : '1.',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR2_NoJet' : '1.00',
        },
    }

#SR3
nuisances['JetRate_JetBack_SR3']  = {
    'name'  : 'JetRate_JetBack_SR3',
    'samples'  : {
        '04_TTTo2L2Nu'                    : '1.',
        '05_ST'                           : '1.',
        '09_TTW'                          : '1.',
        '10_TTZ'                          : '1.',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR3_NoTag' : '1.00',
        },
    }

nuisances['JetRate_DibosonBack_SR3']  = {
    'name'  : 'JetRate_DibosonBack_SR3',
    'samples'  : {
        '06_WW'                            : '1.',
        '02_WZTo3LNu'                      : '1.',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR3_NoTag' : '1.00',
        },
    }

nuisances['NoJetRate_JetBack_SR3']  = {
    'name'  : 'NoJetRate_JetBack_SR3',
    'samples'  : {
        '04_TTTo2L2Nu'                    : '1.',
        '05_ST'                           : '1.',
        '09_TTW'                          : '1.',
        '10_TTZ'                          : '1.',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR3_NoJet' : '1.00',
        },
    }

nuisances['NoJetRate_DibosonBack_SR3']  = {
    'name'  : 'NoJetRate_DibosonBack_SR3',
    'samples'  : {
        '06_WW'                            : '1.',
        '02_WZTo3LNu'                      : '1.',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR3_NoJet' : '1.00',
        },
    }



