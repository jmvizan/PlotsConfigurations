#!/usr/bin/env python
import os
import sys
import ROOT
import math
import copy
import optparse
import json
import copy
from array import *

backgroundProcess = sys.argv[1] if (len(sys.argv)>=2 and sys.argv[1]!='All') else 'ZZ-ttZ-WZW-WZZ-WZ'
years = sys.argv[2] if len(sys.argv)>=3 else '2016HIPM,2016noHIPM,2017,2018'

commonFlag = 'VetoesUL'
plotArea = './Plots/'

if 'WWmt2bin' in backgroundProcess:
    if 'Optim' in backgroundProcess:
        mt2llHistoName = 'mt2llOptimHighExtra'
        mt2llHistoBins = 9
        searchBins = [0, 20, 40, 60, 80, 100, 160, 240, 370, 500]
    elif 'Uni20' in backgroundProcess:
        mt2llHistoName = 'mt2llUni20'
        mt2llHistoBins = 25
        searchBins = [x*20. for x in range(0,26)]
    elif 'Uni40' in backgroundProcess:
        mt2llHistoName = 'mt2llUni40'
        mt2llHistoBins = 13
        searchBins = [x*40. for x in range(0,14)]
    elif 'Uni50' in backgroundProcess:
        mt2llHistoName = 'mt2llUni50'
        mt2llHistoBins = 10
        searchBins = [x*50. for x in range(0,11)]
    centerBins = [ (searchBins[x]+searchBins[x+1])/2. for x in range(len(searchBins)-1) ]

