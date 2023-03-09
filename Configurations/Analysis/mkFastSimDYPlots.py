#!/usr/bin/env python
import os
import sys
import ROOT
import math
import optparse
from array import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 

def getLeptonMass(pdgId) :
    
        if abs(pdgId)==11 :
            return 0.000511
        elif abs(pdgId)==13 :
            return 0.105658
        else :
            print 'mt2llProducer: WARNING: unsupported lepton pdgId'
            return -1

Zmass = 91.1876

yearset=sys.argv[1]

if __name__ == '__main__':

    sims = [ 'fastsim', 'fullsim' ]
    leptons = [ 'Ele', 'Muo' ]

    for year in yearset.split('-'):

        histos = { }
        for sim in sims:

            histos[sim] = { }

            inputFile = ROOT.TFile.Open('./Data/'+year+'/'+'Histos_'+sim+'.root', 'read')  

            for key in inputFile.GetListOfKeys():

                histo = key.ReadObj()
                if histo.ClassName()=='TH2F':

                    histo.SetDirectory(0)
                    histoName = histo.GetName().split('_')

                    if histoName[0] not in histos[sim]: histos[sim][histoName[0]] = { } 
                    histos[sim][histoName[0]][histoName[1]] = histo

            inputFile.Close()

        outputDir = './Plots/'+year+'/FastSim/'
        os.system('mkdir -p '+outputDir)

        for lepton in leptons:
            
            for sim in sims:

                histos[sim][lepton]['tight'].Divide(histos[sim][lepton]['reco'])

                if 'gen' in histos[sim][lepton]:
                    histos[sim][lepton]['tightgen'].Divide(histos[sim][lepton]['gen'])
                    histos[sim][lepton]['recogen'].Divide(histos[sim][lepton]['gen']) 

            histos['fullsim'][lepton]['tight'].Divide(histos['fastsim'][lepton]['tight'])

            plotLevels = [ 'tight' ]

            if 'gen' in histos['fullsim'][lepton] and 'gen' in histos['fastsim'][lepton]:
                histos['fullsim'][lepton]['tightgen'].Divide(histos['fastsim'][lepton]['tightgen'])
                histos['fullsim'][lepton]['recogen'].Divide(histos['fastsim'][lepton]['recogen'])
                plotLevels.append('tightgen')
                plotLevels.append('recogen')

            for level in plotLevels:

                ROOT.gStyle.SetOptStat(ROOT.kFALSE)
                ROOT.gROOT.SetBatch(ROOT.kTRUE)

                plotCanvas = ROOT.TCanvas( 'plotCanvas', '', 1200, 900)
                plotCanvas.Divide(1, 1)

                gPad = plotCanvas.GetPad(1)
                gPad.cd()

                if lepton=='Ele':
                    gPad.SetLogy(1)
                    gPad.SetLogx(0)   
                else:
                    gPad.SetLogx(1)
                    gPad.SetLogy(0)

                histos['fullsim'][lepton][level].GetXaxis().SetLabelFont(42)
                histos['fullsim'][lepton][level].GetXaxis().SetTitleFont(42)
                histos['fullsim'][lepton][level].GetXaxis().SetLabelSize(0.035)
                histos['fullsim'][lepton][level].GetXaxis().SetTitleSize(0.035)
                histos['fullsim'][lepton][level].GetXaxis().SetTitleOffset(1.2)
                histos['fullsim'][lepton][level].GetYaxis().SetLabelFont(42)
                histos['fullsim'][lepton][level].GetYaxis().SetTitleFont(42)
                histos['fullsim'][lepton][level].GetYaxis().SetLabelSize(0.035)
                histos['fullsim'][lepton][level].GetZaxis().SetTitleSize(0.035)
                histos['fullsim'][lepton][level].GetZaxis().SetLabelFont(42)
                histos['fullsim'][lepton][level].GetZaxis().SetTitleFont(42)
                histos['fullsim'][lepton][level].GetZaxis().SetLabelSize(0.035)
                histos['fullsim'][lepton][level].GetZaxis().SetTitleSize(0.035)

                if lepton=='Ele':
                    histos['fullsim'][lepton][level].SetXTitle('super-cluster #eta')
                    histos['fullsim'][lepton][level].SetYTitle('Electron p_{T} [GeV]')
                    histos['fullsim'][lepton][level].GetYaxis().SetNoExponent()
                    histos['fullsim'][lepton][level].GetYaxis().SetMoreLogLabels()
                else:
                    histos['fullsim'][lepton][level].SetXTitle('Muon p_{T} [GeV]')
                    histos['fullsim'][lepton][level].SetYTitle('Muon |#eta|')
                    histos['fullsim'][lepton][level].GetXaxis().SetNoExponent()
                    histos['fullsim'][lepton][level].GetXaxis().SetMoreLogLabels() 
                histos['fullsim'][lepton][level].SetZTitle('Fullsim/FastSim SF')

                NRGBs = 5
                NCont = 255
                stops = array("d",[0.00, 0.34, 0.61, 0.84, 1.00])
                red = array("d",[0.50, 0.50, 1.00, 1.00, 1.00])
                green = array("d",[ 0.50, 1.00, 1.00, 0.60, 0.50])
                blue = array("d",[1.00, 1.00, 0.50, 0.40, 0.50])
                ROOT.TColor.CreateGradientColorTable(NRGBs, stops, red, green, blue, NCont)
                ROOT.gStyle.SetNumberContours(NCont)

                histos['fullsim'][lepton][level].SetMinimum(0.8)
                histos['fullsim'][lepton][level].SetMaximum(1.1)

                drawPlotOption = 'textcolz'
                ROOT.gStyle.SetPaintTextFormat("1.3f")

                histos['fullsim'][lepton][level].Draw(drawPlotOption)

                title = lepton + '_' + year + '_' + level
                plotCanvas.Print(outputDir+title+'.png')
                plotCanvas.Print(outputDir+title+'.pdf')

                plotCanvas.Close()

        #ff = ROOT.TFile.Open('./Data/'+year+'/fastsimLeptonWeights.root', 'recreate')

        #for lepton in leptons:
        #    histos['fullsim'][lepton]['tight'].Write()

        #ff.Close()


