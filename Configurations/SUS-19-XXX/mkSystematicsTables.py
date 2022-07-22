#!/usr/bin/env python
import timeit
import optparse
import sys  
import os
import math
import ROOT
import LatinoAnalysis.Gardener.hwwtools as hwwtools
from collections import OrderedDict

def getMaxBinForShapeUncertainty(NbinsX, cut):

    if opt.useallshapebins: return NbinsX
    if 'Stop' in opt.tag:
        if 'SR3' in cut or 'SR4' in cut: return 6
        else: return NbinsX
    else:
        if 'SR1' in cut: return 7
        elif 'SR2' in cut or 'SR3' in cut: return 8
        else: return NbinsX

def getShapes(systematic, cuts, variables, samples, systSamples, inputFile):

    shapesList = [ ]

    for cut in cuts:
        if 'SR' in cut:

            if '_Tag_' in cut and not opt.includetagsr: continue

            # Here we are assuming one variable for cut!
            for variable in variables:
                if 'cuts' not in variables[variable] or cut in variables[variable]['cuts']:
                    fitvariable = variable

            if fitvariable==None:
                print 'mkSystematicsTables: fit variable not found for cut', cut
                exit()

            folder = inputFile.Get(cut+'/'+fitvariable)

            thisShape = ROOT.TH1F(cut, cut, len(variables[fitvariable]['range'][0])-1, array('d',variables[fitvariable]['range'][0]))
            thisShape.SetDirectory(0)
 
            for sample in samples:
                if (('SM' in opt.samples or sample==opt.samples) and not samples[sample]['isSignal'] and not samples[sample]['isDATA']) or (samples[sample]['isSignal'] and sample in opt.samples):
                    if folder.GetListOfKeys().Contains('histo_'+sample+systematic):
                        thisShape.Add(folder.Get('histo_'+sample+systematic))
                    elif folder.GetListOfKeys().Contains('histo_'+sample): 
                        lnNweight = 1.
                        if 'lnN' in systematic and sample in systSamples:
                            if 'Up' in systematic: lnNweight = float(systSamples[sample])
                            else: lnNweight = 2. - float(systSamples[sample])
                        thisShape.Add(folder.Get('histo_'+sample), lnNweight)
                    else:
                        print 'Warning: missing shapes for sample', sample, 'in cut', cut+'/'+fitvariable

            shapesList.append(thisShape)

    return shapesList

def intround(x): 
    return int(round(x)) 

def getProperRange(minUncertainty, maxUncertainty):

    if maxUncertainty<1.e-04: return '---'
  
    minUncertainty = round(minUncertainty, 1) if minUncertainty<10. else intround(minUncertainty)
    maxUncertainty = round(maxUncertainty, 1) if maxUncertainty<10. else intround(maxUncertainty)

    if maxUncertainty<1.:
        return '$\\lt 1\\%$'

    if minUncertainty==maxUncertainty:
        return '$'+str(maxUncertainty)+'\\%$'

    if round(minUncertainty)<1.:
        return '$\\le '+str(intround(maxUncertainty))+'\\%$' 

    if round(minUncertainty)==round(maxUncertainty):
        return '$'+str(intround(maxUncertainty))+'\\%$'

    return '$'+str(intround(minUncertainty))+'$--$'+str(intround(maxUncertainty))+'\\%$'

