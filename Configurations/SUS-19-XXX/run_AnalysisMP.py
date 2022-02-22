#!/usr/bin/env python
import timeit
import optparse
import sys, os

gridui=True
#To be updated to a more general option
#if gridui is True:
#    SUS19='/gpfs/users/pmatorra/CMSSW_10_2_14/src/PlotsConfigurations/Configurations/SUS-19-XXX/'
#else:
cmsenv=' eval `scramv1 runtime -sh` '
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
SUS19 = dname

if __name__ == '__main__':
    doDC=False
    args=sys.argv
    if len(args)<4:
        print 'Please, specify year, tag and sigset values, in that order'
        sys.exit()

    if args[1]=='-1':
        yearset='2016-2017-2018'
    elif args[1]=='0':
        yearset='2016'
    elif args[1]=='1':
        yearset='2017'
    elif args[1]=='2':
        yearset='2018'
    else:
        yearset=args[1]

    if   args[2]== '0':
        tag='Preselection'
    elif args[2]== '1':
        tag='ValidationRegions'
    elif args[2]=='2':
        tag='StopSignalRegions'
    else:
        tag=args[2]

    #    tag=args[2]

    sigset    = args[3]
    signm     = sigset.split('_')[0]
    fileset   = sigset
    allMP     = False
    doDCopts  = ["dodatacards","dodc", "mkdc","makedatacards"]

    doDC      = ' '
    argfloc   = 0
    limrun    = ' '

    print "before the loop"
    for arg in args[4:]:
        print "args", arg, sigset.split('_')[0]
        if arg.lower() in doDCopts : doDC    = True
        if signm       in arg      : fileset = arg
        if "limrun=" in arg.lower():
            limrun = arg.split("limrun=")[1].split(' ')[0]
            print "this is limrun", limrun



    #dcIdx = 4
    '''
    if len(sys.argv)>=5:
        if os.getenv('USER') in sys.argv[4]:
            SUS19 = sys.argv[4]
            dcIdx = 5
    dcnms=  ["dodatacards","dodc","mkdc","makedatacards"]
    if len(sys.argv)==dcIdx+1:
        if(sys.argv[dcIdx].lower()in dcnms):
            doDC=True
            fileset=sigset
        else:
            fileset=sys.argv[dcIdx]
    elif len(sys.argv)==dcIdx+2:
        fileset=sys.argv[dcIdx] 
        if(sys.argv[dcIdx+1].lower()in dcnms):
            doDC=True
    else:
        fileset=sigset

    if 'SM-' not in fileset:
        fileset = 'SM-' + fileset
    #print sys.argv[4].lower()
    '''
    opts= "--years="+yearset+" --tag="+tag+" --sigset="+sigset 
    if len(limrun)>1: opts+=" --limrun="+limrun
    print "opts", opts
    cmdDatacards =' '
    if(doDC is True):    cmdDatacards += './run_mkDatacards.py '+yearset+' '+tag+ ' '+ sigset+' '+ fileset + ' ;'
    name='python run_CombineTools.py'
    command= ' '+name+' '+opts
    print "Command sent:\t", command,'\n','CWD:', os.getcwd()
    if doDC: print " datacards:\n", cmdDatacards
    else: print "datacards are not made"
    os.system('cd '+ SUS19+ '; '+cmsenv+';'+ cmdDatacards +command)
    if doDC:
        for year in yearset.split('-'):
            for masspoint in sigset.split(','):
                os.system('cd '+SUS19+'; rm -r ./Datacards/'+year+'/'+tag+'/'+masspoint)

    years = yearset.split('-')
