#!/usr/bin/env python
import timeit
import optparse
import sys, os

#To be updated to a more general option
SUS19='/afs/cern.ch/work/p/pmatorra/private/CMSSW_10_2_14/src/PlotsConfigurations/Configurations/SUS-19-XXX/'
print "cwddir before the change", os.getcwd()
cmsenv=' eval `scramv1 runtime -sh` '
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


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
    name='python run_CombineTools.py'
    command= ' '+name+' '+opts
    print "Command sent:\t", command,'\n','CWD:', os.getcwd()
    print "ABSPATH", abspath, "\tOSCWD", os.getcwd(), "\tLONGER OPTION", os.path.dirname(os.path.realpath(__file__))
    os.system('cd '+ SUS19+ '; '+cmsenv+';'+command)

    years = yearset.split('-')
