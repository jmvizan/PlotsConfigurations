import os
import copy
import commonTools
import latinoTools
from LatinoAnalysis.Tools.batchTools import *

def submitCombineJobs(opt, jobName, jobTag, combineJobs):

    nThreads = 1
    splitBatch =  'Targets'
    jobSplit = True if opt.sigset!='' and opt.sigset!='SM' else False

    latinoTools.submitJobs(opt, jobName, jobTag, combineJobs, splitBatch, jobSplit, nThreads)

def setupCombineCommand(opt):

    return '\n'.join([ 'cd '+opt.combineLocation, 'eval `scramv1 runtime -sh`', 'cd '+opt.baseDir ])

def getLimitRun(unblind):

    return 'Both' if unblind else 'Blind'

def prepareDatacards(opt, signal, dryRun=False):

    prepareDatacardCommandList = [ ]

    if not opt.interactive:
        prepareDatacardCommandList.append('cd '+opt.combineTagDir)

    prepareDatacardCommandList.extend(latinoTools.datacards(opt, signal, True))

    prepareDatacardCommand = '\n'.join(prepareDatacardCommandList)

    if dryRun: return prepareDatacardCommand
    else: os.system(prepareDatacardCommand)

def getDatacardList(opt, signal):

    datacardList = [ ]

    addYearToDatacardName = len(opt.year.split('-'))>1

    for year in opt.year.split('-'):

        inputDatacardDir = commonTools.mergeDirPaths(opt.baseDir, commonTools.getSignalDir(opt, year, opt.tag, signal, 'cardsdir'))
        samples, cuts, variables = commonTools.getDictionariesInLoop(opt.configuration, year, opt.tag, 'SM', 'variables', opt.combineAction)

        datacardNameStructure = latinoTools.getDatacardNameStructure(addYearToDatacardName, len(cuts.keys())>1, len(variables.keys())>1)
        datacardNameStructure = datacardNameStructure.replace('year', year)

        for cut in cuts:
            for variable in variables:
                if 'cuts' not in variables[variable] or cut in variables[variable]['cuts']:

                    datacardName = datacardNameStructure.replace('cut', cut).replace('variable', variable)
                    datacardFile = '/'.join([ inputDatacardDir, cut, variable, 'datacard.txt' ])
                    datacardList.append(datacardName+'='+datacardFile)

    return datacardList

#def combineDatacards(opt, signal, datacardList, dryRun=False):
def combineDatacards(opt, signal, dryRun=False):

    combineDatacardCommandList = [ setupCombineCommand(opt) ]

    signalOutputDir = commonTools.getSignalDir(opt, opt.year, opt.tag, signal, 'combineOutDir')
    combineDatacardCommandList.extend([ 'mkdir -p '+signalOutputDir, 'cd '+signalOutputDir ])

    #signalDatacardList = getDatacardList(opt)

    #for datacard in getDatacardList(opt):
    #    signalDatacardList.append(datacard.replace('MASSPOINT', signal))

    combineDatacardCommandList.append('combineCards.py '+' '.join(getDatacardList(opt, signal))+' > combinedDatacard.txt')

    combineDatacardCommand = '\n'.join(combineDatacardCommandList)

    if dryRun: return combineDatacardCommand
    else: os.system(combineDatacardCommand)

def prepareJobDirectory(opt):

    os.system('mkdir -p '+opt.combineTagDir)
    for cfgFile in [ 'configuration', 'samples*', 'cuts', 'variables', 'nuisances', 'structure' ]:
        os.system('cp '+cfgFile+'.py '+opt.combineTagDir)
    os.system(' ; '.join([ 'cd '+opt.combineTagDir, 'ln -s -f '+opt.baseDir+'/Data', 'cd '+opt.baseDir ]))

