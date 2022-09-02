import os
import copy
import ROOT
import math
import PlotsConfigurations.Tools.commonTools  as commonTools
import PlotsConfigurations.Tools.latinoTools  as latinoTools
import PlotsConfigurations.Tools.combineTools as combineTools

### Analysis defaults

def setAnalysisDefaults(opt):

    opt.method = 'PtRel' if 'PtRel' in opt.tag else 'System8'

    opt.combineLocation = '/afs/cern.ch/work/s/scodella/SUSY/CMSSW_10_2_14/src' 

    if opt.year=='test' or opt.year=='*': opt.year = 'UL17nano'

    opt.btagWPs = [ 'DeepCSVL', 'DeepCSVM', 'DeepCSVT', 'DeepJetL', 'DeepJetM', 'DeepJetT' ]
    opt.ptBins = [ 'Pt20to30', 'Pt30to50', 'Pt50to70','Pt70to100','Pt100to140','Pt140to200','Pt200to300','Pt300to600', 'Pt600to1000','Pt1000to1400' ]

    if '_btag' in opt.tag:
        btagToKeepString = opt.tag.split('_btag')[1].split('_')[0]
        btagToKeep = []
        for btagWP in opt.btagWPs:
            if btagToKeepString in btagWP:
                btagToKeep.append(btagWP)
        opt.btagWPs = btagToKeep

    if '_Pt' in opt.tag:
        ptbinToKeep = []
        for ptbin in opt.ptBins:
            if ptbin in opt.tag:
                ptbinToKeep.append(ptbin)
        opt.ptBins = ptbinToKeep
        
    opt.Systematics = [ 'Central' ]
    if 'systematicsawayjet' in opt.option.lower() or 'systematicawayjet' in opt.option.lower() or 'systawayjet' in opt.option.lower():
        opt.Systematics.extend([ 'AwayJetDown', 'AwayJetUp' ])

### Shapes, kinematic weights and prefit plots

def bTagPerfShapes(opt):

    if 'step' not in opt.option:
        print 'Error in ptRelShapes: please choose a step'
        exit()
    
    if 'step0' in opt.option:
        opt.tag = opt.method+'Kinematics'
    elif 'step1' in opt.option:
        opt.tag = opt.method+'Kinematics:mujetpt'
    elif 'step2' in opt.option:
        opt.tag = opt.method+'Kinematics:mujetptProdRun2'
    elif 'step3' in opt.option:
        opt.tag = opt.method+'Kinematics:mujetpt:mujetetaProdRun2'
    elif 'step4' in opt.option:
        opt.tag = opt.method+'TemplatesKinematics:mujetpt:mujetetaProdRun2'
    elif 'step5' not in opt.option or opt.method!='System8':
        print 'Error in bTagPerfShapes: please choose an existing step'
        exit()

    if 'kin' in opt.option.lower():
        if 'step0' in opt.option: opt.option += 'mujetpt'
        if 'step2' in opt.option: opt.option += 'mujeteta'
        kinematicWeights(opt)
    elif 'step5' in opt.option:
        opt.tag = 'System8TemplatesKinematics:mujetpt:mujetetaProdRun2'
        system8Input(opt)
    elif 'plot' in opt.option:
        latinoTools.plots(opt)
    elif 'merges' in opt.option:
        opt.action = 'mergesingle'
        latinoTools.mergesingle(opt)
    elif 'mergea' in opt.option:
        opt.action = 'mergeall'
        latinoTools.mergeall(opt)
    else:
        opt.action = 'shapes'
        opt.batchQueue = 'workday'
        opt.option += 'reset'
        latinoTools.shapes(opt)

