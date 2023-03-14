#!/usr/bin/env python
import os
import sys
import ROOT
import math
import optparse
from array import *

def mergeBins(shape, ibin, fbin):

    shapeerr = ROOT.double()
    shapecon = shape.IntegralAndError(ibin, fbin, shapeerr)
    for ib in range(ibin, fbin+1):
        shape.SetBinContent(ib, shapecon)
        shape.SetBinError(ib, shapeerr)
    return shape

def getBinsToMerge(shape, lastBin, keepSix):

    binsToMerge = []

    uncMax = 10.
    nshpMax, binMax, binMaxUnc = -1, -1, uncMax
    for nshp in range(3):
        for ib in range(1, lastBin+1):
            mergedBin = False
            for rangeToMerge in binsToMerge:
                if ib>=rangeToMerge[0] and ib<=rangeToMerge[1]:
                    mergedBin = True
            if not mergedBin and 100.*shape[nshp].GetBinError(ib)/shape[nshp].GetBinContent(ib)>binMaxUnc:
                nshpMax, binMax, binMaxUnc = nshp, ib, 100.*shape[nshp].GetBinError(ib)/shape[nshp].GetBinContent(ib) 
    while nshpMax>-1 and binMax>-1:
        bP, bM = 0, 0
        mergedUnc = 0.
        for bp in range(0, lastBin-binMax+1):
            for bm in range(0, binMax):
                shapeerr = ROOT.double()
                shapecon = shape[nshpMax].IntegralAndError(binMax-bm, binMax+bp, shapeerr)
                if 100.*abs(shapeerr/shapecon)<uncMax and 100.*abs(shapeerr/shapecon)>mergedUnc:
                    bP, bM = bp, bm
                    mergedUnc = 100.*abs(shapeerr/shapecon)
        binsToMerge.append([binMax-bM, binMax+bP])
        nshpMax, binMax, binMaxUnc = -1, -1, uncMax
        for nshp in range(3):
            for ib in range(1, lastBin+1):
                mergedBin = False
                for rangeToMerge in binsToMerge:
                    if ib>=rangeToMerge[0] and ib<=rangeToMerge[1]:
                        mergedBin = True
                if not mergedBin and 100.*shape[nshp].GetBinError(ib)/shape[nshp].GetBinContent(ib)>binMaxUnc:
                    nshpMax, binMax, binMaxUnc = nshp, ib, 100.*shape[nshp].GetBinError(ib)/shape[nshp].GetBinContent(ib)

    rangeToRemove = []
    rangeToAppend = []
    foundMerge = False
    for range1 in range(len(binsToMerge)):
        if not foundMerge:
            for range2 in range(range1+1, len(binsToMerge)):
                if not foundMerge:
                    rangeToMerge1 = binsToMerge[range1]
                    rangeToMerge2 = binsToMerge[range2]
                    if (rangeToMerge1[0]>=rangeToMerge2[0] and rangeToMerge1[0]<=rangeToMerge2[1]) or (rangeToMerge2[0]>=rangeToMerge1[0] and rangeToMerge2[0]<=rangeToMerge1[1]):
                        minExt = min(rangeToMerge1[0],rangeToMerge2[0])
                        maxExt = max(rangeToMerge1[1],rangeToMerge2[1])
                        rangeToAppend.append([minExt,maxExt])
                        rangeToRemove.append(rangeToMerge1)
                        rangeToRemove.append(rangeToMerge2)
                        foundMerge = True
    while len(rangeToAppend)>0:
        for range1 in rangeToRemove:
            binsToMerge.remove(range1) 
        for range1 in rangeToAppend:
            binsToMerge.append(range1)
        rangeToRemove = []
        rangeToAppend = []
        foundMerge = False
        for rangeToMerge1 in binsToMerge:
            if not foundMerge:
                for rangeToMerge2 in binsToMerge:
                    if rangeToMerge1==rangeToMerge2: continue
                    if (rangeToMerge1[0]>=rangeToMerge2[0] and rangeToMerge1[0]<=rangeToMerge2[1]) or (rangeToMerge2[0]>=rangeToMerge2[0] and rangeToMerge2[0]<=rangeToMerge2[1]):
                        if not foundMerge:
                            minExt = min(rangeToMerge1[0],rangeToMerge2[0])
                            maxExt = max(rangeToMerge1[1],rangeToMerge2[1])
                            rangeToAppend.append([minExt,maxExt])
                            rangeToRemove.append(rangeToMerge1)
                            rangeToRemove.append(rangeToMerge2)
                            foundMerge = True

    if keepSix:
        rangeToRemove = []
        rangeToAppend = []
        for range1 in binsToMerge:
            if 6>=range1[0] and 6<range1[1]:
                rangeToRemove.append(range1)
                if range1[1]!=7:
                    rangeToAppend.append([7,range1[1]])
        for range1 in rangeToRemove:
            binsToMerge.remove(range1)
        for range1 in rangeToAppend:
            binsToMerge.append(range1)

    return binsToMerge

def mergeShapeBins(shape, shapeUp, shapeDo, lastBin, keepSix = True):

    binsToMerge = getBinsToMerge(shape, lastBin, keepSix)
    lastBinAfterMerging = lastBin
    for rangeToMerge in binsToMerge:
        print '   ---> Merging', rangeToMerge
        if lastBinAfterMerging>=rangeToMerge[0] and lastBinAfterMerging<=rangeToMerge[1]: lastBinAfterMerging = rangeToMerge[0]
        for nshp in range(3):
            mergeBins(shape[nshp], rangeToMerge[0], rangeToMerge[1])
            mergeBins(shapeUp[nshp], rangeToMerge[0], rangeToMerge[1])
            mergeBins(shapeDo[nshp], rangeToMerge[0], rangeToMerge[1])
    
    return shape, shapeUp, shapeDo, lastBinAfterMerging

errThrs = 4.

