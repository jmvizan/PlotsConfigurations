#!/usr/bin/env python
import timeit
import optparse
import sys, os
#import LatinoAnalysis.Gardener.hwwtools as hwwtools

# functions used in everyday life ...
#from LatinoAnalysis.Tools.commonTools import *
'''
COMBINE = os.getenv('COMBINE')
SUS19 = os.getenv('SUS19')
if(type(COMBINE) is None): COMBINE = " "
if(type(SUS19) is None): SUS19 = " "
'''
if __name__ == '__main__':

    if len(sys.argv)<4:
        print 'Please, specify year, tag and sigset values, in that order'
        sys.exit()

    if sys.argv[1]=='-1':
        yearset='2016-2017-2018'
    elif sys.argv[1]=='0':
        yearset='2016'
    elif sys.argv[1]=='1':
        yearset='2017'
    elif sys.argv[1]=='2':
        yearset='2018'
    else:
        yearset=sys.argv[1]

    tag=sys.argv[2]

    sigset=sys.argv[3]

    if len(sys.argv)==5:
        fileset=sys.argv[4]
    else:
        fileset=sigset
    if 'SM-' not in fileset:
        fileset = 'SM-' + fileset
    opts= "--years="+yearset+" --tag="+tag+" --sigset="+sigset
    print  "python run_CombineTools.py"+opts
    name='run_CombineTools.py'
    os.system(name+' '+opts)

    years = yearset.split('-')
