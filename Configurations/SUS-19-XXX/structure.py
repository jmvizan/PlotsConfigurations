
# structure configuration for datacard

#structure = {}

# keys here must match keys in samples.py    

# Background              
      
structure['ttbar']  = {  
                  'isSignal' : 0,
                  'isData'   : 0 
              }

# Signal             
      
structure['T2tt']  = {  
                  'isSignal' : 1,
                  'isData'   : 0 
              }

# Data

structure['DATA']  = { 
                  'isSignal' : 0,
                  'isData'   : 1 
              }

