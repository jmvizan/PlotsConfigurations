### nuisances = {}

### statistical uncertainty

nuisances['stat']  = {
              'type'          : 'auto',   # Use the following if you want to apply the automatic combine MC stat nuisances.
              'maxPoiss'      : '10',     # Number of threshold events for Poisson modelling
              'includeSignal' : '1', # Include MC stat nuisances on signal processes (1=True, 0=False)
              'samples'       : {}
             }

