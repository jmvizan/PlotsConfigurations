# plot configuration
if opt.lumi>100: lumi_i=int(opt.lumi)
else           : lumi_i=round(opt.lumi, 1)
legend['lumi'] = 'L = '+str(lumi_i)+'/fb'
legend['sqrt'] = '#sqrt{s} = 13 TeV'

sl  = '#font[12]{l}'
sllatex = '\\font[12]{l}'

# groupPlot = {}
# 
# Groups of samples to improve the plots.
# If not defined, normal plots is used
#

if 'SM' in opt.sigset or 'Backgrounds' in opt.sigset:

    groupPlot['ttbar']  = {
        'nameHR' : 't#bar{t}',
        'nameLatex' : '\\ttbar',
        'isSignal' : 0,
        'color': 400,   # kYellow
        'samples'  : ['ttbar'] 
    }

    groupPlot['WW']  = {
        'nameHR' : 'WW',
        'nameLatex' : '\\WW',
        'isSignal' : 0,
        'color': 851,    # kAzure-9
        'samples'  : ['WW'] 
    }

    groupPlot['tW']  = {
        'nameHR' : 'tW',
        'nameLatex' : '\\tW',
        'isSignal' : 0,
        'color': 403,   # kYellow+3
        'samples'  : ['STtW', 'tW'] 
    }

    groupPlot['DY']  = {
        'nameHR' : 'Drell-Yan',
        'nameLatex' : '\\DY',
        'isSignal' : 0,
        'color': 418,    # kGreen+2
        'samples'  : ['DY'] 
    }

    groupPlot['EOYDrellYan']  = {
        'nameHR' : 'EOY Drell-Yan',
        'nameLatex' : 'EOY \\DY',
        'isSignal' : 0,
        'color': 418,    # kGreen+2
        'fill' : 3005,
        'samples'  : ['EOYDrellYan']
    }

    groupPlot['ZZ']  = {
        'nameHR' : 'ZZ (#rightarrow 2' + sl + '2#nu)',
        'nameLatex' : '\\ZZ ($\\to 2\\ell 2\\nu$)',
        'isSignal' : 0,
        'color': 803,   # kOrange+3
        'samples'  : ['ZZTo2L2Nu', 'ZZ'] 
    }

    groupPlot['ttZ']  = {
        'nameHR' : 't#bar{t}Z',
        'nameLatex' : '\\ttZ',
        'isSignal' : 0,
        'color': 802,   # kOrange+2
        'samples'  : ['ttZ'] 
    }
    
    groupPlot['WZ']  = {
        'nameHR' : 'WZ (#rightarrow 3' + sl + ')',
        'nameLatex' : '\\WZ ($\\to 3\\ell\\nu$)',
        'isSignal' : 0,
        'color': 798,    # kOrange-2
        'samples'  : ['WZ'] 
    }
     
    groupPlot['EOYVZ']  = {
        'nameHR' : 'EOY WZ+ggZZ',
        'nameLatex' : 'EOY WZ+ggZZ',
        'isSignal' : 0,
        'color': 798,    # kOrange-2
        'fill' : 3005,
        'samples'  : ['EOYVZ']
    }

    groupPlot['Others']  = {  
        'nameHR' : 'Minor bkg.',
        'isSignal' : 0,
        'color': 394, #  kYellow-6
        'samples'  : ['ttW', 'VVV', 'Higgs', 'VZ', 'HWW']
    }

    groupPlot['EOYOthers']  = {
        'nameHR' : 'EOY Minor bkg.',
        'isSignal' : 0,
        'color': 394, #  kYellow-6
        'fill' : 3005,
        'samples'  : ['EOYQQ', 'EOYH', 'EOY3V' ]
    }
  
    groupPlot['ZZTo4L'] = {
        'nameHR' : 'ZZ (#rightarrow 4' + sl +')',
        'nameLatex' : '\\ZZ ($\\to 4\\ell$)',
        'isSignal' : 0,
        'color': 49,
        'samples' : ['ZZTo4L']
    }

    groupPlot['EOYZZTo4L'] = {
        'nameHR' : 'EOY ZZ (#rightarrow 4' + sl +')',
        'nameLatex' : 'EOY \\ZZ ($\\to 4\\ell$)',
        'isSignal' : 0,
        'color': 49,
        'fill' : 3005,
        'samples' : ['EOYZZ4L']
    }

    if 'SameSignValidationRegion' in opt.tag:

        groupPlot['ttSemilep']  = {
            'nameHR' : 't#bar{t} Semilep.',
            'nameLatex' : '\\ttbar Semilep.',
            'isSignal' : 0,
            'color': 401,   # kYellow+1
            'samples'  : ['ttSemilep'] 
        }

        groupPlot['ttbar']['nameHR'] += ' Dilep.'
        groupPlot['ttbar']['nameLatex'] += ' Dilep.'
 
    else:

        groupPlot['ttbar']['samples'].extend(['ttSemilep'])

    groupPlot['WJetsToLNu']  = {
        'nameHR' : 'W+jets (#rightarrow ' + sl + '#nu)',
        'nameLatex' : '\\PW+jets ($\\to\\ell\\nu$)',
        'isSignal' : 0,
        'color': 38,
        'samples'  : ['WJetsToLNu']
    }

    groupPlot['EOYWJets']  = {
        'nameHR' : 'EOY W+jets (#rightarrow ' + sl + '#nu)',
        'nameLatex' : 'EOY \\PW+jets ($\\to\\ell\\nu$)',
        'isSignal' : 0,
        'color': 38,
        'fill' : 3005,
        'samples'  : ['EOYWJets']
    }

