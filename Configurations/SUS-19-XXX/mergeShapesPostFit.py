#!/usr/bin/env python

import optparse
import json
import ROOT
import LatinoAnalysis.Gardener.hwwtools as hwwtools
import os.path
import math

def warnMissingShape(shapeName):
    print 'Warning: missing', shapeName, 'shape'

def fillShape(inputShape, shapeName, fitvariable):

    binEdges = fitvariable['range'][0]
    outputShape = ROOT.TH1F(shapeName, shapeName, len(binEdges)-1, array('d',binEdges))
    outputShape.SetXTitle(fitvariable['xaxis'])
    
    if not inputShape:

        if opt.verbose:
            warnMissingShape(shapeName)

    elif inputShape.ClassName()=='TH1F':

        for xb in range(len(binEdges)):
	    outputShape.SetBinContent(xb+1, inputShape.GetBinContent(xb+1))
            outputShape.SetBinError(xb+1, inputShape.GetBinError(xb+1))  

    elif inputShape.ClassName()=='TGraphAsymmErrors':

        for ipoint in range(0, inputShape.GetN()):
            outputShape.SetBinContent(int(inputShape.GetX()[ipoint])+1, inputShape.GetY()[ipoint])
            outputShape.SetBinError(int(inputShape.GetX()[ipoint])+1, inputShape.GetErrorY(ipoint))

    else: 
	print 'fillShape: invalide inputShape class:', inputShape.ClassName()  

    return outputShape

