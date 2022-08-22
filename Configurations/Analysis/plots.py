# plots = {}


# plot configuration

### General parameters

if opt.lumi>100: lumi_i=int(round(opt.lumi, 0))
else           : lumi_i=round(opt.lumi, 1)
legend['lumi'] = 'L = '+str(lumi_i)+'/fb'
legend['sqrt'] = '#sqrt{s} = '+opt.CME+' TeV'

### groupPlot = {}
# 
# Groups of samples to improve the plots.
# If not defined, normal plots is used
#

# ...

## #plot = {}

# keys here must match keys in samples.py    
#    

if 'SM' in opt.sigset or 'MC' in opt.sigset:

    plot['QCDMu']       = { 'nameHR' : 'QCD MuEnriched',
                            'nameLatex' : '\\QCDMu',
                            'color': 4,  
                            'isSignal' : 0,
                            'isData'   : 0, 
                            'scale'    : 1.,
                           }

    lightName = 'udsg' if 'cjets' in samples else 'udsg + c'

    plot['light']       = { 'nameHR' : lightName,
                            'nameLatex' : lightName,
                            'color': 600, #'kBlue',
                            'isSignal' : 0,
                            'isData'   : 0,
                            'scale'    : 1.,
                           }

    plot['cjets']       = { 'nameHR' : 'c',
                            'nameLatex' : 'c',
                            'color': 416, #'kGreen',
                            'isSignal' : 0,
                            'isData'   : 0,
                            'scale'    : 1.,
                           }
 
    plot['bjets']       = { 'nameHR' : 'b',
                            'nameLatex' : 'b',
                            'color': 632, #'kRed',
                            'isSignal' : 0,
                            'isData'   : 0,
                            'scale'    : 1.,
                           }

### samples and groups to be removed from plots               

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

### data

if 'SM' in opt.sigset or 'Data' in opt.sigset:

    plot['DATA']             = { 'nameHR' : 'Data',
                                 'color': 1 ,  
                                 'isSignal' : 0,
                                 'isData'   : 1,
                                 #'isBlind'  : 1
                                }

### Signal  

### cuts to be removed from group

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
        




