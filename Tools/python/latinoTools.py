import os
import copy
import math
import commonTools
from LatinoAnalysis.Tools.batchTools import *

### Shapes

def mkShapesMulti(opt, year, tag, splits, action):

    mainDir = '/'.join([ opt.shapedir, year, tag ])

    shapeMultiCommand = 'mkShapesMulti.py --pycfg='+opt.configuration+' --treeName=Events --tag='+year+tag+' --sigset=SIGSET'
    if 'shapes' in action:
        shapeMultiCommand += ' --doBatch=True --batchQueue='+opt.batchQueue
        if opt.dryRun: shapeMultiCommand += ' --dry-run '
    else:
        shapeMultiCommand += ' --doHadd=True --doNotCleanup'

    for split in splits:
        if len(splits[split])>0:

            splitDir = mainDir + '/' + split
            os.system('mkdir -p '+splitDir)

            splitCommand = shapeMultiCommand+' --outputDir='+splitDir+' --batchSplit='+split
 
            if 'merge' in action:

                sampleFlag = '_SIGSET' if 'worker' in commonTools.getBranch() else '' 
                outputDir = mainDir if 'mergeall' in action else mainDir+'/Samples'
                splitCommand += ' ; mkdir -p '+outputDir+' ; mv '+splitDir+'/plots_'+year+tag+sampleFlag+'.root '+outputDir
                if 'mergesingle' in action: splitCommand += '/plots_'+year+tag+'_ALL_SAMPLE.root'
                else: splitCommand += '/plots_'+tag+commonTools.setFileset('',opt.sigset)+'.root'

            for sample in splits[split]:
                commonTools.resetShapes(opt, split, year, tag, sample, opt.reset)
                os.system(splitCommand.replace('SIGSET', sample).replace('SAMPLE', sample.split(':')[-1]))
 
def getSplits(opt, year, tag, action):

    splits = { 'Samples' : [ ], 'AsMuchAsPossible' : [ ] }

    samples = commonTools.getSamplesInLoop(opt.configuration, year, tag, opt.sigset)

    for sample in samples:
        treeType = samples[sample]['treeType']+':'
        if 'split' in samples[sample] and samples[sample]['split']=='AsMuchAsPossible':
            if opt.recover:
                jobsForSamples = 0
                if 'FilesPerJob' in samples[sample]: jobsForSamples = int(math.ceil(float(len(samples[sample]['name']))/samples[sample]['FilesPerJob']))
                elif 'JobsPerSample' in samples[sample]: jobsForSamples = int(samples[sample]['JobsPerSample']) 
                if jobsForSamples>0:
                    if commonTools.countedSampleShapeFiles(opt.shapedir, year, tag, sample)==jobsForSamples: continue
            splits['AsMuchAsPossible'].append(treeType+sample)
        elif 'shapes' in action:
            if opt.recover and commonTools.foundSampleShapeFile(opt.shapedir, year, tag, sample): continue
            if 'split' in samples[sample] and samples[sample]['split']=='Single':
                splits['Samples'].append(treeType+':'+sample)
            else: 
                sampleList = -1
                for ilist in range(len(splits['Samples'])):
                    if treeType in splits['Samples'][ilist] and '::' not in splits['Samples'][ilist]:
                        sampleList = ilist
                if sampleList==-1: splits['Samples'].append(treeType+sample)
                else:              splits['Samples'][sampleList] += ','+sample
                
    return splits

def shapes(opt):

    if '_' in opt.tag:
        print 'Error in shapes: one of the selecteg tags contains an \'_\'.' 
        print '                 Please use \'_\' only to set datacard options.'
        exit()

    opt.batchQueue = commonTools.batchQueue(opt.batchQueue)

    commonTools.cleanLogs(opt)

    for year in opt.year.split('-'):
        for tag in opt.tag.split('-'):
            splits = getSplits(opt, year, tag, 'shapes')
            mkShapesMulti(opt, year, tag, splits, 'shapes')

def mergesingle(opt):

    for year in opt.year.split('-'):
        for tag in opt.tag.split('-'):
            splits = getSplits(opt, year, tag, 'mergesingle')
            mkShapesMulti(opt, year, tag, splits, 'mergesingle')

def mergeall(opt):

    splits = { 'Samples' : [ opt.sigset ] }

    for year in opt.year.split('-'):
        for tag in opt.tag.split('-'):
            mkShapesMulti(opt, year, tag, splits, 'mergeall')

### Plots