backgroundInfo = { 'ZZ' : { 'validationRegion'   : 'ZZValidationRegion',
                            'signal'             : 'ZZTo4L',
                            'exclusiveSelection' : 1,
                            'measurementRegions' : { 'zz1' : { 'plot'      : 'ZZ_ptmissSR', 
                                                               'bin'       : 8,
                                                               'cuts'      : [ '_NoJet', '_Veto', '_NoTag', '_Tag', 'ZZ' ], 
                                                               'selection' : '(ptmiss\'+ctrltag+\'>=160 && ptmiss\'+ctrltag+\'<220)' } ,
                                                     'zz2' : { 'plot'      : 'ZZ_ptmissSR',
                                                               'bin'       : 9,
                                                               'cuts'      : [ '_NoJet', '_Veto', '_NoTag', '_Tag', 'ZZ' ],
                                                               'selection' : '(ptmiss\'+ctrltag+\'>=220 && ptmiss\'+ctrltag+\'<280)' } ,
                                                     'zz3' : { 'plot'      : 'ZZ_ptmissSR',
                                                               'bin'       : 10,
                                                               'cuts'      : [ '_NoJet', '_Veto', '_NoTag', '_Tag', 'ZZ' ],
                                                               'selection' : '(ptmiss\'+ctrltag+\'>=280 && ptmiss\'+ctrltag+\'<380)' } ,
                                                     'zz4' : { 'plot'      : 'ZZ_ptmissSR',
                                                               'bin'       : 11,
                                                               'cuts'      : [ '_NoJet', '_Veto', '_NoTag', '_Tag', 'ZZ' ],
                                                               'selection' : '(ptmiss\'+ctrltag+\'>=380)' }
                                                    },
                            'samples'            : [ 'ZZTo2L2Nu', 'ZZTo4L' ],
                           },
                   'WZ' : { 'validationRegion'   : 'WZValidationRegion',
                            'signal'             : 'WZ',
                            'exclusiveSelection' : 0,
                            'measurementRegions' : { 'wz1' : { 'plot'      : 'WZ_3Lep__ptmissSR',
                                                               'bin'       : 8,
                                                               'cuts'      : [ '_NoJet', '_Veto', '_NoTag', '_Tag', 'WZ_3Lep_' ],
                                                               'selection' : '(ptmiss\'+ctrltag+\'>=160 && ptmiss\'+ctrltag+\'<220)' } ,
                                                     'wz2' : { 'plot'      : 'WZ_3Lep__ptmissSR',
                                                               'bin'       : 9,
                                                               'cuts'      : [ '_NoJet', '_Veto', '_NoTag', '_Tag', 'WZ_3Lep_' ],
                                                               'selection' : '(ptmiss\'+ctrltag+\'>=220 && ptmiss\'+ctrltag+\'<280)' } ,
                                                     'wz3' : { 'plot'      : 'WZ_3Lep__ptmissSR',
                                                               'bin'       : 10,
                                                               'cuts'      : [ '_NoJet', '_Veto', '_NoTag', '_Tag', 'WZ_3Lep_' ],
                                                               'selection' : '(ptmiss\'+ctrltag+\'>=280 && ptmiss\'+ctrltag+\'<380)' } ,
                                                     'wz4' : { 'plot'      : 'WZ_3Lep__ptmissSR',
                                                               'bin'       : 11,
                                                               'cuts'      : [ '_NoJet', '_Veto', '_NoTag', '_Tag', 'WZ_3Lep_' ],
                                                               'selection' : '(ptmiss\'+ctrltag+\'>=380)' },
                                                     'wz1p': { 'plot'      : 'WZ_3LepZ_ptmissSR',
                                                               'bin'       : 8,
                                                               'cuts'      : [ 'WZ_3LepZ' ],
                                                               'selection' : '(ptmiss\'+ctrltag+\'>=160 && ptmiss\'+ctrltag+\'<220)' } ,
                                                     'wz2p': { 'plot'      : 'WZ_3LepZ_ptmissSR',
                                                               'bin'       : 9,
                                                               'cuts'      : [ 'WZ_3LepZ' ],
                                                               'selection' : '(ptmiss\'+ctrltag+\'>=220 && ptmiss\'+ctrltag+\'<280)' } ,
                                                     'wz3p': { 'plot'      : 'WZ_3LepZ_ptmissSR',
                                                               'bin'       : 10,
                                                               'cuts'      : [ 'WZ_3LepZ' ],
                                                               'selection' : '(ptmiss\'+ctrltag+\'>=280 && ptmiss\'+ctrltag+\'<380)' } ,
                                                     'wz4p': { 'plot'      : 'WZ_3LepZ_ptmissSR',
                                                               'bin'       : 11,
                                                               'cuts'      : [ 'WZ_3LepZ' ],
                                                               'selection' : '(ptmiss\'+ctrltag+\'>=380)' },
                                                    },
                   
                            'samples'            : [ 'WZ' ],
                           },
                   'WZZ': { 'validationRegion'   : 'WZValidationRegionZLeps',
                            'signal'             : 'WZ',
                            'exclusiveSelection' : 0,
                            'measurementRegions' : { 'wz1z': { 'plot'      : 'WZ_3Lep__ptmissSR',
                                                               'bin'       : 8,
                                                               'cuts'      : [ 'WZ_3Lep_' ],
                                                               'selection' : '(ptmiss\'+ctrltag+\'>=160 && ptmiss\'+ctrltag+\'<220)' } ,
                                                     'wz2z': { 'plot'      : 'WZ_3Lep__ptmissSR',
                                                               'bin'       : 9,
                                                               'cuts'      : [ 'WZ_3Lep_' ],
                                                               'selection' : '(ptmiss\'+ctrltag+\'>=220 && ptmiss\'+ctrltag+\'<280)' } ,
                                                     'wz3z': { 'plot'      : 'WZ_3Lep__ptmissSR',
                                                               'bin'       : 10,
                                                               'cuts'      : [ 'WZ_3Lep_' ],
                                                               'selection' : '(ptmiss\'+ctrltag+\'>=280 && ptmiss\'+ctrltag+\'<380)' } ,
                                                     'wz4z': { 'plot'      : 'WZ_3Lep__ptmissSR',
                                                               'bin'       : 11,
                                                               'cuts'      : [ 'WZ_3Lep_' ],
                                                               'selection' : '(ptmiss\'+ctrltag+\'>=380)' },
                                                     'wz1k': { 'plot'      : 'WZ_3LepZ_ptmissSR',
                                                               'bin'       : 8,
                                                               'cuts'      : [ 'WZ_3LepZ' ],
                                                               'selection' : '(ptmiss\'+ctrltag+\'>=160 && ptmiss\'+ctrltag+\'<220)' } ,
                                                     'wz2k': { 'plot'      : 'WZ_3LepZ_ptmissSR',
                                                               'bin'       : 9,
                                                               'cuts'      : [ 'WZ_3LepZ' ],
                                                               'selection' : '(ptmiss\'+ctrltag+\'>=220 && ptmiss\'+ctrltag+\'<280)' } ,
                                                     'wz3k': { 'plot'      : 'WZ_3LepZ_ptmissSR',
                                                               'bin'       : 10,
                                                               'cuts'      : [ 'WZ_3LepZ' ],
                                                               'selection' : '(ptmiss\'+ctrltag+\'>=280 && ptmiss\'+ctrltag+\'<380)' } ,
                                                     'wz4k': { 'plot'      : 'WZ_3LepZ_ptmissSR',
                                                               'bin'       : 11,
                                                               'cuts'      : [ 'WZ_3LepZ' ],
                                                               'selection' : '(ptmiss\'+ctrltag+\'>=380)' },
                                                    },

                            'samples'            : [ 'WZ' ],
                           }, 
                   'ttZ': { 'validationRegion'   : 'ttZValidationRegion',
                            'signal'             : 'ttZ',
                            'exclusiveSelection' : 0,
                            'measurementRegions' : { 'tz10': { 'plot'      : 'ttZ_Zcut10_ptmissSR',
                                                               'bin'       : 8,
                                                               'cuts'      : [ 'ttZ_Zcut10' ],
                                                               'selection' : '(ptmiss\'+ctrltag+\'>=160 && ptmiss\'+ctrltag+\'<220)' } ,
                                                     'tz20': { 'plot'      : 'ttZ_Zcut10_ptmissSR',
                                                               'bin'       : 9,
                                                               'cuts'      : [ 'ttZ_Zcut10' ],
                                                               'selection' : '(ptmiss\'+ctrltag+\'>=220 && ptmiss\'+ctrltag+\'<280)' } ,
                                                     'tz30': { 'plot'      : 'ttZ_Zcut10_ptmissSR',
                                                               'bin'       : 10,
                                                               'cuts'      : [ 'ttZ_Zcut10' ],
                                                               'selection' : '(ptmiss\'+ctrltag+\'>=280 && ptmiss\'+ctrltag+\'<380)' } ,
                                                     'tz40': { 'plot'      : 'ttZ_Zcut10_ptmissSR',
                                                               'bin'       : 11,
                                                               'cuts'      : [ 'ttZ_Zcut10' ],
                                                               'selection' : '(ptmiss\'+ctrltag+\'>=380)' },
                                                     'tz15': { 'plot'      : 'ttZ_Zcut15_ptmissSR',
                                                               'bin'       : 8,
                                                               'cuts'      : [ 'ttZ_Zcut15' ],
                                                               'selection' : '(ptmiss\'+ctrltag+\'>=160 && ptmiss\'+ctrltag+\'<220)' } ,
                                                     'tz25': { 'plot'      : 'ttZ_Zcut15_ptmissSR',
                                                               'bin'       : 9,
                                                               'cuts'      : [ 'ttZ_Zcut15' ],
                                                               'selection' : '(ptmiss\'+ctrltag+\'>=220 && ptmiss\'+ctrltag+\'<280)' } ,
                                                     'tz35': { 'plot'      : 'ttZ_Zcut15_ptmissSR',
                                                               'bin'       : 10,
                                                               'cuts'      : [ 'ttZ_Zcut15' ],
                                                               'selection' : '(ptmiss\'+ctrltag+\'>=280 && ptmiss\'+ctrltag+\'<380)' } ,
                                                     'tz45': { 'plot'      : 'ttZ_Zcut15_ptmissSR',
                                                               'bin'       : 11,
                                                               'cuts'      : [ 'ttZ_Zcut15' ],
                                                               'selection' : '(ptmiss\'+ctrltag+\'>=380)' }
                                                    },
                            'samples'            : [ 'ttZ' ],
                           },
                   'WZW': { 'validationRegion'   : 'WZtoWWValidationRegionTL2',
                            'signal'             : 'WZ',
                            'exclusiveSelection' : 0,
                            'measurementRegions' : { 'wwa0': { 'plot'      : 'WZtoWW_Zcut10_ptmissSR',
                                                               'bin'       : 6,
                                                               'cuts'      : [ 'WZtoWW_Zcut10' ],
                                                               'selection' : '(ptmiss\'+ctrltag+\'>=100 && ptmiss\'+ctrltag+\'<120)' } ,
                                                     'wwb0': { 'plot'      : 'WZtoWW_Zcut10_ptmissSR',
                                                               'bin'       : 7,
                                                               'cuts'      : [ 'WZtoWW_Zcut10' ],
                                                               'selection' : '(ptmiss\'+ctrltag+\'>=120 && ptmiss\'+ctrltag+\'<160)' } ,
                                                     #'wwc0': { 'plot'      : 'WZtoWW_Zcut10_ptmissSR',
                                                     #          'bin'       : [8,11],
                                                     #          'cuts'      : [ 'WZtoWW_Zcut10' ],
                                                     #          'selection' : '(ptmiss\'+ctrltag+\'>=160)' } ,
                                                     'ww10': { 'plot'      : 'WZtoWW_Zcut10_ptmissSR',
                                                               'bin'       : 8,
                                                               'cuts'      : [ 'WZtoWW_Zcut10' ],
                                                               'selection' : '(ptmiss\'+ctrltag+\'>=160 && ptmiss\'+ctrltag+\'<220)' } ,
                                                     'ww20': { 'plot'      : 'WZtoWW_Zcut10_ptmissSR',
                                                               'bin'       : 9,
                                                               'cuts'      : [ 'WZtoWW_Zcut10' ],
                                                               'selection' : '(ptmiss\'+ctrltag+\'>=220 && ptmiss\'+ctrltag+\'<280)' } ,
                                                     'ww30': { 'plot'      : 'WZtoWW_Zcut10_ptmissSR',
                                                               'bin'       : 10,
                                                               'cuts'      : [ 'WZtoWW_Zcut10' ],
                                                               'selection' : '(ptmiss\'+ctrltag+\'>=280 && ptmiss\'+ctrltag+\'<380)' } ,
                                                     'ww40': { 'plot'      : 'WZtoWW_Zcut10_ptmissSR',
                                                               'bin'       : 11,
                                                               'cuts'      : [ 'WZtoWW_Zcut10' ],
                                                               'selection' : '(ptmiss\'+ctrltag+\'>=380)' },
                                                     'wwa5': { 'plot'      : 'WZtoWW_Zcut15_ptmissSR',
                                                               'bin'       : 6,
                                                               'cuts'      : [ 'WZtoWW_Zcut15' ],
                                                               'selection' : '(ptmiss\'+ctrltag+\'>=100 && ptmiss\'+ctrltag+\'<120)' } ,
                                                     'wwb5': { 'plot'      : 'WZtoWW_Zcut15_ptmissSR',
                                                               'bin'       : 7,
                                                               'cuts'      : [ 'WZtoWW_Zcut15' ],
                                                               'selection' : '(ptmiss\'+ctrltag+\'>=120 && ptmiss\'+ctrltag+\'<160)' } , 
                                                     #'wwc5': { 'plot'      : 'WZtoWW_Zcut15_ptmissSR',
                                                     #          'bin'       : [8,11],
                                                     #          'cuts'      : [ 'WZtoWW_Zcut15' ],
                                                     #          'selection' : '(ptmiss\'+ctrltag+\'>=160)' } ,
                                                     'ww15': { 'plot'      : 'WZtoWW_Zcut15_ptmissSR',
                                                               'bin'       : 8,
                                                               'cuts'      : [ 'WZtoWW_Zcut15' ],
                                                               'selection' : '(ptmiss\'+ctrltag+\'>=160 && ptmiss\'+ctrltag+\'<220)' } ,
                                                     'ww25': { 'plot'      : 'WZtoWW_Zcut15_ptmissSR',
                                                               'bin'       : 9,
                                                               'cuts'      : [ 'WZtoWW_Zcut15' ],
                                                               'selection' : '(ptmiss\'+ctrltag+\'>=220 && ptmiss\'+ctrltag+\'<280)' } ,
                                                     'ww35': { 'plot'      : 'WZtoWW_Zcut15_ptmissSR',
                                                               'bin'       : 10,
                                                               'cuts'      : [ 'WZtoWW_Zcut15' ],
                                                               'selection' : '(ptmiss\'+ctrltag+\'>=280 && ptmiss\'+ctrltag+\'<380)' } ,
                                                     'ww45': { 'plot'      : 'WZtoWW_Zcut15_ptmissSR',
                                                               'bin'       : 11,
                                                               'cuts'      : [ 'WZtoWW_Zcut15' ],
                                                               'selection' : '(ptmiss\'+ctrltag+\'>=380)' },
                                                    },

                            'samples'            : [ 'WZ' ],
                           },
                   'WW' : { 'validationRegion'   : 'HighPtMissValidationRegion',
                            'signal'             : 'WW',
                            'exclusiveSelection' : 1,
                            'measurementRegions' : { 'nojet': {'plot'      : 'VR1_NoJet_em_mt2llOptim',
                                                               'bin'       : -1,
                                                               'cuts'      : [ 'VR1' ],
                                                               'selection' : '(Alt$(CleanJet_pt[0],0)<\'+jetPtCut+\')' } ,
                                                    },
                            'samples'            : [ 'WW' ],
                           }
                  }