#plot = {}

# keys here must match keys in samples.py    
#                    

if 'SM' in opt.sigset or 'Backgrounds' in opt.sigset:
    
    plot['DY']  = {  
        'nameHR' : 'Drell-Yan',
        'nameLatex' : '\\DY',
        'color': 418,    # kGreen+2
        'isSignal' : 0,
        'isData'   : 0, 
        'scale'    : 1.   ,
    }
    
    plot['ZZTo2L2Nu'] = { 
        'nameHR' : 'ZZ (#rightarrow 2' + sl + '2#nu)',
        'nameLatex' : '\\ZZ ($\\to 2\\ell 2\\nu$)',
        'color'    : 803,   # kOrange+3
        'isSignal' : 0,
        'isData'   : 0,
        'scale'    : 1.0
    }
    
    plot['ttZ'] = { 
        'nameHR' : 't#bar{t}Z',
        'nameLatex' : '\\ttZ',
        'color'    : 802,   # kOrange+2
        'isSignal' : 0,
        'isData'   : 0,
        'scale'    : 1.0
    }
    
    plot['WZ']  = {
        'nameHR' : 'WZ (#rightarrow 3' + sl + ')',  
        'nameLatex' : '\\WZ ($\\to 3\\ell\\nu$)',
        'color': 798,    # kOrange-2
        'isSignal' : 0,
        'isData'   : 0,
        'scale'    : 1.0                  
    }
    
    plot['WW']  = {  
        'nameHR' : 'WW',
        'nameLatex' : '\\WW',
        'color': 851,    # kAzure-9
        'isSignal' : 0,
        'isData'   : 0,
        'scale'    : 1.0                  
    }
    
    plot['STtW'] = {
        'nameHR' : 'tW',
        'nameLatex' : '\\tW',
        'color': 403,   # kYellow+3
        'isSignal' : 0,
        'isData'   : 0 ,
        'scale'    : 1.0
    }
    
    plot['ttbar'] = {   
        'nameHR' : 't#bar{t}',
        'nameLatex' : '\\ttbar',
        'color': 400,   # kYellow
        'isSignal' : 0,
        'isData'   : 0 ,
        'scale'    : 1.0
    }
    
    plot['ttSemilep'] = {   
        'nameHR' : 't#bar{t} Semilep.',
        'nameLatex' : '$\\ttbar Semilep.',
        'color': 401,   # kYellow+1
        'isSignal' : 0,
        'isData'   : 0 ,
        'scale'    : 1.0
    }
    
    plot['ttW'] = { 
        'nameHR' : 't#bar{t}W',
        'nameLatex' : '\\ttW',
        'color'    : 394, #  kYellow-6
        'isSignal' : 0,
        'isData'   : 0,
        'scale'    : 1.0
    }
    
    plot['VZ'] = { 
        'nameHR' : 'VZ (#rightarrow 2' + sl + '2q)',
        'nameLatex' : '\\VZ ($\\to 2\\ell 2\\Pq$)',
        'color'    : 394, #  kYellow-6
        'isSignal' : 0,
        'isData'   : 0,
        'scale'    : 1.0
    }
        
    plot['VVV'] = { 
        'nameHR' : 'VVV',
        'nameLatex' : '\\VVV',   
        'color'    : 394, #  kYellow-6
        'isSignal' : 0,
        'isData'   : 0,
        'scale'    : 1.0
    }

    plot['Higgs'] = { 
        'nameHR' : 'H #rightarrow WW/#tau#tau',
        'nameLatex' : '$\\PH\\to \\WW /\\tautau$',
        'color'    : 394, #  kYellow-6
        'isSignal' : 0,
        'isData'   : 0,
        'scale'    : 1.0
    }

    plot['ZZTo4L'] = {   
        'nameHR' : 'ZZ (#rightarrow 4' + sl +')',
        'nameHR' : '\\ZZ ($\\to 4\ell$)',
        'color': 49,   
        'isSignal' : 0,
        'isData'   : 0 ,
        'scale'    : 1.0
    }

    plot['WJetsToLNu'] = {
        'nameHR' : 'W+jets (#rightarrow ' + sl + '#nu)',
        'nameLatex' : '\\PW+jets ($\\to\\ell\\nu$)',
        'color': 38,
        'isSignal' : 0,
        'isData'   : 0 ,
        'scale'    : 1.0
    }

    if 'EOY' in opt.tag:
        plot['EOYZZ4L']       = plot['ZZTo4L']
        plot['EOYH']          = plot['Higgs']
        plot['EOYQQ']         = plot['VZ']
        plot['EOYVZ']         = plot['WZ']
        plot['EOYDrellYan']   = plot['DY']
        plot['EOY3V']         = plot['VVV']
        plot['EOYWJets']      = plot['WJetsToLNu']

    # Backward compatibility for background names
    plot['tW']  = plot['STtW']
    plot['ZZ']  = plot['ZZTo2L2Nu']
    plot['HWW'] = plot['Higgs']

