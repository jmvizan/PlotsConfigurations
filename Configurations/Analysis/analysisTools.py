import os
import ROOT
import copy
import PlotsConfigurations.Tools.commonTools as commonTools
import PlotsConfigurations.Tools.latinoTools as latinoTools
import PlotsConfigurations.Tools.combineTools as combineTools
import PlotsConfigurations.Tools.signalMassPoints as signalMassPoints
from array import array

### Analysis defaults

def setAnalysisDefaults(opt):
    
    opt.combineLocation = '/afs/cern.ch/work/s/scodella/SUSY/CMSSW_10_2_14/src'
    opt.isExotics = True

    if opt.year.lower()=='run2split': opt.year = '2016HIPM-2016noHIPM-2017-2018'
    elif opt.year.lower()=='run2': opt.year = '2016-2017-2018'

    inputTag = opt.tag

    validationRegionMap = { 'vr1'    : 'HighPtMissValidationRegionVetoesUL',
                            'wzwwvr' : 'WZtoWWValidationRegionVetoesUL' } 

    opt.signalRegionMap, opt.signalSubsets, opt.tableSigset = { }, { }, { }

    opt.signalRegionMap['stopSR'] = { 'tag' : 'StopSignalRegionsVetoesUL',     'signals' : [ 'T2tt_mS-150to800_dm-80to175' ] } #, 'T2bW_mS-200to1000_mX-1to700' ] }
    opt.signalRegionMap['charSR'] = { 'tag' : 'CharginoSignalRegionsVetoesUL', 'signals' : [ 'TChipmSlepSnu_mC-100to1500_mX-1to750', 'TSlepSlep_mS-100to1000_mX-1to650' ] }
    opt.signalRegionMap['chwwSR'] = { 'tag' : 'TChipmWWSignalRegionsVetoesUL', 'signals' : [ 'TChipmWW_mC-100to700_mX-1to250' ] }

    #opt.tableSigset['TChipmSlepSnu'] = [ 'TChipmSlepSnu_mC-300_mX-1', 'TChipmSlepSnu_mC-400_mX-225', 'TChipmSlepSnu_mC-500_mX-50', 'TChipmSlepSnu_mC-300_mX-175', 'TChipmSlepSnu_mC-500_mX-300', 'TChipmSlepSnu_mC-650_mX-125', 'TChipmSlepSnu_mC-650_mX-350', 'TChipmSlepSnu_mC-800_mX-200', 'TChipmSlepSnu_mC-950_mX-200', 'TChipmSlepSnu_mC-200_mX-125', 'TChipmSlepSnu_mC-200_mX-150', 'TChipmSlepSnu_mC-250_mX-175', 'TChipmSlepSnu_mC-300_mX-200', 'TChipmSlepSnu_mC-300_mX-225', 'TChipmSlepSnu_mC-350_mX-250', 'TChipmSlepSnu_mC-400_mX-275', 'TChipmSlepSnu_mC-450_mX-325', 'TChipmSlepSnu_mC-500_mX-325', 'TChipmSlepSnu_mC-700_mX-425', 'TChipmSlepSnu_mC-800_mX-450', 'TChipmSlepSnu_mC-900_mX-425', 'TChipmSlepSnu_mC-1000_mX-375', 'TChipmSlepSnu_mC-1100_mX-300', 'TChipmSlepSnu_mC-1150_mX-1' ]
    opt.tableSigset['TChipmSlepSnu'] = [ 'TChipmSlepSnu_mC-300_mX-1', 'TChipmSlepSnu_mC-400_mX-225', 'TChipmSlepSnu_mC-500_mX-50', 'TChipmSlepSnu_mC-300_mX-175', 'TChipmSlepSnu_mC-500_mX-300', 'TChipmSlepSnu_mC-650_mX-125', 'TChipmSlepSnu_mC-650_mX-350', 'TChipmSlepSnu_mC-800_mX-200', 'TChipmSlepSnu_mC-950_mX-200', 'TChipmSlepSnu_mC-300_mX-200', 'TChipmSlepSnu_mC-300_mX-225', 'TChipmSlepSnu_mC-350_mX-250', 'TChipmSlepSnu_mC-400_mX-275', 'TChipmSlepSnu_mC-450_mX-325', 'TChipmSlepSnu_mC-500_mX-325', 'TChipmSlepSnu_mC-700_mX-425', 'TChipmSlepSnu_mC-800_mX-450', 'TChipmSlepSnu_mC-900_mX-425', 'TChipmSlepSnu_mC-1000_mX-375', 'TChipmSlepSnu_mC-1100_mX-300', 'TChipmSlepSnu_mC-1150_mX-1' ]
    opt.tableSigset['T2tt']          = [ 'T2tt_mS-300_mX-213', 'T2tt_mS-300_mX-175', 'T2tt_mS-350_mX-263', 'T2tt_mS-350_mX-225', 'T2tt_mS-400_mX-275', 'T2tt_mS-300_mX-125', 'T2tt_mS-350_mX-175', 'T2tt_mS-400_mX-225', 'T2tt_mS-400_mX-313', 'T2tt_mS-475_mX-350', 'T2tt_mS-450_mX-275', 'T2tt_mS-450_mX-325', 'T2tt_mS-475_mX-388', 'T2tt_mS-450_mX-363', 'T2tt_mS-475_mX-300', 'T2tt_mS-475_mX-325', 'T2tt_mS-475_mX-375', 'T2tt_mS-500_mX-325', 'T2tt_mS-500_mX-350', 'T2tt_mS-500_mX-375', 'T2tt_mS-500_mX-400', 'T2tt_mS-500_mX-413', 'T2tt_mS-525_mX-350', 'T2tt_mS-525_mX-375', 'T2tt_mS-525_mX-400', 'T2tt_mS-525_mX-425', 'T2tt_mS-525_mX-438', 'T2tt_mS-550_mX-375', 'T2tt_mS-550_mX-400', 'T2tt_mS-550_mX-425', 'T2tt_mS-550_mX-450', 'T2tt_mS-550_mX-463' ]
    opt.tableSigset['TChipmWW']      = [ 'TChipmWW_mC-100_mX-1', 'TChipmWW_mC-150_mX-1', 'TChipmWW_mC-200_mX-1', 'TChipmWW_mC-200_mX-25', 'TChipmWW_mC-200_mX-50', 'TChipmWW_mC-300_mX-75', 'TChipmWW_mC-400_mX-50' ]    
    opt.tableSigset['Studies']      = [ 'T2tt_mS-525_mX-350','T2tt_mS-525_mX-438','TChipmSlepSnu_mC-1150_mX-1','TChipmSlepSnu_mC-900_mX-475','EOYT2tt_mS-525_mX-350','EOYT2tt_mS-525_mX-438','EOYTChipmSlepSnu_mC-1150_mX-1','EOYTChipmSlepSnu_mC-900_mX-475' ]

    opt.signalSubsets['T2tt']          = [ 'T2tt_mS-150to800_dm-80to175' ]
    opt.signalSubsets['T2bW']          = [ 'T2bW_mS-200to1000_mX-1to700' ]

    if 'SigV6' in inputTag or 'sigv6' in inputTag:
        opt.tableSigset['TSlepSlep'] = [ 'TSlepSlep_mS-200_mX-120', 'TSlepSlep_mS-400_mX-250', 'TSlepSlep_mS-400_mX-300', 'TSlepSlep_mS-600_mX-300', 'TSlepSlep_mS-800_mX-1' ]
        opt.signalSubsets['TChipmSlepSnu'] = [ 'TChipmSlepSnu_mC-100to475_mX-1to750', 'TChipmSlepSnu_mC-500to650_mX-1to750', 'TChipmSlepSnu_mC-675to800_mX-1to750', 'TChipmSlepSnu_mC-825to925_mX-1to750', 'TChipmSlepSnu_mC-950to1050_mX-1to750', 'TChipmSlepSnu_mC-1075to1175_mX-1to750', 'TChipmSlepSnu_mC-1200to1300_mX-1to750', 'TChipmSlepSnu_mC-1325to1425_mX-1to750', 'TChipmSlepSnu_mC-1450to1500_mX-1to750' ]
        opt.signalSubsets['TChipmWW']      = [ 'TChipmWW_mC-100to375_mX-1to250', 'TChipmWW_mC-400to700_mX-1to250' ]
        opt.signalSubsets['TSlepSlep'] = [ 'TSlepSlep_mS-100to275_mX-1to650', 'TSlepSlep_mS-300to400_mX-1to650', 'TSlepSlep_mS-425to600_mX-1to650', 'TSlepSlep_mS-625to900_mX-1to650', 'TSlepSlep_mS-925to1000_mX-1to650' ]
    else:
        opt.tableSigset['TSlepSlep'] = [ 'TSlepSlep_mS-200_mX-125', 'TSlepSlep_mS-200_mX-150', 'TSlepSlep_mS-400_mX-250', 'TSlepSlep_mS-400_mX-275', 'TSlepSlep_mS-400_mX-300', 'TSlepSlep_mS-600_mX-300', 'TSlepSlep_mS-800_mX-1' ]
        opt.signalSubsets['TChipmSlepSnu'] = ['TChipmSlepSnu_mC-100to350_mX-1to750', 'TChipmSlepSnu_mC-375to500_mX-1to750', 'TChipmSlepSnu_mC-525to625_mX-1to750', 'TChipmSlepSnu_mC-650to725_mX-1to750', 'TChipmSlepSnu_mC-750to825_mX-1to750', 'TChipmSlepSnu_mC-850to925_mX-1to750', 'TChipmSlepSnu_mC-950to1025_mX-1to750', 'TChipmSlepSnu_mC-1050to1125_mX-1to750', 'TChipmSlepSnu_mC-1150to1225_mX-1to750', 'TChipmSlepSnu_mC-1250to1325_mX-1to750', 'TChipmSlepSnu_mC-1350to1425_mX-1to750', 'TChipmSlepSnu_mC-1450to1500_mX-1to750']
        opt.signalSubsets['TChipmWW'] = ['TChipmWW_mC-100to275_mX-1to250', 'TChipmWW_mC-300to500_mX-1to250', 'TChipmWW_mC-525to700_mX-1to250']
        opt.signalSubsets['TSlepSlep'] = ['TSlepSlep_mS-100to325_mX-1to650', 'TSlepSlep_mS-350to475_mX-1to650', 'TSlepSlep_mS-500to600_mX-1to650', 'TSlepSlep_mS-625to700_mX-1to650', 'TSlepSlep_mS-725to800_mX-1to650', 'TSlepSlep_mS-825to900_mX-1to650', 'TSlepSlep_mS-925to1000_mX-1to650']

    opt.backgroundsInFit = [ 'ttZ', 'ZZ', 'WZ' ]

    tagList = []

    for vr in validationRegionMap:
        if vr.lower() in inputTag or 'allvr' in inputTag: tagList.append(validationRegionMap[vr])

    for sr in opt.signalRegionMap:
        if sr.lower() in inputTag or 'allsr' in inputTag: tagList.append(opt.signalRegionMap[sr]['tag'])
     
    if 'fitcr' in inputTag:
        fitcrtag = inputTag.replace(inputTag.split('fitcr')[0],'')
        allSR, allFitCR = True, True
        for sr in opt.signalRegionMap:
            if sr.replace('SR','') in fitcrtag: allSR = False
        for backcr in opt.backgroundsInFit:
            if backcr.lower() in fitcrtag: allFitCR = False
        for sr in opt.signalRegionMap:
            if allSR or sr.replace('SR','') in fitcrtag:
                for backcr in opt.backgroundsInFit:
                    if allFitCR or backcr.lower() in fitcrtag:
                        tagList.append(opt.signalRegionMap[sr]['tag'].replace('VetoesUL','FitCR'+backcr+'VetoesUL'))

    elif 'fit' in inputTag:
        for sr in opt.signalRegionMap:
            if 'fit'+sr.replace('SR','') in inputTag:
                tagList.append(opt.signalRegionMap[sr]['tag'].replace('VetoesUL','FitCRVetoesUL'))
     
    if len(tagList)>0: opt.tag = '-'.join( tagList )

    if 'group' in inputTag: opt.tag = opt.tag.replace('SignalRegions','SignalRegionsGroup')
    if 'merge' in inputTag: opt.tag = opt.tag.replace('SignalRegions','SignalRegionsMerge') 
    opt.tag = opt.tag.replace('StopSignalRegionsMerge','StopSignalRegions')
    if 'fast' in inputTag: opt.tag = opt.tag.replace('VetoesUL','VetoesULFast')
    if 'reco' in inputTag: opt.tag = opt.tag.replace('VetoesUL','VetoesULFastReco')
    if 'systwz' in inputTag: opt.tag = opt.tag.replace('VetoesUL','VetoesUL_WZbin')
    if 'systww' in inputTag: opt.tag = opt.tag.replace('VetoesUL','VetoesUL_WWshape')
    if 'sysbww' in inputTag: opt.tag = opt.tag.replace('VetoesUL','VetoesUL_WWShape')
    if 'sysbwz' in inputTag: opt.tag = opt.tag.replace('VetoesUL','VetoesUL_WZBin')

    if opt.action=='shapes':
        for sr in opt.signalRegionMap:
            for signal in opt.signalRegionMap[sr]['signals']:
                if signal.split('_')[0] in opt.sigset:
                    opt.sigset = opt.sigset
 
    if opt.verbose: print opt.year, opt.tag, opt.sigset

