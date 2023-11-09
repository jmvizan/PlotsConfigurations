import os
import copy
import ROOT
import math
import PlotsConfigurations.Tools.commonTools  as commonTools
import PlotsConfigurations.Tools.latinoTools  as latinoTools
import PlotsConfigurations.Tools.combineTools as combineTools

### Analysis defaults

def getCampaignParameters(opt):

    origTag = opt.tag
    opt.tag = opt.year+opt.tag

    samples = {}

    if os.path.exists(commonTools.getCfgFileName(opt,'samples')):
        handle = open(commonTools.getCfgFileName(opt,'samples'),'r')
        exec(handle)
        handle.close()

    opt.tag = origTag
    if opt.year=='test': opt.year = opt.campaign
    opt.btagWPs = bTagWorkingPoints.keys()
    opt.ptBins = jetPtBins.keys()
    opt.Selections = systematicVariations

    if opt.action=='ptHatWeights':
        opt.samples = samples
        opt.qcdMuPtHatBins = qcdMuPtHatBins
        opt.qcdPtHatBins = qcdPtHatBins 

    elif opt.action=='workingPoints':
        opt.samples = samples
        opt.nJetMax = nJetMax
        opt.bTagWorkingPoints = bTagWorkingPoints

    elif opt.action=='frameworkValidation':
        opt.samples = samples.keys()        
        opt.triggerInfos = triggerInfos

    elif opt.action=='kinematicWeights':
        opt.jetPtBins = jetPtBins
        opt.minJetPt  = minJetPt 
        opt.maxJetPt  = maxJetPt
        opt.maxJetEta = float(maxJetEta)

def setAnalysisDefaults(opt):

    opt.baseDir = os.getenv('PWD') 
    opt.treeName = 'btagana/ttree'

    opt.dataConditionScript = '../../../LatinoAnalysis/NanoGardener/python/data/dataTakingConditionsAnalyzer.py'
    opt.combineLocation = '/afs/cern.ch/work/s/scodella/SUSY/CMSSW_10_2_14/src' 

    if opt.action=='ptHatWeights':
        opt.tag = 'PtHatWeights'
        opt.sigset = 'MC'

    elif opt.action=='workingPoints':
        if 'WorkingPoints' not in opt.tag: opt.tag = 'WorkingPoints'
        opt.sigset='MCQCD' if 'SM' in opt.sigset or opt.sigset=='MC' else opt.sigset

    getCampaignParameters(opt) 

### Shapes, kinematic weights and prefit plots

def bTagPerfShapes(opt, tag, action):

    for selection in opt.Selections:

        sel = 'Central' if selection=='' else selection
        if 'vetosel' in opt.option:
            if sel in opt.option: continue
        elif 'sel' in opt.option and sel not in opt.option: continue  

        opt2 = copy.deepcopy(opt)
        opt2.tag = tag.replace(tag.split('.')[0], tag.split('.')[0]+selection)

        sigsets = [ 'MC', 'Data' ] if opt.sigset=='SM' else [ opt.sigset ]
        for sigset in sigsets:

            opt2.sigset = sigset
            if sigset=='Data' and '.' in tag and 'Light' not in tag: opt2.tag = opt2.tag.split('.')[0]
            if sigset=='Data' and 'JEU' in selection: continue
            if sigset=='MC' and 'Light' in opt.tag: opt2.batchQueue = 'testmatch'
            if 'shapes' in action: latinoTools.shapes(opt2)
            elif 'mergesingle' in action: 
                latinoTools.mergesingle(opt2)
                if 'Light' in opt2.tag: mergeLightShapes(opt2)
            elif 'resubmitShapes' in action: latinoTools.remakeMissingShapes(opt2, 'resubmit')
            elif 'recoverShapes' in action: latinoTools.remakeMissingShapes(opt2, 'recover')

def makeShapes(opt):

    for tag in opt.tag.split('-'):
        bTagPerfShapes(opt, tag, 'shapes')

def mergeShapes(opt):

    for tag in opt.tag.split('-'):
        bTagPerfShapes(opt, tag, 'mergesingle')

