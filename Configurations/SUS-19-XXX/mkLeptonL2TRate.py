#!/usr/bin/env python
import os
import sys
import ROOT
import math
import copy
import optparse
from array import *

years = sys.argv[1] if len(sys.argv)>=2 else '2016HIPM-2016noHIPM-2017-2018'

if len(sys.argv)==3:
    inoutflag = 'LeptonL2TRateJetHT' if len(sys.argv)==3 else ''
    pdcuts = [ 'JetHT#ElectronJet40', 'JetHT#ElectronJet80', 'JetHT#ElectronJet140', 'JetHT#ElectronJet200', 'JetHT#ElectronJet200', 'JetHT#ElectronJetXXX', 'JetHT#ElectronDiJet40', 'JetHT#ElectronDiJet80', 'JetHT#ElectronDiJetXX', 'JetHT#ElectronHT1050' ]
    muonpdcuts = []
    for pdcut in pdcuts:
        muonpdcuts.append(pdcut.replace('Electron', 'Muon'))
    pdcuts.extend(muonpdcuts)
else:
    inoutflag = 'TightLeptonL2TRate'
    pdcuts = [ 'SingleMuon#LowPt', 'SingleMuon#HighPt', 'SingleMuon#AllPt', 'SingleElectron#AllPt' ]

ptEdges = [20, 25, 30, 40, 50, 70, 100, 150, 200]
etaEdges = [0.,0.8,1.6,2.4]

def setHistoStyle(flavour, variable, histo):

    histo.SetTitle('')

    histo.GetXaxis().SetLabelFont(42)
    histo.GetXaxis().SetTitleFont(42)
    histo.GetXaxis().SetLabelSize(0.035)
    histo.GetXaxis().SetTitleSize(0.035)
    histo.GetXaxis().SetTitleOffset(1.2)
    histo.GetYaxis().SetLabelFont(42)
    histo.GetYaxis().SetTitleFont(42)
    histo.GetYaxis().SetLabelSize(0.035)

    if variable=='leppt': histo.SetXTitle(flavour.lower()+' p_{T} GeV')
    elif variable=='lepeta': histo.SetXTitle(flavour.lower()+' #eta')
    elif variable=='leppteta': histo.SetXTitle(flavour.lower()+' #eta:p_{T}')
    elif variable=='leppteta2D': 
        histo.SetXTitle(flavour.lower()+' p_{T} GeV')
        histo.SetYTitle(flavour.lower()+' #eta')

    histo.SetLineWidth(2)

if __name__ == '__main__':

    ROOT.gStyle.SetOptStat(ROOT.kFALSE)

    for year in years.split('-'):

        shapeDirectory = './Shapes/'+year+'/'+inoutflag+'/Samples/'

        plotDirectory = './Plots/'+year+'/'+inoutflag+'/'
        os.system('mkdir -p ' + plotDirectory + '; cp Plots/index.php ' + plotDirectory)

        outputRootFile = ROOT.TFile('./Data/'+year+'/'+inoutflag+'.root', 'recreate')

        for flvrange in pdcuts:

            if year=='2017' and 'DiJet' in flvrange: continue

            pdname = flvrange.split('#')[0]
            flavour = 'Electron' if 'Electron' in flvrange else 'Muon'
            flv = flvrange.replace('#', '')          

            dataFile  = ROOT.TFile(shapeDirectory+'plots_'+year+inoutflag+'_ALL_'+pdname+'.root', 'READ')
            dyFile    = ROOT.TFile(shapeDirectory+'plots_'+year+inoutflag+'_ALL_DY.root'               , 'READ') 
            wjetsFile = ROOT.TFile(shapeDirectory+'plots_'+year+inoutflag+'_ALL_WJetsToLNu.root'       , 'READ') 
            ttbarFile = ROOT.TFile(shapeDirectory+'plots_'+year+inoutflag+'_ALL_ttbar.root'            , 'READ')
 
            for variable in [ 'leppt', 'lepeta', 'leppteta' ]:

                dataShapes, ewkShapes, corrShapes = [], [], []

                for selection in  [ 'Loose', 'Tight' ]:

                    dataShape  = dataFile.Get(flv+selection+'/'+variable+'/histo_'+pdname)    ; dataShape.SetDirectory(0) ; setHistoStyle(flavour, variable, dataShape)
                    corrShape  = dataFile.Get(flv+selection+'/'+variable+'/histo_'+pdname)    ; corrShape.SetDirectory(0) ; setHistoStyle(flavour, variable, corrShape)
                    dyShape    = dyFile.Get(flv+selection+'/'+variable+'/histo_DY')           ; dyShape.SetDirectory(0)   ; setHistoStyle(flavour, variable, dyShape)
                    wjetsShape = wjetsFile.Get(flv+selection+'/'+variable+'/histo_WJetsToLNu'); wjetsShape.SetDirectory(0); setHistoStyle(flavour, variable, wjetsShape)  
                    ttbarShape = ttbarFile.Get(flv+selection+'/'+variable+'/histo_ttbar')     ; ttbarShape.SetDirectory(0); setHistoStyle(flavour, variable, ttbarShape)

                    dyShape.Add( wjetsShape )
                    dyShape.Add( ttbarShape )

                    dataShapes.append( dataShape )
                    ewkShapes.append( dyShape )
                    corrShape.Add(dyShape, -1.)
                    corrShapes.append( corrShape)
                     
                plotCanvas = ROOT.TCanvas( 'plotCanvas', '', 1200, 900)

                plotString = plotDirectory+flvrange.replace('#', '')+variable.replace('lep','_')

                dataShapes[0].Draw(); ewkShapes[0].SetLineColor(2); ewkShapes[0].Draw('same')
                plotCanvas.Print(plotString+'_Loose.png')

                dataShapes[1].Draw(); ewkShapes[1].SetLineColor(2); ewkShapes[1].Draw('same')
                plotCanvas.Print(plotString+'_Tight.png')

                dataShapes[1].Divide(dataShapes[0]); dataShapes[1].Draw();
                corrShapes[1].Divide(corrShapes[0]); corrShapes[1].SetLineColor(2); corrShapes[1].Draw('same');
                plotCanvas.Print(plotString+'_rate.png')

                if variable=='leppteta':

                    rate2D = ROOT.TH2F(flavour+'Loose2TightRate', '', len(ptEdges)-1, array('d',ptEdges), len(etaEdges)-1, array('d',etaEdges))
                    setHistoStyle(flavour, variable+'2D', rate2D)

                    for ptb in range(1, len(ptEdges)):
                        for etab in range(1, len(etaEdges)):
                            rate2D.SetBinContent(ptb+etab*(len(ptEdges)+1), corrShapes[1].GetBinContent(etab+(ptb-1)*(len(etaEdges)-1)))

                    NRGBs = 5
                    NCont = 255
                    stops = array("d",[0.00, 0.34, 0.61, 0.84, 1.00])
                    red = array("d",[0.50, 0.50, 1.00, 1.00, 1.00])
                    green = array("d",[ 0.50, 1.00, 1.00, 0.60, 0.50])
                    blue = array("d",[1.00, 1.00, 0.50, 0.40, 0.50])
                    ROOT.TColor.CreateGradientColorTable(NRGBs, stops, red, green, blue, NCont)
                    ROOT.gStyle.SetNumberContours(NCont)
                    ROOT.gStyle.SetPaintTextFormat("4.2f")

                    rate2D.Draw('textcolz')
                    plotCanvas.Print(plotString+'_rate2D.png')
                 
                    outputRootFile.cd()
                    rate2D.Write()
  
                plotCanvas.Close()  

          
