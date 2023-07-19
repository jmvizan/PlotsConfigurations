##### cuts = {}

def andCuts(cutList):
    return ' && '.join(cutList)

def orCuts(cutList, operator = ' || '):
    return '(' + operator.join([ '('+x+')' for x in cutList ]) + ')'

if 'WorkingPoints' in opt.tag:

    cuts['QCD'] = { 'expr' : 'PV_chi2<100.' } 

else:

    print 'No cut selected'