def resubmitShapes(opt):
    
    for tag in opt.tag.split('-'):
        bTagPerfShapes(opt, tag, 'resubmitShapes')

def recoverShapes(opt):

    for tag in opt.tag.split('-'):
        bTagPerfShapes(opt, tag, 'recoverShapes')

def mergeLightShapes(opt):

    if 'PtRelLight' not in opt.tag:
        print 'Please choose a tag (PtRelLightKinematics or PtRelLightTemplates)'
        exit()

    outtag = opt.tag.replace('Light', 'MergedLight')

    samples, cuts, variables, nuisances = commonTools.getDictionariesInLoop(opt.configuration, opt.year, opt.tag, opt.sigset, 'nuisances')

    for sample in samples:    

        inputFile  = commonTools.openSampleShapeFile(opt.shapedir, opt.year, opt.tag, sample)
        outputFile = commonTools.openSampleShapeFile(opt.shapedir, opt.year, outtag, sample, 'recreate')

        for cut in cuts:

            outputFile.mkdir(cut)

            mergedShapes = {}

            for variable in variables:
                if 'cuts' not in variables[variable] or cut in variables[variable]['cuts']:

                    shapeName = '_'.join([ variableString for variableString in variable.split('_') if not variableString.isdigit() ])
                    if shapeName not in mergedShapes: mergedShapes[shapeName] = {}

                    if 'histo_'+sample not in mergedShapes[shapeName]:
                        mergedShapes[shapeName]['histo_'+sample] = inputFile.Get('/'.join([ cut, variable, 'histo_'+sample ]))          
                    else:
                        mergedShapes[shapeName]['histo_'+sample].Add(inputFile.Get('/'.join([ cut, variable, 'histo_'+sample ])))
            
                    for nuisance in nuisances:
                        if nuisance!='stat' and nuisances[nuisance]['type']=='shape':
                            if 'cuts' not in nuisances[nuisance] or cut in nuisances[nuisance]['cuts']:
                                if sample in nuisances[nuisance]['samples']:
                                    for variation in [ 'Up', 'Down' ]:
                                           
                                        nuisanceHistoName = 'histo_'+sample+'_'+nuisances[nuisance]['name']+variation
                                        if nuisanceHistoName not in mergedShapes[shapeName]:
                                            mergedShapes[shapeName][nuisanceHistoName] = inputFile.Get('/'.join([ cut, variable, nuisanceHistoName ]))
                                        else:
                                            mergedShapes[shapeName][nuisanceHistoName].Add(inputFile.Get('/'.join([ cut, variable, nuisanceHistoName ])))

            for variable in mergedShapes:
                
                outputFile.mkdir(cut+'/'+variable)
                outputFile.cd(cut+'/'+variable)

                for histo in mergedShapes[variable]:
                    mergedShapes[variable][histo].Write(histo)

        inputFile.Close()
        outputFile.Close()

def shapesForFit(opt):

    if 'PtRel' in opt.tag: ptRelInput(opt)
    else: system8Input(opt) 

