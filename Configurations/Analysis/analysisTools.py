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
    opt.minPlotPt = minPlotPt
    opt.maxPlotPt = maxPlotPt
    opt.maxJetEta = float(maxJetEta)
    opt.bTagAlgorithms = bTagAlgorithms
    opt.btagWPs = bTagWorkingPoints.keys()
    opt.ptBins = jetPtBins.keys()
    opt.Selections = []
    for selection in systematicVariations:
        sel = 'Central' if selection=='' else selection
        if 'vetosel' in opt.option:
            if sel in opt.option: continue
        elif 'sel' in opt.option and sel not in opt.option: continue
        opt.Selections.append(selection)
    opt.systematicNuisances = systematicNuisances

    if opt.action=='ptHatWeights':
        opt.samples = samples
        opt.qcdMuPtHatBins = qcdMuPtHatBins
        opt.qcdPtHatBins = qcdPtHatBins 

    elif opt.action=='workingPoints':
        opt.workingPointName = workingPointName
        opt.workingPointLimit = workingPointLimit
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

    elif opt.action=='ptRelInput' or opt.action=='shapesForFit':
        opt.templateTreatments = templateTreatments
        opt.bTemplateCorrector = bTemplateCorrector

    elif opt.action=='storeBTagScaleFactors':
        opt.csvSystematics = csvSystematics