def system8Input(opt):

    motherFile = commonTools.openShapeFile(opt.shapedir, opt.year, opt.tag.split('__')[0], 'SM', 'SM')
    
    samples, cuts, variables = commonTools.getDictionariesInLoop(opt.configuration, opt.year, opt.tag, opt.sigset, 'variables')

    outputDir = '/'.join([ './System8Input', opt.year, opt.tag.split('__')[0] ])
    os.system('mkdir -p '+outputDir)

    templateMap = { 'Data' : { 'lepton_in_jet' : [ 'n_pT'   , 'ntag_pT'   , 'p_pT'   , 'ptag_pT'    ] },
                    'QCD'  : { 'lepton_in_jet' : [ 'n_pT'   , 'ntag_pT'   , 'p_pT'   , 'ptag_pT'    ],
                               'MCTruth'       : [ 'n_pT_b' , 'ntag_pT_b' , 'p_pT_b' , 'ptag_pT_b', 'n_pT_cl', 'ntag_pT_cl', 'p_pT_cl', 'ptag_pT_cl' ] } }

    for dataset in templateMap.keys():
        for btagWPcut in cuts:
            if btagWPcut.count('_')==2 and 'Up' not in btagWPcut.split('_')[-1] and 'Down' not in btagWPcut.split('_')[-1]:
                btagWP = btagWPcut.split('_')[2]
                for systcut in cuts:
                    if systcut.count('_')>=2 and btagWP in systcut.split('_')[2]:
                        systematic = 'Central' if systcut.count('_')==2 else systcut.split('_')[3]
                        outputFileName = '_'.join([ 'S8', dataset, systematic, btagWP, 'anyEta.root' ])

                        ptEdges = []
                        for ptbin in cuts:
                            if '_' not in ptbin: 
                                for binedge in [ float(ptbin.split('Pt')[1].split('to')[0]), float(ptbin.split('to')[1]) ]:
                                    if binedge not in ptEdges:
                                        ptEdges.append(binedge)
                        ptEdges.sort()

                        ptRelRange = variables['ptrel']['range']

                        outputHistogram = {}

                        for directory in templateMap[dataset]:
                            outputHistogram[directory] = {}
                            for selection in templateMap[dataset][directory]:

                                outputHistogram[directory][selection] = commonTools.bookHistogram(selection, [ ptEdges ], ptRelRange, selection)

                                if dataset=='QCD' and directory=='lepton_in_jet': continue

                                selectionList = [ ]
                                if 'p' in selection: selectionList.append('AwayJetTag')
                                if 'tag_' in selection: selectionList.append(btagWP)
                                sample = 'bjets' if '_b' in selection else 'light' if '_cl' in selection else 'DATA'
 
                                for ptbin in cuts:
                                    if '_' not in ptbin:
                                        
                                        cutList = copy.deepcopy(selectionList)
                                        cutList.insert(0, ptbin)
                                        cutName = '_'.join(cutList)
                                        motherHisto = motherFile.Get('/'.join([ cutName, 'ptrel', 'histo_'+sample ]))

                                        ptValue = (float(ptbin.split('Pt')[1].split('to')[0])+float(ptbin.split('to')[1]))/2.

                                        for ib in range(1, motherHisto.GetNbinsX()+1):

                                            ptRelValue = motherHisto.GetBinCenter(ib)
                                            bin2D = outputHistogram[directory][selection].FindBin(ptValue, ptRelValue) 
                                            outputHistogram[directory][selection].SetBinContent(bin2D, motherHisto.GetBinContent(ib))
                                            outputHistogram[directory][selection].SetBinError(bin2D, motherHisto.GetBinError(ib)) 

                        if dataset=='QCD':
                            for selection in templateMap['QCD']['lepton_in_jet']:
                                
                                outputHistogram['lepton_in_jet'][selection].Add(outputHistogram['MCTruth'][selection+'_b'])
                                outputHistogram['lepton_in_jet'][selection].Add(outputHistogram['MCTruth'][selection+'_cl'])

                        outputFile = commonTools.openRootFile(outputDir+'/'+outputFileName, 'recreate')

                        for directory in templateMap[dataset]:

                            outputFile.mkdir(directory)
                            outputFile.cd(directory) 

                            for selection in templateMap[dataset][directory]:
                                outputHistogram[directory][selection].Write()

                        outputFile.cd()
                        outputFile.Write()
                        outputFile.Close()

### Fits and postfit plots