### Shapes

# signal

def signalShapes(opt, action='shapes'):

    mergeJobs = { }

    for year in opt.year.split('-'):
        for tag in opt.tag.split('-'):
            for signal in getSignalList(opt, opt.sigset, tag):

                opt2 = copy.deepcopy(opt)
                opt2.year, opt2.tag, opt2.action = year, tag, action

                if action=='shapes':

                    if 'split' in opt.option:
                        for massPoint in getMassPointList(signal):
                            opt2.sigset = massPoint
                            latinoTools.shapes(opt2)
                         
                    else:
                        opt2.sigset = signal
                        latinoTools.shapes(opt2)

                elif action=='checkJobs' or action=='killJobs':
                    opt2.sigset = signal if 'mergesig' in opt.logprocess else signal
                    if action=='checkJobs':  commonTools.checkJobs(opt2)
                    elif action=='killJobs': commonTools.killJobs(opt2)

                elif action=='mergeall':
               
                    if opt.recover:
                        if commonTools.isGoodFile(commonTools.getShapeFileName(opt.shapedir, year, tag, signal, '')): continue

                    if opt.interactive:
                        opt2.sigset = signal
                        latinoTools.mergeall(opt2)
                  
                    else:
                        if year not in mergeJobs: mergeJobs[year] = {}
                        if tag not in mergeJobs[year]: mergeJobs[year][tag] = {}
                        mergeCommandList = [ 'cd '+os.getenv('PWD'), 'eval `scramv1 runtime -sh`' ]
                        mergeCommandList.append('./runAnalysis.py --action=mergeall --year='+year+' --tag='+tag+' --sigset='+signal)
                        mergeJobs[year][tag][signal] = '\n'.join(mergeCommandList) 

    if len(mergeJobs.keys())>0:
        opt.batchQueue = commonTools.batchQueue(opt.batchQueue)
        for year in mergeJobs:
            for tag in mergeJobs[year]:
                if len(mergeJobs[year][tag].keys())>0:
                    latinoTools.submitJobs(opt, 'mergesig', year+tag, mergeJobs[year][tag], 'Targets', True, 1)

