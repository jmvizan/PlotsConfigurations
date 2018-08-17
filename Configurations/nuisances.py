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
        '15_VZ3V'                           : '1.025',
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
        '07_ZJetsHT_DYcorr'                         : '2.',
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
        '15_VZ3V'                           : '1.5',
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
        '15_VZ3V'                           : '1.',
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
        '15_VZ3V'                           : '1.',
        },
    'type'  : 'shape',
    }
"""
nuisances['Idisoele']  = {
    'name'  : 'Idisoele', 
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
        '15_VZ3V'                           : '1.',
        },
    'type'  : 'shape',
    }

nuisances['Idisomu']  = {
    'name'  : 'Idisomu', 
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
        '15_VZ3V'                           : '1.',
        },
    'type'  : 'shape',
    }
"""
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
#        '15_VZ3V'                           : '1.',
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
        '15_VZ3V'                           : '1.02',
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
        '15_VZ3V'                           : '1.',
        },
    'type'  : 'shape',
    }

nuisances['Btaglight']  = {
    'name'  : 'Btaglight', 
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
        '15_VZ3V'                           : '1.',
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
        #'03_ZZ'                            : '1.',
        #'04_TTTo2L2Nu'                     : '1.',
        #'06_WW'                            : '1.',
        #'05_ST'                            : '1.',
        #'09_TTW'                           : '1.',
        #'10_TTZ'                          : '1.',
        #'07_ZJetsHT_DYcorr'                         : '1.',
        #'02_WZTo3LNu'                      : '1.',
        #'11_HWW'                           : '1.',
        #'15_VZ3V'                           : '1.',
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
        #'04_TTTo2L2Nu'                  : '1.',
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
        '15_VZ3V'                           : '1.',
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
        '15_VZ3V'                           : '1.',
        },
    'type'  : 'shape',
    }

#

nuisances['Q2']  = {
    'name'  : 'Q2', 
    'samples'  : {
        #'T'                             : '1.',
        '03_ZZ'                            : '1.',
        '04_TTTo2L2Nu'                     : '1.',
        '06_WW'                            : '1.',
        #'05_ST'                            : '1.',
        '09_TTW'                           : '1.',
        '10_TTZ'                           : '1.',
        '07_ZJetsHT_DYcorr'                       : '1.',
        '02_WZTo3LNu'                      : '1.',
        '11_HWW'                           : '1.',
        '15_VZ3V'                           : '1.',
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
        '15_VZ3V'                           : '1.',
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
        '15_VZ3V'                           : '1.',
        },
    'type'  : 'shape',
    }

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
        '15_VZ3V': {
            'typeStat' : 'bbb',
            },                                
        },
    'type'  : 'shape'
    }

