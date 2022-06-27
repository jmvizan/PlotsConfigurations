#!/usr/bin/env python
import os
import sys
import ROOT
import math
import copy
import optparse
import json
from array import *

backgroundProcess = sys.argv[1] if (len(sys.argv)>=2 and sys.argv[1]!='All') else 'ZZ-ttZ-WW-WZZ-WZ'
years = sys.argv[2] if len(sys.argv)>=3 else '2016HIPM-2016noHIPM-2017-2018'

commonFlag = 'VetoesUL'
plotArea = './Plots/'

backgroundInfo = { 'ZZ' : { 'validationRegion'   : 'ZZValidationRegion',
                            'signal'             : 'ZZTo4L',
                            'exclusiveSelection' : 1,
                            'measurementRegions' : { 'zz1' : { 'plot'      : 'ZZ_ptmissSR', 
                                                               'bin'       : 8,
                                                               'cuts'      : [ '_NoJet', '_Veto', '_NoTag', '_Tag', 'ZZ' ], 
                                                               'selection' : '(ptmiss"+ctrltag+">=160 && ptmiss"+ctrltag+"<220)' } ,
                                                     'zz2' : { 'plot'      : 'ZZ_ptmissSR',
                                                               'bin'       : 9,
                                                               'cuts'      : [ '_NoJet', '_Veto', '_NoTag', '_Tag', 'ZZ' ],
                                                               'selection' : '(ptmiss"+ctrltag+">=220 && ptmiss"+ctrltag+"<280)' } ,
                                                     'zz3' : { 'plot'      : 'ZZ_ptmissSR',
                                                               'bin'       : 10,
                                                               'cuts'      : [ '_NoJet', '_Veto', '_NoTag', '_Tag', 'ZZ' ],
                                                               'selection' : '(ptmiss"+ctrltag+">=280 && ptmiss"+ctrltag+"<380)' } ,
                                                     'zz4' : { 'plot'      : 'ZZ_ptmissSR',
                                                               'bin'       : 11,
                                                               'cuts'      : [ '_NoJet', '_Veto', '_NoTag', '_Tag', 'ZZ' ],
                                                               'selection' : '(ptmiss"+ctrltag+">=380)' }
                                                    },
                            'samples'            : [ 'ZZTo2L2Nu', 'ZZTo4L' ],
                           },
                   'WZ' : { 'validationRegion'   : 'WZValidationRegion',
                            'signal'             : 'WZ',
                            'exclusiveSelection' : 0,
                            'measurementRegions' : { 'wz1' : { 'plot'      : 'WZ_3Lep_ptmissSR',
                                                               'bin'       : 8,
                                                               'cuts'      : [ '_NoJet', '_Veto', '_NoTag', '_Tag', 'WZ_3Lep_' ],
                                                               'selection' : '(ptmiss"+ctrltag+">=160 && ptmiss"+ctrltag+"<220)' } ,
                                                     'wz2' : { 'plot'      : 'WZ_3Lep_ptmissSR',
                                                               'bin'       : 9,
                                                               'cuts'      : [ '_NoJet', '_Veto', '_NoTag', '_Tag', 'WZ_3Lep_' ],
                                                               'selection' : '(ptmiss"+ctrltag+">=220 && ptmiss"+ctrltag+"<280)' } ,
                                                     'wz3' : { 'plot'      : 'WZ_3Lep_ptmissSR',
                                                               'bin'       : 10,
                                                               'cuts'      : [ '_NoJet', '_Veto', '_NoTag', '_Tag', 'WZ_3Lep_' ],
                                                               'selection' : '(ptmiss"+ctrltag+">=280 && ptmiss"+ctrltag+"<380)' } ,
                                                     'wz4' : { 'plot'      : 'WZ_3Lep_ptmissSR',
                                                               'bin'       : 11,
                                                               'cuts'      : [ '_NoJet', '_Veto', '_NoTag', '_Tag', 'WZ_3Lep_' ],
                                                               'selection' : '(ptmiss"+ctrltag+">=380)' },
                                                     'wz1p': { 'plot'      : 'WZ_3LepZ_ptmissSR',
                                                               'bin'       : 8,
                                                               'cuts'      : [ 'WZ_3LepZ' ],
                                                               'selection' : '(ptmiss"+ctrltag+">=160 && ptmiss"+ctrltag+"<220)' } ,
                                                     'wz2p': { 'plot'      : 'WZ_3LepZ_ptmissSR',
                                                               'bin'       : 9,
                                                               'cuts'      : [ 'WZ_3LepZ' ],
                                                               'selection' : '(ptmiss"+ctrltag+">=220 && ptmiss"+ctrltag+"<280)' } ,
                                                     'wz3p': { 'plot'      : 'WZ_3LepZ_ptmissSR',
                                                               'bin'       : 10,
                                                               'cuts'      : [ 'WZ_3LepZ' ],
                                                               'selection' : '(ptmiss"+ctrltag+">=280 && ptmiss"+ctrltag+"<380)' } ,
                                                     'wz4p': { 'plot'      : 'WZ_3LepZ_ptmissSR',
                                                               'bin'       : 11,
                                                               'cuts'      : [ 'WZ_3LepZ' ],
                                                               'selection' : '(ptmiss"+ctrltag+">=380)' },
                                                    },
                   
                            'samples'            : [ 'WZ' ],
                           },
                   'WZZ': { 'validationRegion'   : 'WZValidationRegionZLeps',
                            'signal'             : 'WZ',
                            'exclusiveSelection' : 0,
                            'measurementRegions' : { 'wz1z': { 'plot'      : 'WZ_3Lep_ptmissSR',
                                                               'bin'       : 8,
                                                               'cuts'      : [ 'WZ_3Lep_' ],
                                                               'selection' : '(ptmiss"+ctrltag+">=160 && ptmiss"+ctrltag+"<220)' } ,
                                                     'wz2z': { 'plot'      : 'WZ_3Lep_ptmissSR',
                                                               'bin'       : 9,
                                                               'cuts'      : [ 'WZ_3Lep_' ],
                                                               'selection' : '(ptmiss"+ctrltag+">=220 && ptmiss"+ctrltag+"<280)' } ,
                                                     'wz3z': { 'plot'      : 'WZ_3Lep_ptmissSR',
                                                               'bin'       : 10,
                                                               'cuts'      : [ 'WZ_3Lep_' ],
                                                               'selection' : '(ptmiss"+ctrltag+">=280 && ptmiss"+ctrltag+"<380)' } ,
                                                     'wz4z': { 'plot'      : 'WZ_3Lep_ptmissSR',
                                                               'bin'       : 11,
                                                               'cuts'      : [ 'WZ_3Lep_' ],
                                                               'selection' : '(ptmiss"+ctrltag+">=380)' },
                                                     'wz1k': { 'plot'      : 'WZ_3LepZ_ptmissSR',
                                                               'bin'       : 8,
                                                               'cuts'      : [ 'WZ_3LepZ' ],
                                                               'selection' : '(ptmiss"+ctrltag+">=160 && ptmiss"+ctrltag+"<220)' } ,
                                                     'wz2k': { 'plot'      : 'WZ_3LepZ_ptmissSR',
                                                               'bin'       : 9,
                                                               'cuts'      : [ 'WZ_3LepZ' ],
                                                               'selection' : '(ptmiss"+ctrltag+">=220 && ptmiss"+ctrltag+"<280)' } ,
                                                     'wz3k': { 'plot'      : 'WZ_3LepZ_ptmissSR',
                                                               'bin'       : 10,
                                                               'cuts'      : [ 'WZ_3LepZ' ],
                                                               'selection' : '(ptmiss"+ctrltag+">=280 && ptmiss"+ctrltag+"<380)' } ,
                                                     'wz4k': { 'plot'      : 'WZ_3LepZ_ptmissSR',
                                                               'bin'       : 11,
                                                               'cuts'      : [ 'WZ_3LepZ' ],
                                                               'selection' : '(ptmiss"+ctrltag+">=380)' },
                                                    },

                            'samples'            : [ 'WZ' ],
                           }, 
                   'ttZ': { 'validationRegion'   : 'ttZValidationRegion',
                            'signal'             : 'ttZ',
                            'exclusiveSelection' : 1,
                            'measurementRegions' : { 'tz1' : { 'plot'      : 'ttZ_ptmissSR',
                                                               'bin'       : 8,
                                                               'cuts'      : [ 'ttZ' ],
                                                               'selection' : '(ptmiss"+ctrltag+">=160 && ptmiss"+ctrltag+"<220)' } ,
                                                     'tz2' : { 'plot'      : 'ttZ_ptmissSR',
                                                               'bin'       : 9,
                                                               'cuts'      : [ 'ttZ' ],
                                                               'selection' : '(ptmiss"+ctrltag+">=220 && ptmiss"+ctrltag+"<280)' } ,
                                                     'tz3' : { 'plot'      : 'ttZ_ptmissSR',
                                                               'bin'       : 10,
                                                               'cuts'      : [ 'ttZ' ],
                                                               'selection' : '(ptmiss"+ctrltag+">=280 && ptmiss"+ctrltag+"<380)' } ,
                                                     'tz4' : { 'plot'      : 'ttZ_ptmissSR',
                                                               'bin'       : 11,
                                                               'cuts'      : [ 'ttZ' ],
                                                               'selection' : '(ptmiss"+ctrltag+">=380)' }
                                                    },
                            'samples'            : [ 'ttZ' ],
                           },
                   'WW': { 'validationRegion'   : 'WZtoWWValidationRegion',
                            'signal'             : 'WZ',
                            'exclusiveSelection' : 0,
                            'measurementRegions' : { 'ww10': { 'plot'      : 'WZtoWW_Zcut10_ptmissSR',
                                                               'bin'       : 8,
                                                               'cuts'      : [ 'WZtoWW_Zcut10' ],
                                                               'selection' : '(ptmiss"+ctrltag+">=160 && ptmiss"+ctrltag+"<220)' } ,
                                                     'ww20': { 'plot'      : 'WZtoWW_Zcut10_ptmissSR',
                                                               'bin'       : 9,
                                                               'cuts'      : [ 'WZtoWW_Zcut10' ],
                                                               'selection' : '(ptmiss"+ctrltag+">=220 && ptmiss"+ctrltag+"<280)' } ,
                                                     'ww30': { 'plot'      : 'WZtoWW_Zcut10_ptmissSR',
                                                               'bin'       : 10,
                                                               'cuts'      : [ 'WZtoWW_Zcut10' ],
                                                               'selection' : '(ptmiss"+ctrltag+">=280 && ptmiss"+ctrltag+"<380)' } ,
                                                     'ww40': { 'plot'      : 'WZtoWW_Zcut10_ptmissSR',
                                                               'bin'       : 11,
                                                               'cuts'      : [ 'WZtoWW_Zcut10' ],
                                                               'selection' : '(ptmiss"+ctrltag+">=380)' },
                                                     'ww15': { 'plot'      : 'WZtoWW_Zcut15_ptmissSR',
                                                               'bin'       : 8,
                                                               'cuts'      : [ 'WZtoWW_Zcut15' ],
                                                               'selection' : '(ptmiss"+ctrltag+">=160 && ptmiss"+ctrltag+"<220)' } ,
                                                     'ww25': { 'plot'      : 'WZtoWW_Zcut15_ptmissSR',
                                                               'bin'       : 9,
                                                               'cuts'      : [ 'WZtoWW_Zcut15' ],
                                                               'selection' : '(ptmiss"+ctrltag+">=220 && ptmiss"+ctrltag+"<280)' } ,
                                                     'ww35': { 'plot'      : 'WZtoWW_Zcut15_ptmissSR',
                                                               'bin'       : 10,
                                                               'cuts'      : [ 'WZtoWW_Zcut15' ],
                                                               'selection' : '(ptmiss"+ctrltag+">=280 && ptmiss"+ctrltag+"<380)' } ,
                                                     'ww45': { 'plot'      : 'WZtoWW_Zcut15_ptmissSR',
                                                               'bin'       : 11,
                                                               'cuts'      : [ 'WZtoWW_Zcut15' ],
                                                               'selection' : '(ptmiss"+ctrltag+">=380)' },
                                                    },

                            'samples'            : [ 'WZ' ],
                           },
                  }



