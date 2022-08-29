import os
import copy
import commonTools

### Shapes

def mkShapesMulti(opt, year, tag, splits):

    mainDir = '/'.join([ opt.shapedir, year, tag ])

    shapeMultiCommand = 'mkShapesMulti.py --pycfg='+opt.configuration+' --treeName=Events --tag='+year+tag+' --sigset=SIGSET'
    if 'shapes' in opt.action:
        shapeMultiCommand += ' --doBatch=True --batchQueue='+opt.batchQueue
        if opt.dryRun: shapeMultiCommand += ' --dryRun '
    else:
        shapeMultiCommand += ' --doHadd=True --doNotCleanup'

    for split in splits:
        if len(splits[split])>0:

            splitDir = mainDir + '/' + split
            os.system('mkdir -p '+splitDir)

            splitCommand = shapeMultiCommand+' --outputDir='+splitDir+' --batchSplit='+split
 
            if 'merge' in opt.action:

                outputDir = mainDir if 'mergeall' in opt.action else mainDir+'/Samples'
                splitCommand += ' ; mkdir -p '+outputDir+' ; mv '+splitDir+'/plots_'+year+tag+'.root '+outputDir
                if 'mergesingle' in opt.action: splitCommand += '/plots_'+year+tag+'_ALL_SAMPLE.root'
                else: splitCommand += '/plots_'+tag+commonTools.setFileset('',opt.sigset)+'.root'

            for sample in splits[split]:

                commonTools.resetShapes(opt, split, year, tag, sample, 'reset' in opt.option)
                os.system(splitCommand.replace('SIGSET', sample).replace('SAMPLE', sample.split(':')[-1]))

def getSplits(opt):

    splits = { 'Samples' : [ ], 'AsMuchAsPossible' : [ ] }

    samples = commonTools.getSamples(opt)

    for sample in samples:
        treeType = samples[sample]['treeType']+':'
        if 'split' in samples[sample] and samples[sample]['split']=='AsMuchAsPossible':
            splits['AsMuchAsPossible'].append(treeType+sample)
        elif 'shapes' in opt.action:
            sampleList = -1
            for ilist in range(splits['Samples']):
                if treeType in splits['Samples'][ilist]:
                    sampleList = ilist
            if sampleList==-1:
                splits['Samples'].append(treeType+sample)
            else:
                splits['Samples'][sampleList] += sample
                
    return splits

def shapes(opt):

    if '_' in opt.tag:
        print 'Error in shapes: one of the selecteg tags contains an \'_\'.' 
        print '                 Please use \'_\' only to set datacard options.'
        exit()

    opt.batchQueue = commonTools.batchQueue(opt.batchQueue)

    commonTools.cleanLogs(opt)
    splits = getSplits(opt)

    for year in opt.year.split('-'):
        for tag in opt.tag.split('-'):
            mkShapesMulti(opt, year, tag, splits)

def mergesingle(opt):

    splits = getSplits(opt)

    for year in opt.year.split('-'):
        for tag in opt.tag.split('-'):
            mkShapesMulti(opt, year, tag, splits)

def mergeall(opt):

    splits = { 'Samples' : [ opt.sigset ] }

    for year in opt.year.split('-'):
        for tag in opt.tag.split('-'):
            mkShapesMulti(opt, year, tag, splits)

### Plots

