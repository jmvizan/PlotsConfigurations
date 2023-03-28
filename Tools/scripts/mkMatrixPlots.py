#!/usr/bin/env python

import json
import sys
import ROOT
import optparse
import LatinoAnalysis.Gardener.hwwtools as hwwtools
import logging
import os
import math

def makeMatrixPlot(outputHisto, outputFile, regionsToRemove, legend):
        
    ROOT.gStyle.SetOptFit(0)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptTitle(0)
    ROOT.gStyle.SetPaintTextFormat('1.3f')
    ROOT.gStyle.SetPalette(1)

    canvas = ROOT.TCanvas('canvas', '', 550, 550)
    
    canvas.Divide(1, 1)
    canvas.SetFillColor(10)
    canvas.SetBorderMode(0)
    canvas.SetBorderSize(2)
    canvas.SetFrameFillColor(0)
    canvas.SetFrameFillStyle(0)
    canvas.SetFrameBorderMode(0)

    pad = canvas.GetPad(1)

    #pad.SetGridx()
    #pad.SetGridy()
    if 'Covariance' in outputHisto.GetName():
        pad.SetLogz()
    pad.SetLeftMargin(0.13);
    pad.SetRightMargin(0.13);
    pad.SetTopMargin(0.08);
    pad.SetBottomMargin(0.13);

    pad.cd()

    if 'Covariance' in outputHisto.GetName():
        outputHisto.SetMinimum(0.01);
    #outputHisto.SetMaximum(+1.);

    outputHisto.GetXaxis().SetLabelFont(42)
    outputHisto.GetXaxis().SetLabelSize(0.02)
    #outputHisto.GetXaxis().SetLabelOffset(1.)
    outputHisto.GetYaxis().SetLabelFont(42)
    outputHisto.GetYaxis().SetLabelSize(0.02)
    #outputHisto.GetYaxis().SetLabelOffset(1.)

    outputHisto.GetXaxis().SetTitle('')
    outputHisto.GetYaxis().SetTitle('')

    outputHisto.Draw('colz')

    scaleLeg = outputHisto.GetNbinsX()/(6.*7.*2.)

    T1 = ROOT.TLatex(scaleLeg*0.220, scaleLeg*86., 'CMS')
    T1.SetTextAlign(11)
    T1.SetTextFont(61)
    T1.SetTextSize(0.042)
    T1.Draw()

    T2 = ROOT.TLatex(scaleLeg*11., scaleLeg*86., 'Supplementary')
    T2.SetTextAlign(11)
    T2.SetTextFont(52)
    T2.SetTextSize(0.034)
    T2.Draw()
    T1.Draw()

    arXiv = '' #'arXiv'
    T4 = ROOT.TLatex(scaleLeg*62., scaleLeg*86., arXiv)
    T4.SetTextAlign(31)
    T4.SetTextFont(42)
    T4.SetTextSize(0.032)
    T4.Draw()

    #T3 = ROOT.TLatex(scaleLeg*84., scaleLeg*86., legend')
    T3 = ROOT.TLatex(scaleLeg*89., scaleLeg*86., legend)
    T3.SetTextAlign(31)
    T3.SetTextFont(42)
    T3.SetTextSize(0.032)
    T3.Draw()

    if regionsToRemove!='': outputFile += '_excl-'+regionsToRemove
    canvas.Print(outputFile+'.pdf')
    canvas.Print(outputFile+'.root')

def convertTitle(yTitle):
   
    #ptmissBin = [ '_SR1', '_SR2', '_SR3', '_SR4' ]
    #
    #for ptmb in ptmissBin :
    #    if ptmb in yTitle :
    #
    #        yTitle = yTitle.replace(ptmb, '')
    #        yTitle = ptmb.replace('_', '') + '_' + yTitle
    #
    #yTitle = yTitle.replace('_NoTag', '_jets')
    #yTitle = yTitle.replace('_Veto',  '_0tag')
    #yTitle = yTitle.replace('_Tag',   '_tags')
    #yTitle = yTitle.replace('_NoJet', '_0jet')
    #
    #yTitle = yTitle.replace('_sf', '_SF')
    #yTitle = yTitle.replace('_em', '_DF')

    return yTitle

def keepRegion(label, regionsToRemove):

    if regionsToRemove=='': return True

    for region in regionsToRemove.split(','):
        if region in label:
           return False

    return True

