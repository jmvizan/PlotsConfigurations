import os
import glob
import copy
import ROOT
import subprocess
from array import array
import LatinoAnalysis.ShapeAnalysis.tdrStyle as tdrStyle

### General utilities

tdrStyle.setTDRStyle()

class Object(object):
    pass

def getBranch():

    proc=subprocess.Popen('git branch', stderr = subprocess.PIPE,stdout = subprocess.PIPE, shell = True)
    out, err = proc.communicate()

    for line in out.split("\n"): 
        if '*' in line:
            return line.replace('* ','')

def isGoodFile(filename, minSize=100000.):

    if not os.path.isfile(filename): return False
    fileSize = os.path.getsize(filename)
    return fileSize>minSize

def compile(opt):
  
    if 'base' in opt.option.lower(): directory = '$CMSSW_BASE/src/' 
    elif 'tool' in opt.option.lower() or opt.option=='': directory = '$CMSSW_BASE/src/PlotsConfigurations/Tools/'
    elif 'latino' in opt.option.lower(): directory = '$CMSSW_BASE/src/LatinoAnalysis/'
    else: directory = opt.option
    os.system('cd '+directory+' ; scram b')

### Plot utilities

def bookHistogram(name, xBins, yBins=(), title='', style=''):

    if len(yBins)==0:
        if len(xBins)==1:
            histogram = ROOT.TH1F(name, title, len(xBins[0])-1, array('d',xBins[0]))
        elif len(xBins)==3:
            histogram = ROOT.TH1F(name, title, xBins[0], xBins[1], xBins[2])
    elif len(yBins)==1:
        if len(xBins)==1:
            histogram = ROOT.TH2F(name, title, len(xBins[0])-1, array('d',xBins[0]), len(yBins[0])-1, array('d',yBins[0]))
        elif len(xBins)==3:
            histogram = ROOT.TH2F(name, title, xBins[0], xBins[1], xBins[2], len(yBins[0])-1, array('d',yBins[0]))
    elif len(yBins)==3:
        if len(xBins)==1:
            histogram = ROOT.TH2F(name, title, len(xBins[0])-1, array('d',xBins[0]), yBins[0], yBins[1], yBins[2])
        elif len(xBins)==3:
            histogram = ROOT.TH2F(name, title, xBins[0], xBins[1], xBins[2], yBins[0], yBins[1], yBins[2])

    histogram.SetTitle('')

    #histogram.GetXaxis().SetLabelFont(42)
    #histogram.GetYaxis().SetLabelFont(42)
    #histogram.GetXaxis().SetTitleFont(42)
    #histogram.GetYaxis().SetTitleFont(42)

    if style=='btv':

        histogram.GetXaxis().SetLabelSize(0.05)
        histogram.GetYaxis().SetLabelSize(0.05)
        histogram.GetXaxis().SetTitleSize(0.06)
        histogram.GetYaxis().SetTitleSize(0.06)

        histogram.GetXaxis().SetLabelOffset(0.015)
        histogram.GetYaxis().SetLabelOffset(0.01)
        histogram.GetXaxis().SetTitleOffset(0.95)
        histogram.GetYaxis().SetTitleOffset(1.25)

    elif style=='latino':

        histogram.GetXaxis().SetLabelSize(0.035)
        histogram.GetYaxis().SetLabelSize(0.035)
        histogram.GetXaxis().SetTitleSize(0.035)
        histogram.GetYaxis().SetTitleSize(0.045)

        histogram.GetXaxis().SetLabelOffset(0.015)
        histogram.GetYaxis().SetLabelOffset(0.01)
        histogram.GetXaxis().SetTitleOffset(1.35)
        histogram.GetYaxis().SetTitleOffset(1.55)

        histogram.GetXaxis().SetNdivisions(505)
        histogram.GetYaxis().SetNdivisions(505)

    return histogram