if 'WWmt2bin' in backgroundProcess:
    backgroundInfo[backgroundProcess] = { 'validationRegion'   : 'WZtoWWValidationRegionNormWZ',
                                          'signal'             : 'WZ',
                                          'exclusiveSelection' : 0,
                                          'measurementRegions' : { 'wwmt2bin1' : { 'plot'      : 'WZtoWW_Zcut15_ptmiss-100_'+mt2llHistoName,
                                                                   'bin'       : 1,
                                                                   'cuts'      : [ 'WZtoWW_Zcut15_ptmiss-100' ],
                                                                   'selection' : '' } } ,
                                          'samples'            : [ 'WW' ],
                                         }
    for ibin in range(2, mt2llHistoBins+1):
        backgroundInfo[backgroundProcess]['measurementRegions']['wwmt2bin'+str(ibin)] = copy.deepcopy(backgroundInfo[backgroundProcess]['measurementRegions']['wwmt2bin1']) 
        backgroundInfo[backgroundProcess]['measurementRegions']['wwmt2bin'+str(ibin)]['bin'] = ibin

def getYieldsFromHistogram(histo, binNumber):

    if type(binNumber)==list: firstBin, lastBin = binNumber[0], binNumber[1]
    else: firstBin, lastBin = binNumber, binNumber

    if firstBin!=-1. and firstBin==lastBin:
        return histo.GetBinContent(binNumber), histo.GetBinError(binNumber)
    else:
        integralError = ROOT.double() 
        return histo.IntegralAndError(firstBin, lastBin, integralError), integralError

