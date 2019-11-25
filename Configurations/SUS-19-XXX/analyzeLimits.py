#!/usr/bin/env python
import os
import sys
import ROOT
import optparse

def fileExist(fileName):
    return os.path.isfile(fileName)

def getFileName(outputDirectory, outputFileName, extension='.root'):
    os.system('mkdir -p ' + outputDirectory)
    return outputDirectory + '/' + outputFileName + extension

def fillEmptyBins(sigset, histo):

    if 'T2tt' in sigset:

        for iter in range(4):
            for xb in range(1, histo.GetNbinsX()+1):
                #massX = histo.GetXaxis().GetBinLowEdge(xb)
                massX = histo.GetXaxis().GetBinCenter(xb)
                for yb in range(1, histo.GetNbinsY()+1):
                    massY = histo.GetYaxis().GetBinCenter(yb);
                    if massX-massY>80.:
                        if histo.GetBinContent(xb, yb)==0.:

                            if iter==0 and histo.GetBinContent(xb, yb+1)>0.:
                                if histo.GetYaxis().GetBinLowEdge(yb)<=0.:
                                    histo.SetBinContent(xb, yb, histo.GetBinContent(xb, yb+1))
                                elif histo.GetBinContent(xb, yb-1)>0.:
                                    binContent = (histo.GetBinContent(xb, yb+1)+histo.GetBinContent(xb, yb-1))/2.
                                    histo.SetBinContent(xb, yb, binContent)

                            if iter==1 and histo.GetBinContent(xb+1, yb)>0 and histo.GetBinContent(xb-1, yb)>0.:
                                binContent = (histo.GetBinContent(xb+1, yb)+histo.GetBinContent(xb-1, yb))/2.
                                histo.SetBinContent(xb, yb, binContent)

                            if iter==2 and massX-massY<90. and histo.GetBinContent(xb+1, yb+1)>0. and histo.GetBinContent(xb-1, yb-1)>0.:
                                binContent = (histo.GetBinContent(xb+1, yb+1)+histo.GetBinContent(xb-1, yb-1))/2.
                                histo.SetBinContent(xb, yb, binContent)

                            if iter==3 and massX-massY==175. and histo.GetBinContent(xb+1, yb+1)>0. and histo.GetBinContent(xb-1, yb-1)>0.:
                                binContent = (histo.GetBinContent(xb+1, yb+1)+histo.GetBinContent(xb-1, yb-1))/2.
                                histo.SetBinContent(xb, yb, binContent)
                                
    else:
        print 'Warning: strategy for filling empty bins not available for model', model

def fillMassScanHistograms(year, tag, sigset, limitOption, fillemptybins, outputFileName):
    
    # Get mass points and mass limits
    modelHistogramSettings = { 'T2tt' : { #'X' : { 'binWidth' : 12.5, 'minCenter' : 1.0,  'maxCenter' :  1.0, 'label' : 'M_{#tilde t_{1}} [GeV]'        },
                                          'X' : { 'binWidth' : 12.5, 'minCenter' : 0.5,  'maxCenter' :  0.5, 'label' : 'M_{#tilde t_{1}} [GeV]'        },
                                          'Y' : { 'binWidth' : 12.5, 'minCenter' : 1.5,  'maxCenter' : 16.5, 'label' : 'M_{#tilde #Chi^{0}_{1}} [GeV]' } },
                               # ...
    }
    
    massPoints = { }
    massLimits = { 'X' : { 'min' : 999999., 'max' : -1. }, 'Y' : { 'min' : 999999., 'max' : -1. } }

    inputDirectory = './Limits/'+year+'/' 
    
    limitType = 'blind' if (limitOption=='Blind') else 'expected'
    for model in signalMassPoints:
        if model in sigset:
            if model in modelHistogramSettings.keys():
                histogramSettings = modelHistogramSettings[model]
            else:
                print 'Error: histogram setting for model', model, 'not available'
                exit()
            
            for massPoint in sorted(signalMassPoints[model]):
                #print "masspoint", massPoint
                #print massPointInSignalSet(massPoint,sigset)
                if massPointInSignalSet(massPoint, sigset): 
                  
                    inputFileName = inputDirectory + massPoint + '/higgsCombine_' + tag + '_' + limitOption + '.AsymptoticLimits.mH120.root'
                    inputFile = ROOT.TFile(inputFileName, 'READ')
                
                    inputTree = inputFile.Get('limit')
                    
                    if inputTree:
                        #print "I am indeed reading the tree<---"
                        massX = float(massPoint.split('_')[1].split('-')[1])
                        massY = float(massPoint.split('_')[2].split('-')[1])

                        massLimits['X']['min']  = min(massLimits['X']['min'], massX)
                        massLimits['X']['max']  = max(massLimits['X']['max'], massX)
                        massLimits['Y']['min']  = min(massLimits['Y']['min'], massY)
                        massLimits['Y']['max']  = max(massLimits['Y']['max'], massY)
                        
                        massPoints[massPoint] = { 'massX' : massX, 'massY' : massY }

                        massPointLimits = { } 

                        for event in inputTree :

                            if inputTree.quantileExpected==-1.:
                                massPointLimits['histo_r_observed'] =  inputTree.limit
                            elif inputTree.quantileExpected==0.5:
                                massPointLimits['histo_r_'+limitType] =  inputTree.limit
                            elif round(inputTree.quantileExpected, 2)==0.84:
                                massPointLimits['histo_r_'+limitType+'_up'] =  inputTree.limit
                            elif round(inputTree.quantileExpected, 2)==0.16:
                                massPointLimits['histo_r_'+limitType+'_down'] =  inputTree.limit

                        massPoints[massPoint]['limits'] = massPointLimits
                    
                    inputFile.Close()
    
    # Create and fill histograms
    histoMin, histoMax, histoBin = { }, { }, { } 
    for axis in [ 'X', 'Y' ]:
        binWidth = histogramSettings[axis]['binWidth']
        minEdge = binWidth*int(massLimits[axis]['min']/binWidth)
        maxEdge = binWidth*int(massLimits[axis]['max']/binWidth)
        histoMin[axis] = minEdge - histogramSettings[axis]['minCenter']*binWidth
        histoMax[axis] = maxEdge + histogramSettings[axis]['maxCenter']*binWidth
        histoBin[axis] = int((histoMax[axis] - histoMin[axis])/binWidth)

    massScanHistos = { } 

    for massPoint in massPoints:
        for limit in massPoints[massPoint]['limits']:

            if limit not in massScanHistos:

                massScanHistos[limit] = ROOT.TH2F(limit, 'limit', histoBin['X'], histoMin['X'], histoMax['X'], 
                                                                  histoBin['Y'], histoMin['Y'], histoMax['Y'])
                massScanHistos[limit].SetXTitle(histogramSettings['X']['label'])
                massScanHistos[limit].SetYTitle(histogramSettings['Y']['label'])

            massPointBin = massScanHistos[limit].FindBin(massPoints[massPoint]['massX'], massPoints[massPoint]['massY'])
            massScanHistos[limit].SetBinContent(massPointBin, massPoints[massPoint]['limits'][limit])
    
    # Save histogram file 
    outputFile = ROOT.TFile(outputFileName, 'recreate')

    for histo in massScanHistos:
        if fillemptybins:
            fillEmptyBins(sigset, massScanHistos[histo]) 
        massScanHistos[histo].Write()

    outputFile.Close()

def makeMassScanHistograms(year, tag, sigset, limitOption, fillemptybins, reMakeHistos):
    if tag!='':
      
        outputFileName = getFileName('./Limits/' + year + '/Histograms', 'massScan_' + tag + '_' + sigset + '_' + limitOption)

        if fillemptybins==False:
            outputFileName = outputFileName.replace('.root', '_noFillEmptyBins' + '.root')
            
        if reMakeHistos or not fileExist(outputFileName):
            fillMassScanHistograms(year, tag, sigset, limitOption, fillemptybins, outputFileName)

def plotLimits(year, tags, sigset, limitOptions, plotOption, fillemptybins):
                 
    if plotOption!='Histograms':
        if plotOption=='Contours':
            print 'Error: option Contours for limit comparison not yet implemented'
        else:
            print 'Error: unkown option', plotOption, 'for limit comparison'
        exit()

    emptyBinsOption = ''			
    if fillemptybins==False:		
        emptyBinsOption = '_noFillEmptyBins'

    # Get the objects
    tagObj = [ ] 

    for tag in tags:

        if tag=='':
            continue
            
        tagFileName = getFileName('./Limits/' + year + '/' + plotOption, 'massScan_' + tag + '_' + sigset + '_' + limitOptions[1] + emptyBinsOption)

        if not fileExist(tagFileName):
            print 'Error: input file', tagFileName, 'not found'
            exit()
            
        tagFile = ROOT.TFile(tagFileName, 'READ')

        if plotOption=='Histograms':
            objectName = 'histo_r_'+limitOptions[0].lower()

        obj = tagFile.Get(objectName)
        print "--->obj", obj, "\t FILE", tagFileName, "\t OBJECT", objectName
        obj.SetDirectory(0)
        tagObj.append(obj)

    # Draw comparison
    ROOT.gStyle.SetOptStat(0)

    plotCanvas = ROOT.TCanvas( 'plotCanvas', '', 600, 400)
    
    plotTitle = tags[0]
    
    if tags[1]!='':
        plotTitle += '_to_' + tags[1] 
        if plotOption=='Histograms':
            tagObj[0].Divide(tagObj[1])

    plotTitle += '_' + sigset + '_' + limitOptions[0] + '_' + plotOption + emptyBinsOption
    tagObj[0].SetTitle(plotTitle)

    tagObj[0].Draw('textcolz')
 
    outputFileName = getFileName('./Plots/' + year + '/Limits', plotTitle, '.png')
    plotCanvas.Print(outputFileName)

    plotCanvas.Close()

