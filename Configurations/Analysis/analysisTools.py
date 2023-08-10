import os
import copy
import ROOT
import math
import PlotsConfigurations.Tools.commonTools  as commonTools
import PlotsConfigurations.Tools.latinoTools  as latinoTools
import PlotsConfigurations.Tools.combineTools as combineTools

### Analysis defaults

def setAnalysisDefaults(opt):

    opt.baseDir = os.getenv('PWD') 
    opt.treeName = 'btagana/ttree'

    opt.method = 'PtRel' if 'PtRel' in opt.tag else 'System8'

    opt.combineLocation = '/afs/cern.ch/work/s/scodella/SUSY/CMSSW_10_2_14/src' 

    if opt.year=='test' or opt.year=='*': opt.year = 'Summer22'

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

    opt.dataConditionScript = '../../../LatinoAnalysis/NanoGardener/python/data/dataTakingConditionsAnalyzer.py'

    if 'Summer22' in opt.year:
        opt.simulationPileupFile = 'pileup_DistrWinter22_Run3_2022_LHC_Simulation_10h_2h.root'
        if opt.year=='Summer22EE': opt.dataPileupFile = '/afs/cern.ch/work/s/scodella/BTagging/CMSSW_10_6_28/src/LatinoAnalysis/NanoGardener/python/data/PUweights/2022/2022EFG.root'
        elif opt.year=='Summer22': opt.dataPileupFile = '/afs/cern.ch/work/s/scodella/BTagging/CMSSW_10_6_28/src/LatinoAnalysis/NanoGardener/python/data/PUweights/2022/2022CD.root'

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

def mergeLightShapes(opt):

    if 'PtRelLight' not in opt.tag:
        print 'Please choose a tag (PtRelLightKinematics or PtRelLightTemplates)'
        exit()

    outtag = opt.tag.replace('Light', 'MergedLight')

    samples, cuts, variables = commonTools.getDictionariesInLoop(opt.configuration, opt.year, opt.tag, opt.sigset, 'variables')

    for sample in samples:    

        inputFile  = commonTools.openSampleShapeFile(opt.shapedir, opt.year, opt.tag, sample)
        outputFile = commonTools.openSampleShapeFile(opt.shapedir, opt.year, opt.tag.replace('Light', 'MergedLight'), sample, 'recreate')

        for cut in cuts:

            outputFile.mkdir(cut)

            mergedShapes = {}

            for variable in variables:
                if 'cuts' not in variables[variable] or cut in variables[variable]['cuts']:

                    shapeName = '_'.join([ variableString for variableString in variable.split('_') if not variableString.isdigit() ])
                    if shapeName not in mergedShapes:
                        mergedShapes[shapeName] = inputFile.Get('/'.join([ cut, variable, 'histo_'+sample ]))          
                    else:
                        mergedShapes[shapeName].Add(inputFile.Get('/'.join([ cut, variable, 'histo_'+sample ])))
            
            for variable in mergedShapes:
                
                outputFile.mkdir(cut+'/'+variable)
                outputFile.cd(cut+'/'+variable)

                mergedShapes[variable].Write('histo_'+sample)

        inputFile.Close()
        outputFile.Close()
            

def mergeLightKinematics(opt):

    opt.tag = 'PtRelLightKinematics' if 'PtRelLightKinematics' not in opt.tag else opt.tag
    mergeLightShapes(opt)

def mergeLightTemplates(opt):
    
    opt.tag = 'PtRelLightTemplates' if 'PtRelLightTemplates' not in opt.tag else opt.tag
    mergeLightShapes(opt)

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

### Working points

