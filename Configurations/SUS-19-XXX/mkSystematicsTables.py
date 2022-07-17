#!/usr/bin/env python
import timeit
import optparse
import sys  
import os
import math
import ROOT
import LatinoAnalysis.Gardener.hwwtools as hwwtools

def getMaxBinForShapeUncertainty(NbinsX, useallshapebins, cut):

    if useallshapebins or NbinsX==7 or 'SR4' in cut: return NbinsX
    elif 'SR1' in cut: return 7
    elif 'SR2' in cut or 'SR3' in cut: return 8

def getShapes(systematic, cuts, variables, samples, systSamples, inputFile):

    shapesList = [ ]

    for cut in cuts:
        if 'SR' in cut and not ('_Tag_' in cut and 'Stop' not in tag):

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
                if not samples[sample]['isSignal'] and not samples[sample]['isDATA']:
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


if __name__ == '__main__':

    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)

    parser.add_option('--inputdir'          , dest='inputdir'          , help='Input directory'                          , default='./Shapes')
    parser.add_option('--tag'               , dest='tag'               , help='Tag used for the tag file name'           , default='')
    parser.add_option('--sigset'            , dest='sigset'            , help='Sigset'                                   , default='')
    parser.add_option('--masspoints'        , dest='masspoints'        , help='Mass points'                              , default='all')
    parser.add_option('--years'             , dest='years'             , help='Year to be processed. Default: all'       , default='all')
    parser.add_option('--postFit'           , dest='postFit'           , help='Fake'                                     , default='n')
    parser.add_option('--error'             , dest='error'             , help='0 -> symmetric, 1 -> maximum'             , default=0)
    parser.add_option('--keepsplit'         , dest='keepsplit'         , help='Keep split systematic unmerged'           , default=False, action='store_true')
    parser.add_option('--useallshapebins'   , dest='useallshapebins'   , help='Use all bins, not the more significant'   , default=False, action='store_true')
    parser.add_option('--tablelevel'        , dest='tablelevel'        , help='Table level'                              , default='ptmiss')

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
    if 'SM' not in opt.sigset: opt.sigset = 'SM-' + opt.sigset

    opt.mergesplit = not opt.keepsplit

    outputDir = './Tables/'+yearset+'/'+tag+'/SM-'+opt.masspoints+'/'
    os.system('mkdir -p '+outputDir)

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

        systematics['stat'] = { }
        for centralShape in centralShapes:
            systematics['stat'][centralShape.GetName()] = { }
            centralIntegralError = ROOT.double(); centralIntegral = histo.IntegralAndError(-1, -1, centralIntegralError)
            systematics['stat'][centralShape.GetName()]['integralUncertainty'] = 100.*centralIntegralError/centralIntegral
            shapeUncertainty = 0.
            for ib in range(getMaxBinForShapeUncertainty(centralShape.GetNbinsX(), opt.useallshapebins, centralShape.GetName())):           
                shapeUncertainty = max(100.*centralShape.GetBinError(ib+1)/centralShape.GetBinContent(ib+1), shapeUncertainty)
            systematics['stat'][centralShape.GetName()]['shapeUncertainty'] = shapeUncertainty

        for nuisance in nuisances:

            if nuisance=='stat': continue

            systematic = nuisances[nuisance]['name'].replace(datayear, 'uncorrelated') 

            if systematic not in systematics:
                systematics[systematic] = { }
             
            systCuts = cuts if 'cuts' not in nuisances[nuisance] else nuisances[nuisance]['cuts']

            variation = '_'+nuisances[nuisance]['name'] if nuisances[nuisance]['type']=='shape' else 'lnN'
 
            systematicShapesUp = getShapes(variation+'Up',   systCuts, variables, samples, nuisances[nuisance]['samples'], inputFile)
            systematicShapesDo = getShapes(variation+'Down', systCuts, variables, samples, nuisances[nuisance]['samples'], inputFile)
                                        
            for cut in systCuts:

                for centralShape in centralShapes:
                    if centralShape.GetName()==cut: 
                        break

                for upShape in systematicShapesUp:
                    if upShape.GetName()==cut:
                        break

                for doShape in systematicShapesDo:
                    if doShape.GetName()==cut:
                        break

                systUp = 100.*abs(upShape.Integral() - centralShape.Integral())/centralShape.Integral()
                systDo = 100.*abs(doShape.Integral() - centralShape.Integral())/centralShape.Integral()                   
                systSm = 100.*abs(upShape.Integral() -      doShape.Integral())/centralShape.Integral()/2.

                integralUncertainty = systSm if opt.error==0 else max(systUp, systDo)

                upShape.Scale(centralShape.Integral()/upShape.Integral()); upShape.Divide(centralShape)
                doShape.Scale(centralShape.Integral()/doShape.Integral()); doShape.Divide(centralShape)
 
                shapeUncertainty = 0.        
                for ib in range(getMaxBinForShapeUncertainty(centralShape.GetNbinsX(), opt.useallshapebins, cut)):
                    shapeUncertainty = max(100.*abs(upShape.GetBinContent(ib+1) - 1.), shapeUncertainty)
                    shapeUncertainty = max(100.*abs(doShape.GetBinContent(ib+1) - 1.), shapeUncertainty) 

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
 
    systematicDictionary = { 'lumi_total'                : 'Luminosity',
                             'normVZall_uncorrelated'    : '', 
                             'qcdScale'                  : '', 
                             'normVVVall_uncorrelated'   : '',
                             'lepExtra_uncorrelated'     : '', 
                             'normSTtWall_uncorrelated'  : '', 
                             'pileup'                    : '', 
                             'lepReco_uncorrelated'      : '', 
                             'lumi_total'                : '', 
                             'normttWall_uncorrelated'   : '', 
                             'normHiggsall_uncorrelated' : '',
                             'unclustEn_uncorrelated'    : '',
                             'jesTotal_uncorrelated'     : '',
                             'jer_uncorrelated'          : '', 
                             'trigger_uncorrelated'      : 'Trigger efficiency', 
                             'toppt'                     : '', 
                             'nonpromptLep_uncorrelated' : '', 
                             'prefiring_uncorrelated'    : '', 
                             'normDYall_uncorrelated'    : '', 
                             'mistag_uncorrelated'       : '', 
                             'normttSemilepall_uncorrelated' : '', 
                             'btag_total'                : 'b tagging', 
                             'pdf',                      : '',
                             'lepIdIso_uncorrelated'     : '' 
                             'stat'                      : 'Simuated samples statistics'
                            }

    

    for systematic in systematics:
        
        systematicLegend = systematic if systematic not in systematicDictionary else systematicDictionary[systematic]








           