def checkSignalJobs(opt):

    signalShapes(opt, action='checkJobs')

def killSignalJobs(opt):

    signalShapes(opt, action='killJobs')

def mergeSignal(opt):

    signalShapes(opt, action='mergeall')

# stuff for 2016  

def merge2016(opt):

    inputNuisances = commonTools.getCfgFileName(opt, 'nuisances') 

    for tag in opt.tag.split('-'):

        outputDir = '/'.join([ opt.shapedir, '2016', tag ])
        outputFile = outputDir+'/plots_'+tag+'_'+opt.sigset+'.root'
        if opt.recover and commonTools.isGoodFile(outputFile): continue
        os.system('rm -r -f '+outputFile)
        commonTools.mergeDataTakingPeriodShapes(opt, '2016HIPM-2016noHIPM', tag, opt.sigset, 'deep', outputDir, inputNuisances, 'None', opt.verbose)

def merge2016SR(opt):

    opt2 = copy.deepcopy(opt)

    for tag in opt.tag.split('-'):
  
        opt2.tag = tag

        for sigset in getSignalList(opt, opt.sigset, tag):
            opt2.sigset = sigset
            merge2016(opt2)

        if 'SM' in opt.sigset:
 
            opt2.sigset = 'SM'
            merge2016(opt2)

            for backcr in opt.backgroundsInFit:
                opt2.tag = tag.replace('VetoesUL', 'FitCR'+backcr+'VetoesUL')
                merge2016(opt2)

