import os
import ROOT
import PlotsConfigurations.Tools.commonTools as commonTools
from array import array

### Analysis defaults

def setAnalysisDefaults(opt):

    if opt.year.lower()=='run2split': opt.year = '2016HIPM-2016noHIPM-2017-2018'
    elif opt.year.lower()=='run2': opt.year = '2016-2017-2018'

    taglower = opt.tag.lower()

    validationRegionMap = { 'vr1'    : 'HighPtMissValidationRegionVetoesUL',
                            'wzwwvr' : 'WZtoWWValidationRegionVetoesUL' } 

    opt.signalRegionMap = { }
    opt.signalRegionMap['stopSR'] = { 'tag' : 'StopSignalRegionsVetoesUL',     'signals' : [ 'T2tt_mS-150to800_dm-80to175', 'T2bW_mS-200to1000_mX-1to700' ] }
    opt.signalRegionMap['charSR'] = { 'tag' : 'CharginoSignalRegionsVetoesUL', 'signals' : [ 'TChipmSlepSnu_mC-100to1500_mX-1to750', 'TSlepSlep_mS-100to1000_mX-1to650' ] }
    opt.signalRegionMap['chwwSR'] = { 'tag' : 'TChipmWWSignalRegionsVetoesUL', 'signals' : [ 'TChipmWW_mC-100to700_mX-1to250' ] } 

    signalSubsets = { 'T2tt'          : [ ],
                      'T2bW'          : [ ],
                      'TChipmSlepSnu' : [ ],
                      'TChipmWW'      : [ ],
                      'TSlepSlep'     : [ ] }

    opt.backgroundsInFit = [ 'ttZ', 'ZZ', 'WZ' ]

    tagList = []

    for vr in validationRegionMap:
        if vr.lower() in taglower or 'allvr' in taglower: tagList.append(validationRegionMap[vr])

    for sr in opt.signalRegionMap:
        if sr.lower() in taglower or 'allsr' in taglower: tagList.append(opt.signalRegionMap[sr]['tag'])
     
    if 'fitcr' in taglower:
        fitcrtag = taglower.replace(taglower.split('fitcr')[0],'')
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
     
    if len(tagList)>0: opt.tag = '-'.join( tagList )

    if 'merge' in taglower: opt.tag = opt.tag.replace('SignalRegions','SignalRegionsMerge') 

    if 'signal' in opt.sigset:
        coreSigset = opt.sigset.replace(opt.sigset.split('-')[-1],'') if '-' in opt.sigset else ''
        for sr in opt.signalRegionMap:
            if opt.signalRegionMap[sr]['tag'] in opt.tag.replace('Merge',''):
                signalList = []
                if opt.sigset.split('signal')[-1]!='': signalList.append(opt.signalRegionMap[sr]['signals'][int(opt.sigset.split('signal')[-1])])
                else: signalList = opt.signalRegionMap[sr]['signals']
                opt.sigset = coreSigset+','.join(signalList)

    if opt.action=='shapes':
        for sr in opt.signalRegionMap:
            for signal in opt.signalRegionMap[sr]['signals']:
                if signal.split('_')[0] in opt.sigset:
                    opt.sigset = 'EOY' + opt.sigset
 
    if opt.verbose: print opt.year, opt.tag, opt.sigset

### Shapes

def mergeFitCR(opt):

    for year in opt.year.split('-'):
        for tag in opt.tag.split('-'):

            if year=='2016': 

                inputNuisances = commonTools.getCfgFileName(opt, 'nuisances')
                outputDir = '/'.join([ opt.shapedir, year, tag ])
               
                commonTools.mergeDataTakingPeriodShapes(opt, '2016HIPM-2016noHIPM', tag, 'SM'       , 'deep', outputDir, inputNuisances, 'None', opt.verbose)
                commonTools.mergeDataTakingPeriodShapes(opt, '2016HIPM-2016noHIPM', tag, opt.sigset , 'deep', outputDir, inputNuisances, 'None', opt.verbose)

                for backcr in opt.backgroundsInFit: 
                    fittag = tag.replace('VetoesUL', 'FitCR'+backcr+'VetoesUL')
                    commonTools.mergeDataTakingPeriodShapes(opt, '2016HIPM-2016noHIPM', fittag, 'SM', 'deep', outputDir, inputNuisances, 'None', opt.verbose)                      
            shapeDir = commonTools.getShapeDirName(opt.shapedir, year, tag)

            fitFileList = [ shapeDir+'/plots_'+tag.replace('VetoesUL', 'FitCRVetoesUL')+'_SM-'+opt.sigset+'.root' ]
            fitFileList.extend([ shapeDir+'/plots_'+tag+'_SM.root', shapeDir+'/plots_'+tag+'_'+opt.sigset+'.root' ])
            for backcr in opt.backgroundsInFit:
                fitFileList.append(shapeDir+'/plots_'+tag.replace('VetoesUL', 'FitCR'+backcr+'VetoesUL')+'_SM.root')

            os.system('haddfast --compress '+' '.join(fitFileList))

### Tools for handling signal mass points

def splitSignalMassPoints(opt, massPointForSubset=300):

    promptMassStep = 25
    signalSubsets = { }

    for sr in opt.signalRegionMap:
        for signal in opt.signalRegionMap[sr]['signals']:

            baseSignal = signal.split('_')[0]
            signalSubsets[baseSignal] = [ ]  

            if opt.verbose: print 'Splitting mass points for', baseSignal          

            samples = commonTools.getSamplesInLoop(opt.configuration, '2018', opt.signalRegionMap[sr]['tag'], signal)

            nMassPoints = len(samples.keys()) 
            minPromptMass = int(signal.split('_')[1].split('-')[1].split('to')[0])
            maxPromptMass = int(signal.split('_')[1].split('to')[1])

            nDivisions = int(round(float(nMassPoints)/massPointForSubset))
            signalMmassPointForSubset = nMassPoints/nDivisions

            promptMassRangeDraft = signal.split('_')[1].split('-')[0]+'-minPromptMasstomaxPromptMass'
            signalDraft = '_'.join([ baseSignal, promptMassRangeDraft, signal.split('_')[2] ])

            minSubsetPromptMass = minPromptMass

            for division in range(nDivisions):
                for promptMass in range(minSubsetPromptMass, maxPromptMass+1, promptMassStep):
                    
                    signalSubset = signalDraft.replace('minPromptMass', str(minSubsetPromptMass)).replace('maxPromptMass', str(promptMass))
                    subsamples = commonTools.getSamplesInLoop(opt.configuration, '2018', opt.signalRegionMap[sr]['tag'], signalSubset)

                    if len(subsamples.keys())>=signalMmassPointForSubset or promptMass==maxPromptMass:

                        signalSubsets[baseSignal].append(signalSubset)
                        minSubsetPromptMass = promptMass + promptMassStep
                        break

    for signal in signalSubsets:
        print 'signalSubsets[\''+signal+'\'] = '+repr(signalSubsets[signal])+'\n\n'               

### Analysis specific weights, efficiencies, scale factors, etc.


