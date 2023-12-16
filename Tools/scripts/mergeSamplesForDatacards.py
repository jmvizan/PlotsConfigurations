#!/usr/bin/env python
import optparse
import json
import os
import ROOT
import copy
import LatinoAnalysis.Gardener.hwwtools as hwwtools

if __name__ == '__main__':

    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)

    parser.add_option('--inputDir'       , dest='inputDir'       , help='Input directory'                    , default='./Shapes')
    parser.add_option('--tag'            , dest='tag'            , help='Tag used for the input file name'   , default=None)
    parser.add_option('--outputtag'      , dest='outputtag'      , help='Tag used for the output file name'  , default=None)
    parser.add_option('--year'           , dest='year'           , help='Year'                               , default='all')
    parser.add_option('--groups'         , dest='groups'         , help='Group dictionary'                   , default={})
    parser.add_option('--sigset'         , dest='sigset'         , help='Signal samples [SM]'                , default='SM')
    parser.add_option('--outputShapeDir' , dest='outputShapeDir' , help='Output directory'                   , default=None)
    parser.add_option('--nuisancesFile'  , dest='nuisancesFile'  , help='File with nuisances configurations' , default=None )
    parser.add_option('--verbose'        , dest='verbose'        , help='Activate print for debugging'       , default=False, action='store_true')
    # read default parsing options as well
    hwwtools.addOptions(parser)
    hwwtools.loadOptDefaults(parser)
    (opt, args) = parser.parse_args()

    tag = opt.tag

    opt.tag = opt.year + tag

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

    nuisances = {}
    if os.path.exists(opt.nuisancesFile) :
        handle = open(opt.nuisancesFile,'r')
        exec(handle)
        handle.close()

    outDirName = opt.outputShapeDir if opt.outputShapeDir!=None else '/'.join([ opt.inputDir, opt.year, opt.outputtag ])
    os.system ('mkdir -p ' + outDirName)

    outFileName = '_'.join([ '/plots', opt.outputtag , opt.sigset+'.root' ])
    outFile = ROOT.TFile.Open(outDirName+outFileName, 'recreate') 

    inputFileName = '/'.join([ opt.inputDir, opt.year, tag ])+outFileName.replace(opt.outputtag, tag)
    if not os.path.isfile(inputFileName): 
        print('Error in mergeDataTakingPeriodShapes: input file', inputFileName, 'not found') 
        exit()
    inputFile = ROOT.TFile(inputFileName, 'READ')

    missingSampleList = [ ] 

    groups = {}
    for grp in opt.groups.split('-'):
        group = grp.split(':')[0]
        groups[group] = grp.split(':')[1].split(',')
 
    for sample in samples:
        sampleToGroup = False
        for group in groups:
            if sample in groups[group]:
                sampleToGroup = True
        if not sampleToGroup:
            groups[sample] = [ sample ]

    for cutName in cuts:

        outFile.mkdir(cutName)
        for variableName in variables:
            if 'cuts' not in variables[variableName] or cutName in variables[variableName]['cuts']:

                folderName = cutName + '/' + variableName
                outFile.mkdir(folderName)

                if opt.verbose: print('################################', folderName)

                inDir = inputFile.Get(folderName)

                for group in groups:

                    for nuisance in nuisances:                        
                        if 'cuts' in nuisances[nuisance] and cutName not in nuisances[nuisance]['cuts']: continue

                        if nuisance!='stat':
                            if 'type' not in nuisances[nuisance]:
                                print('Warning: nuisance without type -> ', nuisance)
                                continue
                            if nuisances[nuisance]['type']=='lnN': continue
                            if nuisances[nuisance]['type']=='rateParam': continue
                            if nuisances[nuisance]['type']!='shape':
                                print('Warning: unknown nuisance type -> ', nuisances[nuisance]['type'])
                                continue

                        nuisanceInGroup = False 
                        for sample in groups[group]:
                            if sample in nuisances[nuisance]['samples'] or nuisance=='stat':                        
                                nuisanceInGroup = True
 
                        if nuisanceInGroup:
                            for var in [ 'Up', 'Down' ]:

                                if nuisance=='stat' and var=='Down': continue

                                skipGroup = False
                                shapeGroup = 'histo_'+group if nuisance=='stat' else 'histo_'+group+'_'+nuisances[nuisance]['name']+var

                                for isample, sample in enumerate(groups[group]):

                                    skipHisto = False
                                    shapeName = 'histo_' + sample
                                    shapeVar = shapeName if nuisance=='stat' else shapeName + '_' + nuisances[nuisance]['name'] + var
                                 
                                    if inDir.GetListOfKeys().Contains(shapeVar):
                                        tmpHisto = inDir.Get(shapeVar)
                                        tmpHisto.SetDirectory(0)   

                                    else:

                                        if sample in nuisances[nuisance]['samples'] or nuisance=='stat':
                                            print('Warning: nuisance', nuisance, 'for sample', sample, 'not in input shape file for', cutName)

                                        if inDir.GetListOfKeys().Contains(shapeName):
                                            tmpHisto = inDir.Get(shapeName)
                                            tmpHisto.SetDirectory(0)

                                        else:
                                            if sample not in missingSampleList:
                                                print('Warning:', sample, 'not in input shape file for', cutName, 'in', opt.year, 'year!')
                                                missingSampleList.append(sample)
                                            skipHisto = True
                                            skipGroup = True

                                    if not skipHisto:
                                        if isample==0:
                                            sumHisto = tmpHisto.Clone()
                                            sumHisto.SetDirectory(0)
                                            sumHisto.SetTitle(shapeVar)
                                            sumHisto.SetName(shapeVar)
                                        else:
                                            sumHisto.Add(tmpHisto)

                                if not skipGroup: 
                                    outFile.cd(folderName)
                                    sumHisto.SetTitle(shapeGroup)
                                    sumHisto.SetName(shapeGroup)
                                    sumHisto.Write()                         
 
 
    
