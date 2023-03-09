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

def mkDivide(histo1, histo2, kind) :

    #histo1.Divide(histo2)
    for xb in range(1, histo1.GetXaxis().GetNbins()+1):
        for yb in range(1, histo1.GetYaxis().GetNbins()+1):  

            cont2 = histo2.GetBinContent(xb, yb)
            if cont2>0.:

                cont1 = histo1.GetBinContent(xb, yb)
                ratio = cont1/cont2

                if kind=='eff':
                    error = math.sqrt(ratio*(1.-ratio)/cont2)
                else:
                    error1 = histo1.GetBinError(xb, yb)
                    error2 = histo2.GetBinError(xb, yb)
                    error = ratio*math.sqrt(math.pow(error1/cont1, 2) + math.pow(error2/cont2, 2))

                histo1.SetBinContent(xb, yb, ratio)
                histo1.SetBinError(xb, yb, error)

def mkPlot(histo, lepton, year, level, sim) :

    ROOT.gStyle.SetOptStat(ROOT.kFALSE)
    ROOT.gROOT.SetBatch(ROOT.kTRUE)

    plotCanvas = ROOT.TCanvas( 'plotCanvas', '', 1200, 900)
    plotCanvas.Divide(1, 1)

    gPad = plotCanvas.GetPad(1)
    gPad.cd()

    gPad.SetRightMargin(0.15)

    if lepton=='Ele':
        gPad.SetLogy(1)
        gPad.SetLogx(0)   
    else:
        gPad.SetLogx(1)
        gPad.SetLogy(0)

    histo.GetXaxis().SetLabelFont(42)
    histo.GetXaxis().SetTitleFont(42)
    histo.GetXaxis().SetLabelSize(0.035)
    histo.GetXaxis().SetTitleSize(0.035)
    histo.GetXaxis().SetTitleOffset(1.2)
    histo.GetYaxis().SetLabelFont(42)
    histo.GetYaxis().SetTitleFont(42)
    histo.GetYaxis().SetLabelSize(0.035)
    histo.GetZaxis().SetTitleSize(0.035)
    histo.GetZaxis().SetLabelFont(42)
    histo.GetZaxis().SetTitleFont(42)
    histo.GetZaxis().SetLabelSize(0.035)
    histo.GetZaxis().SetTitleSize(0.035)
    histo.GetZaxis().SetTitleOffset(1.2)

    if lepton=='Ele':
        histo.SetXTitle('super-cluster #eta')
        histo.SetYTitle('Electron p_{T} [GeV]')
        histo.GetYaxis().SetNoExponent()
        histo.GetYaxis().SetMoreLogLabels()
    else:
        histo.SetXTitle('Muon p_{T} [GeV]')
        histo.SetYTitle('Muon |#eta|')
        histo.GetXaxis().SetNoExponent()
        histo.GetXaxis().SetMoreLogLabels()

    if sim=='': 
        histo.SetZTitle('FullSim/FastSim SF')
    else:
        histo.SetZTitle(sim.replace('f', 'F').replace('sim', 'Sim')+' Efficiency')

    NRGBs = 5
    NCont = 255
    stops = array("d",[0.00, 0.34, 0.61, 0.84, 1.00])
    red = array("d",[0.50, 0.50, 1.00, 1.00, 1.00])
    green = array("d",[ 0.50, 1.00, 1.00, 0.60, 0.50])
    blue = array("d",[1.00, 1.00, 0.50, 0.40, 0.50])
    ROOT.TColor.CreateGradientColorTable(NRGBs, stops, red, green, blue, NCont)
    ROOT.gStyle.SetNumberContours(NCont)

    minimum = 0.75 if sim=='' else 0.3
    histo.SetMinimum(minimum)
    histo.SetMaximum(1.10)

    drawPlotOption = 'textecolz'
    ROOT.gStyle.SetPaintTextFormat("1.3f")

    histo.Draw(drawPlotOption)

    title = lepton + '_' + year + '_' + level
    if sim!='':
        title += '_' + sim
    plotCanvas.Print(outputDir+title+'.png')
    plotCanvas.Print(outputDir+title+'.pdf')

    plotCanvas.Close()

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

                #histos[sim][lepton]['tight'].Divide(histos[sim][lepton]['reco'])
                mkDivide(histos[sim][lepton]['tight'], histos[sim][lepton]['reco'], 'eff')
                mkPlot(histos[sim][lepton]['tight'], lepton, year, 'tight', sim)

                if 'gen' in histos[sim][lepton]:
                    histos[sim][lepton]['tightgen'].Divide(histos[sim][lepton]['gen'])
                    histos[sim][lepton]['recogen'].Divide(histos[sim][lepton]['gen']) 

            mkDivide(histos['fullsim'][lepton]['tight'], histos['fastsim'][lepton]['tight'], 'sf')

            plotLevels = [ 'tight' ]

            if 'gen' in histos['fullsim'][lepton] and 'gen' in histos['fastsim'][lepton]:
                histos['fullsim'][lepton]['tightgen'].Divide(histos['fastsim'][lepton]['tightgen'])
                histos['fullsim'][lepton]['recogen'].Divide(histos['fastsim'][lepton]['recogen'])
                plotLevels.append('tightgen')
                plotLevels.append('recogen')

            for level in plotLevels:
                mkPlot(histos['fullsim'][lepton][level], lepton, year, level, '')

        #ff = ROOT.TFile.Open('./Data/'+year+'/fastsimLeptonWeights.root', 'recreate')

        #for lepton in leptons:
        #    histos['fullsim'][lepton]['tight'].Write()

        #ff.Close()


