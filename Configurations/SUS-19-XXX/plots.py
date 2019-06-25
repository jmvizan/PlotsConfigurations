# plot configuration

legend['lumi'] = 'L = 35.9/fb'
legend['sqrt'] = '#sqrt{s} = 13 TeV'

sl  = '#font[12]{l}'

# groupPlot = {}
# 
# Groups of samples to improve the plots.
# If not defined, normal plots is used
#

groupPlot['ttbar']  = {
                        'nameHR' : 't#bar{t}',
                        'isSignal' : 0,
                        'color': 400,   # kYellow
                        'samples'  : ['ttbar'] 
                       }

groupPlot['WW']  = {
                        'nameHR' : 'WW',
                        'isSignal' : 0,
                        'color': 851,    # kAzure-9
                        'samples'  : ['WW'] 
                       }

groupPlot['tW']  = {
                        'nameHR' : 'tW',
                        'isSignal' : 0,
                        'color': 403,   # kYellow+3
                        'samples'  : ['tW'] 
                       }

groupPlot['DY']  = {
                        'nameHR' : 'Drell-Yan',
                        'isSignal' : 0,
                        'color': 418,    # kGreen+2
                        'samples'  : ['DY'] 
                       }

groupPlot['ZZ']  = {
                        'nameHR' : 'ZZ (#rightarrow 2' + sl + '2#nu)',
                        'isSignal' : 0,
                        'color': 803,   # kOrange+3
                        'samples'  : ['ZZ'] 
                       }

groupPlot['ttZ']  = {
                        'nameHR' : 't#bar{t}Z',
                        'isSignal' : 0,
                        'color': 802,   # kOrange+2
                        'samples'  : ['ttZ'] 
                       }

groupPlot['WZ']  = {
                        'nameHR' : 'WZ (#rightarrow 3' + sl + ')',
                        'isSignal' : 0,
                        'color': 798,    # kOrange-2
                        'samples'  : ['WZ'] 
                       }

groupPlot['Others']  = {  
                         'nameHR' : 'Minor bkg.',
                         'isSignal' : 0,
                         'color': 394, #  kYellow-6
                         'samples'  : ['ttW', 'VZ', 'VVV', 'HWW']
                        } 


#plot = {}

# keys here must match keys in samples.py    
#                    

plot['DY']  = {  
                  'nameHR' : 'Drell-Yan',
                  'color': 418,    # kGreen+2
                  'isSignal' : 0,
                  'isData'   : 0, 
                  'scale'    : 1.   ,
              }

plot['ZZ'] = { 
                  'nameHR' : 'ZZ (#rightarrow 2' + sl + '2#nu)',
                  'color'    : 803,   # kOrange+3
                  'isSignal' : 0,
                  'isData'   : 0,
                  'scale'    : 1.0
                  }

plot['ttZ'] = { 
                  'nameHR' : 't#bar{t}Z',
                  'color'    : 802,   # kOrange+2
                  'isSignal' : 0,
                  'isData'   : 0,
                  'scale'    : 1.0
                  }

plot['WZ']  = {
                  'nameHR' : 'WZ (#rightarrow 3' + sl + ')',  
                  'color': 798,    # kOrange-2
                  'isSignal' : 0,
                  'isData'   : 0,
                  'scale'    : 1.0                  
              }
               
plot['WW']  = {  
                  'nameHR' : 'WW',
                  'color': 851,    # kAzure-9
                  'isSignal' : 0,
                  'isData'   : 0,
                  'scale'    : 1.0                  
              }

plot['tW'] = {
                  'nameHR' : 'tW',
                  'color': 403,   # kYellow+3
                  'isSignal' : 0,
                  'isData'   : 0 ,
                  'scale'    : 1.0
                  }

plot['ttbar'] = {   
                  'nameHR' : 't#bar{t}',
                  'color': 400,   # kYellow
                  'isSignal' : 0,
                  'isData'   : 0 ,
                  'scale'    : 1.0
                  }

plot['ttW'] = { 
                  'nameHR' : 't#bar{t}W',
                  'color'    : 394, #  kYellow-6
                  'isSignal' : 0,
                  'isData'   : 0,
                  'scale'    : 1.0
                  }

plot['VZ'] = { 
                  'nameHR' : 'VZ (#rightarrow 2' + sl + '2q)',
                  'color'    : 394, #  kYellow-6
                  'isSignal' : 0,
                  'isData'   : 0,
                  'scale'    : 1.0
                  }

plot['VVV'] = { 
                  'nameHR' : 'VVV',
                  'color'    : 394, #  kYellow-6
                  'isSignal' : 0,
                  'isData'   : 0,
                  'scale'    : 1.0
                  }

plot['HWW'] = { 
                  'nameHR' : 'H #rightarrow WW',
                  'color'    : 394, #  kYellow-6
                  'isSignal' : 0,
                  'isData'   : 0,
                  'scale'    : 1.0
                  }

if 'ControlRegion-ZZ' in opt.tag:

    plot['ZZTo4L'] = {   
                       'nameHR' : 'ZZ (#rightarrow 4' + sl +')',
                       'color': 49,   
                       'isSignal' : 0,
                       'isData'   : 0 ,
                       'scale'    : 1.0
    }

# data

plot['DATA']  = { 
                  'nameHR' : 'Data',
                  'color': 1 ,  
                  'isSignal' : 0,
                  'isData'   : 1 ,
                  #'isBlind'  : 1
              }