def mkPlot(opt, year, tag, sigset, nuisances, fitoption='', yearInFit=''):

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

    if sigset!='SM': plotsDirList.append(sigset)
    plotsDir = '/'.join(plotsDirList)

    shapeFileName = commonTools.getShapeFileName(opt.shapedir, year, tag, sigset, fileset, fitoption+yearInFit) 

    os.system('mkdir -p '+plotsDir+' ; cp ../../index.php '+opt.plotsdir)

    subDir = opt.plotsdir
    for subdir in plotsDir.split('/'):
        if subdir not in subDir:
            subDir += '/'+subdir
            os.system('cp ../../index.php '+subDir)

    plotCommand = 'mkPlot.py --pycfg='+opt.configuration+' --tag='+year+tag+' --sigset='+sigset+' --inputFile='+shapeFileName+' --outputDirPlots='+plotsDir+' --maxLogCratio=1000 --minLogCratio=0.1 --scaleToPlot=2 --nuisancesFile='+nuisances

    if 'normalizedCR' in opt.option: plotCommand += ' --plotNormalizedCRratio=1' # This is not yet re-implemented in latino's mkPlot.py
    elif 'normalized' in opt.option: plotCommand += ' --plotNormalizedDistributions=1'
    elif plotAsExotics:              plotCommand += ' --showDataVsBkgOnly'       # This is not yet re-implemented in latino's mkPlot.py
    if 'noyields' not in opt.option: plotCommand += ' --showIntegralLegend=1'
    if 'saveC'        in opt.option: plotCommand += ' --fileFormats=\'png,root,C\''
    if 'plotsmearvar' in opt.option: plotCommand += ' --plotSmearVariation=1'    # This is not yet re-implemented in latino's mkPlot.py
    if 'fit' in opt.option.lower() : plotCommand += ' --postFit=p'

    os.system(plotCommand)

    if not opt.keepallplots:
        plotToDelete = 'c_' if 'SM' in opt.sigset else 'cratio_'
        for plot2delete in [ plotToDelete, 'log_'+plotToDelete, 'cdifference_', 'log_cdifference_' ]:
            os.system('rm '+plotsDir+'/'+plot2delete+'*')

# Plots merging different data taking periods (years) without combine (e.g. control regions)

def mergedPlots(opt):

    for tag in opt.tag.split('-'):

        opt2 = copy.deepcopy(opt)
        opt2.tag = tag           
        opt2.nuisances = commonTools.getCfgFileName(opt, 'nuisances') if 'nonuisance' not in opt.option else 'None'
        commonTools.mergeShapes(opt2) 
        
        mkPlot(opt, opt.year, tag, opt2.nuisances)
        os.system('rm -f nuisances_*.py')

# Tools for making plots from combine fits

def getDatacardNameStructure(addYearToDatacardName, addCutToDatacardName, addVariableToDatacardName):

    datacardNameStructureList = [ ]
    if addYearToDatacardName: datacardNameStructureList.append('year')
    if addCutToDatacardName: datacardNameStructureList.append('cut')
    if addVariableToDatacardName: datacardNameStructureList.append('variable')
    return '_'.join(datacardNameStructureList)

def mkPostFitPlot(opt, fitoption, fittedYear, year, tag, cut, variable, signal, sigset, datacardNameStructure):

    fitkind = 'p' if fitoption=='PreFit' else fitoption[7:].lower()
    postFitPlotCommandList = [ '--kind='+fitkind, '--structureFile='+commonTools.getCfgFileName(opt, 'structure') ]
    postFitPlotCommandList.extend([ '--tag='+tag, '--sigset='+sigset ])

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

    convertShapes = True if 'noreset' not in opt.option else False
    postFitPlots(opt, convertShapes, False) 

def postFitPlotsOnly(opt):

    postFitPlots(opt, False, True)

# Generic plots from mkShapes output

def plots(opt):

    if 'merge' in opt.option: mergedPlots(opt)
    elif 'fit' in opt.option.lower(): postfitPlots(opt)
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
        sigset = fileset.replace(fileset.split('-')[-1], '').replace('_','')+'MASSPOINT'
    elif inputsigset=='' or inputsigset=='SM': # This should work for SM searches
        sigset = inputsigset
    else:                                    # Guessing latinos' usage
        sigset = 'MASSPOINT'

    return fileset, sigset

def datacards(opt, dryRun=False):

    if not commonTools.foundShapeFiles(opt, True): exit()

    commonTools.cleanDatacards(opt)

    fileset, sigset = getPerSignalSigset(opt.fileset, opt.sigset)

    samples = commonTools.getSamples(opt)

    for year in opt.year.split('-'):
        for tag in opt.tag.split('-'):
 
            for sample in samples:
                if samples[sample]['isSignal']:

                    outputDir = commonTools.getSignalDir(opt, year, tag, sample, 'cardsdir')

                    os.system('mkdir -p '+outputDir)

                    datacardCommand = 'mkDatacards.py --pycfg='+opt.configuration+' --tag='+year+opt.tag+' --sigset='+sigset.replace('MASSPOINT',sample)+' --outputDirDatacard='+outputDir+' --inputFile='+commonTools.getShapeFileName(opt.shapedir, year, tag.split('_')[0], '', fileset)

                    if dryRun: return datacardCommand 
                    else: os.system(datacardCommand)