def bTagPerfAnalysis(opt, action):

    rawTag = opt.tag.split('__')[0]

    for btagWP in opt.btagWPs:
        for ptbin in opt.ptBins:

            opt.tag = '_'.join([ rawTag, '_btag'+btagWP, '___'+ptbin ])

            if action=='datacards':
                combineTools.writeDatacards(opt)

            elif action=='ptrelfit': 
                combineTools.mlfits(opt)

            elif action=='system8fit':
                runSystem8Fit(opt)

            elif action=='getsystem8results':
                 getSystem8FitResults(opt)

            elif 'Results' in opt.tag:
                getPtRelFitResults(opt)

            elif commonTools.goodCombineFit(opt, opt.year, opt.tag, '', 'PostFitS'):
             
                if action=='postfitshapes':  latinoTools.postFitShapes(opt) 
                elif action=='postfitplots': latinoTools.postFitPlots(opt)
                elif action=='getptrelresults': getPtRelFitResults(opt)

            elif action=='checkfit':
                print 'Failed fit for campaign='+opt.year+', WP='+btagWP+', bin='+ptbin

def ptRelDatacards(opt):

    bTagPerfAnalysis(opt, 'datacards')
 
def ptRelFits(opt):

    opt.batchQueue = 'nextweek'
    opt.option += 'resetskipbonly'
    bTagPerfAnalysis(opt, 'ptrelfit')

def ptRelFitCheck(opt):

    bTagPerfAnalysis(opt, 'checkfit')

def ptRelPostFitShapes(opt):

    opt.option += 'postfits'
    bTagPerfAnalysis(opt, 'postfitshapes')

def ptRelPostFitPlots(opt):

    opt.option += 'postfits'
    bTagPerfAnalysis(opt, 'postfitplots')

def system8Fits(opt):

    bTagPerfAnalysis(opt, 'system8fit')

def runSystem8Fit(opt):

    print 'please, write me if useful'

### Efficiencies and scale factors

def efficiencyError(P, F, eP, eF, correlation):

    T = P + F
    dP = (1./T -P/pow(T,2))
    dF = (-P/pow(T,2))

    return math.sqrt( pow(eP*dP,2) + pow(eF*dF,2) + 2.*correlation*eP*dP*eF*dF )

def getPtRelEfficiency(opt, inputFile, fileType, btagWP, ptbin, systematic):

    cut = '_'.join([ btagWP, ptbin, systematic, 'BTAGSTATUS' ]).replace('_Central','')

    if fileType=='shapes': histoPath = cut+'/ptrel/histo_bjets'
    else: histoPath = 'shapes_fit_s/'+cut+'/bjets'

    histoPass = inputFile.Get(histoPath.replace('BTAGSTATUS','Pass'))
    histoFail = inputFile.Get(histoPath.replace('BTAGSTATUS','Fail'))

    errorPassYield, errorFailYield = ROOT.double(), ROOT.double()
    passYield = histoPass.IntegralAndError(-1,-1,errorPassYield)
    failYield = histoFail.IntegralAndError(-1,-1,errorFailYield)

    efficiency = passYield/(passYield+failYield)

    correlation = 0.

    if fileType!='shapes': # Use a trick for the time being
        histoTotal = inputFile.Get('shapes_fit_s/total_signal')
        errorTotalYield = ROOT.double()
        totalYield = histoTotal.IntegralAndError(-1,-1,errorTotalYield)

        if errorPassYield*errorFailYield!=0:
            correlation = (pow(errorTotalYield,2)-pow(errorPassYield,2)-pow(errorFailYield,2))/(2*errorPassYield*errorFailYield)
     
    return efficiency, efficiencyError(passYield, failYield, errorPassYield, errorFailYield, correlation)