def runCombine(opt):

    if not commonTools.foundShapeFiles(opt, True): exit()

    if not opt.interactive and opt.action!='writeDatacards':
        commonTools.checkProxy(opt)
        opt.batchQueue = commonTools.batchQueue(opt.batchQueue)

    if not hasattr(opt, 'combineAction'):
        if 'limit' in opt.option: limits(opt)
        elif 'fit' in opt.option: mlfits(opt)
        elif 'impact' in opt.option: impactsPlots(opt)
        else: print 'Please, speficy if you want to compute limits, make ML fits, or produce impacts plots'
        exit()

    opt.logprocess = opt.combineAction
    if opt.combineLocation=='COMBINE': opt.combineLocation = os.getenv('PWD').split('/src/')[0]+'/src/'

    makeDatacards  = 'skipdatacard' not in opt.option.lower() and 'skipdc' not in opt.option.lower()
    cleanDatacards = 'keepdatacard' not in opt.option.lower() and 'keepdc' not in opt.option.lower()
    runCombineJob  = 'onlydatacard' not in opt.option.lower() and 'onlydc' not in opt.option.lower()

    if not runCombineJob:
        opt.interactive = True
        cleanDatacards = False

    opt2 = copy.deepcopy(opt)

    opt2.baseDir = os.getenv('PWD')
    opt2.cardsdir = commonTools.mergeDirPaths(opt2.baseDir, opt2.cardsdir)
    opt2.shapedir = commonTools.mergeDirPaths(opt2.baseDir, opt2.shapedir)

    opt2.fileset, baseSigset = latinoTools.getPerSignalSigset(opt.fileset, opt.sigset) 

    samples = commonTools.getSamples(opt)

    yearList = opt.year.split('-') if 'split' in opt.option else [ opt.year ]

    for year in yearList:
        for tag in opt.tag.split('-'):

            opt2.year, opt2.tag = year, tag
            #datacardList = getDatacardList(opt2)
            combineJobs = { } 

            if not opt.interactive: 
                commonTools.cleanLogs(opt2)
                opt2.combineTagDir = commonTools.mergeDirPaths(opt2.baseDir, commonTools.getSignalDir(opt2, year, tag, '', 'combineOutDir'))
                if makeDatacards: prepareJobDirectory(opt2)

            combineCommandList = [ ]
            if makeDatacards:  combineCommandList.append(prepareDatacards(opt2, 'MASSPOINT', True))
            combineCommandList.append(combineDatacards(opt2, 'MASSPOINT', True))
            if runCombineJob:  combineCommandList.append(opt.combineCommand)
            combineCommandList.append( 'cd '+opt2.baseDir )
            if cleanDatacards: combineCommandList.append(commonTools.cleanSignalDatacards(opt2, year, tag, 'MASSPOINT', True))

            combineCommand = '\n'.join(combineCommandList)

            for sample in samples:
                if samples[sample]['isSignal']:

                    #opt2.sigset = baseSigset.replace('MASSPOINT', sample)
                    if runCombineJob:
                        combineOutputFileName = commonTools.getCombineOutputFileName(opt2, sample)

                        if opt.reset: 
                            os.system('rm -f '+combineOutputFileName)
                        elif commonTools.isGoodFile(combineOutputFileName, 6000.):
                            continue

                    #os.system('mkdir -p '+opt2.combineSignalDir)

                    #combineCommandList = [ ]   
                    #if makeDatacards:  combineCommandList.append(prepareDatacards(opt2, sample, True))
                    #combineCommandList.append(combineDatacards(opt2, sample, datacardList, True))
                    #if runCombineJob:  combineCommandList.append(' '.join(['combine', opt.combineOption, 'combinedDatacard.txt' ]))
                    #combineCommandList.append( 'cd '+opt2.baseDir )
                    #if cleanDatacards: combineCommandList.append(commonTools.cleanSignalDatacards(opt2, year, tag, sample, True))

                    #combineCommand = '\n'.join(combineCommandList) 

                    signalCombineCommand = combineCommand.replace('MASSPOINT', sample)

                    if opt.debug: print signalCombineCommand
                    elif opt.interactive: os.system(signalCombineCommand)
                    else:
                        combineJobs[sample] = signalCombineCommand

            if not opt.debug and not opt.interactive:
                if len(combineJobs.keys())>0: 
                    submitCombineJobs(opt, opt.combineAction, year+tag, combineJobs)
                else:
                    print 'Noting left to submit for tag', tag, 'in year', year

def writeDatacards(opt):

    opt.combineAction = 'datacard'
    opt.option += 'onlydatacards'
    opt.combineCommand = 'dummy'
    opt.combineOutDir = opt.cardsdir

    runCombine(opt)

def limits(opt):

    opt.combineAction = 'limits'
    limitRun = getLimitRun(opt.unblind)
    opt.combineCommand = ' '.join([ 'combine -M AsymptoticLimits', '--run '+limitRun.lower(), '-n _'+limitRun, 'combinedDatacard.txt' ])
    opt.combineOutDir = opt.limitdir

    runCombine(opt)

def mlfits(opt):

    opt.combineAction = 'mlfits'
    skipBOnlyFit = '--skipBOnlyFit' if 'skipbonly' in opt.option.lower() else ''
    asimovOption = ''
    if 'asimovb' in opt.option.lower(): asimovOption = '-t -1 --expectSignal 0  -n _asimovB'
    if 'asimovs' in opt.option.lower(): asimovOption = '-t -1 --expectSignal 1  -n _asimovS'
    if 'asimovi' in opt.option.lower(): asimovOption = '-t -1 --expectSignal 15 -n _asimovI'
    opt.combineCommand = ' '.join(['combine -M FitDiagnostics', '--saveShapes', '--saveWithUncertainties', skipBOnlyFit, '--saveOverallShapes', asimovOption, 'combinedDatacard.txt' ])
    opt.combineOutDir = opt.mlfitdir

    runCombine(opt)

def impactsPlots(opt):

    opt.combineAction = 'impacts'
    asimovOption = ''
    if 'asimovb' in opt.option.lower(): asimovOption = ' -t -1 --expectSignal 0  -n _asimovB'
    if 'asimovs' in opt.option.lower(): asimovOption = ' -t -1 --expectSignal 1  -n _asimovS'
    if 'asimovi' in opt.option.lower(): asimovOption = ' -t -1 --expectSignal 15 -n _asimovI'
    autoOption = ' --autoBoundsPOIs="*"' if 'autob'  in opt.option.lower() else ''
    stepList = [ 'text2workspace.py combinedDatacard.txt']
    stepList.append('combineTool.py -M Impacts -d combinedDatacard.root -m 125 --doInitialFit --robustFit 1'+autoOption+asimovOption)
    stepList.append('combineTool.py -M Impacts -d combinedDatacard.root -m 125 --robustFit 1 --doFits --parallel 100'+autoOption+asimovOption)
    stepList.append('combineTool.py -M Impacts -d combinedDatacard.root -m 125 -o impacts.json '+autoOption+asimovOption)
    stepList.append('plotImpacts.py -i impacts.json -o impacts')
    opt.combineCommand = ' ; '.join(stepList)
    opt.combineOutDir = opt.impactdir

    runCombine(opt)