def ptRelInput(opt):

    ptRelTemplateFileName = './PtRelTools/Templates/PtRel_TemplatesAll_PS'+opt.year+'_KinEtaAfterPtBinsCentral_LowPtAwayTrgConf_Run2016Production.root'
    if 'nolight' in opt.option: ptRelTemplateFileName = ptRelTemplateFileName.replace('TemplatesAll', 'Templates')

    ptRelTemplateFile = ROOT.TFile(ptRelTemplateFileName, 'recreate')

    samples, cuts, variables, nuisances = commonTools.getDictionaries(opt)

    for datatype in [ 'MuEnriched', 'Inclusive' ]:
        if datatype=='Inclusive' and 'nolight' in opt.option: continue
        for sigset in [ 'MC', 'Data' ]:
            for selection in opt.Selections:

                sel = 'Central' if selection=='' else selection
                fromCentral = False
                if sigset=='Data' and 'JEU' in selection: fromCentral = True
                if datatype=='Inclusive' and 'AwayJet' in selection: fromCentral = True

                opt2 = copy.deepcopy(opt)
                if not fromCentral: opt2.tag = opt.tag.replace(opt.tag.split('.')[0], opt.tag.split('.')[0]+selection)
                if sigset=='Data' and datatype=='MuEnriched': opt2.tag = opt2.tag.split('.')[0]
                if datatype=='Inclusive': opt2.tag = opt2.tag.replace('Templates','MergedLightTemplates').replace('mujet','lightjet')
                opt2.sigset = sigset

                samples, cuts, variables = commonTools.getDictionariesInLoop(opt2.configuration, opt2.year, opt2.tag, opt2.sigset, 'variables')            
          
                for sample in samples:

                    if datatype=='Inclusive':
                        if not commonTools.foundSampleShapeFile(opt2.shapedir, opt2.year, opt2.tag, sample) or opt.reset:
                            opt2.tag = opt2.tag.replace('MergedLight','Light')
                            mergeLightShapes(opt2) 
                            opt2.tag = opt2.tag.replace('PtRelLight','PtRelMergedLight')

                    inputTemplateFile = commonTools.openSampleShapeFile(opt2.shapedir, opt2.year, opt2.tag, sample)
                    ptRelTemplateFile.cd()

                    for cut in cuts:
                        for variable in variables:
                            if 'cuts' not in variables[variable] or cut in variables[variable]['cuts']:
 
                                histoName = '/'.join([ cut, variable, 'histo_' + sample ])
                                template = inputTemplateFile.Get(histoName)

                                dataset = 'BTagMu' if sample=='DATA' else 'QCDMu' if 'jets' in sample else sample.replace('MET','HT')
                                tagCondition = 'Tag' if 'Pass' in variable else 'Untag'
                                templateNameList = [ 'PtRel', dataset, cut.replace('to',''), 'anyEta', sel, variable.split('_')[1], tagCondition ]
                                if sample=='bjets' or sample=='cjets': templateNameList.append(sample.replace('jets',''))
                                elif sample=='ljets': templateNameList.append('lg')
                                elif sample!='DATA': templateNameList.append('trk')
                                templateName = '_'.join(templateNameList)

                                if datatype=='MuEnriched':
                                    template.SetName(templateName)
                                    template.SetTitle(templateName)
                                    template.Write()
                          
                                elif datatype=='Inclusive':
                                    for btagWP in opt.btagWPs:
                                        for btagCut in [ '_Tag', '_Untag' ]:
                                            template.SetName(templateName.replace(variable.split('_')[1]+'_'+tagCondition,btagWP+btagCut))
                                            template.SetTitle(templateName.replace(variable.split('_')[1]+'_'+tagCondition,btagWP+btagCut))
                                            template.Write()

                                if selection=='':
                                    for nuisance in nuisances:
                                        if nuisance!='stat' and nuisances[nuisance]['type']=='shape':
                                            if 'cuts' not in nuisances[nuisance] or cut in nuisances[nuisance]['cuts']:
                                                for variation in [ 'Up', 'Down' ]:

                                                    if sample in nuisances[nuisance]['samples']:
                                                        templateNuisance = inputTemplateFile.Get(histoName + '_' + nuisances[nuisance]['name'] + variation)
                                                    else: templateNuisance = inputTemplateFile.Get(histoName)
                                                    templateNuisanceName = templateName.replace('Central',nuisances[nuisance]['name'] + variation)

                                                    if datatype=='MuEnriched':
                                                        templateNuisance.SetName(templateNuisanceName)
                                                        templateNuisance.SetTitle(templateNuisanceName)
                                                        templateNuisance.Write()

                                                    elif datatype=='Inclusive':
                                                        for btagWP in opt.btagWPs:
                                                            for btagCut in [ '_Tag', '_Untag' ]:
                                                                templateNuisance.SetName(templateNuisanceName.replace(variable.split('_')[1]+'_'+tagCondition,btagWP+btagCut))
                                                                templateNuisance.SetTitle(templateNuisanceName.replace(variable.split('_')[1]+'_'+tagCondition,btagWP+btagCut))
                                                                templateNuisance.Write()

def system8Input(opt):

    print 'Please, complete me!'

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