def readOldPtRelFitResultsFromTables(opt, btagWP, ptbin):

    systematic = 'Central'

    tableName = '/afs/cern.ch/work/s/scodella/BTagging/CodeDevelopment/CMSSW_10_2_11/src/RecoBTag/PerformanceMeasurements/test/PtRelTools/Tables/PtRelFit_'+btagWP+'_anyEta_'+ptbin.replace('to','')+'_'+systematic+'_PSRun2017UL17_KinEtaAfterPtBinsCentral_LowPtAwayTrgConf_Run2016Production.txt'

    if btagWP not in opt.bTagPerfResults: opt.bTagPerfResults[btagWP] = {}
    if systematic not in opt.bTagPerfResults[btagWP]: opt.bTagPerfResults[btagWP][systematic] = {}

    opt.bTagPerfResults[btagWP][systematic][ptbin] = {}

    tableFile = open(tableName, 'r')
    lines = tableFile.readlines()
    for line in lines:
        if 'Efficiency MC' in line:
            opt.bTagPerfResults[btagWP][systematic][ptbin]['efficiencyMC']             = float(line.split(' = ')[1].split(' +/- ')[0])
            opt.bTagPerfResults[btagWP][systematic][ptbin]['efficiencyMCUncertainty']  = float(line.split(' +/- ')[1].split('\n')[0])
        elif 'Eff. data' in line:
            opt.bTagPerfResults[btagWP][systematic][ptbin]['efficiencyFit']            = float(line.split(' = ')[1].split(' +/- ')[0])
            opt.bTagPerfResults[btagWP][systematic][ptbin]['efficiencyFitUncertainty'] = float(line.split(' +/- ')[1].split(' (')[0])
        elif 'Scale factor' in line:
            opt.bTagPerfResults[btagWP][systematic][ptbin]['scaleFactor']              = float(line.split(' = ')[1].split(' +/- ')[0])
            opt.bTagPerfResults[btagWP][systematic][ptbin]['scaleFactorUncertainty']   = float(line.split(' +/- ')[1].split('\n')[0])

def getPtRelFitResults(opt):

    btagWP = opt.tag.split('_btag')[1].split('_')[0]
    ptbin = 'Pt'+opt.tag.split('_Pt')[1].split('_')[0]

    if 'Results' in opt.tag:
        readOldPtRelFitResultsFromTables(opt, btagWP, ptbin)
        return

    motherFile = commonTools.openShapeFile(opt.shapedir, opt.year, opt.tag.split('_')[0], 'SM', 'SM')
    fitFile = commonTools.openCombineFitFile(opt, '', opt.year, opt.tag)

    for systematic in opt.Systematics:
 
        efficiencyMC,  uncertaintyMC  = getPtRelEfficiency(opt, motherFile, 'shapes', btagWP, ptbin, systematic)
        efficiencyFit, uncertaintyFit = getPtRelEfficiency(opt, fitFile,    'fit',    btagWP, ptbin, systematic)

        scaleFactor = efficiencyFit/efficiencyMC
        scaleFactorUncertainty = scaleFactor*math.sqrt(pow(uncertaintyFit/efficiencyFit,2)+pow(uncertaintyMC/efficiencyMC,2))

        if btagWP not in opt.bTagPerfResults: opt.bTagPerfResults[btagWP] = {}
        if systematic not in opt.bTagPerfResults[btagWP]: opt.bTagPerfResults[btagWP][systematic] = {}

        opt.bTagPerfResults[btagWP][systematic][ptbin] = {}
        opt.bTagPerfResults[btagWP][systematic][ptbin]['efficiencyMC']             = efficiencyMC
        opt.bTagPerfResults[btagWP][systematic][ptbin]['efficiencyMCUncertainty']  = uncertaintyMC
        opt.bTagPerfResults[btagWP][systematic][ptbin]['efficiencyFit']            = efficiencyFit
        opt.bTagPerfResults[btagWP][systematic][ptbin]['efficiencyFitUncertainty'] = uncertaintyFit
        opt.bTagPerfResults[btagWP][systematic][ptbin]['scaleFactor']              = scaleFactor
        opt.bTagPerfResults[btagWP][systematic][ptbin]['scaleFactorUncertainty']   = scaleFactorUncertainty

    motherFile.Close()
    fitFile.Close()

def getSystem8FitResults(opt):

    print 'please, write me if useful'

def getBTagPerfResults(opt):

    opt.bTagPerfResults = {}
    bTagPerfAnalysis(opt, 'get'+opt.method.lower()+'results')