def setAnalysisDefaults(opt):

    opt.baseDir = os.getenv('PWD') 
    opt.treeName = 'btagana/ttree'
    opt.unblind = True

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

        opt2 = copy.deepcopy(opt)
        opt2.tag = tag.replace(tag.split('.')[0], tag.split('.')[0]+selection)

        sigsets = [ 'MC', 'Data' ] if opt.sigset=='SM' else [ opt.sigset ]
        for sigset in sigsets:

            opt2.sigset = sigset
            if sigset=='Data' and '.' in tag and 'Light' not in tag: opt2.tag = opt2.tag.split('.')[0]
            if sigset=='Data' and 'JEU' in selection: continue
            if 'MC' in sigset and 'Light' in opt.tag: opt2.batchQueue = 'testmatch'
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

    if 'ptreltools' in opt.option.lower(): 
        ptRelInputForPtRelTools(opt)
        return

    doBCorrections, doLCorrections = False, False
    templateTreatmentDict = {}
    templateTreatmentFlag = ''

    for treatment in opt.templateTreatments:
        option = opt.option.lower()
        if treatment in option:

            templateTreatmentDict[treatment] = []
            templateTreatmentFlag += treatment.capitalize()

            samplesForTreatment = option.split(treatment)[-1]
            for othertreatment in opt.templateTreatments: samplesForTreatment = samplesForTreatment.split(othertreatment)[0]

            for sample in [ 'ljets', 'bjets' ]:
               if sample.replace('jets','') in samplesForTreatment: 
                   templateTreatmentDict[treatment].append(sample)
                   templateTreatmentFlag += sample.replace('jets','').upper()
                   if sample=='ljets': doLCorrections = True
                   if sample=='bjets': doBCorrections = True

            if len(templateTreatmentDict[treatment])==0: 
                print 'Error: no sample found for template treatment', treatment
                exit()

    if opt.verbose: 
        print 'Preparing fit templates with templateTreatmentFlag =', templateTreatmentFlag
        print 'Reading templates'

    outputTemplates = {}

    for datatype in [ 'MuEnriched', 'Inclusive' ]:
        if datatype=='Inclusive' and not doLCorrections: continue
        for sigset in [ 'MC', 'Data' ]:
            for selection in opt.Selections:

                sel = 'Central' if selection=='' else selection
                if sigset=='Data' and 'JEU' in selection: continue
                if datatype=='Inclusive' and 'AwayJet' in selection: continue

                opt2 = copy.deepcopy(opt)
                opt2.tag = opt.tag.replace(opt.tag.split('.')[0], opt.tag.split('.')[0]+selection)
                if sigset=='Data' and datatype=='MuEnriched': opt2.tag = opt2.tag.split('.')[0]
                if datatype=='Inclusive': opt2.tag = opt2.tag.replace('Templates','MergedLightTemplates').replace('mujet','lightjet')
                opt2.sigset = sigset

                samples, cuts, variables, nuisances = commonTools.getDictionaries(opt2)

                for sample in samples:

                    if opt.verbose: print '     selection', sel, ' and sample', sample

                    if datatype=='Inclusive':
                        if not commonTools.foundSampleShapeFile(opt2.shapedir, opt2.year, opt2.tag, sample) or opt.reset:
                            opt2.tag = opt2.tag.replace('MergedLight','Light')
                            mergeLightShapes(opt2)
                            opt2.tag = opt2.tag.replace('PtRelLight','PtRelMergedLight')

                    inputTemplateFile = commonTools.openSampleShapeFile(opt2.shapedir, opt2.year, opt2.tag, sample)

                    for ptBin in opt.ptBins:
                        for btagWP in opt.btagWPs:
                            for btagCut in [ 'Pass', 'Fail' ]:

                                cutName = '_'.join([ ptBin, btagWP, btagCut ]) if selection=='' else '_'.join([ ptBin, btagWP, btagCut, selection ])
                                if cutName not in outputTemplates: outputTemplates[cutName] = {}

                                variable = '_'.join([ 'ptrel', btagWP, btagCut ]) if datatype!='Inclusive' else '_'.join([ 'ptrel', ptBin ])
                                histoName = '/'.join([ ptBin, variable, 'histo_' + sample ])
                                template = copy.deepcopy(inputTemplateFile.Get(histoName))

                                sampleToSave = sample.replace('MET','').replace('HT','')
                                template.SetName('_'.join([ 'histo', sampleToSave ]))
                                template.SetTitle('_'.join([ 'histo', sampleToSave ]))
                                outputTemplates[cutName][template.GetName().split('/')[-1]] = template

                                if 'JEU' in selection:
                                    jeuTemplate = copy.deepcopy(template)
                                    jeuTemplate.SetName('_'.join([ 'histo', sample, selection]))
                                    jeuTemplate.SetTitle('_'.join([ 'histo', sample, selection]))
                                    outputTemplates[cutName.replace('_'+selection,'')][jeuTemplate.GetName().split('/')[-1]] = jeuTemplate

                                for nuisance in nuisances:
                                    if nuisance!='stat' and nuisances[nuisance]['type']=='shape':
                                        if 'cuts' not in nuisances[nuisance] or ptBin in nuisances[nuisance]['cuts']:
                                            if sample in nuisances[nuisance]['samples']:
                                                for variation in [ 'Up', 'Down' ]:

                                                    templateNuisance = copy.deepcopy(inputTemplateFile.Get(histoName + '_' + nuisances[nuisance]['name'] + variation))
                                                    outputTemplates[cutName][templateNuisance.GetName().split('/')[-1]] = templateNuisance

                                    elif nuisance!='stat' and nuisances[nuisance]['type']=='lnN':
                                        if '2D' in opt.option and ('ljets' in nuisances[nuisance]['samples'] or 'cjets' in nuisances[nuisance]['samples']):
                                            if sample=='ljets' or sample=='cjets':
                                                for variation in [ 'Up', 'Down' ]:

                                                    centralTemplate = copy.deepcopy(inputTemplateFile.Get(histoName))
                                                    if sample in nuisances[nuisance]['samples']:
                                                        if variation=='Up': centralTemplate.Scale(float(nuisances[nuisance]['samples'][sample]))
                                                        else: centralTemplate.Scale(2.-float(nuisances[nuisance]['samples'][sample]))
                                                    centralTemplate.SetName('_'.join([ 'histo', sample, nuisances[nuisance]['name']+variation]))
                                                    centralTemplate.SetTitle('_'.join([ 'histo', sample, nuisances[nuisance]['name']+variation]))
                                                    outputTemplates[cutName][centralTemplate.GetName().split('/')[-1]] = centralTemplate

    if opt.verbose: print 'Normalizing templates'

    cutNameList = outputTemplates.keys()

    for cutName in cutNameList:
        
        errorDataYields = ROOT.double()
        if 'JEU' in cutName: outputTemplates[cutName]['histo_DATA'] = copy.deepcopy(outputTemplates['_'.join([ cutName.split('_')[x] for x in range(3) ])]['histo_DATA'])
        dataYields = outputTemplates[cutName]['histo_DATA'].IntegralAndError(-1,-1,errorDataYields) 
        dataPS = pow(dataYields/errorDataYields, 2)/dataYields

        if doLCorrections:
            jetCutName = cutName if 'histo_Jet' in outputTemplates[cutName] else '_'.join([ cutName.split('_')[x] for x in range(3) ])
            errorJetYields = ROOT.double()
            jetYields = outputTemplates[jetCutName]['histo_Jet'].IntegralAndError(-1,-1,errorJetYields)
            jetPS = pow(jetYields/errorJetYields, 2)/jetYields

        for template in outputTemplates[cutName]:
            if 'histo_Jet' in template: 
                outputTemplates[cutName][template].Scale(jetPS)
            elif 'histo_QCD' in template:
                qcdYields = outputTemplates[cutName][template].Integral(-1,-1)
                outputTemplates[cutName][template].Scale(jetPS*jetYields/qcdYields)
            else:
                outputTemplates[cutName][template].Scale(dataPS)

    if opt.verbose: print 'Computing corrections'

    for cutName in cutNameList:

        if doLCorrections: 
            outputTemplates[cutName+'_CorrL'] = {}
            jetCutName = cutName if 'histo_Jet' in outputTemplates[cutName] else '_'.join([ cutName.split('_')[x] for x in range(3) ])
            qcdCutName = cutName if 'histo_QCD' in outputTemplates[cutName] else '_'.join([ cutName.split('_')[x] for x in range(3) ])
            jetHisto = copy.deepcopy(outputTemplates[jetCutName]['histo_Jet'])
            for template in outputTemplates[cutName].keys():
                if 'histo_ljets' in template:

                    correctedHisto = copy.deepcopy(outputTemplates[cutName][template])

                    if template.replace('_ljets','_QCD') in outputTemplates[qcdCutName]:
                        qcdHisto = copy.deepcopy(outputTemplates[qcdCutName][template.replace('_ljets','_QCD')])
                    else: qcdHisto = copy.deepcopy(outputTemplates[qcdCutName]['histo_QCD'])

                    correctedHisto.Multiply(jetHisto)
                    correctedHisto.Divide(qcdHisto)   
                    outputTemplates[cutName+'_CorrL'][template] = correctedHisto

        if doBCorrections:
            outputTemplates[cutName+'_CorrB'] = {}
            cutNameCorrector = cutName.replace(cutName.split('_')[1],opt.bTemplateCorrector[cutName.split('_')[1]]).replace('Fail','Pass')
            for template in outputTemplates[cutName].keys():
                if 'histo_bjets' in template:

                    dataHisto = copy.deepcopy(outputTemplates[cutNameCorrector]['histo_DATA'])
                    dataYields = dataHisto.Integral(-1,-1)

                    correctedHisto = copy.deepcopy(outputTemplates[cutName][template])

                    bHisto = copy.deepcopy(outputTemplates[cutNameCorrector][template])

                    if template.replace('_bjets','_cjets') in outputTemplates[cutNameCorrector]:
                        cHisto = copy.deepcopy(outputTemplates[cutNameCorrector][template.replace('_bjets','_cjets')])
                    else: cHisto = copy.deepcopy(outputTemplates[cutNameCorrector]['histo_cjets'])
 
                    if template.replace('_bjets','_ljets') in outputTemplates[cutNameCorrector]:
                        lHisto = copy.deepcopy(outputTemplates[cutNameCorrector][template.replace('_bjets','_ljets')])
                    else: lHisto = copy.deepcopy(outputTemplates[cutNameCorrector]['histo_ljets'])

                    mcYields = bHisto.Integral(-1,-1) + cHisto.Integral(-1,-1) + lHisto.Integral(-1,-1)
                    bHisto.Scale(dataYields/mcYields); cHisto.Scale(dataYields/mcYields); lHisto.Scale(dataYields/mcYields);
                    dataHisto.Add(cHisto,-1); dataHisto.Add(lHisto,-1);

                    correctedHisto.Multiply(dataHisto)
                    correctedHisto.Divide(bHisto)
                    outputTemplates[cutName+'_CorrB'][template] = correctedHisto

    if '2D' in opt.option:

        if opt.verbose: print 'Merging light and c templates'

        for cutName in cutNameList:
            for template in outputTemplates[cutName].keys():
                if 'ljets' in template:
                    outputTemplates[cutName][template].Add(outputTemplates[cutName][template.replace('ljets','cjets')])
                    if doLCorrections: outputTemplates[cutName+'_CorrL'][template].Add(outputTemplates[cutName][template.replace('ljets','cjets')])

    if opt.verbose: print 'Saving templates', cutName

    outtag = opt.tag.replace(opt.tag.split('.')[0], opt.tag.split('.')[0]+'ForFit')
    if '2D' in opt.option: outtag = outtag.replace('Templates', 'Templates2D')
    outtag = outtag.replace('Templates', 'Templates'+templateTreatmentFlag)
    ptRelTemplateFile = commonTools.openShapeFile(opt.shapedir, opt.year, outtag, opt.sigset, opt.fileset, 'recreate')

    for cutName in cutNameList:

        if opt.verbose: print '     Saving templates for cut', cutName, '\n'

        ptRelTemplateFile.mkdir(cutName)
        ptRelTemplateFile.mkdir(cutName+'/ptrel')
        ptRelTemplateFile.cd(cutName+'/ptrel')

        sampleCutName = { 'DATA' : '' }
        if '2D' not in opt.option: sampleCutName['cjets'] = ''
        sampleCutName['ljets'] = '_CorrL' if 'corr' in templateTreatmentDict and 'ljets' in templateTreatmentDict['corr'] else ''
        sampleCutName['bjets'] = '_CorrB' if 'corr' in templateTreatmentDict and 'bjets' in templateTreatmentDict['corr'] else ''

        for template in outputTemplates[cutName].keys():
            sample = template.split('_')[1]
            if sample in sampleCutName:
                if opt.verbose: print '        ', cutName, sample, sampleCutName[sample], template
                outputTemplates[cutName+sampleCutName[sample]][template].Write()

        if opt.verbose: print '\n'

        nuisCutNameList = [ cutName ]
        if 'syst' in templateTreatmentDict and len(cutName.split('_'))==3:
            for systSample in templateTreatmentDict['syst']:
            
                systCutName = cutName+'_Corr'+systSample.replace('jets','').upper()
                ptRelTemplateFile.mkdir(systCutName)
                ptRelTemplateFile.mkdir(systCutName+'/ptrel')
                ptRelTemplateFile.cd(systCutName+'/ptrel')

                sampleSystCutName = copy.deepcopy(sampleCutName)
                sampleSystCutName[systSample] = '_Corr'+systSample.replace('jets','').upper() if sampleCutName[systSample]=='' else ''

                for template in outputTemplates[cutName].keys():
                    sample = template.split('_')[1]
                    if sample in sampleSystCutName:
                        if opt.verbose: print '        ', systCutName, sample, sampleSystCutName[sample], template
                        outputTemplates[cutName+sampleSystCutName[sample]][template].Write()

                nuisCutNameList.append(systCutName)
                if opt.verbose: print '\n'

        if 'nuis' in templateTreatmentDict:
            for nuisSample in templateTreatmentDict['nuis']:

                correctionFlag = '_Corr'+nuisSample.replace('jets','').upper()
                nominalHisto = copy.deepcopy(outputTemplates[cutName]['histo_'+nuisSample])
                correctedHisto = copy.deepcopy(outputTemplates[cutName+correctionFlag]['histo_'+nuisSample])

                if sampleCutName[nuisSample]=='':
                    nominalHisto.SetName('histo_'+nuisSample+correctionFlag+'Down')
                    nominalHisto.SetTitle('histo_'+nuisSample+correctionFlag+'Down')
                    correctedHisto.SetName('histo_'+nuisSample+correctionFlag+'Up')
                    correctedHisto.SetTitle('histo_'+nuisSample+correctionFlag+'Up')
                else:
                    nominalHisto.SetName('histo_'+nuisSample+correctionFlag+'Up')
                    nominalHisto.SetTitle('histo_'+nuisSample+correctionFlag+'Up')
                    correctedHisto.SetName('histo_'+nuisSample+correctionFlag+'Down')
                    correctedHisto.SetTitle('histo_'+nuisSample+correctionFlag+'Down')

                for nuisCutName in nuisCutNameList:
                    ptRelTemplateFile.cd(nuisCutName+'/ptrel')
                    if opt.verbose: print '        ', cutName, nuisSample, correctionFlag, nominalHisto.GetName(), correctedHisto.GetName(), '->', nuisCutName
                    nominalHisto.Write()
                    correctedHisto.Write()

        if opt.verbose: print '\n'

        if len(cutName.split('_'))==3:
            doneNuisance = []
            for nuisTemplate in outputTemplates[cutName].keys():
                if len(nuisTemplate.split('_'))>2:

                    nuisance = nuisTemplate.replace('histo_'+nuisTemplate.split('_')[1]+'_','')
                    if cutName+'_'+nuisance in outputTemplates: continue
                    if nuisance in doneNuisance: continue

                    ptRelTemplateFile.mkdir(cutName+'_'+nuisance)
                    ptRelTemplateFile.mkdir(cutName+'_'+nuisance+'/ptrel')
                    ptRelTemplateFile.cd(cutName+'_'+nuisance+'/ptrel')

                    for sample in sampleCutName:

                        if '_'.join([ 'histo', sample, nuisance ]) in outputTemplates[cutName+sampleCutName[sample]].keys():

                            nuisanceHisto = copy.deepcopy(outputTemplates[cutName+sampleCutName[sample]]['_'.join([ 'histo', sample, nuisance ])])
                            nuisanceHisto.Write()
                            if opt.verbose: print '        ', cutName+'_'+nuisance, sampleCutName[sample], '_'.join([ 'histo', sample, nuisance ]), nuisanceHisto.GetName()

                            centralTemplate = copy.deepcopy(nuisanceHisto)
                            centralTemplate.SetName('histo_'+sample)
                            centralTemplate.SetTitle('histo_'+sample)
                            centralTemplate.Write()
                            if opt.verbose: print '        ', cutName+'_'+nuisance, sampleCutName[sample], '_'.join([ 'histo', sample, nuisance ]), centralTemplate.GetName()

                            nuisanceCorrections = [ 1. ]
                            originalCentralTemplate = copy.deepcopy(outputTemplates[cutName+sampleCutName[sample]]['histo_'+sample])
                            for ib in range(1, nuisanceHisto.GetNbinsX()+1): 
                                if originalCentralTemplate.GetBinContent(ib)>0.: nuisanceCorrections.append(nuisanceHisto.GetBinContent(ib)/originalCentralTemplate.GetBinContent(ib))
                                else: nuisanceCorrections.append(1.)

                            for template in outputTemplates[cutName+sampleCutName[sample]].keys():                           
                                if template.split('_')[1]==sample and nuisance not in template and template!='histo_'+sample:
                                    templateCut = cutName+template.replace('histo_'+sample,'')+sampleCutName[sample]
                                    if templateCut in outputTemplates and '_'.join([ 'histo', sample, nuisance ]) in outputTemplates[templateCut]:
                                        templateHisto = copy.deepcopy(outputTemplates[templateCut]['_'.join([ 'histo', sample, nuisance ])])
                                        templateHisto.SetName(template)
                                        templateHisto.SetTitle(template)
                                        templateHisto.Write()
                                        if opt.verbose: print '        ', cutName+'_'+nuisance, templateCut, '_'.join([ 'histo', sample, nuisance ]), templateHisto.GetName()
                                    else:
                                        templateHisto = copy.deepcopy(outputTemplates[cutName+sampleCutName[sample]][template])
                                        correctionStatus = ''
                                        if nuisance.replace('Up','').replace('Down','') not in template:
                                            for ib in range(1, nuisanceHisto.GetNbinsX()+1):
                                                templateHisto.SetBinContent(ib, templateHisto.GetBinContent(ib)*nuisanceCorrections[ib])
                                            correctionStatus = 'corrected'
                                        templateHisto.Write()
                                        if opt.verbose: print '        ', cutName+'_'+nuisance, sampleCutName[sample], template, templateHisto.GetName(), correctionStatus 

                        else:
                            for template in outputTemplates[cutName+sampleCutName[sample]].keys():
                                if template.split('_')[1]==sample:
                                    templateHisto = copy.deepcopy(outputTemplates[cutName+sampleCutName[sample]][template])
                                    templateHisto.Write()
                                    if opt.verbose: print '        ', cutName+'_'+nuisance, sampleCutName[sample], template, templateHisto.GetName()  

                        if 'nuis' in templateTreatmentDict:
                            if sample in templateTreatmentDict['nuis']:

                                correctionFlag = '_Corr'+sample.replace('jets','').upper()
                                nuisanceFlag = '_'+nuisance if '_'.join([ 'histo', sample, nuisance ]) in outputTemplates[cutName+sampleCutName[sample]].keys() else ''
                                nominalHisto = copy.deepcopy(outputTemplates[cutName]['histo_'+sample+nuisanceFlag])
                                correctedHisto = copy.deepcopy(outputTemplates[cutName+correctionFlag]['histo_'+sample+nuisanceFlag])

                                if sampleCutName[sample]=='':
                                    nominalHisto.SetName('histo_'+sample+correctionFlag+'Down')
                                    nominalHisto.SetTitle('histo_'+sample+correctionFlag+'Down')
                                    correctedHisto.SetName('histo_'+sample+correctionFlag+'Up')
                                    correctedHisto.SetTitle('histo_'+sample+correctionFlag+'Up')
                                else:
                                    nominalHisto.SetName('histo_'+sample+correctionFlag+'Up')
                                    nominalHisto.SetTitle('histo_'+sample+correctionFlag+'Up')
                                    correctedHisto.SetName('histo_'+sample+correctionFlag+'Down')
                                    correctedHisto.SetTitle('histo_'+sample+correctionFlag+'Down')

                                nominalHisto.Write()
                                correctedHisto.Write()
                                if opt.verbose: print '        ', cutName+'_'+nuisance, sampleCutName[sample], sample, correctionFlag, nominalHisto.GetName(), correctedHisto.GetName(), '->', cutName+'_'+nuisance 

                    if opt.verbose: print '        ', 'done', cutName, nuisance, '\n'
                    doneNuisance.append(nuisance)

        if opt.verbose: print '\n\n'