def getYieldsFromHistogram(histo, binNumber):

    if binNumber!=-1:
        return histo.GetBinContent(binNumber), histo.GetBinError(binNumber)
    else:
        integralError = ROOT.double() 
        return histo.IntegralAndError(-1, -1, integralError), integralError

def getYieldsFromTGraphAsymmErrors(graph, binNumber):

    yields, yieldsErrorSquared, yieldsErrorSum = 0., 0., 0.

    if binNumber!=-1 and graph.GetN()<binNumber: return -1., -1.

    for point in range(graph.GetN()):
        if binNumber==-1 or (point+1)==binNumber:
            xP, yP = ROOT.double(), ROOT.double()
            graph.GetPoint(point, xP, yP)
            yields += yP
            yieldsErrorSquared += pow(graph.GetErrorY(point), 2) # that's highly questionable ...
            yieldsErrorSum += graph.GetErrorY(point) # that's highly questionable ...

    return yields, math.sqrt(yieldsErrorSquared), yieldsErrorSum

def getScaleFactorFromCanvas(fileName, canvasName, dataName, signalName, binNumber):

    scaleFactor, scaleFactorError, data, dataError, signal, signalStatError, mc, mcError = -1., -1., -1., -1., -1., -1., -1., -1.

    inputRootFile = ROOT.TFile(fileName, 'read')

    canvas = inputRootFile.Get(canvasName)

    for canvasObj in canvas.GetListOfPrimitives():
        if canvasObj.ClassName()=='TPad':
            for padObject in canvasObj.GetListOfPrimitives():
                if padObject.ClassName()=='TH1D' or padObject.ClassName()=='TH1F':
                    if padObject.GetName()==dataName:
                        data, dataError = getYieldsFromHistogram(padObject, binNumber)
                elif padObject.ClassName()=='TGraphAsymmErrors':
                    if 'Over' not in padObject.GetName(): # this is canvas dependent
                        yields, yieldsErrorSquaredSum, yieldsErrorLinearSum = getYieldsFromTGraphAsymmErrors(padObject, binNumber)
                        if padObject.GetName()=='Graph': data, dataError = yields, yieldsErrorSquaredSum # this is canvas dependent
                        else: mc, mcError = yields, yieldsErrorLinearSum # that's highly questionable ...
                elif padObject.ClassName()=='THStack':
                    for histo in padObject.GetHists():
                        if histo.GetName()==signalName:
                            signal, signalStatError = getYieldsFromHistogram(histo, binNumber)

    if data==-1. or dataError==-1.: print 'getScaleFactorFromCanvas: data yields not found' 
    elif signal==-1. or signalStatError==-1.: print 'getScaleFactorFromCanvas: signal yields not found'
    elif mc==-1. or mcError==-1.: print 'getScaleFactorFromCanvas: mc yields not found'
    else:
        bkg = mc - signal
        #bkgError = bkg*mcError/mc # some assumptions here
        signalError = signal*mcError/mc # some assumptions here
        scaleFactor = (data-bkg)/signal
        #scaleFactorError = math.sqrt(pow(dataError/signal,2)+pow(bkgError/signal,2)+pow((data-bkg)*signalError/(signal*signal),2))
        scaleFactorError = math.sqrt(pow(dataError/signal,2)+pow(data*signalError/(signal*signal),2))#+pow((data-bkg)*signalStatError/(signal*signal),2))

    return scaleFactor, scaleFactorError