# MT2ll correlate regions
"""
nuisances['MT2llBin4Top']  = {
    'name'  : 'MT2llBin4Top',  
    'samples'  : {
        '04_TTTo2L2Nu' : '0.05',
        '05_ST'        : '0.05',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin5Top']  = {
    'name'  : 'MT2llBin5Top',  
    'samples'  : {
        '04_TTTo2L2Nu' : '0.05',
        '05_ST'        : '0.05',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin6Top']  = {
    'name'  : 'MT2llBin6Top',  
    'samples'  : {
        '04_TTTo2L2Nu' : '0.05',
        '05_ST'        : '0.05',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin7Top']  = {
    'name'  : 'MT2llBin7Top',  
    'samples'  : {
        '04_TTTo2L2Nu' : '0.05',
        '05_ST'        : '0.05',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin4WW']  = {
    'name'  : 'MT2llBin4WW',  
    'samples'  : {
        '04_TTTo2L2Nu' : '0.05',
        '05_ST'        : '0.05',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin5WW']  = {
    'name'  : 'MT2llBin5WW',  
    'samples'  : {
        '04_TTTo2L2Nu' : '0.05',
        '05_ST'        : '0.05',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin6WW']  = {
    'name'  : 'MT2llBin6WW',  
    'samples'  : {
        '04_TTTo2L2Nu' : '0.05',
        '05_ST'        : '0.05',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin7WW']  = {
    'name'  : 'MT2llBin7WW',  
    'samples'  : {
        '04_TTTo2L2Nu' : '0.05',
        '05_ST'        : '0.05',
        },
    'type'  : 'shape',
    }
"""
# MT2ll correlate bins
"""
nuisances['MT2llBin4Bin5Bin6Bin7SR1Top']  = {
    'name'  : 'MT2llBin4Bin5Bin6Bin7SR1Top',  
    'samples'  : {
        '04_TTTo2L2Nu' : '0.05',
        '05_ST'        : '0.05',
        },
    'cuts'  : {
        'SR1_' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin4Bin5Bin6Bin7SR2Top']  = {
    'name'  : 'MT2llBin4Bin5Bin6Bin7SR2Top',  
    'samples'  : {
        '04_TTTo2L2Nu' : '0.05',
        '05_ST'        : '0.05',
        },
    'cuts'  : {
        'SR2_' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin4Bin5Bin6Bin7SR3Top']  = {
    'name'  : 'MT2llBin4Bin5Bin6Bin7SR3Top',  
    'samples'  : {
        '04_TTTo2L2Nu' : '0.05',
        '05_ST'        : '0.05',
        },
    'cuts'  : {
        'SR3_' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin4Bin5Bin6Bin7SR1WW']  = {
    'name'  : 'MT2llBin4Bin5Bin6Bin7SR1WW',  
    'samples'  : {
        '06_WW'        : '0.05',
        },
    'cuts'  : {
        'SR1_' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin4Bin5Bin6Bin7SR2WW']  = {
    'name'  : 'MT2llBin4Bin5Bin6Bin7SR2WW',  
    'samples'  : {
        '06_WW'        : '0.05',
        },
    'cuts'  : {
        'SR2_' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin4Bin5Bin6Bin7SR3WW']  = {
    'name'  : 'MT2llBin4Bin5Bin6Bin7SR3WW',  
    'samples'  : {
        '06_WW'        : '0.05',
        },
    'cuts'  : {
        'SR3_' : '1.00',
        },
    'type'  : 'shape',
    }
"""
# MT2ll correlate regions and bins
"""
nuisances['MT2llBin4Bin5Bin6Bin7Top']  = {
    'name'  : 'MT2llBin4Bin5Bin6Bin7Top',  
    'samples'  : {
        '04_TTTo2L2Nu' : '0.05',
        '05_ST'        : '0.05',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin4Bin5Bin6Bin7WW']  = {
    'name'  : 'MT2llBin4Bin5Bin6Bin7WW',  
    'samples'  : {
        '06_WW' : '0.05',
        },
    'type'  : 'shape',
    }
"""
# MT2ll correlate nothing
"""
nuisances['MT2llBin4TopSR1']  = {
    'name'  : 'MT2llBin4TopSR1',  
    'samples'  : {
        '04_TTTo2L2Nu' : '0.05',
        '05_ST'        : '0.05',
        },
    'cuts'  : {
        'SR1_' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin4TopSR2']  = {
    'name'  : 'MT2llBin4TopSR2',  
    'samples'  : {
        '04_TTTo2L2Nu' : '0.05',
        '05_ST'        : '0.05',
        },
    'cuts'  : {
        'SR2_' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin4TopSR3']  = {
    'name'  : 'MT2llBin4TopSR3',  
    'samples'  : {
        '04_TTTo2L2Nu' : '0.05',
        '05_ST'        : '0.05',
        },
    'cuts'  : {
        'SR3_' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin5TopSR1']  = {
    'name'  : 'MT2llBin5TopSR1',  
    'samples'  : {
        '04_TTTo2L2Nu' : '0.05',
        '05_ST'        : '0.05',
        },
    'cuts'  : {
        'SR1_' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin6TopSR1']  = {
    'name'  : 'MT2llBin6TopSR1',  
    'samples'  : {
        '04_TTTo2L2Nu' : '0.15',
        '05_ST'        : '0.15',
        },
    'cuts'  : {
        'SR1_' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin7TopSR1']  = {
    'name'  : 'MT2llBin7TopSR1',  
    'samples'  : {
        '04_TTTo2L2Nu' : '0.30',
        '05_ST'        : '0.30',
        },
    'cuts'  : {
        'SR1_' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin5TopSR2']  = {
    'name'  : 'MT2llBin5TopSR2',  
    'samples'  : {
        '04_TTTo2L2Nu' : '0.05',
        '05_ST'        : '0.05',
        },
    'cuts'  : {
        'SR2_' : '1.00',        },
    'type'  : 'shape',
    }

nuisances['MT2llBin6TopSR2']  = {
    'name'  : 'MT2llBin6TopSR2',  
    'samples'  : {
        '04_TTTo2L2Nu' : '0.15',
        '05_ST'        : '0.15',
        },
    'cuts'  : {
        'SR2_' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin7TopSR2']  = {
    'name'  : 'MT2llBin7TopSR2',  
    'samples'  : {
        '04_TTTo2L2Nu' : '0.30',
        '05_ST'        : '0.30',
        },
    'cuts'  : {
        'SR2_' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin5TopSR3']  = {
    'name'  : 'MT2llBin5TopSR3',  
    'samples'  : {
        '04_TTTo2L2Nu' : '0.05',
        '05_ST'        : '0.05',
        },
    'cuts'  : {
        'SR3_' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin6TopSR3']  = {
    'name'  : 'MT2llBin6TopSR3',  
    'samples'  : {
        '04_TTTo2L2Nu' : '0.15',
        '05_ST'        : '0.15',
        },
    'cuts'  : {
        'SR3_' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin7TopSR3']  = {
    'name'  : 'MT2llBin7TopSR3',  
    'samples'  : {
        '04_TTTo2L2Nu' : '0.30',
        '05_ST'        : '0.30',
        },
    'cuts'  : {
        'SR3_' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin4WWSR1']  = {
    'name'  : 'MT2llBin4WWSR1',  
    'samples'  : {
        '06_WW'        : '0.05',
        },
    'cuts'  : {
        'SR1_' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin4WWSR2']  = {
    'name'  : 'MT2llBin4WWSR2',  
    'samples'  : {
        '06_WW'        : '0.05',
        },
    'cuts'  : {
        'SR2_' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin4WWSR3']  = {
    'name'  : 'MT2llBin4WWSR3',  
    'samples'  : {
        '06_WW'        : '0.05',
        },
    'cuts'  : {
        'SR3_' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin5WWSR1']  = {
    'name'  : 'MT2llBin5WWSR1',  
    'samples'  : {
        '06_WW' : '0.05',
        },
    'cuts'  : {
        'SR1_' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin6WWSR1']  = {
    'name'  : 'MT2llBin6WWSR1',  
    'samples'  : {
        '06_WW' : '0.15',
        },
    'cuts'  : {
        'SR1_' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin7WWSR1']  = {
    'name'  : 'MT2llBin7WWSR1',  
    'samples'  : {
        '06_WW' : '0.30',
        },
    'cuts'  : {
        'SR1_' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin5WWSR2']  = {
    'name'  : 'MT2llBin5WWSR2',  
    'samples'  : {
        '06_WW' : '0.05',
        },
    'cuts'  : {
        'SR2_' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin6WWSR2']  = {
    'name'  : 'MT2llBin6WWSR2',  
    'samples'  : {
        '06_WW' : '0.15',
        },
    'cuts'  : {
        'SR2_' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin7WWSR2']  = {
    'name'  : 'MT2llBin7WWSR2',  
    'samples'  : {
        '06_WW' : '0.30',
        },
    'cuts'  : {
        'SR2_' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin5WWSR3']  = {
    'name'  : 'MT2llBin5WWSR3',  
    'samples'  : {
        '06_WW' : '0.05',
        },
    'cuts'  : {
        'SR3_' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin6WWSR3']  = {
    'name'  : 'MT2llBin6WWSR3',  
    'samples'  : {
        '06_WW' : '0.15',
        },
    'cuts'  : {
        'SR3_' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin7WWSR3']  = {
    'name'  : 'MT2llBin7WWSR3',  
    'samples'  : {
        '06_WW' : '0.30',
        },
    'cuts'  : {
        'SR3_' : '1.00',
        },
    'type'  : 'shape',
    }
"""
# MT2ll V9C new style

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

