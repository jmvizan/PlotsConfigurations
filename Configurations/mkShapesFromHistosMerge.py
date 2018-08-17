#!/usr/bin/env python

import json
import sys
import ROOT
import optparse
import LatinoAnalysis.Gardener.hwwtools as hwwtools
import logging
import os.path
import math

# ----------------------------------------------------- ShapeFactory --------------------------------------

class ShapeFactory:
    _logger = logging.getLogger('ShapeFactory')

    # _____________________________________________________________________________
    def __init__(self):
      
        variables = {}
        self._variables = variables

        cuts = {}
        self._cuts = cuts

        samples = {}
        self._samples = samples
        ## list of [processes]  
        self.processes = []
        ## list of [signal processes]
        self.signals = []
        ## list of [background processes]
        self.backgrounds = []
        ## data
        self.data = []        
        ## list of [(name of uncert, type of nuisance, list of samples affected, with value, additional value [in case of gmN])]
        self.systs   = []

    # _____________________________________________________________________________
    # 
    # _____________________________________________________________________________
    def makeShapesFromHistos( self, inputDir, outputDir, outputFileName, analysisName, lumi, variables, cuts, samples, structureFile, nuisances, signalPoint, fastsimMet):
    
        print "=============================="
        print "==== makeShapesFromHistos ===="
        print "=============================="
        
        self._variables = variables
        self._samples   = samples
        self._cuts      = cuts

        self._inputDir  = inputDir
        self._outputDir = outputDir

        self._fastsimMet = fastsimMet

        #self._fileIn = ROOT.TFile(inputFile, "READ")
        
        # divide the list of samples among signal, background and data
        for sampleName, sample in self._samples.iteritems():
          if structureFile[sampleName]['isSignal'] == 1 :
            self.signals.append(sampleName)
          if structureFile[sampleName]['isData'] == 1 :
            self.data.append(sampleName)
          if structureFile[sampleName]['isSignal'] == 0 and structureFile[sampleName]['isData'] == 0:
            self.backgrounds.append(sampleName)
          
        if not os.path.isdir (self._outputDir + "/") :
          os.mkdir (self._outputDir + "/")
          
        self._outFile = ROOT.TFile.Open( self._outputDir + "/" + outputFileName + signalPoint + ".root", 'recreate')
        ROOT.TH1.SetDefaultSumw2(True)
        
        # loop over cuts  
        for cutName in self._cuts :

          print "cut = ", cutName, " :: ", cuts[cutName]

          self._outFile.mkdir (cutName)

          # loop over variables
          for variableName, variable in self._variables.iteritems():

            cutNameSplit = cutName.split('_')
            print analysisName + "/" + cutNameSplit[0] + '_' + cutNameSplit[1] + '/h_' + variableName + '_' + cutNameSplit[2]
            shapeName = analysisName + "/02_" + cutNameSplit[0] + '_' + cutNameSplit[1] + '/h_' + variableName + '_' + cutNameSplit[2]
            shapeNameGen = analysisName + "/02_" + cutNameSplit[0] + 'gen_' + cutNameSplit[1] + '/h_' + variableName + 'gen_' + cutNameSplit[2]

            print "  variableName = ", variableName
            tagNameToAppearInDatacard = cutName
            self._outFile.mkdir (cutName + "/" + variableName)
           
            for sampleName in self.signals:
              inputFile = inputDir.replace("NoTopPt", "Oct17") + '/nominal/' + analysisName + '/' + sampleName + signalPoint + '.root'
              fileIn = ROOT.TFile(inputFile, "READ")
              histo = self._getFastSimShape(fileIn, shapeName, shapeNameGen, lumi)
              histo.SetName('histo_' + sampleName)
              self._outFile.cd(cutName + "/" + variableName)
              histo.Write()
              fileIn.Close()
              
            for sampleName in self.backgrounds:
              inputFile = inputDir + '/nominal/' + analysisName + '/' + sampleName + '.root'
              fileIn = ROOT.TFile(inputFile, "READ")
              #shapeName = analysisName + "/" + cutName + '/h_' + variableName
              histo = self._getShape(fileIn, sampleName, shapeName, lumi)
              histo.SetName('histo_' + sampleName)
              self._outFile.cd(cutName + "/" + variableName)
              histo.Write()
              fileIn.Close()
            
            for sampleName in self.data:
              inputFile = inputDir + '/nominal/' + analysisName + '/' + sampleName + '.root'
              fileIn = ROOT.TFile(inputFile, "READ")
              #shapeName = analysisName + "/" + cutName + '/h_' + variableName
              histo = self._getShape(fileIn, sampleName, shapeName, -999.)
              histo.SetName('histo_' + sampleName)
              if (sampleName != "01_Data") : # for psuedo data
                  histo.Scale(lumi)
                  nBins = histo.GetNbinsX()
                  for iBin in range(1, nBins+1):
                      yValue = histo.GetBinContent(iBin)
                      histo.SetBinError(iBin, math.sqrt(abs(yValue)))
              self._outFile.cd(cutName + "/" + variableName)
              histo.Write()
              fileIn.Close()
                                     
            # Now make nuisances
            for nuisanceName, nuisance in nuisances.iteritems():
              
              # check if a nuisance can be skipped because not in this particular cut
              use_this_nuisance = False
              if  'cuts' in nuisance.keys() :
                for Cuts_where_to_use_nuisance  in   nuisance['cuts'] :  
                  #if Cuts_where_to_use_nuisance == cutName :
                  if Cuts_where_to_use_nuisance in cutName :
                    # use this niusance
                    use_this_nuisance = True
              else :
                # default is use the nuisance everywhere
                use_this_nuisance = True 
              
              if use_this_nuisance :
               
                if (nuisanceName != 'stat' and nuisanceName != 'Metfastsim' and 'MT2llBin' not in nuisanceName): # 'stat' has a separate treatment, it's the MC/data statistics
                  
                  if 'type' in nuisance.keys() : # some nuisances may not have "type" ... why?
                    print "nuisance[type] = ", nuisance ['type']," ","nuisance[name] = ", nuisance ['name']
                    if (nuisance ['type'] == 'shape' or nuisance ['type'] == 'shapeN') :
                        if 'all' in nuisance.keys() and nuisance ['all'] == 1 : # for all samples
                            print 'what about the shapes?'
                        else :
                            # apply only to selected samples
                            for sampleName in self.signals:
                                if sampleName in nuisance['samples'].keys() :
                                    # save the nuisance histograms in the root file
                                    inputFile = inputDir.replace("NoTopPt", "Oct17") + '/' + nuisance['name'] + 'up/' + analysisName + '/' + sampleName + signalPoint + '.root'
                                    fileInUp = ROOT.TFile(inputFile, "READ")
                                    histo = self._getFastSimShape(fileInUp, shapeName, shapeNameGen, lumi)
                                    histo.SetName('histo_' + sampleName + '_' + (nuisance['name']) + "Up")
                                    self._outFile.cd(cutName + "/" + variableName)
                                    histo.Write()
                                    fileInUp.Close()
                                    inputFile = inputDir.replace("NoTopPt", "Oct17") + '/' + nuisance['name'] + 'do/' + analysisName + '/' + sampleName + signalPoint + '.root'
                                    fileInDo = ROOT.TFile(inputFile, "READ")
                                    histo = self._getFastSimShape(fileInDo, shapeName, shapeNameGen, lumi)
                                    histo.SetName('histo_' + sampleName + '_' + (nuisance['name']) + "Down")
                                    self._outFile.cd(cutName + "/" + variableName)
                                    histo.Write()
                                    fileInDo.Close()
                                    
                            for sampleName in self.backgrounds:
                                if sampleName in nuisance['samples'].keys() :
                                    # save the nuisance histograms in the root file
                                    inputFile = inputDir + '/' + nuisance['name'] + 'up/' + analysisName + '/' + sampleName + '.root'
                                    fileInUp = ROOT.TFile(inputFile, "READ")                            
                                    histo = self._getShape(fileInUp, sampleName, shapeName, lumi)
                                    histo.SetName('histo_' + sampleName + '_' + (nuisance['name']) + "Up")
                                    self._outFile.cd(cutName + "/" + variableName)
                                    histo.Write()
                                    fileInUp.Close()
                                    inputFile = inputDir + '/' + nuisance['name'] + 'do/' + analysisName + '/' + sampleName + '.root'
                                    fileInDo = ROOT.TFile(inputFile, "READ")
                                    histo = self._getShape(fileInDo, sampleName, shapeName, lumi)
                                    histo.SetName('histo_' + sampleName + '_' + (nuisance['name']) + "Down")
                                    self._outFile.cd(cutName + "/" + variableName)
                                    histo.Write()
                                    fileInDo.Close()

                # MT2ll bin nuisances
                if 'MT2llBin' in nuisanceName:

                    print "nuisance[type] = ", nuisance ['type']," ","nuisance[name] = ", nuisance ['name']
                    for sampleName in self.backgrounds:
                        if sampleName in nuisance['samples'].keys() :

                            inputFile = inputDir + '/nominal/' + analysisName + '/' + sampleName + '.root'
                            fileIn = ROOT.TFile(inputFile, "READ")
                            histoTemplate = self._getShape(fileIn, sampleName, shapeName, lumi)

                            nBins = histoTemplate.GetNbinsX()
                            xInitial = histoTemplate.GetBinLowEdge(1)
                            xFinal = histoTemplate.GetBinLowEdge(nBins+1)
                            #normTemp = histoTemplate.Integral()

                            for cut_in_use in nuisance['cuts'] : 
                                if cut_in_use in cutName :
                                    for bin_in_use in nuisance['cuts'][cut_in_use] :
                            
                                        histoBinUpName = 'histo_' + sampleName + '_' + (nuisance['name']).replace("Bin", bin_in_use) + "Up"
                                        histoBinUp = ROOT.TH1F(histoBinUpName, '', nBins, xInitial, xFinal)
                            
                                        histoBinDoName = 'histo_' + sampleName + '_' + (nuisance['name']).replace("Bin", bin_in_use) + "Down"
                                        histoBinDo = ROOT.TH1F(histoBinDoName, '', nBins, xInitial, xFinal)
                      
                                        for iBin in range(1, nBins+1):
                                     
                                            yValue = histoTemplate.GetBinContent(iBin)
                                            yError = histoTemplate.GetBinError(iBin)
                                            yShift = 0.

                                            this_bin = "Bin" + str(iBin+2)
                                            if this_bin == bin_in_use :
                                                uncRel = float(nuisance['cuts'][cut_in_use][bin_in_use])
                                                if bin_in_use=="Bin4" :
                                                    uncRel = 0.02
                                                yShift = yValue * uncRel 
                                                yError = yShift

                                            histoBinUp.SetBinContent(iBin, yValue + yShift)
                                            histoBinUp.SetBinError  (iBin, yError)
                                            histoBinDo.SetBinContent(iBin, yValue - yShift)
                                            histoBinDo.SetBinError  (iBin, yError)
                       
                                        #normBinUp = histoBinUp.Integral()
                                        #histoBinUp.Scale(normTemp/normBinUp)
                                        #normBinDo = histoBinDo.Integral()
                                        #histoBinDo.Scale(normTemp/normBinDo)
           
                                        self._outFile.cd(cutName + "/" + variableName)
                                        #histoBinUp = self._checkBadBins(histoBinUp)
                                        histoBinUp.Write()
                                        #histoBinDo = self._checkBadBins(histoBinDo)
                                        histoBinDo.Write()

                            fileIn.Close()

                # Metfastsim https://twiki.cern.ch/twiki/bin/viewauth/CMS/SUSRecommendationsMoriond17#Special_treatment_of_MET_uncerta
                if nuisanceName == 'Metfastsim' :

                    print "nuisance[type] = ", nuisance ['type']," ","nuisance[name] = ", nuisance ['name']
                    for sampleName in self.signals:
                        if sampleName in nuisance['samples'].keys() :
                   
                            inputFile = inputDir.replace("NoTopPt", "Oct17") + '/nominal/' + analysisName + '/' + sampleName + signalPoint + '.root'
                            fileIn = ROOT.TFile(inputFile, "READ")
                            shapeNameUp = shapeName
                            if self._fastsimMet=="gen": 
                                shapeNameUp = shapeNameGen
                            shapeNameDo = shapeNameGen
                            if self._fastsimMet=="reco":
                                shapeNameDo = shapeName                            
                            histoUp = self._getShape(fileIn, sampleName, shapeNameUp, lumi)
                            histoUp.SetName('histo_' + sampleName + '_' + (nuisance['name']) + "Up")
                            histoDo = self._getShape(fileIn, sampleName, shapeNameDo, lumi)
                            histoDo.SetName('histo_' + sampleName + '_' + (nuisance['name']) + "Down")
                            self._outFile.cd(cutName + "/" + variableName)
                            histoUp.Write()
                            histoDo.Write()
                            fileIn.Close()
                            

                # stat nuisances  
                if nuisanceName == 'stat' : # 'stat' has a separate treatment, it's the MC/data statistics
                
                  for sampleName in self.signals:
                    if sampleName in nuisance['samples'].keys() :

                      inputFile = inputDir.replace("NoTopPt", "Oct17") + '/nominal/' + analysisName + '/' + sampleName + signalPoint + '.root'
                      fileIn = ROOT.TFile(inputFile, "READ")
                      histoTemplate = self._getFastSimShape(fileIn, shapeName, shapeNameGen, lumi)

                      nBins = histoTemplate.GetNbinsX()
                      xInitial = histoTemplate.GetBinLowEdge(1)
                      xFinal = histoTemplate.GetBinLowEdge(nBins+1)
                           
                      histoUpName = 'histo_' + sampleName + '_stat' + "Up"
                      histoUp = ROOT.TH1F(histoUpName, '', nBins, xInitial, xFinal)
                      
                      histoDoName = 'histo_' + sampleName + '_stat' + "Down"
                      histoDo = ROOT.TH1F(histoDoName, '', nBins, xInitial, xFinal)
                      
                      for iBin in range(1, nBins+1):
                          
                          yValue = histoTemplate.GetBinContent(iBin)
                          yError = histoTemplate.GetBinError(iBin)

                          ValueUp = yValue + yError
                          ValueDo = yValue - yError
                          if ValueDo<=0. :
                              ValueDo = 0.
                          
                          histoUp.SetBinContent(iBin, ValueUp)
                          histoUp.SetBinError  (iBin, yError)
                          histoDo.SetBinContent(iBin, ValueDo)
                          histoDo.SetBinError  (iBin, yError)
                          
                          histoBinUpName = 'histo_' + sampleName + '_ibin_' + str(iBin) + '_statUp'
                          histoBinUp = ROOT.TH1F(histoBinUpName, '', nBins, xInitial, xFinal)

                          histoBinDoName = 'histo_' + sampleName + '_ibin_' + str(iBin) + '_statDown'
                          histoBinDo = ROOT.TH1F(histoBinDoName, '', nBins, xInitial, xFinal)
                          
                          histoBinUp.SetBinContent(iBin, ValueUp)
                          histoBinUp.SetBinError  (iBin, yError)
                          histoBinDo.SetBinContent(iBin, ValueDo)
                          histoBinDo.SetBinError  (iBin, yError)

                          for iBin2 in range(1, nBins+1):
                              if iBin2 != iBin:

                                  yValue2 = histoTemplate.GetBinContent(iBin2)
                                  yError2 = histoTemplate.GetBinError(iBin2)
                          
                                  histoBinUp.SetBinContent(iBin2, yValue2)
                                  histoBinUp.SetBinError  (iBin2, yError2)
                                  histoBinDo.SetBinContent(iBin2, yValue2)
                                  histoBinDo.SetBinError  (iBin2, yError2)
                                  
                        
                          self._outFile.cd(cutName + "/" + variableName)
                          #histoBinUp = self._checkBadBins(histoBinUp, 1.)
                          histoBinUp.Write()
                          #histoBinDo = self._checkBadBins(histoBinDo, 1.)
                          histoBinDo.Write()
                          
                          
                      self._outFile.cd(cutName + "/" + variableName)
                      #histoUp = self._checkBadBins(histoUp, 1.)
                      histoUp.Write()
                      #histoDo = self._checkBadBins(histoDo, 1.)
                      histoDo.Write()  
                      
                      fileIn.Close()

                  for sampleName in self.backgrounds:
                    if sampleName in nuisance['samples'].keys() :

                      inputFile = inputDir + '/nominal/' + analysisName + '/' + sampleName + '.root'
                      fileIn = ROOT.TFile(inputFile, "READ")
                      histoTemplate = self._getShape(fileIn, sampleName, shapeName, lumi)

                      nBins = histoTemplate.GetNbinsX()
                      xInitial = histoTemplate.GetBinLowEdge(1)
                      xFinal = histoTemplate.GetBinLowEdge(nBins+1)
                           
                      histoUpName = 'histo_' + sampleName + '_stat' + "Up"
                      histoUp = ROOT.TH1F(histoUpName, '', nBins, xInitial, xFinal)
                      
                      histoDoName = 'histo_' + sampleName + '_stat' + "Down"
                      histoDo = ROOT.TH1F(histoDoName, '', nBins, xInitial, xFinal)

                      for iBin in range(1, nBins+1):

                          yValue = histoTemplate.GetBinContent(iBin)
                          yError = histoTemplate.GetBinError(iBin)

                          ValueUp = yValue + yError
                          ValueDo = yValue - yError
                          if ValueDo<=0. :
                              ValueDo = 0.0005
                          
                          histoUp.SetBinContent(iBin, ValueUp)
                          histoUp.SetBinError  (iBin, yError)
                          histoDo.SetBinContent(iBin, ValueDo)
                          histoDo.SetBinError  (iBin, yError)
                          
                          histoBinUpName = 'histo_' + sampleName + '_ibin_' + str(iBin) + '_statUp'
                          histoBinUp = ROOT.TH1F(histoBinUpName, '', nBins, xInitial, xFinal)

                          histoBinDoName = 'histo_' + sampleName + '_ibin_' + str(iBin) + '_statDown'
                          histoBinDo = ROOT.TH1F(histoBinDoName, '', nBins, xInitial, xFinal)
                          
                          histoBinUp.SetBinContent(iBin, ValueUp)
                          histoBinUp.SetBinError  (iBin, yError)
                          histoBinDo.SetBinContent(iBin, ValueDo)
                          histoBinDo.SetBinError  (iBin, yError)

                          for iBin2 in range(1, nBins+1):
                              if iBin2 != iBin:

                                  yValue2 = histoTemplate.GetBinContent(iBin2)
                                  yError2 = histoTemplate.GetBinError(iBin2)
                          
                                  histoBinUp.SetBinContent(iBin2, yValue2)
                                  histoBinUp.SetBinError  (iBin2, yError2)
                                  histoBinDo.SetBinContent(iBin2, yValue2)
                                  histoBinDo.SetBinError  (iBin2, yError2)
                                  
                        
                          self._outFile.cd(cutName + "/" + variableName)
                          #histoBinUp = self._checkBadBins(histoBinUp, 1.)
                          histoBinUp.Write()
                          #histoBinDo = self._checkBadBins(histoBinDo, 1.)
                          histoBinDo.Write()
                          
                          
                      self._outFile.cd(cutName + "/" + variableName)
                      #histoUp = self._checkBadBins(histoUp, 1.)
                      histoUp.Write()
                      #histoDo = self._checkBadBins(histoDo, 1.)
                      histoDo.Write()  
                      
                      fileIn.Close()

    def _mergeBins(self, histo):

        fitHisto = ROOT.TH1F('fitHisto', '', 5, 0, 5)
        
        thisBin = 1
        thisBinContent = 0.
        thisBinError = 0.

        nBins = histo.GetNbinsX()
        for iBin in range(1, nBins+1):

            yValue = histo.GetBinContent(iBin)
            yError = histo.GetBinError(iBin)
            if ((histo.GetXaxis().GetBinCenter(iBin-1)<40 and histo.GetXaxis().GetBinCenter(iBin)>40) or 
                (histo.GetXaxis().GetBinCenter(iBin)>80) ):
                fitHisto.SetBinContent(thisBin, thisBinContent)
                fitHisto.SetBinError(thisBin, math.sqrt(thisBinError))
                thisBinContent = 0.
                thisBinError = 0.
                thisBin = thisBin + 1
            thisBinContent += yValue
            thisBinError += (yError*yError)

        fitHisto.SetBinContent(thisBin, thisBinContent)
        fitHisto.SetBinError(thisBin, math.sqrt(thisBinError))

        return fitHisto;


    def _checkBadBins(self, histo, lumi, sampleName, thisShapeName):

        if lumi<-1. :
            return self._mergeBins(histo)

        if lumi==-1. :
            return histo

        histo.Scale(lumi)

        histoIntegral = histo.Integral()
        AverageWeight = 0.
        if histo.GetEntries()>0 :
            AverageWeight = histoIntegral/histo.GetEntries()
        nBins = histo.GetNbinsX()
        for iBin in range(1, nBins+1):
            yValue = histo.GetBinContent(iBin)
            if yValue <= 0. :
                zeroValue = 0.001
                #if 'SR3_Tag/h_MT2llisr_em' in thisShapeName and sampleName=="02_WZTo3LNu" :
                #    zeroValue = 0.0185
                histo.SetBinContent(iBin, zeroValue)
                if yValue == 0. :
                    ApplyZeroStat = True
                    if "07_ZJets" in sampleName :
                        ApplyZeroStat = False
                        if iBin>1 :
                            if histo.GetBinContent(iBin-1)>0.005 :
                                ApplyZeroStat = True
                        if iBin<nBins :
                            if histo.GetBinContent(iBin+1)>0.005 :
                                ApplyZeroStat = True
                    elif (sampleName=="T" or sampleName==" ") :
                        #print " turning off ", sampleName
                        ApplyZeroStat = False
                    if ApplyZeroStat :
                        histo.SetBinError(iBin, 1.84102*AverageWeight)
              
        #for iBin in range(2, nBins+1):
         #   yValue = histo.GetBinContent(iBin)
                      
        histoIntegralCorrected = histo.Integral()
        if (histoIntegralCorrected!=0 and histoIntegral > 0) :
            histo.Scale(histoIntegral/histoIntegralCorrected)

        #histo.Scale(lumi)
        #print sampleName, thisShapeName
        if "10_TTZ" in sampleName :
            histo.Scale(1.44)
            #print "Scaling TTZ"
        elif "02_WZTo3LNu" in sampleName :
            histo.Scale(0.97)
            #print "Scaling WZ"
        elif "03_ZZ" in sampleName :
            if "_NoJet" in thisShapeName :
                histo.Scale(0.74)
                #print "Scaling ZZ NoJet"
            elif "_NoTag" in thisShapeName :
                histo.Scale(1.21)
                #print "Scaling ZZ NoTag"
            else :
                histo.Scale(1.06)
                #print "Scaling ZZ Veto"

        return self._mergeBins(histo)
        
    def _readShape(self, fileIn, thisShapeName):

        if "_sf" not in thisShapeName:
            thisHisto = fileIn.Get(thisShapeName)
            return thisHisto
        else:
            eeShapeName = thisShapeName.replace("_sf", "_ee")
            mmShapeName = thisShapeName.replace("_sf", "_mm")
            #print thisShapeName, eeShapeName, mmShapeName
            sfHisto = fileIn.Get(eeShapeName)
            mmHisto = fileIn.Get(mmShapeName)
            sfHisto.Add(mmHisto)
            return sfHisto

    def _getShape(self, fileIn, sampleName, thisShapeName, lumi):
        
        if "_Veto" in thisShapeName:
            histo1  = self._readShape(fileIn, thisShapeName.replace("_Veto", "_NoTag"))
            histo2  = self._readShape(fileIn, thisShapeName.replace("_Veto", "_NoJet"))
            histo1.Add(histo2)
            return self._checkBadBins(histo1, lumi, sampleName, thisShapeName)
        else :
            thisHisto = self._readShape(fileIn, thisShapeName)
            return self._checkBadBins(thisHisto, lumi, sampleName, thisShapeName)

    def _getFastSimShape(self, fileIn, shapeName, shapeNameGen, lumi):
        
        historeco = self._getShape(fileIn, " ", shapeName, -1.)

        if self._fastsimMet=="reco" :
            return self._checkBadBins(historeco, lumi, " ", " ")
        
        histogen  = self._getShape(fileIn, " ", shapeNameGen, -1.)
        
        if self._fastsimMet=="gen" :
            return self._checkBadBins(histogen, lumi, " ", " ")

        nBins = historeco.GetNbinsX()
        xInitial = historeco.GetBinLowEdge(1)
        xFinal = historeco.GetBinLowEdge(nBins+1)
        
        histo = ROOT.TH1F('histo', '', nBins, xInitial, xFinal)

        for iBin in range(1, nBins+1):

            yValue = (historeco.GetBinContent(iBin) + histogen.GetBinContent(iBin))/2.
            yError = (historeco.GetBinError(iBin)   + histogen.GetBinError(iBin))/2.
            
            histo.SetBinContent(iBin, yValue)
            histo.SetBinError(iBin, yError)


        return self._checkBadBins(histo, lumi, " ", " ")