def workingPoints(opt): 

    tag = 'WorkingPoints' if 'WorkingPoints' not in opt.tag else opt.tag
    opt.tag = opt.year+tag
    opt.sigset='MCQCD' if 'SM' in opt.sigset or opt.sigset=='MC' else opt.sigset

    samples = {}
    if os.path.exists(commonTools.getCfgFileName(opt,'samples')):
        handle = open(commonTools.getCfgFileName(opt,'samples'),'r')
        exec(handle)
        handle.close()

    wpSamples = []
    for sample in samples:
        if not samples[sample]['isDATA']: wpSamples.append(sample)

    if len(wpSamples)!=1: 
        print 'workingPoints error: too many samples selected ->', wpSamples
        exit()

    inputFile = ROOT.TFile.Open('/'.join([ opt.shapedir, opt.year, tag.split('_')[0], 'Samples', 'plots_'+opt.tag.split('_')[0]+'_ALL_'+wpSamples[0]+'.root' ]), 'read')

    discriminantDone = []

    for btagwp in bTagWorkingPoints.keys():
        if bTagWorkingPoints[btagwp]['discriminant'] not in discriminantDone:

            bJetDisc = inputFile.Get('QCD/Jet_'+bTagWorkingPoints[btagwp]['discriminant']+'_5_0/histo_'+wpSamples[0])
            lJetDisc = inputFile.Get('QCD/Jet_'+bTagWorkingPoints[btagwp]['discriminant']+'_0_0/histo_'+wpSamples[0])

            for ijet in range(1, nJetMax):
                bJetDisc.Add(inputFile.Get('QCD/Jet_'+bTagWorkingPoints[btagwp]['discriminant']+'_5_'+str(ijet)+'/histo_'+wpSamples[0]))
                lJetDisc.Add(inputFile.Get('QCD/Jet_'+bTagWorkingPoints[btagwp]['discriminant']+'_0_'+str(ijet)+'/histo_'+wpSamples[0]))

            if 'noprint' not in opt.option:
                print '\n\nWorking Points for', btagwp[:-1]

            workingPointName = [ 'Loose', 'Medium', 'Tight', 'VeryTight', 'SuperTight' ]
            workingPointLimit = [ 0.1, 0.01, 0.001, 0.0005, 0.0001 ]

            oldWorkingPoint = []
            for wp in workingPointName:
                if btagwp[:-1]+wp[:1] in bTagWorkingPoints: oldWorkingPoint.append(float(bTagWorkingPoints[btagwp[:-1]+wp[:1]]['cut']))
                else: oldWorkingPoint.append(0.9) 

            integralLightJets  = lJetDisc.Integral(0, lJetDisc.GetNbinsX())
            integralBottomJets = bJetDisc.Integral(0, bJetDisc.GetNbinsX())
 
            if 'csv' in opt.option:
                print '   ', btagwp[:-1],
            elif 'yml' in opt.option:
                print btagwp[:-1]+':'

            for wp in range(len(workingPointName)):

                mistagRateDistance =  999.
                binAtWorkingPoint  = -999

                for ib in range(1, bJetDisc.GetNbinsX()+1):

                    mistagRate = lJetDisc.Integral(ib, lJetDisc.GetNbinsX())/integralLightJets

                    if abs(mistagRate-workingPointLimit[wp])<mistagRateDistance: 

                        mistagRateDistance = abs(mistagRate-workingPointLimit[wp])
                        binAtWorkingPoint = ib

                if 'noprint' not in opt.option:
                    print '   ', workingPointName[wp], 'working point:', lJetDisc.GetBinLowEdge(binAtWorkingPoint), '(', lJetDisc.GetBinLowEdge(binAtWorkingPoint-1), ',', lJetDisc.GetBinLowEdge(binAtWorkingPoint+1), ')'
                    print '        MistagRate:', lJetDisc.Integral(binAtWorkingPoint, lJetDisc.GetNbinsX())/integralLightJets, '(', lJetDisc.Integral(binAtWorkingPoint-1, lJetDisc.GetNbinsX())/integralLightJets, ', ', lJetDisc.Integral(binAtWorkingPoint+1, lJetDisc.GetNbinsX())/integralLightJets, ') over', integralLightJets
                    print '        Efficiency:', bJetDisc.Integral(binAtWorkingPoint, bJetDisc.GetNbinsX())/integralBottomJets, '(', bJetDisc.Integral(binAtWorkingPoint-1, bJetDisc.GetNbinsX())/integralBottomJets, ', ', bJetDisc.Integral(binAtWorkingPoint+1, bJetDisc.GetNbinsX())/integralBottomJets, ') over', integralBottomJets

                    binOldWorkingPoint = lJetDisc.FindBin(oldWorkingPoint[wp])
                    print '        OldWorkingPoint', oldWorkingPoint[wp], lJetDisc.Integral(binOldWorkingPoint, lJetDisc.GetNbinsX())/integralLightJets, bJetDisc.Integral(binOldWorkingPoint, lJetDisc.GetNbinsX())/integralBottomJets, '\n'

                elif 'csv' in opt.option:
                    print lJetDisc.GetBinLowEdge(binAtWorkingPoint), 
                    print round((100.*bJetDisc.Integral(binAtWorkingPoint, bJetDisc.GetNbinsX())/integralBottomJets),1),
                    print round((100.*lJetDisc.Integral(binAtWorkingPoint, lJetDisc.GetNbinsX())/integralLightJets),1 if workingPointName[wp]=='Loose' else 2), 
                elif 'yml' in opt.option:
                    print '   ',workingPointName[wp][:1]+':'
                    print '       ', 'eff:', round((100.*bJetDisc.Integral(binAtWorkingPoint, bJetDisc.GetNbinsX())/integralBottomJets),1)
                    print '       ', 'wp:', lJetDisc.GetBinLowEdge(binAtWorkingPoint) 


                if btagwp[:-1]+workingPointName[wp][:1] not in bTagWorkingPoints:
                    bTagWorkingPoints[btagwp[:-1]+workingPointName[wp][:1]] = {}
                    bTagWorkingPoints[btagwp[:-1]+workingPointName[wp][:1]]['discriminant'] = bTagWorkingPoints[btagwp]['discriminant']

                bTagWorkingPoints[btagwp[:-1]+workingPointName[wp][:1]]['cut'] = str(lJetDisc.GetBinLowEdge(binAtWorkingPoint))

            if 'csv' in opt.option: print ''

            discriminantDone.append(bTagWorkingPoints[btagwp]['discriminant'])

    if 'noprint' not in opt.option:
        print '\n\nbTagWorkingPoints =', bTagWorkingPoints, '\n\n' 