def merge2016CR(opt):

    opt2 = copy.deepcopy(opt)

    for tag in opt.tag.split('-'):

        opt2.tag = tag

        opt2.sigset = 'SM'
        merge2016(opt2)

        for sigset in getSignalList(opt, opt.sigset, tag):
            opt2.sigset = sigset
            merge2016(opt2)

# To study signal in CRs

def mergeCRToSignal(opt):

    for year in opt.year.split('-'):
        for tag in opt.tag.split('-'):

            for sigset in getSignalList(opt, opt.sigset, tag):

                outputDir = commonTools.getShapeDirName(opt.shapedir, year, tag)
                outputFile = outputDir + '/plots_' + tag + '_SM-' + sigset + '.root'
                smFile     = outputDir + '/plots_' + tag + '_SM.root' 
                signalFile = outputDir.replace('Group','') + '/plots_' + tag.replace('Group','') + '_' + sigset + '.root'

                os.system('haddfast --compress '+outputFile+' '+smFile+' '+signalFile) 

# groups

def mergeGroupsForDatacards(opt):

    inputnuisances = commonTools.getCfgFileName(opt, 'nuisances')

    groups = { 'ttbar' : [ 'ttbar', 'ttSemilep' ],
               'minor' : [ 'Higgs', 'VVV', 'ttW', 'VZ' ] }

    groupList = []
    for group in groups:
        groupList.append(group+':'+','.join(groups[group]))

    mergeCommandList = [ '--inputDir='+opt.shapedir, '--sigset='+opt.sigset, '--nuisancesFile='+inputnuisances ]
    mergeCommandList.append('--groups='+'-'.join(groupList))
    if opt.verbose: mergeCommandList.append('--verbose')

    for year in opt.year.split('-'):
        for tag in opt.tag.split('-'):

            loopMergeCommandList = mergeCommandList
            loopMergeCommandList.extend([ '--year='+year, '--tag='+tag ])
            outputtag = tag.replace('FitCR', 'GroupFitCR') if 'FitCR' in tag else tag.replace('VetoesUL', 'GroupVetoesUL')
            loopMergeCommandList.append('--outputtag='+outputtag)

            os.system('mergeSamplesForDatacards.py '+' '.join( loopMergeCommandList))

