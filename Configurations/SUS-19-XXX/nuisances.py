# nuisances

#nuisances = {}

# name of samples here must match keys in samples.py 
        
#### Luminosity
nuisances['lumi']  = {
               'name'  : 'lumi_13TeV',
               'samples'  : {
                   'ttbar'    : '1.023',
                   },
               'type'  : 'lnN',
              }
"""
nuisances['btag1b']  = {
               'name'  : 'btagb',
               'samples'  : {
                   'ttbar'    : ['btagWeight_1tag_b_up/btagWeight_1tag', 'btagWeight_1tag_b_down/btagWeight_1tag'],
                   },
               'kind'  : 'weight',
               'type'  : 'shape',
               'cuts'  : [
                 'TwoLep_em_tag',
                ]           
              }

nuisances['btag0b']  = {
               'name'  : 'btagb',
               'samples'  : {
                   'ttbar'    : ['(1.-btagWeight_1tag_b_up)/(1.-btagWeight_1tag)', '(1.-btagWeight_1tag_b_down)/(1.-btagWeight_1tag)'],
                   },
               'kind'  : 'weight',
               'type'  : 'shape',
               'cuts'  : [
                 'TwoLep_em_notag',
                ]           
              }
"""