### Analysis specific weights, efficiencies, scale factors, etc.

import sys
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import McM

def getGeneratorParametersFromMCM(mcm_query):

    mcm = McM(dev=False)
    requests = mcm.get('requests', None, mcm_query)
    nValidRequests = 0
    for request in requests:
        if request['status']=='done' and ('GEN' in request['prepid'] or 'GS' in request['prepid']):
            xSec = request['generator_parameters'][0]['cross_section']
            fEff = request['generator_parameters'][0]['filter_efficiency']
            nValidRequests += 1

    if nValidRequests==1: return [ xSec, fEff ]
    elif nValidRequests==0: print 'No request for', mcm_query, 'query found in McM'
    else: print 'Too many requests for', mcm_query, 'query found in McM'
    return [ -1., -1. ]

def ptHatWeights(opt):

    opt.tag = opt.year+'PtHatWeights'
    opt.sigset = 'MC'

    samples = {}
    if os.path.exists(commonTools.getCfgFileName(opt,'samples')):
        handle = open(commonTools.getCfgFileName(opt,'samples'),'r')
        exec(handle)
        handle.close()

    for sample in samples:
 
        ptHatBin = sample.split('_')[-1]
        events = ROOT.TChain(opt.treeName)
        for tree in samples[sample]['name']: events.Add(tree.replace('#',''))
            
        if 'QCDMu_' in sample:
            qcdMuPtHatBins[ptHatBin]['events'] = str(events.GetEntries())
            if not 'xSec' in qcdMuPtHatBins[ptHatBin]: 
             xSec, fEff = getGeneratorParametersFromMCM('dataset_name=QCD_*'+ptHatBin+'_MuEnrichedPt5_*&prepid=BTV*'+opt.year+'G*')
             qcdMuPtHatBins[ptHatBin]['xSec'] = str(xSec)+'*'+str(fEff)
            else:
                genPars = qcdMuPtHatBins[ptHatBin]['xSec'].split('*')
                xSec = float(genPars[0])
                fEff = 1. if len(genPars)==1 else float(genPars[1])
            qcdMuPtHatBins[ptHatBin]['weight'] = str(1000.*xSec*fEff/events.GetEntries())
        elif 'QCD_' in sample:
            qcdPtHatBins[ptHatBin]['events'] = str(events.GetEntries())
            if not 'xSec' in qcdPtHatBins[ptHatBin]:
                xSec, fEff = getGeneratorParametersFromMCM('dataset_name=QCD_*'+ptHatBin+'_Tune*&prepid=BTV*'+opt.year+'G*')
                qcdPtHatBins[ptHatBin]['xSec'] = str(xSec)+'*'+str(fEff)
            else:
                genPars = qcdPtHatBins[ptHatBin]['xSec'].split('*')
                xSec = float(genPars[0])
                fEff = 1. if len(genPars)==1 else float(genPars[1])
            qcdPtHatBins[ptHatBin]['weight'] = str(1000.*xSec*fEff/events.GetEntries())

    print '\nqcdMuPtHatBins =', qcdMuPtHatBins
    print '\nqcdPtHatBins =', qcdPtHatBins, '\n'