if __name__ == '__main__':
    print 'SHAPE MAKER'

    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)

    parser.add_option('--tag'                , dest='tag'               , help='Tag used for the shape file name'           , default=None)
    parser.add_option('--sigset'             , dest='sigset'            , help='Signal samples [SM]'                        , default='SM')
    parser.add_option('--inputDir'           , dest='inputDir'          , help='input directory'                            , default='./')
    parser.add_option('--outputDir'          , dest='outputDir'         , help='output directory'                           , default='./')
    parser.add_option('--outputFileName'     , dest='outputFileName'    , help='output file name'                           , default='Shapes')
    parser.add_option('--analysisName'       , dest='analysisName'      , help='analysis name'                              , default='Stop')
    parser.add_option('--structureFile'      , dest='structureFile'     , help='file with datacard configurations'          , default=None )
    parser.add_option('--nuisancesFile'      , dest='nuisancesFile'     , help='file with nuisances configurations'         , default=None )
    parser.add_option('--signalPoint'        , dest='signalPoint'       , help='signal name (mass point)'                   , default='')
    parser.add_option('--fastsimMet'         , dest='fastsimMet'        , help='treatment of Met in FastSim'                , default='mix')

    # read default parsing options as well
    hwwtools.addOptions(parser)
    hwwtools.loadOptDefaults(parser)
    (opt, args) = parser.parse_args()

    sys.argv.append( '-b' )
    ROOT.gROOT.SetBatch()


    print " configuration file = ", opt.pycfg
    
    print " inputDir          =          ", opt.inputDir
    print " outputDir         =          ", opt.outputDir
    print " outputFileName    =          ", opt.outputFileName
 
    if not opt.debug:
        pass
    elif opt.debug == 2:
        print 'Logging level set to DEBUG (%d)' % opt.debug
        logging.basicConfig( level=logging.DEBUG )
    elif opt.debug == 1:
        print 'Logging level set to INFO (%d)' % opt.debug
        logging.basicConfig( level=logging.INFO )
     
    factory = ShapeFactory()
    #factory._energy    = opt.energy
    factory._lumi      = opt.lumi
    factory._tag       = opt.tag
    
    # ~~~~
    variables = {}
    if os.path.exists(opt.variablesFile) :
      handle = open(opt.variablesFile,'r')
      exec(handle)
      handle.close()
    
    cuts = {}
    if os.path.exists(opt.cutsFile) :
      handle = open(opt.cutsFile,'r')
      exec(handle)
      handle.close()
    
    samples = {}
    if os.path.exists(opt.samplesFile) :
      handle = open(opt.samplesFile,'r')
      exec(handle)
      handle.close()
   
    # ~~~~
    structure = {}
    if opt.structureFile == None :
       print " Please provide the datacard structure "
       exit ()
       
    if os.path.exists(opt.structureFile) :
      handle = open(opt.structureFile,'r')
      exec(handle)
      handle.close()


    # ~~~~
    nuisances = {}
    if opt.nuisancesFile == None :
       print " Please provide the nuisances structure if you want to add nuisances "
       
    if os.path.exists(opt.nuisancesFile) :
      handle = open(opt.nuisancesFile,'r')
      exec(handle)
      handle.close()
    

    factory.makeShapesFromHistos( opt.inputDir ,opt.outputDir, opt.outputFileName, opt.analysisName, opt.lumi, variables, cuts, samples, structure, nuisances, opt.signalPoint, opt.fastsimMet)
    
        
        