def bookCanvas(name, xSize, ySize, title=''):

    canvas = ROOT.TCanvas(name, title, xSize, ySize)

    canvas.Range(0,0,1,1)

    #canvas.SetFillColor(10)
    #canvas.SetFillStyle(4000)

    #canvas.SetBorderMode(0)
    #canvas.SetBorderSize(2)

    #canvas.SetTickx(1)
    #canvas.SetTicky(1)

    #canvas.SetLeftMargin(0.16)
    #canvas.SetRightMargin(0.02)
    #canvas.SetTopMargin(0.05)
    #canvas.SetBottomMargin(0.13)

    #canvas.SetFrameFillColor(0)
    #canvas.SetFrameFillStyle(0)
    #canvas.SetFrameBorderMode(0)

    return canvas

def bookPad(name, xlow, ylow, xup, yup, title=''):

    pad = ROOT.TPad(name, title, xlow, ylow, xup, yup)

    #pad.SetFillColor(0)

    #pad.SetBorderMode(0)
    #pad.SetBorderSize(2)

    #pad.SetTickx(1)
    #pad.SetTicky(1)

    #pad.SetLeftMargin(0.16)
    #pad.SetRightMargin(0.02)
    #pad.SetTopMargin(0.065)
    #pad.SetBottomMargin(0.13)

    #pad.SetFrameFillColor(0)
    #pad.SetFrameFillStyle(0)
    #pad.SetFrameBorderMode(0)

    return pad

### Utilities for reading and setting cfg parameters

def getCfgFileName(opt, cfgName):

    process=subprocess.Popen('grep '+cfgName+'"File" '+opt.configuration, stderr = subprocess.PIPE,stdout = subprocess.PIPE, shell = True)
    processOutput, processError = process.communicate()

    if not processOutput: 
        print 'getCfgFileName error: '+cfgName+' File line not found in '+opt.configuration
        exit() 

    return processOutput.split('=')[1].replace(' ','').replace('\'','').split('.')[0]+'.py'

def getDictionaries(optOrig, lastDictionary='nuisances'):

    dictionaryList = [ 'samples', 'cuts', 'variables', 'nuisances' ]

    lastDictionaryIndex = dictionaryList.index(lastDictionary)

    samples, cuts, variables, nuisances = {}, {}, {}, {}

    opt = copy.deepcopy(optOrig)
    opt.tag = optOrig.year+optOrig.tag

    for dic in range(lastDictionaryIndex+1):

        dictionaryCfg = getCfgFileName(opt, dictionaryList[dic])

        if os.path.exists(dictionaryCfg):
            handle = open(dictionaryCfg,'r')
            exec(handle)
            handle.close()
        else:
            print '    Error: sample cfg file', dictionaryCfg, 'not found'
            exit()

    optOrig.lumi = opt.lumi
    if   lastDictionaryIndex==0: return samples
    elif lastDictionaryIndex==1: return samples, cuts
    elif lastDictionaryIndex==2: return samples, cuts, variables
    elif lastDictionaryIndex==3: return samples, cuts, variables, nuisances

def getDictionariesInLoop(configuration, year, tag, sigset, lastDictionary='nuisances', combineAction=''):

    opt2 = Object()
    opt2.configuration, opt2.year, opt2.tag, opt2.sigset = configuration, year, tag, sigset
    if combineAction!='': opt2.combineAction = combineAction
    return getDictionaries(opt2, lastDictionary)

def getSamples(opt):

    return getDictionaries(opt, 'samples')

def getSignals(opt):

    signals, samples = {}, getSamples(opt)
    for sample in samples:
        if samples[sample]['isSignal']:
            signals[sample] = samples[sample]
    return signals

def getSamplesInLoop(configuration, year, tag, sigset, combineAction=''):

    return getDictionariesInLoop(configuration, year, tag, sigset, 'samples', combineAction)

def setFileset(fileset, sigset):

    if fileset=='':
        if sigset=='': return '' # So we are prepared to switch from 'SM' to '' if required 
        else: return '_'+sigset
    elif fileset[0]=='_': return fileset
    else: return '_'+fileset

def getTagForDatacards(tag, sigset):

    flagsToAppend = []
    for fl in range(len(sigset.split('_')[0].split('-'))-1):
        if sigset.split('-')[fl]!='SM' and sigset.split('-')[fl] not in tag: flagsToAppend.append(sigset.split('-')[fl])

    if len(flagsToAppend)!=0:
        rawtag = tag.split('_')[0]
        tag = tag.replace(rawtag, rawtag+'_'+'_'.join([ x for x in flagsToAppend ]))

    return tag