def triggerPrescales(opt):

    campaigns = opt.year.split('-')

    mergeJobs = {}

    for campaign in campaigns:

        opt.tag = campaign+opt.tag

        samples = {}
        if os.path.exists(commonTools.getCfgFileName(opt,'samples')):
            handle = open(commonTools.getCfgFileName(opt,'samples'),'r')
            exec(handle)
            handle.close()

        commandList = [ opt.dataConditionScript ]
        commandList.append('--action=ps')
        commandList.append('--years='+campaignRunPeriod['year'])
        commandList.append('--periods='+campaignRunPeriod['period'])
        commandList.append('--outputDir='+commonTools.mergeDirPaths(opt.baseDir,opt.datadir+'/'+campaign))

        for trigger in triggerInfos:
            for hltpath in [ trigger, triggerInfos[trigger]['jetTrigger'] ]:
                if 'hltpath:' in opt.option and hltpath not in opt.option: continue
                if 'hltpathveto:' in opt.option and hltpath in opt.option: continue
                if opt.interactive:
                    os.system(' '.join(commandList)+' --hltPaths=HLT_'+hltpath)
                else:
                    mergeJobs[campaign+'_'+hltpath] = commonTools.cdWorkDir(opt)+' '.join(commandList)+' --hltPaths=HLT_'+hltpath

    if len(mergeJobs.keys())>0:
            latinoTools.submitJobs(opt, 'prescales', campaign+'Prescales', mergeJobs, 'Targets', True, 1)

