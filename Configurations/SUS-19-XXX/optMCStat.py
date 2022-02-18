#!/usr/bin/env python

import optparse
import json
import ROOT
import LatinoAnalysis.Gardener.hwwtools as hwwtools
import os.path

if __name__ == '__main__':

    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)

    parser.add_option('--tag'            , dest='tag'            , help='Tag used for the shape file name'          , default=None)
    parser.add_option('--years'          , dest='years'          , help='Years'                                     , default='all')
    parser.add_option('--sigset'         , dest='sigset'         , help='Signal samples [SM]'                       , default='SM')
    parser.add_option('--inputDir'       , dest='inputDir'       , help='Input directory'                           , default='./Shapes')
    parser.add_option('--verbose'        , dest='verbose'        , help='Activate print for debugging'              , default=False, action='store_true')
    parser.add_option('--statcorr'       , dest='statcorr'       , help='Apply statistical corrections'             , default=False, action='store_true')
    # read default parsing options as well
    hwwtools.addOptions(parser)
    hwwtools.loadOptDefaults(parser)
    (opt, args) = parser.parse_args()
   
    if opt.years=='-1' or opt.years.lower()=='all':
        years =  [ '2016', '2017', '2018' ]
    elif opt.years=='0':
        years = [ '2016' ]
    elif opt.years=='1':
        years = [ '2017' ]
    elif opt.years=='2':
        years = [ '2018' ]
    else:
        years = opt.years.split('-')

    localtag = opt.tag
    opt.tag = years[0] + localtag

    if 'SM' not in opt.sigset:
        opt.sigset = 'SM-' + opt.sigset

    samples = {}
    if os.path.exists(opt.samplesFile) :
      handle = open(opt.samplesFile,'r')
      exec(handle)
      handle.close()

    cuts = {}
    if os.path.exists(opt.cutsFile) :
      handle = open(opt.cutsFile,'r')
      exec(handle)
      handle.close()
 
    variables = {}
    if os.path.exists(opt.variablesFile) :
      handle = open(opt.variablesFile,'r')
      exec(handle)
      handle.close()

    inFiles = { }
    for year in years:
        inFiles[year] = [ ]
        inDirName = opt.inputDir + '/' + year + '/' + localtag + '/'
        for inFileName in os.listdir(inDirName):
            if 'plots_'+localtag+'_'+opt.sigset.split('_')[0] in inFileName and '.root' in inFileName: 
                inFiles[year].extend([ ROOT.TFile(inDirName+inFileName, 'READ') ])

    exec(open('./signalMassPoints.py').read())

    sampleYields = { 'backgrounds' : {} }

    for model in signalMassPoints:
        if model in opt.sigset:
            for massPoint in signalMassPoints[model]:
                if massPointInSignalSet(massPoint, opt.sigset):
                    sampleYields[massPoint] = {}

    for cutName in cuts:
        if 'SR' in cutName:

            for sample in sampleYields:
                sampleYields[sample][cutName] = {}

            for variableName in variables:
                if 'cuts' not in variables[variableName] or cutName in variables[variableName]['cuts']:

                    nBins = variables[variableName]['range'][0] if len(variables[variableName]['range'])==1 else len(variables[variableName]['range'][0])-1
                    for sample in sampleYields:
                        for ib in range(1, nBins+1):
                            sampleYields[sample][cutName]['bin'+str(ib)] = { 'value' : 0., 'squaredError' : 0. }

                    folderName = cutName + '/' + variableName
       
                    if opt.verbose: print '################################', folderName

                    for year in inFiles:

                        gotSamples = [ ]

                        for infile in inFiles[year]:

                            cutDir = infile.Get(folderName)

                            for sample in samples:
                                if not samples[sample]['isDATA'] and ('isControlSample' not in samples[sample] or not samples[sample]['isControlSample']):
                                    if sample not in gotSamples and cutDir.GetListOfKeys().Contains('histo_'+sample):

                                        tmpHisto = cutDir.Get('histo_' + sample)

                                        if tmpHisto.GetNbinsX()!=nBins:
                                            print 'Error: number of bins not matching for cut', cutName, 'and sample', sample
                                            exit()

                                        sampleName = sample if samples[sample]['isSignal'] else 'backgrounds'
 
                                        statCorr = 1.
                                        if opt.statcorr:
                                            if samples[sample]['isSignal']:
                                                mx = float(sample.split('_')[1].split('-')[1])
                                                my = float(sample.split('_')[2].split('-')[1])  
                                                if 'T2tt' in sample:
                                                    if mx>=350:
                                                        statCorr = pow(min(1.+(mx-300.)/100.,4.), 2)
                                                if 'TChipmSlepSnu' in sample:
                                                    if mx-my<=175:
                                                        statCorr = max((int((175.-(mx-my))/25.)-max(int((my-250.)/25.),0)+4),1)
                                                if 'TChipmWW' in sample:
                                                    statCorr = 2.
                                                    if mx-my<=150:
                                                        fk = min(int((225.-(mx-my))/25.), 5)
                                                        if mx>=350.-25.*fk:
                                                           fk = max(fk-int((mx-(350.-25.*fk))/25.+1),2)
                                                        statCorr = fk
                                                if 'TSlepSlep' in sample:
                                                    if mx-my<=100:
                                                        mye = my if mx-my>=50. else mx-25
                                                        statCorr = max((math.ceil((100.-(mx-mye))/25.)-max(int((mye-350.)/25.),0)+2),1)
                                        for ib in range(1, nBins+1):
                                            sampleYields[sampleName][cutName]['bin'+str(ib)]['value'] += tmpHisto.GetBinContent(ib)
                                            sampleYields[sampleName][cutName]['bin'+str(ib)]['squaredError'] += tmpHisto.GetBinError(ib)*tmpHisto.GetBinError(ib)/statCorr

                                        gotSamples.extend([sample])

    if opt.sigset.count('to')!=2: 
        print 'Warning: sigset', opt.sigset, 'not defining an area on the mass plane. Will not create plots'
        exit()

    minMassX = float(opt.sigset.split('_')[1].split('to')[0].split('-')[1]) - 25.
    maxMassX = float(opt.sigset.split('_')[1].split('to')[1]) + 25.
    if '_dm' not in opt.sigset:
        minMassY = max(float(opt.sigset.split('_')[2].split('to')[0].split('-')[1]) - 50., 0.)
        maxMassY = float(opt.sigset.split('_')[2].split('to')[1]) + 50.
    else:
        minMassY = max(minMassX - float(opt.sigset.split('_')[2].split('to')[1]) - 50., 0.)
        maxMassY = maxMassX - float(opt.sigset.split('_')[2].split('to')[0].split('-')[1]) + 50.

    sigHisto = { }

    for histoName in [ 'sigHistoText', 'sigHistoColour' ]:

        sigHisto[histoName] = ROOT.TH2F(histoName, '', int(maxMassX-minMassX), minMassX, maxMassX, int(maxMassY-minMassY), minMassY, maxMassY)
        sigHisto[histoName].SetXTitle('m_{prompt} [GeV]')
        sigHisto[histoName].SetYTitle('m_{LSP} [GeV]')

    for massPoint in sampleYields:
        if massPoint!='backgrounds': 

            maxStatSignificance, maxSignificance = 0., 0.
            signalRelativeErrorForMaxStatSignificance, signalRelativeErrorForMaxSignificance = 1., 1. 
        
            for cutName in sampleYields[massPoint]:
	        for mt2llbin in sampleYields[massPoint][cutName]:

                    signalYields           = sampleYields[massPoint][cutName][mt2llbin]['value']
                    signalSquaredError     = sampleYields[massPoint][cutName][mt2llbin]['squaredError']
                    backgroundYields       = sampleYields['backgrounds'][cutName][mt2llbin]['value']
                    backgroundSquaredError = sampleYields['backgrounds'][cutName][mt2llbin]['squaredError'] 

                    if signalYields>0.:

                        binStatSignificance = signalYields/math.sqrt(backgroundYields + signalYields)
                        binSignificance     =  signalYields/math.sqrt(backgroundYields + signalYields + backgroundSquaredError + signalSquaredError)

                        if binStatSignificance>maxStatSignificance: 
                            signalRelativeErrorForMaxStatSignificance = math.sqrt(signalSquaredError)/signalYields
                            maxStatSignificance = binStatSignificance

                        if binSignificance>maxSignificance: 
                            signalRelativeErrorForMaxSignificance = math.sqrt(signalSquaredError)/signalYields
                            maxSignificance = binSignificance

            if opt.verbose:
                print massPoint, 100.*signalRelativeErrorForMaxStatSignificance, 100.*signalRelativeErrorForMaxSignificance

            for xMass in range(int(massPoint.split('_')[1].split('-')[1])-5,int(massPoint.split('_')[1].split('-')[1])+5):
                for yMass in range(int(massPoint.split('_')[2].split('-')[1])-5,int(massPoint.split('_')[2].split('-')[1])+5): 	
                    massPointBin = sigHisto['sigHistoColour'].FindBin(xMass, yMass)
                    sigHisto['sigHistoColour'].SetBinContent(massPointBin, round(100.*signalRelativeErrorForMaxSignificance))
        
            massPointBin = sigHisto['sigHistoText'].FindBin(int(massPoint.split('_')[1].split('-')[1]), int(massPoint.split('_')[2].split('-')[1]))
            sigHisto['sigHistoText'].SetBinContent(massPointBin, round(100.*signalRelativeErrorForMaxSignificance))

    ROOT.gStyle.SetOptStat(ROOT.kFALSE)

    NRGBs = 5
    NCont = 255
    stops = array("d",[0.00, 0.34, 0.61, 0.84, 1.00])
    red = array("d",[0.50, 0.50, 1.00, 1.00, 1.00])
    green = array("d",[ 0.50, 1.00, 1.00, 0.60, 0.50])
    blue = array("d",[1.00, 1.00, 0.50, 0.40, 0.50])
    ROOT.TColor.CreateGradientColorTable(NRGBs, stops, red, green, blue, NCont)
    ROOT.gStyle.SetNumberContours(NCont)

    plotCanvas = ROOT.TCanvas( 'plotCanvas', '', 1200, 900)

    sigHisto['sigHistoColour'].SetMinimum(0.)
    sigHisto['sigHistoColour'].SetMaximum(50.)
    sigHisto['sigHistoColour'].Draw('colz')
    sigHisto['sigHistoText'].Draw('sametext')

    outputDir = './Plots/optMCStat/'
    os.system('mkdir -p ' + outputDir)
    os.system('cp Plots/index.php ' + outputDir)
    statcorr = '_statCorr' if opt.statcorr else ''
    plotCanvas.Print(outputDir+opt.sigset.replace('SM-','')+'_'+year+statcorr+'.png')