if __name__ == '__main__':

    # Input parameters
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    
    parser.add_option('--years'        , dest='years'        , help='Year(s) to be processed'                     , default='all')
    parser.add_option('--tag'          , dest='tag'          , help='Tag used for the tag file name'              , default='Test')
    parser.add_option('--sigset'       , dest='sigset'       , help='Model and mass point range'                  , default='')
    parser.add_option('--limitoption'  , dest='limitOption'  , help='Observed (0), Expected (1), Blind (2) limit' , default='Blind')
    parser.add_option('--sigmp'        , dest='signalMPcfg'  , help='Signal mass point cfg file'                  , default='./signalMassPoints.py') 
    parser.add_option('--nomakehistos' , dest='noMakeHistos' , help='Do not make the mass scan histograms'        , default=False, action='store_true')
    parser.add_option('--remakehistos' , dest='reMakeHistos' , help='Redo the mass scan histograms'               , default=False, action='store_true')
    parser.add_option('--nofillempties', dest='noFillEmpties', help='Do not fill empty bins'                      , default=False, action='store_true')
    parser.add_option('--plotoption'   , dest='plotOption'   , help='No plot (-1), Histograms (0), Contours (1)'  , default='-1')
    parser.add_option('--compareto'    , dest='compareTo'    , help='Reference tag used for comparison'           , default='')
    (opt, args) = parser.parse_args()

    if opt.years=='-1' or opt.years=='all' or opt.years=='All':
        year = '2016-2017-2018'
    elif opt.years=='0':
        year = '2016'
    elif opt.years=='1':
        year = '2017'
    elif opt.years=='2':
        year ='2018'
    else:
        year = opt.years

    if opt.limitOption=='0':
        limitOption = 'Observed'
    elif opt.limitOption=='1':
        limitOption = 'Expected-Observed'
    elif opt.limitOption=='2':
        limitOption = 'Expected'
    elif opt.limitOption=='3':
        limitOption = 'Blind'
    else:
        limitOption = opt.limitOption

    limitOptions = limitOption.split('-')
    if len(limitOptions)==1:
        limitOptions.append(limitOption)

    fillEmpties = not opt.noFillEmpties

    if opt.plotOption=='0':
        plotOption = 'Histograms'
    elif opt.plotOption=='1':
        plotOption = 'Contours'
    else:
        plotOption = opt.plotOption
    
    if not opt.noMakeHistos:
        exec(open(opt.signalMPcfg).read())
        makeMassScanHistograms(year, opt.tag,       opt.sigset, limitOptions[1], fillEmpties, opt.reMakeHistos)
        makeMassScanHistograms(year, opt.compareTo, opt.sigset, limitOptions[1], fillEmpties, opt.reMakeHistos)

    if plotOption=='Histograms' or plotOption=='Contours': 
        plotLimits(year, [ opt.tag, opt.compareTo ], opt.sigset, limitOptions, plotOption, fillEmpties) 

