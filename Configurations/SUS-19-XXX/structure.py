
# structure configuration for datacard

#structure = {}

# keys here must match keys in samples.py   

for sample in samples:

    structure[sample] = {
                  'isSignal' : samples[sample]['isSignal'],
                  'isData'   : samples[sample]['isDATA']
    }
 
    if 'removeFromCuts' in samples[sample]:
        structure[sample]['removeFromCuts'] = samples[sample]['removeFromCuts']
     
    if '_ScaleStat' in opt.tag:  
        scaleStat = float(opt.tag.split('_ScaleStat')[1])                            
        if samples[sample]['isSignal']:
            if scaleStat>=999.:
                mx = float(sample.split('_')[1].replace('mC-','').replace('mS-',''))
                my = float(sample.split('_')[2].replace('mX-',''))
                if mx-my<=100.: scaleStat = 5
                elif mx-my<=125.: scaleStat = 4
                elif mx-my<=150.: scaleStat = 3
                else: scaleStat = 2
            if '_ScaleStat9999' in opt.tag: scaleStat *= 2
            structure[sample]['scaleStatUnc'] = scaleStat
  