# merging CRs in the fit

def mergeFitCR(opt):

    if 'merge2016' in opt.option: merge2016SR(opt)

    for year in opt.year.split('-'):
        for tag in opt.tag.split('-'):

            outputTag = tag.replace('VetoesUL', 'FitCRVetoesUL')
            outputDir = commonTools.getShapeDirName(opt.shapedir, year, outputTag)
            os.system('mkdir -p '+outputDir)

            for signal in getSignalList(opt, opt.sigset, tag):

                outputFile = outputDir + '/plots_' + outputTag + '_SM-' + signal + '.root'
                if opt.recover and commonTools.isGoodFile(outputFile): continue
                os.system('rm -r -f '+outputFile)

                filesToMerge = [ outputFile.replace('FitCR','').replace('-'+signal,'').replace('FastReco','').replace('Fast','').replace('SigV6','') ]
                filesToMerge.append(outputFile.replace('FitCR','').replace('SM-','').replace('Group','').replace('WWTails','').replace('WWHighs','').replace('WWPol1a','').replace('SmtEU',''))
                for backcr in opt.backgroundsInFit:
                    filesToMerge.append(outputFile.replace('FitCR','FitCR'+backcr).replace('-'+signal,'').replace('FastReco','').replace('Fast','').replace('SigV6','').replace('WWTails','').replace('WWHighs','').replace('WWPol1a','').replace('SmtEU',''))

                foundFilesToMerge = True
                for fileToMerge in filesToMerge:
                    if not commonTools.isGoodFile(fileToMerge):
                        print 'mergeFitCR error: input file', fileToMerge, 'not found or corrupted' 
                        foundFilesToMerge = False

                if foundFilesToMerge:
                    os.system('haddfast --compress '+outputFile+' '+' '.join(filesToMerge))

### Combine with mass points

def signalCombine(opt, action):

    if opt.sigset=='SM': opt.sigset = 'signal'

    smset = opt.sigset.split('_')[0]
    smset = smset.replace(smset.split('-')[-1],'')
    if smset=='': smset = 'SM-'

    for tag in opt.tag.split('-'):

        opt2 = copy.deepcopy(opt)
        opt2.year, opt2.tag = opt.year, tag

        filesetMap = {}
        signalList = getSignalList(opt, opt.sigset, tag)      

        if 'signal' in opt.sigset and 'tabsignal' not in opt.sigset:
            for fileset in signalList:
                filesetMap[smset+fileset] = [ fileset ]

        else:
            for signal in signalList:
                massPoints = getMassPointList(signal)
                for massPoint in massPoints:
                    if opt.fileset!='': signalFileset = opt.fileset
                    else: signalFileset = smset+getMassPointSubset(opt, massPoint)
                    if signalFileset!=None:
                        if signalFileset not in filesetMap: filesetMap[signalFileset] = []
                        filesetMap[signalFileset].append(massPoint)

        for fileset in filesetMap:

            opt2.fileset = fileset
            opt2.sigset = smset+','.join(filesetMap[fileset])

            if action=='limits': combineTools.limits(opt2)
            if action=='mlfits': combineTools.mlfits(opt2)
            if action=='impactsPlots': combineTools.impactsPlots(opt2)