def getSignalDir(opt, year, tag, signal, directory):

    signalDirList = [ getattr(opt, directory), year ]
    tag = tag.replace('___','_')
    if '__' in tag:
        signalDirList.append(tag.replace('__','/'))
    else:
        signalDirList.append(tag) 
    if opt.sigset!='' and opt.sigset!='SM': signalDirList.append(signal)

    return '/'.join(signalDirList)

def isExotics(opt):

    return hasattr(opt, 'isExotics')

def plotAsExotics(opt):

    return 'notexotics' not in opt.option and (isExotics(opt) or 'isexotics' in opt.option)    

def mergeDirPaths(baseDir, subDir):
    
    baseDirOriginal, subDirOriginal = baseDir, subDir
    if subDir[0]=='/': return subDir
    if subDir[0]!='.': return baseDir+'/'+subDir
    if subDir[:2]=='./': subDir = subDir[2:]
    while subDir[:3]=='../':
        baseDir = baseDir.replace('/'+baseDir.split('/')[-1], '')
        subDir = subDir[3:]
    if baseDir!='' and subDir[0]!='.' and subDir[0]!='/': return baseDir+'/'+subDir 
    print 'Error: something pathological in mergeDirName:',  baseDirOriginal, subDirOriginal, '->', baseDir, subDir
 
### Tools to check or clean logs, shapes, plots, datacards and jobs

# logs

def getLogDir(opt, year, tag, sample=''):

    logDirBase = opt.logs+'/'+opt.logprocess+'__'+year+tag+'EXT'
    if sample!='': logDirBase += '/*'+sample+'*'

    logDirList = [ ]

    if opt.logprocess=='mkShapes' or (opt.sigset!='' and opt.sigset!='SM') or opt.logprocess=='*':
        logDirList.append(logDirBase.replace('EXT','__ALL'))        

    if opt.logprocess!='mkShapes' and (opt.sigset=='' or opt.sigset=='SM'):
        logDirList.append(logDirBase.replace('EXT',''))

    return ' '.join(logDirList)

def cleanDirectory(directory):

    for extension in [ '', '__ALL' ]:
        if os.path.isdir(directory.replace('*', extension)):
            os.system('rmdir --ignore-fail-on-non-empty '+directory)

def deleteDirectory(directory):

    os.system('rm -r -f '+directory)

def cleanSampleLogs(opt, year, tag, sample):

    deleteDirectory(getLogDir(opt, year, tag, sample))

def cleanLogs(opt):

    for year in opt.year.split('-'):
        for tag in opt.tag.split('-'):

            combineAction = opt.combineAction if hasattr(opt, 'combineAction') else ''
            samples = getSamplesInLoop(opt.configuration, year, tag, opt.sigset, combineAction)

            for sample in samples:
                cleanSampleLogs(opt, year, tag, sample)
  
            cleanDirectory(getLogDir(opt, year, tag))

def deleteLogs(opt):

    for year in opt.year.split('-'):
        for tag in opt.tag.split('-'):
            deleteDirectory(getLogDir(opt, year, tag))

def getLogFileList(opt, extension):

    logFileList = [ ]

    for year in opt.year.split('-'):
        for tag in opt.tag.split('-'):

            logDirList = getLogDir(opt, year, tag, '').split(' ')
            for sample in getSamplesInLoop(opt.configuration, year, tag, opt.sigset):
                logDirList += getLogDir(opt, year, tag, sample).split(' ')

            for logDir in logDirList:
                logFileList += glob.glob(logDir+'/*'+extension)

    return logFileList

def purgeLogs(opt):

    deleteDirectory(opt.logs+'/'+opt.logprocess+'__*')

# shapes