def frameworkValidation(opt):

    if 'JEU' in opt.tag:
        print 'frameworkValidation: JEU in PtRelTools not up-to-date, exiting'
        exit()

    if 'Light' in opt.tag and 'Merged' not in opt.tag:
        mergeLightShapes(opt)
        opt.tag = opt.tag.replace('Light', 'MergedLight')

    ptRelToolsDir = '/afs/cern.ch/work/s/scodella/BTagging/CMSSW_10_6_28/src/PlotsConfigurations/Configurations/Analysis/PtRelTools/Templates/Histograms/'

    histoToCompare = { 'LightKinematics'   : { 'jetpt'         : [ 'jetPt_DATASET_PTTBIN_anyEta_TRIGGER_SELECTION',                    'PTBIN/lightjetpt_PTBIN/histo_SAMPLE'       ] },
                       'PtRelKinematics'   : { 'jetpt'         : [ 'jetPt_DATASET_PTTBIN_anyEta_TRIGGER_SELECTION',                    'PTBIN/mujetpt_PTBIN/histo_SAMPLE'          ] },
                       'System8Kinematics' : { 'jetpt'         : [ 'jetPt_DATASET_PTTBIN_anyEta_TRIGGER_SELECTION',                    'PTBIN/mujetpt_PTBIN/histo_SAMPLE'          ] },
                       'LightTemplates'    : { 'ptrel'         : [ 'PtRel_DATASET_PTTBIN_anyEta_TRIGGER_SELECTION_DeepJetM_Untag_trk', 'PTBIN/ptrel_PTBIN/histo_SAMPLE'            ] },
                       'PtRelTemplates'    : { 'ptrelpass'     : [ 'PtRel_DATASET_PTTBIN_anyEta_TRIGGER_SELECTION_TAGWP_TagFLAVOUR',   'PTBIN/ptrel_TAGWP_Pass/histo_SAMPLE'       ],
                                               'ptrelfail'     : [ 'PtRel_DATASET_PTTBIN_anyEta_TRIGGER_SELECTION_TAGWP_UntagFLAVOUR', 'PTBIN/ptrel_TAGWP_Fail/histo_SAMPLE'       ] },
                       'System8Templates'  : { 'ptrel'         : [ 'n_pT_PTTBIN_anyEta_TRIGGER_SELECTIONFLAVOUR',                      'PTBIN/ptrel/histo_SAMPLE'                  ],
                                               'ptrelpass'     : [ 'ntag_pT_PTTBIN_anyEta_TRIGGER_SELECTION_TAGWPFLAVOUR',             'PTBIN/ptrel_TAGWP/histo_SAMPLE'            ],
                                               'ptrelaway'     : [ 'p_pT_PTTBIN_anyEta_TRIGGER_SELECTIONFLAVOUR',                      'PTBIN_AwayJetTag/ptrel/histo_SAMPLE'       ],
                                               'ptrelawaypass' : [ 'ptag_pT_PTTBIN_anyEta_TRIGGER_SELECTION_TAGWPFLAVOUR',             'PTBIN_AwayJetTag/ptrel_TAGWP/histo_SAMPLE' ] } }

    keyTag = ''
    for key in histoToCompare:
        if key in opt.tag: keyTag = key
    if keyTag=='': 
        print 'frameworkValidation: invalid keyTag, exiting'
        exit()

    selection = 'Central'
    for sel in opt.Selections:
        if sel in opt.tag: 
            if sel=='AwayJetUp': selection = 'JBPT'
            elif sel=='AwayJetDown': selection = 'JBPL'
            elif sel=='MuPtUp': selection = 'MuPt8'
            elif sel=='MuPtDown': selection = 'MuPt6'
            elif sel=='MuDRUp': selection = 'MuDRPlus'
            elif sel=='MuDRDown': selection = 'MuDRMinus'

    for sample in opt.samples:

        if sample=='JetMET': 
            ptRelToolsFileName = 'PtRel_LightHistograms_Run2022FG_LowPtAwayTrgConf.root'
            dataset = 'JetHT'
        elif sample=='QCD': 
            ptRelToolsFileName = 'PtRel_LightHistograms_PT-80to120_LowPtAwayTrgConf.root'
            dataset = 'QCD'
        elif 'PtRel' in opt.tag:
            if sample=='DATA': 
                ptRelToolsFileName = 'PtRel_Histograms_BTagMu_Run2022FG_LowPtAwayTrgConf.root'
                dataset = 'BTagMu'
            else:
                ptRelToolsFileName = 'PtRel_Histograms_QCDMu_PT-80to120_LowPtAwayTrgConf.root'
                dataset = 'QCDMu'
        elif 'System8' in opt.tag:
            if sample=='DATA':  
                ptRelToolsFileName = 'System8_Histograms_Run2022FG_LowPtAway.root'
                dataset = 'BTagMu'
            else: 
                ptRelToolsFileName = 'System8_Histograms_PT-80to120_LowPtAway.root'
                dataset = 'QCDMu'

        inputFile = [ commonTools.openRootFile(ptRelToolsDir+ptRelToolsFileName), commonTools.openSampleShapeFile(opt.shapedir, opt.year, opt.tag, sample) ]

        flavour = ''
        if sample=='light': flavour = '_cl'
        elif sample=='ljets': flavour = '_lg'
        elif 'jets' in sample: flavour = '_'+sample.replace('jets','')

        for ptbin in opt.ptBins:
            
            for tr in opt.triggerInfos:
                if float(ptbin.split('Pt')[1].split('to')[0])<float(opt.triggerInfos[tr]['jetPtRange'][1]) and float(opt.triggerInfos[tr]['jetPtRange'][0])<float(ptbin.split('to')[1]):
                    trigger = tr.replace('BTagMu_AK4','').replace('_Mu5','')                  

            for histokey in histoToCompare[keyTag]:

                btagWPList = opt.btagWPs if 'pass' in histokey or 'fail' in histokey else [ '' ] 
                for wp in btagWPList:
                    if 'VT' in wp or 'VVT' in wp or 'JBPT' in wp: continue 

                    histos = []
                    for his in range(2):
                        histoName = histoToCompare[keyTag][histokey][his].replace('DATASET',dataset).replace('PTTBIN',ptbin.replace('to','')).replace('TRIGGER',trigger).replace('SELECTION',selection).replace('FLAVOUR',flavour).replace('PTBIN',ptbin).replace('SAMPLE',sample).replace('TAGWP',wp).replace('10001400','1000')
                        histos.append(inputFile[his].Get(histoName))

                    if histos[0].GetEntries()==0.: continue

                    if sample!='DATA' and sample!='JetMET':
                        weight0 = 0.39821973443 if 'LightTemplates' in opt.tag else histos[0].Integral(-1,-1)/histos[0].GetEntries()
                        histos[0].Scale(1./weight0)

                    lastBin0 = histos[0].GetBinContent(histos[0].GetNbinsX())+histos[0].GetBinContent(histos[0].GetNbinsX()+1)
                    histos[0].SetBinContent(histos[0].GetNbinsX(), lastBin0)

                    if abs(histos[1].Integral()/histos[0].Integral()-1.)>0.00003 or opt.verbose:
                        print 'Events', sample, ptbin, histokey, wp, histos[0].Integral(), histos[1].Integral(), histos[1].Integral()/histos[0].Integral()-1.

                    if 'events' in opt.option: continue
 
                    if 'jetpt' not in histokey and histos[0].GetNbinsX()!=histos[1].GetNbinsX():
                        if histos[0].GetNbinsX()>histos[1].GetNbinsX():
                            rbin = float(histos[0].GetNbinsX())/float(histos[1].GetNbinsX())
                            if rbin==int(rbin): histos[0].Rebin(int(rbin))
                            elif opt.verbose: 
                                print 'Binning not comparable:', ptbin, histokey, wp, histos[0].GetNbinsX(), histos[1].GetNbinsX()
                                continue
                        elif histos[1].GetNbinsX()>histos[0].GetNbinsX():
                            rbin = float(histos[1].GetNbinsX())/float(histos[0].GetNbinsX())
                            if rbin==int(rbin): histos[1].Rebin(int(rbin))
                            elif opt.verbose: 
                                print 'Binning not comparable:', ptbin, histokey, wp, histos[0].GetNbinsX(), histos[1].GetNbinsX()
                                continue

                    binoffset = int(ptbin.split('Pt')[1].split('to')[0]) if 'jetpt' in histokey else 0

                    for ib in range(1, histos[1].GetNbinsX()+1):
                        if histos[0].GetBinContent(ib+binoffset)>0.:
                            if abs(histos[1].GetBinContent(ib)/histos[0].GetBinContent(ib+binoffset)-1.)>0.00003 and (opt.verbose or abs(histos[1].GetBinContent(ib)-histos[0].GetBinContent(ib+binoffset))>1):
                                print 'Shapes', sample, ptbin, histokey, wp, histos[1].GetBinLowEdge(ib), histos[0].GetBinContent(ib+binoffset), histos[1].GetBinContent(ib), histos[1].GetBinContent(ib)/histos[0].GetBinContent(ib+binoffset)-1.

