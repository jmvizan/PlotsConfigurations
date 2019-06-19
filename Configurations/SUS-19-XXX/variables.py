# variables

#variables = {}
    
#   
mt2 = '#font[50]{m}_{T2}'
sll = '#font[12]{ll}'
                    
variables['mt2ll']  = {   'name'  : 'mt2ll',                #   variable name    
                          'range' : (7,0,140),              #   variable range
                          'xaxis' : mt2 + '(' + sll + ')',  #   x axis name
                          'fold'  : 1                       #   fold overflow
                          }
                    
variables['mt2llgen']  = {   'name'  : 'mt2llgen',             #   variable name    
                             'range' : (7,0,140),              #   variable range
                             'xaxis' : mt2 + '(' + sll + ')',  #   x axis name
                             'fold'  : 1                       #   fold overflow
                         }