"""
#include "TCanvas.h"
#include "TH1D.h"
#include "TH2D.h"
#include "TString.h"
#include "TFile.h"
#include <TROOT.h>
#include <TStyle.h>
#include <TLegend.h>
#include <TLatex.h>
#include <map>

#include "SUSYCrossSections.C"
 
bool Verbose = false;

void MassScan(TString Type = "", TString Version = "", TString Signal = "_T2tt", bool MakeContour = false) {
  
  TH2F *MassLimit, *hXsec_exp, *hR_exp, *hR_exp_up, *hR_exp_do, *hXsec_obs, *hR_obs, *hR_obs_up, *hR_obs_do, *hXsec_the;
  if (Signal.Contains("T2tt")) {
    if (!MakeContour) {
      //MassLimit    = new TH2F("MassLimit",    "",  9, 287.5,  512.5, 13, 112.5, 437.5);
      //MassLimit    = new TH2F("MassLimit",    "", 17, 187.5,  612.5, 18,  87.5, 537.5);
      MassLimit    = new TH2F("MassLimit",    "", 42, 162.5, 1212.5, 32,  12.5, 812.5);
      hXsec_exp    = new TH2F("hXsec_exp",    "", 42, 162.5, 1212.5, 32,  12.5, 812.5);
      hR_exp       = new TH2F("hR_exp",       "", 42, 162.5, 1212.5, 32,  12.5, 812.5);
      hR_exp_up    = new TH2F("hR_exp_up",    "", 42, 162.5, 1212.5, 32,  12.5, 812.5);
      hR_exp_do    = new TH2F("hR_exp_do",    "", 42, 162.5, 1212.5, 32,  12.5, 812.5);
      hXsec_obs    = new TH2F("hXsec_obs",    "", 42, 162.5, 1212.5, 32,  12.5, 812.5);
      hR_obs       = new TH2F("hR_obs",       "", 42, 162.5, 1212.5, 32,  12.5, 812.5);
      hR_obs_up    = new TH2F("hR_obs_up",    "", 42, 162.5, 1212.5, 32,  12.5, 812.5);
      hR_obs_do    = new TH2F("hR_obs_do",    "", 42, 162.5, 1212.5, 32,  12.5, 812.5);
      hXsec_the    = new TH2F("hXsec_the",    "", 42, 162.5, 1212.5, 32,  12.5, 812.5);
    } else {
      MassLimit    = new TH2F("MassLimit",    "", 86, 137.5, 1212.5, 66,  -6.25-12.5, 806.25);
      hXsec_exp    = new TH2F("hXsec_exp",    "", 86, 137.5, 1212.5, 66,  -6.25-12.5, 806.25);
      hR_exp       = new TH2F("hR_exp",       "", 86, 137.5, 1212.5, 66,  -6.25-12.5, 806.25);
      hR_exp_up    = new TH2F("hR_exp_up",    "", 86, 137.5, 1212.5, 66,  -6.25-12.5, 806.25);
      hR_exp_do    = new TH2F("hR_exp_do",    "", 86, 137.5, 1212.5, 66,  -6.25-12.5, 806.25);
      hXsec_obs    = new TH2F("hXsec_obs",    "", 86, 137.5, 1212.5, 66,  -6.25-12.5, 806.25);
      hR_obs       = new TH2F("hR_obs",       "", 86, 137.5, 1212.5, 66,  -6.25-12.5, 806.25);
      hR_obs_up    = new TH2F("hR_obs_up",    "", 86, 137.5, 1212.5, 66,  -6.25-12.5, 806.25);
      hR_obs_do    = new TH2F("hR_obs_do",    "", 86, 137.5, 1212.5, 66,  -6.25-12.5, 806.25);
      hXsec_the    = new TH2F("hXsec_the",    "", 86, 137.5, 1212.5, 66,  -6.25-12.5, 806.25);
    }
  } else if (Signal.Contains("T2bW")) {
    //MassLimit    = new TH2F("MassLimit",    "", 21, 187.5,  712.5, 26, -12.5, 637.5);
    MassLimit    = new TH2F("MassLimit",    "", 43, 137.5, 1212.5, 33,  -12.5, 812.5);
    hXsec_exp    = new TH2F("hXsec_exp",    "", 43, 137.5, 1212.5, 33,  -12.5, 812.5);
    hR_exp       = new TH2F("hR_exp",       "", 43, 137.5, 1212.5, 33,  -12.5, 812.5);
    hR_exp_up    = new TH2F("hR_exp_up",    "", 43, 137.5, 1212.5, 33,  -12.5, 812.5);
    hR_exp_do    = new TH2F("hR_exp_do",    "", 43, 137.5, 1212.5, 33,  -12.5, 812.5);
    hXsec_obs    = new TH2F("hXsec_obs",    "", 43, 137.5, 1212.5, 33,  -12.5, 812.5);
    hR_obs       = new TH2F("hR_obs",       "", 43, 137.5, 1212.5, 33,  -12.5, 812.5);
    hR_obs_up    = new TH2F("hR_obs_up",    "", 43, 137.5, 1212.5, 33,  -12.5, 812.5);
    hR_obs_do    = new TH2F("hR_obs_do",    "", 43, 137.5, 1212.5, 33,  -12.5, 812.5);
    hXsec_the    = new TH2F("hXsec_the",    "", 43, 137.5, 1212.5, 33,  -12.5, 812.5);
    //hXsec_exp    = new TH2F("hXsec_exp",    "", 42, 150.0, 1200.0, 32,   0.0, 800.0);
    //hR_exp       = new TH2F("hR_exp",       "", 42, 150.0, 1200.0, 32,   0.0, 800.0);
    //hR_exp_up    = new TH2F("hR_exp_up",    "", 42, 150.0, 1200.0, 32,   0.0, 800.0);
    //hR_exp_do    = new TH2F("hR_exp_do",    "", 42, 150.0, 1200.0, 32,   0.0, 800.0);
  } else if (Signal.Contains("dM10to80")) {
    MassLimit    = new TH2F("MassLimit",    "", 15, 237.5,  612.5,  44, 155.,  595.);
    hXsec_exp    = new TH2F("hXsec_exp",    "", 42, 162.5, 1212.5, 120,  -5., 1195.);
    hR_exp       = new TH2F("hR_exp",       "", 42, 162.5, 1212.5, 120,  -5., 1195.);
    hR_exp_up    = new TH2F("hR_exp_up",    "", 42, 162.5, 1212.5, 120,  -5., 1195.);
    hR_exp_do    = new TH2F("hR_exp_do",    "", 42, 162.5, 1212.5, 120,  -5., 1195.);
  } else if (Signal.Contains("ChiWW")) {
    MassLimit    = new TH2F("MassLimit",    "", 11,  87.5,  362.5, 56,  -7.5, 272.5);
    hXsec_exp    = new TH2F("hXsec_exp",    "", 11,  87.5,  362.5, 56,  -7.5, 272.5);
    hR_exp       = new TH2F("hR_exp",       "", 11,  87.5,  362.5, 56,  -7.5, 272.5);
    hR_exp_up    = new TH2F("hR_exp_up",    "", 11,  87.5,  362.5, 56,  -7.5, 272.5);
    hR_exp_do    = new TH2F("hR_exp_do",    "", 11,  87.5,  362.5, 56,  -7.5, 272.5);
    hXsec_obs    = new TH2F("hXsec_obs",    "", 11,  87.5,  362.5, 56,  -7.5, 272.5);
    hR_obs       = new TH2F("hR_obs",       "", 11,  87.5,  362.5, 56,  -7.5, 272.5);
    hR_obs_up    = new TH2F("hR_obs_up",    "", 11,  87.5,  362.5, 56,  -7.5, 272.5);
    hR_obs_do    = new TH2F("hR_obs_do",    "", 11,  87.5,  362.5, 56,  -7.5, 272.5);
    hXsec_the    = new TH2F("hXsec_the",    "", 11,  87.5,  362.5, 56,  -7.5, 272.5);
  } else if (Signal.Contains("ChiSlep")) {
    MassLimit    = new TH2F("MassLimit",    "", 37,  87.5,  1012.5, 25, -12.5, 612.5);
    hXsec_exp    = new TH2F("hXsec_exp",    "", 37,  87.5,  1012.5, 25, -12.5, 612.5);
    hR_exp       = new TH2F("hR_exp",       "", 37,  87.5,  1012.5, 25, -12.5, 612.5);
    hR_exp_up    = new TH2F("hR_exp_up",    "", 37,  87.5,  1012.5, 25, -12.5, 612.5);
    hR_exp_do    = new TH2F("hR_exp_do",    "", 37,  87.5,  1012.5, 25, -12.5, 612.5);
    hXsec_obs    = new TH2F("hXsec_obs",    "", 37,  87.5,  1012.5, 25, -12.5, 612.5);
    hR_obs       = new TH2F("hR_obs",       "", 37,  87.5,  1012.5, 25, -12.5, 612.5);
    hR_obs_up    = new TH2F("hR_obs_up",    "", 37,  87.5,  1012.5, 25, -12.5, 612.5);
    hR_obs_do    = new TH2F("hR_obs_do",    "", 37,  87.5,  1012.5, 25, -12.5, 612.5);
    hXsec_the    = new TH2F("hXsec_the",    "", 37,  87.5,  1012.5, 25, -12.5, 612.5);
  }

  //SetSUSYProductionMap(Signal);

  ifstream InFile; InFile.open("./MassPointList" + Signal + ".txt");
  
  float CentralQuantile = -1.;
  if (Type!="") CentralQuantile = 0.5;
  if (Type.Contains("Do")) CentralQuantile = 0.84;
  if (Type.Contains("Up")) CentralQuantile = 0.16;
  if (Type.Contains("Blind")) Type = "Blind";
  else if (Type.Contains("Expected")) Type = "Expected";
  else Type = "";

  while (InFile) {

    TString MassPointName;
    InFile >> MassPointName;
    
    if (!MassPointName.Contains("#") && MassPointName!="") {
      
      TString RootFileName = "./Datacards" + Version + "/MassPoint" + MassPointName + "/datacardFinal" + Type + ".root";
      //TString RootFileName = "./Datacards" + Version + "/MassPoint" + MassPointName + "/datacardFinalExpected.root";
      //RootFileName.ReplaceAll("2tt", "tt");
      TFile *RootFile = TFile::Open(RootFileName, "read");

      if (!RootFile) continue;

      //if (Signal=="") MassPointName.ReplaceAll("tt_isr", ""); 	     
      TString StopMass = MassPointName;
      StopMass.Replace(0, StopMass.First("_")+1, "");
      if (Signal.Contains("T2tt")) StopMass.Replace(0, StopMass.First("_")+1, "");
      //if (Signal=="") StopMass.Replace(0, StopMass.First("_")+1, ""); 
      TString XMass = StopMass;
      StopMass.Replace(StopMass.First("_"), 10000,""); 
      StopMass.ReplaceAll("Sm", "");
      StopMass.ReplaceAll("Xm", "");
      XMass.Replace(0, XMass.First("_")+1, "");
      XMass.ReplaceAll("Xm", "");
      int iStopMass = StopMass.Atoi();
      int iXMass = XMass.Atoi();

      //MassPoint ThisMassPoint (iStopMass, iXMass);
      //MassPointParameters TheseMassPointParameters = StopNeutralinoMap.at(ThisMassPoint);
      //StopCrossSection ThisStopCrossSection = TheseMassPointParameters.first;
 
      if (Signal.Contains("T2") && iStopMass%5!=0) continue;

      if (Signal.Contains("T2")) GetSUSYCrossSection(1.*iStopMass, "T2");
      else GetSUSYCrossSection(1.*iStopMass, "TChi");
      
      //float CrossSection   = ThisStopCrossSection.first;
      float CrossSectionUp = CrossSection + CrossSectionUncertainty;//ThisStopCrossSection.second;
      float CrossSectionDo = CrossSection - CrossSectionUncertainty;//ThisStopCrossSection.second;

      //if (Signal=="_TChiWW") {
      //CrossSection   /= 0.10497000068426132;
      //CrossSectionUp /= 0.10497000068426132;
      //CrossSectionDo /= 0.10497000068426132;
      //}
      
      if (!RootFile) { 
	if (Verbose) cout << " Warning: file " << MassPointName << " not found " << endl;
	//int iBin = hXsec_exp->FindBin(iStopMass, iXMass);
        //float _plimit = hR_exp->GetBinContent(iBin-1);
	//hXsec_exp->Fill(iStopMass, iXMass, _plimit*CrossSection);
	continue;
      }
      
      TTree *fChain = (TTree*) RootFile->Get("limit");
      
      float _quantileExpected; Double_t _limit;
      fChain->SetBranchAddress("quantileExpected", &_quantileExpected);
      fChain->SetBranchAddress("limit",            &_limit);
      
      int _nentries     = fChain->GetEntries();
      
      if (_nentries<6) {
	if (Verbose) cout << " Warning: file " << MassPointName << " not written " << endl;
	//int iBin = hXsec_exp->GetBin(iStopMass, iXMass);
        //_limit = hR_exp->GetBinContent(iBin-1);
	//if (_limit==0.8) 
	//hXsec_exp->Fill(iStopMass, iXMass, 0.08*CrossSection);
	//hR_exp->Fill(iStopMass, iXMass, 0.08);
	continue;
      }
      
      for (Long64_t jentry=0; jentry<_nentries; jentry++) {
	
	fChain->GetEntry(jentry);
	
	//if (_quantileExpected==-1. && iStopMass==100 && iXMass==1) cout << "ss " << _limit << endl;
	
	int _ilimit = 100.*_limit;
	float _flimit = _limit>=0.01 ? _ilimit/100. : 0.01 ;
	
	if (_quantileExpected==CentralQuantile) {
	  MassLimit->Fill(iStopMass, iXMass, _flimit);
	  hXsec_the->Fill(iStopMass, iXMass, CrossSection);
	}
	
	if (_quantileExpected==0.5) {
	  hXsec_exp->Fill(iStopMass, iXMass, _limit*CrossSection);
	  hR_exp->Fill(iStopMass, iXMass, _limit);
	  if (CentralQuantile!=-1.) {
	    hXsec_obs->Fill(iStopMass, iXMass, _limit*CrossSection);
	    hR_obs->Fill(iStopMass, iXMass, _limit);
	  }
	} else if (_quantileExpected>0.15 && _quantileExpected<0.17) {
	  hR_exp_up->Fill(iStopMass, iXMass, _limit);
	  if (CentralQuantile!=-1.) hR_obs_up->Fill(iStopMass, iXMass, _limit);
        } else if (_quantileExpected>0.83 && _quantileExpected<0.85) { 	
	  hR_exp_do->Fill(iStopMass, iXMass, _limit);
	  if (CentralQuantile!=-1.) hR_obs_do->Fill(iStopMass, iXMass, _limit);
        } else if (_quantileExpected==-1. && CentralQuantile==-1.) {
	  hXsec_obs->Fill(iStopMass, iXMass, _limit*CrossSection);
	  hR_obs->Fill(iStopMass, iXMass, _limit);
	  hR_obs_up->Fill(iStopMass, iXMass, _limit*CrossSection/CrossSectionUp);
	  hR_obs_do->Fill(iStopMass, iXMass, _limit*CrossSection/CrossSectionDo);
	}

      }

    }

  }

  gStyle->SetOptStat(0);
  MassLimit->SetXTitle("M_{#tilde t} [GeV]");
  MassLimit->SetYTitle("M_{#tilde #Chi^{0}_{1}} [GeV]");
  if (Signal.Contains("TChi")) MassLimit->SetXTitle("M_{#tilde #Chi^{#pm}_{1}} [GeV]");

  TCanvas *CC = new TCanvas("CC", "", 900, 600);
  CC->cd();

  if (!MakeContour) MassLimit->Draw("TEXT");
  //if (!MakeContour) hR_obs->Draw("TEXTCOLZ");
  
  //if (!MakeContour) hXsec_exp->Draw("TEXTCOLZ");
  //return;
  /*TFile *RootFile = new TFile(Signal + "_histo.root", "recreate");	
  RootFile->cd();
  
  hR_exp->Write(); 
  hR_exp_up->Write();
  hR_exp_do->Write(); 

  RootFile->Close();*/
  
  if (!MakeContour) return;

  if (Signal=="_TChiWW") {

    for (int xx = 1; xx<=MassLimit->GetNbinsX(); xx++) {
      
      int XX = MassLimit->GetXaxis()->GetBinCenter(xx);
      GetSUSYCrossSection(1.*XX, "TChi");
      
      MassLimit->SetBinContent(xx, 1, 0.5);
      hXsec_exp->SetBinContent(xx, 1, 0.5*CrossSection);
      hR_exp   ->SetBinContent(xx, 1, 0.5);
      hR_exp_up->SetBinContent(xx, 1, 0.5);
      hR_exp_do->SetBinContent(xx, 1, 0.5);
      hR_obs   ->SetBinContent(xx, 1, 0.5);
      hR_obs_up->SetBinContent(xx, 1, 0.5);
      hR_obs_do->SetBinContent(xx, 1, 0.5);
      
    }

    for (int xx = 1; xx<=MassLimit->GetNbinsX(); xx++) {
      float XX = MassLimit->GetXaxis()->GetBinCenter(xx);
      for (int yy = 2; yy<=MassLimit->GetNbinsY(); yy++) {
	float YY = MassLimit->GetYaxis()->GetBinCenter(yy);

	if (XX-YY>80.) {

	  if (YY>20.) {
	    
	    //MassLimit->SetBinContent(xx, yy, 1.5);
	    //hXsec_exp->SetBinContent(xx, yy, 1.5*CrossSection);
	    hR_exp   ->SetBinContent(xx, yy, 1.5);
	    //hR_exp_up->SetBinContent(xx, yy, 1.5);
	    hR_exp_do->SetBinContent(xx, yy, 1.5);
	    hR_obs   ->SetBinContent(xx, yy, 1.5);
	    hR_obs_up->SetBinContent(xx, yy, 1.5);
	    hR_obs_do->SetBinContent(xx, yy, 1.5);
	    
	  } 

	  if (MassLimit->GetBinContent(xx, yy)==0.) {
	  
	    int Yoffset;
	    if (XX-YY<100.) Yoffset = 1;
	    else {
	      int bb = (yy-2)%5;
	      if (bb<=2) Yoffset = -bb;
	      else Yoffset = 5-bb;
	    }
	    //MassLimit->SetBinContent(xx, yy, MassLimit->GetBinContent(xx, yy+Yoffset));
	    hXsec_exp->SetBinContent(xx, yy, hXsec_exp->GetBinContent(xx, yy+Yoffset));
	    hR_exp_up->SetBinContent(xx, yy, hR_exp_up->GetBinContent(xx, yy+Yoffset));
	    hXsec_the->SetBinContent(xx, yy, hXsec_the->GetBinContent(xx, yy+Yoffset));
	    if (YY<25.) {
	      hXsec_obs->SetBinContent(xx, yy, hXsec_obs->GetBinContent(xx, yy+Yoffset));
	      hR_exp   ->SetBinContent(xx, yy, hR_exp   ->GetBinContent(xx, yy+Yoffset));
	      hR_exp_do->SetBinContent(xx, yy, hR_exp_do->GetBinContent(xx, yy+Yoffset));
	      hR_obs   ->SetBinContent(xx, yy, hR_obs   ->GetBinContent(xx, yy+Yoffset));
	      hR_obs_up->SetBinContent(xx, yy, hR_obs_up->GetBinContent(xx, yy+Yoffset));
	      hR_obs_do->SetBinContent(xx, yy, hR_obs_do->GetBinContent(xx, yy+Yoffset));
	    }

	  }

	}

      }

    }

    // Smooth
    //hR_exp->SetBinContent(2, 1, (hR_exp->GetBinContent(1,1)+hR_exp->GetBinContent(3,1))/2.);
    //hR_exp->SetBinContent(4, 1, (hR_exp->GetBinContent(3,1)+hR_exp->GetBinContent(5,1))/2.);
    //hR_exp->SetBinContent(5, 4, 0.98);
    //hR_exp->SetBinContent(5, 5, 0.98);
    
  }
  
  if (Signal=="_TChiSlep") {
    
    for (int lk = 0; lk<2; lk++) {
      for (int yy = 1; yy<=MassLimit->GetNbinsY(); yy++) {

	int YY = yy>1 ? MassLimit->GetYaxis()->GetBinCenter(yy) : 1;
	int holebegin = -1, holeend = -1;
	float LastLimit = -1.;
	
	for (int xx = 1; xx<=MassLimit->GetNbinsX(); xx++) {
	  
	  int XX = MassLimit->GetXaxis()->GetBinCenter(xx);

	  if (XX-YY-25.<10.) continue;
	  if (YY>420.) continue;
	  
	  float xRef = lk==0 ? hR_exp->GetBinContent(xx, yy) : hR_obs->GetBinContent(xx, yy);
	  if (lk==1 && hR_obs->GetBinContent(xx, yy)/hR_exp->GetBinContent(xx, yy)<0.21) {
	    hXsec_obs->SetBinContent(xx, yy, 0.);
	    hR_obs->SetBinContent(xx, yy, 0.);
	    hR_obs_up->SetBinContent(xx, yy, 0.);
	    hR_obs_do->SetBinContent(xx, yy, 0.);
	    xRef = 0.;
	  }

	  if (LastLimit==-1.) {
	    if (xRef>0.) LastLimit = xRef;
	    continue;
	  }

	  //if (hXsec_exp->GetBinContent(xx, yy)<0.05) cout << MassLimit->GetXaxis()->GetBinCenter(xx) << " " << MassLimit->GetYaxis()->GetBinCenter(yy) << " " << hXsec_exp->GetBinContent(xx, yy) << endl;

	  if (xRef>0. && holebegin==-1) {
	    //LastLimit = MassLimit->GetBinContent(xx, yy);
	    LastLimit = xRef;
	    continue;
	  } else {

	    if (xRef==0.) {
	      if (holebegin==-1) holebegin = xx;
	      continue;
	    } else {
	      	
	      holeend = xx-1;
	      float LimitStep = (xRef - LastLimit)/(xx-holebegin+1); 
	      float LimitStepExp = (hR_exp->GetBinContent(xx, yy)-hR_exp->GetBinContent(holebegin-1, yy))/(xx-holebegin+1);
	      float LimitStepObs = (hR_obs->GetBinContent(xx, yy)-hR_obs->GetBinContent(holebegin-1, yy))/(xx-holebegin+1);
	      		
	      for (int hx = holebegin; hx<xx; hx++) {
		
		float HoleLimit = LastLimit + LimitStep*(hx-holebegin+1);
		float HoleLimitExp =  hR_exp->GetBinContent(holebegin-1, yy) + LimitStepExp*(hx-holebegin+1);
		float HoleLimitObs =  hR_obs->GetBinContent(holebegin-1, yy) + LimitStepObs*(hx-holebegin+1);

		int HX = MassLimit->GetXaxis()->GetBinCenter((hx+xx)/2);
		GetSUSYCrossSection(1.*XX, "TChi");
		float CrossSectionUp = CrossSection + CrossSectionUncertainty;
		float CrossSectionDo = CrossSection - CrossSectionUncertainty;
		
		//MassLimit->SetBinContent(hx, yy, HoleLimit);
		if (lk==0) {
		  hXsec_exp->SetBinContent(hx, yy, HoleLimit*CrossSection);
		  hR_exp   ->SetBinContent(hx, yy, HoleLimit);
		  hXsec_the->SetBinContent(hx, yy, CrossSection); 
		} else {
		  GetSUSYCrossSection(1.*HX, "TChi");
		  hXsec_obs->SetBinContent(hx, yy, HoleLimit*CrossSection);
		  hR_obs   ->SetBinContent(hx, yy, HoleLimit);
		  hR_obs_up->SetBinContent(hx, yy, HoleLimit*CrossSection/CrossSectionUp);
		  hR_obs_do->SetBinContent(hx, yy, HoleLimit*CrossSection/CrossSectionDo);
		}

	      }
	      
	      holebegin = -1;
	      holeend = -1;
	      
	    }
	    
	  }
	  
	}
	
      }
    }

  }
  
  if (Signal.Contains("_T2tt")) {
    
    for (int xx = 1; xx<=MassLimit->GetNbinsX(); xx++) {
      
      int XX = MassLimit->GetXaxis()->GetBinCenter(xx);
      GetSUSYCrossSection(1.*XX, "T2");

      MassLimit->SetBinContent(xx, 1, 0.5);
      hXsec_exp->SetBinContent(xx, 1, 0.5*CrossSection);
      hXsec_obs->SetBinContent(xx, 1, 0.5*CrossSection);
      hR_exp   ->SetBinContent(xx, 1, 0.5);
      hR_exp_up->SetBinContent(xx, 1, 0.5);
      hR_exp_do->SetBinContent(xx, 1, 0.5);
      hR_obs   ->SetBinContent(xx, 1, 1.5);
      hR_obs_up->SetBinContent(xx, 1, 1.5);
      hR_obs_do->SetBinContent(xx, 1, 1.5);
      
    }
    
    for (int iter = 0; iter<4; iter++) {
      
      for (int yy = 2; yy<=MassLimit->GetNbinsY(); yy++) {

	if (MassLimit->GetYaxis()->GetBinCenter(yy)>651.) continue;
	
	int YY = MassLimit->GetYaxis()->GetBinCenter(yy);
	float rYY = MassLimit->GetYaxis()->GetBinCenter(yy);
	
	for (int xx = 1; xx<=MassLimit->GetNbinsX(); xx++) {
	  
	  int XX = MassLimit->GetXaxis()->GetBinCenter(xx);
	  float rXX = MassLimit->GetXaxis()->GetBinCenter(xx);

	  if (XX-YY<80.) continue;

	  if (MassLimit->GetBinContent(xx, yy)==0.) {
	    
	    float NextLimit = -1, NextXsec;
	    float Next_hR_exp, Next_hR_exp_up, Next_hR_exp_do;
	    float Next_hR_obs, Next_hR_obs_up, Next_hR_obs_do;
	   
	    if (iter==0) {
	      
	      if (MassLimit->GetBinContent(xx+1, yy)>0.) {
		NextLimit      = MassLimit->GetBinContent(xx+1, yy);
		Next_hR_exp    = hR_exp   ->GetBinContent(xx+1, yy);
		Next_hR_exp_up = hR_exp_up->GetBinContent(xx+1, yy);
		Next_hR_exp_do = hR_exp_do->GetBinContent(xx+1, yy);
		Next_hR_obs    = hR_obs   ->GetBinContent(xx+1, yy);
		Next_hR_obs_up = hR_obs_up->GetBinContent(xx+1, yy);
		Next_hR_obs_do = hR_obs_do->GetBinContent(xx+1, yy);
		NextXsec       = hXsec_the->GetBinContent(xx+1, yy);
	      }

	    } else if (iter==1 && XX-YY>305.) {

	      if ((yy-2)%4==0) {
		int xm = (MassLimit->GetBinContent(xx+1, yy)>0.) ? -2 : -1;
		int xp = (MassLimit->GetBinContent(xx+1, yy)>0.) ? +1 : +2;
		int xc = (MassLimit->GetBinContent(xx+1, yy)>0.) ?  0 : +1;
		NextLimit      = (MassLimit->GetBinContent(xx+xm, yy)+MassLimit->GetBinContent(xx+xp, yy))/2.;
		Next_hR_exp    = (hR_exp   ->GetBinContent(xx+xm, yy)+hR_exp   ->GetBinContent(xx+xp, yy))/2.;
		Next_hR_exp_up = (hR_exp_up->GetBinContent(xx+xm, yy)+hR_exp_up->GetBinContent(xx+xp, yy))/2.;
		Next_hR_exp_do = (hR_exp_do->GetBinContent(xx+xm, yy)+hR_exp_do->GetBinContent(xx+xp, yy))/2.;
		Next_hR_obs    = (hR_obs   ->GetBinContent(xx+xm, yy)+hR_obs   ->GetBinContent(xx+xp, yy))/2.;
		Next_hR_obs_up = (hR_obs_up->GetBinContent(xx+xm, yy)+hR_obs_up->GetBinContent(xx+xp, yy))/2.;
		Next_hR_obs_do = (hR_obs_do->GetBinContent(xx+xm, yy)+hR_obs_do->GetBinContent(xx+xp, yy))/2.;
		GetSUSYCrossSection(1.*hXsec_the->GetXaxis()->GetBinLowEdge(xx+xc), "T2");
		NextXsec       = CrossSection;
	      }

	    } else if (iter==2) {
	      
	      if ((yy-2)%4==2) { 
		if (MassLimit->GetBinContent(xx-2, yy-2)>0. && MassLimit->GetBinContent(xx+2, yy+2)>0.) {
		  NextLimit      = (MassLimit->GetBinContent(xx-2, yy-2)+MassLimit->GetBinContent(xx+2, yy+2))/2.;
		  Next_hR_exp    = (hR_exp   ->GetBinContent(xx-2, yy-2)+hR_exp   ->GetBinContent(xx+2, yy+2))/2.;
		  Next_hR_exp_up = (hR_exp_up->GetBinContent(xx-2, yy-2)+hR_exp_up->GetBinContent(xx+2, yy+2))/2.;
		  Next_hR_exp_do = (hR_exp_do->GetBinContent(xx-2, yy-2)+hR_exp_do->GetBinContent(xx+2, yy+2))/2.;
		  Next_hR_obs    = (hR_obs   ->GetBinContent(xx-2, yy-2)+hR_obs   ->GetBinContent(xx+2, yy+2))/2.;
		  Next_hR_obs_up = (hR_obs_up->GetBinContent(xx-2, yy-2)+hR_obs_up->GetBinContent(xx+2, yy+2))/2.;
		  Next_hR_obs_do = (hR_obs_do->GetBinContent(xx-2, yy-2)+hR_obs_do->GetBinContent(xx+2, yy+2))/2.;
		} else { 
		  NextLimit      = (MassLimit->GetBinContent(xx, yy-2)+MassLimit->GetBinContent(xx, yy+2))/2.;
		  Next_hR_exp    = (hR_exp   ->GetBinContent(xx, yy-2)+hR_exp   ->GetBinContent(xx, yy+2))/2.;
		  Next_hR_exp_up = (hR_exp_up->GetBinContent(xx, yy-2)+hR_exp_up->GetBinContent(xx, yy+2))/2.;
		  Next_hR_exp_do = (hR_exp_do->GetBinContent(xx, yy-2)+hR_exp_do->GetBinContent(xx, yy+2))/2.;
		  Next_hR_obs    = (hR_obs   ->GetBinContent(xx, yy-2)+hR_obs   ->GetBinContent(xx, yy+2))/2.;
		  Next_hR_obs_up = (hR_obs_up->GetBinContent(xx, yy-2)+hR_obs_up->GetBinContent(xx, yy+2))/2.;
		  Next_hR_obs_do = (hR_obs_do->GetBinContent(xx, yy-2)+hR_obs_do->GetBinContent(xx, yy+2))/2.;
		}
		int xc = (int(hXsec_the->GetXaxis()->GetBinLowEdge(xx))%5==0) ? 0 : +1;
		GetSUSYCrossSection(1.*hXsec_the->GetXaxis()->GetBinLowEdge(xx+xc), "T2");
		NextXsec       = CrossSection;
	      }
	      
	    } else if (iter==3) {
	      
	      if ((yy-2)%2==1) { 
		if (MassLimit->GetBinContent(xx-1, yy-1)>0. && MassLimit->GetBinContent(xx+1, yy+1)>0.) {
		  NextLimit      = (MassLimit->GetBinContent(xx-1, yy-1)+MassLimit->GetBinContent(xx+1, yy+1))/2.;
		  Next_hR_exp    = (hR_exp   ->GetBinContent(xx-1, yy-1)+hR_exp   ->GetBinContent(xx+1, yy+1))/2.;
		  Next_hR_exp_up = (hR_exp_up->GetBinContent(xx-1, yy-1)+hR_exp_up->GetBinContent(xx+1, yy+1))/2.;
		  Next_hR_exp_do = (hR_exp_do->GetBinContent(xx-1, yy-1)+hR_exp_do->GetBinContent(xx+1, yy+1))/2.;
		  Next_hR_obs    = (hR_obs   ->GetBinContent(xx-1, yy-1)+hR_obs   ->GetBinContent(xx+1, yy+1))/2.;
		  Next_hR_obs_up = (hR_obs_up->GetBinContent(xx-1, yy-1)+hR_obs_up->GetBinContent(xx+1, yy+1))/2.;
		  Next_hR_obs_do = (hR_obs_do->GetBinContent(xx-1, yy-1)+hR_obs_do->GetBinContent(xx+1, yy+1))/2.;
		} else {
		  NextLimit      = (MassLimit->GetBinContent(xx, yy-1)+MassLimit->GetBinContent(xx, yy+1))/2.;
		  Next_hR_exp    = (hR_exp   ->GetBinContent(xx, yy-1)+hR_exp   ->GetBinContent(xx, yy+1))/2.;
		  Next_hR_exp_up = (hR_exp_up->GetBinContent(xx, yy-1)+hR_exp_up->GetBinContent(xx, yy+1))/2.;
		  Next_hR_exp_do = (hR_exp_do->GetBinContent(xx, yy-1)+hR_exp_do->GetBinContent(xx, yy+1))/2.;
		  Next_hR_obs    = (hR_obs   ->GetBinContent(xx, yy-1)+hR_obs   ->GetBinContent(xx, yy+1))/2.;
		  Next_hR_obs_up = (hR_obs_up->GetBinContent(xx, yy-1)+hR_obs_up->GetBinContent(xx, yy+1))/2.;
		  Next_hR_obs_do = (hR_obs_do->GetBinContent(xx, yy-1)+hR_obs_do->GetBinContent(xx, yy+1))/2.;
		}
		int xc = (int(hXsec_the->GetXaxis()->GetBinLowEdge(xx))%5==0) ? 0 : +1;
		GetSUSYCrossSection(1.*hXsec_the->GetXaxis()->GetBinLowEdge(xx+xc), "T2");
		NextXsec       = CrossSection;
	      }
	      
	    } else if (iter==4) {
	      if ((yy-2)%2==0 && (XX-YY)<82.) { // && YY<460. && YY>370.) {
		int xc = (int(hXsec_the->GetXaxis()->GetBinLowEdge(xx))%5==0) ? 0 : +1;
		GetSUSYCrossSection(1.*hXsec_the->GetXaxis()->GetBinLowEdge(xx+xc), "T2");
		NextXsec       = CrossSection;
		Next_hR_exp    = (hR_exp   ->GetBinContent(xx-1, yy-1)+hR_exp   ->GetBinContent(xx+1, yy+1))/2.;
		Next_hR_obs    = (hR_obs   ->GetBinContent(xx-1, yy-1)+hR_obs   ->GetBinContent(xx+1, yy+1))/2.;
		hXsec_exp->SetBinContent(xx, yy, Next_hR_exp*NextXsec);
		hXsec_obs->SetBinContent(xx, yy, Next_hR_obs*NextXsec);
		if (XX==481) {
		  GetSUSYCrossSection(450., "T2");
		  Next_hR_exp    = (hR_exp   ->GetBinContent(xx-3, yy-3)+hR_exp   ->GetBinContent(xx-1, yy-1))/2.;
		  Next_hR_obs    = (hR_obs   ->GetBinContent(xx-3, yy-3)+hR_obs   ->GetBinContent(xx-1, yy-1))/2.;
		  hXsec_exp->SetBinContent(xx-2, yy-2, Next_hR_exp*CrossSection);
		  hXsec_obs->SetBinContent(xx-2, yy-2, Next_hR_obs*CrossSection);
		  GetSUSYCrossSection(500., "T2");
		  Next_hR_exp    = (hR_exp   ->GetBinContent(xx+1, yy+1)+hR_exp   ->GetBinContent(xx+3, yy+3))/2.;
		  Next_hR_obs    = (hR_obs   ->GetBinContent(xx+1, yy+1)+hR_obs   ->GetBinContent(xx+3, yy+3))/2.;
		  hXsec_exp->SetBinContent(xx+2, yy+2, Next_hR_exp*CrossSection);
		  hXsec_obs->SetBinContent(xx+2, yy+2, Next_hR_obs*CrossSection);
		}
	      }
	      
	    }
	    
	    /*if (fabs(XX-YY-175)<15. &&
	      (MassLimit->GetBinContent(xx, yy+1)>=1. || MassLimit->GetBinContent(xx, yy-1)>=1.) &&
		(MassLimit->GetBinContent(xx, yy+1)<1.  || MassLimit->GetBinContent(xx, yy-1)<1. )) {

	      

		}  
	    if (XX-YY>80. && XX-YY<305.) {
	    
	      if (MassLimit->GetBinContent(xx, yy+1)>0. && MassLimit->GetBinContent(xx, yy-1)>0.) {
		NextLimit = (MassLimit->GetBinContent(xx, yy+1)+MassLimit->GetBinContent(xx, yy-1))/2.;
		Next_hR_exp    = (hR_exp   ->GetBinContent(xx, yy+1)+hR_exp   ->GetBinContent(xx, yy-1))/2.;
		Next_hR_exp_up = (hR_exp_up->GetBinContent(xx, yy+1)+hR_exp_up->GetBinContent(xx, yy-1))/2.;
		Next_hR_exp_do = (hR_exp_do->GetBinContent(xx, yy+1)+hR_exp_do->GetBinContent(xx, yy-1))/2.;
		Next_hR_obs    = (hR_obs   ->GetBinContent(xx, yy+1)+hR_obs   ->GetBinContent(xx, yy-1))/2.;
		Next_hR_obs_up = (hR_obs_up->GetBinContent(xx, yy+1)+hR_obs_up->GetBinContent(xx, yy-1))/2.;
		Next_hR_obs_do = (hR_obs_do->GetBinContent(xx, yy+1)+hR_obs_do->GetBinContent(xx, yy-1))/2.;
	      }
	      
	    } else 
	      } else if (iter==1 && (yy-2)%2==1) {
		int ys = ((yy-2)%4==1) ? -1 : 1;
		NextLimit      = MassLimit->GetBinContent(xx, yy+ys);
		Next_hR_exp    = hR_exp   ->GetBinContent(xx, yy+ys);
		Next_hR_exp_up = hR_exp_up->GetBinContent(xx, yy+ys);
		Next_hR_exp_do = hR_exp_do->GetBinContent(xx, yy+ys);
		Next_hR_obs    = hR_obs   ->GetBinContent(xx, yy+ys);
		Next_hR_obs_up = hR_obs_up->GetBinContent(xx, yy+ys);
		Next_hR_obs_do = hR_obs_do->GetBinContent(xx, yy+ys);
	      } else if (iter==2 && (yy-2)%4==2) {
		NextLimit = (MassLimit->GetBinContent(xx, yy+1)+MassLimit->GetBinContent(xx, yy-1))/2.;
		Next_hR_exp    = (hR_exp   ->GetBinContent(xx, yy+1)+hR_exp   ->GetBinContent(xx, yy-1))/2.;
		Next_hR_exp_up = (hR_exp_up->GetBinContent(xx, yy+1)+hR_exp_up->GetBinContent(xx, yy-1))/2.;
		Next_hR_exp_do = (hR_exp_do->GetBinContent(xx, yy+1)+hR_exp_do->GetBinContent(xx, yy-1))/2.;
		Next_hR_obs    = (hR_obs   ->GetBinContent(xx, yy+1)+hR_obs   ->GetBinContent(xx, yy-1))/2.;
		Next_hR_obs_up = (hR_obs_up->GetBinContent(xx, yy+1)+hR_obs_up->GetBinContent(xx, yy-1))/2.;
		Next_hR_obs_do = (hR_obs_do->GetBinContent(xx, yy+1)+hR_obs_do->GetBinContent(xx, yy-1))/2.;
	      }
	      
	      }*/

	    if (NextLimit<0.) {
	      //cout << "T2tt wrong limit " << XX << " " << YY << " " << XX-YY << endl; 
	      continue;
	    } else {
	    
	      GetSUSYCrossSection(1.*XX, "T2");
	      //NextXsec = CrossSection;

	      MassLimit->SetBinContent(xx, yy, NextLimit);
	      hXsec_the->SetBinContent(xx, yy, NextXsec);
	      hXsec_exp->SetBinContent(xx, yy, Next_hR_exp*NextXsec);
	      hXsec_obs->SetBinContent(xx, yy, Next_hR_obs*NextXsec);
	      hR_exp   ->SetBinContent(xx, yy, Next_hR_exp);
	      hR_exp_up->SetBinContent(xx, yy, Next_hR_exp_up);
	      hR_exp_do->SetBinContent(xx, yy, Next_hR_exp_do);
	      hR_obs   ->SetBinContent(xx, yy, Next_hR_obs);
	      hR_obs_up->SetBinContent(xx, yy, Next_hR_obs_up);
	      hR_obs_do->SetBinContent(xx, yy, Next_hR_obs_do);

	    }

	  }
	  
	}
	
      }

    }

  } else if (Signal.Contains("T2bW")) {

    for (int iter = 0; iter<2; iter++) {

      for (int yy = 1; yy<=MassLimit->GetNbinsY(); yy++) {

	if (MassLimit->GetYaxis()->GetBinCenter(yy)>651.) continue;
	
	int YY = MassLimit->GetYaxis()->GetBinCenter(yy);
	float rYY = MassLimit->GetYaxis()->GetBinCenter(yy);
	
	for (int xx = 1; xx<=MassLimit->GetNbinsX(); xx++) {
	  
	  int XX = MassLimit->GetXaxis()->GetBinCenter(xx);
	  float rXX = MassLimit->GetXaxis()->GetBinCenter(xx);

	  if (rXX-rYY<170.) continue;

	  if (MassLimit->GetBinContent(xx, yy)==0.) {
	    
	    float NextLimit = -1;
	    float Next_hR_exp, Next_hR_exp_up, Next_hR_exp_do;
	    float Next_hR_obs, Next_hR_obs_up, Next_hR_obs_do;

	    if (iter==0) {

	      if (MassLimit->GetBinContent(xx-1, yy)>0. && MassLimit->GetBinContent(xx+1, yy)>0.) {
		NextLimit      = (MassLimit->GetBinContent(xx-1, yy)+MassLimit->GetBinContent(xx+1, yy))/2.;
		Next_hR_exp    = (hR_exp   ->GetBinContent(xx-1, yy)+hR_exp   ->GetBinContent(xx+1, yy))/2.;
		Next_hR_exp_up = (hR_exp_up->GetBinContent(xx-1, yy)+hR_exp_up->GetBinContent(xx+1, yy))/2.;
		Next_hR_exp_do = (hR_exp_do->GetBinContent(xx-1, yy)+hR_exp_do->GetBinContent(xx+1, yy))/2.;
		Next_hR_obs    = (hR_obs   ->GetBinContent(xx-1, yy)+hR_obs   ->GetBinContent(xx+1, yy))/2.;
		Next_hR_obs_up = (hR_obs_up->GetBinContent(xx-1, yy)+hR_obs_up->GetBinContent(xx+1, yy))/2.;
		Next_hR_obs_do = (hR_obs_do->GetBinContent(xx-1, yy)+hR_obs_do->GetBinContent(xx+1, yy))/2.;
	      }

	    } else if (iter==1) {
	      
	      if (MassLimit->GetBinContent(xx-1, yy-1)>0. && MassLimit->GetBinContent(xx+1, yy+1)>0.) {
		NextLimit      = (MassLimit->GetBinContent(xx-1, yy-1)+MassLimit->GetBinContent(xx+1, yy+1))/2.;
		Next_hR_exp    = (hR_exp   ->GetBinContent(xx-1, yy-1)+hR_exp   ->GetBinContent(xx+1, yy+1))/2.;
		Next_hR_exp_up = (hR_exp_up->GetBinContent(xx-1, yy-1)+hR_exp_up->GetBinContent(xx+1, yy+1))/2.;
		Next_hR_exp_do = (hR_exp_do->GetBinContent(xx-1, yy-1)+hR_exp_do->GetBinContent(xx+1, yy+1))/2.;
		Next_hR_obs    = (hR_obs   ->GetBinContent(xx-1, yy-1)+hR_obs   ->GetBinContent(xx+1, yy+1))/2.;
		Next_hR_obs_up = (hR_obs_up->GetBinContent(xx-1, yy-1)+hR_obs_up->GetBinContent(xx+1, yy+1))/2.;
		Next_hR_obs_do = (hR_obs_do->GetBinContent(xx-1, yy-1)+hR_obs_do->GetBinContent(xx+1, yy+1))/2.;
	      } else {
		NextLimit      = (MassLimit->GetBinContent(xx, yy-1)+MassLimit->GetBinContent(xx, yy+1))/2.;
		Next_hR_exp    = (hR_exp   ->GetBinContent(xx, yy-1)+hR_exp   ->GetBinContent(xx, yy+1))/2.;
		Next_hR_exp_up = (hR_exp_up->GetBinContent(xx, yy-1)+hR_exp_up->GetBinContent(xx, yy+1))/2.;
		Next_hR_exp_do = (hR_exp_do->GetBinContent(xx, yy-1)+hR_exp_do->GetBinContent(xx, yy+1))/2.;
		Next_hR_obs    = (hR_obs   ->GetBinContent(xx, yy-1)+hR_obs   ->GetBinContent(xx, yy+1))/2.;
		Next_hR_obs_up = (hR_obs_up->GetBinContent(xx, yy-1)+hR_obs_up->GetBinContent(xx, yy+1))/2.;
		Next_hR_obs_do = (hR_obs_do->GetBinContent(xx, yy-1)+hR_obs_do->GetBinContent(xx, yy+1))/2.;
	      }
	      
	    }
	      
	    /*if (fabs(XX-YY-175)<15. &&
		(MassLimit->GetBinContent(xx, yy+1)>=1. || MassLimit->GetBinContent(xx, yy-1)>=1.) &&
		(MassLimit->GetBinContent(xx, yy+1)<1.  || MassLimit->GetBinContent(xx, yy-1)<1. )) {

	      

		}  
	    if (XX-YY>80. && XX-YY<305.) {
	    
	      if (MassLimit->GetBinContent(xx, yy+1)>0. && MassLimit->GetBinContent(xx, yy-1)>0.) {
		NextLimit = (MassLimit->GetBinContent(xx, yy+1)+MassLimit->GetBinContent(xx, yy-1))/2.;
		Next_hR_exp    = (hR_exp   ->GetBinContent(xx, yy+1)+hR_exp   ->GetBinContent(xx, yy-1))/2.;
		Next_hR_exp_up = (hR_exp_up->GetBinContent(xx, yy+1)+hR_exp_up->GetBinContent(xx, yy-1))/2.;
		Next_hR_exp_do = (hR_exp_do->GetBinContent(xx, yy+1)+hR_exp_do->GetBinContent(xx, yy-1))/2.;
		Next_hR_obs    = (hR_obs   ->GetBinContent(xx, yy+1)+hR_obs   ->GetBinContent(xx, yy-1))/2.;
		Next_hR_obs_up = (hR_obs_up->GetBinContent(xx, yy+1)+hR_obs_up->GetBinContent(xx, yy-1))/2.;
		Next_hR_obs_do = (hR_obs_do->GetBinContent(xx, yy+1)+hR_obs_do->GetBinContent(xx, yy-1))/2.;
	      }
	      
	    } else 
	      } else if (iter==1 && (yy-2)%2==1) {
		int ys = ((yy-2)%4==1) ? -1 : 1;
		NextLimit      = MassLimit->GetBinContent(xx, yy+ys);
		Next_hR_exp    = hR_exp   ->GetBinContent(xx, yy+ys);
		Next_hR_exp_up = hR_exp_up->GetBinContent(xx, yy+ys);
		Next_hR_exp_do = hR_exp_do->GetBinContent(xx, yy+ys);
		Next_hR_obs    = hR_obs   ->GetBinContent(xx, yy+ys);
		Next_hR_obs_up = hR_obs_up->GetBinContent(xx, yy+ys);
		Next_hR_obs_do = hR_obs_do->GetBinContent(xx, yy+ys);
	      } else if (iter==2 && (yy-2)%4==2) {
		NextLimit = (MassLimit->GetBinContent(xx, yy+1)+MassLimit->GetBinContent(xx, yy-1))/2.;
		Next_hR_exp    = (hR_exp   ->GetBinContent(xx, yy+1)+hR_exp   ->GetBinContent(xx, yy-1))/2.;
		Next_hR_exp_up = (hR_exp_up->GetBinContent(xx, yy+1)+hR_exp_up->GetBinContent(xx, yy-1))/2.;
		Next_hR_exp_do = (hR_exp_do->GetBinContent(xx, yy+1)+hR_exp_do->GetBinContent(xx, yy-1))/2.;
		Next_hR_obs    = (hR_obs   ->GetBinContent(xx, yy+1)+hR_obs   ->GetBinContent(xx, yy-1))/2.;
		Next_hR_obs_up = (hR_obs_up->GetBinContent(xx, yy+1)+hR_obs_up->GetBinContent(xx, yy-1))/2.;
		Next_hR_obs_do = (hR_obs_do->GetBinContent(xx, yy+1)+hR_obs_do->GetBinContent(xx, yy-1))/2.;
	      }
	      
	      }*/

	    if (NextLimit<0.) {
	      //cout << "T2tt wrong limit " << XX << " " << YY << " " << XX-YY << endl; 
	      continue;
	    } else {
	    
	      GetSUSYCrossSection(1.*XX, "T2");
	      
	      MassLimit->SetBinContent(xx, yy, NextLimit);
	      hXsec_exp->SetBinContent(xx, yy, Next_hR_exp*CrossSection);
	      hXsec_obs->SetBinContent(xx, yy, Next_hR_obs*CrossSection);
	      hXsec_the->SetBinContent(xx, yy, CrossSection);
	      hR_exp   ->SetBinContent(xx, yy, Next_hR_exp);
	      hR_exp_up->SetBinContent(xx, yy, Next_hR_exp_up);
	      hR_exp_do->SetBinContent(xx, yy, Next_hR_exp_do);
	      hR_obs   ->SetBinContent(xx, yy, Next_hR_obs);
	      hR_obs_up->SetBinContent(xx, yy, Next_hR_obs_up);
	      hR_obs_do->SetBinContent(xx, yy, Next_hR_obs_do);
	      
	    }

	  }
	  
	}
	
      }
      
    }

  }

  //hXsec_exp->SetMaximum(100.);
  //hR_exp_up->GetXaxis()->SetRangeUser(150,400);
  //hR_exp_up->GetYaxis()->SetRangeUser(  0,300);
  //hR_obs->Draw("text");
  //hXsec_exp->Draw("TEXTCOLZ");
  //MassLimit->GetXaxis()->SetRangeUser(150,500);
  //MassLimit->GetYaxis()->SetRangeUser(  0,400);
  //MassLimit->Draw("TEXTCOLZ");
  //hXsec_exp->SetMaximum(30.);
  //hXsec_exp->SetMinimum(1.);
  //hXsec_exp->Draw("TEXTCOLZ");
  
  TString OutputFileName = Version;
  if (Type!="") OutputFileName += "_" + Type;
  TFile *OutputFile = new TFile("RootFiles/" + OutputFileName + ".root", "recreate");	
  OutputFile->cd();
  
  bool doSmooth = true;
  if (doSmooth) {

    if (Signal.Contains("T2tt")) {
      for (int xx = 1; xx<=hXsec_exp->GetNbinsX(); xx++) {
	for (int yy = 1; yy<=hXsec_exp->GetNbinsY(); yy++) {
	  
	  float XX = hXsec_obs->GetXaxis()->GetBinCenter(xx);
	  float YY = hXsec_obs->GetYaxis()->GetBinCenter(yy);
	  if ((XX-YY)>80. && (XX-YY)<82. && (XX==456.25 || XX==481.25 || XX==531.25)) {
	    int xc = (int(hXsec_the->GetXaxis()->GetBinLowEdge(xx))%5==0) ? 0 : +1;
	    float myMass = hXsec_the->GetXaxis()->GetBinLowEdge(xx+xc);
	    GetSUSYCrossSection(myMass, "T2");
	    hXsec_obs->SetBinContent(xx, yy, hR_obs->GetBinContent(xx+1, yy)*CrossSection);
	  }
	}
      }
    }

    hXsec_exp->Smooth(1, "k3a");
    hXsec_obs->Smooth(1, "k3a");

    if (Signal.Contains("T2tt")) {
      hR_exp->Smooth(1, "k3a");
      hR_exp_up->Smooth(1, "k3a");
      hR_exp_do->Smooth(1, "k3a");
      hR_obs->Smooth(1, "K3a");
      hR_obs_up->Smooth(1, "k3a");
      //hR_obs_do->Smooth(1, "k3a");
    } 

    //hR_exp->Draw("TEXTCOLZ");
    
    for(int binx=1; binx<=hR_exp->GetNbinsX(); ++binx){
      double x = hR_exp->GetXaxis()->GetBinCenter(binx);
      for(int biny=1; biny<=hR_exp->GetNbinsY(); ++biny){
	double y = hR_exp->GetYaxis()->GetBinCenter(biny);
	if ( (Signal.Contains("T2tt") && fabs(x-y-80.+12.5)<10.) ||
	     (Signal.Contains("T2bW") && fabs(x-y-150.)<10.) ||
	     (Signal.Contains("TChiSlep") && (fabs(x-y-25.)<10. || y>420.)) ) {
	  //cout << x <<  " " << y << endl;
	  hXsec_exp->SetBinContent(hR_exp->GetBin(binx,biny), 0.);
	  hXsec_obs->SetBinContent(hR_exp->GetBin(binx,biny), 0.);
	  hR_exp   ->SetBinContent(hR_exp->GetBin(binx,biny), 0.);
	  hR_exp_up->SetBinContent(hR_exp->GetBin(binx,biny), 0.);
	  hR_exp_do->SetBinContent(hR_exp->GetBin(binx,biny), 0.);
	  hR_obs   ->SetBinContent(hR_exp->GetBin(binx,biny), 0.);
	  hR_obs_up->SetBinContent(hR_exp->GetBin(binx,biny), 0.);
	  hR_obs_do->SetBinContent(hR_exp->GetBin(binx,biny), 0.);
	} 
      }
    }

  }
  
  int U1[3] = {0, 0, 0};
  vector<double> vx, vy, vz, vzup, vzdo;
  for(int binx=1; binx<=hR_exp->GetNbinsX(); ++binx){
    double x = hR_exp->GetXaxis()->GetBinCenter(binx);
    for(int biny=1; biny<=hR_exp->GetNbinsY(); ++biny){
      double y = hR_exp->GetYaxis()->GetBinCenter(biny);
      vx.push_back(x);
      vy.push_back(y);
      double z = hR_exp->GetBinContent(hR_exp->GetBin(binx,biny)); 
      if (Signal=="_TChiSlep" && z==0. && hR_exp->GetBinContent(hR_exp->GetBin(binx-1,biny))<0.99 && hR_exp->GetBinContent(hR_exp->GetBin(binx-1,biny))>0.) z = 0.1;
      if (z==0.) z = 3.;
      vz.push_back(z);
      hR_exp->SetBinContent(hR_exp->GetBin(binx,biny), z); 
      if (z<1.) U1[0]++;
      z = hR_exp_up->GetBinContent(hR_exp_up->GetBin(binx,biny)); 
      if (Signal=="_TChiSlep" && z==0. && hR_exp_up->GetBinContent(hR_exp_up->GetBin(binx-1,biny))<0.99 && hR_exp_up->GetBinContent(hR_exp_up->GetBin(binx-1,biny))>0.) z = 0.1;
      if (z==0.) z = 3.;
      vzup.push_back(z);
      hR_exp_up->SetBinContent(hR_exp->GetBin(binx,biny), z); 
      if (z<1.) U1[1]++;
      z = hR_exp_do->GetBinContent(hR_exp_do->GetBin(binx,biny)); 
      if (Signal=="_TChiSlep" && z==0. && hR_exp_do->GetBinContent(hR_exp_do->GetBin(binx-1,biny))<0.99 && hR_exp_do->GetBinContent(hR_exp_do->GetBin(binx-1,biny))>0.) z = 0.1;
      if (z==0.) z = 3.;
      vzdo.push_back(z);
      hR_exp_do->SetBinContent(hR_exp->GetBin(binx,biny), z); 
      if (z<1.) U1[2]++;
    }
  }

  TGraph2D gsmooth("gsmooth", "", vx.size(), &vx.at(0), &vy.at(0), &vz.at(0));
  gsmooth.SetNpx(500);
  gsmooth.SetNpy(500);
  gsmooth.GetHistogram();
  TList *list = gsmooth.GetContourList(1.); 
  TIter liter(list);
  int max_points = 20, min_points = 20;
  for(int i = 0; i < list->GetSize(); ++i){
    TGraph *g = static_cast<TGraph*>(list->At(i));
    if(g == nullptr) continue;
    int n_points = g->GetN();
    cout<<"Exp:     Contour with "<<n_points<<" points "<<endl;
    //for (int pp = 0; pp<n_points; pp++){
    // double X,Y; g->GetPoint(pp, X, Y); 
    // cout << pp << " " << X << " "<< Y<<endl;
    //}
    if (n_points==23) continue;
    if(n_points > max_points && n_points >= min_points){
      //graph = g;
      cout << "DD"<<endl;
      g->SetName("gr_Exp");
      g->Write();
      //g->SetName("gr_ExpM");
      //g->Write();
      if (CentralQuantile!=-1) {
	g->SetName("gr_Obs");
	g->Write();
      }
      max_points = n_points;
    }
  }
  
  TGraph2D gsmoothup("gsmoothup", "", vx.size(), &vx.at(0), &vy.at(0), &vzup.at(0));
  gsmoothup.SetNpx(15.);
  gsmoothup.SetNpy(10.);
  gsmoothup.GetHistogram();
  if (U1[1]>0) {
    TList *listup = gsmoothup.GetContourList(1.); 
    TIter literup(listup);
    max_points = 20;
    for(int i = 0; i < listup->GetSize(); ++i){
      TGraph *g = static_cast<TGraph*>(listup->At(i));
      if(g == nullptr) continue;
      int n_points = g->GetN();
      cout<<"Exp up:   Contour with "<<n_points<<" points "<<endl;
      if(n_points > max_points && n_points >= min_points){
	//graph = g;
	g->SetName("gr_ExpP");
	g->Write();
	if (CentralQuantile!=-1) {
	  g->SetName("gr_ObsP");
	  g->Write();
	}
	max_points = n_points;
      }
    } 
  } else {
    TGraph *g = new TGraph();
    g->SetName("gr_ExpP");
    g->Write();
    if (CentralQuantile!=-1) {
      g->SetName("gr_ObsP");
      g->Write();
    }
  }

  TGraph2D gsmoothdo("gsmoothdo", "", vx.size(), &vx.at(0), &vy.at(0), &vzdo.at(0));
  gsmoothdo.SetNpx(500.);
  gsmoothdo.SetNpy(500.);
  gsmoothdo.GetHistogram();
  if (U1[2]>1) {
    TList *listdo = gsmoothdo.GetContourList(1.); 
    TIter literdo(listdo);
    max_points = 19;
    for(int i = 0; i < listdo->GetSize(); ++i){
      TGraph *g = static_cast<TGraph*>(listdo->At(i));
      if(g == nullptr) continue;
      int n_points = g->GetN();
      cout<<"Exp down: Contour with "<<n_points<<" points "<<endl;
      if(n_points > max_points && n_points >= min_points){
	//graph = g;
	g->SetName("gr_ExpM");
	g->Write();
	if (CentralQuantile!=-1) {
	  g->SetName("gr_ObsM");
	  g->Write();
	}
	max_points = n_points;
      }
    }
  } else {
    cout<<"Exp down: no contour" << endl;
    TGraph *g = new TGraph();
    g->SetName("gr_ExpM");
    g->Write();
    if (CentralQuantile!=-1) {
      g->SetName("gr_ObsM");
      g->Write();
    }
  }

  if (CentralQuantile==-1) {

    U1[0] = U1[1] = U1[2] = 0;
    vector<double> tx, ty, tz, tzup, tzdo;
    for(int binx=1; binx<=hR_obs->GetNbinsX(); ++binx){
      double x = hR_obs->GetXaxis()->GetBinCenter(binx);
      for(int biny=1; biny<=hR_obs->GetNbinsY(); ++biny){
	double y = hR_obs->GetYaxis()->GetBinCenter(biny);
	tx.push_back(x);
	ty.push_back(y);
	double z = hR_obs->GetBinContent(hR_obs->GetBin(binx,biny));
	if (z==0.) z = 2.;
	tz.push_back(z);
	if (z<1.) U1[0]++;
	z = hR_obs_up->GetBinContent(hR_obs_up->GetBin(binx,biny));
	if (z==0.) z = 2.;
	tzup.push_back(z);
	if (z<1.) U1[1]++;
	z = hR_obs_do->GetBinContent(hR_obs_do->GetBin(binx,biny));
	if (z==0.) z = 2.;
	tzdo.push_back(z);
	if (z<1.) U1[2]++;
      }
    }
    
    TGraph2D gsmooth_obs("gsmooth_obs", "", tx.size(), &tx.at(0), &ty.at(0), &tz.at(0));
    gsmooth_obs.SetNpx(15);
    gsmooth_obs.SetNpy(10);
    gsmooth_obs.GetHistogram();
    if (U1[0]>0) { cout << U1[0]<<endl;
      TList *list_obs = gsmooth_obs.GetContourList(1.); 
      TIter liter_obs(list_obs);
      max_points = 24;
      for(int i = 0; i < list_obs->GetSize(); ++i){
	TGraph *g = static_cast<TGraph*>(list_obs->At(i));
	if(g == nullptr) continue;
	int n_points = g->GetN();
	cout<<"Obs:      Contour with "<<n_points<<" points "<<endl;
	//for (int pp = 0; pp<n_points; pp++){
	// double X,Y; g->GetPoint(pp, X, Y); 
	// cout << pp << " " << X << " "<< Y<<endl;
	//}
	if(n_points > max_points && n_points >= min_points){
	  //graph = g;
	  g->SetName("gr_Obs");
	  g->Write();
	  max_points = n_points;
	}
      }
    } else {
      cout<<"Obs: no contour" << endl;
      TGraph *g = new TGraph();
      g->SetName("gr_Obs");
      g->Write();
    }
    
    TGraph2D gsmoothup_obs("gsmoothup_obs", "", tx.size(), &tx.at(0), &ty.at(0), &tzup.at(0));
    gsmoothup_obs.SetNpx(15.);
    gsmoothup_obs.SetNpy(10.);
    gsmoothup_obs.GetHistogram();
    if (U1[1]>0) {
      TList *listup_obs = gsmoothup_obs.GetContourList(1.); 
      TIter literup_obs(listup_obs);
      max_points = 24;
      for(int i = 0; i < listup_obs->GetSize(); ++i){
	TGraph *g = static_cast<TGraph*>(listup_obs->At(i));
	if(g == nullptr) continue;
	int n_points = g->GetN();
	cout<<"Obs up:   Contour with "<<n_points<<" points "<<endl;
	if(n_points > max_points && n_points >= min_points){
	  //graph = g;
	  g->SetName("gr_ObsP");
	  g->Write();
	  max_points = n_points;
	}
      } 
    } else {
      cout<<"Obs up: no contour" << endl;
      TGraph *g = new TGraph();
      g->SetName("gr_ObsP");
      g->Write();
    }

    TGraph2D gsmoothdo_obs("gsmoothdo_obs", "", tx.size(), &tx.at(0), &ty.at(0), &tzdo.at(0));
    gsmoothdo_obs.SetNpx(15.);
    gsmoothdo_obs.SetNpy(10.);
    gsmoothdo_obs.GetHistogram();
    if (U1[2]>0) {
      TList *listdo_obs = gsmoothdo_obs.GetContourList(1.); 
      TIter literdo_obs(listdo_obs);
      max_points = 24;
      for(int i = 0; i < listdo_obs->GetSize(); ++i){
	TGraph *g = static_cast<TGraph*>(listdo_obs->At(i));
	if(g == nullptr) continue;
	int n_points = g->GetN();
	cout<<"Obs down: Contour with "<<n_points<<" points "<<endl;
	if(n_points > max_points && n_points >= min_points){
	  //graph = g;
	  g->SetName("gr_ObsM");
	  g->Write();
	  max_points = n_points;
	}
      } 
    } else {
      cout<<"Obs down: no contour" << endl;
      TGraph *g = new TGraph();
      g->SetName("gr_ObsM");
      g->Write();
    }
    
  }

  bool xSecSC = false;
  if (xSecSC) {

    for (int xx = 1; xx<=hXsec_exp->GetNbinsX(); xx++) {
      for (int yy = 1; yy<=hXsec_exp->GetNbinsY(); yy++) {
	
	float XX = hXsec_obs->GetXaxis()->GetBinCenter(xx);
	float YY = hXsec_obs->GetYaxis()->GetBinCenter(yy);

	TString mySignal = Signal.Contains("T2") ? "T2" : "TChi";
	float myMass = XX; bool toR = false, testR = true;
	if (Signal.Contains("T2tt")) {
	  int xc = (int(hXsec_the->GetXaxis()->GetBinLowEdge(xx))%5==0) ? 0 : +1;
	  myMass = hXsec_the->GetXaxis()->GetBinLowEdge(xx+xc);
	  //if (XX-YY<82. && myMass!=425.) toR = false; // F
	  //if (XX-YY<82. && YY<460. && YY>370.) toR = true; //E 
	}
	GetSUSYCrossSection(myMass, mySignal);
	float myCrossSection =  CrossSection; // hXsec_the->GetBinContent(xx, yy);

	if (toR) {
	  hXsec_exp->SetBinContent(xx, yy, myCrossSection*hR_exp->GetBinContent(xx, yy));
	  hXsec_obs->SetBinContent(xx, yy, myCrossSection*hR_obs->GetBinContent(xx, yy));
	}
	if (testR) {
	  if (hXsec_obs->GetBinContent(xx, yy)/myCrossSection<1.) hXsec_obs->SetBinContent(xx, yy, 0.);
	  if (hXsec_exp->GetBinContent(xx, yy)/myCrossSection<1.) hXsec_exp->SetBinContent(xx, yy, 0.);
	}

      }
    }

  }

  if (CentralQuantile==-1) hXsec_obs->Write();
  hXsec_exp->Write();


  bool checkLimits = true;
  if (checkLimits) {
    for (int xx = 1; xx<=hXsec_exp->GetNbinsX(); xx++) {
      for (int yy = 1; yy<=hXsec_exp->GetNbinsY(); yy++) {
	if (hR_exp->GetBinContent(xx, yy)<1.) hR_exp->SetBinContent(xx, yy, 0.);
	if (hR_obs->GetBinContent(xx, yy)<1.) hR_obs->SetBinContent(xx, yy, 0.);
      }
    }
    hR_exp->Write();
    hR_obs->Write();
  }

  OutputFile->Close();
  
}

"""