### Prefit plots

def plotKinematics(opt):

    if not commonTools.foundShapeFiles(opt, True, False):
        if '.' in opt.tag:
            os.system('cp '+commonTools.getSampleShapeFileName(opt.shapedir, opt.year, opt.tag.split('.')[0], 'DATA')+' '+commonTools.getSampleShapeFileName(opt.shapedir, opt.year, opt.tag, 'DATA'))
        latinoTools.mergeall(opt) 

    latinoTools.plots(opt)

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

    for systematic in opt.Selections:
 
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

    wpSamples = []
    for sample in opt.samples:
        if not opt.samples[sample]['isDATA']: wpSamples.append(sample)

    if len(wpSamples)!=1: 
        print 'workingPoints error: too many samples selected ->', wpSamples
        exit()

    inputFile = ROOT.TFile.Open('/'.join([ opt.shapedir, opt.year, opt.tag.split('_')[0], 'Samples', 'plots_'+opt.year+opt.tag.split('_')[0]+'_ALL_'+wpSamples[0]+'.root' ]), 'read')

    discriminantDone = []

    for btagwp in opt.bTagWorkingPoints.keys():
        if opt.bTagWorkingPoints[btagwp]['discriminant'] not in discriminantDone:

            bJetDisc = inputFile.Get('QCD/Jet_'+opt.bTagWorkingPoints[btagwp]['discriminant']+'_5_0/histo_'+wpSamples[0])
            lJetDisc = inputFile.Get('QCD/Jet_'+opt.bTagWorkingPoints[btagwp]['discriminant']+'_0_0/histo_'+wpSamples[0])

            for ijet in range(1, opt.nJetMax):
                bJetDisc.Add(inputFile.Get('QCD/Jet_'+opt.bTagWorkingPoints[btagwp]['discriminant']+'_5_'+str(ijet)+'/histo_'+wpSamples[0]))
                lJetDisc.Add(inputFile.Get('QCD/Jet_'+opt.bTagWorkingPoints[btagwp]['discriminant']+'_0_'+str(ijet)+'/histo_'+wpSamples[0]))

            if 'noprint' not in opt.option:
                print '\n\nWorking Points for', btagwp[:-1]

            workingPointName = [ 'Loose', 'Medium', 'Tight', 'VeryTight', 'VeryVeryTight' ]
            workingPointLimit = [ 0.1, 0.01, 0.001, 0.0005, 0.0001 ]

            oldWorkingPoint = []
            for wp in workingPointName:
                wpflag = ''.join([ x for x in wp if x.isupper() ])
                if btagwp[:-1]+wpflag in opt.bTagWorkingPoints: oldWorkingPoint.append(float(opt.bTagWorkingPoints[btagwp[:-1]+wpflag]['cut']))
                else: oldWorkingPoint.append(0.9) 

            integralLightJets  = lJetDisc.Integral(0, lJetDisc.GetNbinsX())
            integralBottomJets = bJetDisc.Integral(0, bJetDisc.GetNbinsX())
 
            if 'csv' in opt.option:
                print '   ', btagwp[:-1],
            elif 'yml' in opt.option:
                print btagwp[:-1]+':'

            for wp in range(len(workingPointName)):

                wpflag = ''.join([ x for x in workingPointName[wp] if x.isupper() ])
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
                    print '   ',wpflag+':'
                    print '       ', 'eff:', round((100.*bJetDisc.Integral(binAtWorkingPoint, bJetDisc.GetNbinsX())/integralBottomJets),1)
                    print '       ', 'wp:', lJetDisc.GetBinLowEdge(binAtWorkingPoint) 


                if btagwp[:-1]+wpflag not in opt.bTagWorkingPoints:
                    opt.bTagWorkingPoints[btagwp[:-1]+wpflag] = {}
                    opt.bTagWorkingPoints[btagwp[:-1]+wpflag]['discriminant'] = opt.bTagWorkingPoints[btagwp]['discriminant']

                opt.bTagWorkingPoints[btagwp[:-1]+wpflag]['cut'] = str(lJetDisc.GetBinLowEdge(binAtWorkingPoint))

            if 'csv' in opt.option: print ''

            discriminantDone.append(opt.bTagWorkingPoints[btagwp]['discriminant'])

    if 'noprint' not in opt.option:
        print '\n\nbTagWorkingPoints =', opt.bTagWorkingPoints, '\n\n' 

