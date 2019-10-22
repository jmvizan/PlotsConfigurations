### nuisances

### general parameters
if '2016' in opt.tag : 
    year = '_2016'
    lumi_uncertainty = '1.025'
elif '2017' in opt.tag : 
    year = '_2017'
    lumi_uncertainty = '1.023'
elif '2018' in opt.tag : 
    year = '_2018'
    lumi_uncertainty = '1.025'

###nuisances = {}
 
### statistical uncertainty

nuisances['stat']  = {
              'type'  : 'auto',   # Use the following if you want to apply the automatic combine MC stat nuisances.
              'maxPoiss'  : '10',     # Number of threshold events for Poisson modelling
              'includeSignal'  : '1', # Include MC stat nuisances on signal processes (1=True, 0=False)
              'samples' : {}
             }

### lnN

# luminosity -> https://twiki.cern.ch/twiki/bin/view/CMS/TWikiLUM#TabLum
nuisances['lumi']  = {
               'name'  : 'lumi_13TeV'+year,
               'samples'  : { },
               'type'  : 'lnN',
              }
for sample in samples.keys():
    if sample!='DATA':
        nuisances['lumi']  ['samples'][sample] = lumi_uncertainty 

# background normalization

### shapes

# b-tagging scale factors
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

# LHE weights

# JES and MET

# mt2ll backgrounds

mt2llRegions = ['Veto', 'SR1_', 'SR2_', 'SR3_']
mt2llBins = ['Bin4', 'Bin5', 'Bin6', 'Bin7']
mt2llEdges = ['60.', '80.', '100.', '120.', '999999999.']
mt2llSystematics = [0.05, 0.10, 0.20, 0.30]

for mt2llregion in mt2llRegions: 
    for mt2llbin in range(len(mt2llBins)):

        mt2llsystname = mt2llregion + mt2llBins[mt2llbin]
        mt2llweightUp = '(mt2ll>='+mt2llEdges[mt2llbin]+' && mt2ll<'+mt2llEdges[mt2llbin+1]+') ? '+str(1.+mt2llSystematics[mt2llbin])+' : 1.'  
        mt2llweightDo = '(mt2ll>='+mt2llEdges[mt2llbin]+' && mt2ll<'+mt2llEdges[mt2llbin+1]+') ? '+str(1.-mt2llSystematics[mt2llbin])+' : 1.'  
        
        nuisances['Top_'+mt2llsystname]  = {
               'name'  : 'Top_'+mt2llsystname+year,
               'samples'  : { 
                   'ttbar' : [ mt2llweightUp, mt2llweightDo],
                   'tW'    : [ mt2llweightUp, mt2llweightDo],
               },
               'kind'  : 'weight',
               'type'  : 'shape',
               'cuts'  : [ ]           
              }
        
        nuisances['WW_'+mt2llsystname]  = {
               'name'  : 'WW_'+mt2llsystname+year,
               'samples'  : { 
                   'WW' : [ mt2llweightUp, mt2llweightDo],
               },
               'kind'  : 'weight',
               'type'  : 'shape',
               'cuts'  : [ ]           
              }

        for cut in cuts.keys():
            if mt2llregion in cut:
                nuisances['Top_'+mt2llsystname]['cuts'].append(cut)
                nuisances['WW_' +mt2llsystname]['cuts'].append(cut)

# rate parameters

for mt2llregion in mt2llRegions: 

    rateparamname = mt2llregion+'rateparam'

    nuisances['Top_'+rateparamname]  = {
        'name'  : 'Top_'+rateparamname+year,
        'samples'  : {
            '04_TTTo2L2Nu' : '1.00',
            '05_ST' : '1.00',
        },
        'type'  : 'rateParam',
        'cuts'  : [ ] 
    }

    for cut in cuts.keys():
        if mt2llregion in cut:
            nuisances['Top_'+rateparamname]['cuts'].append(cut)

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