def applyResult(corrUnc, emRawUnc, sfRawUnc, corrUncOpp, emRawUncOpp, sfRawUncOpp, emStat, sfStat):

    #rawCorrThrs = 1.
    #if emRawUnc!=0. and sfRawUnc!=0.: rawCorrThrs = min(abs(emStat/emRawUnc), abs(sfStat/sfRawUnc), abs(emStat/sfRawUnc), abs(sfStat/emRawUnc))
    #elif emRawUnc!=0.: rawCorrThrs = min(abs(emStat/emRawUnc), abs(sfStat/emRawUnc)) 
    #elif sfRawUnc!=0.: rawCorrThrs = min(abs(sfStat/sfRawUnc), abs(emStat/sfRawUnc))
    corrThrs = 1.#min(2., pow(1.15, math.sqrt(max(1.,rawCorrThrs)-1.)))     
    emUnc, sfUnc = 999., 999.
    if getSign(emRawUnc)==getSign(corrUnc) and abs(emRawUnc)<errThrs*corrThrs:
        emUnc = emRawUnc
    if getSign(sfRawUnc)==getSign(corrUnc) and abs(sfRawUnc)<errThrs*corrThrs:
        sfUnc = sfRawUnc
    minUn = min(abs(emUnc), abs(sfUnc))
    if minUn<999.:
        maxUn = max(abs(emUnc), abs(sfUnc))
        rawunc = minUn if maxUn>=999. else maxUn
        if abs(corrUnc)<0.66*rawunc:
            #if rawunc>errThrs:
            #    print '   ---> New apply strategy', corrUnc, emRawUnc, sfRawUnc, rawunc, '(',emStat, sfStat, corrThrs,')'
            return False, rawunc*getSign(corrUnc)

    if getSign(emRawUnc)==getSign(corrUnc) and getSign(sfRawUnc)==getSign(corrUnc) and getSign(emRawUncOpp)==getSign(corrUncOpp) and getSign(sfRawUncOpp)==getSign(corrUncOpp): 
        minUn = min(abs(emRawUnc), abs(sfRawUnc), abs(emRawUncOpp), abs(sfRawUncOpp))
        if minUn<2.*errThrs and abs(corrUnc)<0.66*minUn:
            #print '   ---> New apply strategy four'
            return False, minUn*getSign(corrUnc)

    if getSign(emRawUnc)==getSign(corrUnc) and getSign(sfRawUnc)==getSign(corrUnc) and abs(emRawUnc)>4. and abs(sfRawUnc)>4.:
        if abs(emRawUnc/emStat)>0.25 and abs(sfRawUnc/sfStat)>0.25 and abs(corrUnc)<4. and abs(corrUnc)<0.66*min(abs(emRawUnc), abs(sfRawUnc)): 
            #print '   ---> New apply strategy both', corrUnc
            return False, 4.*getSign(corrUnc)

    return True, corrUnc

def setConsistency(corrUncUp, emRawUncUp, sfRawUncUp, corrUncDo, emRawUncDo, sfRawUncDo):

    var = 'None'
    if abs(corrUncUp)<0.5*abs(corrUncDo):
        var, emRawUnc, sfRawUnc, corrUnc = 'Up', abs(emRawUncUp), abs(sfRawUncUp), abs(corrUncDo)
    elif abs(corrUncDo)<0.5*abs(corrUncUp):
        var, emRawUnc, sfRawUnc, corrUnc = 'Do', abs(emRawUncDo), abs(sfRawUncDo), abs(corrUncUp)
    if var!='None':
        if emRawUnc>corrUnc and emRawUnc<2.*corrUnc and emRawUnc<2.*errThrs: return var
        if sfRawUnc>corrUnc and sfRawUnc<2.*corrUnc and sfRawUnc<2.*errThrs: return var
    return 'None'

def getSign(a):
    if a==0.: return 1.
    return a/abs(a)