def resetShapes(opt, split, year, tag, sigset, forceReset):

    splitDir = '/'.join([ opt.shapedir, year, tag, split ])

    if 'merge' in opt.action:
        os.system('rm -f '+splitDir+'/*_temp*.root '+splitDir+'/plots_'+year+tag+'.root')

    if forceReset:

        if 'mergeall' in opt.action:
            os.system('rm -f '+getShapeFileName(opt.shapedir, year, tag, sigset, ''))

        else:

            samples = getSamplesInLoop(opt.configuration, year, tag, sigset)

            outputDir = splitDir if 'shapes' in opt.action else '/'.join([ opt.shapedir, year, tag, 'Samples' ])

            for sample in samples:
                os.system('rm -f '+outputDir+'/plots_*ALL_'+sample+'.*root')

def cleanShapes(opt):

    for year in opt.year.split('-'):
        for tag in opt.tag.split('-'):

            deleteDirectory('/'.join([ opt.shapedir, year, tag, 'AsMuchAsPossible' ]))

def deleteShapes(opt):

    for year in opt.year.split('-'):
        for tag in opt.tag.split('-'):
            deleteDirectory('/'.join([ opt.shapedir, year, tag ]))

        cleanDirectory('/'.join([ opt.shapedir, year ]))

# plots

def copyIndexForPlots(mainPlotdir, finalPlotDir):

    subDir = mainPlotdir
    for subdir in finalPlotDir.split('/'):
        if subdir not in subDir.split('/'):
            subDir += '/'+subdir
            os.system('cp ../../index.php '+subDir)

def deletePlots(opt):

    opt.shapedir = opt.plotsdir
    deleteShapes(opt)

# Datacards

def cleanSignalDatacards(opt, year, tag, signal, dryRun=False):

    cleanSignalDatacardCommandList = []

    for singleYear in year.split('-'):
        cleanSignalDatacardCommandList.append('rm -r -f '+getSignalDir(opt, singleYear, tag, signal, 'cardsdir'))

    if dryRun: return '\n'.join(cleanSignalDatacardCommandList)
    else: os.system('\n'.join(cleanSignalDatacardCommandList))

def cleanDatacards(opt):

    for year in opt.year.split('-'):
        for tag in opt.tag.split('-'):

            samples = getSamples(opt)

            for sample in samples:
                if samples[sample]['isSignal']:
                    cleanSignalDatacards(opt, year, tag, sample)

def deleteDatacards(opt):

    opt.shapedir = opt.cardsdir
    deleteShapes(opt)

def purgeDatacards(opt):

    deleteDirectory(opt.cardsdir+'/*')

# jobs

def showQueue(opt):

    if 'ifca' in os.uname()[1] or 'cloud' in os.uname()[1]: 
        print '\nAvailable queues in slurm:\n cms_main = 24 hours\n cms_med  = 8 hours\n cms_high = 3 hours\n'
    else: #cern 
        print '\nAvailable queues in condor:\n espresso     = 20 minutes\n microcentury = 1 hour\n longlunch    = 2 hours\n workday      = 8 hours\n tomorrow     = 1 day\n testmatch    = 3 days\n nextweek     = 1 week\n'

def batchQueue(opt, batchQueue):

    if 'ifca' in os.uname()[1] or 'cloud' in os.uname()[1]:
        if batchQueue not in [ 'cms_main', 'cms_med', 'cms_high' ]: 
            if opt.verbose: print 'Batch queue', batchQueue, 'not available in gridui. Setting it to cms_high'
            return 'cms_high'
    else: # cern
        if batchQueue not in ['espresso', 'microcentury', 'longlunch', 'workday', 'tomorrow', 'testmatch', 'nextweek' ]:
            if opt.verbose: print 'Batch queue', batchQueue, 'not available in lxplus. Setting it to workday'
            return 'workday'

    return batchQueue

def checkProxy(opt):

    cmd='voms-proxy-info'
    proc=subprocess.Popen(cmd, stderr = subprocess.PIPE,stdout = subprocess.PIPE, shell = True)
    out, err = proc.communicate()

    if 'Proxy not found' in err :
        print 'WARNING: No GRID proxy -> Get one first with:'
        print 'voms-proxy-init -voms cms -rfc --valid 168:0'
        exit()

    timeLeft = 0
    for line in out.split("\n"):
        if 'timeleft' in line : timeLeft = int(line.split(':')[1])

    if timeLeft < 24 :
        print 'WARNING: Your proxy is only valid for ',str(timeLeft),' hours -> Renew it with:'
        print 'voms-proxy-init -voms cms -rfc --valid 168:0'
        exit()