### Plots for efficiencies and scale factors

def templateHistogram(opt, result):

    ptEdges = []
    for ptbin in opt.ptBins:
        for binedge in [ float(ptbin.split('Pt')[1].split('to')[0]), float(ptbin.split('to')[1]) ]:
            if binedge not in ptEdges:
                ptEdges.append(binedge)

    ptEdges.sort()

    return commonTools.bookHistogram(result, [ ptEdges ], style='')

def fillBTagPerfHistogram(opt, result, btagWP, systematic):

    bTagPerfHisto = templateHistogram(opt, result)
    bTagPerfHisto.SetDirectory(0)

    for ptbin in opt.bTagPerfResults[btagWP][systematic]:

        ib = bTagPerfHisto.FindBin((float(ptbin.split('Pt')[1].split('to')[0])+float(ptbin.split('to')[1]))/2.)
        bTagPerfHisto.SetBinContent(ib, opt.bTagPerfResults[btagWP][systematic][ptbin][result])
        bTagPerfHisto.SetBinError(ib, opt.bTagPerfResults[btagWP][systematic][ptbin][result+'Uncertainty'])

    bTagPerfHisto.SetXTitle('#mu-jet #font[50]{p}_{T} [GeV]')

    if 'efficiency' in result: 
        bTagPerfHisto.SetYTitle('b-tag Efficiency #epsilon_{b}')
        bTagPerfHisto.SetMinimum(0.4)
        bTagPerfHisto.SetMaximum(1.1)
    else: 
        bTagPerfHisto.SetYTitle(btagWP+' Data/Sim. SF_{b}')
        bTagPerfHisto.SetMinimum(0.7)
        bTagPerfHisto.SetMaximum(1.3)

    return bTagPerfHisto

def makeBTagPerformancePlot(opt, btagWP, bTagPerfHistos, resultToPlot):

    ySize, ylow = 700, 0.52
 
    if resultToPlot!='both':
        ySize, ylow = 350, 0.03

    canvas = commonTools.bookCanvas('canvas', 700, ySize)
    canvas.cd()

    pad = []
    pad.append(commonTools.bookPad('pad0', 0.02, ylow, 0.98, 0.98))
    pad[0].Draw()

    if resultToPlot=='both': 
        pad.append(commonTools.bookPad('pad1', 0.02, 0.03, 0.98, 0.49))
        pad[1].Draw()

    for result in [ 'efficiency', 'scalefactor' ]:
        if result==resultToPlot or resultToPlot=='both':

            if result=='scalefactor' and resultToPlot=='both': pad[1].cd()
            else: pad[0].cd()

            drawOption = 'p'
            markerColor =  1
            for tag in bTagPerfHistos:
                markerStyle = 20
                for systematic in bTagPerfHistos[tag]:
                    styleOffset = 0
                    for btaghisto in [ 'efficiencyFit', 'efficiencyMC', 'scaleFactor' ]:
                        if result in btaghisto.lower():

                            bTagPerfHistos[tag][systematic][btaghisto].SetMarkerStyle(markerStyle+styleOffset)
                            bTagPerfHistos[tag][systematic][btaghisto].SetMarkerColor(markerColor)                
                            bTagPerfHistos[tag][systematic][btaghisto].Draw(drawOption)
                            drawOption = 'psame'
          
                            styleOffset = 4
                    markerStyle += 1
                markerColor +=1

    tagFlag = '-'.join(bTagPerfHistos.keys())
    systematicFlag = '-'.join(bTagPerfHistos[bTagPerfHistos.keys()[0]].keys())
     
    outputDir = '/'.join([ opt.plotsdir, opt.year, opt.method+'Results', tagFlag+'_'+systematicFlag ]) 
    os.system('mkdir -p '+outputDir+' ; cp ../../index.php '+opt.plotsdir)
    commonTools.copyIndexForPlots(opt.plotsdir, outputDir)

    canvas.Print(outputDir+'/'+btagWP+'.png')

