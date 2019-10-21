# nuisances

# general parameters
if '2016' in opt.tag : 
    year = '_2016'
    lumi_uncertainty = '1.025'
elif '2017' in opt.tag : 
    year = '_2017'
    lumi_uncertainty = '1.023'
elif '2018' in opt.tag : 
    year = '_2018'
    lumi_uncertainty = '1.025'

#nuisances = {}

# luminosity -> https://twiki.cern.ch/twiki/bin/view/CMS/TWikiLUM#TabLum
nuisances['lumi']  = {
               'name'  : 'lumi_13TeV'+year,
               'samples'  : { },
               'type'  : 'lnN',
              }
for sample in samples.keys():
    if sample!='DATA':
        nuisances['lumi']  ['samples'][sample] = lumi_uncertainty 
 
# statistical uncertainty

# scale factors
nuisances['btag1b']  = {
               'name'  : 'btagb'+year,
               'samples'  : { },
               'kind'  : 'weight',
               'type'  : 'shape',
               'cuts'  : [ ]           
              }
for sample in samples.keys():
    if sample!='DATA':
        nuisances['btag1b']['samples'][sample] = ['btagWeight_1tag_b_up/btagWeight_1tag', 'btagWeight_1tag_b_down/btagWeight_1tag']
for cut in cuts.keys():
    if '_Tag' in cut:
        nuisances['btag1b']['cuts'].append(cut)

nuisances['btag0b']  = {
               'name'  : 'btagb'+year,
               'samples'  : { },
               'kind'  : 'weight',
               'type'  : 'shape',
               'cuts'  : [ ]           
              }
for sample in samples.keys():
    if sample!='DATA':
        nuisances['btag0b']['samples'][sample] = ['(1.-btagWeight_1tag_b_up)/(1.-btagWeight_1tag)', '(1.-btagWeight_1tag_b_down)/(1.-btagWeight_1tag)']
for cut in cuts.keys():
    if '_Veto' in cut:
        nuisances['btag0b']['cuts'].append(cut)

# background normalization

# LHE weights

# JES and MET

# mt2ll backgrounds

# rate parameters

# mt2ll signal

nuisances['mt2ll']  = {
               'name'  : 'mt2ll'+year,
               'samples'  : { },
               'kind'  : 'weight',
               'type'  : 'shape',
              }
for model in signalMassPoints:
    if model in opt.sigset:
        for massPoint in signalMassPoints[model]:
            if massPoint in opt.sigset: 
              nuisances['mt2ll']  ['samples'][massPoint] = ['1.2', '0.8'] # placeholder