def getProcessIdList(opt):

    processIdList = { }

    for year in opt.year.split('-'):
        for tag in opt.tag.split('-'):

            jidFileList = [ ]

            logDirList = getLogDir(opt, year, tag, '').split(' ')
           
            if opt.sigset=='*':
                logDirList += getLogDir(opt, year, tag, '*').split(' ')
            elif 'mergesig' in opt.logprocess:
                logDirList += getLogDir(opt, year, tag, opt.sigset).split(' ')
            else:
                for sample in getSamplesInLoop(opt.configuration, year, tag, opt.sigset):
                    logDirList += getLogDir(opt, year, tag, sample).split(' ')

            for logDir in logDirList:
                jidFileList += glob.glob(logDir+'/*jid')

            for jidFile in jidFileList:

                logprocess = jidFile.replace('./','').split('__')[0].split('/')[1]
                sample = jidFile.split('__')[-1].split('.')[0]                  
  
                yearJob, tagJob = year, tag
                if '*' in year or '*' in tag:
                    yeartag = jidFile.split('s__')[1].split('/')[0].replace('__ALL','')
                    if '*' in year and '*' in tag:
                        yearJob, tagJob = yeartag, yeartag
                    elif '*' in year: yearJob = yeartag.replace(tag, '')
                    elif '*' in tag:  tagJob  = yeartag.replace(year,'')

                process=subprocess.Popen('cat '+jidFile, stderr = subprocess.PIPE,stdout = subprocess.PIPE, shell = True)
                processOutput, processError = process.communicate()

                if processOutput:

                    processId = processOutput.replace('Submitted batch job','').split('\n')[0].split('.')[0]
                    if processId not in processIdList.keys(): 
                        processIdList[processId] = { 'logprocess' : logprocess, 'year' : yearJob, 'tag' : tagJob, 'samples' : [] }
                    if sample not in processIdList[processId]['samples']: processIdList[processId]['samples'].append(sample)    

    return processIdList 

def checkJobs(opt):

    checkCommand = 'condor_q' if 'cern' in os.uname()[1] else 'squeue'

    processIdList = getProcessIdList(opt) 

    if len(processIdList.keys())==0:
        logprocessInfo = 'logprocess='+opt.logprocess+', ' if opt.logprocess!='*' else ''
        print 'No job running for '+logprocessInfo+'year='+opt.year+', tag='+opt.tag+', sigset='+opt.sigset
        return

    process=subprocess.Popen(checkCommand, stderr = subprocess.PIPE,stdout = subprocess.PIPE, shell = True)
    processOutput, processError = process.communicate()

    if processError: print processError
    
    jobInfoList = [ 'year', 'tag' ]
    if '*' in opt.logprocess: jobInfoList.insert(0, 'logprocess') 

    if processOutput:
        for processLine in processOutput.split('\n'):
            if 'JOB' in processLine: print processLine
            else:
                for processId in processIdList:
                    if processId in processLine:
                        jobInfos = ', '.join([ x+'='+processIdList[processId][x] for x in jobInfoList ])
                        print processLine+' '+jobInfos+', samples='+','.join(processIdList[processId]['samples'])

def killJobs(opt):

    killCommand = 'condor_rm ' if 'cern' in os.uname()[1] else 'scancel '

    processIdList = getProcessIdList(opt)

    if len(processIdList.keys())==0:
        logprocessInfo = 'logprocess='+opt.logprocess+', ' if opt.logprocess!='*' else ''
        print 'No job running for '+logprocessInfo+'year='+opt.year+', tag='+opt.tag+', and sigset='+opt.sigset
        
    else:
        for processId in processIdList:    
            os.system(killCommand+processId)

    cleanLogs(opt)