def plotBTagPerformance(opt, resultToPlot='both', action='plot'):

    bTagPerfHistos = {}
    for btagWP in opt.btagWPs: bTagPerfHistos[btagWP] = {}

    opt2 = copy.deepcopy(opt)

    for tag in opt.tag.split('-'):

        rawTag = tag.split('__')[0]
        opt2.tag = rawTag
        getBTagPerfResults(opt2)

        for btagWP in opt2.bTagPerfResults:
            bTagPerfHistos[btagWP][rawTag] = {} 
            for systematic in opt2.bTagPerfResults[btagWP]:
                bTagPerfHistos[btagWP][rawTag][systematic] = {}

                if action=='plot':
                    for result in [ 'efficiencyMC', 'efficiencyFit', 'scaleFactor' ]:
                        if resultToPlot in result.lower() or resultToPlot=='both':
                            bTagPerfHistos[btagWP][rawTag][systematic][result] = fillBTagPerfHistogram(opt2, result, btagWP, systematic)

                else:
                    print '#####', btagWP, rawTag, systematic
                    bTagPerfShort = opt2.bTagPerfResults[btagWP][systematic]
                    for ptbin in bTagPerfShort.keys():
                        print '     ', ptbin, bTagPerfShort[ptbin]['efficiencyMC'], bTagPerfShort[ptbin]['efficiencyFit'], bTagPerfShort[ptbin]['scaleFactor']

                        
    if action=='plot':
        for btagWP in opt.btagWPs:
            makeBTagPerformancePlot(opt, btagWP, bTagPerfHistos[btagWP], resultToPlot)

def printBTagPerformance(opt):

    plotBTagPerformance(opt, action='print')

def plotBTagEfficiencies(opt):
 
    plotBTagPerformance(opt, resultToPlot='efficiency')

def plotBTagScaleFactors(opt):

    plotBTagPerformance(opt, resultToPlot='scalefactor')

### Store scale factores

def storeBTagScaleFactors(opt):

    getBTagPerfResults(opt)
    print 'please, complete me :('

### Analysis specific weights, efficiencies, scale factors, etc.