def ptRelInputForPtRelTools(opt):

    ptRelTemplateFileName = './PtRelTools/Templates/PtRel_TemplatesAll_PS'+opt.year+'_KinEtaAfterPtBinsCentral_LowPtAwayTrgConf_Run2016Production.root'
    if 'nolight' in opt.option: ptRelTemplateFileName = ptRelTemplateFileName.replace('TemplatesAll', 'Templates')

    ptRelTemplateFile = commonTools.openRootFile(ptRelTemplateFileName, 'recreate')

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

def plotTemplates(opt):

    bTagPerfAnalysis(opt, 'prefitplots')

### Fits and postfit plots

def bTagPerfAnalysis(opt, action):

    splitJetPtBins = [ 'all' ] if '_mergedJetPtBins' in opt.tag else opt.ptBins
    splitSelections = [ 'all' ] if '_mergedSelections' in opt.tag else opt.Selections
    mergedSelectionFlag = '_mergedSelections_nuisSelections' if '_nuisSelections' in opt.tag else '_mergedSelections'

    for btagWP in opt.btagWPs:
        fitTagList = []
        for ptbin in splitJetPtBins:
            for selection in splitSelections:
                sel = 'Central' if selection=='' else selection

                tagOptionList = [ opt.tag.split('_')[0], '_btag'+btagWP ]
                if ptbin=='all': tagOptionList.append('_mergedJetPtBins')
                else: tagOptionList.append('_Jet'+ptbin)
                if sel=='all': tagOptionList.append(mergedSelectionFlag)
                else: tagOptionList.append('_sel'+sel)

                opt2 = copy.deepcopy(opt)
                opt2.tag = '_'.join(tagOptionList)

                fitTagList.append(opt2.tag.replace('__sel','____sel'))

                if action=='prefitplots': latinoTools.plots(opt2)
                elif action=='datacards': combineTools.writeDatacards(opt2)
                elif action=='ptrelfit': 
                    if len(fitTagList)==len(splitJetPtBins)*len(splitSelections):      
                        opt2.tag = '-'.join(fitTagList)
                        combineTools.mlfits(opt2)
                elif action=='system8fit': runSystem8Fit(opt2)
                elif action=='getsystem8results': getSystem8FitResults(opt2)
                elif action=='getptrelresults': getPtRelFitResults(opt2, opt)
                elif 'prefit' in action or 'postfit' in action:
                    if commonTools.isGoodFile(commonTools.getCombineOutputFileName(opt2, '', '', opt2.tag, 'mlfits'), 6000.):
                        if action=='prefitplots': latinoTools.postFitPlots(opt2)
                        elif commonTools.goodCombineFit(opt2, opt2.year, opt2.tag, '', 'PostFitS'):  
                            if action=='postfitshapes':  latinoTools.postFitShapes(opt2) 
                            elif action=='postfitplots': latinoTools.postFitPlots(opt2)
                        elif opt.verbose: print 'Warning: failed fit for campaign='+opt2.year+', WP='+btagWP+', bin='+ptbin
                    elif opt.verbose: print 'Warning: input ML fit file', commonTools.getCombineOutputFileName(opt2), '', '', opt2.tag, 'mlfits', 'not found' 
                elif action=='checkfit': 
                    if not commonTools.isGoodFile(commonTools.getCombineOutputFileName(opt, '', '', opt.tag, 'mlfits'), 6000.):
                        print 'Input ML fit file', commonTools.getCombineOutputFileName(opt, '', '', opt.tag, 'mlfits'), 'not found'
                    elif not commonTools.goodCombineFit(opt, opt2.year, opt2.tag, '', 'PostFitS'):
                        print 'Failed fit for campaign='+opt2.year+', WP='+btagWP+', bin='+ptbin