if __name__ == '__main__':

    for year in years.split('-'):

        normBackgrounds = {}

        for background in backgroundProcess.split('-'):

            bkgInfo = backgroundInfo[background]

            for sample in bkgInfo['samples']:
                normBackgrounds[sample] = {}
                for meas in bkgInfo['measurementRegions']:
                    normBackgrounds[sample][meas] = {}

            plotDirectory = plotArea+year+'/'+bkgInfo['validationRegion']+commonFlag

            for meas in bkgInfo['measurementRegions']:

                measInfo = bkgInfo['measurementRegions'][meas]

                inputRootFileName = plotDirectory+'/cratio_'+measInfo['plot']+'.root'
                canvasName = 'ccRatio'+measInfo['plot']
                signalName = 'new_histo_group_'+bkgInfo['signal']+'_'+measInfo['plot']            

                scaleFactor, scaleFactorError = getScaleFactorFromCanvas(inputRootFileName, canvasName, 'Graph', signalName, +measInfo['bin']) 

                for sample in bkgInfo['samples']:
                    normBackgrounds[sample][meas]['exclusiveSelection'] = bkgInfo['exclusiveSelection']
                    normBackgrounds[sample][meas]['scalefactor'] = { str(scaleFactor) : str(scaleFactorError) }
                    normBackgrounds[sample][meas]['cuts'] = measInfo['cuts']
                    normBackgrounds[sample][meas]['selection'] = measInfo['selection'] 

            for sample in bkgInfo['samples']:
                print "normBackgrounds['"+sample+"'] = "+json.dumps(normBackgrounds[sample])







 