def printJobErrors(opt):

    for errFile in getLogFileList(opt, 'err'):

        logprocess = errFile.replace('./','').split('__')[0].split('/')[1] if '*' in opt.logprocess else ''
        sample = errFile.split('__')[-1].split('.')[0]
        yeartag = errFile.split('__')[1].split('/')[0]

        print '\n\n\n###### '+' '.join([ logprocess, sample, yeartag ])+' ######\n'
        os.system('cat '+errFile)

def printKilledJobs(opt):

    killString = '\'Job removed\'' if 'cern' in os.uname()[1] else 'TODO'

    for logFile in getLogFileList(opt, 'log'):

        process=subprocess.Popen(' '.join(['grep', killString, logFile]), stderr = subprocess.PIPE,stdout = subprocess.PIPE, shell = True)
        processOutput, processError = process.communicate()

        if processOutput:

            logprocess = logFile.replace('./','').split('__')[0].split('/')[1] if '*' in opt.logprocess else ''
            sample = logFile.split('__')[-1].split('.')[0]
            yeartag = logFile.split('__')[1].split('/')[0]

            print '\n###### '+' '.join([ logprocess, sample, yeartag ])+processOutput

### Methods for analyzing shapes 

def getShapeDirName(shapeDir, year, tag, fitoption=''):

    shapeDirList = [ shapeDir, year, tag.split('_')[0], fitoption ]

    if fitoption!='':
        tag = tag.replace('___','_')
        if '__' in tag:
            shapeDirList.append(tag.replace(tag.split('__')[0],'').replace('__','/'))

    return '/'.join(shapeDirList)

def getShapeFileName(shapeDir, year, tag, sigset, fileset, fitoption=''):

    shapeDirList = [ shapeDir, year, tag.split('_')[0], fitoption ]

    if fitoption!='':
        tag = tag.replace('___','_').split('__')[0]

    return getShapeDirName(shapeDir, year, tag, fitoption)+'/plots_'+tag+setFileset(fileset, sigset)+'.root'

def foundShapeFiles(opt, rawShapes=False):

    missingShapeFiles = False

    for year in opt.year.split('-'):
        for tag in opt.tag.split('-'):
            rawtag = tag.split('_')[0] if rawShapes else tag

            if not os.path.isfile(getShapeFileName(opt.shapedir, year, rawtag, opt.sigset, opt.fileset)): 
                print 'Error: input shape file', getShapeFileName(opt.shapedir, year, rawtag, opt.sigset, opt.fileset), 'is missing'
                missingShapeFiles = True
     
    return not missingShapeFiles

def countedSampleShapeFiles(shapeDir, year, tag, sample):

    sampleShapeDir = '/'.join([ shapeDir, year, tag, 'AsMuchAsPossible' ])
    return len(glob.glob(sampleShapeDir+'/plots_'+year+tag+'_ALL_'+sample+'.*.root'))

def foundSampleShapeFile(shapeDir, year, tag, sample):

    sampleShapeDir = '/'.join([ shapeDir, year, tag, 'Samples' ])
    return os.path.isfile(sampleShapeDir+'/plots_'+year+tag+'_ALL_'+sample+'.root')

def openRootFile(fileName, mode='READ'):

    return ROOT.TFile(fileName, mode)

def openShapeFile(shapeDir, year, tag, sigset, fileset):

    return openRootFile(getShapeFileName(shapeDir, year, tag, sigset, fileset))

def mergeDataTakingPeriodShapes(opt, years, tag, fileset, strategy='deep', outputdir=None, inputnuisances=None, outputnuisances=None, verbose=False):

    mergeCommandList = [ '--inputDir='+opt.shapedir, '--years='+years, '--tag='+tag, '--sigset='+fileset, '--nuisancesFile='+inputnuisances ]
    if verbose: mergeCommandList.append('--verbose')

    if strategy=='deep': mergeCommandList.extend([ '--outputShapeDir='+outputdir, '--skipLNN' ])
    else:                mergeCommandList.extend([ '--outputNuisFile='+outputnuisances, '--saveNuisances' ])

    os.system('mergeDataTakingPeriodShapes.py '+' '.join( mergeCommandList ))

