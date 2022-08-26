### nuisances = {}

### statistical uncertainty

nuisances['stat']  = {
              'type'          : 'auto',   # Use the following if you want to apply the automatic combine MC stat nuisances.
              'maxPoiss'      : '10',     # Number of threshold events for Poisson modelling
              'includeSignal' : '1', # Include MC stat nuisances on signal processes (1=True, 0=False)
              'samples'       : {}
             }

### rate parameters

for cut in cuts:
    for sample in samples:
        if not samples[sample]['isDATA']:
 
            nuisances[sample+'_'+cut]  = { 'name'  : sample+'_'+cut,
                                           'samples'  : { sample : '1.' },
                                           'type'  : 'rateParam',
                                           'cuts'  : [ cut ] 
                                          }


