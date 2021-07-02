#!/usr/bin/env python
import os, sys, optparse
from ROOT import *# TH1D, TH2D, TFile, TTree, TCanvas, gROOT, gStyle, gSystem
import numpy as np

gROOT.SetBatch(True)
c1 = TCanvas( 'c1', 'Dynamic Filling Example', 200,10, 1600, 1200 )
c1.SetLeftMargin(0.12)

EOYArea = "../../../../../CMSSW_10_2_14/src/PlotsConfigurations/Configurations/SUS-19-XXX/"

#Scale histograms                                                                                   
def ScaleToInt(histo):
    norm  = histo.GetSumOfWeights()
    histo.Scale(1/norm)
    return histo

def GetRanges(histo1, histo2, isLog=False):
    maxVal = max(histo1.GetMaximum(), histo2.GetMaximum())
    minVal = min(histo1.GetMinimum(1e-8), histo2.GetMinimum(1e-8))
    multip = 1.05
    if isLog: multip =1.2
    histo1.GetYaxis().SetRangeUser(minVal,multip*maxVal)

def fileismissing(filenm):
    skip = False
    if os.path.isfile(filenm) is False:
        print "\nFILE MISSING: "+filenm+"\n"
        skip = True
    return skip

usage  = 'usage: %prog [options]'
parser = optparse.OptionParser(usage)
parser.add_option('-t', '--test'     , dest = 'test'     , help = 'Just some plots  ', default = False, action = 'store_true')
(opt, args) = parser.parse_args()

if len(sys.argv)<4:
  print 'Please, specify year, tag and process to plot'
  sys.exit()
    
years=sys.argv[1]
tags=sys.argv[2]
processes=sys.argv[3]

yearlist = years.split('-')
taglist = tags.split('-')
processlist = processes.split('-')

if 'WWW' in os.environ:
  web = os.environ["WWW"]
else:
  web = './Plots/'
compweb = web+"CompareToEOY/"
os.system("mkdir -p " + compweb)

doTest  = opt.test
sameFolder = False
if "pmatorra" in  os.getenv('USER'): sameFolder = True

for year in yearlist:
  for tag in taglist:
    opt.tag = year + tag
    for process in processlist:
      process = process.replace('Data', 'DATA')
      opt.sigset = 'Data' if process=='DATA' else 'Backgrounds'+process
      
      #Generate dictionaries with variables and cuts
      variables = {}
      samples   = {}
      cuts      = {} 
      exec(open('samples_nanoAODv8.py').read())
      exec(open('variables.py').read())
      exec(open('cuts.py').read())

      try:
        os
      except NameError:
        import os

      
      #if "Control" not in tag: continue
      #tweaks         = all_info[tag]["tweaks"]
      #for tweak in tweaks:
      #variables      = all_info[tag]["variables"]
      #ControlRegions = all_info[tag]["ControlRegions"]
      ControlRegions = cuts.keys()
      #if "VetoNoiseEE" in tweak :
      #    ControlRegions += extraCRs
      #    variables       = VetoNoiseEEvars
      #for year in all_info[tag]["years"]:
      #hfileV8nm  = "Data/plots_"+year+tag+tweak+"V8_ALL_DATA.root"
      #hfileV6nm  = "Data/plots_"+year+tag+tweak+"V6_ALL_DATA.root"
      if sameFolder is True :
          hfileV8nm  = "Shapes/"+year+"/"+tag+"_V8/Samples/plots_"+year+tag+"_V8_ALL_"+process+".root"
          hfileV6nm  = "Shapes/"+year+"/"+tag+"_V6/Samples/plots_"+year+tag+"_V6_ALL_"+process+".root"
      else:
          hfileV8nm  = "Shapes/"+year+"/"+tag+"/Samples/plots_"+year+tag+"_ALL_"+process+".root"
          hfileV6nm  = EOYArea + hfileV8nm
      #missV8     = fileismissing(hfileV8nm)
      #missV6     = fileismissing(hfileV6nm)
      #if missV8 or missV6: continue
      hfileV8 = TFile(hfileV8nm)
      hfileV6 = TFile(hfileV6nm)
      for region in ControlRegions:
        #folloc  = year+"/"+tag+"/"+tweak+"/"+region+"/"
        folloc  = year+"/"+tag+"/"+region+"/"+process+"/"
        #thisfol = "Figures/"+folloc
        webloc  = compweb+folloc
        os.system("mkdir -p " + webloc)
        otherfol = ''
        for folsplit in folloc.split('/'):
          otherfol += folsplit+'/'
          if folsplit =='': continue
          os.system('cp '+web+'index.php ' + compweb+otherfol)
        nplots  = 0
        for var in variables:
          if nplots>0 and doTest: continue
          cr_i  = hfileV8.cd(region)
          var_i = gDirectory.cd(var)
          if cr_i is False:
            print "something's wrong with", year+tag, "region", region
            exit()
            continue
          if var_i is False:
            print "something's wrong with", region
            continue
          doLogY  = False
          doLogX  = False
          if "ptll+" in var:
            doLogY = True
            doLogX = True
          figbase = tag+"_"+year+"_"+region+"_"+var
          #os.system("mkdir -p "+thisfol)
          legend  = TLegend(0.6,0.8,0.88,0.88);
          histoV8 = hfileV8.Get(region+"/"+var+"/histo_"+process)
          histoV6 = hfileV6.Get(region+"/"+var+"/histo_"+process)
          legend.AddEntry(histoV8, region+"V8     " )
          legend.AddEntry(histoV6, region+"V6loose" )
          histoV6.SetTitle(region+"-"+var+" "+year)
          histoV6.GetXaxis().SetTitle(var)
          histoV6.GetYaxis().SetTitle("Events")
          gPad.SetLogy(doLogY)
          GetRanges(histoV6, histoV8)
          if "ptll" in var: histoV6.GetXaxis().SetRangeUser(0,500)
          histoV6.SetStats(False)
          histoV6.Draw()
          histoV8.Draw("Same")
          histoV8.SetLineWidth(0)
          histoV8.SetMarkerStyle(3)
          histoV8.SetMarkerSize(2)
          histoV8.SetMarkerColor(2)
          legend.Draw()
          histoV8.SetLineColor(2)

          nV6 = histoV6.GetSumOfWeights()
          nV6i = histoV6.GetEntries()
          nV8 = histoV8.GetSumOfWeights()
          #print nV6, nV6i
          c1.SaveAs(webloc+figbase+".png")

          gPad.SetLogy(True)
          GetRanges(histoV6,histoV8, True)
          histoV6.Draw()
          histoV8.Draw("Same")
          c1.SaveAs(webloc+"log_"+figbase+".png")

          gPad.SetLogy(False)
          histoV6Norm = ScaleToInt(histoV6)
          histoV8Norm = ScaleToInt(histoV8)
          histoV6Norm.Draw("")
          histoV6Norm.GetYaxis().SetTitle("Norm. Events")
          histoV8Norm.Draw("Same")
          legend.Draw()
          GetRanges(histoV6Norm, histoV8Norm, doLogY)
          c1.SaveAs(webloc+"scaled_"+figbase+".png")

          gPad.SetLogy(True)
          histoV6Norm.Draw()
          histoV8Norm.Draw("Same")
          legend.Draw()
          GetRanges(histoV6Norm, histoV8Norm, True)
          c1.SaveAs(webloc+"log_scaled_"+figbase+".png")

          nplots+=1