def ptRelDatacards(opt):

    bTagPerfAnalysis(opt, 'datacards')
 
def ptRelFits(opt):

    opt.batchQueue = 'workday' if '_merged' in opt.tag else 'longlunch'
    opt.option += 'skipbonly'
    bTagPerfAnalysis(opt, 'ptrelfit')

def ptRelFitCheck(opt):

    bTagPerfAnalysis(opt, 'checkfit')

def ptRelPreFitPlots(opt):

    opt.option += 'prefit'
    bTagPerfAnalysis(opt, 'prefitplots')

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

    cut = '_'.join([ ptbin, btagWP, 'BTAGSTATUS', systematic ]).replace('_Central','')

    if fileType=='shapes': histoPath = cut+'/ptrel/histo_bjets'
    else: histoPath = 'shapes_fit_s/'+cut+'/total_signal'

    histoPass = inputFile.Get(histoPath.replace('BTAGSTATUS','Pass'))
    histoFail = inputFile.Get(histoPath.replace('BTAGSTATUS','Fail'))

    errorPassYield, errorFailYield = ROOT.double(), ROOT.double()
    passYield = histoPass.IntegralAndError(-1,-1,errorPassYield)
    failYield = histoFail.IntegralAndError(-1,-1,errorFailYield)

    if opt.verbose and fileType=='fit' and (errorPassYield==0. or errorFailYield==0.): 
        print '    Warning: missing erros in ML fit for', btagWP, ptbin, systematic

    efficiency = passYield/(passYield+failYield)

    correlation = 0.

    if fileType!='shapes': # Use a trick for the time being
        histoTotal = inputFile.Get('shapes_fit_s/total_signal')
        errorTotalYield = ROOT.double()
        totalYield = histoTotal.IntegralAndError(-1,-1,errorTotalYield)

        if errorPassYield*errorFailYield!=0:
            correlation = (pow(errorTotalYield,2)-pow(errorPassYield,2)-pow(errorFailYield,2))/(2*errorPassYield*errorFailYield)

    return efficiency, efficiencyError(passYield, failYield, errorPassYield, errorFailYield, correlation), passYield+failYield