def getYieldsFromTGraphAsymmErrors(graph, binNumber):

    yields, yieldsErrorSquared, yieldsErrorSum, yieldsErrorHighSquared, yieldsErrorLowSquared = 0., 0., 0., 0., 0.

    if type(binNumber)==list: firstBin, lastBin = binNumber[0], binNumber[1]
    else: firstBin, lastBin = binNumber, binNumber

    if lastBin!=-1 and graph.GetN()<lastBin: return -1., -1., -1., -1., 1.

    if firstBin==-1: firstBin = 1
    if lastBin==-1: lastBin = graph.GetN() 

    for point in range(graph.GetN()):
        if (point+1)>=firstBin and (point+1)<=lastBin:
            xP, yP = ROOT.double(), ROOT.double()
            graph.GetPoint(point, xP, yP)
            yields += yP
            yieldsErrorSquared += pow(graph.GetErrorY(point), 2) # that's highly questionable ...
            yieldsErrorHighSquared += pow(graph.GetErrorYhigh(point), 2) # that's highly questionable ...
            yieldsErrorLowSquared += pow(graph.GetErrorYlow(point), 2) # that's highly questionable ...
            yieldsErrorSum += graph.GetErrorY(point) # that's highly questionable ...

    return yields, math.sqrt(yieldsErrorSquared), yieldsErrorSum, math.sqrt(yieldsErrorHighSquared), math.sqrt(yieldsErrorLowSquared)

