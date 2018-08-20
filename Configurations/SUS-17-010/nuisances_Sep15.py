# lnN

nuisances['lumiMoriond17']  = {
    'name'  : 'lumiMoriond17', 
    'samples'  : {
        #https://twiki.cern.ch/twiki/bin/view/CMS/TWikiLUM#CurRec
        'T'                             : '1.026',
        #'03_VZ'                            : '1.026',
        '04_TTTo2L2Nu'                     : '1.026',
        '06_WW'                            : '1.026',
        '05_ST'                            : '1.026',
        '09_TTW'                           : '1.026',
        #'10_TTZ'                           : '1.026',
        #'07_ZJetsHT_scaled'                         : '1.026',
        '02_WZTo3LNu'                      : '1.026',
        '11_HWW'                           : '1.026',
        '13_VVV'                           : '1.026',
        },
    'type'  : 'lnN',
    }

nuisances['normWZ']  = {
    'name'  : 'normTTW', 
    'samples'  : {
        '02_WZTo3LNu'                      : '1.04',
        },
    'type'  : 'lnN',
    }

nuisances['normTTZ']  = {
    'name'  : 'normTTZ', 
    'samples'  : {
        '10_TTZ'                           : '1.25',
        },
    'type'  : 'lnN',
    }


#nuisances['normVZ']  = {
#    'name'  : 'normVZ', 
#    'samples'  : {
#        '03_VZ'                            : '1.21',
#        },
#    'type'  : 'lnN',
#    }

#nuisances['normDY']  = {
#    'name'  : 'normDY', 
#    'samples'  : {
#        '07_ZJetsHT'                         : '1.37',
#        },
#    'type'  : 'lnN',
#    }

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
        '03_VZ'                            : '1.',
        '04_TTTo2L2Nu'                     : '1.',
        '06_WW'                            : '1.',
        '05_ST'                            : '1.',
        '09_TTW'                           : '1.',
        '10_TTZ'                          : '1.',
        '07_ZJetsHT_scaled'                         : '1.',
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
        '03_VZ'                            : '1.',
        '04_TTTo2L2Nu'                     : '1.',
        '06_WW'                            : '1.',
        '05_ST'                            : '1.',
        '09_TTW'                           : '1.',
        '10_TTZ'                          : '1.',
        '07_ZJetsHT_scaled'                         : '1.',
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
#        '03_VZ'                            : '1.',
#        '04_TTTo2L2Nu'                     : '1.',
#        '06_WW'                            : '1.',
#        '05_ST'                            : '1.',
#        '09_TTW'                           : '1.',
#        '10_TTZ'                          : '1.',
#        '07_ZJetsHT_scaled'                         : '1.',
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
#        '03_VZ'                            : '1.',
#        '04_TTTo2L2Nu'                     : '1.',
#        '06_WW'                            : '1.',
#        '05_ST'                            : '1.',
#        '09_TTW'                           : '1.',
#        '10_TTZ'                          : '1.',
#        '07_ZJetsHT_scaled'                         : '1.',
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
#        '03_VZ'                            : '1.',
#        '04_TTTo2L2Nu'                     : '1.',
#        '06_WW'                            : '1.',
#        '05_ST'                            : '1.',
#        '09_TTW'                           : '1.',
#        '10_TTZ'                          : '1.',
#        '07_ZJetsHT_scaled'                         : '1.',
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
        #'03_VZ'                            : '1.02',
        '04_TTTo2L2Nu'                     : '1.02',
        '06_WW'                            : '1.02',
        '05_ST'                            : '1.02',
        '09_TTW'                           : '1.02',
        #'10_TTZ'                           : '1.02',
        #'07_ZJetsHT_scaled'                         : '1.02',
        '02_WZTo3LNu'                      : '1.02',
        '11_HWW'                           : '1.',
        '13_VVV'                           : '1.',
        },
    'type'  : 'lnN',
    }

nuisances['Btag']  = {
    'name'  : 'Btag', 
    'samples'  : {
        'T'                             : '1.',
        '03_VZ'                            : '1.',
        '04_TTTo2L2Nu'                     : '1.',
        '06_WW'                            : '1.',
        '05_ST'                            : '1.',
        '09_TTW'                           : '1.',
        '10_TTZ'                          : '1.',
        '07_ZJetsHT_scaled'                         : '1.',
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
        '03_VZ'                            : '1.',
        '04_TTTo2L2Nu'                     : '1.',
        '06_WW'                            : '1.',
        '05_ST'                            : '1.',
        '09_TTW'                           : '1.',
        '10_TTZ'                           : '1.',
        '07_ZJetsHT_scaled'                         : '1.',
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
        '03_VZ'                            : '1.',
        '04_TTTo2L2Nu'                     : '1.',
        '06_WW'                            : '1.',
        '05_ST'                            : '1.',
        '09_TTW'                           : '1.',
        '10_TTZ'                           : '1.',
        '07_ZJetsHT_scaled'                         : '1.',
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
        '03_VZ'                            : '1.',
        '04_TTTo2L2Nu'                     : '1.',
        '06_WW'                            : '1.',
        #'05_ST'                            : '1.',
        '09_TTW'                           : '1.',
        '10_TTZ'                           : '1.',
        '07_ZJetsHT_scaled'                       : '1.',
        '02_WZTo3LNu'                      : '1.',
        '11_HWW'                           : '1.',
        '13_VVV'                           : '1.',
        },
    'type'  : 'shape',
    }

nuisances['PDF']  = {
    'name'  : 'PDF', 
    'samples'  : {
        '03_VZ'                            : '1.',
        '04_TTTo2L2Nu'                     : '1.',
        '06_WW'                            : '1.',
        #'05_ST'                            : '1.',
        '09_TTW'                           : '1.',
        '10_TTZ'                           : '1.',
        '07_ZJetsHT_scaled'                       : '1.',
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
        '04_TTTo2L2Nu'                      : '1.',
        },
    'type'  : 'shape',
    }

# Stat