def signalLimits(opt):

    signalCombine(opt, 'limits')

def signalMLFits(opt):

    signalCombine(opt, 'mlfits')

def signalImpactsPlots(opt):

    signalCombine(opt, 'impactsPlots')

### Post fit analysis

# Yields

def yieldsSR(opt):

    yearInDatacard = '-' in opt.year and 'split' not in opt.option

    for tag in opt.tag.split('-'):
        opt2 = copy.deepcopy(opt)
        opt2.tag = tag
        cardNameStructure = latinoTools.getDatacardNameStructure(yearInDatacard, True, 'Merge' in tag)
        commonTools.postFitYieldsTables(opt2, cardNameStructure, ','.join(getSignalList(opt, 'tabsignal', tag)))

def preFitYieldsSR(opt):
    
    opt.option += 'prefit'
    yieldsSR(opt)

# Limits 

def printLimits(opt):

    signalList = getSignalList(opt, opt.sigset, opt.tag)
    if 'tab' not in opt.sigset: 
        massPointList = []
        for signal in sorted(signalList):
            massPointList.extend(getMassPointList(signal))
        signalList = massPointList

    for signal in sorted(signalList):

        limitResult = {}

        for tags in [ '', '_WWSimm' ]:
            for tagm in [ '', 'WWTails', 'WWHighs', 'WWPol1a' ]:
                if (tags=='' and tagm=='') or (tags!='' and tagm!=''): continue
                #if 'Stop' in opt.tag and 'Merge' in tagm: continue
                #if 'Stop' not in opt.tag and 'Merge' not in tagm: continue
                tagopt = (tagm+tags).replace('_WWSimm','')
                tag = opt.tag.replace('Group', tagm+'Group')
                tag += tags
                outputDir = '/'.join([ opt.limitdir, opt.year, tag, signal ])
                if not commonTools.isGoodFile(outputDir+'/higgsCombine_Blind.AsymptoticLimits.mH120.root', 6000.):
                    if opt.debug: print outputDir+'/higgsCombine_Blind.AsymptoticLimits.mH120.root'
                    continue
                inputFile =  commonTools.openRootFile(outputDir+'/higgsCombine_Blind.AsymptoticLimits.mH120.root')

                if tagopt=='': limitResult['central'] = []
                else: limitResult[tagopt] = []

                for event in inputFile.limit:
                    if opt.debug: print tagopt, event.limit
                    if tagopt=='': limitResult['central'].append(event.limit)
                    else: limitResult[tagopt].append(event.limit)

        printSignal = True
        signalResult = []
        if 'central' not in limitResult: continue
        availableResultList = [ 'central' ]
        if len(limitResult.keys())==1: printSignal = True
        for evt in range(len(limitResult['central'])):
            resultList = [ str(limitResult['central'][evt]) ]
            for tags in [ '', 'WWTails', 'WWHighs', 'WWPol1a' ]:
                for tagm in [ '' ]:
                    tagopt = tagm+tags
                    if tagopt!='' and tagopt in limitResult:
                        diff = abs(1. - limitResult[tagopt][evt]/limitResult['central'][evt])
                        if diff>0.0: printSignal = True
                        if tagopt not in availableResultList: availableResultList.append(tagopt)
                        #resultList.append(str(limitResult[tagopt][evt]/limitResult['central'][evt]))
                        resultList.append(str(limitResult[tagopt][evt]))
                        
            signalResult.append(' '.join(resultList)) 
        availableResult = ' '.join(availableResultList)

        if printSignal:
            print '####', signal
            print '    ', availableResult
            for evt in range(len(signalResult)):
                print signalResult[evt]
            if len(signalResult)==6:
                ccc = []
                obs = signalResult[5].split(' ')
                cen = signalResult[2].split(' ')
                pus = signalResult[3].split(' ')
                pds = signalResult[4].split(' ')
                mus = signalResult[1].split(' ')
                mds = signalResult[0].split(' ')
                for rr in range(len(obs)):
                    if float(obs[rr])<float(cen[rr]) and float(obs[rr])>float(mus[rr]):
                        ccc.append((float(obs[rr])-float(cen[rr]))/(float(cen[rr])-float(mus[rr])))
                    elif float(obs[rr])<float(mus[rr]) and float(obs[rr])>float(mds[rr]):
                        ccc.append(-1.+(float(obs[rr])-float(mus[rr]))/(float(mus[rr])-float(mds[rr])))
                    elif float(obs[rr])<float(mds[rr]):
                        ccc.append(-2.5)
                    elif float(obs[rr])>float(cen[rr]) and float(obs[rr])<float(pus[rr]):
                        ccc.append((float(obs[rr])-float(cen[rr]))/(float(pus[rr])-float(cen[rr])))
                    elif float(obs[rr])>float(pus[rr]) and float(obs[rr])<float(pds[rr]):
                        ccc.append(1.+(float(obs[rr])-float(pus[rr]))/(float(pds[rr])-float(pus[rr])))
                    elif float(obs[rr])>float(pds[rr]):
                        ccc.append(+2.5)
                print ccc
            print '\n\n'