sampleToRemoveFromPlot = [ ] 

for sample in plot:
    if sample not in samples:
        sampleToRemoveFromPlot.append(sample)

for sample in sampleToRemoveFromPlot:
    del plot[sample]

groupToRemoveFromPlot = [ ] 

for group in groupPlot:
    for sample in sampleToRemoveFromPlot:
        if sample in groupPlot[group]['samples']:
            groupPlot[group]['samples'].remove(sample)
    if len(groupPlot[group]['samples'])==0:
        groupToRemoveFromPlot.append(group)
    
for group in groupToRemoveFromPlot:
    del groupPlot[group]

# data

if 'SM' in opt.sigset or 'Data' in opt.sigset:

    plot['DATA']  = { 
        'nameHR' : 'Data',
        'color': 1 ,  
        'isSignal' : 0,
        'isData'   : 1 ,
        #'isBlind'  : 1
    }

# Signal  

signalColor = 1 if opt.postFit=='n' else 880 # kViolet

LSP = '#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{0}}}#kern[-1.3]{#scale[0.85]{_{1}}}'
CHR = '#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{#pm}}}#kern[-1.3]{#scale[0.85]{_{1}}}'
STP = '#tilde{t}'

for model in signalMassPoints:
    if model in opt.sigset:
        for massPoint in signalMassPoints[model]:
            if massPointInSignalSet(massPoint, opt.sigset):

                massPointName = massPoint.replace('_mS-', ' m_{'+STP+'}=').replace('_mC-', ' m_{'+CHR+'}=').replace('_mX-', ' m_{'+LSP+'}=')
                massPointNameLatex = massPoint.replace('_mS-', ' \\invM{\\PSQtDo}=').replace('_mC-', ' \\invM{\\PSGcpmDo}=').replace('_mX-', ', \\invM{\\PSGczDo}=')
                #massPointNameLatex = massPointNameLatex.replace('TChipmSlepSnu', '\\PSGcpmDo\\PSGcpmDo, \\TChipmDecay,') 
                #massPointNameLatex = massPointNameLatex.replace('T2tt', '\\PSQtDo\\PASQtDo, \\PSQtDo\\to\\PQt\\PSGczDo,')
                massPointNameLatex = massPointNameLatex.replace('TChipmSlepSnu', '').replace('T2tt', '')
                massPointNameLatex = '\\ensuremath{'+massPointNameLatex+'}'              

                plot[massPoint]  = { 
                    'nameHR' : massPointName,
                    'nameLatex' : massPointNameLatex,
                    'color': signalColor,  
                    'isSignal' : 1,
                    'isData'   : 0,
                    'scale'    : 1.0
                }

                groupPlot[massPoint]  = {
                    'nameHR' : massPointName,
                    'nameLatex' : massPointNameLatex,
                    'isSignal' : 1,
                    'color': signalColor,  
                    'samples'  : [massPoint], 
                    'scale'    : 1.0
                }
                
                signalColor += 1

for group in groupPlot:
    cutToRemoveFromGroup = [ ]
    for cut in cuts:
        samplesInCut = [ ]
        for sample in groupPlot[group]['samples']:
            if not ('removeFromCuts' in samples[sample] and cut in samples[sample]['removeFromCuts']):
                samplesInCut.append(sample)
        if len(samplesInCut)==0:
            cutToRemoveFromGroup.append(cut)
    if len(cutToRemoveFromGroup)>0:
        groupPlot[group]['removeFromCuts'] = cutToRemoveFromGroup
        