nuisances['stat']  = {
    # apply to the following samples: name of samples here must match keys in samples.py
    'samples'  : {
        
        'T'                           : {
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
        '03_VZ': {
            'typeStat' : 'bbb',
                         },
        '09_TTW': {
            'typeStat' : 'bbb',
                         }, 
        '10_TTZ': {
            'typeStat' : 'bbb',
                         },  
        '07_ZJetsHT_scaled': {
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
        'SR1_Tag_ee' : '1.00',
        'SR1_Tag_em' : '1.00',
        'SR1_Tag_mm' : '1.00',
        'SR1_NoTag_ee' : '1.00',
        'SR1_NoTag_em' : '1.00',
        'SR1_NoTag_mm' : '1.00',
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
        'SR2_Tag_ee' : '1.00',
        'SR2_Tag_em' : '1.00',
        'SR2_Tag_mm' : '1.00',
        'SR2_NoTag_ee' : '1.00',
        'SR2_NoTag_em' : '1.00',
        'SR2_NoTag_mm' : '1.00',
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
        'SR3_Tag_ee' : '1.00',
        'SR3_Tag_em' : '1.00',
        'SR3_Tag_mm' : '1.00',
        'SR3_NoTag_ee' : '1.00',
        'SR3_NoTag_em' : '1.00',
        'SR3_NoTag_mm' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin4Bin5Bin6Bin7SR1WW']  = {
    'name'  : 'MT2llBin4Bin5Bin6Bin7SR1WW',  
    'samples'  : {
        '06_WW'        : '0.05',
        },
    'cuts'  : {
        'SR1_Tag_ee' : '1.00',
        'SR1_Tag_em' : '1.00',
        'SR1_Tag_mm' : '1.00',
        'SR1_NoTag_ee' : '1.00',
        'SR1_NoTag_em' : '1.00',
        'SR1_NoTag_mm' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin4Bin5Bin6Bin7SR2WW']  = {
    'name'  : 'MT2llBin4Bin5Bin6Bin7SR2WW',  
    'samples'  : {
        '06_WW'        : '0.05',
        },
    'cuts'  : {
        'SR2_Tag_ee' : '1.00',
        'SR2_Tag_em' : '1.00',
        'SR2_Tag_mm' : '1.00',
        'SR2_NoTag_ee' : '1.00',
        'SR2_NoTag_em' : '1.00',
        'SR2_NoTag_mm' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin4Bin5Bin6Bin7SR3WW']  = {
    'name'  : 'MT2llBin4Bin5Bin6Bin7SR3WW',  
    'samples'  : {
        '06_WW'        : '0.05',
        },
    'cuts'  : {
        'SR3_Tag_ee' : '1.00',
        'SR3_Tag_em' : '1.00',
        'SR3_Tag_mm' : '1.00',
        'SR3_NoTag_ee' : '1.00',
        'SR3_NoTag_em' : '1.00',
        'SR3_NoTag_mm' : '1.00',
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

nuisances['MT2llBin4TopSR1']  = {
    'name'  : 'MT2llBin4TopSR1',  
    'samples'  : {
        '04_TTTo2L2Nu' : '0.05',
        '05_ST'        : '0.05',
        },
    'cuts'  : {
        'SR1_Tag_ee' : '1.00',
        'SR1_Tag_em' : '1.00',
        'SR1_Tag_mm' : '1.00',
        'SR1_Tag_ll' : '1.00',
        'SR1_Tag_sf' : '1.00',
        'SR1_NoTag_ee' : '1.00',
        'SR1_NoTag_em' : '1.00',
        'SR1_NoTag_mm' : '1.00',
        'SR1_NoTag_ll' : '1.00',
        'SR1_NoTag_sf' : '1.00',
        'SR1_NoJet_ee' : '1.00',
        'SR1_NoJet_em' : '1.00',
        'SR1_NoJet_mm' : '1.00',
        'SR1_NoJet_ll' : '1.00',
        'SR1_NoJet_sf' : '1.00',
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
        'SR2_Tag_ee' : '1.00',
        'SR2_Tag_em' : '1.00',
        'SR2_Tag_mm' : '1.00',
        'SR2_Tag_ll' : '1.00',
        'SR2_Tag_sf' : '1.00',
        'SR2_NoTag_ee' : '1.00',
        'SR2_NoTag_em' : '1.00',
        'SR2_NoTag_mm' : '1.00',
        'SR2_NoTag_ll' : '1.00',
        'SR2_NoTag_sf' : '1.00',
        'SR2_NoJet_ee' : '1.00',
        'SR2_NoJet_em' : '1.00',
        'SR2_NoJet_mm' : '1.00',
        'SR2_NoJet_ll' : '1.00',
        'SR2_NoJet_sf' : '1.00',
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
        'SR3_Tag_ee' : '1.00',
        'SR3_Tag_em' : '1.00',
        'SR3_Tag_mm' : '1.00',
        'SR3_Tag_ll' : '1.00',
        'SR3_Tag_sf' : '1.00',
        'SR3_NoTag_ee' : '1.00',
        'SR3_NoTag_em' : '1.00',
        'SR3_NoTag_mm' : '1.00',
        'SR3_NoTag_ll' : '1.00',
        'SR3_NoTag_sf' : '1.00',
        'SR3_NoJet_ee' : '1.00',
        'SR3_NoJet_em' : '1.00',
        'SR3_NoJet_mm' : '1.00',
        'SR3_NoJet_ll' : '1.00',
        'SR3_NoJet_sf' : '1.00',
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
        'SR1_Tag_ee' : '1.00',
        'SR1_Tag_em' : '1.00',
        'SR1_Tag_mm' : '1.00',
        'SR1_Tag_ll' : '1.00',
        'SR1_Tag_sf' : '1.00',
        'SR1_NoTag_ee' : '1.00',
        'SR1_NoTag_em' : '1.00',
        'SR1_NoTag_mm' : '1.00',
        'SR1_NoTag_ll' : '1.00',
        'SR1_NoTag_sf' : '1.00',
        'SR1_NoJet_ee' : '1.00',
        'SR1_NoJet_em' : '1.00',
        'SR1_NoJet_mm' : '1.00',
        'SR1_NoJet_ll' : '1.00',
        'SR1_NoJet_sf' : '1.00',
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
        'SR1_Tag_ee' : '1.00',
        'SR1_Tag_em' : '1.00',
        'SR1_Tag_mm' : '1.00',
        'SR1_Tag_ll' : '1.00',
        'SR1_Tag_sf' : '1.00',
        'SR1_NoTag_ee' : '1.00',
        'SR1_NoTag_em' : '1.00',
        'SR1_NoTag_mm' : '1.00',
        'SR1_NoTag_ll' : '1.00',
        'SR1_NoTag_sf' : '1.00',
        'SR1_NoJet_ee' : '1.00',
        'SR1_NoJet_em' : '1.00',
        'SR1_NoJet_mm' : '1.00',
        'SR1_NoJet_ll' : '1.00',
        'SR1_NoJet_sf' : '1.00',
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
        'SR1_Tag_ee' : '1.00',
        'SR1_Tag_em' : '1.00',
        'SR1_Tag_mm' : '1.00',
        'SR1_Tag_ll' : '1.00',
        'SR1_Tag_sf' : '1.00',
        'SR1_NoTag_ee' : '1.00',
        'SR1_NoTag_em' : '1.00',
        'SR1_NoTag_mm' : '1.00',
        'SR1_NoTag_ll' : '1.00',
        'SR1_NoTag_sf' : '1.00',
        'SR1_NoJet_ee' : '1.00',
        'SR1_NoJet_em' : '1.00',
        'SR1_NoJet_mm' : '1.00',
        'SR1_NoJet_ll' : '1.00',
        'SR1_NoJet_sf' : '1.00',
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
        'SR2_Tag_ee' : '1.00',
        'SR2_Tag_em' : '1.00',
        'SR2_Tag_mm' : '1.00',
        'SR2_Tag_ll' : '1.00',
        'SR2_Tag_sf' : '1.00',
        'SR2_NoTag_ee' : '1.00',
        'SR2_NoTag_em' : '1.00',
        'SR2_NoTag_mm' : '1.00',
        'SR2_NoTag_ll' : '1.00',
        'SR2_NoTag_sf' : '1.00',
        'SR2_NoJet_ee' : '1.00',
        'SR2_NoJet_em' : '1.00',
        'SR2_NoJet_mm' : '1.00',
        'SR2_NoJet_ll' : '1.00',
        'SR2_NoJet_sf' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin6TopSR2']  = {
    'name'  : 'MT2llBin6TopSR2',  
    'samples'  : {
        '04_TTTo2L2Nu' : '0.15',
        '05_ST'        : '0.15',
        },
    'cuts'  : {
        'SR2_Tag_ee' : '1.00',
        'SR2_Tag_em' : '1.00',
        'SR2_Tag_mm' : '1.00',
        'SR2_Tag_ll' : '1.00',
        'SR2_Tag_sf' : '1.00',
        'SR2_NoTag_ee' : '1.00',
        'SR2_NoTag_em' : '1.00',
        'SR2_NoTag_mm' : '1.00',
        'SR2_NoTag_ll' : '1.00',
        'SR2_NoTag_sf' : '1.00',
        'SR2_NoJet_ee' : '1.00',
        'SR2_NoJet_em' : '1.00',
        'SR2_NoJet_mm' : '1.00',
        'SR2_NoJet_ll' : '1.00',
        'SR2_NoJet_sf' : '1.00',
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
        'SR2_Tag_ee' : '1.00',
        'SR2_Tag_em' : '1.00',
        'SR2_Tag_mm' : '1.00',
        'SR2_Tag_ll' : '1.00',
        'SR2_Tag_sf' : '1.00',
        'SR2_NoTag_ee' : '1.00',
        'SR2_NoTag_em' : '1.00',
        'SR2_NoTag_mm' : '1.00',
        'SR2_NoTag_ll' : '1.00',
        'SR2_NoTag_sf' : '1.00',
        'SR2_NoJet_ee' : '1.00',
        'SR2_NoJet_em' : '1.00',
        'SR2_NoJet_mm' : '1.00',
        'SR2_NoJet_ll' : '1.00',
        'SR2_NoJet_sf' : '1.00',
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
        'SR3_Tag_ee' : '1.00',
        'SR3_Tag_em' : '1.00',
        'SR3_Tag_mm' : '1.00',
        'SR3_Tag_ll' : '1.00',
        'SR3_Tag_sf' : '1.00',
        'SR3_NoTag_ee' : '1.00',
        'SR3_NoTag_em' : '1.00',
        'SR3_NoTag_mm' : '1.00',
        'SR3_NoTag_ll' : '1.00',
        'SR3_NoTag_sf' : '1.00',
        'SR3_NoJet_ee' : '1.00',
        'SR3_NoJet_em' : '1.00',
        'SR3_NoJet_mm' : '1.00',
        'SR3_NoJet_ll' : '1.00',
        'SR3_NoJet_sf' : '1.00',
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
        'SR3_Tag_ee' : '1.00',
        'SR3_Tag_em' : '1.00',
        'SR3_Tag_mm' : '1.00',
        'SR3_Tag_ll' : '1.00',
        'SR3_Tag_sf' : '1.00',
        'SR3_NoTag_ee' : '1.00',
        'SR3_NoTag_em' : '1.00',
        'SR3_NoTag_mm' : '1.00',
        'SR3_NoTag_ll' : '1.00',
        'SR3_NoTag_sf' : '1.00',
        'SR3_NoJet_ee' : '1.00',
        'SR3_NoJet_em' : '1.00',
        'SR3_NoJet_mm' : '1.00',
        'SR3_NoJet_ll' : '1.00',
        'SR3_NoJet_sf' : '1.00',
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
        'SR3_Tag_ee' : '1.00',
        'SR3_Tag_em' : '1.00',
        'SR3_Tag_mm' : '1.00',
        'SR3_Tag_ll' : '1.00',
        'SR3_Tag_sf' : '1.00',
        'SR3_NoTag_ee' : '1.00',
        'SR3_NoTag_em' : '1.00',
        'SR3_NoTag_mm' : '1.00',
        'SR3_NoTag_ll' : '1.00',
        'SR3_NoTag_sf' : '1.00',
        'SR3_NoJet_ee' : '1.00',
        'SR3_NoJet_em' : '1.00',
        'SR3_NoJet_mm' : '1.00',
        'SR3_NoJet_ll' : '1.00',
        'SR3_NoJet_sf' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin4WWSR1']  = {
    'name'  : 'MT2llBin4WWSR1',  
    'samples'  : {
        '06_WW'        : '0.05',
        },
    'cuts'  : {
        'SR1_Tag_ee' : '1.00',
        'SR1_Tag_em' : '1.00',
        'SR1_Tag_mm' : '1.00',
        'SR1_Tag_ll' : '1.00',
        'SR1_Tag_sf' : '1.00',
        'SR1_NoTag_ee' : '1.00',
        'SR1_NoTag_em' : '1.00',
        'SR1_NoTag_mm' : '1.00',
        'SR1_NoTag_ll' : '1.00',
        'SR1_NoTag_sf' : '1.00',
        'SR1_NoJet_ee' : '1.00',
        'SR1_NoJet_em' : '1.00',
        'SR1_NoJet_mm' : '1.00',
        'SR1_NoJet_ll' : '1.00',
        'SR1_NoJet_sf' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin4WWSR2']  = {
    'name'  : 'MT2llBin4WWSR2',  
    'samples'  : {
        '06_WW'        : '0.05',
        },
    'cuts'  : {
        'SR2_Tag_ee' : '1.00',
        'SR2_Tag_em' : '1.00',
        'SR2_Tag_mm' : '1.00',
        'SR2_Tag_ll' : '1.00',
        'SR2_Tag_sf' : '1.00',
        'SR2_NoTag_ee' : '1.00',
        'SR2_NoTag_em' : '1.00',
        'SR2_NoTag_mm' : '1.00',
        'SR2_NoTag_ll' : '1.00',
        'SR2_NoTag_sf' : '1.00',
        'SR2_NoJet_ee' : '1.00',
        'SR2_NoJet_em' : '1.00',
        'SR2_NoJet_mm' : '1.00',
        'SR2_NoJet_ll' : '1.00',
        'SR2_NoJet_sf' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin4WWSR3']  = {
    'name'  : 'MT2llBin4WWSR3',  
    'samples'  : {
        '06_WW'        : '0.05',
        },
    'cuts'  : {
        'SR3_Tag_ee' : '1.00',
        'SR3_Tag_em' : '1.00',
        'SR3_Tag_mm' : '1.00',
        'SR3_Tag_ll' : '1.00',
        'SR3_Tag_sf' : '1.00',
        'SR3_NoTag_ee' : '1.00',
        'SR3_NoTag_em' : '1.00',
        'SR3_NoTag_mm' : '1.00',
        'SR3_NoTag_ll' : '1.00',
        'SR3_NoTag_sf' : '1.00',
        'SR3_NoJet_ee' : '1.00',
        'SR3_NoJet_em' : '1.00',
        'SR3_NoJet_mm' : '1.00',
        'SR3_NoJet_ll' : '1.00',
        'SR3_NoJet_sf' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin5WWSR1']  = {
    'name'  : 'MT2llBin5WWSR1',  
    'samples'  : {
        '06_WW' : '0.05',
        },
    'cuts'  : {
        'SR1_Tag_ee' : '1.00',
        'SR1_Tag_em' : '1.00',
        'SR1_Tag_mm' : '1.00',
        'SR1_Tag_ll' : '1.00',
        'SR1_Tag_sf' : '1.00',
        'SR1_NoTag_ee' : '1.00',
        'SR1_NoTag_em' : '1.00',
        'SR1_NoTag_mm' : '1.00',
        'SR1_NoTag_ll' : '1.00',
        'SR1_NoTag_sf' : '1.00',
        'SR1_NoJet_ee' : '1.00',
        'SR1_NoJet_em' : '1.00',
        'SR1_NoJet_mm' : '1.00',
        'SR1_NoJet_ll' : '1.00',
        'SR1_NoJet_sf' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin6WWSR1']  = {
    'name'  : 'MT2llBin6WWSR1',  
    'samples'  : {
        '06_WW' : '0.15',
        },
    'cuts'  : {
        'SR1_Tag_ee' : '1.00',
        'SR1_Tag_em' : '1.00',
        'SR1_Tag_mm' : '1.00',
        'SR1_Tag_ll' : '1.00',
        'SR1_Tag_sf' : '1.00',
        'SR1_NoTag_ee' : '1.00',
        'SR1_NoTag_em' : '1.00',
        'SR1_NoTag_mm' : '1.00',
        'SR1_NoTag_ll' : '1.00',
        'SR1_NoTag_sf' : '1.00',
        'SR1_NoJet_ee' : '1.00',
        'SR1_NoJet_em' : '1.00',
        'SR1_NoJet_mm' : '1.00',
        'SR1_NoJet_ll' : '1.00',
        'SR1_NoJet_sf' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin7WWSR1']  = {
    'name'  : 'MT2llBin7WWSR1',  
    'samples'  : {
        '06_WW' : '0.30',
        },
    'cuts'  : {
        'SR1_Tag_ee' : '1.00',
        'SR1_Tag_em' : '1.00',
        'SR1_Tag_mm' : '1.00',
        'SR1_Tag_ll' : '1.00',
        'SR1_Tag_sf' : '1.00',
        'SR1_NoTag_ee' : '1.00',
        'SR1_NoTag_em' : '1.00',
        'SR1_NoTag_mm' : '1.00',
        'SR1_NoTag_ll' : '1.00',
        'SR1_NoTag_sf' : '1.00',
        'SR1_NoJet_ee' : '1.00',
        'SR1_NoJet_em' : '1.00',
        'SR1_NoJet_mm' : '1.00',
        'SR1_NoJet_ll' : '1.00',
        'SR1_NoJet_sf' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin5WWSR2']  = {
    'name'  : 'MT2llBin5WWSR2',  
    'samples'  : {
        '06_WW' : '0.05',
        },
    'cuts'  : {
        'SR2_Tag_ee' : '1.00',
        'SR2_Tag_em' : '1.00',
        'SR2_Tag_mm' : '1.00',
        'SR2_Tag_ll' : '1.00',
        'SR2_Tag_sf' : '1.00',
        'SR2_NoTag_ee' : '1.00',
        'SR2_NoTag_em' : '1.00',
        'SR2_NoTag_mm' : '1.00',
        'SR2_NoTag_ll' : '1.00',
        'SR2_NoTag_sf' : '1.00',
        'SR2_NoJet_ee' : '1.00',
        'SR2_NoJet_em' : '1.00',
        'SR2_NoJet_mm' : '1.00',
        'SR2_NoJet_ll' : '1.00',
        'SR2_NoJet_sf' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin6WWSR2']  = {
    'name'  : 'MT2llBin6WWSR2',  
    'samples'  : {
        '06_WW' : '0.15',
        },
    'cuts'  : {
        'SR2_Tag_ee' : '1.00',
        'SR2_Tag_em' : '1.00',
        'SR2_Tag_mm' : '1.00',
        'SR2_Tag_ll' : '1.00',
        'SR2_Tag_sf' : '1.00',
        'SR2_NoTag_ee' : '1.00',
        'SR2_NoTag_em' : '1.00',
        'SR2_NoTag_mm' : '1.00',
        'SR2_NoTag_ll' : '1.00',
        'SR2_NoTag_sf' : '1.00',
        'SR2_NoJet_ee' : '1.00',
        'SR2_NoJet_em' : '1.00',
        'SR2_NoJet_mm' : '1.00',
        'SR2_NoJet_ll' : '1.00',
        'SR2_NoJet_sf' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin7WWSR2']  = {
    'name'  : 'MT2llBin7WWSR2',  
    'samples'  : {
        '06_WW' : '0.30',
        },
    'cuts'  : {
        'SR2_Tag_ee' : '1.00',
        'SR2_Tag_em' : '1.00',
        'SR2_Tag_mm' : '1.00',
        'SR2_Tag_ll' : '1.00',
        'SR2_Tag_sf' : '1.00',
        'SR2_NoTag_ee' : '1.00',
        'SR2_NoTag_em' : '1.00',
        'SR2_NoTag_mm' : '1.00',
        'SR2_NoTag_ll' : '1.00',
        'SR2_NoTag_sf' : '1.00',
        'SR2_NoJet_ee' : '1.00',
        'SR2_NoJet_em' : '1.00',
        'SR2_NoJet_mm' : '1.00',
        'SR2_NoJet_ll' : '1.00',
        'SR2_NoJet_sf' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin5WWSR3']  = {
    'name'  : 'MT2llBin5WWSR3',  
    'samples'  : {
        '06_WW' : '0.05',
        },
    'cuts'  : {
        'SR3_Tag_ee' : '1.00',
        'SR3_Tag_em' : '1.00',
        'SR3_Tag_mm' : '1.00',
        'SR3_Tag_ll' : '1.00',
        'SR3_Tag_sf' : '1.00',
        'SR3_NoTag_ee' : '1.00',
        'SR3_NoTag_em' : '1.00',
        'SR3_NoTag_mm' : '1.00',
        'SR3_NoTag_ll' : '1.00',
        'SR3_NoTag_sf' : '1.00',
        'SR3_NoJet_ee' : '1.00',
        'SR3_NoJet_em' : '1.00',
        'SR3_NoJet_mm' : '1.00',
        'SR3_NoJet_ll' : '1.00',
        'SR3_NoJet_sf' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin6WWSR3']  = {
    'name'  : 'MT2llBin6WWSR3',  
    'samples'  : {
        '06_WW' : '0.15',
        },
    'cuts'  : {
        'SR3_Tag_ee' : '1.00',
        'SR3_Tag_em' : '1.00',
        'SR3_Tag_mm' : '1.00',
        'SR3_Tag_ll' : '1.00',
        'SR3_Tag_sf' : '1.00',
        'SR3_NoTag_ee' : '1.00',
        'SR3_NoTag_em' : '1.00',
        'SR3_NoTag_mm' : '1.00',
        'SR3_NoTag_ll' : '1.00',
        'SR3_NoTag_sf' : '1.00',
        'SR3_NoJet_ee' : '1.00',
        'SR3_NoJet_em' : '1.00',
        'SR3_NoJet_mm' : '1.00',
        'SR3_NoJet_ll' : '1.00',
        'SR3_NoJet_sf' : '1.00',
        },
    'type'  : 'shape',
    }

nuisances['MT2llBin7WWSR3']  = {
    'name'  : 'MT2llBin7WWSR3',  
    'samples'  : {
        '06_WW' : '0.30',
        },
    'cuts'  : {
        'SR3_Tag_ee' : '1.00',
        'SR3_Tag_em' : '1.00',
        'SR3_Tag_mm' : '1.00',
        'SR3_Tag_ll' : '1.00',
        'SR3_Tag_sf' : '1.00',
        'SR3_NoTag_ee' : '1.00',
        'SR3_NoTag_em' : '1.00',
        'SR3_NoTag_mm' : '1.00',
        'SR3_NoTag_ll' : '1.00',
        'SR3_NoTag_sf' : '1.00',
        'SR3_NoJet_ee' : '1.00',
        'SR3_NoJet_em' : '1.00',
        'SR3_NoJet_mm' : '1.00',
        'SR3_NoJet_ll' : '1.00',
        'SR3_NoJet_sf' : '1.00',
        },
    'type'  : 'shape',
    }

# VR --> From fit (not used)
"""
nuisances['TopMT2llShape']  = {
    'name'  : 'TopMT2llShape', 
    'rootfile'  : 'VR1TagFit', 
    'samples'  : {
        '04_TTTo2L2Nu' : '1.',
        '05_ST'        : '1.',
        },
    'cuts'  : {
        'VR1_Tag_ee' : '1.00',
        'VR1_Tag_em' : '1.00',
        'VR1_Tag_mm' : '1.00',
        'VR1_NoTag_ee' : '1.00',
        'VR1_NoTag_em' : '1.00',
        'VR1_NoTag_mm' : '1.00',
        'SR1_Tag_ee' : '1.00',
        'SR1_Tag_em' : '1.00',
        'SR1_Tag_mm' : '1.00',
        'SR1_NoTag_ee' : '1.00',
        'SR1_NoTag_em' : '1.00',
        'SR1_NoTag_mm' : '1.00',
        'SR2_Tag_ee' : '1.00',
        'SR2_Tag_em' : '1.00',
        'SR2_Tag_mm' : '1.00',
        'SR2_NoTag_ee' : '1.00',
        'SR2_NoTag_em' : '1.00',
        'SR2_NoTag_mm' : '1.00',
        'SR3_Tag_ee' : '1.00',
        'SR3_Tag_em' : '1.00',
        'SR3_Tag_mm' : '1.00',
        'SR3_NoTag_ee' : '1.00',
        'SR3_NoTag_em' : '1.00',
        'SR3_NoTag_mm' : '1.00',
        },
    'type'  : 'shapefit',
    }

nuisances['WWMT2llShape']  = {
    'name'  : 'WWMT2llShape', 
    'rootfile'  : 'VR1NoTagFit', 
    'samples'  : {
        '06_WW' : '1.',
        },
    'cuts'  : {
        'SR1_Tag_ee' : '1.00',
        'SR1_Tag_em' : '1.00',
        'SR1_Tag_mm' : '1.00',
        'SR1_NoTag_ee' : '1.00',
        'SR1_NoTag_em' : '1.00',
        'SR1_NoTag_mm' : '1.00',
        'SR2_Tag_ee' : '1.00',
        'SR2_Tag_em' : '1.00',
        'SR2_Tag_mm' : '1.00',
        'SR2_NoTag_ee' : '1.00',
        'SR2_NoTag_em' : '1.00',
        'SR2_NoTag_mm' : '1.00',
        'SR3_Tag_ee' : '1.00',
        'SR3_Tag_em' : '1.00',
        'SR3_Tag_mm' : '1.00',
        'SR3_NoTag_ee' : '1.00',
        'SR3_NoTag_em' : '1.00',
        'SR3_NoTag_mm' : '1.00',
        },
    'type'  : 'shapefit',
    }
"""

# rateParam ttbar

nuisances['Topnorm_SR1_em']  = {
    'name'  : 'Topnorm_SR1_em',
    'samples'  : {
        '04_TTTo2L2Nu' : '1.00',
        #'05_ST' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR1_Tag_em' : '1.00',
        'SR1_NoTag_em' : '1.00',
        'SR1_NoJet_em' : '1.00',
        },
    }

nuisances['Topnorm_SR1_ee']  = {
    'name'  : 'Topnorm_SR1_ee',
    'samples'  : {
        '04_TTTo2L2Nu' : '1.00',
        #'05_ST' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR1_Tag_ee' : '1.00',
        'SR1_NoTag_ee' : '1.00',
        'SR1_NoJet_ee' : '1.00',
        },
    }

nuisances['Topnorm_SR1_mm']  = {
    'name'  : 'Topnorm_SR1_mm',
    'samples'  : {
        '04_TTTo2L2Nu' : '1.00',
        #'05_ST' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR1_Tag_mm' : '1.00',
        'SR1_NoTag_mm' : '1.00',
        'SR1_NoJet_mm' : '1.00',
        },
    }

nuisances['Topnorm_SR1_ll']  = {
    'name'  : 'Topnorm_SR1_ll',
    'samples'  : {
        '04_TTTo2L2Nu' : '1.00',
        #'05_ST' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR1_Tag_ll' : '1.00',
        'SR1_NoTag_ll' : '1.00',
        'SR1_NoJet_ll' : '1.00',
        },
    }

nuisances['Topnorm_SR1_sf']  = {
    'name'  : 'Topnorm_SR1_sf',
    'samples'  : {
        '04_TTTo2L2Nu' : '1.00',
        #'05_ST' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR1_Tag_sf' : '1.00',
        'SR1_NoTag_sf' : '1.00',
        'SR1_NoJet_sf' : '1.00',
        },
    }

nuisances['Topnorm_SR2_em']  = {
    'name'  : 'Topnorm_SR2_em',
    'samples'  : {
        '04_TTTo2L2Nu' : '1.00',
        #'05_ST' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR2_Tag_em' : '1.00',
        'SR2_NoTag_em' : '1.00',
        'SR2_NoJet_em' : '1.00',
        },
    }

nuisances['Topnorm_SR2_ee']  = {
    'name'  : 'Topnorm_SR2_ee',
    'samples'  : {
        '04_TTTo2L2Nu' : '1.00',
        #'05_ST' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR2_Tag_ee' : '1.00',
        'SR2_NoTag_ee' : '1.00',
        'SR2_NoJet_ee' : '1.00',
        },
    }

nuisances['Topnorm_SR2_mm']  = {
    'name'  : 'Topnorm_SR2_mm',
    'samples'  : {
        '04_TTTo2L2Nu' : '1.00',
        #'05_ST' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR2_Tag_mm' : '1.00',
        'SR2_NoTag_mm' : '1.00',
        'SR2_NoJet_mm' : '1.00',
        },
    }

nuisances['Topnorm_SR2_ll']  = {
    'name'  : 'Topnorm_SR2_ll',
    'samples'  : {
        '04_TTTo2L2Nu' : '1.00',
        #'05_ST' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR2_Tag_ll' : '1.00',
        'SR2_NoTag_ll' : '1.00',
        'SR2_NoJet_ll' : '1.00',
        },
    }

nuisances['Topnorm_SR2_sf']  = {
    'name'  : 'Topnorm_SR2_sf',
    'samples'  : {
        '04_TTTo2L2Nu' : '1.00',
        #'05_ST' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR2_Tag_sf' : '1.00',
        'SR2_NoTag_sf' : '1.00',
        'SR2_NoJet_sf' : '1.00',
        },
    }

nuisances['Topnorm_SR3_em']  = {
    'name'  : 'Topnorm_SR3_em',
    'samples'  : {
        '04_TTTo2L2Nu' : '1.00',
        #'05_ST' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR3_Tag_em' : '1.00',
        'SR3_NoTag_em' : '1.00',
        'SR3_NoJet_em' : '1.00',
        },
    }

nuisances['Topnorm_SR3_ee']  = {
    'name'  : 'Topnorm_SR3_ee',
    'samples'  : {
        '04_TTTo2L2Nu' : '1.00',
        #'05_ST' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR3_Tag_ee' : '1.00',
        'SR3_NoTag_ee' : '1.00',
        'SR3_NoJet_ee' : '1.00',
        },
    }

nuisances['Topnorm_SR3_mm']  = {
    'name'  : 'Topnorm_SR3_mm',
    'samples'  : {
        '04_TTTo2L2Nu' : '1.00',
        #'05_ST' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR3_Tag_mm' : '1.00',
        'SR3_NoTag_mm' : '1.00',
        'SR3_NoJet_mm' : '1.00',
        },
    }

nuisances['Topnorm_SR3_ll']  = {
    'name'  : 'Topnorm_SR3_ll',
    'samples'  : {
        '04_TTTo2L2Nu' : '1.00',
        #'05_ST' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR3_Tag_ll' : '1.00',
        'SR3_NoTag_ll' : '1.00',
        'SR3_NoJet_ll' : '1.00',
        },
    }

nuisances['Topnorm_SR3_sf']  = {
    'name'  : 'Topnorm_SR3_sf',
    'samples'  : {
        '04_TTTo2L2Nu' : '1.00',
        #'05_ST' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR3_Tag_sf' : '1.00',
        'SR3_NoTag_sf' : '1.00',
        'SR3_NoJet_sf' : '1.00',
        },
    }
"""
nuisances['Topnorm_VR1_em']  = {
    'name'  : 'Topnorm_VR1_em',
    'samples'  : {
        '04_TTTo2L2Nu' : '1.00',
        #'05_ST' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'VR1_Tag_em' : '1.00',
        'VR1_NoTag_em' : '1.00',
        'VR1_NoJet_em' : '1.00',
        },
    }

nuisances['Topnorm_VR1_ee']  = {
    'name'  : 'Topnorm_VR1_ee',
    'samples'  : {
        '04_TTTo2L2Nu' : '1.00',
        #'05_ST' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'VR1_Tag_ee' : '1.00',
        'VR1_NoTag_ee' : '1.00',
        'VR1_NoJet_ee' : '1.00',
        },
    }

nuisances['Topnorm_VR1_mm']  = {
    'name'  : 'Topnorm_VR1_mm',
    'samples'  : {
        '04_TTTo2L2Nu' : '1.00',
        #'05_ST' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'VR1_Tag_mm' : '1.00',
        'VR1_NoTag_mm' : '1.00',
        'VR1_NoJet_mm' : '1.00',
        },
    }

nuisances['Topnorm_VR1_ll']  = {
    'name'  : 'Topnorm_VR1_ll',
    'samples'  : {
        '04_TTTo2L2Nu' : '1.00',
        #'05_ST' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'VR1_Tag_ll' : '1.00',
        'VR1_NoTag_ll' : '1.00',
        'VR1_NoJet_ll' : '1.00',
        },
    }

nuisances['Topnorm_VR1_sf']  = {
    'name'  : 'Topnorm_VR1_sf',
    'samples'  : {
        '04_TTTo2L2Nu' : '1.00',
        #'05_ST' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'VR1_Tag_sf' : '1.00',
        'VR1_NoTag_sf' : '1.00',
        'VR1_NoJet_sf' : '1.00',
        },
    }
"""
# rateParam tW

nuisances['tWnorm_SR1_em']  = {
    'name'  : 'Topnorm_SR1_em',
    'samples'  : {
        #'04_TTTo2L2Nu' : '1.00',
        '05_ST' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR1_Tag_em' : '1.00',
        'SR1_NoTag_em' : '1.00',
        'SR1_NoJet_em' : '1.00',
        },
    }

nuisances['tWnorm_SR1_ee']  = {
    'name'  : 'Topnorm_SR1_ee',
    'samples'  : {
        #'04_TTTo2L2Nu' : '1.00',
        '05_ST' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR1_Tag_ee' : '1.00',
        'SR1_NoTag_ee' : '1.00',
        'SR1_NoJet_ee' : '1.00',
        },
    }

nuisances['tWnorm_SR1_mm']  = {
    'name'  : 'Topnorm_SR1_mm',
    'samples'  : {
        #'04_TTTo2L2Nu' : '1.00',
        '05_ST' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR1_Tag_mm' : '1.00',
        'SR1_NoTag_mm' : '1.00',
        'SR1_NoJet_mm' : '1.00',
        },
    }

nuisances['tWnorm_SR1_ll']  = {
    'name'  : 'Topnorm_SR1_ll',
    'samples'  : {
        #'04_TTTo2L2Nu' : '1.00',
        '05_ST' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR1_Tag_ll' : '1.00',
        'SR1_NoTag_ll' : '1.00',
        'SR1_NoJet_ll' : '1.00',
        },
    }

nuisances['tWnorm_SR1_sf']  = {
    'name'  : 'Topnorm_SR1_sf',
    'samples'  : {
        #'04_TTTo2L2Nu' : '1.00',
        '05_ST' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR1_Tag_sf' : '1.00',
        'SR1_NoTag_sf' : '1.00',
        'SR1_NoJet_sf' : '1.00',
        },
    }

nuisances['tWnorm_SR2_em']  = {
    'name'  : 'Topnorm_SR2_em',
    'samples'  : {
        #'04_TTTo2L2Nu' : '1.00',
        '05_ST' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR2_Tag_em' : '1.00',
        'SR2_NoTag_em' : '1.00',
        'SR2_NoJet_em' : '1.00',
        },
    }

nuisances['tWnorm_SR2_ee']  = {
    'name'  : 'Topnorm_SR2_ee',
    'samples'  : {
        #'04_TTTo2L2Nu' : '1.00',
        '05_ST' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR2_Tag_ee' : '1.00',
        'SR2_NoTag_ee' : '1.00',
        'SR2_NoJet_ee' : '1.00',
        },
    }

nuisances['tWnorm_SR2_mm']  = {
    'name'  : 'Topnorm_SR2_mm',
    'samples'  : {
        #'04_TTTo2L2Nu' : '1.00',
        '05_ST' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR2_Tag_mm' : '1.00',
        'SR2_NoTag_mm' : '1.00',
        'SR2_NoJet_mm' : '1.00',
        },
    }

nuisances['tWnorm_SR2_ll']  = {
    'name'  : 'Topnorm_SR2_ll',
    'samples'  : {
        #'04_TTTo2L2Nu' : '1.00',
        '05_ST' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR2_Tag_ll' : '1.00',
        'SR2_NoTag_ll' : '1.00',
        'SR2_NoJet_ll' : '1.00',
        },
    }

nuisances['tWnorm_SR2_sf']  = {
    'name'  : 'Topnorm_SR2_sf',
    'samples'  : {
        #'04_TTTo2L2Nu' : '1.00',
        '05_ST' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR2_Tag_sf' : '1.00',
        'SR2_NoTag_sf' : '1.00',
        'SR2_NoJet_sf' : '1.00',
        },
    }

nuisances['tWnorm_SR3_em']  = {
    'name'  : 'Topnorm_SR3_em',
    'samples'  : {
        #'04_TTTo2L2Nu' : '1.00',
        '05_ST' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR3_Tag_em' : '1.00',
        'SR3_NoTag_em' : '1.00',
        'SR3_NoJet_em' : '1.00',
        },
    }

nuisances['tWnorm_SR3_ee']  = {
    'name'  : 'Topnorm_SR3_ee',
    'samples'  : {
        #'04_TTTo2L2Nu' : '1.00',
        '05_ST' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR3_Tag_ee' : '1.00',
        'SR3_NoTag_ee' : '1.00',
        'SR3_NoJet_ee' : '1.00',
        },
    }

nuisances['tWnorm_SR3_mm']  = {
    'name'  : 'Topnorm_SR3_mm',
    'samples'  : {
        #'04_TTTo2L2Nu' : '1.00',
        '05_ST' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR3_Tag_mm' : '1.00',
        'SR3_NoTag_mm' : '1.00',
        'SR3_NoJet_mm' : '1.00',
        },
    }

nuisances['tWnorm_SR3_ll']  = {
    'name'  : 'Topnorm_SR3_ll',
    'samples'  : {
        #'04_TTTo2L2Nu' : '1.00',
        '05_ST' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR3_Tag_ll' : '1.00',
        'SR3_NoTag_ll' : '1.00',
        'SR3_NoJet_ll' : '1.00',
        },
    }

nuisances['tWnorm_SR3_sf']  = {
    'name'  : 'Topnorm_SR3_sf',
    'samples'  : {
        #'04_TTTo2L2Nu' : '1.00',
        '05_ST' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR3_Tag_sf' : '1.00',
        'SR3_NoTag_sf' : '1.00',
        'SR3_NoJet_sf' : '1.00',
        },
    }
"""
nuisances['tWnorm_VR1_em']  = {
    'name'  : 'Topnorm_VR1_em',
    'samples'  : {
        #'04_TTTo2L2Nu' : '1.00',
        '05_ST' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'VR1_Tag_em' : '1.00',
        'VR1_NoTag_em' : '1.00',
        'VR1_NoJet_em' : '1.00',
        },
    }

nuisances['tWnorm_VR1_ee']  = {
    'name'  : 'Topnorm_VR1_ee',
    'samples'  : {
        #'04_TTTo2L2Nu' : '1.00',
        '05_ST' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'VR1_Tag_ee' : '1.00',
        'VR1_NoTag_ee' : '1.00',
        'VR1_NoJet_ee' : '1.00',
        },
    }


nuisances['tWnorm_VR1_mm']  = {
    'name'  : 'Topnorm_VR1_mm',
    'samples'  : {
        #'04_TTTo2L2Nu' : '1.00',
        '05_ST' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'VR1_Tag_mm' : '1.00',
        'VR1_NoTag_mm' : '1.00',
        'VR1_NoJet_mm' : '1.00',
        },
    }

nuisances['tWnorm_VR1_ll']  = {
    'name'  : 'Topnorm_VR1_ll',
    'samples'  : {
        #'04_TTTo2L2Nu' : '1.00',
        '05_ST' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'VR1_Tag_ll' : '1.00',
        'VR1_NoTag_ll' : '1.00',
        'VR1_NoJet_ll' : '1.00',
        },
    }

nuisances['tWnorm_VR1_sf']  = {
    'name'  : 'Topnorm_VR1_sf',
    'samples'  : {
        #'04_TTTo2L2Nu' : '1.00',
        '05_ST' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'VR1_Tag_sf' : '1.00',
        'VR1_NoTag_sf' : '1.00',
        'VR1_NoJet_sf' : '1.00',
        },
    }
"""
# rateParam WW

nuisances['WWnorm_SR1_em']  = {
    'name'  : 'WWnorm_SR1_em',
    'samples'  : {
        '06_WW' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR1_Tag_em' : '1.00',
        'SR1_NoTag_em' : '1.00',
        'SR1_NoJet_em' : '1.00',
        },
    }

nuisances['WWnorm_SR1_ee']  = {
    'name'  : 'WWnorm_SR1_ee',
    'samples'  : {
        '06_WW' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR1_Tag_ee' : '1.00',
        'SR1_NoTag_ee' : '1.00',
        'SR1_NoJet_ee' : '1.00',
        },
    }

nuisances['WWnorm_SR1_mm']  = {
    'name'  : 'WWnorm_SR1_mm',
    'samples'  : {
        '06_WW' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR1_Tag_mm' : '1.00',
        'SR1_NoTag_mm' : '1.00',
        'SR1_NoJet_mm' : '1.00',
        },
    }

nuisances['WWnorm_SR1_ll']  = {
    'name'  : 'WWnorm_SR1_ll',
    'samples'  : {
        '06_WW' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR1_Tag_ll' : '1.00',
        'SR1_NoTag_ll' : '1.00',
        'SR1_NoJet_ll' : '1.00',
        },
    }

nuisances['WWnorm_SR1_sf']  = {
    'name'  : 'WWnorm_SR1_sf',
    'samples'  : {
        '06_WW' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR1_Tag_sf' : '1.00',
        'SR1_NoTag_sf' : '1.00',
        'SR1_NoJet_sf' : '1.00',
        },
    }

nuisances['WWnorm_SR2_em']  = {
    'name'  : 'WWnorm_SR2_em',
    'samples'  : {
        '06_WW' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR2_Tag_em' : '1.00',
        'SR2_NoTag_em' : '1.00',
        'SR2_NoJet_em' : '1.00',
        },
    }

nuisances['WWnorm_SR2_ee']  = {
    'name'  : 'WWnorm_SR2_ee',
    'samples'  : {
        '06_WW' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR2_Tag_ee' : '1.00',
        'SR2_NoTag_ee' : '1.00',
        'SR2_NoJet_ee' : '1.00',
        },
    }

nuisances['WWnorm_SR2_mm']  = {
    'name'  : 'WWnorm_SR2_mm',
    'samples'  : {
        '06_WW' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR2_Tag_mm' : '1.00',
        'SR2_NoTag_mm' : '1.00',
        'SR2_NoJet_mm' : '1.00',
        },
    }

nuisances['WWnorm_SR2_ll']  = {
    'name'  : 'WWnorm_SR2_ll',
    'samples'  : {
        '06_WW' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR2_Tag_ll' : '1.00',
        'SR2_NoTag_ll' : '1.00',
        'SR2_NoJet_ll' : '1.00',
        },
    }

nuisances['WWnorm_SR2_sf']  = {
    'name'  : 'WWnorm_SR2_sf',
    'samples'  : {
        '06_WW' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR2_Tag_sf' : '1.00',
        'SR2_NoTag_sf' : '1.00',
        'SR2_NoJet_sf' : '1.00',
        },
    }

nuisances['WWnorm_SR3_em']  = {
    'name'  : 'WWnorm_SR3_em',
    'samples'  : {
        '06_WW' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR3_Tag_em' : '1.00',
        'SR3_NoTag_em' : '1.00',
        'SR3_NoJet_em' : '1.00',
        },
    }

nuisances['WWnorm_SR3_ee']  = {
    'name'  : 'WWnorm_SR3_ee',
    'samples'  : {
        '06_WW' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR3_Tag_ee' : '1.00',
        'SR3_NoTag_ee' : '1.00',
        'SR3_NoJet_ee' : '1.00',
        },
    }

nuisances['WWnorm_SR3_mm']  = {
    'name'  : 'WWnorm_SR3_mm',
    'samples'  : {
        '06_WW' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR3_Tag_mm' : '1.00',
        'SR3_NoTag_mm' : '1.00',
        'SR3_NoJet_mm' : '1.00',
        },
    }

nuisances['WWnorm_SR3_ll']  = {
    'name'  : 'WWnorm_SR3_ll',
    'samples'  : {
        '06_WW' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR3_Tag_ll' : '1.00',
        'SR3_NoTag_ll' : '1.00',
        'SR3_NoJet_ll' : '1.00',
        },
    }

nuisances['WWnorm_SR3_sf']  = {
    'name'  : 'WWnorm_SR3_sf',
    'samples'  : {
        '06_WW' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR3_Tag_sf' : '1.00',
        'SR3_NoTag_sf' : '1.00',
        'SR3_NoJet_sf' : '1.00',
        },
    }
"""
nuisances['WWnorm_VR1_em']  = {
    'name'  : 'WWnorm_VR1_em',
    'samples'  : {
        '06_WW' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        #'VR1_Tag_em' : '1.00',
        'VR1_NoTag_em' : '1.00',
        'VR1_NoJet_em' : '1.00',
        },
    }

nuisances['WWnorm_VR1_ee']  = {
    'name'  : 'WWnorm_VR1_ee',
    'samples'  : {
        '06_WW' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        #'VR1_Tag_ee' : '1.00',
        'VR1_NoTag_ee' : '1.00',
        'VR1_NoJet_ee' : '1.00',
        },
    }

nuisances['WWnorm_VR1_mm']  = {
    'name'  : 'WWnorm_VR1_mm',
    'samples'  : {
        '06_WW' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        #'VR1_Tag_mm' : '1.00',
        'VR1_NoTag_mm' : '1.00',
        'VR1_NoJet_mm' : '1.00',
        },
    }

nuisances['WWnorm_VR1_ll']  = {
    'name'  : 'WWnorm_SR1_ll',
    'samples'  : {
        '06_WW' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        #'VR1_Tag_ll' : '1.00',
        'VR1_NoTag_ll' : '1.00',
        'VR1_NoJet_ll' : '1.00',
        },
    }

nuisances['WWnorm_VR1_sf']  = {
    'name'  : 'WWnorm_SR1_sf',
    'samples'  : {
        '06_WW' : '1.00',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        #'VR1_Tag_sf' : '1.00',
        'VR1_NoTag_sf' : '1.00',
        'VR1_NoJet_sf' : '1.00',
        },
    }
"""
# Specific for 3Reg
"""
nuisances['Nojetrate']  = {
    'name'  : 'Nojetrate', 
    'samples'  : {
        'T'                             : '1.',
        '03_VZ'                            : '1.',
        '04_TTTo2L2Nu'                     : '1.',
        '06_WW'                            : '1.',
        '05_ST'                            : '1.',
        '09_TTW'                           : '1.',
        '10_TTZ'                          : '1.',
        '07_ZJetsHT_scaled'                         : '1.',
        '02_WZTo3LNu'                      : '1.',
        '11_HWW'                           : '1.',
        '13_VVV'                           : '1.',
        },
    'type'  : 'shape',
    'cuts'  : {
        'SR1_NoJet_ee' : '1.00',
        'SR1_NoJet_em' : '1.00',
        'SR1_NoJet_mm' : '1.00',
        'SR1_NoTag_ee' : '1.00',
        'SR1_NoTag_em' : '1.00',
        'SR1_NoTag_mm' : '1.00',
        'SR2_NoJet_ee' : '1.00',
        'SR2_NoJet_em' : '1.00',
        'SR2_NoJet_mm' : '1.00',
        'SR2_NoTag_ee' : '1.00',
        'SR2_NoTag_em' : '1.00',
        'SR2_NoTag_mm' : '1.00',
        #'SR3_NoJet_ee' : '1.00',
        #'SR3_NoJet_em' : '1.00',
        #'SR3_NoJet_mm' : '1.00',
        #'SR3_NoTag_ee' : '1.00',
        #'SR3_NoTag_em' : '1.00',
        #'SR3_NoTag_mm' : '1.00',
        'SR1_NoJet_ll' : '1.00',
        'SR1_NoTag_ll' : '1.00',
        'SR2_NoJet_ll' : '1.00',
        'SR2_NoTag_ll' : '1.00',
        #'SR3_NoJet_ll' : '1.00',
        #'SR3_NoTag_ll' : '1.00',
        'SR1_NoJet_sf' : '1.00',
        'SR1_NoTag_sf' : '1.00',
        'SR2_NoJet_sf' : '1.00',
        'SR2_NoTag_sf' : '1.00',
        #'SR3_NoJet_sf' : '1.00',
        #'SR3_NoTag_sf' : '1.00',
        },
    }

nuisances['Nojetrate_SR1']  = {
    'name'  : 'Nojetrate_SR1', 
    'samples'  : {
        'T'                             : '1.',
        '03_VZ'                            : '1.',
        '04_TTTo2L2Nu'                     : '1.',
        '06_WW'                            : '1.',
        '05_ST'                            : '1.',
        '09_TTW'                           : '1.',
        '10_TTZ'                          : '1.',
        '07_ZJetsHT_scaled'                         : '1.',
        '02_WZTo3LNu'                      : '1.',
        '11_HWW'                           : '1.',
        '13_VVV'                           : '1.',
        },
    'type'  : 'shape',
    'cuts'  : {
        'SR1_NoJet_ee' : '1.00',
        'SR1_NoJet_em' : '1.00',
        'SR1_NoJet_mm' : '1.00',
        'SR1_NoJet_ll' : '1.00',
        'SR1_NoJet_sf' : '1.00',
        'SR1_NoTag_ee' : '1.00',
        'SR1_NoTag_em' : '1.00',
        'SR1_NoTag_mm' : '1.00',
        'SR1_NoTag_ll' : '1.00',
        'SR1_NoTag_sf' : '1.00',
        },
    }

nuisances['Nojetrate_SR2']  = {
    'name'  : 'Nojetrate_SR2', 
    'samples'  : {
        'T'                             : '1.',
        '03_VZ'                            : '1.',
        '04_TTTo2L2Nu'                     : '1.',
        '06_WW'                            : '1.',
        '05_ST'                            : '1.',
        '09_TTW'                           : '1.',
        '10_TTZ'                          : '1.',
        '07_ZJetsHT_scaled'                         : '1.',
        '02_WZTo3LNu'                      : '1.',
        '11_HWW'                           : '1.',
        '13_VVV'                           : '1.',
        },
    'type'  : 'shape',
    'cuts'  : {
        'SR2_NoJet_ee' : '1.00',
        'SR2_NoJet_em' : '1.00',
        'SR2_NoJet_mm' : '1.00',
        'SR2_NoJet_ll' : '1.00',
        'SR2_NoJet_sf' : '1.00',
        'SR2_NoTag_ee' : '1.00',
        'SR2_NoTag_em' : '1.00',
        'SR2_NoTag_mm' : '1.00',
        'SR2_NoTag_ll' : '1.00',
        'SR2_NoTag_sf' : '1.00',
        },
    }

nuisances['Nojetrate_SR3']  = {
    'name'  : 'Nojetrate_SR3', 
    'samples'  : {
        'T'                             : '1.',
        '03_VZ'                            : '1.',
        '04_TTTo2L2Nu'                     : '1.',
        '06_WW'                            : '1.',
        '05_ST'                            : '1.',
        '09_TTW'                           : '1.',
        '10_TTZ'                          : '1.',
        '07_ZJetsHT_scaled'                         : '1.',
        '02_WZTo3LNu'                      : '1.',
        '11_HWW'                           : '1.',
        '13_VVV'                           : '1.',
        },
    'type'  : 'shape',
    'cuts'  : {
        'SR3_NoJet_ee' : '1.00',
        'SR3_NoJet_em' : '1.00',
        'SR3_NoJet_mm' : '1.00',
        'SR3_NoJet_ll' : '1.00',
        'SR3_NoJet_sf' : '1.00',
        'SR3_NoTag_ee' : '1.00',
        'SR3_NoTag_em' : '1.00',
        'SR3_NoTag_mm' : '1.00',
        'SR3_NoTag_ll' : '1.00',
        'SR3_NoTag_sf' : '1.00',
        },
    }
"""
"""
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
        'SR1_NoJet_ll' : '1.00',
        'SR1_NoJet_sf' : '1.00',
        'SR1_NoJet_em' : '1.00',
        'SR1_NoJet_ee' : '1.00',
        'SR1_NoJet_mm' : '1.00',
        },
    }

nuisances['NoJetRate_NoJetBack_SR1']  = {
    'name'  : 'NoJetRate_NoJetBack_SR1',
    'samples'  : {
        '06_WW'                            : '1.',
        #'07_ZJetsHT_scaled'                         : '1.',
        '02_WZTo3LNu'                      : '1.',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR1_NoJet_ll' : '1.00',
        'SR1_NoJet_sf' : '1.00',
        'SR1_NoJet_em' : '1.00',
        'SR1_NoJet_ee' : '1.00',
        'SR1_NoJet_mm' : '1.00',
        },
    }

nuisances['NoJetRate_DYBack_SR1']  = {
    'name'  : 'NoJetRate_DYBack_SR1',
    'samples'  : {
        '07_ZJetsHT_scaled'                         : '1.',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR1_NoJet_ll' : '1.00',
        'SR1_NoJet_sf' : '1.00',
        'SR1_NoJet_em' : '1.00',
        'SR1_NoJet_ee' : '1.00',
        'SR1_NoJet_mm' : '1.00',
        },
    }

nuisances['NoJetRate_METBack_SR1']  = {
    'name'  : 'NoJetRate_METBack_SR1',
    'samples'  : {
        '03_VZ'                            : '1.',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR1_NoJet_ll' : '1.00',
        'SR1_NoJet_sf' : '1.00',
        'SR1_NoJet_em' : '1.00',
        'SR1_NoJet_ee' : '1.00',
        'SR1_NoJet_mm' : '1.00',
        },
    }

nuisances['NoTagRate_JetBack_SR1']  = {
    'name'  : 'NoTagRate_JetBack_SR1',
    'samples'  : {
        '04_TTTo2L2Nu'                    : '1.',
        '05_ST'                           : '1.',
        '09_TTW'                          : '1.',
        '10_TTZ'                          : '1.',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR1_NoTag_ll' : '1.00',
        'SR1_NoTag_sf' : '1.00',
        'SR1_NoTag_em' : '1.00',
        'SR1_NoTag_ee' : '1.00',
        'SR1_NoTag_mm' : '1.00',
        },
    }

nuisances['NoTagRate_NoJetBack_SR1']  = {
    'name'  : 'NoTagRate_NoJetBack_SR1',
    'samples'  : {
        '06_WW'                            : '1.',
        #'07_ZJetsHT_scaled'                         : '1.',
        '02_WZTo3LNu'                      : '1.',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR1_NoTag_ll' : '1.00',
        'SR1_NoTag_sf' : '1.00',
        'SR1_NoTag_em' : '1.00',
        'SR1_NoTag_ee' : '1.00',
        'SR1_NoTag_mm' : '1.00',
        },
    }

nuisances['NoTagRate_DYBack_SR1']  = {
    'name'  : 'NoTagRate_DYBack_SR1',
    'samples'  : {
        '07_ZJetsHT_scaled'                         : '1.',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR1_NoTag_ll' : '1.00',
        'SR1_NoTag_sf' : '1.00',
        'SR1_NoTag_em' : '1.00',
        'SR1_NoTag_ee' : '1.00',
        'SR1_NoTag_mm' : '1.00',
        },
    }

nuisances['NoTagRate_METBack_SR1']  = {
    'name'  : 'NoTagRate_METBack_SR1',
    'samples'  : {
        '03_VZ'                            : '1.',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR1_NoTag_ll' : '1.00',
        'SR1_NoTag_sf' : '1.00',
        'SR1_NoTag_em' : '1.00',
        'SR1_NoTag_ee' : '1.00',
        'SR1_NoTag_mm' : '1.00',
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
        'SR2_NoJet_ll' : '1.00',
        'SR2_NoJet_sf' : '1.00',
        'SR2_NoJet_em' : '1.00',
        'SR2_NoJet_ee' : '1.00',
        'SR2_NoJet_mm' : '1.00',
        },
    }

nuisances['NoJetRate_NoJetBack_SR2']  = {
    'name'  : 'NoJetRate_NoJetBack_SR2',
    'samples'  : {
        '06_WW'                            : '1.',
        #'07_ZJetsHT_scaled'                         : '1.',
        '02_WZTo3LNu'                      : '1.',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR2_NoJet_ll' : '1.00',
        'SR2_NoJet_sf' : '1.00',
        'SR2_NoJet_em' : '1.00',
        'SR2_NoJet_ee' : '1.00',
        'SR2_NoJet_mm' : '1.00',
        },
    }

nuisances['NoJetRate_DYBack_SR2']  = {
    'name'  : 'NoJetRate_DYBack_SR2',
    'samples'  : {
        '07_ZJetsHT_scaled'                         : '1.',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR2_NoJet_ll' : '1.00',
        'SR2_NoJet_sf' : '1.00',
        'SR2_NoJet_em' : '1.00',
        'SR2_NoJet_ee' : '1.00',
        'SR2_NoJet_mm' : '1.00',
        },
    }

nuisances['NoJetRate_METBack_SR2']  = {
    'name'  : 'NoJetRate_METBack_SR2',
    'samples'  : {
        '03_VZ'                            : '1.',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR2_NoJet_ll' : '1.00',
        'SR2_NoJet_sf' : '1.00',
        'SR2_NoJet_em' : '1.00',
        'SR2_NoJet_ee' : '1.00',
        'SR2_NoJet_mm' : '1.00',
        },
    }

nuisances['NoTagRate_JetBack_SR2']  = {
    'name'  : 'NoTagRate_JetBack_SR2',
    'samples'  : {
        '04_TTTo2L2Nu'                    : '1.',
        '05_ST'                           : '1.',
        '09_TTW'                          : '1.',
        '10_TTZ'                          : '1.',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR2_NoTag_ll' : '1.00',
        'SR2_NoTag_sf' : '1.00',
        'SR2_NoTag_em' : '1.00',
        'SR2_NoTag_ee' : '1.00',
        'SR2_NoTag_mm' : '1.00',
        },
    }

nuisances['NoTagRate_NoJetBack_SR2']  = {
    'name'  : 'NoTagRate_NoJetBack_SR2',
    'samples'  : {
        '06_WW'                            : '1.',
        #'07_ZJetsHT_scaled'                         : '1.',
        '02_WZTo3LNu'                      : '1.',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR2_NoTag_ll' : '1.00',
        'SR2_NoTag_sf' : '1.00',
        'SR2_NoTag_em' : '1.00',
        'SR2_NoTag_ee' : '1.00',
        'SR2_NoTag_mm' : '1.00',
        },
    }

nuisances['NoTagRate_DYBack_SR2']  = {
    'name'  : 'NoTagRate_DYBack_SR2',
    'samples'  : {
        '07_ZJetsHT_scaled'                         : '1.',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR2_NoTag_ll' : '1.00',
        'SR2_NoTag_sf' : '1.00',
        'SR2_NoTag_em' : '1.00',
        'SR2_NoTag_ee' : '1.00',
        'SR2_NoTag_mm' : '1.00',
        },
    }

nuisances['NoTagRate_METBack_SR2']  = {
    'name'  : 'NoTagRate_METBack_SR2',
    'samples'  : {
        '03_VZ'                            : '1.',
        },
    'type'  : 'rateParam',
    'cuts'  : {
        'SR2_NoTag_ll' : '1.00',
        'SR2_NoTag_sf' : '1.00',
        'SR2_NoTag_em' : '1.00',
        'SR2_NoTag_ee' : '1.00',
        'SR2_NoTag_mm' : '1.00',
        },
    }

"""