def yieldsTables(opt, masspoints=''):

    if 'fit' in opt.option.lower(): postFitYieldsTables(opt, masspoints)
    else: 
        print 'please, complete me :('
        print 'using postFitYieldsTables for the time being'
        opt.option += 'prefit'
        postFitYieldsTables(opt, masspoints)

def systematicsTables(opt):

    print 'please, port me from https://github.com/scodella/PlotsConfigurations/blob/worker/Configurations/SUS-19-XXX/mkSystematicsTables.py :('

def mkPseudoData(opt, reftag=None, refsigset=None):
  
    optionCommand = ''
    if opt.verbose: optionCommand += ' --verbose'
    if reftag!=None: optionCommand += ' --reftag='+reftag
    if refsigset!=None: optionCommand += ' --refsigset='+refsigset

    for year in opt.year.split('-'):
        os.system('mkPseudoData.py --year='+year+' --tag='+opt.tag+' --sigset='+opt.sigset+optionCommand)

### Modules for analyzing results from combine

def getCombineOptionFlag(option, isForPlot=False):

    combineOptionFlag = '_Toy' if 'toy' in option.lower() else ''
    if 'asimovb' in option.lower(): combineOptionFlag = '_asimovB'
    if 'asimovs' in option.lower(): combineOptionFlag = '_asimovS'
    if 'asimovi' in option.lower(): combineOptionFlag = '_asimovI'
    if not isForPlot: return combineOptionFlag
    else:
        if combineOptionFlag=='': return 'FitsToData'
        else: return combineOptionFlag.replace('_a', 'A')

def getCombineOutputFileName(opt, signal, year='', tag='', combineAction=''):

    if year=='': year = opt.year
    if tag=='': tag = opt.tag
    if getCombineOptionFlag(opt.option) not in tag: tag += getCombineOptionFlag(opt.option)

    if hasattr(opt, 'combineAction'):
        combineAction = opt.combineAction

    if combineAction=='limits':
        combineOutDir = 'limitdir'
        limitRun = 'Both' if opt.unblind else 'Blind'
        outputFileName = 'higgsCombine_'+limitRun+'.AsymptoticLimits.mH120.root'
    elif combineAction=='mlfits': 
        combineOutDir = 'mlfitdir'
        outputFileName = 'fitDiagnostics'+getCombineOptionFlag(opt.option)+'.root'
    elif combineAction=='impacts':
        combineOutDir = 'impactdir'
        outputFileName = 'impacts.pdf'
    else:
        print 'Error in getCombineOutputFileName: please speficy if you want the output from a limit or a ML fit'
        exit()

    return getSignalDir(opt, year, tag, signal, combineOutDir)+'/'+outputFileName

def openCombineLimitFile(opt, signal, year='', tag=''):

    return openRootFile(getCombineLimitFileName(opt, signal, year, tag))

def getCombineLimitFileName(opt, signal, year='', tag=''):

    return getCombineOutputFileName(opt, signal, year, tag, 'limits')

def openCombineFitFile(opt, signal, year='', tag=''):

    return openRootFile(getCombineFitFileName(opt, signal, year, tag))

def getCombineFitFileName(opt, signal, year='', tag=''):

    return getCombineOutputFileName(opt, signal, year, tag, 'mlfits')

def goodCombineFit(opt, year, tag, signal, fitoption):

    fitFile = openRootFile(getCombineFitFileName(opt, signal, year, tag))
    if not fitFile.Get('shapes_'+fitoption.lower().replace('postfit','fit_')): return False
    return True

def deleteLimits(opt):

    opt.shapedir = opt.limitdir
    deleteShapes(opt)

def purgeLimits(opt):

    deleteDirectory(opt.limitdir+'/*')

def deleteMLFits(opt):

    opt.shapedir = opt.mlfitdir
    deleteShapes(opt)

def purgeMLFits(opt):

    deleteDirectory(opt.mlfitdir+'/*')

def massScanLimits(opt):

    print 'please, port me from https://github.com/scodella/PlotsConfigurations/blob/worker/Configurations/SUS-19-XXX/analyzeLimits.py :('