if __name__ == '__main__':

    # Input parameters
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)

    parser.add_option('--year'          , dest='year'          , help='Year(s) to be processed'             , default='all')
    parser.add_option('--tag'           , dest='tag'           , help='Tag used for the tag file name'      , default='Test')
    parser.add_option('--sigset'        , dest='sigset'        , help='Samples'                             , default='Backgrounds')
    parser.add_option('--fileset'       , dest='fileset'       , help='Fileset'                             , default='SM')
    parser.add_option('--verbose'       , dest='verbose'       , help='Activate print for debugging'        , default=False, action='store_true')
    parser.add_option('--binmet'        , dest='binmet'        , help='pTmiss bin'                          , default='all')
    parser.add_option('--binjet'        , dest='binjet'        , help='Jet bin'                             , default='all')
    parser.add_option('--binflv'        , dest='binflv'        , help='Channel'                             , default='all')
    parser.add_option('--source'        , dest='source'        , help='Source'                              , default='all')
    parser.add_option('--mergeoff'      , dest='mergeoff'      , help='Turn off merging'                    , default=False, action='store_true')
    parser.add_option('--fixsignoff'    , dest='fixsignoff'    , help='Turn off sign fixing'                , default=False, action='store_true')
    parser.add_option('--fixspikesoff'  , dest='fixspikesoff'  , help='Turn off spikes fixing'              , default=False, action='store_true')
    parser.add_option('--smoothoff'     , dest='smoothoff'     , help='Turn off smoothing'                  , default=False, action='store_true')
    parser.add_option('--consistenoff'  , dest='consistenoff'  , help='Turn off consistency check'          , default=False, action='store_true')
    parser.add_option('--corroff'       , dest='corroff'       , help='Turn off corrections'                , default=False, action='store_true')
    parser.add_option('--keepdyin'      , dest='keepdy'        , help='Keep DY in evaluation'               , default=False, action='store_true')
    (opt, args) = parser.parse_args()

    if opt.corroff:
        opt.mergeoff = True
        opt.fixsignoff = True
        opt.fixspikesoff = True
        opt.smoothoff = True
        opt.consistenoff = True

    if opt.year=='run2split': opt.year = '2016HIPM-2016noHIPM-2017-2018'

    yearlist = opt.year.split('-')

    tag = opt.tag
    opt.tag = yearlist[0]+tag

    debug = opt.binmet!='all' or opt.binjet!='all' or opt.binflv!='all' or opt.source!='all'

    samples = { }
    exec(open('samples_nanoAODv9.py').read())

    for year in yearlist:
        
        inputFileName = './Shapes/'+year+'/'+tag+'/'+'plots_'+tag+'_'+opt.fileset+'.root'
        inputFile     = ROOT.TFile(inputFileName.replace('Merge',''), 'READ') 
        outputFileName = inputFileName.replace('VetoesUL','SmtEUVetoesUL')
        if outputFileName==inputFileName or 'SmtEU' not in outputFileName: 
            print 'Wrong output file name'
            exit()
        if not debug:
            os.system('mkdir -p '+outputFileName.split('/plots_')[0]+' ; cp '+inputFileName+' '+outputFileName)
            outputFile    = ROOT.TFile(outputFileName, 'update')

        for binmet in [ 'SR1', 'SR2', 'SR3', 'SR4' ]:
            if opt.binmet!='all' and binmet!=opt.binmet: continue
            mt2Dir = 'mt2ll' if 'Merge' not in tag else 'mt2ll'+binmet
            for binjet in [ 'NoJet', 'NoTag', 'Veto', 'Tag' ]:
                if opt.binjet!='all' and binjet!=opt.binjet: continue
                if 'Stop' in tag and 'No' in binjet: continue
                if ('Chargino' in tag or 'TChipmWW' in tag) and 'No' in binjet and binmet in ['SR3', 'SR4']: continue
                if ('Chargino' in tag or 'TChipmWW' in tag) and binjet=='Veto' and binmet in ['SR1', 'SR2']: continue

                for source in [ 'jesTotal', 'jer', 'unclustEn' ]:
                    if opt.source!='all' and source!=opt.source: continue

                    keepDY = True if (source=='jesTotal' or opt.keepdy) else False

                    if opt.verbose or debug: print binmet, binjet, source
                    sampleShape, sampleShpUp, sampleShpDo = [], [], []
                    dyShape, dyShpUp, dyShpDo = [], [], []
                    gotFirst = [ False, False, False, False, False ]
                    gotDYFrs = [ False, False, False, False, False ]

                    #for binflv in [ 'em', 'sf' ]:
                        #if opt.binflv!='all' and binflv!=opt.binflv: continue

                    #    if not debug:
                    #        shapeDir = '_'.join([binmet,binjet,binflv])+'/'+mt2Dir
                            #outputFile.cd(shapeDir)

                    for metbin in [ 'SR1', 'SR2', 'SR3', 'SR4' ]:
                        for jetbin in [ 'NoJet', 'NoTag', 'Veto', 'Tag' ]: 
                            if 'Stop' in tag and 'No' in jetbin: continue
                            if ('Chargino' in tag or 'TChipmWW' in tag) and 'No' in jetbin and metbin in ['SR3', 'SR4']: continue
                            if ('Chargino' in tag or 'TChipmWW' in tag) and jetbin=='Veto' and metbin in ['SR1', 'SR2']: continue
                            for channel in [ 'em', 'sf' ]:

                                for nshp in range(5):

                                    resetHisto = False
                                    if nshp==1 and metbin!=binmet: resetHisto = True
                                    if nshp==2 and jetbin!=binjet:
                                        if binjet=='Tag' or jetbin=='Tag' or binjet=='NoJet' or (binjet=='NoTag' and jetbin=='NoJet'): 
                                            resetHisto = True
                                    if nshp==3 and (metbin!=binmet or jetbin!=binjet or channel!='em'): resetHisto = True
                                    if nshp==4 and (metbin!=binmet or jetbin!=binjet or channel!='sf'): resetHisto = True
                                    for sample in samples:

                                        shapeName = '_'.join([metbin,jetbin,channel])+'/mt2ll/histo_'+sample
                                        tempShape = inputFile.Get(shapeName);                            tempShape.SetDirectory(0)
                                        tempShpUp = inputFile.Get(shapeName+'_'+source+'_'+year+'Up');   tempShpUp.SetDirectory(0)
                                        tempShpDo = inputFile.Get(shapeName+'_'+source+'_'+year+'Down'); tempShpDo.SetDirectory(0)
                                        if resetHisto:
                                            tempShape.Reset()
                                            tempShpUp.Reset()
                                            tempShpDo.Reset()

                                        if not keepDY and sample=='DY': 
                                             
                                            if not gotDYFrs[nshp]:
                                                dyShape.append(tempShape)
                                                dyShpUp.append(tempShpUp)
                                                dyShpDo.append(tempShpDo)
                                                dyShape[nshp].SetDirectory(0)
                                                dyShpUp[nshp].SetDirectory(0)
                                                dyShpDo[nshp].SetDirectory(0)
                                                gotDYFrs[nshp] = True
                                            else:
                                                dyShape[nshp].Add(tempShape)
                                                dyShpUp[nshp].Add(tempShpUp)
                                                dyShpDo[nshp].Add(tempShpDo)

                                        else:

                                            if sample=='DY' and source!='jesTotal':
                                                if tempShape.GetEntries()!=0.:
                                                    avgWgt = tempShape.Integral()/tempShape.GetEntries()
                                                    for ib in range(1, tempShape.GetNbinsX()+1):
                                                        if tempShape.GetBinContent(ib)==0. and tempShpUp.GetBinContent(ib)!=0.:
                                                            sign = getSign(tempShpUp.GetBinContent(ib))
                                                            effN = 1./pow(tempShpUp.GetBinError(ib)/tempShpUp.GetBinContent(ib),2)
                                                            tempShpUp.SetBinContent(ib, sign*avgWgt*effN)
                                                        if tempShape.GetBinContent(ib)==0. and tempShpDo.GetBinContent(ib)!=0.:
                                                            sign = getSign(tempShpDo.GetBinContent(ib))
                                                            effN = 1./pow(tempShpDo.GetBinError(ib)/tempShpDo.GetBinContent(ib),2)
                                                            tempShpDo.SetBinContent(ib, sign*avgWgt*effN)
           
                                            if not gotFirst[nshp]:
                                                sampleShape.append(tempShape)
                                                sampleShpUp.append(tempShpUp)
                                                sampleShpDo.append(tempShpDo)
                                                sampleShape[nshp].SetDirectory(0)
                                                sampleShpUp[nshp].SetDirectory(0)
                                                sampleShpDo[nshp].SetDirectory(0)
                                                gotFirst[nshp] = True
                                            else:
                                                sampleShape[nshp].Add(tempShape)
                                                sampleShpUp[nshp].Add(tempShpUp)
                                                sampleShpDo[nshp].Add(tempShpDo)

                    if not gotFirst[0] or not gotFirst[1] or not gotFirst[2] or not gotFirst[3] or not gotFirst[4]:
                        print 'missing shapes'

                    else:
                            
                        if opt.verbose:
                            print '   Raw number of events'
                            for ib in range(1, sampleShape[3].GetNbinsX()+1):
                                print '      ', ib, sampleShape[0].GetBinContent(ib), sampleShape[1].GetBinContent(ib), sampleShape[2].GetBinContent(ib), sampleShape[3].GetBinContent(ib)
                        LastBin = sampleShape[3].GetNbinsX()
                        if 'Merge' in tag:
                            if binmet=='SR1': LastBin = 7
                            elif binmet!='SR4': LastBin = 8
                        if LastBin<sampleShape[3].GetNbinsX():
                            for nshp in range(5):
                                sampleShape[nshp] = mergeBins(sampleShape[nshp], LastBin, sampleShape[nshp].GetNbinsX())
                                sampleShpUp[nshp] = mergeBins(sampleShpUp[nshp], LastBin, sampleShpUp[nshp].GetNbinsX())
                                sampleShpDo[nshp] = mergeBins(sampleShpDo[nshp], LastBin, sampleShpDo[nshp].GetNbinsX())
                                if not keepDY:
                                    dyShape[nshp] = mergeBins(dyShape[nshp], LastBin, dyShape[nshp].GetNbinsX())
                                    dyShpUp[nshp] = mergeBins(dyShpUp[nshp], LastBin, dyShpUp[nshp].GetNbinsX())
                                    dyShpDo[nshp] = mergeBins(dyShpDo[nshp], LastBin, dyShpDo[nshp].GetNbinsX())
                        if not opt.mergeoff: 
                            keepSix = True
                            if 'Stop' in opt.tag and opt.year=='2018' and binmet=='SR4' and source=='jesTotal':
                                keepSix = False
                                print '   ---> Allow to merge bin 6 for', binmet, binjet, source
                            sampleShape, sampleShpUp, sampleShpDo, LastBinAfterMerging = mergeShapeBins(sampleShape, sampleShpUp, sampleShpDo, LastBin, keepSix)
                        for nshp in range(5):
                            sampleShpUp[nshp].Add(sampleShape[nshp],-1)
                            sampleShpUp[nshp].Divide(sampleShape[nshp]) 
                            sampleShpUp[nshp].Scale(100.)
                            sampleShpDo[nshp].Add(sampleShape[nshp],-1)
                            sampleShpDo[nshp].Divide(sampleShape[nshp])
                            sampleShpDo[nshp].Scale(100.)
                            if not keepDY and nshp<3:
                                dyShpUp[nshp].Add(dyShape[nshp],-1)
                                dyShpUp[nshp].Divide(dyShape[nshp])
                                dyShpUp[nshp].Scale(100.)
                                dyShpDo[nshp].Add(dyShape[nshp],-1)
                                dyShpDo[nshp].Divide(dyShape[nshp])
                                dyShpDo[nshp].Scale(100.)

                        if opt.verbose:
                            print '   Up uncertainties in sideband regions'
                            for ib in range(1, LastBin+1):
                                print '      ', ib, sampleShpUp[0].GetBinContent(ib), 100.*sampleShape[0].GetBinError(ib)/sampleShape[0].GetBinContent(ib), '   ', sampleShpUp[1].GetBinContent(ib), 100.*sampleShape[1].GetBinError(ib)/sampleShape[1].GetBinContent(ib), '   ', sampleShpUp[2].GetBinContent(ib), 100.*sampleShape[2].GetBinError(ib)/sampleShape[2].GetBinContent(ib)
                            print '   Down uncertainties in sideband regions'
                            for ib in range(1, LastBin+1):
                                print '      ', ib, sampleShpDo[0].GetBinContent(ib), 100.*sampleShape[0].GetBinError(ib)/sampleShape[0].GetBinContent(ib), '   ', sampleShpDo[1].GetBinContent(ib), 100.*sampleShape[1].GetBinError(ib)/sampleShape[1].GetBinContent(ib), '   ', sampleShpDo[2].GetBinContent(ib), 100.*sampleShape[2].GetBinError(ib)/sampleShape[2].GetBinContent(ib)

                        sampleShpUp[1].Multiply(sampleShpUp[2])
                        sampleShpUp[1].Divide(sampleShpUp[0])
                        sampleShpDo[1].Multiply(sampleShpDo[2])
                        sampleShpDo[1].Divide(sampleShpDo[0])
                        if not keepDY:
                            dyShpUp[1].Multiply(dyShpUp[2])
                            dyShpUp[1].Divide(dyShpUp[0])
                            dyShpDo[1].Multiply(dyShpDo[2])
                            dyShpDo[1].Divide(dyShpDo[0])

                        if not opt.fixsignoff:
                            for ib in range(1, LastBinAfterMerging+1):
                                if sampleShpUp[1].GetBinContent(ib)<0. or sampleShpDo[1].GetBinContent(ib)>0.:
                                    keepIt = False
                                    if sampleShpUp[1].GetBinContent(ib)<-1. or sampleShpDo[1].GetBinContent(ib)>1.:
                                        if sampleShpUp[1].GetBinContent(ib)<0. and sampleShpDo[1].GetBinContent(ib)>0.:
                                            if sampleShpUp[2].GetBinContent(ib)<0. and sampleShpDo[2].GetBinContent(ib)>0.: 
                                                if sampleShpUp[0].GetBinContent(ib)<0. and sampleShpDo[0].GetBinContent(ib)>0.: keepIt = True
                                                elif sampleShpUp[3].GetBinContent(ib)<0. and sampleShpDo[3].GetBinContent(ib)>0. and sampleShpUp[4].GetBinContent(ib)<0. and sampleShpDo[4].GetBinContent(ib)>0.: keepIt = True
                                                else:
                                                    if ib>1 and sampleShpUp[1].GetBinContent(ib-1)<0. and sampleShpDo[1].GetBinContent(ib-1)>0.: keepIt = True
                                                    if ib<LastBinAfterMerging and sampleShpUp[1].GetBinContent(ib+1)<0. and sampleShpDo[1].GetBinContent(ib+1)>0.: keepIt = True
                                        elif sampleShpUp[2].GetBinContent(ib)<0. and sampleShpDo[2].GetBinContent(ib)>0.:
                                            if sampleShpUp[3].GetBinContent(ib)<0. and sampleShpDo[3].GetBinContent(ib)>0. and sampleShpUp[4].GetBinContent(ib)<0. and sampleShpDo[4].GetBinContent(ib)>0.:
                                                if sampleShpUp[1].GetBinContent(ib)>0. and abs(sampleShpUp[0].GetBinContent(ib))<1.:
                                                    sampleShpUp[1].SetBinContent(ib, -sampleShpUp[1].GetBinContent(ib))
                                                    keepIt = True
                                                elif sampleShpDo[1].GetBinContent(ib)<0. and abs(sampleShpDo[0].GetBinContent(ib))<1.:
                                                    sampleShpDo[1].SetBinContent(ib, -sampleShpDo[1].GetBinContent(ib))
                                                    keepIt = True
                                    if not keepIt:
                                       if sampleShpUp[1].GetBinContent(ib)<0.: sampleShpUp[1].SetBinContent(ib, -sampleShpUp[1].GetBinContent(ib))
                                       if sampleShpDo[1].GetBinContent(ib)>0.: sampleShpDo[1].SetBinContent(ib, -sampleShpDo[1].GetBinContent(ib))

                        if not opt.fixspikesoff:
                            shp1UncLimit = 40.
                            #if 'Stop' in opt.tag and opt.year=='2018' and binmet=='SR4' and source=='jesTotal':
                            #    print '   ---> Ad hoc spike limit for', binmet, binjet, source
                            #    shp1UncLimit = 35.
                            for ib in range(1, LastBinAfterMerging+1):
                                upOK, doOK = True, True
                                if sampleShpUp[1].GetBinError(ib)>shp1UncLimit:
                                    if sampleShpDo[1].GetBinError(ib)<40. and abs(sampleShpUp[1].GetBinContent(ib))<abs(sampleShpDo[1].GetBinContent(ib)):
                                        #print '   ---> New spike strategy for', binmet, binjet, ib, source, 'Up'
                                        pass
                                    elif abs(sampleShape[2].GetBinError(ib)/sampleShape[2].GetBinContent(ib))<0.05: 
                                        fixC = abs(sampleShpUp[2].GetBinContent(ib))*getSign(sampleShpUp[1].GetBinContent(ib))
                                        sampleShpUp[1].SetBinContent(ib, fixC )
                                    elif sampleShpDo[1].GetBinError(ib)<shp1UncLimit:
                                        sampleShpUp[1].SetBinContent(ib, -sampleShpDo[1].GetBinContent(ib))
                                    else: 
                                        #print '   ---> No  spike strategy for', binmet, binjet, ib, source, 'Up'
                                        upOK = False
                                if sampleShpDo[1].GetBinError(ib)>shp1UncLimit:
                                    if sampleShpUp[1].GetBinError(ib)<40. and abs(sampleShpDo[1].GetBinContent(ib))<abs(sampleShpUp[1].GetBinContent(ib)):
                                        #print '   ---> New spike strategy for', binmet, binjet, ib, source, 'Down'
                                        pass
                                    elif abs(sampleShape[2].GetBinError(ib)/sampleShape[2].GetBinContent(ib))<0.05:
                                        fixC = abs(sampleShpDo[2].GetBinContent(ib))*getSign(sampleShpDo[1].GetBinContent(ib))   
                                        sampleShpDo[1].SetBinContent(ib, fixC )
                                    elif sampleShpUp[1].GetBinError(ib)<shp1UncLimit:
                                        sampleShpDo[1].SetBinContent(ib, -sampleShpUp[1].GetBinContent(ib))
                                    else: 
                                        #print '   ---> No  spike strategy for', binmet, binjet, ib, source, 'Down'
                                        doOK = False
                                if not upOK or not doOK:
                                    if upOK: sampleShpDo[1].SetBinContent(ib, -sampleShpUp[1].GetBinContent(ib))
                                    elif doOK: sampleShpUp[1].SetBinContent(ib, -sampleShpDo[1].GetBinContent(ib))
                                    elif ib>1:
                                        upFix, doFix = 0., 0.
                                        if abs(sampleShpUp[2].GetBinContent(ib)/sampleShpUp[2].GetBinContent(ib-1))<100.:
                                            upFix = abs(sampleShpUp[1].GetBinContent(ib-1)*sampleShpUp[2].GetBinContent(ib)/sampleShpUp[2].GetBinContent(ib-1)) 
                                        else: print '      ---> huge up spike translation', abs(sampleShpUp[2].GetBinContent(ib)/sampleShpUp[2].GetBinContent(ib-1)), binmet, binjet, ib, source, 'Up'
                                        if abs(sampleShpDo[2].GetBinContent(ib)/sampleShpDo[2].GetBinContent(ib-1))<100.:
                                            doFix = abs(sampleShpDo[1].GetBinContent(ib-1)*sampleShpDo[2].GetBinContent(ib)/sampleShpDo[2].GetBinContent(ib-1))
                                        else: print '      ---> huge up spike translation', abs(sampleShpDo[2].GetBinContent(ib)/sampleShpDo[2].GetBinContent(ib-1)), binmet, binjet, ib, source, 'Down'
                                        if upFix!=0. or doFix!=0.:
                                            uncTrn = max(upFix, doFix)
                                            uncRaw = max(abs(sampleShpUp[3].GetBinContent(ib)), abs(sampleShpDo[3].GetBinContent(ib)), abs(sampleShpUp[4].GetBinContent(ib)), abs(sampleShpUp[4].GetBinContent(ib)))
                                            uncFix = min(uncTrn,uncRaw)
                                            sampleShpUp[1].SetBinContent(ib, uncFix*getSign(sampleShpUp[1].GetBinContent(ib)))
                                            sampleShpDo[1].SetBinContent(ib, uncFix*getSign(sampleShpDo[1].GetBinContent(ib)))
                                        else: print '      ---> Still there!'
                                        #print '   ---> New spike strategy for', binmet, binjet, ib, source
                                    else: print '      ---> Still there!'
  
                        if not opt.consistenoff:
                            for ib in range(1, LastBinAfterMerging+1):
                                if sampleShape[1].GetBinContent(ib)!=0.:
 
                                    emStat = 100.*sampleShape[3].GetBinError(ib)/sampleShape[3].GetBinContent(ib) 
                                    sfStat = 100.*sampleShape[4].GetBinError(ib)/sampleShape[4].GetBinContent(ib)
                                    useResult, rawUnc = applyResult(sampleShpUp[1].GetBinContent(ib), sampleShpUp[3].GetBinContent(ib), sampleShpUp[4].GetBinContent(ib), sampleShpDo[1].GetBinContent(ib), sampleShpDo[3].GetBinContent(ib), sampleShpDo[4].GetBinContent(ib), emStat, sfStat)
                                    if not useResult: sampleShpUp[1].SetBinContent(ib, rawUnc)
                                    useResult, rawUnc = applyResult(sampleShpDo[1].GetBinContent(ib), sampleShpDo[3].GetBinContent(ib), sampleShpDo[4].GetBinContent(ib), sampleShpUp[1].GetBinContent(ib), sampleShpUp[3].GetBinContent(ib), sampleShpUp[4].GetBinContent(ib), emStat, sfStat)
                                    if not useResult: sampleShpDo[1].SetBinContent(ib, rawUnc)
                                    setConsisten = setConsistency(sampleShpUp[1].GetBinContent(ib), sampleShpUp[3].GetBinContent(ib), sampleShpUp[4].GetBinContent(ib), sampleShpDo[1].GetBinContent(ib), sampleShpDo[3].GetBinContent(ib), sampleShpDo[4].GetBinContent(ib))
                                    if setConsisten=='Up': sampleShpUp[1].SetBinContent(ib, -sampleShpDo[1].GetBinContent(ib))
                                    if setConsisten=='Do': sampleShpDo[1].SetBinContent(ib, -sampleShpUp[1].GetBinContent(ib)) 

                        if not opt.smoothoff:
                            for ib in range(2, LastBinAfterMerging):
                                if getSign(sampleShpUp[1].GetBinContent(ib))==getSign(sampleShpUp[1].GetBinContent(ib-1)):
                                    if getSign(sampleShpUp[1].GetBinContent(ib))==getSign(sampleShpUp[1].GetBinContent(ib+1)):
                                        minC = min(abs(sampleShpUp[1].GetBinContent(ib-1)),abs(sampleShpUp[1].GetBinContent(ib+1)))
                                        maxC = max(abs(sampleShpUp[1].GetBinContent(ib-1)),abs(sampleShpUp[1].GetBinContent(ib+1)))
                                        if abs(sampleShpUp[1].GetBinContent(ib))<0.75*minC and abs(sampleShpUp[1].GetBinContent(ib))<0.50*maxC:
                                            meanC = (sampleShpUp[1].GetBinContent(ib-1)+sampleShpUp[1].GetBinContent(ib+1))/2.
                                            sampleShpUp[1].SetBinContent(ib, meanC)
                                if getSign(sampleShpDo[1].GetBinContent(ib))==getSign(sampleShpDo[1].GetBinContent(ib-1)):
                                    if getSign(sampleShpDo[1].GetBinContent(ib))==getSign(sampleShpDo[1].GetBinContent(ib+1)):
                                        minC = min(abs(sampleShpDo[1].GetBinContent(ib-1)),abs(sampleShpDo[1].GetBinContent(ib+1)))
                                        maxC = max(abs(sampleShpDo[1].GetBinContent(ib-1)),abs(sampleShpDo[1].GetBinContent(ib+1)))
                                        if abs(sampleShpDo[1].GetBinContent(ib))<0.75*minC and abs(sampleShpDo[1].GetBinContent(ib))<0.50*maxC:
                                            meanC = (sampleShpDo[1].GetBinContent(ib-1)+sampleShpDo[1].GetBinContent(ib+1))/2.
                                            sampleShpDo[1].SetBinContent(ib, meanC)

                        if LastBin>LastBinAfterMerging:
                            for ib in range(LastBinAfterMerging+1, LastBin+1): 
                                sampleShpUp[1].SetBinContent(ib, sampleShpUp[1].GetBinContent(LastBinAfterMerging))
                                sampleShpDo[1].SetBinContent(ib, sampleShpDo[1].GetBinContent(LastBinAfterMerging))

                        for binflv in [ 'em', 'sf' ]:
                            if opt.binflv!='all' and binflv!=opt.binflv: continue

                            if not debug:
                                shapeDir = '_'.join([binmet,binjet,binflv])+'/'+mt2Dir
                                outputFile.cd(shapeDir)


                            if opt.verbose or debug:
                                print '   Final predictions', binflv
                                orig = 3 if binflv=='em' else 4 
                                for ib in range(1, LastBin+1):
                                    if sampleShape[orig].GetBinContent(ib)!=0.:
                                        print '      ', ib,  sampleShpUp[orig].GetBinContent(ib), sampleShpUp[1].GetBinContent(ib), sampleShpUp[1].GetBinError(ib), '            ', sampleShpDo[orig].GetBinContent(ib), sampleShpDo[1].GetBinContent(ib), sampleShpDo[1].GetBinError(ib), '            ', 100.*sampleShape[orig].GetBinError(ib)/sampleShape[orig].GetBinContent(ib) 

                            
                            if not keepDY:
                                orig = 3 if binflv=='em' else 4        
                                if binflv=='sf':

                                    if opt.verbose:
                                        for ib in range(1, LastBin+1):
                                            if dyShape[orig].GetBinContent(ib)==0. and (dyShpUp[orig].GetBinContent(ib)!=0. or dyShpDo[orig].GetBinContent(ib)!=0.):
                                                print '   ---> DY1: ', ib, binmet, binjet, source, dyShape[orig].GetBinContent(ib),'+/-',dyShape[orig].GetBinError(ib), dyShpUp[orig].GetBinContent(ib),'+/-',dyShpUp[orig].GetBinError(ib), dyShpDo[orig].GetBinContent(ib),'+/-',dyShpDo[orig].GetBinError(ib)
                                                print '            ', ib, dyShape[orig].GetBinContent(ib),'+/-',dyShape[orig].GetBinError(ib), dyShpUp[orig].GetBinContent(ib),'+/-',dyShpUp[orig].GetBinError(ib), dyShpDo[orig].GetBinContent(ib),'+/-',dyShpDo[orig].GetBinError(ib)
                                                print '            ', ib, dyShape[1].GetBinContent(ib), dyShape[0].GetBinContent(ib), dyShape[2].GetBinContent(ib)
                                                print '            ', ib, dyShape[orig].GetEntries(), dyShape[orig].Integral(), dyShape[orig].Integral()/dyShape[orig].GetEntries()
                                                if dyShpUp[orig].GetBinContent(ib)!=0.:
                                                    dyShpUp[orig].SetBinContent(ib,(dyShape[orig].Integral()/dyShape[orig].GetEntries())/pow(dyShpUp[orig].GetBinError(ib)/dyShpUp[orig].GetBinContent(ib),2))
                                                if dyShpDo[orig].GetBinContent(ib)!=0.:
                                                    dyShpDo[orig].SetBinContent(ib,(dyShape[orig].Integral()/dyShape[orig].GetEntries())/pow(dyShpDo[orig].GetBinError(ib)/dyShpDo[orig].GetBinContent(ib),2))
                                            if dyShape[orig].GetBinContent(ib)!=0.: 
                                                if  abs(dyShape[orig].GetBinError(ib)/dyShape[orig].GetBinContent(ib))>0.1:
                                                    print '   ---> DY2: ', ib, binmet, binjet, source, dyShape[orig].GetBinContent(ib),'+/-',dyShape[orig].GetBinError(ib), dyShpUp[orig].GetBinContent(ib),'+/-',dyShpUp[orig].GetBinError(ib), dyShpDo[orig].GetBinContent(ib),'+/-',dyShpDo[orig].GetBinError(ib)
                                                    if dyShpUp[orig].GetBinError(ib)!=0. and dyShpDo[orig].GetBinError(ib)!=0.: print '             ', ib, binmet, binjet, source, (dyShpUp[orig].GetBinContent(ib)-dyShape[orig].GetBinContent(ib))/dyShpUp[orig].GetBinError(ib), ' ', (dyShpDo[orig].GetBinContent(ib)-dyShape[orig].GetBinContent(ib))/dyShpDo[orig].GetBinError(ib) 
                                                if dyShape[orig].GetBinError(ib)==dyShape[orig].GetBinContent(ib) and dyShape[orig].GetBinContent(ib)<0.05:
                                                    dyShpUp[orig].SetBinContent(ib, dyShape[orig].GetBinContent(ib)); dyShpDo[orig].SetBinContent(ib, dyShape[orig].GetBinContent(ib))
                                if opt.verbose: 
                                    print '      DY'
                                    for ib in range(1, LastBin+1):
                                        print '      ', ib, dyShape[orig].GetBinContent(ib), dyShpUp[orig].GetBinContent(ib)-dyShape[orig].GetBinContent(ib), dyShpDo[orig].GetBinContent(ib)-dyShape[orig].GetBinContent(ib)
                                    for ib in range(1, LastBin+1):
                                        print '      ', ib, 'Up', 100.*((dyShpUp[orig].GetBinContent(ib)-dyShape[orig].GetBinContent(ib)+0.01*sampleShpUp[orig].GetBinContent(ib)*sampleShape[orig].GetBinContent(ib))/(sampleShape[orig].GetBinContent(ib)+dyShape[orig].GetBinContent(ib))), 100.*((dyShpUp[orig].GetBinContent(ib)-dyShape[orig].GetBinContent(ib)+0.01*sampleShpUp[1].GetBinContent(ib)*sampleShape[orig].GetBinContent(ib))/(sampleShape[orig].GetBinContent(ib)+dyShape[orig].GetBinContent(ib))), 100.*((0.01*dyShpUp[1].GetBinContent(ib)*dyShape[orig].GetBinContent(ib)+0.01*sampleShpUp[1].GetBinContent(ib)*sampleShape[orig].GetBinContent(ib))/(sampleShape[orig].GetBinContent(ib)+dyShape[orig].GetBinContent(ib))), 100.*((0.01*dyShpUp[2].GetBinContent(ib)*dyShape[orig].GetBinContent(ib)+0.01*sampleShpUp[1].GetBinContent(ib)*sampleShape[orig].GetBinContent(ib))/(sampleShape[orig].GetBinContent(ib)+dyShape[orig].GetBinContent(ib))), 't',sampleShape[orig].GetBinContent(ib)+dyShape[orig].GetBinContent(ib)
                                        print '         Do', 100.*((dyShpDo[orig].GetBinContent(ib)-dyShape[orig].GetBinContent(ib)+0.01*sampleShpDo[orig].GetBinContent(ib)*sampleShape[orig].GetBinContent(ib))/(sampleShape[orig].GetBinContent(ib)+dyShape[orig].GetBinContent(ib))), 100.*((dyShpDo[orig].GetBinContent(ib)-dyShape[orig].GetBinContent(ib)+0.01*sampleShpDo[1].GetBinContent(ib)*sampleShape[orig].GetBinContent(ib))/(sampleShape[orig].GetBinContent(ib)+dyShape[orig].GetBinContent(ib))), 100.*((0.01*dyShpDo[1].GetBinContent(ib)*dyShape[orig].GetBinContent(ib)+0.01*sampleShpDo[1].GetBinContent(ib)*sampleShape[orig].GetBinContent(ib))/(sampleShape[orig].GetBinContent(ib)+dyShape[orig].GetBinContent(ib))), 100.*((0.01*dyShpDo[2].GetBinContent(ib)*dyShape[orig].GetBinContent(ib)+0.01*sampleShpDo[1].GetBinContent(ib)*sampleShape[orig].GetBinContent(ib))/(sampleShape[orig].GetBinContent(ib)+dyShape[orig].GetBinContent(ib)))

                                avgWgt = dyShape[orig].Integral()/dyShape[orig].GetEntries()
                                for ib in range(1, LastBin+1):
                                    effNUp, effNDo = 0., 0.
                                    if dyShpUp[orig].GetBinContent(ib)!=0. and dyShpUp[orig].GetBinError(ib)!=0.: effNUp = 1./pow(dyShpUp[orig].GetBinError(ib)/dyShpUp[orig].GetBinContent(ib),2)
                                    if dyShpDo[orig].GetBinContent(ib)!=0. and dyShpDo[orig].GetBinError(ib)!=0.: effNDo = 1./pow(dyShpDo[orig].GetBinError(ib)/dyShpDo[orig].GetBinContent(ib),2)
                                    if dyShape[orig].GetBinContent(ib)==0. and dyShpUp[orig].GetBinContent(ib)!=0.:
                                        sign = getSign(dyShpUp[orig].GetBinContent(ib))
                                        dyShpUp[orig].SetBinContent(ib, sign*avgWgt*effNUp)
                                    else:
                                        #dyShpUp[orig].SetBinContent(ib, 0.01*dyShpUp[1].GetBinContent(ib)*dyShape[orig].GetBinContent(ib))
                                        dyShpUp[orig].SetBinContent(ib, dyShpUp[orig].GetBinContent(ib)-dyShape[orig].GetBinContent(ib))
                                    if dyShape[orig].GetBinContent(ib)==0. and dyShpDo[orig].GetBinContent(ib)!=0.:
                                        sign = getSign(dyShpDo[orig].GetBinContent(ib))
                                        dyShpDo[orig].SetBinContent(ib, sign*avgWgt*effNDo)
                                    else:
                                        #dyShpDo[orig].SetBinContent(ib, 0.01*dyShpDo[1].GetBinContent(ib)*dyShape[orig].GetBinContent(ib)) 
                                        dyShpDo[orig].SetBinContent(ib, dyShpDo[orig].GetBinContent(ib)-dyShape[orig].GetBinContent(ib))
                                    largeWeight = False
                                    if dyShpUp[orig].GetBinContent(ib)!=0. and dyShpDo[orig].GetBinContent(ib)!=0.:
                                        if effNUp<effNDo and 2.*math.sqrt(effNUp)<(effNDo-effNUp):
                                            largeWeight = True
                                            dyShpUp[orig].SetBinContent(ib, -dyShpDo[orig].GetBinContent(ib))
                                        elif effNDo<effNUp and 2.*math.sqrt(effNDo)<(effNUp-effNDo):
                                            largeWeight = True
                                            dyShpDo[orig].SetBinContent(ib, -dyShpUp[orig].GetBinContent(ib))
                                    if dyShape[orig].GetBinContent(ib)!=0.:
                                        isLargeAss = False
                                        #if ib==8: print abs(dyShpUp[orig].GetBinContent(ib)/(dyShape[orig].GetBinContent(ib)+sampleShape[orig].GetBinContent(ib))), abs(dyShpUp[orig].GetBinContent(ib)/dyShpDo[orig].GetBinContent(ib))
                                        if abs(dyShpUp[orig].GetBinContent(ib)/(dyShape[orig].GetBinContent(ib)+sampleShape[orig].GetBinContent(ib)))>0.01 and dyShpDo[orig].GetBinContent(ib)!=0.:
                                            if abs(dyShpUp[orig].GetBinContent(ib)/dyShpDo[orig].GetBinContent(ib))>90. or abs(dyShpUp[orig].GetBinContent(ib)/(dyShape[orig].GetBinContent(ib)+sampleShape[orig].GetBinContent(ib)))>0.10: 
                                                isLargeAss = True
                                                #print '   ---> DY3', dyShpUp[orig].GetBinContent(ib)/dyShpDo[orig].GetBinContent(ib), abs(dyShpUp[orig].GetBinContent(ib)/dyShape[orig].GetBinContent(ib)), dyShpUp[orig].GetBinContent(ib), dyShpUp[orig].GetBinContent(ib)/(dyShape[orig].GetBinContent(ib)+sampleShape[orig].GetBinContent(ib)), binmet, binjet, source, ib
                                        if abs(dyShpDo[orig].GetBinContent(ib)/(dyShape[orig].GetBinContent(ib)+sampleShape[orig].GetBinContent(ib)))>0.01 and dyShpUp[orig].GetBinContent(ib)!=0.:
                                            if abs(dyShpDo[orig].GetBinContent(ib)/dyShpUp[orig].GetBinContent(ib))>90. or abs(dyShpDo[orig].GetBinContent(ib)/(dyShape[orig].GetBinContent(ib)+sampleShape[orig].GetBinContent(ib)))>0.10:
                                                isLargeAss = True
                                                #print '   ---> DY3', dyShpDo[orig].GetBinContent(ib)/dyShpUp[orig].GetBinContent(ib), abs(dyShpDo[orig].GetBinContent(ib)/dyShape[orig].GetBinContent(ib)), dyShpDo[orig].GetBinContent(ib), dyShpDo[orig].GetBinContent(ib)/(dyShape[orig].GetBinContent(ib)+sampleShape[orig].GetBinContent(ib)), binmet, binjet, source, ib
                                        if isLargeAss: 
                                            #print dyShpUp[1].GetBinError(ib), dyShpDo[1].GetBinError(ib)
                                            #print dyShpUp[1].GetBinContent(ib), dyShpDo[1].GetBinContent(ib)
                                            #print dyShpUp[2].GetBinContent(ib), dyShpDo[2].GetBinContent(ib)
                                            fixUp = dyShpUp[1].GetBinContent(ib) if (dyShpUp[1].GetBinError(ib)<20. or abs(dyShpUp[1].GetBinContent(ib))<5.) else 999.
                                            fixDo = dyShpDo[1].GetBinContent(ib) if (dyShpDo[1].GetBinError(ib)<20. or abs(dyShpDo[1].GetBinContent(ib))<5.) else 999.
                                            if fixUp!=999. or fixDo!=999.:
                                                if fixUp==999.:  
                                                    fixUp = -fixDo
                                                    if abs(dyShpUp[orig].GetBinContent(ib)/(dyShape[orig].GetBinContent(ib)+sampleShape[orig].GetBinContent(ib)))>0.10: 
                                                        fixUp *= 3.
                                                        #print '   ---> DY4', fixUp
                                                if fixDo==999.:  
                                                    fixDo = -fixUp
                                                    if abs(dyShpDo[orig].GetBinContent(ib)/(dyShape[orig].GetBinContent(ib)+sampleShape[orig].GetBinContent(ib)))>0.10: 
                                                        fixDo *= 3.  
                                                        #print '   ---> DY4', fixDo          
                                            else: 
                                                #print '    ---> DY3 failed'
                                                fixUp = dyShpUp[1].GetBinContent(ib) if abs(dyShpUp[1].GetBinContent(ib))<abs(dyShpDo[1].GetBinContent(ib)) else -dyShpDo[1].GetBinContent(ib)
                                                fixDo = -fixUp
                                            dyShpUp[orig].SetBinContent(ib, 0.01*fixUp*dyShape[orig].GetBinContent(ib))
                                            dyShpDo[orig].SetBinContent(ib, 0.01*fixDo*dyShape[orig].GetBinContent(ib))

                                        isDYInv = False
                                        if getSign(dyShpUp[orig].GetBinContent(ib))==getSign(dyShpDo[orig].GetBinContent(ib)):
                                            minUnc = min(abs(dyShpUp[orig].GetBinContent(ib)), abs(dyShpDo[orig].GetBinContent(ib)))
                                            if dyShpUp[orig].GetBinContent(ib)<0.: dyShpUp[orig].SetBinContent(ib,  1.*minUnc)
                                            if dyShpDo[orig].GetBinContent(ib)>0.: dyShpDo[orig].SetBinContent(ib, -1.*minUnc)
                                            isDYInv = True

                                        if opt.verbose and (isLargeAss or largeWeight or isDYInv):
                                            if isLargeAss: print '   ---> DY large assymetry'
                                            if largeWeight: print '   ---> DY large weight'
                                            if isDYInv: print '   ---> DY inverted'
                                            print '      ', ib, 'Up', sampleShpUp[1].GetBinContent(ib), 100.*((dyShpUp[orig].GetBinContent(ib)+0.01*sampleShpUp[1].GetBinContent(ib)*sampleShape[orig].GetBinContent(ib))/(sampleShape[orig].GetBinContent(ib)+dyShape[orig].GetBinContent(ib))), 100.*((0.01*dyShpUp[1].GetBinContent(ib)*dyShape[orig].GetBinContent(ib)+0.01*sampleShpUp[1].GetBinContent(ib)*sampleShape[orig].GetBinContent(ib))/(sampleShape[orig].GetBinContent(ib)+dyShape[orig].GetBinContent(ib))), 100.*((0.01*dyShpUp[2].GetBinContent(ib)*dyShape[orig].GetBinContent(ib)+0.01*sampleShpUp[1].GetBinContent(ib)*sampleShape[orig].GetBinContent(ib))/(sampleShape[orig].GetBinContent(ib)+dyShape[orig].GetBinContent(ib)))   
                                            print '         Do',      sampleShpDo[1].GetBinContent(ib), 100.*((dyShpDo[orig].GetBinContent(ib)+0.01*sampleShpDo[1].GetBinContent(ib)*sampleShape[orig].GetBinContent(ib))/(sampleShape[orig].GetBinContent(ib)+dyShape[orig].GetBinContent(ib))), 100.*((0.01*dyShpDo[1].GetBinContent(ib)*dyShape[orig].GetBinContent(ib)+0.01*sampleShpDo[1].GetBinContent(ib)*sampleShape[orig].GetBinContent(ib))/(sampleShape[orig].GetBinContent(ib)+dyShape[orig].GetBinContent(ib))), 100.*((0.01*dyShpDo[2].GetBinContent(ib)*dyShape[orig].GetBinContent(ib)+0.01*sampleShpDo[1].GetBinContent(ib)*sampleShape[orig].GetBinContent(ib))/(sampleShape[orig].GetBinContent(ib)+dyShape[orig].GetBinContent(ib)))

                            if not debug:
                                for sample in samples:
                                    for variation in [ 'Up', 'Down' ]:

                                        if not keepDY and sample=='DY':

                                            if binflv=='em':
                                                tempName = shapeDir+'/histo_'+sample+'_'+source+'_'+year+variation
                                                sampleTemp = outputFile.Get(tempName)
                                                sampleTemp.SetDirectory(0)

                                            else:
                                                tempName = shapeDir+'/histo_'+sample
                                                sampleTemp = outputFile.Get(tempName)
                                                sampleTemp.SetDirectory(0)
                                                for ib in range(1, LastBin+1):
                                                    dyUnc = dyShpUp[4].GetBinContent(ib) if variation=='Up' else dyShpDo[4].GetBinContent(ib)
                                                    bincon = sampleTemp.GetBinContent(ib)
                                                    sampleTemp.SetBinContent(ib, bincon+dyUnc)
                                                    
                                        else: 
                                            tempName = shapeDir+'/histo_'+sample
                                            sampleTemp = outputFile.Get(tempName)
                                            sampleTemp.SetDirectory(0)
                                            if sampleTemp.GetNbinsX()!=LastBin: print 'Wrong binning: input =', LastBin, ' output =', sampleTemp.GetNbinsX() 
                                            for ib in range(1, LastBin+1):
                                                corr = sampleShpUp[1].GetBinContent(ib) if variation=='Up' else sampleShpDo[1].GetBinContent(ib)
                                                bincon = sampleTemp.GetBinContent(ib)
                                                binerr = sampleTemp.GetBinError(ib)
                                                sampleTemp.SetBinContent(ib, bincon*(1.+corr/100.))
                                                sampleTemp.SetBinError(ib, binerr*(1.+corr/100.))

                                        sampleTemp.SetName('histo_'+sample+'_Smooth'+source+'_'+year+variation)
                                        sampleTemp.SetTitle('histo_'+sample+'_Smooth'+source+'_'+year+variation)
                                        sampleTemp.Write()
                                 