def kinematicWeights(opt):

    if 'jetpteta' in opt.option.lower():
        print 'kinematicWeights in 2D not supported yet'
        exit()

    if 'jetpt' in opt.option.lower() or 'jeteta' in opt.option.lower():
        print 'kinematicWeights only supported for jetpt and jeteta'
        exit()

    samples = {}
    if os.path.exists(commonTools.getCfgFileName(opt,'samples')):
        handle = open(commonTools.getCfgFileName(opt,'samples'),'r')
        exec(handle)
        handle.close() 

    jetPtEdges = []
    for jetBin in jetPtBins:
        for edge in range(2):
            if float(jetPtBins[jetBin][edge]) not in jetPtEdges:
                jetPtEdges.append(float(jetPtBins[jetBin][edge])) 
    jetPtEdges.sort()

    for year in opt.year.split('-'):

        outputDir = '/'.join([ opt.datadir, year, 'Kinematics' ])
        os.system('mkdir -p '+outputDir)

        samples, cuts, variables = commonTools.getDictionariesInLoop(opt.configuration, year, opt.tag, opt.sigset, 'variables')

        data, backgrounds = 'DATA', [ ]
        for sample in samples:
            if samples[sample]['isDATA']: data = sample
            else: backgrounds.append(sample)

        data_File = commonTools.openSampleShapeFile(opt.shapedir, opt.year, opt.tag.replace('MergedLight','').split(':')[0], data) 

        for variable in variables: # There should be just one
            if variable.split('_')[0] not in opt.option.lower(): continue

            if 'jetpt' in variable:
                xBins = ( int(maxJetPt-minJetPt), minJetPt, maxJetPt )
                yBins = ( 1, -1.*float(maxJetEta), float(maxJetEta) )
            elif 'jeteta' in variable:
                xBins = [ jetPtEdges ]
                yBins = ( int((2.*float(maxJetEta))/0.1), 1.*float(maxJetEta), float(maxJetEta) )
            else:
                print 'Error in kinematicWeights: no function variable chosen for corrections'
                exit()

            for back in backgrounds:

                inputFile = commonTools.openSampleShapeFile(opt.shapedir, opt.year, opt.tag, back)

                outputname = opt.tag.split('Prod')[0].replace('Kinematics','').replace('MergedLight','') + '_' + back + ':' + variable.split('_')[0]
                outputFile = commonTools.openRootFile(outputDir+'/'+outputname+'.root', 'recreate')

                weightsHisto = commonTools.bookHistogram(opt.option.lower(), xBins, yBins)    

                for cut in cuts: 
                    if 'cuts' not in variables[variable] or cut in variables[variable]['cuts']:

                        dataHisto = data_File.Get('/'.join([ cut, variable.replace('mujet','lightjet'), 'histo_'+data ])) ; dataHisto.SetDirectory(0)
                        backHisto = inputFile.Get('/'.join([ cut, variable                            , 'histo_'+back ])) ; backHisto.SetDirectory(0)

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

                        if 'jetpt' in opt.option.lower() or 'jeteta' in opt.option.lower():

                            dataHisto.Divide(backHisto) 

                            if 'jetpt' in opt.option.lower():
                        
                                minPtFit, maxPtFit = dataHisto.GetBinLowEdge(1), dataHisto.GetBinLowEdge(dataHisto.GetNbinsX()+1)
                                ptfit = ROOT.TF1('ptfit', 'pol3', minPtFit, maxPtFit)
                                dataHisto.Fit('ptfit')

                            binx, biny, binz = ROOT.Long(), ROOT.Long(), ROOT.Long()

                            ptval  = cutLowerPtEdge[cut] + 0.1
                            etaval = weightsHisto.GetYaxis().GetBinCenter(1)

                            for ib in range(dataHisto.GetNbinsX()):

                                if 'jetpt' in opt.option.lower():
                                    ptval  = dataHisto.GetBinCenter(ib+1)
                                    weight = ptfit.Eval(dataHisto.GetBinCenter(ib+1))

                                elif 'jeteta' in opt.option.lower():
                                    etaval = dataHisto.GetBinCenter(ib+1)
                                    weight = dataHisto.GetBinContent(ib+1)

                                bin2D = weightsHisto.FindBin(ptval, etaval)
                                weightsHisto.GetBinXYZ(bin2D, binx, biny, binz)
                                weightsHisto.SetBinContent(binx, biny, weight)

                                if 'verbose' in opt.option:
                                    print back, cut, ptval, etaval, weight

                inputFile.Close()

                outputFile.cd()
                weightsHisto.Write()                        
                outputFile.Close()

        data_File.Close()