systematicDictionary = OrderedDict()
systematicDictionary['lumi']         = 'Integrated luminosity'
systematicDictionary['trigger']      = 'Trigger efficiency'
systematicDictionary['pileup']       = 'Pileup'
systematicDictionary['jesTotal']     = 'Jet energy scale'
systematicDictionary['jer']          = 'Jet energy resolution'
systematicDictionary['unclustEn']    =  'Unclustered energy'
systematicDictionary['prefiring']    =  'Prefiring'
systematicDictionary['lepReco']      =  'Lepton reconstruction'
systematicDictionary['lepReco']      =  'Lepton reconstruction'
systematicDictionary['lepIdIso']     =  'Lepton ident./isolation'
systematicDictionary['lepExtra']     =  'Lepton additional cuts'
systematicDictionary['btag']         =  'b tagging'
systematicDictionary['mistag']       =  'b tagging (light jets)'
systematicDictionary['stat']         =  'Simulated samples statistics'
systematicDictionary['qcdScale']     =  'Renorm./fact. scales'
systematicDictionary['pdf']          =  'PDFs'
systematicDictionary['normDYall']    =  '\\DY normalization'
systematicDictionary['normSTtWall']  =  '\\tW normalization'
systematicDictionary['normMinorBkg'] =  'Minor bkg. normalization'
systematicDictionary['nonpromptLep'] =  'Nonprompt leptons'
systematicDictionary['toppt']        = '\\ttbar \\pt reweighting'
systematicDictionary['isrFS']        = 'ISR reweighting'
systematicDictionary['leptonIdIsoFS']= 'Lepton ident./isolation (\\FastSim)'
systematicDictionary['btagFS']       = 'b tagging (\\FastSim'
systematicDictionary['ptmissfastsim']= '\\ptmiss (\\FastSim)'

