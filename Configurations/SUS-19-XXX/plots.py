# plot configuration

legend['lumi'] = 'L = '+str(opt.lumi)+'/fb'
legend['sqrt'] = '#sqrt{s} = 13 TeV'

sl  = '#font[12]{l}'

# groupPlot = {}
# 
# Groups of samples to improve the plots.
# If not defined, normal plots is used
#

if 'SM' in opt.sigset or 'Backgrounds' in opt.sigset:

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
    
    if '2018' not in opt.tag :
        groupPlot['Others']  = {  
            'nameHR' : 'Minor bkg.',
            'isSignal' : 0,
            'color': 394, #  kYellow-6
            'samples'  : ['ttW', 'VZ', 'VVV', 'HWW']
        }
    elif '2018' in opt.tag : 
        groupPlot['Others']  = {  
            'nameHR' : 'Minor bkg.',
            'isSignal' : 0,
            'color': 394, #  kYellow-6
            'samples'  : ['ttW', 'VVV', 'HWW']
        }
        
#plot = {}

# keys here must match keys in samples.py    
#                    

if 'SM' in opt.sigset or 'Backgrounds' in opt.sigset:
    
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
    
    if '2018' not in opt.tag :
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

if 'SM' in opt.sigset or 'Data' in opt.sigset:

    plot['DATA']  = { 
        'nameHR' : 'Data',
        'color': 1 ,  
        'isSignal' : 0,
        'isData'   : 1 ,
        #'isBlind'  : 1
    }

# Signal  

signalColor = 1

for model in signalMassPoints:
    if model in opt.sigset:
        for massPoint in signalMassPoints[model]:
            if massPointInSignalSet(massPoint, opt.sigset):

                massPointName = massPoint.replace('_mS-', ' m_{#stop}=').replace('_mC-', ' m_{#X^\pm}=').replace('_mX-', ' m_{#X^0}=')

                plot[massPoint]  = { 
                    'nameHR' : massPointName,
                    'color': signalColor,  
                    'isSignal' : 1,
                    'isData'   : 0,
                    'scale'    : 1.0
                }

                groupPlot[massPoint]  = {
                    'nameHR' : massPointName,
                    'isSignal' : 1,
                    'color': signalColor,  
                    'samples'  : [massPoint], 
                    'scale'    : 1.0
                }
                
                signalColor += 1
                