def makePseudoDataShapes(opt):

    for year in opt.year.split('-'):
        
        signalList = getSignalList(opt, opt.sigset, opt.tag)
        for signal in signalList:
            for pseudodata in [ '', 'WWHighs' ]:

                opt2 = copy.deepcopy(opt)
                opt2.year = year
                
                if pseudodata=='' or pseudodata not in opt.tag:
                    opt2.sigset = 'SM-PseudoDATA'+pseudodata+'-'+signal
                    reftag = opt.tag.replace('Group', pseudodata+'Group')

                else:
                    opt2.sigset = 'SM-PseudoDATANo'+pseudodata+'-'+signal
                    reftag = opt.tag.replace(pseudodata, '')
              
                commonTools.mkPseudoData(opt2, reftag)

def makeContours(opt, plotoption='2', fitOption='Blind'):

    sigset = ','.join(getSignalList(opt, opt.sigset, opt.tag))

    histogramDir = '/'.join([ opt.limitdir, opt.year, opt.tag, 'Histograms' ])
    contourDir   = '/'.join([ opt.limitdir, opt.year, opt.tag, 'Contours' ])

    histogramFileNoFillEmptyBins = histogramDir + '_'.join([ '/massScan', opt.tag, sigset, fitOption, 'noFillEmptyBins' ]) + '.root'
    histogramFile                = histogramDir + '_'.join([ '/massScan', opt.tag, sigset, fitOption ]) + '.root'
    contourFile                  = contourDir   + '_'.join([ '/massScan', opt.tag, sigset, fitOption ]) + '.root' 

    if opt.reset: 
        os.system('rm -f '+' '.join([ histogramFileNoFillEmptyBins, histogramFile, contourFile ]))
 
    commandList = [ '--years='+opt.year, '--tag='+opt.tag, '--sigset='+sigset, '--limitoption='+fitOption ]

    if not os.path.isfile(histogramFileNoFillEmptyBins):
        os.system('analyzeLimits.py '+' '.join(commandList + [ '--nofillempties' ]))

    if plotoption!='0':
        if not os.path.isfile(contourFile):
            os.system('analyzeLimits.py '+' '.join(commandList + [ '--makecontours' ])) 

def exclusionPlot(opt, plotoption='2'):

    tagList = opt.tag.split('-')

    if len(tagList)>2: 
        print 'Comparison of more than two tags not supported'  
        exit()

    fitOption = 'Both' if opt.unblind else 'Blind'

    sigset = ','.join(getSignalList(opt, opt.sigset, tagList[0]))
 
    opt2 = copy.deepcopy(opt)
    for tag in tagList:
        opt2.tag = tag
        makeContours(opt2, plotoption, fitOption)

    plotCommandList = [ '--years='+opt.year, '--tag='+tagList[0], '--sigset='+sigset, '--limitoption='+fitOption, '--plotoption='+plotoption ]
    if len(tagList)>1: plotCommandList.append('--compareto='+tagList[1])
    if plotoption=='0': plotCommandList.append('--nofillempties')

    os.system('analyzeLimits.py '+' '.join(plotCommandList))

def plotLimits(opt):

    exclusionPlot(opt, '0')

def plotContours(opt):

    exclusionPlot(opt, '1')
    
### Tools for handling signal mass points

def getMassPointSubset(opt, massPoint):

    for subset in opt.signalSubsets[massPoint.split('_')[0]]:
        if signalMassPoints.massPointInSignalSet(massPoint, subset):
            return subset

    return None
          