def mkPlot(opt, year, tag, sigset, nuisances, fitoption='', yearInFit='', extraOutDirFlag=''):

    plotAsExotics = commonTools.plotAsExotics(opt)

    plotsDirList = [ opt.plotsdir, year ]

    if fitoption=='':
        fileset = opt.fileset
        plotsDirList.append(tag)

    else:
        fileset = ''
        if yearInFit==year: yearInFit = ''
        plotsDirList.extend([ fitoption+tag.split('___')[0].replace('__','/'), yearInFit ])
        if fitoption=='PostFitS': plotAsExotics = False

    if sigset!='SM': plotsDirList.append(sigset.split(':')[-1]+extraOutDirFlag)
    plotsDir = '/'.join(plotsDirList)

    shapeFileName = commonTools.getShapeFileName(opt.shapedir, year, tag, sigset, fileset, fitoption+yearInFit) 

    os.system('mkdir -p '+plotsDir+' ; cp ../../index.php '+opt.plotsdir)
    commonTools.copyIndexForPlots(opt.plotsdir, plotsDir)

    plotCommand = 'mkPlot.py --pycfg='+opt.configuration+' --tag='+year+tag+' --sigset='+sigset+' --inputFile='+shapeFileName+' --outputDirPlots='+plotsDir+' --maxLogCratio=1000 --minLogCratio=0.1 --scaleToPlot=2 --nuisancesFile='+nuisances

    if 'normalizedCR' in opt.option: plotCommand += ' --plotNormalizedCRratio=1' # This is not yet re-implemented in latino's mkPlot.py
    elif 'normalized' in opt.option: plotCommand += ' --plotNormalizedDistributions=1'
    elif plotAsExotics:              plotCommand += ' --showDataVsBkgOnly'       # This is not yet re-implemented in latino's mkPlot.py
    if 'noyields' not in opt.option: plotCommand += ' --showIntegralLegend=1'
    if 'saveC'        in opt.option: plotCommand += ' --fileFormats=\'png,root,C\''
    if 'plotsmearvar' in opt.option: plotCommand += ' --plotSmearVariation=1'    # This is not yet re-implemented in latino's mkPlot.py
    if 'fit' in opt.option.lower() : plotCommand += ' --postFit=p'
    if 'nostat' in opt.option.lower() : plotCommand += ' --removeMCStat'
    if 'nuisanceVariations' in opt.option: plotCommand += ' --nuisanceVariations'

    os.system(plotCommand)

    if not opt.keepallplots:
        plotToDelete = 'c_' if 'SM' in opt.sigset else 'cratio_'
        for plot2delete in [ plotToDelete, 'log_'+plotToDelete, 'cdifference_', 'log_cdifference_' ]:
            os.system('rm '+plotsDir+'/'+plot2delete+'*')

# Plot shape nuisances

def plotNuisances(opt):

   opt.fileset = commonTools.setFileset(opt.fileset, opt.sigset)
   opt.samplesFile = commonTools.getCfgFileName(opt, 'samples')
   opt.option += 'nuisanceVariations'

   for year in opt.year.split('-'):
       for tag in opt.tag.split('-'):

           opt2 = copy.deepcopy(opt)
           opt2.year, opt2.tag = year, tag
           samples, cuts, variables, nuisances = commonTools.getDictionaries(opt2)
     
           singleNuisances = {}

           for nuisance in nuisances:
               if nuisance=='stat' or ('type' in nuisances[nuisance] and nuisances[nuisance]['type']=='shape'):
                   singleNuisanceName = 'statistics' if nuisance=='stat' else nuisances[nuisance]['name']
                   if 'nuisances:' not in opt.option or singleNuisanceName in opt.option:
                       nuisanceName = 'statistics' if nuisance=='stat' else nuisance
                       if singleNuisanceName not in singleNuisances:
                           singleNuisances[singleNuisanceName] = { }
                       singleNuisances[singleNuisanceName][nuisanceName] = nuisances[nuisance]

           for singleNuisance in singleNuisances:

               opt2.option = opt.option if singleNuisance=='statistics' else opt.option+'nostat'

               backgroundList, sampleList = [], []

               for sample in samples:
                   useThisSample = singleNuisance=='statistics'
                   if not useThisSample:
                       for nuisanceName in singleNuisances[singleNuisance]:
                           if sample in nuisances[nuisanceName]['samples']:
                               useThisSample = True
                               break
                   if useThisSample:
                       if samples[sample]['isSignal']: sampleList.append(sample)
                       elif sample not in backgroundList: 
                           backgroundTreeType = samples[sample]['treeType']
                           backgroundList.append(sample)

               if len(backgroundList)>=1:
                   sampleList.append(backgroundTreeType)
                   if len(backgroundList)<=3: 
                       sampleList.append(backgroundTreeType+':'+','.join(backgroundList))                        
 
               singleNuisanceFile = './nuisance_'+singleNuisance+'_'+opt.year+opt.tag+'.py'
               with open(singleNuisanceFile, 'w') as file:
                   file.write('nuisances = '+str(singleNuisances[singleNuisance]))                   

               for samplesToPlot in sampleList:
                   opt2.sigset = samplesToPlot
                   mkPlot(opt2, year, tag, opt2.sigset, singleNuisanceFile, extraOutDirFlag='_'+singleNuisance)

               os.system('rm '+singleNuisanceFile)