### Analysis specific weights, efficiencies, scale factors, etc.

import sys
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import McM

def getGeneratorParametersFromMCM(mcm_query):

    mcm = McM(dev=True)
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

    for sample in opt.samples:

        ptHatBin = sample.split('_')[-1]
        events = ROOT.TChain(opt.treeName)
        for tree in opt.samples[sample]['name']: events.Add(tree.replace('#',''))
            
        if 'uQCDMu_' in sample:
            opt.qcdMuPtHatBins[ptHatBin]['events'] = str(events.GetEntries())
            if not 'xSec' in opt.qcdMuPtHatBins[ptHatBin]: 
                xSec, fEff = getGeneratorParametersFromMCM('dataset_name=QCD_*'+ptHatBin+'_MuEnrichedPt5_*&prepid=BTV*'+opt.year+'G*')
                opt.qcdMuPtHatBins[ptHatBin]['xSec'] = str(xSec)+'*'+str(fEff)
            else:
                genPars = opt.qcdMuPtHatBins[ptHatBin]['xSec'].split('*')
                xSec = float(genPars[0])
                fEff = 1. if len(genPars)==1 else float(genPars[1])
            opt.qcdMuPtHatBins[ptHatBin]['weight'] = str(1000.*xSec*fEff/events.GetEntries())

        elif 'QCD_' in sample:
            opt.qcdPtHatBins[ptHatBin]['events'] = str(events.GetEntries())
            if not 'xSec' in opt.qcdPtHatBins[ptHatBin]:
                xSec, fEff = getGeneratorParametersFromMCM('dataset_name=QCD_*'+ptHatBin+'_Tune*&prepid=BTV*'+opt.year+'G*')
                opt.qcdPtHatBins[ptHatBin]['xSec'] = str(xSec)+'*'+str(fEff)
            else:
                genPars = opt.qcdPtHatBins[ptHatBin]['xSec'].split('*')
                xSec = float(genPars[0])
                fEff = 1. if len(genPars)==1 else float(genPars[1])
            opt.qcdPtHatBins[ptHatBin]['weight'] = str(1000.*xSec*fEff/events.GetEntries())

    print '\nqcdMuPtHatBins =', opt.qcdMuPtHatBins
    print '\nqcdPtHatBins =', opt.qcdPtHatBins, '\n'

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

    if 'jetpt' not in opt.option.lower() and 'jeteta' not in opt.option.lower():
        print 'kinematicWeights only supported for jetpt and jeteta'
        exit()

    jetPtEdges = []
    for jetBin in opt.jetPtBins:
        for ptEdge in [ float(opt.jetPtBins[jetBin][0]), float(opt.jetPtBins[jetBin][1]) ]:
            if ptEdge not in jetPtEdges:
                jetPtEdges.append(ptEdge)
    jetPtEdges.sort()

    outputDir = '/'.join([ opt.datadir, opt.year, 'Kinematics' ])
    os.system('mkdir -p '+outputDir)

    if 'Light' in opt.tag and 'MergedLight' not in opt.tag:
        mergeLightShapes(opt)
        opt.tag = opt.tag.replace('Light', 'MergedLight')

    samples, cuts, variables = commonTools.getDictionariesInLoop(opt.configuration, opt.year, opt.tag, opt.sigset, 'variables')

    data, backgrounds = 'DATA', [ ]
    for sample in samples:
        if sample!='DATA': backgrounds.append(sample)

    data_File = commonTools.openSampleShapeFile(opt.shapedir, opt.year, opt.tag.replace('MergedLight','').split('.')[0], data) 

    kinematicVariable = ''
    for variable in variables: 
        if variable.split('_')[0] in opt.option.lower(): kinematicVariable = variable.split('_')[0]

    if kinematicVariable=='': 
        print 'kinematicWeights: no valid variable found for', opt.option.lower()
        exit()

    if 'jetpt' in kinematicVariable:
        xBins = ( int(opt.maxJetPt-opt.minJetPt), opt.minJetPt, opt.maxJetPt )
        yBins = ( 1, -opt.maxJetEta, opt.maxJetEta )
    elif 'jeteta' in kinematicVariable:
        xBins = [ jetPtEdges ]
        yBins = ( int((2.*opt.maxJetEta)/0.1), -opt.maxJetEta, opt.maxJetEta )
    else:
        print 'Error in kinematicWeights: no function variable chosen for corrections'
        exit()

    for back in backgrounds:

        inputFile = commonTools.openSampleShapeFile(opt.shapedir, opt.year, opt.tag, back)

        tagkinweights = '' if '.' not in opt.tag else '.'+opt.tag.split('.',1)[-1]
        outputname = opt.method + '_' + back + tagkinweights + '.' + kinematicVariable
        outputFile = commonTools.openRootFile(outputDir+'/'+outputname+'.root', 'recreate')

        weightsHisto = commonTools.bookHistogram(kinematicVariable, xBins, yBins)   

        for cut in cuts:
            for variable in variables:
                if variable.split('_')[0]!=kinematicVariable: continue
                if 'cuts' not in variables[variable] or cut in variables[variable]['cuts']:

                    dataHisto = data_File.Get('/'.join([ cut, variable.replace('lightjet','mujet').replace('jeteta_'+cut,'jeteta'), 'histo_'+data ])) ; dataHisto.SetDirectory(0)
                    backHisto = inputFile.Get('/'.join([ cut, variable                                                            , 'histo_'+back ])) ; backHisto.SetDirectory(0)

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
                            if spikeShifts>0:
                                spikeContent /= spikeShifts
                                backHisto.SetBinContent(spike, spikeContent)

                    if 'jetpt' in opt.option.lower() or 'jeteta' in opt.option.lower():

                        dataHisto.Divide(backHisto) 

                        if 'jetpt' in opt.option.lower():
                        
                            minPtFit, maxPtFit = dataHisto.GetBinLowEdge(1), dataHisto.GetBinLowEdge(dataHisto.GetNbinsX()+1)
                            ptfit = ROOT.TF1('ptfit', 'pol3', minPtFit, maxPtFit)
                            dataHisto.Fit('ptfit')

                        binx, biny, binz = ROOT.Long(), ROOT.Long(), ROOT.Long()

                        ptval  = float(opt.jetPtBins[cut][0]) + 0.1
                        etaval = weightsHisto.GetYaxis().GetBinCenter(1)

                        for ib in range(dataHisto.GetNbinsX()):

                            if 'jetpt' in opt.option.lower():
                                ptval  = dataHisto.GetBinCenter(ib+1)
                                weight = ptfit.Eval(dataHisto.GetBinCenter(ib+1))

                            elif 'jeteta' in opt.option.lower():
                                etaval = dataHisto.GetBinCenter(ib+1)
                                weight = dataHisto.GetBinContent(ib+1)

                            weightsHisto.SetBinContent(weightsHisto.FindBin(ptval, etaval), weight)

                            if opt.verbose:
                                print back, cut, ptval, etaval, weight

        inputFile.Close()

        outputFile.cd()
        weightsHisto.Write()                        
        outputFile.Close()

    data_File.Close()