# MT2ll V11mtll40 new style
"""
nuisances['MT2llBinWWSR1']  = {
    'name'  : 'MT2llBinWWSR1',  
    'samples'  : {
        '06_WW' : '1.00',
        },
    'cuts'  : {
        'SR1_' : {'Bin4': '0.05', 'Bin5': '0.10', 'Bin6': '0.40', 'Bin7': '0.40', },
        },
    'type'  : 'shape',
    }

nuisances['MT2llBinWWSR2']  = {
    'name'  : 'MT2llBinWWSR2',  
    'samples'  : {
        '06_WW' : '1.00',
        },
    'cuts'  : {
        'SR2_' : {'Bin4': '0.05', 'Bin5': '0.10', 'Bin6': '0.40', 'Bin7': '0.40', },
        },
    'type'  : 'shape',
    }

nuisances['MT2llBinWWSR3']  = {
    'name'  : 'MT2llBinWWSR3',  
    'samples'  : {
        '06_WW' : '1.00',
        },
    'cuts'  : {
        'SR3_' : {'Bin4': '0.05', 'Bin5': '0.10', 'Bin6': '0.40', 'Bin7': '0.40', },
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
        'SR1_' : {'Bin4': '0.05', 'Bin5': '0.10', 'Bin6': '0.40', 'Bin7': '0.40', },
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
        'SR2_' : {'Bin4': '0.05', 'Bin5': '0.10', 'Bin6': '0.40', 'Bin7': '0.40', },
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
        'SR3_' : {'Bin4': '0.05', 'Bin5': '0.10', 'Bin6': '0.40', 'Bin7': '0.40', },
        },
    'type'  : 'shape',
    }
"""
# MT2ll uncorr NoJet
"""
nuisances['MT2llBinWWSR1']  = {
    'name'  : 'MT2llBinWWSR1',  
    'samples'  : {
        '06_WW' : '1.00',
        },
    'cuts'  : {
        'SR1_Tag' :   {'Bin4': '0.05', 'Bin5': '0.10', 'Bin6': '0.20', 'Bin7': '0.30', },
        #'SR1_NoJet' : {'Bin4': '0.05', 'Bin5': '0.15', 'Bin6': '0.40', 'Bin7': '0.40', },
        'SR1_NoTag' : {'Bin4': '0.05', 'Bin5': '0.10', 'Bin6': '0.20', 'Bin7': '0.30', },
        'SR1_Veto' :  {'Bin4': '0.05', 'Bin5': '0.10', 'Bin6': '0.20', 'Bin7': '0.30', },
        },
    'type'  : 'shape',
    }

nuisances['MT2llBinWWSR2']  = {
    'name'  : 'MT2llBinWWSR2',  
    'samples'  : {
        '06_WW' : '1.00',
        },
    'cuts'  : {
        'SR2_Tag' :   {'Bin4': '0.05', 'Bin5': '0.10', 'Bin6': '0.20', 'Bin7': '0.30', },
        #'SR2_NoJet' : {'Bin4': '0.05', 'Bin5': '0.15', 'Bin6': '0.40', 'Bin7': '0.40', },
        'SR2_NoTag' : {'Bin4': '0.05', 'Bin5': '0.10', 'Bin6': '0.20', 'Bin7': '0.30', },
        'SR2_Veto' :  {'Bin4': '0.05', 'Bin5': '0.10', 'Bin6': '0.20', 'Bin7': '0.30', },
        },
    'type'  : 'shape',
    }

nuisances['MT2llBinWWSR3']  = {
    'name'  : 'MT2llBinWWSR3',  
    'samples'  : {
        '06_WW' : '1.00',
        },
    'cuts'  : {
        'SR3_Tag' :   {'Bin4': '0.05', 'Bin5': '0.10', 'Bin6': '0.20', 'Bin7': '0.30', },
        #'SR3_NoJet' : {'Bin4': '0.05', 'Bin5': '0.15', 'Bin6': '0.40', 'Bin7': '0.40', },
        'SR3_NoTag' : {'Bin4': '0.05', 'Bin5': '0.10', 'Bin6': '0.20', 'Bin7': '0.30', },
        'SR3_Veto' :  {'Bin4': '0.05', 'Bin5': '0.10', 'Bin6': '0.20', 'Bin7': '0.30', },
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
        'SR1_Tag' :   {'Bin4': '0.05', 'Bin5': '0.10', 'Bin6': '0.20', 'Bin7': '0.30', },
        #'SR1_NoJet' : {'Bin4': '0.05', 'Bin5': '0.15', 'Bin6': '0.40', 'Bin7': '0.40', },
        'SR1_NoTag' : {'Bin4': '0.05', 'Bin5': '0.10', 'Bin6': '0.20', 'Bin7': '0.30', },
        'SR1_Veto' :  {'Bin4': '0.05', 'Bin5': '0.10', 'Bin6': '0.20', 'Bin7': '0.30', },
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
        'SR2_Tag' :   {'Bin4': '0.05', 'Bin5': '0.10', 'Bin6': '0.20', 'Bin7': '0.30', },
        #'SR2_NoJet' : {'Bin4': '0.05', 'Bin5': '0.15', 'Bin6': '0.40', 'Bin7': '0.40', },
        'SR2_NoTag' : {'Bin4': '0.05', 'Bin5': '0.10', 'Bin6': '0.20', 'Bin7': '0.30', },
        'SR2_Veto' :  {'Bin4': '0.05', 'Bin5': '0.10', 'Bin6': '0.20', 'Bin7': '0.30', },
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
        'SR3_Tag' :   {'Bin4': '0.05', 'Bin5': '0.10', 'Bin6': '0.20', 'Bin7': '0.30', },
        #'SR3_NoJet' : {'Bin4': '0.05', 'Bin5': '0.15', 'Bin6': '0.40', 'Bin7': '0.40', },
        'SR3_NoTag' : {'Bin4': '0.05', 'Bin5': '0.10', 'Bin6': '0.20', 'Bin7': '0.30', },
        'SR3_Veto' :  {'Bin4': '0.05', 'Bin5': '0.10', 'Bin6': '0.20', 'Bin7': '0.30', },
        },
    'type'  : 'shape',
    }

nuisances['MT2llBinTopSR1NoJet']  = {
    'name'  : 'MT2llBinTopSR1NoJet',  
    'samples'  : {
        '04_TTTo2L2Nu' : '1.00',
        '05_ST' : '1.00',
        },
    'cuts'  : {
        'SR1_NoJet' : {'Bin4': '0.05', 'Bin5': '0.15', 'Bin6': '0.40', 'Bin7': '0.40', },
        },
    'type'  : 'shape',
    }

nuisances['MT2llBinTopSR2NoJet']  = {
    'name'  : 'MT2llBinTopSR2NoJet',  
    'samples'  : {
        '04_TTTo2L2Nu' : '1.00',
        '05_ST' : '1.00',
        },
    'cuts'  : {
        'SR2_NoJet' : {'Bin4': '0.05', 'Bin5': '0.15', 'Bin6': '0.40', 'Bin7': '0.40', },
        },
    'type'  : 'shape',
    }

nuisances['MT2llBinTopSR3NoJet']  = {
    'name'  : 'MT2llBinTopSR3NoJet',  
    'samples'  : {
        '04_TTTo2L2Nu' : '1.00',
        '05_ST' : '1.00',
        },
    'cuts'  : {
        'SR3_NoJet' : {'Bin4': '0.05', 'Bin5': '0.15', 'Bin6': '0.40', 'Bin7': '0.40', },
        },
    'type'  : 'shape',
    }

nuisances['MT2llBinWWSR1NoJet']  = {
    'name'  : 'MT2llBinWWSR1NoJet',  
    'samples'  : {
        '06_WW' : '1.00',
        },
    'cuts'  : {
        'SR1_NoJet' : {'Bin4': '0.05', 'Bin5': '0.15', 'Bin6': '0.40', 'Bin7': '0.40', },
        },
    'type'  : 'shape',
    }

nuisances['MT2llBinWWSR2NoJet']  = {
    'name'  : 'MT2llBinWWSR2NoJet',  
    'samples'  : {
        '06_WW' : '1.00',
        },
    'cuts'  : {
        'SR2_NoJet' : {'Bin4': '0.05', 'Bin5': '0.15', 'Bin6': '0.40', 'Bin7': '0.40', },
        },
    'type'  : 'shape',
    }

nuisances['MT2llBinWWSR3NoJet']  = {
    'name'  : 'MT2llBinWWSR3NoJet',  
    'samples'  : {
        '06_WW' : '1.00',
        },
    'cuts'  : {
        'SR3_NoJet' : {'Bin4': '0.05', 'Bin5': '0.15', 'Bin6': '0.40', 'Bin7': '0.40', },
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


