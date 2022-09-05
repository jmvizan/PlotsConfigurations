import os
import ROOT
import PlotsConfigurations.Tools.commonTools as commonTools
from array import array

### Analysis defaults

def setAnalysisDefaults(opt):

    if opt.year.lower()=='run2split': opt.year = '2016HIPM-2016noHIPM-2017-2018'
    elif opt.year.lower()=='run2': opt.year = '2016-2017-2018'

    taglower = opt.tag.lower()

    validationRegionMap = { 'vr1' : 'HighPtMissValidationRegionVetoesUL' } 

    signalRegionMap = { 'stopSR' : { 'tag' : 'StopSignalRegionsVetoesUL',     'signals' : [ 'T2tt', 'T2bW' ] },
                        'charSR' : { 'tag' : 'CharginoSignalRegionsVetoesUL', 'signals' : [ 'TChipmSlepSnu', 'TSlepSlep' ] },
                        'chwwSR' : { 'tag' : 'TChipmWWSignalRegionsVetoesUL', 'signals' : [ 'TChipmWW' ] } }

    backgroundsInFit = [ 'ttZ', 'ZZ', 'WZ' ]

    tagList = []

    for vr in validationRegionMap:
        if vr.lower() in taglower or 'allvr' in taglower: tagList.append(validationRegionMap[vr])

    for sr in signalRegionMap:
        if sr.lower() in taglower or 'allsr' in taglower: tagList.append(signalRegionMap[sr]['tag'])
     
    if 'fitcr' in taglower:
        fitcrtag = taglower.replace(taglower.split('fitcr')[0],'')
        allSR, allFitCR = True, True
        for sr in signalRegionMap:
            if sr.replace('SR','') in fitcrtag: allSR = False
        for backcr in backgroundsInFit:
            if backcr.lower() in fitcrtag: allFitCR = False
        for sr in signalRegionMap:
            if allSR or sr.replace('SR','') in fitcrtag:
                for backcr in backgroundsInFit:
                    if allFitCR or backcr.lower() in fitcrtag:
                        tagList.append(signalRegionMap[sr]['tag'].replace('Regions','RegionsFitCR'+backcr))
     
    if len(tagList)>0: opt.tag = '-'.join( tagList )

    if 'merge' in taglower: opt.tag = opt.tag.replace('SignalRegions','SignalRegionsMerge') 

    if 'signal' in opt.sigset:
        coreSigset = opt.sigset.replace(opt.sigset.split('-')[-1],'') if '-' in opt.sigset else ''
        for sr in signalRegionMap:
            if signalRegionMap[sr]['tag'] in opt.tag.replace('Merge',''):
                signalList = []
                if opt.sigset.split('signal')[-1]!='': signalList.append(signalRegionMap[sr]['signals'][int(opt.sigset.split('signal')[-1])])
                else: signalList = signalRegionMap[sr]['signals']
                opt.sigset = coreSigset+','.join(signalList)

    if opt.action=='shapes':
        for sr in signalRegionMap:
            for signal in signalRegionMap[sr]['signals']:
                if signal in opt.sigset: 
                    opt.sigset = 'EOY' + opt.sigset 
 
    print opt.year, opt.tag, opt.sigset

### Loops on analysis years and tags

### Analysis specific weights, efficiencies, scale factors, etc.


