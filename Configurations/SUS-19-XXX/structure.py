
# structure configuration for datacard

#structure = {}

# keys here must match keys in samples.py   

for sample in samples:

    structure[sample] = {
                  'isSignal' : samples[sample]['isSignal'],
                  'isData'   : samples[sample]['isDATA']
    }

    cutToRemove = [ ] 

    for cut in cuts:
        if ('SR' in cut and 'isControlSample' in samples[sample] and samples[sample]['isControlSample']==1) or ('CR' in cut and samples[sample]['isSignal']==1):
            cutToRemove.append(cut)

    if len(cutToRemove)>0:
        structure[sample]['removeFromCuts'] = cutToRemove


                                     
