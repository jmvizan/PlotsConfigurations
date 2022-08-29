import os
import copy
import commonTools
import latinoTools
from LatinoAnalysis.Tools.batchTools import *

def submitCombineJobs(opt, combineJobs):

    opt.batchQueue = commonTools.batchQueue(opt.batchQueue)
    nThreads = 1
    splitBatch =  'Targets'
    jobSplit = True if opt.sigset!='' and opt.sigset!='SM' else False

    for year in combineJobs:
        for tag in combineJobs[year]:

            targetList = combineJobs[year][tag].keys()

            if len(targetList)==0:
                print 'Noting left to submit for tag', tag, 'in year', year
                continue

            else:

                jobs = batchJobs(opt.combineAction,year+tag,['ALL'],targetList,splitBatch,'',JOB_DIR_SPLIT_READY=jobSplit)
                jobs.nThreads = nThreads

                for signal in targetList:
                    jobs.Add('ALL', signal, combineJobs[year][tag][signal])

                jobs.Sub(opt.batchQueue,opt.IiheWallTime,True)                

def setupCombineCommand(opt):

    return '\n'.join([ 'cd '+opt.combineLocation, 'eval `scramv1 runtime -sh`', 'cd '+opt.baseDir ])

def getLimitRun(unblind):

    return 'Both' if unblind else 'Blind'

def prepareDatacards(opt, dryRun=False):

    prepareDatacardCommandList = [ ]

    if 'interactive' not in opt.option:

        prepareDatacardCommandList.append('cd '+commonTools.mergeDirPaths(opt.baseDir, opt.combineSignalDir)) 

        for cfgFile in [ 'configuration', 'samples*', 'cuts', 'variables', 'nuisances', 'structure' ]:
            os.system('cp '+cfgFile+'.py '+opt.combineSignalDir) 

        os.system(' ; '.join([ 'cd '+opt.combineSignalDir, 'ln -s -f '+opt.baseDir+'/Data', 'cd '+opt.baseDir ]))

    opt.cardsdir = commonTools.mergeDirPaths(opt.baseDir, opt.cardsdir)
    opt.shapedir = commonTools.mergeDirPaths(opt.baseDir, opt.shapedir)

    prepareDatacardCommandList.append(latinoTools.datacards(opt, True))

    prepareDatacardCommand = '\n'.join(prepareDatacardCommandList)

    if dryRun: return prepareDatacardCommand
    else: os.system(prepareDatacardCommand)

def combineDatacards(opt, signal, dryRun=False):

    combineDatacardCommandList = [ setupCombineCommand(opt) ]

    combineDatacardCommandList.append('cd '+opt.combineSignalDir)

    datacardList = [ ]

    addYearToDatacardName = len(opt.year.split('-'))>1

    for year in opt.year.split('-'):

        inputDatacardDir = commonTools.mergeDirPaths(opt.baseDir, commonTools.getSignalDir(opt, year, opt.tag, signal, 'cardsdir'))

        samples, cuts, variables = commonTools.getDictionariesInLoop(opt.configuration, year, opt.tag, opt.sigset, 'variables')

        datacardNameStructure = latinoTools.getDatacardNameStructure(addYearToDatacardName, len(cuts.keys())>1, len(variables.keys())>1)
        datacardNameStructure = datacardNameStructure.replace('year', year)

        for cut in cuts:
            for variable in variables:
                if 'cuts' not in variables[variable] or cut in variables[variable]['cuts']:

                    datacardName = datacardNameStructure.replace('cut', cut).replace('variable', variable)
                    datacardFile = '/'.join([ inputDatacardDir, cut, variable, 'datacard.txt' ])   
                    datacardList.append(datacardName+'='+datacardFile)

    combineDatacardCommandList.append('combineCards.py '+' '.join(datacardList)+' > combinedDatacard.txt')

    combineDatacardCommand = '\n'.join(combineDatacardCommandList)

    if dryRun: return combineDatacardCommand
    else: os.system(combineDatacardCommand)

