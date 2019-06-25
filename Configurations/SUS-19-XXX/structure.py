
# structure configuration for datacard

#structure = {}

# keys here must match keys in samples.py    

# Background              
      
structure['ttbar']  = {  
                  'isSignal' : 0,
                  'isData'   : 0 
              }             
      
structure['tW']  = {  
                  'isSignal' : 0,
                  'isData'   : 0 
              }            
      
structure['WW']  = {  
                  'isSignal' : 0,
                  'isData'   : 0 
              }            
      
structure['ZZ']  = {  
                  'isSignal' : 0,
                  'isData'   : 0 
              }             
      
structure['WZ']  = {  
                  'isSignal' : 0,
                  'isData'   : 0 
              }           
      
structure['ttZ']  = {  
                  'isSignal' : 0,
                  'isData'   : 0 
              }            
      
structure['ttW']  = {  
                  'isSignal' : 0,
                  'isData'   : 0 
              }                 
      
structure['HWW']  = {  
                  'isSignal' : 0,
                  'isData'   : 0 
              }       
      
structure['VZ']  = {  
                  'isSignal' : 0,
                  'isData'   : 0 
              }            
      
structure['VVV']  = {  
                  'isSignal' : 0,
                  'isData'   : 0 
              }            
      
structure['DY']  = {  
                  'isSignal' : 0,
                  'isData'   : 0 
              }

# Signal             
    
#exec(open(opt.signalMassPointsFile).read())
#exec(open('./signalMassPoints.py').read())

for model in signalMassPoints:
    if model in opt.sigset:
        for massPoint in signalMassPoints[model]:
            if massPoint in opt.sigset:  

                structure[massPoint]  = {  
                    'isSignal' : 1,
                    'isData'   : 0 
                }

# Data

structure['DATA']  = { 
                  'isSignal' : 0,
                  'isData'   : 1 
              }

