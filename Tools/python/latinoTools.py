import os
import copy
import commonTools

### Shapes

def mkShapesMulti(opt, splits):

    opt.batchQueue = commonTools.batchQueue(opt.batchQueue)

    for year in opt.year.split('-'):
        for tag in opt.tag.split('-'):

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

    commonTools.cleanLogs(opt)
    splits = getSplits(opt)
    mkShapesMulti(opt, splits)

def mergesingle(opt):

    splits = getSplits(opt)
    mkShapesMulti(opt, splits)

def mergeall(opt):

    splits = { 'Samples' : [ opt.sigset ] }
    mkShapesMulti(opt, splits)

### Plots

def mkPlot(opt, year, tag, nuisances):

    plotAsExotics = commonTools.plotAsExotics(opt)

    fileyear, fitType = year, ''
    if 'fit' in opt.option.lower():
        fileyear = opt.year
        fitType  = commmonTools.fitType(opt.option)
        if fitType=='PostFitS': plotAsExotics = False

    shapeFileName = commonTools.getShapeFileName(opt.shapedir, fileyear, tag, opt.sigset, opt.fileset, fitType)
    plotsDir = '/'.join([ opt.plotsdir, fileyear, fitType+tag ])
    if fileyear!=year: plotsDir += '/'+year
    if opt.sigset!='SM': plotsDir += '/'+opt.sigset

    os.system('mkdir -p '+plotsDir+' ; cp ../../index.php '+opt.plotsdir)

    subDir = opt.plotsdir
    for subdir in plotsDir.split('/'):
        if subdir not in subDir:
            subDir += '/'+subdir
            os.system('cp ../../index.php '+subDir)

    plotCommand = 'mkPlot.py --pycfg='+opt.configuration+' --tag='+year+tag+' --sigset='+opt.sigset+' --inputFile='+shapeFileName+' --outputDirPlots='+plotsDir+' --maxLogCratio=1000 --minLogCratio=0.1 --scaleToPlot=2 --nuisancesFile='+nuisances

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

def mergedPlots(opt):

    for tag in opt.tag.split('-'):

        opt2 = commonTools.Object()
        opt2 = copy.deepcopy(opt)
        opt2.tag = tag           
        opt2.nuisances = commonTools.getCfgFileName(opt, 'nuisances') if 'nonuisance' not in opt.option else 'None'
        commonTools.mergeShapes(opt2) 
        
        mkPlot(opt, opt.year, tag, opt2.nuisances)
        os.system('rm -f nuisances_*.py')

def postfitPlots(opt):

    if 'fit' not in opt.option.lower():
        print 'plotsPostFit error: please chose a fit option (prefit, postfit, postfits)'
        exit()

    commonTools.postfitShapes(opt)

    yearList = opt.year.split('-')
    if len(yearList)>1:
        yearList.append(opt.year)

    for year in yearList:
        mkPlot(opt, year, opt.tag, 'None')

def plots(opt):

    if 'merge' in opt.option: mergedPlots(opt)
    elif 'fit' in opt.option.lower(): postfitPlots(opt)
    else: 

        if not commonTools.foundShapeFiles(opt): exit()

        nuisances = commonTools.getCfgFileName(opt, 'nuisances') if 'nonuisance' not in opt.option else 'None'

        for year in opt.year.split('-'):
            for tag in opt.tag.split('-'):
                mkPlot(opt, year, tag, nuisances)

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

    if not commonTools.foundShapeFiles(opt): exit()

    commonTools.cleanDatacards(opt)

    fileset, sigset = getPerSignalSigset(opt.fileset, opt.sigset)

    samples = commonTools.getSamples(opt)

    for year in opt.year.split('-'):
        for tag in opt.tag.split('-'):
 
            inputtag = tag.split('_')[0]

            for sample in samples:
                if samples[sample]['isSignal']:

                    outputDir = commonTools.getSignalDir(opt, year, tag, sample, 'cardsdir')

                    os.system('mkdir -p '+outputDir)

                    datacardCommand = 'mkDatacards.py --pycfg='+opt.configuration+' --tag='+year+opt.tag+' --sigset='+sigset.replace('MASSPOINT',sample)+' --outputDirDatacard='+outputDir+' --inputFile='+commonTools.getShapeFileName(opt.shapedir, year, inputtag, '', fileset)

                    if dryRun: return datacardCommand 
                    else: os.system(datacardCommand)