if __name__ == '__main__':

    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)

    parser.add_option('--inputdir'          , dest='inputdir'          , help='Input directory'                          , default='./Shapes')
    parser.add_option('--tag'               , dest='tag'               , help='Tag used for the tag file name'           , default='')
    parser.add_option('--sigset'            , dest='sigset'            , help='Sigset'                                   , default='SM')
    parser.add_option('--samples'           , dest='samples'           , help='Samples'                                  , default='SM')
    parser.add_option('--years'             , dest='years'             , help='Year to be processed. Default: all'       , default='all')
    parser.add_option('--postFit'           , dest='postFit'           , help='Fake'                                     , default='n')
    parser.add_option('--error'             , dest='error'             , help='0 -> symmetric, 1 -> maximum'             , default=0)
    parser.add_option('--keepsplit'         , dest='keepsplit'         , help='Keep split systematic unmerged'           , default=False, action='store_true')
    parser.add_option('--useallshapebins'   , dest='useallshapebins'   , help='Use all bins, not the more significant'   , default=False, action='store_true')
    parser.add_option('--tablelevel'        , dest='tablelevel'        , help='Table level'                              , default='ptmiss')
    parser.add_option('--splitminorbkg'     , dest='splitminorbkg'     , help='Split minor backgrounds'                  , default=False, action='store_true')
    parser.add_option('--includetagsr'      , dest='includetagsr'      , help='Include Tag signal region'                , default=False, action='store_true')
    parser.add_option('--debugcut'          , dest='debugcut'          , help='Debug cut'                                , default='XXX')
    parser.add_option('--debugsyst'         , dest='debugsyst'         , help='Debug systematic'                         , default='XXX')
    parser.add_option('--usemaxshape'       , dest='usemaxshape'       , help='Use max shape instead of symmetric'       , default=False, action='store_true')
    # read default parsing options as well
    hwwtools.addOptions(parser)
    hwwtools.loadOptDefaults(parser)
    (opt, args) = parser.parse_args()

    if opt.years=='-1' or opt.years=='all':
        yearset='2016-2017-2018'
    elif opt.years=='0':
        yearset='2016'
    elif opt.years=='1':
        yearset='2017'
    elif opt.years=='2':
        yearset='2018'
    else:
        yearset=opt.years

    tag = opt.tag

    opt.mergesplit = not opt.keepsplit
    opt.mergeminorbkg = not opt.splitminorbkg
    opt.includetagsr = opt.includetagsr or 'Stop' in opt.tag

    systematics = { }

    for datayear in yearset.split('-'):

        inputFile = ROOT.TFile(opt.inputdir+'/'+datayear+'/'+tag+'/plots_'+tag+'_'+opt.sigset+'.root', 'READ')

        opt.tag = datayear + tag
 
        samples = { }
        cuts = { }
        variables = { }
        nuisances = { }

        exec(open(opt.samplesFile).read())
        exec(open(opt.cutsFile).read())
        exec(open(opt.variablesFile).read())
        exec(open('./nuisances.py').read())

        centralShapes = getShapes('', cuts, variables, samples, samples, inputFile)

        if 'stat' not in systematics:
            systematics['stat'] = { }

        for centralShape in centralShapes:
            if centralShape.GetBinContent(centralShape.GetNbinsX()+1)!=0.: print 'HORROR'
            if centralShape.Integral()==0.: continue
            systematics['stat'][datayear+'_'+centralShape.GetName()] = { }
            centralIntegralError = ROOT.double(); centralIntegral = centralShape.IntegralAndError(-1, -1, centralIntegralError)
            systematics['stat'][datayear+'_'+centralShape.GetName()]['integralUncertainty'] = 100.*centralIntegralError/centralIntegral
            shapeUncertainty = -1.
            for ib in range(getMaxBinForShapeUncertainty(centralShape.GetNbinsX(), centralShape.GetName())):           
                if centralShape.GetBinContent(ib+1)>0.:
                    if opt.sigset!='SM' and (ib+1<5 or centralShape.GetBinContent(ib+1)<0.3): continue
                    shapeUncertainty = max(100.*centralShape.GetBinError(ib+1)/centralShape.GetBinContent(ib+1), shapeUncertainty)
            systematics['stat'][datayear+'_'+centralShape.GetName()]['shapeUncertainty'] = shapeUncertainty

        for nuisance in nuisances:

            if nuisance=='stat': continue

            hasSamples = False
            for sample in nuisances[nuisance]['samples']:
                if (('SM' in opt.samples or sample==opt.samples) and not samples[sample]['isSignal'] and not samples[sample]['isDATA']) or (samples[sample]['isSignal'] and sample in opt.samples):
                    hasSamples = True
                    break

            if not hasSamples: continue

            systematic = nuisances[nuisance]['name'].replace(datayear, 'uncorrelated').replace('ctagFS', 'btagFS_c').replace('mistagFS', 'btagFS_l') 
            if opt.mergeminorbkg and 'DY' not in systematic and 'STtW' not in systematic: systematic = systematic.replace('norm', 'normMinorBkg_')

            if systematic not in systematics:
                systematics[systematic] = { }
             
            systCuts = cuts if 'cuts' not in nuisances[nuisance] else nuisances[nuisance]['cuts']

            variation = '_'+nuisances[nuisance]['name'] if nuisances[nuisance]['type']=='shape' else 'lnN'
 
            systematicShapesUp = getShapes(variation+'Up',   systCuts, variables, samples, nuisances[nuisance]['samples'], inputFile)
            systematicShapesDo = getShapes(variation+'Down', systCuts, variables, samples, nuisances[nuisance]['samples'], inputFile)
                                        
            for cut in systCuts:

                if '_Tag_' in cut and not opt.includetagsr: continue

                for centralShape in centralShapes:
                    if centralShape.GetName()==cut: 
                        break

                if centralShape.Integral()==0.: continue

                for upShape in systematicShapesUp:
                    if upShape.GetName()==cut:
                        break

                for doShape in systematicShapesDo:
                    if doShape.GetName()==cut:
                        break

                if opt.debugcut in cut or opt.debugsyst in systematic:
                    print systematic, cut
                    print 'Integral', centralShape.Integral(), upShape.Integral(), doShape.Integral()
                    print 'Entries', centralShape.GetEntries(), upShape.GetEntries(), doShape.GetEntries()
                    for ib in range(centralShape.GetNbinsX()):
                        if centralShape.GetBinContent(ib+1)>0.:
                            if abs(upShape.GetBinContent(ib+1)/centralShape.GetBinContent(ib+1)-1.)>0.5 or abs(doShape.GetBinContent(ib+1)/centralShape.GetBinContent(ib+1)-1.)>0.5:
                                print ib+1, 'yields   ', centralShape.GetBinContent(ib+1), upShape.GetBinContent(ib+1), doShape.GetBinContent(ib+1)
                                print ib+1, 'error    ', centralShape.GetBinError(ib+1), upShape.GetBinError(ib+1), doShape.GetBinError(ib+1)
                                print ib+1, 'rel. err.', str(100.*abs(upShape.GetBinContent(ib+1)/centralShape.GetBinContent(ib+1)-1.))+'%', str(100.*abs(doShape.GetBinContent(ib+1)/centralShape.GetBinContent(ib+1)-1.))+'%'
                        elif upShape.GetBinContent(ib+1)>0. or doShape.GetBinContent(ib+1)>0.:
                                print '>>>      ', centralShape.GetBinContent(ib+1), upShape.GetBinContent(ib+1), doShape.GetBinContent(ib+1)

                systUp = 100.*abs(upShape.Integral() - centralShape.Integral())/centralShape.Integral()
                systDo = 100.*abs(doShape.Integral() - centralShape.Integral())/centralShape.Integral()                   
                systSm = 100.*abs(upShape.Integral() -      doShape.Integral())/centralShape.Integral()/2.

                integralUncertainty = systSm if opt.error==0 else max(systUp, systDo)

                upShape.Scale(centralShape.Integral()/upShape.Integral()); upShape.Divide(centralShape)
                doShape.Scale(centralShape.Integral()/doShape.Integral()); doShape.Divide(centralShape)

                shapeUncertainty = -1.       
                for ib in range(getMaxBinForShapeUncertainty(centralShape.GetNbinsX(), cut)):
                    if centralShape.GetBinContent(ib+1)==0.:
                        fixedUpContent = 1. if upShape.GetBinContent(ib+1)==0. else 1.; upShape.SetBinContent(ib+1, fixedUpContent)
                        fixedDoContent = 1. if doShape.GetBinContent(ib+1)==0. else 1.; doShape.SetBinContent(ib+1, fixedUpContent)
                    if opt.sigset!='SM' and (ib+1<5 or centralShape.GetBinContent(ib+1)<0.3):
                        continue
                    if opt.usemaxshape:
                        shapeUncertainty = max(100.*abs(upShape.GetBinContent(ib+1) - 1.), shapeUncertainty)
                        shapeUncertainty = max(100.*abs(doShape.GetBinContent(ib+1) - 1.), shapeUncertainty)
                    else:
                        shapeUncertainty = max(100.*abs(upShape.GetBinContent(ib+1) - doShape.GetBinContent(ib+1))/2, shapeUncertainty)

                systematics[systematic][datayear+'_'+cut] = { }   
                systematics[systematic][datayear+'_'+cut]['integralUncertainty'] = integralUncertainty
                systematics[systematic][datayear+'_'+cut]['shapeUncertainty'] = shapeUncertainty

    if opt.mergesplit:

        systematicsToMerge = { }

        for systematic in systematics:
            for testedsyst in systematics:
                if systematic!=testedsyst and systematic.split('_')[0]==testedsyst.split('_')[0]:
                    if systematic.split('_')[0] not in systematicsToMerge:
                        systematicsToMerge[systematic.split('_')[0]] = [ systematic ]
                    if testedsyst not in systematicsToMerge[systematic.split('_')[0]]:
                        systematicsToMerge[systematic.split('_')[0]].append(testedsyst)

        for mergedsyst in systematicsToMerge:

            systematics[mergedsyst+'_total'] = { }

            for syst2merge in systematicsToMerge[mergedsyst]:
                for cut in systematics[syst2merge]:
                    if cut not in systematics[mergedsyst+'_total']:
                        systematics[mergedsyst+'_total'][cut] = { }
                        systematics[mergedsyst+'_total'][cut]['integralUncertainty'] = 0.
                        systematics[mergedsyst+'_total'][cut]['shapeUncertainty'] = 0.
                    systematics[mergedsyst+'_total'][cut]['integralUncertainty'] += pow(systematics[syst2merge][cut]['integralUncertainty'] ,2)
                    systematics[mergedsyst+'_total'][cut]['shapeUncertainty'] += pow(systematics[syst2merge][cut]['shapeUncertainty'] ,2)
                del systematics[syst2merge]
    

            for cut in systematics[mergedsyst+'_total']:
                systematics[mergedsyst+'_total'][cut]['integralUncertainty'] = math.sqrt(systematics[mergedsyst+'_total'][cut]['integralUncertainty'])
                systematics[mergedsyst+'_total'][cut]['shapeUncertainty'] = math.sqrt(systematics[mergedsyst+'_total'][cut]['shapeUncertainty']) 

    systematicColumns = { }

    for systematic in systematics:
        for cut in systematics[systematic]:
            columnElements = [ ]
            if 'year'   in opt.tablelevel: columnElements.append(cut.split('_')[0])
            if 'ptmiss' in opt.tablelevel: columnElements.append(cut.split('_')[1])
            if 'jet'    in opt.tablelevel: columnElements.append(cut.split('_')[2])
            if 'flav'   in opt.tablelevel: columnElements.append(cut.split('_')[3])
            if len(columnElements)==0: column = 'SM processes'
            else: column = '_'.join(columnElements)
            if column not in systematicColumns:
                systematicColumns[column] = [ ]
            systematicColumns[column].append(cut)
 
    for systematic in systematics:
        if systematic.split('_')[0] not in systematicDictionary:
            print 'Error:', systematic.split('_')[0], 'not in dictionary'
            exit()

    yieldHeader, shapeHeader = 'Change in yields', 'Change in \\mtll shape' 
    if len(systematicColumns.keys())>1:
        yieldHeader, shapeHeader = 'Yields', '\\mtll shape'

    table  = '\\begin{table}[hbt]\\centering\n'
    table += '  \\topcaption{\\label{tab:syst_'+yearset+'_'+opt.samples+'_'+opt.tablelevel+'} Sizes of systematic uncertainties in the predicted yields for '+opt.samples+' processes. The first column shows the range of the uncertainties in the global background normalization across the different SRs. The second column quantifies the effect on the \\mtll shape. This is computedSizes of systematic uncertainties in the predicted yields for SM processes. The first by taking the maximum variation across the \\mtll bins (after renormalizing for the global change of all the distribution) in each SR. The range of this variation across the SRs is given.}\n'
    table += '  \\cmsTable {\n'
    table += '    \\begin{tabular}{l'+'cc'*len(systematicColumns.keys())+'}\n'
    table += '    \\hline\n'
    table += '    \multirow{2}{*}{Source of uncertainty}'
    for column in sorted(systematicColumns):
        table += ' & \multicolumn{2}{c}{'+column+'}'
    table += ' \\\\\n'
    table += '    '
    for column in systematicColumns:
        table += ' & '+yieldHeader+' & '+shapeHeader
    table += ' \\\\\n'     
    table += '    \\hline\n'

    for systematicInDictionary in systematicDictionary:
        
        systematicInDictionaryList = [ ]
        for systematic in systematics:
            if systematicInDictionary==systematic.split('_')[0]:
                systematicInDictionaryList.append(systematic) 

        for systematic in systematicInDictionaryList:

            if len(systematicInDictionaryList)>1:
                print 'Warning: systematic legend to be complited in case of split uncertainty'

            table += '    '+systematicDictionary[systematicInDictionary]

            for column in sorted(systematicColumns):
                minIntegralUncertainty, maxIntegralUncertainty, minShapeUncertainty, maxShapeUncertainty = 999., 0., 999., 0.
                for cut in systematicColumns[column]:
                     if cut in systematics[systematic]:

                         if systematics[systematic][cut]['integralUncertainty']>=0.:
                             minIntegralUncertainty = min(systematics[systematic][cut]['integralUncertainty'], minIntegralUncertainty)
                             maxIntegralUncertainty = max(systematics[systematic][cut]['integralUncertainty'], maxIntegralUncertainty)

                         if systematics[systematic][cut]['shapeUncertainty']>=0.:
                             minShapeUncertainty    = min(systematics[systematic][cut]['shapeUncertainty'],    minShapeUncertainty)
                             maxShapeUncertainty    = max(systematics[systematic][cut]['shapeUncertainty'],    maxShapeUncertainty)

                table += ' & '+getProperRange(minIntegralUncertainty, maxIntegralUncertainty)
                table += ' & '+getProperRange(minShapeUncertainty,    maxShapeUncertainty)

            table += '\\\\\n'

    table += '    \\hline\n'
    table += '    \\end{tabular}\n'
    table += '  }\n'
    table += '\\end{table}\n'

    print table




           