def makeHistoCopy(inputHisto, regionsToRemove='', fillContent=True):

    nBinsX = 0
    for xb in range(inputHisto.GetNbinsX()) :
        if keepRegion(inputHisto.GetXaxis().GetBinLabel(xb+1), regionsToRemove) :
            nBinsX += 1

    outputHisto = ROOT.TH2D('CovarianceMatrix', '', nBinsX, 0., nBinsX, nBinsX, 0., nBinsX)

    nBinsX = 0
    for xb in range(inputHisto.GetNbinsX()) :
        if keepRegion(inputHisto.GetXaxis().GetBinLabel(xb+1), regionsToRemove) :

            nBinsY = 0
            for yb in range(inputHisto.GetNbinsY()) :
                if keepRegion(inputHisto.GetYaxis().GetBinLabel(yb+1), regionsToRemove) :

                    if fillContent:
                        outputHisto.SetBinContent(nBinsX+1, nBinsY+1, inputHisto.GetBinContent(xb+1, yb+1))
                                                  
                    if nBinsX==0 :
                        outputHisto.GetYaxis().SetBinLabel(nBinsY+1, convertTitle(inputHisto.GetYaxis().GetBinLabel(yb+1)))

                    nBinsY += 1

            outputHisto.GetXaxis().SetBinLabel(nBinsX+1, convertTitle(inputHisto.GetXaxis().GetBinLabel(xb+1)))
            nBinsX += 1
                    
    return outputHisto

##Main body of the analysis
if __name__ == '__main__':

    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)

    parser.add_option('--verbose'        , dest='verbose'        , help='verbose'        , default=0                     , type='int'   )
    parser.add_option('--inputFile'      , dest='inputFile'      , help='inputFile'      , default='fitDiagnostics'      , type='string')
    parser.add_option('--postFit'        , dest='postFit'        , help='postFit'        , default='fit_b'               , type='string')
    parser.add_option('--covarianceHisto', dest='covarianceHisto', help='covarianceHisto', default='overall_total_covar' , type='string')
    parser.add_option('--saveCovariance' , dest='saveCovariance' , help='saveCovariance' , default=False           , action='store_true')
    parser.add_option('--regionsToRemove', dest='regionsToRemove', help='regionsToRemove', default=''                    , type='string')
    parser.add_option('--outputDir'      , dest='outputDir'      , help='outputDir'      , default='./Plots/'            , type='string')
    parser.add_option('--signal'         , dest='signal'         , help='signal'         , default=''                    , type='string')
    parser.add_option('--legend'         , dest='legend'         , help='legend'         , default=''                    , type='string')

    (opt, args) = parser.parse_args()

    outputName = opt.postFit
    if opt.signal!='': outputName += '_'+opt.signal

    os.system('mkdir -p '+opt.outputDir)

    fileIn = ROOT.TFile.Open(opt.inputFile, 'READ')

    covariance = fileIn.Get('shapes_'+opt.postFit+'/'+opt.covarianceHisto)
    covariance.SetDirectory(0)
    fileIn.Close()

    covariance = makeHistoCopy(covariance, regionsToRemove=opt.regionsToRemove)

    if opt.saveCovariance:
        covariance.SetName('CovarianceMatrix')
        makeMatrixPlot(covariance, opt.outputDir+'/CovarianceMatrix_'+outputName, opt.regionsToRemove, opt.legend)

    CovarianceMatrix = ROOT.TMatrixD(covariance.GetNbinsX(), covariance.GetNbinsY())
    DiagonalMatrix = ROOT.TMatrixD(covariance.GetNbinsX(), covariance.GetNbinsY())
    
    for xb in range(covariance.GetNbinsX()) :
        for yb in range(covariance.GetNbinsY()) :
            CovarianceMatrix[xb][yb] = covariance.GetBinContent(xb+1, yb+1)
            if xb==yb: DiagonalMatrix[xb][yb] = 1./math.sqrt(covariance.GetBinContent(xb+1, yb+1))
            else: DiagonalMatrix[xb][yb] = 0.

    AuxiliaryMatrix = ROOT.TMatrixD(covariance.GetNbinsX(), covariance.GetNbinsY())
    AuxiliaryMatrix.Mult(DiagonalMatrix, CovarianceMatrix)

    CorrelationMatrix = ROOT.TMatrixD(covariance.GetNbinsX(), covariance.GetNbinsY())
    CorrelationMatrix.Mult(AuxiliaryMatrix, DiagonalMatrix)
    
    correlation = makeHistoCopy(covariance, fillContent=False)
    correlation.SetName('CorrelationMatrix')
    
    for xb in range(covariance.GetNbinsX()) :
        for yb in range(covariance.GetNbinsY()) :
            correlation.SetBinContent(xb+1, yb+1, CorrelationMatrix(xb, yb))

    makeMatrixPlot(correlation, opt.outputDir+'/CorrelationMatrix_'+outputName, opt.regionsToRemove, opt.legend)