def kinematicWeights(opt):

    if 'mujetpteta' in opt.option.lower():
        print 'kinematicWeights in 2D not supported yet'
        exit()

    for year in opt.year.split('-'):

        outputDir = '/'.join([ opt.datadir, year, 'Kinematics' ])
        os.system('mkdir -p '+outputDir)

        samples, cuts, variables = commonTools.getDictionariesInLoop(opt.configuration, year, opt.tag, opt.sigset, 'variables')

        data, backgrounds = '', [ ]
        for sample in samples:
            if samples[sample]['isDATA']: data = sample
            else: backgrounds.append(sample)

        if 'mujetpt' in opt.option.lower() or 'mujeteta' in opt.option.lower():

            minMuJetPt, maxMuJetPt, maxMuJetEta, muJetPtEdges, cutLowerPtEdge = 999999., -999999., -10., [], {}

            for cut in cuts:

                cutList =  cuts[cut]['expr'].split(' ')
                cutLowerPt = 999999.
                nJetPtCuts, nJetEtaCuts = 0, 0
                for subcut in cutList:
                    if 'muJet_eta' in subcut and 'muJet_phi' not in subcut and nJetEtaCuts==0:
                        etaCut = float(subcut.split('<')[1].replace('=','').replace(')',''))
                        maxMuJetEta = max(maxMuJetEta, etaCut)
                        nJetEtaCuts += 1
                    elif 'muJet_pt' in subcut and ')' not in subcut and nJetPtCuts<2:
                        ptCut = float(subcut.replace('>','<').split('<')[1].replace('=','').replace(')',''))
                        minMuJetPt = min(minMuJetPt, ptCut)
                        maxMuJetPt = max(maxMuJetPt, ptCut)
                        cutLowerPt = min(cutLowerPt, ptCut)
                        if ptCut not in muJetPtEdges:
                            muJetPtEdges.append(ptCut)
                        nJetPtCuts += 1

                cutLowerPtEdge[cut] = cutLowerPt              

            minMuJetEta = -maxMuJetEta
            muJetPtEdges.sort()

            weightsHisto = { }

            if 'mujetpt' in opt.option.lower():
                histogramTitle = 'BACK-mujetpt'
                xBins = ( int(maxMuJetPt-minMuJetPt), minMuJetPt, maxMuJetPt )
                yBins = ( 1, minMuJetEta, maxMuJetEta )
            elif 'mujeteta' in opt.option.lower():
                histogramTitle = 'BACK-mujeteta'
                xBins = [ muJetPtEdges ]
                yBins = ( int((maxMuJetEta-minMuJetEta)/0.1), minMuJetEta, maxMuJetEta )
            else:
                print 'Error in kinematicWeights: no function variable chosen for corrections'
            for back in backgrounds:
                weightsHisto[back] = commonTools.bookHistogram(histogramTitle.replace('BACK',back), xBins, yBins)    

        inputFile = commonTools.openShapeFile(opt.shapedir, opt.year, opt.tag, opt.sigset, opt.fileset)


        for variable in variables:

            if variable.split('_')[0] not in opt.option.lower(): continue

            outputname = opt.tag.split('Prod')[0].replace('Kinematics','') + ':' + variable.split('_')[0]
            outputFile = ROOT.TFile(outputDir+'/'+outputname+'.root', 'recreate')

            for back in backgrounds:

                for cut in cuts: 
                    if 'cuts' not in variables[variable] or cut in variables[variable]['cuts']:

                        dataHisto = inputFile.Get('/'.join([ cut, variable, 'histo_'+data ])) ; dataHisto.SetDirectory(0)
                        backHisto = inputFile.Get('/'.join([ cut, variable, 'histo_'+back ])) ; backHisto.SetDirectory(0)

                        if 'skipfixspikes' not in opt.option:

                            spikeList = [ ]
                            for ib in range(1, backHisto.GetNbinsX()+1):
                                isSpike = True
                                for shift in [ ib-1, ib+1 ]:
                                    if backHisto.GetBinContent(shift)>0.:
                                        if backHisto.GetBinContent(ib)/backHisto.GetBinContent(shift)<1.1:
                                            isSpike = False
                                if isSpike: spikeList.append(ib)

                            for spike in spikeList:
                                spikeContent, spikeShifts = 0., 0
                                for shift in [ spike-1, spike+1 ]:
                                    if backHisto.GetBinContent(shift)>0.:
                                        spikeContent += backHisto.GetBinContent(shift)
                                        spikeShifts += 1
                                spikeContent /= spikeShifts
                                backHisto.SetBinContent(spike, spikeContent)

                        if 'mujetpt' in opt.option.lower() or 'mujeteta' in opt.option.lower():

                            dataHisto.Divide(backHisto) 

                            if 'mujetpt' in opt.option.lower():
                        
                                minPtFit, maxPtFit = dataHisto.GetBinLowEdge(1), dataHisto.GetBinLowEdge(dataHisto.GetNbinsX()+1)
                                ptfit = ROOT.TF1('ptfit', 'pol3', minPtFit, maxPtFit)
                                dataHisto.Fit('ptfit')

                            binx, biny, binz = ROOT.Long(), ROOT.Long(), ROOT.Long()

                            ptval  = cutLowerPtEdge[cut] + 0.1
                            etaval = weightsHisto[back].GetYaxis().GetBinCenter(1)

                            for ib in range(dataHisto.GetNbinsX()):

                                if 'mujetpt' in opt.option.lower():
                                    ptval  = dataHisto.GetBinCenter(ib+1)
                                    weight = ptfit.Eval(dataHisto.GetBinCenter(ib+1))

                                elif 'mujeteta' in opt.option.lower():
                                    etaval = dataHisto.GetBinCenter(ib+1)
                                    weight = dataHisto.GetBinContent(ib+1)

                                bin2D = weightsHisto[back].FindBin(ptval, etaval)
                                weightsHisto[back].GetBinXYZ(bin2D, binx, biny, binz)
                                weightsHisto[back].SetBinContent(binx, biny, weight)

                                if 'verbose' in opt.option:
                                    print back, cut, ptval, etaval, weight

                weightsHisto[back].Write()                        

            outputFile.Close()

