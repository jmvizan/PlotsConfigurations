#!/usr/bin/env python
import os
import sys
import ROOT
import math
import copy
import optparse
from array import *

if __name__ == '__main__':

    selectionFlag = 'MLLtag' #'3Lep'
    years = [ '2016HIPM', '2016noHIPM', '2017', '2018']
    #leptons = { '' : [ 'DATA', 'ttbar' ], 'Latino' : [ 'DATA' ], 'LatinoCut' : [ 'DATA' ] }
    #leptonWPs = { '' : [ 'MET', 'ttbar' ] }
    leptonWPs = { '' : [ 'MET' ] }
    if selectionFlag=='MLLtag':
        triggerCuts = { 'none', 'met', 'btag', 'veto' }
    else:
        triggerCuts = { 'none', 'met' }
    etaBins = { '_full' : '', '_cent' : ' && abs(Lepton_eta[0])<=1.2', '_forw' : ' && abs(Lepton_eta[0])>1.2 && abs(Lepton_eta[0])<=2.4' }
    fullTrigger = '(Trigger_dblEl || Trigger_dblMu || Trigger_ElMu  || Trigger_sngEl || Trigger_sngMu)'
    channels = [ 'ee', 'em', 'mm' ]
    triggerLevel = { 'MET' : [ 'double', 'both', 'full' ], 'ttbar' : [ 'eff' ] } 
    variables = { 'Leptonpt1pt2' : [20, 25, 30, 40, 50, 70, 100, 150, 200], 'Leptonpt1pt2bis' : [20, 30, 40, 60, 100, 160, 200] }

    if len(sys.argv)>1:
       years = sys.argv[1].split('-')
       if len(sys.argv)>2:
           channels = sys.argv[2].split('-')

    for year in years:

        outputDir = './Plots/'+year+'/Trigger'+selectionFlag+'/'
        os.system('mkdir -p '+outputDir)
        os.system('cp ./Plots/index.php '+outputDir)

        outputRootDir = './Data/'+year+'/'
        os.system('mkdir -p '+outputRootDir)
        outputRootFile = ROOT.TFile(outputRootDir+'TriggerEfficiencies_UL'+year+'_'+selectionFlag+'.root', 'recreate')

        for variable in variables:
            outputRootFile.mkdir(variable)
            for ch in channels:
                outputRootFile.mkdir(variable+'/'+ch)

        for leptonWP in leptonWPs: 

            for sample in leptonWPs[leptonWP]:

	        inputFileName = './Shapes/'+year+'/Trigger'+selectionFlag+leptonWP+'/Samples/plots_'+year+'Trigger'+selectionFlag+leptonWP+'_ALL_'+sample+'.root'
                if not os.path.isfile(inputFileName): continue
                inputFile = ROOT.TFile(inputFileName, 'READ')

                for ch in channels:
                    for etab in etaBins:
                        for cutt in triggerCuts:

                            denominatorName = ch+etab+'_'+cutt 

                            for trgbit in triggerLevel[sample]:

                                numeratorName = denominatorName + '_' + trgbit

                                for variable in variables:

                                    outputDirVar = outputDir+variable+'/'+ch+'/'
                                    os.system('mkdir -p '+outputDirVar)
                                    os.system('cp ./Plots/index.php '+outputDir+variable+'/')
                                    os.system('cp ./Plots/index.php '+outputDirVar)

                                    binsx = variables[variable]
                                    binsy = variables[variable]

                                    DEN = inputFile.Get(denominatorName+'/'+variable+'/histo_'+sample) 
                                    NUM = inputFile.Get(numeratorName  +'/'+variable+'/histo_'+sample)
     
                                    if len(binsx)==0:
                                        pass

                                    histoName = 'efficiency_' + leptonWP + '_' + year + '_' + sample + '_' + ch + etab + '_' + cutt + '_' + trgbit
                                    histoName = histoName.replace('__', '_')
                                    plotTitle = histoName.replace('_'+year, '').replace('_'+ch, '')

                                    EFF = ROOT.TH2F(histoName, '', len(binsx)-1, array('d',binsx), len(binsy)-1, array('d',binsy))     
                                    EFF.SetXTitle('Leading lepton p_{T}')
                                    EFF.SetYTitle('Trailing lepton p_{T}')

                                    for binx in range(1, EFF.GetNbinsX()+1):
                                        for biny in range(1, EFF.GetNbinsY()+1): 

                                            binf = EFF.GetNbinsY()*(binx - 1) + biny
                      
                                            den = DEN.GetBinContent(binf)
                                            num = NUM.GetBinContent(binf)  

                                            if den>0.:

                                                efficiency = num/den
                                                error = math.sqrt(efficiency*(1.-efficiency)/den)        

                                                EFF.SetBinContent(binx, biny, efficiency)
                                                EFF.SetBinError(binx, biny, error)

                                    # Draw comparison
                                    ROOT.gStyle.SetOptStat(ROOT.kFALSE)
                                    ROOT.gROOT.SetBatch(ROOT.kTRUE)

                                    NRGBs = 5
                                    NCont = 255
                                    stops = array("d",[0.00, 0.34, 0.61, 0.84, 1.00])
                                    red = array("d",[0.50, 0.50, 1.00, 1.00, 1.00])
                                    green = array("d",[ 0.50, 1.00, 1.00, 0.60, 0.50])
                                    blue = array("d",[1.00, 1.00, 0.50, 0.40, 0.50])
                                    ROOT.TColor.CreateGradientColorTable(NRGBs, stops, red, green, blue, NCont)
                                    ROOT.gStyle.SetNumberContours(NCont)

                                    plotCanvas = ROOT.TCanvas( 'plotCanvas', '', 1200, 900)
    
                                    EFF.GetXaxis().SetLabelFont(42)
                                    EFF.GetXaxis().SetTitleFont(42)
                                    EFF.GetXaxis().SetLabelSize(0.035)
                                    EFF.GetXaxis().SetTitleSize(0.035)
                                    EFF.GetXaxis().SetTitleOffset(1.2)
                                    EFF.GetYaxis().SetLabelFont(42)
                                    EFF.GetYaxis().SetTitleFont(42)
                                    EFF.GetYaxis().SetLabelSize(0.035)
                                    EFF.GetZaxis().SetTitleSize(0.035)
                                    EFF.GetZaxis().SetLabelFont(42)
                                    EFF.GetZaxis().SetTitleFont(42)
                                    EFF.GetZaxis().SetLabelSize(0.035)
                                    EFF.GetZaxis().SetTitleSize(0.035)

                                    EFF.SetMinimum(0.70)
                                    EFF.SetMaximum(1.00)

                                    drawPlotOption = 'textecolz'
                                    ROOT.gStyle.SetPaintTextFormat("1.3f")

                                    EFF.Draw(drawPlotOption)

                                    if leptonWP=='' and sample=='MET':
                                        outputRootFile.cd(variable+'/'+ch)
                                        EFF.Write(plotTitle)

                                    plotCanvas.Print(outputDirVar+plotTitle+'.png')
                                    plotCanvas.Print(outputDirVar+plotTitle+'.pdf')

                                    plotCanvas.Close()


