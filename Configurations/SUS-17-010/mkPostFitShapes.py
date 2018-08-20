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

        # list of [processes]  
        self.processes = {}

        self.shapelevels = []
        self.shapelevels.append('shapes_prefit')
        self.shapelevels.append('shapes_fit_b')
        self.shapelevels.append('shapes_fit_s')
        

    # _____________________________________________________________________________
    # 
    # _____________________________________________________________________________
    def makePostFitShapes( self, inputFileName, workingDir, inputDir, analysisName, variables, cuts, samples, structureFile, signalPoint):
    
        print "=============================="
        print "===== makePostFitShapes ======"
        print "=============================="
        
        self._variables = variables
        self._samples   = samples
        self._cuts      = cuts

        self._inputFileName  = inputFileName
        self._workingDir     = workingDir
       
        inputFile = workingDir + '/' + inputFileName + '.root'
        inFile = ROOT.TFile(inputFile, "READ")

        inputFileData = inputDir + '/nominal/' + analysisName + '/'
        for sampleName, sample in self._samples.iteritems():
            if structureFile[sampleName]['isData'] == 1:
                inputFileData = inputFileData + sampleName + ".root"
        
        workingDirName = self._workingDir + "/Postfit/" + analysisName
        if 'asimov' in inputFileName:
            workingDirName = workingDirName.replace('Postfit', 'Postfitasimov')
        if not os.path.isdir (workingDirName):
            os.makedirs(workingDirName)

        for sampleName, sample in self._samples.iteritems():
            processType = 'Background'
            if structureFile[sampleName]['isSignal'] == 1 :
                processType = 'Signal'
            elif structureFile[sampleName]['isData'] == 1 :
                processType = 'Data'
            self.processes.update({sampleName:processType})
        self.processes.update({'total_background':'TotalBackground'})
        self.processes.update({'total':'Total'})

        # Loop over processes
        for sampleName in self.processes :

            processName = sampleName
            if self.processes[sampleName] == 'Signal' :
                processName = sampleName + signalPoint
            elif self.processes[sampleName] == 'TotalBackground' :
                processName = '99_TotalBackground'
            elif self.processes[sampleName] == 'Total' :
                processName = '00_Total'
                
            print "Create rootfile for process ",processName 

            self._outFile = ROOT.TFile.Open( workingDirName + "/" + processName + ".root", 'recreate')
            ROOT.TH1.SetDefaultSumw2(True)
        
            self._outFile.mkdir (analysisName)

            _createdCutDir = []

            # loop over cuts  
            for cutName in self._cuts :

                cutNameSplit = cutName.split('_')
                cutDirName = analysisName + "/02_" + cutNameSplit[0] + '_' + cutNameSplit[1] 
                datacutCutDirName = cutNameSplit[1] + "_" + cutNameSplit[0] + "_" + cutNameSplit[2]
                if "Chi" in workingDirName :
                    datacutCutDirName = cutNameSplit[0] + "_" + cutNameSplit[1] + "_" + cutNameSplit[2]

                createdDir = False
                for existingCutDir in _createdCutDir:
                    if cutDirName==existingCutDir:
                        createdDir = True
                        
                if not createdDir:
                    self._outFile.mkdir (cutDirName)
                    _createdCutDir.append(cutDirName)

                print "    Filling histograms for cut ",cutDirName," channel ",cutNameSplit[2] 
                    
                # loop over variables
                for variableName, variable in self._variables.iteritems():
                        
                    # Manually for the moment (attention to isr)
                    #if variableName!="MT2ll":
                    #    continue
                    
                    nBins     = 7
                    xInitial = 0.
                    xFinal    = 140.
                    
                    for shapeLevel in self.shapelevels:

                        outputHistoName = 'h_' + variableName + '_' + shapeLevel.replace("shapes_", "") + '_' + cutNameSplit[2]
                        
                        if self.processes[sampleName] != 'Data' :

                            inputHistoName = shapeLevel + '/' + datacutCutDirName + '/' + sampleName
                            inputHisto = inFile.Get(inputHistoName)
                            
                            outputHisto = ROOT.TH1F(outputHistoName, '', nBins, xInitial, xFinal)
                            print inputHistoName
                            for iBin in range(1, nBins+1):
                                
                                yValue = inputHisto.GetBinContent(iBin)
                                yError = inputHisto.GetBinError(iBin)
                                
                                outputHisto.SetBinContent(iBin, yValue)
                                outputHisto.SetBinError(iBin, yError)
                                
                            outputHisto.SetLabelOffset(0.02, "X");
                            outputHisto.SetLabelOffset(0.02, "Y");
                            outputHisto.SetNdivisions ( 505, "X");
                            outputHisto.SetNdivisions ( 505, "Y");

                            self._outFile.cd(cutDirName)
                            outputHisto.Write()

                        else:

                            inFileData = ROOT.TFile(inputFileData, "READ")
                            inputHistoName = cutDirName + '/h_' + variableName + '_' + cutNameSplit[2] 
                            outputHisto = self._getShape(inFileData, inputHistoName)
                            self._outFile.cd(cutDirName)
                            outputHisto.SetName(outputHistoName)
                            outputHisto.Write()
                            inFileData.Close()

            self._outFile.Close()

        inFile.Close()

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

    def _getShape(self, fileIn, thisShapeName):
        
        if "_Veto" in thisShapeName:
            histo1  = self._readShape(fileIn, thisShapeName.replace("_Veto", "_NoTag"))
            histo2  = self._readShape(fileIn, thisShapeName.replace("_Veto", "_NoJet"))
            histo1.Add(histo2)
            return histo1
        else :
            thisHisto = self._readShape(fileIn, thisShapeName)
            return thisHisto
         
if __name__ == '__main__':
    print 'SHAPE MAKER'

    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)

    parser.add_option('--inputFileName'      , dest='inputFileName'     , help='input file name'                            , default='mlfit')
    parser.add_option('--workingDir'         , dest='workingDir'        , help='working directory'                          , default='./')
    parser.add_option('--inputDir'           , dest='inputDir'          , help='input directory for data'                   , default='./')
    parser.add_option('--analysisName'       , dest='analysisName'      , help='analysis name'                              , default='Stop')
    parser.add_option('--structureFile'      , dest='structureFile'     , help='file with datacard configurations'          , default=None )
    parser.add_option('--signalPoint'        , dest='signalPoint'       , help='signal name (mass point)'                   , default='')

    # read default parsing options as well
    hwwtools.addOptions(parser)
    hwwtools.loadOptDefaults(parser)
    (opt, args) = parser.parse_args()

    sys.argv.append( '-b' )
    ROOT.gROOT.SetBatch()


    print " configuration file = ", opt.pycfg
    
    print " inputFile         =          ", opt.inputFileName
    print " workingDir        =          ", opt.workingDir
    print " inputDir (data)   =          ", opt.inputDir
 
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
    #factory._lumi      = opt.lumi
    
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

    factory.makePostFitShapes( opt.inputFileName, opt.workingDir, opt.inputDir, opt.analysisName, variables, cuts, samples, structure, opt.signalPoint)
    
        
        