def readOldPtRelFitResultsFromTables(opt, optOrig, btagWP, ptbin, systematic):

    tableName = '/afs/cern.ch/work/s/scodella/BTagging/CodeDevelopment/CMSSW_10_2_11/src/RecoBTag/PerformanceMeasurements/test/PtRelTools/Tables/PtRelFit_'+btagWP+'_anyEta_'+ptbin.replace('to','')+'_'+systematic+'_PSRun2017UL17_KinEtaAfterPtBinsCentral_LowPtAwayTrgConf_Run2016Production.txt'

    tableFile = open(tableName, 'r')
    lines = tableFile.readlines()
    for line in lines:
        if 'Efficiency MC' in line:
            optOrig.bTagPerfResults[btagWP][systematic][ptbin]['efficiencyMC']             = float(line.split(' = ')[1].split(' +/- ')[0])
            optOrig.bTagPerfResults[btagWP][systematic][ptbin]['efficiencyMCUncertainty']  = float(line.split(' +/- ')[1].split('\n')[0])
        elif 'Eff. data' in line:
            optOrig.bTagPerfResults[btagWP][systematic][ptbin]['efficiencyFit']            = float(line.split(' = ')[1].split(' +/- ')[0])
            optOrig.bTagPerfResults[btagWP][systematic][ptbin]['efficiencyFitUncertainty'] = float(line.split(' +/- ')[1].split(' (')[0])
        elif 'Scale factor' in line:
            optOrig.bTagPerfResults[btagWP][systematic][ptbin]['scaleFactor']              = float(line.split(' = ')[1].split(' +/- ')[0])
            optOrig.bTagPerfResults[btagWP][systematic][ptbin]['scaleFactorUncertainty']   = float(line.split(' +/- ')[1].split('\n')[0])

def getPtRelFitResults(opt, optOrig):

    btagWP = opt.tag.split('_btag')[1].split('_')[0] 
    ptbinList = [ 'Pt'+opt.tag.split('_JetPt')[1].split('_')[0] ] if '_JetPt' in opt.tag else opt.ptBins 
    systematicList = [ opt.tag.split('_sel')[1].split('_')[0] ] if '_sel' in opt.tag else opt.Selections

    if btagWP not in optOrig.bTagPerfResults: optOrig.bTagPerfResults[btagWP] = {}
  
    for syst in systematicList:
        systematic = 'Central' if syst=='' else syst
        if systematic not in optOrig.bTagPerfResults[btagWP]: optOrig.bTagPerfResults[btagWP][systematic] = {}
        for ptbin in ptbinList :
            optOrig.bTagPerfResults[btagWP][systematic][ptbin] = {}

            if 'ptreltools' in opt.option.lower():
                readOldPtRelFitResultsFromTables(opt, optOrig, btagWP, ptbin, systematic)
                return

            efficiencyMC, uncertaintyMC, efficiencyFit, uncertaintyFit, scaleFactor, scaleFactorUncertainty = -1., -1., -1., -1., -1., -1.

            if commonTools.isGoodFile(commonTools.getCombineOutputFileName(opt, '', '', opt.tag, 'mlfits'), 6000.):
                if commonTools.goodCombineFit(opt, opt.year, opt.tag, '', 'PostFitS'):

                    motherFile = commonTools.openShapeFile(opt.shapedir, opt.year, opt.tag.split('_')[0], 'SM', 'SM')
                    fitFile = commonTools.openCombineFitFile(opt, '', opt.year, opt.tag)
 
                    efficiencyMC,  uncertaintyMC,  yieldsMC  = getPtRelEfficiency(opt, motherFile, 'shapes', btagWP, ptbin, systematic)
                    efficiencyFit, uncertaintyFit, yieldsFit = getPtRelEfficiency(opt, fitFile,    'fit',    btagWP, ptbin, systematic)

                    if efficiencyFit>0.999 or (efficiencyFit>0.99 and efficiencyFit/efficiencyMC>1.1) or (efficiencyFit>0.98 and efficiencyFit/efficiencyMC>1.5): 
                        efficiencyFit, uncertaintyFit = 0.01, math.sqrt(efficiencyMC*(1.-efficiencyMC)/yieldsFit)
                    elif uncertaintyFit==0.:
                        uncertaintyFit = math.sqrt(efficiencyFit*(1.-efficiencyFit)/yieldsFit)

                    scaleFactor = efficiencyFit/efficiencyMC
                    scaleFactorUncertainty = scaleFactor*math.sqrt(pow(uncertaintyFit/efficiencyFit,2)+pow(uncertaintyMC/efficiencyMC,2))

                    motherFile.Close()
                    fitFile.Close()

                elif opt.verbose: '  Warning: failed fit for campaign='+opt.year+', WP='+btagWP+', bin='+ptbin
            elif opt.verbose: print 'Warning: input ML fit file', commonTools.getCombineOutputFileName(opt, '', '', opt.tag, 'mlfits'), 'not found'

            optOrig.bTagPerfResults[btagWP][systematic][ptbin] = {}
            optOrig.bTagPerfResults[btagWP][systematic][ptbin]['efficiencyMC']             = efficiencyMC
            optOrig.bTagPerfResults[btagWP][systematic][ptbin]['efficiencyMCUncertainty']  = uncertaintyMC
            optOrig.bTagPerfResults[btagWP][systematic][ptbin]['efficiencyFit']            = efficiencyFit
            optOrig.bTagPerfResults[btagWP][systematic][ptbin]['efficiencyFitUncertainty'] = uncertaintyFit
            optOrig.bTagPerfResults[btagWP][systematic][ptbin]['scaleFactor']              = scaleFactor
            optOrig.bTagPerfResults[btagWP][systematic][ptbin]['scaleFactorUncertainty']   = scaleFactorUncertainty

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