if __name__ == '__main__':

    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)

    parser.add_option('--inputDir'     , dest='inputDir'     , help='inputDir'                         , default='./MaxLikelihoodFits' , type='string')
    parser.add_option('--tag'          , dest='tag'          , help='Tag used for the shape file name' , default=None)
    parser.add_option('--years'        , dest='years'        , help='Years'                            , default='-1')
    parser.add_option('--inputFile'    , dest='inputFile'    , help='inputFile'                        , default='fitDiagnostics'      , type='string')
    parser.add_option('--masspoint'    , dest='masspoint'    , help='Signal mass point'                , default='')
    parser.add_option('--outputDir'    , dest='outputDir'    , help='output directory'                 , default='./Shapes')
    parser.add_option('--postFit'      , dest='postFit'      , help='post-fit distribution'            , default='PostFit')
    parser.add_option('--prefitSignal' , dest='prefitSignal' , help='get the prefit signal'            , default=False, action='store_true')
    parser.add_option('--verbose'      , dest='verbose'      , help='activate print for debugging'     , default=False, action='store_true')

    # read default parsing options as well
    hwwtools.addOptions(parser)
    hwwtools.loadOptDefaults(parser)
    (opt, args) = parser.parse_args()
 
    if opt.masspoint=='':
        print 'Error: please, choose a signal mass point'
        exit()

    opt.masspoint = opt.masspoint.replace('SM-', '')

    if opt.postFit!='PreFit' and opt.postFit!='PostFit' and opt.postFit!='PostFitS':
        print 'Error:', opt.postFit, ' wrong post-fit distribution. Please, use PreFit, PostFit or PostFitS'

    if opt.years=='-1' or opt.years.lower()=='all':
        years = '2016-2017-2018'
    elif opt.years=='0':
        years = '2016'
    elif opt.years=='1':
        years = '2017'
    elif opt.years=='2':
        years = '2018'
    else:
        years = opt.years

    prefitSignal = opt.prefitSignal or opt.postFit=='PostFit'

    tag = opt.tag
    opt.tag = years + opt.tag

    opt.sigset = 'SM-' + opt.masspoint

    samples = { }
    cuts = { }
    variables = { }

    exec(open(opt.samplesFile).read())
    exec(open(opt.cutsFile).read())
    exec(open(opt.variablesFile).read())

    shapes = { }
    shapes['cuts'] = { }
    shapes['overall'] = { }

    fitkindToOpt = { '_prefit' : 'PreFit' , '_postfit_b' : 'PostFit' , '_postfit_s' : 'PostFitS' }

    inputFile = ROOT.TFile.Open(opt.inputDir + '/' + years + '/' + tag + '/' + opt.masspoint + '/' + opt.inputFile + tag + '.root', 'read')

    for key in inputFile.GetListOfKeys():
        if key.ReadObj().ClassName()=='TDirectoryFile' and 'shapes_' in key.ReadObj().GetName():

            fitdir = key.ReadObj().GetName()
            fitkind = fitdir.replace('shapes', '').replace('_fit', '_postfit')

            for keycut in inputFile.Get(fitdir).GetListOfKeys():
                if keycut.ReadObj().ClassName()=='TDirectoryFile':
                   
                    cut = keycut.ReadObj().GetName()
                    if cut not in shapes['cuts']:
                        shapes['cuts'][cut] = { }

                    # Here we are assuming one variable for cut!
                    for variable in variables:
                        if 'cuts' not in variables[variable] or cut.replace('_'+cut.split('_')[-1], '') in variables[variable]['cuts']:
                            fitvariable = variables[variable]  
                 
                    if fitvariable==None:
                        print 'mergeShapesPostFit: fit variable not found for cut', cut
                        exit()
 
                    for sample in samples:

                        if 'SR' in cut and 'isControlSample' in samples[sample] and samples[sample]['isControlSample']==1: continue
                        if 'CR' in cut and samples[sample]['isSignal']==1: continue
                        if samples[sample]['isSignal']==1 and prefitSignal and fitkind!='_prefit': continue
                        if samples[sample]['isSignal']==1 and not prefitSignal and opt.postFit!=fitkindToOpt[fitkind]: continue
                        if samples[sample]['isSignal']==0 and opt.postFit!=fitkindToOpt[fitkind]: continue    
            
                        shapeName = 'data' if samples[sample]['isDATA'] else sample
                        inputShape = inputFile.Get(fitdir+'/'+cut+'/'+shapeName)
                        shapes['cuts'][cut][sample] = fillShape(inputShape, 'histo_'+shapeName.replace('data', 'DATA'), fitvariable)

                    for shapeName in [ 'total_background', 'total', 'total_signal' ]:
                        
                        outputShapeName = shapeName if opt.postFit==fitkindToOpt[fitkind] else shapeName+fitkind          
                        inputShape = inputFile.Get(fitdir+'/'+cut+'/'+shapeName)
                        if inputShape:
                            shapes['cuts'][cut][shapeName+fitkind] = fillShape(inputShape, 'histo_'+outputShapeName, fitvariable)
                        elif opt.verbose:
                            warnMissingShape(fitdir+'/'+cut+'/'+shapeName)                        

            for shapeName in [ 'total_overall', 'total_signal', 'total_background', 'total_data', 'overall_total_covar' ]:
                
                outputShapeName = shapeName if opt.postFit==fitkindToOpt[fitkind] else shapeName+fitkind
                inputShape = inputFile.Get(fitdir+'/'+shapeName)
                if inputShape:
                    inputShape.SetName('histo_'+outputShapeName)
                    inputShape.SetTitle('histo_'+outputShapeName)
                    shapes['overall'][shapeName+fitkind] = inputShape
                elif opt.verbose:
                    warnMissingShape(fitdir+'/'+shapeName)
                
    if '-' in years and 'PostFit' in opt.postFit: # Use mergeShapes to merge prefit shapes across the years
   
        cutList = [ ]
        for cut in shapes['cuts'].keys():
            if years.split('-')[0] in cut:
                cutList.append(cut.replace('_'+years.split('-')[0], ''))

        for cut in cutList:
            shapeList = [ ]
            for shape in shapes['cuts'][cut+'_'+years.split('-')[0]].keys(): shapeList.append(shape)

            shapes['cuts'][cut] = { } 
            for shape in shapeList:

                for year in years.split('-'):
                    if shape in shapes['cuts'][cut+'_'+year]:
                        if shape not in shapes['cuts'][cut]: shapes['cuts'][cut][shape] = shapes['cuts'][cut+'_'+year][shape]
                        else:
                            shapes['cuts'][cut][shape].Add(shapes['cuts'][cut+'_'+year][shape])

                if shape=='histo_total' or (shape=='histo_total_background' and opt.postFit=='PostFit'):
                    for ibin in range(1, shapes['cuts'][cut][shape].GetNbinsX()+1):
                        binSquaredError = 0.
                        for yearx in years.split('-'):
                            errorX = shapes['cuts'][cut+'_'+yearx][shape].GetBinError(ibin)
                            binCovX = shapes['overall']['overall_total_covar'].GetXaxis().FindBin(cut+'_'+yearx+'_'+str(ibin-1))
                            for yeary in years.split('-'):
                                errorY = shapes['cuts'][cut+'_'+yeary][shape].GetBinError(ibin) 
                                binCovY = shapes['overall']['overall_total_covar'].GetYaxis().FindBin(cut+'_'+yeary+'_'+str(ibin-1))
                                covariance = shapes['overall']['overall_total_covar'].GetBinContent(binCovX, binCovY)
                                binSquaredError += errorX*errorY*covariance
                        shapes['cuts'][cut][shape].SetBinError(math.sqrt(binSquaredError)) 
 
                elif shape=='histo_DATA':
                    pass # check if something is needed here


    outputDir = opt.outputDir + '/' + years + '/' + tag + '/'
    os.system('mkdir -p ' + outputDir)
    outputFile = ROOT.TFile.Open(outputDir + 'plots_' + opt.postFit + tag + '_SM-' + opt.masspoint + '.root', 'recreate')
    print "OutputFile:", outputDir + 'plots_' + opt.postFit + tag + '_SM-' + opt.masspoint + '.root'

    for shapeName in [ 'total_overall', 'total_signal', 'total_background', 'total_data', 'overall_total_covar' ]:
        for fitkind in fitkindToOpt:
            if shapeName+fitkind in shapes['overall']:
                shapes['overall'][shapeName+fitkind].Write()

    for cut in shapes['cuts']:

        cutName = cut.replace('_'+years, '')  

        outputFile.mkdir(cutName)
        outputFile.mkdir(cutName+'/'+fitvariable['name'])
        
        outputFile.cd(cutName+'/'+fitvariable['name'])

        for sample in samples:
            if sample in shapes['cuts'][cut]:
                shapes['cuts'][cut][sample].Write()
            elif opt.verbose:
                 warnMissingShape('saving '+cutName+'/'+shapeName)

        for shapeName in [ 'total_background', 'total', 'total_signal' ]:
            for fitkind in fitkindToOpt:
                if shapeName+fitkind in shapes['cuts'][cut]:
                    shapes['cuts'][cut][shapeName+fitkind].Write()

