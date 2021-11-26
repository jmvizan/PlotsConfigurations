#!/usr/bin/env python
import os
import sys
import ROOT
import math
import copy
import optparse
from array import *

if __name__ == '__main__':

    years = [ '2016HIPM', '2016noHIPM', '2017', '2018']
    #leptons = { '' : [ 'DATA', 'ttbar' ], 'Latino' : [ 'DATA' ], 'LatinoCut' : [ 'DATA' ] }
    leptonWPs = { '' : [ 'MET' ] }
    triggerCuts = { 'none' : '', 'met' : ' && MET_pt>100.' }
    etaBins = { '_full' : '', '_cent' : ' && abs(Lepton_eta[0])<=1.2', '_forw' : ' && abs(Lepton_eta[0])>1.2 && abs(Lepton_eta[0])<=2.4' }
    fullTrigger = '(Trigger_dblEl || Trigger_dblMu || Trigger_ElMu  || Trigger_sngEl || Trigger_sngMu)'
    channels = { 'ee' : { 'double' : 'Trigger_dblEl', 'both' : '(Trigger_dblEl || Trigger_sngEl)'                 , 'full' : fullTrigger },
                 'mm' : { 'double' : 'Trigger_dblEl', 'both' : '(Trigger_dblMu || Trigger_sngMu)'                 , 'full' : fullTrigger },
                 'em' : { 'double' : 'Trigger_ElMu' , 'both' : '(Trigger_ElMu  || Trigger_sngEl || Trigger_sngMu)', 'full' : fullTrigger }
                }
    variables = { 'Leptonpt1pt2' : [20, 25, 30, 40, 50, 70, 100, 150, 200], 'Leptonpt1pt2bis' : [20, 30, 40, 60, 100, 160, 200] }

    for year in years:

        outputDir = './Plots/'+year+'/Trigger/'
        os.system('mkdir -p '+outputDir)
        os.system('cp ./Plots/index.php '+outputDir)

        EFFhistos = { }

        for leptonWP in leptonWPs: 

            for sample in leptonWPs[leptonWP]:

                inputFile = ROOT.TFile('./Shapes/'+year+'/Trigger'+leptonWP+'/Samples/plots_'+year+'Trigger'+leptonWP+'_ALL_'+sample+'.root', 'READ')

                for ch in channels:

                    outputDirChannel = outputDir+ch+'/'
                    os.system('mkdir -p '+outputDirChannel)
                    os.system('cp ./Plots/index.php '+outputDirChannel)

                    for etab in etaBins:
                        for cutt in triggerCuts:

                            denominatorName = ch+etab+'_'+cutt 

                            for trgbit in channels[ch]:

                                numeratorName = denominatorName + '_' + trgbit

                                for variable in variables:

                                    if variable not in EFFhistos:
                                        EFFhistos[variable] = { }
                                    if ch not in EFFhistos[variable]:
                                        EFFhistos[variable][ch] = [ ] 

                                    outputDirVar = outputDirChannel+variable+'/'
                                    os.system('mkdir -p '+outputDirVar)
                                    os.system('cp ./Plots/index.php '+outputDirVar)

                                    binsx = variables[variable]
                                    binsy = variables[variable]

                                    DEN = inputFile.Get(denominatorName+'/'+variable+'/histo_'+sample) 
                                    NUM = inputFile.Get(numeratorName  +'/'+variable+'/histo_'+sample)
     
                                    if len(binsx)==0:
                                        pass

                                    title = 'efficiency_' + year + '_' + leptonWP + '_' + sample + '_' + ch + etab + '_' + cutt + '_' + trgbit
                                    title = title.replace('__', '_')

                                    EFF = ROOT.TH2F(title, '', len(binsx)-1, array('d',binsx), len(binsy)-1, array('d',binsy))     
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

                                    plotCanvas.Print(outputDirVar+title+'.png')
                                    plotCanvas.Print(outputDirVar+title+'.pdf')

                                    plotCanvas.Close()
 
                                    EFFhistos[variable][ch].append(EFF)

                                    #if sample=='MET' and (leptonWP=='' or leptonWP=='Latino'): 
                                    #lpt = 'susy' if leptonWP=='' else leptonWP
                                    #if lpt not in EFFhistos: EFFhistos[lpt] = { }
                                    #EFFhistos[lpt][channel] = copy.deepcopy(EFF)

        # Save histogram file
        outputRootDir = './Data/'+year+'/'
        os.system('mkdir -p '+outputRootDir)
        outputRootFile = ROOT.TFile(outputRootDir+'TriggerEfficiencies_UL'+year+'.root', 'recreate')

        for variable in variables:
            outputRootFile.mkdir(variable)
            for ch in channels:
                outputRootFile.mkdir(variable+'/'+ch)
                outputRootFile.cd(variable+'/'+ch)
                for histo in EFFhistos[variable][ch]:
                    histo.Write()

"""
        for channel in channels:

            EFFhistos['susy'][channel].Divide(EFFhistos['Latino'][channel])

            ROOT.gStyle.SetPaintTextFormat("1.3f")
            sfCanvas = ROOT.TCanvas( 'sfCanvas', '', 1200, 900)

            EFFhistos['susy'][channel].Draw('textcolz')

            title = 'scalefactors_' + year + '_' + channel
            sfCanvas.Print(outputDir+title+'.png')
            sfCanvas.Print(outputDir+title+'.pdf')
"""