def runCombine(opt):

    if not commonTools.foundShapeFiles(opt, True): exit()

    if 'interactive' not in opt.option and opt.action!='writeDatacards':
        commonTools.checkProxy(opt)

    if not hasattr(opt, 'combineAction'):
        if 'limit' in opt.option: limits(opt)
        elif 'fit' in opt.option: mlfits(opt)
        else: print 'Please, speficy if you want to compute limits or make ML fits'
        exit()

    opt.logprocess = opt.combineAction
    if opt.combineLocation=='COMBINE': opt.combineLocation = os.getenv('PWD').split('/src/')[0]+'/src/'

    makeDatacards  = 'skipdatacard' not in opt.option.lower() and 'skipdc' not in opt.option.lower()
    cleanDatacards = 'keepdatacard' not in opt.option.lower() and 'keepdc' not in opt.option.lower()
    runCombineJob  = 'onlydatacard' not in opt.option.lower() and 'onlydc' not in opt.option.lower()

    if not runCombineJob:
        opt.option += 'interactive'
        cleanDatacards = False

    combineJobs = { }

    opt2 = copy.deepcopy(opt)

    opt2.baseDir = os.getenv('PWD')
    opt2.fileset, sigset = latinoTools.getPerSignalSigset(opt.fileset, opt.sigset)

    samples = commonTools.getSamples(opt)

    yearList = opt.year.split('-') if 'split' in opt.option else [ opt.year ]

    for year in yearList:

        opt2.year = year
        combineJobs[year] = { }

        for tag in opt.tag.split('-'):

            opt2.tag = tag
            combineJobs[year][tag] = { }

            for sample in samples:
                if samples[sample]['isSignal']:

                    opt2.sigset = sigset.replace('MASSPOINT', sample)
                    opt2.combineSignalDir = commonTools.getSignalDir(opt2, year, tag, sample, 'combineOutDir')

                    if runCombineJob:
                        if 'reset' in opt.option: 
                            commonTools.deleteDirectory(opt2.combineSignalDir)
                        elif os.path.isfile(commonTools.getCombineOutputFileName(opt2, sample)): 
                            continue

                    os.system('mkdir -p '+opt2.combineSignalDir)

                    combineCommandList = [ ]   

                    if makeDatacards:  combineCommandList.append(prepareDatacards(opt2, True))
                    combineCommandList.append(combineDatacards(opt2, sample, True))
                    if runCombineJob:  combineCommandList.append(' '.join(['combine', opt.combineOption, 'combinedDatacard.txt' ]))
                    combineCommandList.append( 'cd '+opt2.baseDir )
                    if cleanDatacards: combineCommandList.append(commonTools.cleanSignalDatacards(opt2, year, tag, sample, True))

                    combineCommand = '\n'.join(combineCommandList) 

                    if 'debug' in opt.option: print combineCommand
                    elif 'interactive' in opt.option: os.system(combineCommand)
                    else:
                        commonTools.cleanLogs(opt2) 
                        combineJobs[year][tag][sample] = combineCommand

    if 'debug' not in opt.option and 'interactive' not in opt.option: 
        submitCombineJobs(opt, combineJobs)
  
def writeDatacards(opt):

    opt.combineAction = 'datacard'
    opt.option        += 'onlydatacards'
    opt.combineOption  = 'dummy'
    opt.combineOutDir  = opt.cardsdir

    runCombine(opt)

def limits(opt):

    opt.combineAction = 'limits'
    limitRun = getLimitRun(opt.unblind)
    opt.combineOption = ' '.join([ '-M AsymptoticLimits', '--run '+limitRun.lower(), '-n _'+limitRun ])
    opt.combineOutDir = opt.limitdir

    runCombine(opt)

def mlfits(opt):

    opt.combineAction = 'mlfits'
    skipBOnlyFit = '--skipBOnlyFit' if 'skipbonly' in opt.option.lower() else ''
    opt.combineOption = ' '.join(['-M FitDiagnostics', '--saveShapes', '--saveWithUncertainties', skipBOnlyFit, '--saveOverallShapes' ])
    opt.combineOutDir = opt.mlfitdir

    runCombine(opt)