def getSignalList(opt, sigset, tag):

    if sigset=='SM': return []

    for sr in opt.signalRegionMap:
        #if tag.split('_')[0].replace('Merge','').replace('FitCR','').replace('Group','').replace('FastReco','').replace('Fast','').replace('SigV6','').replace('WWTails','').replace('SmtEU','')==opt.signalRegionMap[sr]['tag']:
       if opt.signalRegionMap[sr]['tag'].replace('VetoesUL','') in tag:
            if 'all' in sigset:
                signalList = []
                for signal in opt.signalRegionMap[sr]['signals']:
                    if signal.split('_')[0] in sigset:
                        signalList.append(signal)
                if len(signalList)==0: return opt.signalRegionMap[sr]['signals']
                else: return signalList
            elif 'tabsignal' in sigset:
                signalList = []
                for signal in opt.signalRegionMap[sr]['signals']:
                    if sigset.split('-')[-1]=='tabsignal' or sigset.split('-')[-1]=='tabsignalset' or signal.split('_')[0] in sigset:
                        if signal.split('_')[0] in opt.tableSigset:
                            signalList.extend(opt.tableSigset[signal.split('_')[0]])
                if 'tabsignalset' in sigset: return [ ','.join(signalList) ]
                else: return signalList

            elif 'signal' in sigset:
                signalList = []
                for signal in opt.signalRegionMap[sr]['signals']:
                    if sigset.split('-')[-1]=='signal' or signal.split('_')[0] in sigset:
                        signalList.extend(opt.signalSubsets[signal.split('_')[0]])
                return signalList

            else:
                setToRemove = sigset.split('_')[0].split('-')
                for st in range(len(setToRemove)-1): sigset = sigset.replace(setToRemove[st]+'-', '')
                return sigset.split(',')

    if 'SignalRegion' not in tag:
        if 'tabsignal' in sigset:
            for signal in opt.tableSigset:
                if signal in sigset:
                   if 'tabsignalset' in sigset: return [ ','.join(opt.tableSigset[signal]) ]
                   else: return opt.tableSigset[signal]
        else:
            setToRemove = sigset.split('_')[0].split('-')
            for st in range(len(setToRemove)-1): sigset = sigset.replace(setToRemove[st]+'-', '')
            return sigset.split(',')

def splitSignalMassPoints(opt, massPointForSubset=100):

    promptMassStep = 25
    signalSubsets = { }

    for sr in opt.signalRegionMap:
        for signal in opt.signalRegionMap[sr]['signals']:

            baseSignal = signal.split('_')[0]
            signalSubsets[baseSignal] = [ ]  

            if opt.verbose: print 'Splitting mass points for', baseSignal          

            massPoints = getMassPointList(signal)

            nMassPoints = len(massPoints) 
            minPromptMass = int(signal.split('_')[1].split('-')[1].split('to')[0])
            maxPromptMass = int(signal.split('_')[1].split('to')[1])
            
            nDivisions = max(1, int(round(float(nMassPoints)/massPointForSubset)))

            if nDivisions==1:
                signalSubsets[baseSignal].append(signal)
                continue

            signalMmassPointForSubset = nMassPoints/nDivisions

            promptMassRangeDraft = signal.split('_')[1].split('-')[0]+'-minPromptMasstomaxPromptMass'
            signalDraft = '_'.join([ baseSignal, promptMassRangeDraft, signal.split('_')[2] ])

            minSubsetPromptMass = minPromptMass

            for division in range(nDivisions):
                for promptMass in range(minSubsetPromptMass, maxPromptMass+1, promptMassStep):
                    
                    signalSubset = signalDraft.replace('minPromptMass', str(minSubsetPromptMass)).replace('maxPromptMass', str(promptMass))
                    massPointSubsets = getMassPointList(signalSubset)

                    if len(massPointSubsets)>=signalMmassPointForSubset or promptMass==maxPromptMass:

                        signalSubsets[baseSignal].append(signalSubset)
                        minSubsetPromptMass = promptMass + promptMassStep
                        break

    for signal in signalSubsets:
        print 'signalSubsets[\''+signal+'\'] = '+repr(signalSubsets[signal])+'\n'               

def getMassPointList(signal):

    massPointList = []
    for massPoint in signalMassPoints.signalMassPoints[signal.split('_')[0]]:
        if signalMassPoints.massPointInSignalSet(massPoint, signal):
            massPointList.append(massPoint)

    return massPointList

### Analysis specific weights, efficiencies, scale factors, etc.


