import os
import glob
import ROOT
import subprocess

### General utilities

class Object(object):
    pass

### Utilities for reading and setting parameters

def getCfgFileName(opt, cfgName):

    process=subprocess.Popen('grep '+cfgName+'"File" '+opt.configuration, stderr = subprocess.PIPE,stdout = subprocess.PIPE, shell = True)
    processOutput, processError = process.communicate()

    if not processOutput: 
        print 'getCfgFileName error: '+cfgName+'File line not found in '+opt.configuration
        exit() 

    return processOutput.split('=')[1].replace(' ','').replace('\'','').split('.')[0]+'.py'

def getDictionaries(opt, lastDictionary='nuisances'):

    dictionaryList = [ 'samples', 'cuts', 'variables', 'nuisances' ]

    lastDictionaryIndex = dictionaryList.index(lastDictionary)

    samples, cuts, variables, nuisances = {}, {}, {}, {}

    for dic in range(lastDictionaryIndex+1):

        dictionaryCfg = getCfgFileName(opt, dictionaryList[dic])

        if os.path.exists(dictionaryCfg):
            handle = open(dictionaryCfg,'r')
            exec(handle)
            handle.close()
        else:
            print '    Error: sample cfg file', dictionaryCfg, 'not found'
            exit()

    if   lastDictionaryIndex==0: return samples
    elif lastDictionaryIndex==1: return samples, cuts
    elif lastDictionaryIndex==2: return samples, cuts, variables
    elif lastDictionaryIndex==3: return samples, cuts, variables, nuisances

def getDictionariesInLoop(configuration, year, tag, sigset, lastDictionary='nuisances'):

    opt2 = Object()
    opt2.configuration, opt2.year, opt2.tag, opt2.sigset = configuration, year, tag, sigset
    return getDictionaries(opt2, lastDictionary)

def getSamples(opt):

    return getDictionaries(opt, 'samples')

def getSamplesInLoop(configuration, year, tag, sigset):

    return getDictionariesInLoop(configuration, year, tag, sigset, 'samples')

def setFileset(fileset, sigset):

    if fileset=='':
        if sigset=='': return '' # So we are prepared to switch from 'SM' to '' if required 
        else: return '_'+sigset
    else:
        return '_'+fileset.replace('_','')

def isExotics(opt):

    process=subprocess.Popen('grep "isExotics" '+opt.configuration, stderr = subprocess.PIPE,stdout = subprocess.PIPE, shell = True)
    processOutput, processError = process.communicate()
    return 'True' in processOutput

def plotAsExotics(opt):

    return 'notexotics' not in opt.option and (isExotics(opt) or 'isexotics' in opt.option)    

### Cleaning logs, shapes, plots and jobs

# logs

def cleanDirectory(directory):

    if os.path.isdir(directory):
        os.system('rmdir --ignore-fail-on-non-empty '+directory)

def cleanSampleLogs(logs, year, tag, sample):

    os.system('rm -r -f '+logs+'/mkShapes__'+year+tag+'__ALL/'+sample+'*')

def cleanLogs(opt):

    for year in opt.year.split('-'):
        for tag in opt.tag.split('-'):

            samples = getSamplesInLoop(opt.configuration, year, tag, opt.sigset)

            for sample in samples:
                cleanSampleLogs(opt.logs, year, tag, sample)
  
            cleanDirectory(opt.logs+'/mkShapes__'+year+tag+'__ALL')

def deleteLogs(opt):

    for year in opt.year.split('-'):
        for tag in opt.tag.split('-'):
            os.system('rm -r '+opt.logs+'/mkShapes__'+year+tag+'__ALL')

def printError(opt):

    for year in opt.year.split('-'):
        for tag in opt.tag.split('-'):

            samples = getSamplesInLoop(opt.configuration, year, tag, opt.sigset)

            for sample in samples:

                errFileList = glob.glob(opt.logs+'/mkShapes__'+year+tag+'__ALL/'+sample+'*/*err')

                for errFile in errFileList:
                    print '\n\n\n###### '+errFile.split('__')[1]+' '+errFile.split('__')[5]+' ######\n'
                    os.system('cat '+errFile)

def purgeLogs(opt):

    os.system('rm -r '+opt.logs+'/*')

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
            os.system('rm -r '+'/'.join([ opt.shapedir, year, tag, 'AsMuchAsPossible' ]))

def deleteShapes(opt):

    for year in opt.year.split('-'):

        for tag in opt.tag.split('-'):
            os.system('rm -r '+'/'.join([ opt.shapedir, year, tag ]))

        cleanDirectory('/'.join([ opt.shapedir, year ]))

# plots

def deletePlots(opt):

    opt.shapedir = opt.plotsdir
    deleteShapes(opt)

