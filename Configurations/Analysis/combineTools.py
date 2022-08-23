import os
import commonTools
import latinoTools
from LatinoAnalysis.Tools.batchTools import *

def submit(opt):

    use_singularity = True if 'slc7' in os.environ['SCRAM_ARCH'] else False

    jobs = batchJobs('combine',opt.tag,['ALL'],['T2tt','T2bW'],'Targets','',JOB_DIR_SPLIT_READY=True,USE_SINGULARITY=use_singularity)

def combineDatacards(opt):
    pass

def runCombine(opt, combineOption=''):

    if 'iterative' not in opt.option:
        commonTools.checkProxy(opt)

    if combineOption=='':
        if 'limit' in opt.option: limits(opt)
        elif 'fit' in opt.option: mlfits(opt)
        else: print 'Please, speficy if you want to compute limits or make ML fits'
        exit()

    if opt.combineLocation=='COMBINE': opt.combineLocation = os.getenv('PWD').split('CMSSW_')[0]+'CMSSW_10_2_14/src/'

    makeDatacards  = 'skipdatacard' not in opt.option.lower() and 'skipdc' not opt.option.lower()
    cleanDatacards = 'keepdatacard' not in opt.option.lower() and 'keepdc' not opt.option.lower()

    opt2 = commonTools.Object()
    opt2 = opt

    opt2.fileset, sigset = getPerSignalSigset(opt.fileset, opt.sigset)

    samples = commonTools.getSamples(opt)

    yearList = opt.year.split('-') if 'split' in opt.option else opt.year

    for year in yearList:

        opt2.year = year

        for sample in samples:
            if samples[sample]['isSignal']:

                opt2.sigset = sigset.replace('MASSPOINT', sample):

                if 'iterative' in opt.option:

                    if makeDatacards: latinoTools.datacards(opt2)
                    combineDatacards(opt2)
                    if cleanDatacards: latinoTools.cleanDatacards(opt2)

                else: 

                    if makeDatacards:  combineCommand  = latinoTools.datacards(opt2, True)
                    combineCommand += combineDatacards(opt2, True)
                    if cleanDatacards: combineCommand += latinoTools.cleanDatacards(opt2, True)

def limits(opt):

    runCombine(opt, combineOption='cacca')

def mlfits(opt):

    runCombine(opt, combineOption='culo')