# Plots merging different data taking periods (years) without combine (e.g. control regions)

def mergedPlots(opt):

    inputNuisances = commonTools.getCfgFileName(opt, 'nuisances') if 'nonuisance' not in opt.option else 'None'

    for tag in opt.tag.split('-'):

        if opt.deepMerge!=None:
            year = opt.deepMerge
            outputNuisances = inputNuisances
            outputDir = '/'.join([ opt.shapedir, year, tag ])
            commonTools.mergeDataTakingPeriodShapes(opt, opt.year, tag, opt.fileset, 'deep', outputDir, inputNuisances, 'None', opt.verbose)

        else:
            year = opt.year
            outputNuisances =  '_'.join([ 'nuisances', opt.year, opt.tag, opt.sigset+'.py' ])
            commonTools.mergeDataTakingPeriodShapes(opt, opt.year, tag, opt.fileset, '', 'None', inputNuisances, outputNuisances, opt.verbose)
        
        mkPlot(opt, year, tag, opt.sigset, outputNuisances)
        os.system('rm -f nuisances_*.py')

# Tools for making plots from combine fits

def getDatacardNameStructure(addYearToDatacardName, addCutToDatacardName, addVariableToDatacardName):

    datacardNameStructureList = [ ]
    if addCutToDatacardName: datacardNameStructureList.append('cut')
    if addVariableToDatacardName: datacardNameStructureList.append('variable')
    if addYearToDatacardName: datacardNameStructureList.append('year')
    return '_'.join(datacardNameStructureList)

def mkPostFitPlot(opt, fitoption, fittedYear, year, tag, cut, variable, signal, sigset, datacardNameStructure):

    fitkind = 'p' if fitoption=='PreFit' else fitoption[7:].lower()
    postFitPlotCommandList = [ '--kind='+fitkind, '--structureFile='+commonTools.getCfgFileName(opt, 'structure') ]
    postFitPlotCommandList.extend([ '--tag='+fittedYear+tag, '--sigset='+sigset ])

    postFitPlotCommandList.extend([ '--cutNameInOriginal='+cut, '--variable='+variable ])
    postFitPlotCommandList.append('--cut='+datacardNameStructure.replace('year', year).replace('cut', cut).replace('variable', variable))
    if fitoption=='PostFitB': postFitPlotCommandList.append('--getSignalFromPrefit=1')

    tagoption = fitoption if year==fittedYear else fitoption+year
    postFitPlotCommandList.append('--inputFileCombine='+commonTools.getCombineFitFileName(opt, signal, fittedYear, tag))
    postFitPlotCommandList.append('--inputFile='+commonTools.getShapeFileName(opt.shapedir, year, tag.split('_')[0], opt.sigset, opt.fileset))
    postFitPlotCommandList.append('--outputFile='+commonTools.getShapeFileName(opt.shapedir, fittedYear, tag, sigset, '', tagoption))

    os.system('mkPostFitPlot.py '+' '.join(postFitPlotCommandList))