def fillBTagPerfHistogram(opt, result, btagWP, bTagPerfSystematicResults):

    bTagPerfHisto = templateHistogram(opt, result)
    bTagPerfHisto.SetDirectory(0)

    for ptbin in bTagPerfSystematicResults:

        ib = bTagPerfHisto.FindBin((float(ptbin.split('Pt')[1].split('to')[0])+float(ptbin.split('to')[1]))/2.)
        bTagPerfHisto.SetBinContent(ib, bTagPerfSystematicResults[ptbin][result])
        bTagPerfHisto.SetBinError(ib, bTagPerfSystematicResults[ptbin][result+'Uncertainty'])

    bTagPerfHisto.SetXTitle('#mu-jet #font[50]{p}_{T} [GeV]')
    bTagPerfHisto.GetXaxis().SetRangeUser(opt.minPlotPt, opt.maxPlotPt)

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

    ySize, ylow = 800, 0.52
 
    if resultToPlot!='performance':
        ySize, ylow = 400, 0.03

    canvas = commonTools.bookCanvas('canvas', 1200, ySize)
    canvas.cd()

    pad = []
    pad.append(commonTools.bookPad('pad0', 0.02, ylow, 0.98, 0.98))
    if opt.maxPlotPt>=300.: pad[0].SetLogx()
    pad[0].Draw()

    if resultToPlot=='performance': 
        pad.append(commonTools.bookPad('pad1', 0.02, 0.03, 0.98, 0.49))
        if opt.maxPlotPt>=300.: pad[1].SetLogx()
        pad[1].Draw()

    for result in [ 'efficiency', 'scalefactor' ]:
        if result==resultToPlot or resultToPlot=='performance':

            if result=='scalefactor' and resultToPlot=='performance': pad[1].cd()
            else: pad[0].cd()

            drawOption = 'p'
            markerColor =  1
            for tag in bTagPerfHistos:
                markerStyle = 20
                for systematic in opt.Selections: #bTagPerfHistos[tag]: # So the orfer is respected
                    styleOffset = 0
                    for btaghisto in [ 'efficiencyFit', 'efficiencyMC', 'scaleFactor' ]:
                        if result in btaghisto.lower():

                            if systematic=='FinalSystematics': 
                                bTagPerfHistos[tag][systematic][btaghisto].SetFillStyle(3005);
                                bTagPerfHistos[tag][systematic][btaghisto].SetFillColor(2);
                                drawOption = 'pe2'

                            bTagPerfHistos[tag][systematic][btaghisto].SetMarkerStyle(markerStyle+styleOffset)
                            bTagPerfHistos[tag][systematic][btaghisto].SetMarkerColor(markerColor)                
                            bTagPerfHistos[tag][systematic][btaghisto].Draw(drawOption)
                            drawOption = 'psame'
                            styleOffset = 4

                    if systematic!='FinalSystematics':
                        markerStyle += 1
                        markerColor += 1

    tagFlag = '-'.join(bTagPerfHistos.keys())
    if 'DepOn' in opt.option or 'Final' in opt.option:
        systematicFlag = opt.option
    else: 
        systematicFlag = '-'.join(bTagPerfHistos[bTagPerfHistos.keys()[0]].keys())

    outputDir = '/'.join([ opt.plotsdir, opt.year, opt.method+'Results', tagFlag, resultToPlot ]) 
    os.system('mkdir -p '+outputDir+' ; cp ../../index.php '+opt.plotsdir)
    commonTools.copyIndexForPlots(opt.plotsdir, outputDir)

    canvas.Print(outputDir+'/'+btagWP+'_'+systematicFlag+opt.fitOption+'.png')

def computeFinalScaleFactors(opt):

    systematics, selections = [], []
    for systematic in opt.Selections:
        if systematic!='' and 'Down' not in systematic: 
            systematics.append(systematic.replace('Up',''))
            if systematic.replace('Up','') not in opt.systematicNuisances: selections.append(systematic.replace('Up',''))

    for btagWP in opt.btagWPs:

        wpSF = copy.deepcopy(opt.bTagPerfResults[btagWP])
        opt.bTagPerfResults[btagWP]['Final'] = {}
        opt.bTagPerfResults[btagWP]['StatisticsUp'] = {}
        opt.bTagPerfResults[btagWP]['StatisticsDown'] = {}
        opt.bTagPerfResults[btagWP]['FinalSystematics'] = {}
        opt.bTagPerfResults[btagWP]['FinalUp'] = {}
        opt.bTagPerfResults[btagWP]['FinalDown'] = {}

        for ptbin in opt.ptBins:

            centralSF = wpSF['Central'][ptbin]['scaleFactor']
            centralSFerror = wpSF['Central'][ptbin]['scaleFactorUncertainty']

            systSF, systSFerror = {}, {}
            for systematic in systematics:
                if systematic+'Up' in opt.Selections:
                    systSF[systematic], systSFerror[systematic] = {}, {}
                    sfUp, sfDown = 'Up', 'Down'
                    if wpSF[systematic+'Up'][ptbin]['scaleFactor']<wpSF[systematic+'Down'][ptbin]['scaleFactor']:
                        sfUp, sfDown = 'Down', 'Up'
                    systSF[systematic]['Up'] = wpSF[systematic+sfUp][ptbin]['scaleFactor']
                    systSF[systematic]['Down'] = wpSF[systematic+sfDown][ptbin]['scaleFactor']
                    systSFerror[systematic]['Up'] = wpSF[systematic+sfUp][ptbin]['scaleFactorUncertainty']
                    systSFerror[systematic]['Down'] = wpSF[systematic+sfDown][ptbin]['scaleFactorUncertainty']

            goodCentral = False

            if centralSF>0.1 and wpSF['Central'][ptbin]['efficiencyFit']>0.01:
                for systematic in selections:
                    if systematic+'Up' in opt.Selections:
                        if centralSF>=systSF[systematic]['Down'] and centralSF<=systSF[systematic]['Up']:
                            goodCentral = True
            
            if goodCentral: finalScaleFactor, finalScaleFactorUncertainty = centralSF, centralSFerror
            else: 
               
                finalScaleFactor, finalScaleFactorUncertainty, scaleFactorSystematicUncertainty = -1., -1., -1.

                scaleFactorList, scaleFactorUncertaintyList = [], []
                for systematic in wpSF.keys():
                    if systematic=='Central' or systematic.replace('Up','').replace('Down','') in selections:
                        if wpSF[systematic][ptbin]['scaleFactor']>0.1 and wpSF[systematic][ptbin]['efficiencyFit']>0.01: 
                            scaleFactorList.append(wpSF[systematic][ptbin]['scaleFactor'])
                            scaleFactorUncertaintyList.append(wpSF[systematic][ptbin]['scaleFactorUncertainty'])

                hasOutliers = True
                while len(scaleFactorList)>0 and hasOutliers:
                    
                    finalScaleFactor = sum(scaleFactorList)/len(scaleFactorList)
                    finalScaleFactorUncertainty = sum(scaleFactorUncertaintyList)/len(scaleFactorUncertaintyList)
                    standardDeviaton = 0.
                    for sfValue in scaleFactorList: standardDeviaton += pow(sfValue-finalScaleFactor, 2)
                    standardDeviaton = math.sqrt(standardDeviaton/len(scaleFactorList))

                    scaleFactorToRemove = []
                    for sfValue in scaleFactorList:
                        if abs(sfValue-finalScaleFactor)>2.*standardDeviaton: scaleFactorToRemove.append(sfValue)
                    for sfValue in scaleFactorToRemove: 
                        scaleFactorList.remove(sfValue)
                    hasOutliers = len(scaleFactorToRemove)>0

            if finalScaleFactor>0.: 

                if opt.verbose: print '####', btagWP, ptbin

                scaleFactorSystematicUncertainty = pow(finalScaleFactorUncertainty,2)    

                for systematic in systematics:

                    systematicVariations = {}

                    for variation in [ '', 'Up', 'Down' ]:
                        if systematic+variation in wpSF:
                            if wpSF[systematic+variation][ptbin]['scaleFactor']>0.1 and wpSF[systematic+variation][ptbin]['efficiencyFit']>0.01:
                                if wpSF[systematic+variation][ptbin]['scaleFactorUncertainty']<0.1 and abs(wpSF[systematic+variation][ptbin]['scaleFactor']-finalScaleFactor)<0.2:
                                    systematicVariations[variation] = wpSF[systematic+variation][ptbin]['scaleFactor']-finalScaleFactor

                    if len(systematicVariations.keys())==2:
                        if max(abs(systematicVariations['Up']),abs(systematicVariations['Down']))>0.1:
                            if min(abs(systematicVariations['Up']),abs(systematicVariations['Down']))>0.02:
                                if abs(systematicVariations['Up'])>abs(systematicVariations['Down']): del systematicVariations['Up']
                                else: del systematicVariations['Down']

                    if len(systematicVariations.keys())==0: 
                        systematicUncertainty = 0.05*finalScaleFactor # Bho?
                    elif len(systematicVariations.keys())==1: 
                        for variation in systematicVariations.keys():
                             systematicUncertainty = systematicVariations[variation] if variation!='Down' else -systematicVariations[variation]
                    else: 
                        systematicUncertainty = (abs(systematicVariations['Up'])+abs(systematicVariations['Down']))/2.
                        if systematicVariations['Up']*systematicVariations['Down']<0.: systematicUncertainty = math.copysign(systematicUncertainty, systematicVariations['Up'])
                        elif abs(systematicVariations['Up'])>=abs(systematicVariations['Down']): systematicUncertainty = math.copysign(systematicUncertainty, systematicVariations['Up'])
                        else: systematicUncertainty = math.copysign(systematicUncertainty, -systematicVariations['Up'])

                    for variation in ['Up', 'Down' ]: 
                        if systematic+variation not in opt.bTagPerfResults[btagWP]:
                            opt.bTagPerfResults[btagWP][systematic+variation] = {}
                        if ptbin not in opt.bTagPerfResults[btagWP][systematic+variation]:
                            opt.bTagPerfResults[btagWP][systematic+variation][ptbin] = {} 

                    if opt.verbose: print '    ', systematic, systematicUncertainty

                    opt.bTagPerfResults[btagWP][systematic+'Up'][ptbin]['scaleFactor'] = finalScaleFactor + systematicUncertainty
                    opt.bTagPerfResults[btagWP][systematic+'Down'][ptbin]['scaleFactor'] = finalScaleFactor - systematicUncertainty
                              
                    scaleFactorSystematicUncertainty += pow(systematicUncertainty,2)

                scaleFactorSystematicUncertainty = math.sqrt(scaleFactorSystematicUncertainty)

                if opt.verbose: print '     Total', scaleFactorSystematicUncertainty, '\n\n'    

            opt.bTagPerfResults[btagWP]['Final'][ptbin] = {}
            opt.bTagPerfResults[btagWP]['Final'][ptbin]['scaleFactor'] = finalScaleFactor
            opt.bTagPerfResults[btagWP]['Final'][ptbin]['scaleFactorUncertainty'] = finalScaleFactorUncertainty
            opt.bTagPerfResults[btagWP]['StatisticsUp'][ptbin], opt.bTagPerfResults[btagWP]['StatisticsDown'][ptbin] = {}, {}
            opt.bTagPerfResults[btagWP]['StatisticsUp'][ptbin]['scaleFactor'] = finalScaleFactor + finalScaleFactorUncertainty
            opt.bTagPerfResults[btagWP]['StatisticsDown'][ptbin]['scaleFactor'] = finalScaleFactor - finalScaleFactorUncertainty
            opt.bTagPerfResults[btagWP]['FinalSystematics'][ptbin] = {}
            opt.bTagPerfResults[btagWP]['FinalSystematics'][ptbin]['scaleFactor'] = finalScaleFactor
            opt.bTagPerfResults[btagWP]['FinalSystematics'][ptbin]['scaleFactorUncertainty'] = scaleFactorSystematicUncertainty
            opt.bTagPerfResults[btagWP]['FinalUp'][ptbin], opt.bTagPerfResults[btagWP]['FinalDown'][ptbin] = {}, {} 
            opt.bTagPerfResults[btagWP]['FinalUp'][ptbin]['scaleFactor'] = finalScaleFactor + scaleFactorSystematicUncertainty
            opt.bTagPerfResults[btagWP]['FinalDown'][ptbin]['scaleFactor'] = finalScaleFactor - scaleFactorSystematicUncertainty