# jobs

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

            samples = getSamplesInLoop(opt.configuration, year, tag, opt.sigset)

            for sample in samples:

                jidFileList = glob.glob(opt.logs+'/mkShapes__'+year+tag+'__ALL/'+sample+'*/*jid')

                for jidFile in jidFileList:
                    
                    yearJob, tagJob = year, tag
                    if '*' in year or '*' in tag:
                        yeartag = jidFile.split('__')[1]
                        if '*' in year and '*' in tag:
                            yearJob, tagJob = yeartag, yeartag
                        elif '*' in year: yearJob = yeartag.replace(tag, '')
                        elif '*' in tag:  tagJob  = yeartag.replace(year,'')

                    process=subprocess.Popen('cat '+jidFile, stderr = subprocess.PIPE,stdout = subprocess.PIPE, shell = True)
                    processOutput, processError = process.communicate()

                    if processOutput:

                        processId = processOutput.split('\n')[0].split('.')[0]
                        if processId not in processIdList.keys(): 
                            processIdList[processId] = { 'year' : yearJob, 'tag' : tagJob, 'samples' : [] }
                        if sample not in processIdList[processId]['samples']: processIdList[processId]['samples'].append(sample)    

    return processIdList 

def checkJobs(opt):

    checkCommand = 'condor_q' if 'cern' in os.uname()[1] else 'squeue'

    processIdList = getProcessIdList(opt) 

    if len(processIdList.keys())==0:
        print 'No job running for year='+opt.year+', tag='+opt.tag+', and sigset='+opt.sigset
        exit()

    process=subprocess.Popen(checkCommand, stderr = subprocess.PIPE,stdout = subprocess.PIPE, shell = True)
    processOutput, processError = process.communicate()

    if processError: print processError
    
    if processOutput:

        for processLine in processOutput.split('\n'):
            if 'JOB' in processLine: print processLine
            else:
                for processId in processIdList:
                    if processId in processLine:
                        jobInfo = processIdList[processId]
                        print processLine+' year='+jobInfo['year']+', tag='+jobInfo['tag']+', samples='+','.join(jobInfo['samples'])

def killJobs(opt):

    killCommand = 'condor_rm ' if 'cern' in os.uname()[1] else 'scancel '

    processIdList = getProcessIdList(opt)

    if len(processIdList.keys())==0:
        print 'No job running for year='+opt.year+', tag='+opt.tag+', and sigset='+opt.sigset
        
    else:
        for processId in processIdList:    
            os.system(killCommand+processId)

    cleanLogs(opt)

### Methods for analyzing shapes 

def getShapeFileName(shapeDir, year, tag, sigset, fileset, tagoption=''):

    return '/'.join([ shapeDir, year, tag, 'plots_'+tagoption+tag+setFileset(fileset, sigset)+'.root' ])

def openShapeFile(shapeDir, year, tag, sigset, fileset):

    return ROOT.TFile(getShapeFileName(shapeDir, year, tag, sigset, fileset), 'READ')

def mergeShapes(opt):

    print 'please, port me from https://github.com/scodella/PlotsConfigurations/blob/worker/Configurations/SUS-19-XXX/mergeShapes.py :('

def yieldsTables(opt):

    if 'fit' in opt.option.lower(): postfitYieldsTables(opt)
    else: 
        print 'please, complete me :('
        print 'using postfitYieldsTables for the time being'
        opt.option += 'prefit'
        postfitYieldsTables(opt)

def systematicsTables(opt):

    print 'please, port me from https://github.com/scodella/PlotsConfigurations/blob/worker/Configurations/SUS-19-XXX/mkSystematicsTables.py :('

### Modules for analyzing results from combine

def postfitShapes(opt):

    print 'please, port me from https://github.com/scodella/PlotsConfigurations/blob/worker/Configurations/SUS-19-XXX/mergeShapesPostFit.py :('

def massScanLimits(opt):

    print 'please, port me from https://github.com/scodella/PlotsConfigurations/blob/worker/Configurations/SUS-19-XXX/analyzeLimits.py :('

def fitMatrices(opt):

    print 'please, port me fromhttps://github.com/scodella/PlotsConfigurations/blob/worker/Configurations/SUS-19-XXX/mkMatrixPlots.py :('

def postfitYieldsTables(opt):

    print 'please, port me from https://github.com/scodella/PlotsConfigurations/blob/worker/Configurations/SUS-19-XXX/mkYieldsTables.py :('

### Methods for computing weights, efficiencies, scale factors, etc.

def triggerEfficiencies(opt):

    print 'please, port me from https://github.com/scodella/PlotsConfigurations/blob/worker/Configurations/SUS-19-XXX/mkTriggerEfficiencies.py :('

def theoryNormalizations(opt):

    print 'please, port me from https://github.com/scodella/PlotsConfigurations/blob/worker/Configurations/SUS-19-XXX/computeTheoryNormalizations.py :('

def backgroundScaleFactors(opt):

    print 'please, port me fromhttps://github.com/scodella/PlotsConfigurations/blob/worker/Configurations/SUS-19-XXX/mkBackgroundScaleFactors.py :('