def fitMatrices(opt):

    signals = getSignals(opt)
    yearList = opt.year.split('-') if 'split' in opt.option else [ opt.year ]    

    fitlevels = []
    if 'prefit' in opt.option.lower(): fitlevels.append('prefit')
    elif 'postfitb' in opt.option.lower(): fitlevels.append('fit_b')
    elif 'postfits' in opt.option.lower(): fitlevels.append('fit_s')
    else: print 'Error in fitMatrices: please choose a fit level (prefit, postfitb, postfits)'

    for year in yearList:
        for tag in opt.tag.split('-'):
            for fitlevel in fitlevels:

                opt2 = copy.deepcopy(opt)
                opt2.year, opt2.tag = year, year+tag
                signals = getSignals(opt2)
                luminosity = int(round(opt.lumi, 0)) if opt.lumi>100 else round(opt.lumi, 1)
                legend = '\'L = '+str(luminosity)+'/fb (#sqrt{s} = 13 TeV)\''
                fitoption = fitlevel.replace('prefit','PreFit').replace('fit_b','PostFitB').replace('fit_s','PostFitS')
                mainOutputDir = '/'.join([ opt.plotsdir, year, tag, getCombineOptionFlag(opt.option,True) ])        

                commandList = [ '--postFit='+fitlevel, '--legend='+legend ]
                if 'nosavecov' not in opt.option.lower(): commandList.append('--saveCovariance')
                if 'cutsToRemove:' in opt.option:
                    commandList.append('--cutsToRemove='+opt.option.split('cutsToRemove:')[1].split(':')[0])
                if 'nuisToRemove:' in opt.option:
                    commandList.append('--nuisToRemove='+opt.option.split('nuisToRemove:')[1].split(':')[0])
 
                for signal in signals:

                    signalCommandList = commandList
                    signalCommandList.append('--inputFile='+getCombineFitFileName(opt, signal, year, tag))
                    signalCommandList.append('--outputDir='+'/'.join([ mainOutputDir, fitoption, signal ]))
                    signalCommandList.append('--signal='+signal)

                    if not 'onlynuis' in opt.option.lower(): os.system('mkMatrixPlots.py '+' '.join(signalCommandList))
                    if not 'onlycuts' in opt.option.lower(): os.system('mkMatrixPlots.py '+' '.join(signalCommandList+['--doNuisances']))
                    copyIndexForPlots(opt.plotsdir, '/'.join([ mainOutputDir, fitoption, signal ]))

def postFitYieldsTables(opt, cardNameStructure='cut', masspoints=''):

    yearList = opt.year.split('-') if 'split' in opt.option else [ opt.year ]

    if 'prefit' in opt.option.lower(): fittype = 'PreFit'
    elif 'postfitb' in opt.option.lower(): fittype = 'PostFitB'
    else: fittype = 'PostFitS'

    for year in yearList:
        for tag in opt.tag.split('-'):

            commandList = [ '--tag='+year+tag, '--year='+year, '--fit='+fittype, '--cardName='+cardNameStructure, '--masspoints='+masspoints ]

            commandList.append('--inputDirMaxFit='+'/'.join([ opt.mlfitdir, year, tag ]))
            commandList.append('--outputTableDir='+'/'.join([ opt.tabledir, year, tag ]))

            if opt.unblind: commandList.append('--unblind')
            if 'nosignal' in opt.option: commandList.append('--nosignal')
    
            os.system('mkPostFitYieldsTables.py '+' '.join(commandList))

### Methods for computing weights, efficiencies, scale factors, etc.

def triggerEfficiencies(opt):

    print 'please, port me from https://github.com/scodella/PlotsConfigurations/blob/worker/Configurations/SUS-19-XXX/mkTriggerEfficiencies.py :('

def theoryNormalizations(opt):

    print 'please, port me from https://github.com/scodella/PlotsConfigurations/blob/worker/Configurations/SUS-19-XXX/computeTheoryNormalizations.py :('

def backgroundScaleFactors(opt):

    print 'please, port me fromhttps://github.com/scodella/PlotsConfigurations/blob/worker/Configurations/SUS-19-XXX/mkBackgroundScaleFactors.py :('