def getSystematicsForComparison(opt):

    systematicToCompare = [ ]

    for selection in opt.Selections:
        if selection.replace('Up','').replace('Down','') in opt.option:
            if selection not in systematicToCompare:
                systematicToCompare.append(selection)

    return systematicToCompare

def bTagPerfResults(opt, action='plot'):

    opt.bTagPerfResults = {} 
    opt2 = copy.deepcopy(opt)

    for tag in opt.tag.split('-'):

        rawTag = tag.split('__')[0]
        if '_mergedSelections' in tag:
            if  '_mergedSelections' not in rawTag: rawTag += '_mergedSelections'
            if '_nuisSelections' in tag and '_nuisSelections' not in rawTag: rawTag += '_nuisSelections'
        if '_mergedJetPtBins' in tag and '_mergedJetPtBins' not in rawTag: rawTag += '_mergedJetPtBins'       
 
        opt2.tag = rawTag
        getBTagPerfResults(opt2)

        if 'plot' in action or 'store' in action: 
            opt.fitOption = ''
            if 'finalplot' in action or 'store' in action: 
                if '_nuisSelections' in tag: opt.fitOption = '_nuisSelections'    
                computeFinalScaleFactors(opt2)
        opt.bTagPerfResults[rawTag] = opt2.bTagPerfResults
 
def printBTagPerformance(opt):

    bTagPerfResults(opt, action='print')

    for btagWP in opt.btagWPs:
        for ptbin in opt.ptBins:
            print '####', btagWP, ptbin
            for tag in opt.bTagPerfResults:    
                for systematic in opt.Selections:
                    syst = systematic if systematic!='' else 'Central'
                    bTagPerfShort = opt.bTagPerfResults[tag][btagWP][syst]
                    print '    ', tag, syst, bTagPerfShort[ptbin]['efficiencyMC'], bTagPerfShort[ptbin]['efficiencyFit'], bTagPerfShort[ptbin]['scaleFactor'], bTagPerfShort[ptbin]['scaleFactorUncertainty']
                print ''

def plotBTagPerformance(opt, resultToPlot='performance', action='plot'):

    if 'DepOn' in opt.option:
        opt.Selections = getSystematicsForComparison(opt)
        if len(opt.Selections)<2: return

    bTagPerfResults(opt, action)   

    if action=='finalplot':
        opt.Selections = [ 'FinalSystematics', 'Final', 'Central' ] if 'central' in opt.option.lower() else [ 'FinalSystematics', 'Final' ]
        opt.option = 'FinalCompared' if len(opt.Selections)>2 else 'Final' 
    elif opt.Selections[0]=='': opt.Selections[0] = 'Central'

    bTagPerfHistos = {}
    for btagWP in opt.btagWPs:
        bTagPerfHistos[btagWP] = {}
        for tag in opt.bTagPerfResults:
            bTagPerfHistos[btagWP][tag] = {}
            for systematic in opt.Selections:
                bTagPerfHistos[btagWP][tag][systematic] = {}
                for result in [ 'efficiencyMC', 'efficiencyFit', 'scaleFactor' ]:
                    if resultToPlot in result.lower() or resultToPlot=='performance':
                        bTagPerfHistos[btagWP][tag][systematic][result] = fillBTagPerfHistogram(opt, result, btagWP, opt.bTagPerfResults[tag][btagWP][systematic])

    for btagWP in opt.btagWPs:
        makeBTagPerformancePlot(opt, btagWP, bTagPerfHistos[btagWP], resultToPlot)

def plotBTagEfficiencies(opt):
 
    plotBTagPerformance(opt, resultToPlot='efficiency')

def plotBTagScaleFactors(opt):

    plotBTagPerformance(opt, resultToPlot='scalefactor') 