def getScaleFactorFromCanvas(fileName, canvasName, dataName, signalName, binNumber):

    scaleFactor, scaleFactorError, scaleFactorErrorHigh, scaleFactorErrorLow, data, dataError, dataErrorHigh, dataErrorLow, signal, signalStatError, mc, mcError = -1., -1., -1., -1., -1., -1., -1., -1., -1., -1., -1., -1.

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
                        yields, yieldsErrorSquaredSum, yieldsErrorLinearSum,  yieldsErrorHighSquaredSum,  yieldsErrorLowSquaredSum = getYieldsFromTGraphAsymmErrors(padObject, binNumber)
                        if padObject.GetName()=='Graph': data, dataError, dataErrorHigh, dataErrorLow = yields, yieldsErrorSquaredSum, yieldsErrorHighSquaredSum,  yieldsErrorLowSquaredSum # this is canvas dependent
                        else: mc, mcError = yields, yieldsErrorLinearSum # that's highly questionable ...
                elif padObject.ClassName()=='THStack':
                    for histo in padObject.GetHists():
                        if histo.GetName()==signalName:
                            signal, signalStatError = getYieldsFromHistogram(histo, binNumber)

    if data==-1. or dataError==-1.: print 'getScaleFactorFromCanvas: data yields not found' 
    elif signal==-1. or signalStatError==-1.: print 'getScaleFactorFromCanvas: signal yields not found'
    elif mc==-1. or mcError==-1.: print 'getScaleFactorFromCanvas: mc yields not found'
    elif signal>0.:
        bkg = mc - signal
        #bkgError = bkg*mcError/mc # some assumptions here
        signalError = signal*mcError/mc # some assumptions here
        scaleFactor = (data-bkg)/signal
        #scaleFactorError = math.sqrt(pow(dataError/signal,2)+pow(bkgError/signal,2)+pow((data-bkg)*signalError/(signal*signal),2))
        #scaleFactorError = math.sqrt(pow(dataError/signal,2)+pow(data*signalError/(signal*signal),2))#+pow((data-bkg)*signalStatError/(signal*signal),2))
        scaleFactorError = dataError/signal
        scaleFactorErrorHigh = dataErrorHigh/signal
        scaleFactorErrorLow = dataErrorLow/signal
        if scaleFactor<=0.: scaleFactor = 0.001
    return scaleFactor, scaleFactorError, scaleFactorErrorHigh, scaleFactorErrorLow