def postFitPlots(opt, convertShapes=True, makePlots=True):

    fitoption = ''
    if 'prefit' in opt.option.lower(): fitoption = 'PreFit'
    elif 'postfitb' in opt.option.lower(): fitoption = 'PostFitB'
    elif 'postfits' in opt.option.lower(): fitoption = 'PostFitS'

    if fitoption=='':
        print 'plotsPostFit error: please choose a fit option (prefit, postfitb, postfits)'
        exit()

    fittedYearList = opt.year.split('-') if 'split' in opt.option else [ opt.year ]
    if 'splitandcomb' in opt.option: fittedYearList.append(opt.year)

    for tag in opt.tag.split('-'):
        for fittedYear in fittedYearList:

            yearInFitList = fittedYear.split('-')
            if 'mergeyear' in opt.option and '-' in fittedYear: yearInFitList.append('') 

            signals = commonTools.getDictionariesInLoop(opt.configuration, yearInFitList[0], tag, opt.sigset, 'samples')
            for signal in signals:
                if signals[signal]['isSignal']:

                    if not commonTools.goodCombineFit(opt, fittedYear, tag, signal, fitoption):
                        print 'Warning in postFitPlots: no good fit for year='+fittedYear+', tag='+tag+', signal='+signal+', fitoption='+fitoption

                    sigset = opt.sigset if opt.sigset=='' or opt.sigset=='SM' else 'SM-'+signal if 'SM' in opt.sigset else signal

                    for year in yearInFitList:

                        tagoption = fitoption if year==fittedYear else fitoption+year
                        postFitShapeFile = commonTools.getShapeFileName(opt.shapedir, fittedYear, tag, sigset, '', tagoption)    

                        if convertShapes or not os.path.isfile(postFitShapeFile):
 
                            os.system('rm -f '+postFitShapeFile)
                            os.system('mkdir -p '+commonTools.getShapeDirName(opt.shapedir, fittedYear, tag, tagoption))

                            if year!='':

                                samples, cuts, variables = commonTools.getDictionariesInLoop(opt.configuration, year, tag, sigset, 'variables')
                                datacardNameStructure = getDatacardNameStructure(len(fittedYear.split('-'))>1, len(cuts.keys())>1, len(variables.keys())>1)

                                for cut in cuts:
                                    for variable in variables:
                                        if 'cuts' not in variables[variable] or cut in  variables[variable]['cuts']:
                                            mkPostFitPlot(opt, fitoption, fittedYear, year, tag, cut, variable, signal, sigset, datacardNameStructure)

                            else:
                                pass

                        if makePlots:
                            mkPlot(opt, fittedYear, tag, sigset, 'None', fitoption, year)

def postFitShapes(opt):

    convertShapes = True if not opt.recover else False
    postFitPlots(opt, convertShapes, False) 

def postFitPlotsOnly(opt):

    postFitPlots(opt, False, True)

# Generic plots from mkShapes output

def plots(opt):

    if 'merge' in opt.option: mergedPlots(opt)
    elif 'fit' in opt.option.lower(): postFitPlots(opt)
    else: 

        if not commonTools.foundShapeFiles(opt): exit()

        nuisances = commonTools.getCfgFileName(opt, 'nuisances') if 'nonuisance' not in opt.option else 'None'

        for year in opt.year.split('-'):
            for tag in opt.tag.split('-'):
                mkPlot(opt, year, tag, opt.sigset, nuisances)

### Datacards

def getPerSignalSigset(inputfileset, inputsigset):

    fileset = commonTools.setFileset(inputfileset, inputsigset)

    if '-' in fileset:                       # This is SUSY like
        auxfileset = fileset if fileset[0]!='_' else fileset[1:]
        auxfileset = auxfileset.split('_')[0]
        sigset = auxfileset.replace(auxfileset.split('-')[-1], '')+'MASSPOINT'
    elif inputsigset=='' or inputsigset=='SM': # This should work for SM searches
        sigset = inputsigset
    else:                                    # Guessing latinos' usage
        sigset = 'MASSPOINT'

    return fileset, sigset

def datacards(opt, signal='', dryRun=False):

    fileset, sigset = getPerSignalSigset(opt.fileset, opt.sigset)

    if signal!='': 
        signalList = [ signal ]
    else: 
        signalList = []
        samples = commonTools.getSamples(opt)
        for sample in samples:
            if samples[sample]['isSignal']:
                signalList.append(sample)

    datacardCommandList = []

    blindData = '' if opt.unblind else ' --blindData '

    for year in opt.year.split('-'):
        for tag in opt.tag.split('-'):
            for sample in signalList:

                outputDir = commonTools.getSignalDir(opt, year, tag, sample, 'cardsdir')

                datacardCommand = 'mkdir -p '+outputDir+' \n mkDatacards.py --pycfg='+opt.configuration+' --tag='+year+opt.tag+' --sigset='+sigset.replace('MASSPOINT',sample)+' --outputDirDatacard='+outputDir+' --inputFile='+commonTools.getShapeFileName(opt.shapedir, year, tag.split('_')[0], '', fileset)+blindData

                if dryRun: datacardCommandList.append(datacardCommand) 
                else: os.system(datacardCommand)

    if dryRun: return datacardCommandList

### Batch

def submitJobs(opt, jobName, jobTag, targetList, splitBatch, jobSplit, nThreads):

    jobs = batchJobs(jobName,jobTag,['ALL'],targetList.keys(),splitBatch,'',JOB_DIR_SPLIT_READY=jobSplit)
    jobs.nThreads = nThreads

    for signal in targetList:
        jobs.Add('ALL', signal, targetList[signal])

    jobs.Sub(opt.batchQueue,opt.IiheWallTime,True)