def analyzeBTagScaleFactorSytematics(opt):

    resultToPlot = 'performance' if 'performance' in opt.option else 'efficiency' if 'efficiency' in opt.option else 'scalefactor'

    opt.origSelections = opt.Selections

    for systematic in opt.origSelections: 
        if systematic!='' and 'Down' not in systematic:
            opt.option = 'DepOn' + systematic.replace('Up','')
            plotBTagPerformance(opt, resultToPlot)
            opt.Selections = opt.origSelections

def plotFinalBTagScaleFactors(opt):

    plotBTagPerformance(opt, action='finalplot', resultToPlot='scalefactor')

### Store scale factores

def storeBTagScaleFactors(opt):

    operatingPoints = { 'L'   : ROOT.BTagEntry.OperatingPoint.OP_LOOSE, 
                        'M'   : ROOT.BTagEntry.OperatingPoint.OP_MEDIUM, 
                        'T'   : ROOT.BTagEntry.OperatingPoint.OP_TIGHT,
                        'VT'  : ROOT.BTagEntry.OperatingPoint.OP_LOOSE,
                        'VVT' : ROOT.BTagEntry.OperatingPoint.OP_MEDIUM
                       } 

    bTagPerfResults(opt, action='store')

    systematics = [ 'Central' ]
    for systematic in opt.Selections:
        if systematic!='' and 'Down' not in systematic: systematics.append(systematic.replace('Up',''))

    for tag in opt.bTagPerfResults:
 
        csvDirectory = '/'.join([ '.', 'CSVFiles', tag, '' ])
        os.system('mkdir -p '+csvDirectory)

        btagAlgorithms = {}
        for btagAlgorithm in opt.bTagAlgorithms:
            for btagWP in opt.bTagPerfResults[tag]:
                if btagAlgorithm in btagWP:
                    if btagAlgorithm not in btagAlgorithms: btagAlgorithms[btagAlgorithm] = [ btagWP ]
                    else: btagAlgorithms[btagAlgorithm].append(btagWP)
 
        for btagAlgorithm in btagAlgorithms:
             
            csvFileName = btagAlgorithm if len(btagAlgorithms[btagAlgorithm])>1 else btagAlgorithms[btagAlgorithm][0]
            csvFile = ROOT.BTagCalibration(csvFileName+'_' +opt.method+opt.fitOption+'.csv')

            for btagWP in sorted(btagAlgorithms[btagAlgorithm]):
                for systematic in opt.csvSystematics:
                    if opt.csvSystematics[systematic] in opt.bTagPerfResults[tag][btagWP]:
                        for ptbin in opt.bTagPerfResults[tag][btagWP][opt.csvSystematics[systematic]]:
  
                            ptMin = float(ptbin.replace('Pt','').split('to')[0])
                            ptMax = float(ptbin.replace('Pt','').split('to')[1])
                            params = ROOT.BTagEntry.Parameters(operatingPoints[btagWP.replace(btagAlgorithm,'')], opt.method.lower(), systematic, 
                                                               ROOT.BTagEntry.FLAV_B, -opt.maxJetEta, opt.maxJetEta, ptMin, ptMax, 0., 1.)

                            SFFun = ROOT.TF1 ('SFFun', str(opt.bTagPerfResults[tag][btagWP][opt.csvSystematics[systematic]][ptbin]['scaleFactor']), ptMin, ptMax)
                            entry = ROOT.BTagEntry(SFFun, params)
                            csvFile.addEntry(entry)
           
            with open(csvDirectory+'/'+csvFileName+'_' +opt.method+opt.fitOption+'.csv', 'w') as f:
                f.write(csvFile.makeCSV())
                                
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

            #opt.workingPointName = [ 'Loose', 'Medium', 'Tight', 'VeryTight', 'VeryVeryTight' ]
            #opt.workingPointLimit = [ 0.1, 0.01, 0.001, 0.0005, 0.0001 ]

            oldWorkingPoint = []
            for wp in opt.workingPointName:
                wpflag = ''.join([ x for x in wp if x.isupper() ])
                if btagwp[:-1]+wpflag in opt.bTagWorkingPoints: oldWorkingPoint.append(float(opt.bTagWorkingPoints[btagwp[:-1]+wpflag]['cut']))
                else: oldWorkingPoint.append(0.9) 

            integralLightJets  = lJetDisc.Integral(0, lJetDisc.GetNbinsX())
            integralBottomJets = bJetDisc.Integral(0, bJetDisc.GetNbinsX())
 
            if 'csv' in opt.option:
                print '   ', btagwp[:-1],
            elif 'yml' in opt.option:
                print btagwp[:-1]+':'

            for wp in range(len(opt.workingPointName)):

                wpflag = ''.join([ x for x in opt.workingPointName[wp] if x.isupper() ])
                mistagRateDistance =  999.
                binAtWorkingPoint  = -999

                for ib in range(1, bJetDisc.GetNbinsX()+1):

                    mistagRate = lJetDisc.Integral(ib, lJetDisc.GetNbinsX())/integralLightJets

                    if abs(mistagRate-opt.workingPointLimit[wp])<mistagRateDistance: 

                        mistagRateDistance = abs(mistagRate-opt.workingPointLimit[wp])
                        binAtWorkingPoint = ib

                if 'noprint' not in opt.option:
                    print '   ', opt.workingPointName[wp], 'working point:', lJetDisc.GetBinLowEdge(binAtWorkingPoint), '(', lJetDisc.GetBinLowEdge(binAtWorkingPoint-1), ',', lJetDisc.GetBinLowEdge(binAtWorkingPoint+1), ')'
                    print '        MistagRate:', lJetDisc.Integral(binAtWorkingPoint, lJetDisc.GetNbinsX())/integralLightJets, '(', lJetDisc.Integral(binAtWorkingPoint-1, lJetDisc.GetNbinsX())/integralLightJets, ', ', lJetDisc.Integral(binAtWorkingPoint+1, lJetDisc.GetNbinsX())/integralLightJets, ') over', integralLightJets
                    print '        Efficiency:', bJetDisc.Integral(binAtWorkingPoint, bJetDisc.GetNbinsX())/integralBottomJets, '(', bJetDisc.Integral(binAtWorkingPoint-1, bJetDisc.GetNbinsX())/integralBottomJets, ', ', bJetDisc.Integral(binAtWorkingPoint+1, bJetDisc.GetNbinsX())/integralBottomJets, ') over', integralBottomJets

                    binOldWorkingPoint = lJetDisc.FindBin(oldWorkingPoint[wp])
                    print '        OldWorkingPoint', oldWorkingPoint[wp], lJetDisc.Integral(binOldWorkingPoint, lJetDisc.GetNbinsX())/integralLightJets, bJetDisc.Integral(binOldWorkingPoint, lJetDisc.GetNbinsX())/integralBottomJets, '\n'

                elif 'csv' in opt.option:
                    print lJetDisc.GetBinLowEdge(binAtWorkingPoint), 
                    print round((100.*bJetDisc.Integral(binAtWorkingPoint, bJetDisc.GetNbinsX())/integralBottomJets),1),
                    print round((100.*lJetDisc.Integral(binAtWorkingPoint, lJetDisc.GetNbinsX())/integralLightJets),1 if opt.workingPointName[wp]=='Loose' else 2), 
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