if __name__ == '__main__':

    for year in years.split(','):
        print '\t\tYEAR:'+year+'\n'
        normBackgrounds = {}

        if 'WWmt2' in backgroundProcess:
            mt2llHisto = ROOT.TH1D('mt2ll','',len(searchBins)-1,array('d',searchBins))
            mt2llHisto.SetMinimum(0.)
            mt2llHisto.SetMaximum(2.)
            mt2llGraph = ROOT.TGraphAsymmErrors()
            if 'Optim' in backgroundProcess:
                baseRootFile = ROOT.TFile('./Shapes/'+year+'/'+backgroundInfo[backgroundProcess]['validationRegion'].replace('NormWZ','')+commonFlag+'/plots_'+backgroundInfo[backgroundProcess]['validationRegion'].replace('NormWZ','')+commonFlag+'_SM.root', 'read')
                baseWZHistoUni20 = baseRootFile.Get('WZtoWW_Zcut15_ptmiss-100/mt2llUni20/histo_WZ')
                for ib in range(len(searchBins)-1):
                    wgtm, wgt = 0., 0.
                    for ibc in range(1, baseWZHistoUni20.GetNbinsX()+1):
                        if baseWZHistoUni20.GetBinCenter(ibc)>=searchBins[ib] and baseWZHistoUni20.GetBinCenter(ibc)<searchBins[ib+1]:
                            wgt += baseWZHistoUni20.GetBinContent(ibc)
                            wgtm += baseWZHistoUni20.GetBinContent(ibc)*baseWZHistoUni20.GetBinCenter(ibc)
                    centerBins[ib] = wgtm/wgt

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

                scaleFactor, scaleFactorError, scaleFactorErrorHigh, scaleFactorErrorLow = getScaleFactorFromCanvas(inputRootFileName, canvasName, 'Graph', signalName, measInfo['bin']) 

                for sample in bkgInfo['samples']:
                    normBackgrounds[sample][meas]['exclusiveSelection'] = bkgInfo['exclusiveSelection']
                    normBackgrounds[sample][meas]['scalefactor'] = { str(scaleFactor) : str(scaleFactorError) }
                    normBackgrounds[sample][meas]['cuts'] = measInfo['cuts']
                    normBackgrounds[sample][meas]['selection'] = measInfo['selection'] 

                if 'wwmt2bin' in meas and scaleFactor>0.:
                    ib = int(meas.replace('wwmt2bin',''))
                    #mt2llHisto.SetBinContent(ib, scaleFactor)
                    #mt2llHisto.SetBinError(ib, scaleFactorError)
                    mt2llGraph.SetPoint(ib-1, centerBins[ib-1], scaleFactor)
                    mt2llGraph.SetPointError(ib-1, centerBins[ib-1]-searchBins[ib-1], searchBins[ib]-centerBins[ib-1], scaleFactorErrorLow, scaleFactorErrorHigh)

            for sample in bkgInfo['samples']:
                print '\t\tnormBackgrounds[\''+sample+'\'] = '+json.dumps(normBackgrounds[sample]).replace('"','\'')
        
        if 'WWmt2' in backgroundProcess:
            ROOT.gStyle.SetOptStat(ROOT.kFALSE)
            plotCanvas = ROOT.TCanvas( 'plotCanvas', '', 1200, 900)
            mt2llHisto.Draw()
            mt2llHisto.SetXTitle('#font[50]{m}_{T2}(#font[12]{ll}) [GeV]')
            mt2llHisto.SetYTitle('(Data-Back.)/WZ')
            minMT2Fit = 0.
            drawErrors = False
            #mt2llFun = ROOT.TF1('mt2llFun', '[0]+[1]*x+[2]*x*x', mt2llHisto.GetBinLowEdge(1),  mt2llHisto.GetBinLowEdge(mt2llHisto.GetNbinsX()+1))
            mt2llFun = ROOT.TF1('mt2llFun', '[0]+[1]*x', mt2llHisto.GetBinLowEdge(1),  mt2llHisto.GetBinLowEdge(mt2llHisto.GetNbinsX()+1)); minMT2Fit = 40.; drawErrors = True
            #mt2llFun = ROOT.TF1('mt2llFun', '[0]+[1]*log(x+[3])*log(x+[3])*(3-[2]*log(x+[3]))', mt2llHisto.GetBinLowEdge(1),  mt2llHisto.GetBinLowEdge(mt2llHisto.GetNbinsX()+1))
            #mt2llFun = ROOT.TF1('mt2llFun', '[0]*(1.+[1]*x)/(1.+[2]*x)', mt2llHisto.GetBinLowEdge(1),  mt2llHisto.GetBinLowEdge(mt2llHisto.GetNbinsX()+1)); mt2llFun.SetParameters(9.06333e-01, 7.05381e-03, 3.33219e-03)
            #mt2llFun = ROOT.TF1('mt2llFun', '[0]*(1.+[1]*x+[3]*x*x)/(1.+[2]*x+[4]*x*x)', mt2llHisto.GetBinLowEdge(1),  mt2llHisto.GetBinLowEdge(mt2llHisto.GetNbinsX()+1)); mt2llFun.SetParameters(4.83969e-01, 1.08049e+00, 5.47807e-01, 1.76432e-03, 0.)
            fitReults = mt2llGraph.Fit(mt2llFun, 'S', '', minMT2Fit, 600.)
            mt2llGraph.Draw('P0')
            if drawErrors:
                corMatrix = fitReults.GetCorrelationMatrix()
                #corMatrix.Print()
                x1 = (1.-mt2llFun.GetParameter(0))/mt2llFun.GetParameter(1)
                slopeUp  = mt2llFun.GetParameter(1)+mt2llFun.GetParError(1)
                #offsetUp = mt2llFun.GetParameter(0)-mt2llFun.GetParError(0)
                offsetUp = 1. - slopeUp*x1
                slopeDo  = mt2llFun.GetParameter(1)-mt2llFun.GetParError(1)
                #offsetDo = mt2llFun.GetParameter(0)+mt2llFun.GetParError(0)
                offsetDo = 1. - slopeDo*x1
                print x1, mt2llFun.GetParameter(0), mt2llFun.GetParameter(1), offsetUp, slopeUp, offsetDo, slopeDo
                fitUp = ROOT.TLine(minMT2Fit, offsetUp+minMT2Fit*slopeUp, 500., offsetUp+500.*slopeUp)
                fitDo = ROOT.TLine(minMT2Fit, offsetDo+minMT2Fit*slopeDo, 500., offsetDo+500.*slopeDo)
                fitUp.SetLineColor(2); fitUp.SetLineStyle(2); fitUp.Draw()
                fitDo.SetLineColor(2); fitDo.SetLineStyle(2); fitDo.Draw()
            plotCanvas.Print('./Plots/'+year+'/'+backgroundInfo[backgroundProcess]['validationRegion']+commonFlag+'/fit_'+backgroundProcess.replace('WWmt2bin','')+'.png')
            
