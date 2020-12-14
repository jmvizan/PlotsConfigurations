#!/usr/bin/env python
import timeit
import optparse
import sys  
import os
import LatinoAnalysis.Gardener.hwwtools as hwwtools

def _getSampleYields(sample, shape):

    sampleYields = ''
    maxYields = 0.
    for ibin in range(1, shape.GetNbinsX()+1):
        yields = shape.GetBinContent(ibin)
        error = shape.GetBinError(ibin)  
        if yields>=maxYields:
            maxYields = yields 
        if yields>=100.:
            yieldsString = '%.0f' % yields
            errorString = '%.0f' % error
        elif yields>=1.:
            yieldsString = '%.1f' % yields
            errorString = '%.1f' % error
        else:
            yieldsString = '%.2f' % yields
            errorString = '%.2f' % error    
        sampleYields += ' & $' + yieldsString + '\\pm ' + errorString +'$'

    return sampleYields, maxYields

if __name__ == '__main__':

    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)

    parser.add_option('--inputDirMaxFit'    , dest='inputDirMaxFit'    , help='intput directory from fit '               , default='MaxLikelihoodFits')
    parser.add_option('--tag'               , dest='tag'               , help='Tag used for the tag file name'           , default='')
    parser.add_option('--masspoints'        , dest='masspoints'        , help='Mass points'                              , default='referenceMassPoints')
    parser.add_option('--years'             , dest='years'             , help='Year to be processed. Default: all'       , default='all')
    parser.add_option('--fit'               , dest='fit'               , help='Fit level'                                , default='prefit')
    parser.add_option('--unblind'           , dest='unblind'           , help='Unblind data'                             , default=False, action='store_true') 		
    parser.add_option('--nosignal'          , dest='nosignal'          , help='Do not write signal yields'               , default=False, action='store_true')
    parser.add_option('--maxsignallines'    , dest='maxsignallines'    , help='Maximum number of lines for signals'      , default=5)

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
    opt.tag = yearset.split('-')[0] + tag

    massPointOutput = opt.masspoints

    if opt.masspoints=='referenceMassPoints':
        opt.masspoints = 'TChipmSlepSnu_mC-200_mX-125,TChipmSlepSnu_mC-450_mX-300,TChipmSlepSnu_mC-700_mX-425,TChipmSlepSnu_mC-1000_mX-400,TChipmSlepSnu_mC-1175_mX-1'

    opt.sigset = 'SM-' + opt.masspoints

    samples = { }
    variables = { }
    cuts = { }
    plot = { } 
    groupPlot = { }
    legend = { }

    exec(open(opt.samplesFile).read())
    exec(open(opt.variablesFile).read())
    exec(open(opt.cutsFile).read())
    exec(open(opt.plotFile).read())

    samples['total_background'] = { 'isData' : 0, 'isSignal' : 0 }
    plot['total_background'] = { 'isData' : 0, 'isSignal' : 0, 'nameHR' : 'SM Processes' } 

    outputDir = './Tables/'+yearset+'/'+tag+'/'+massPointOutput+'/'
    os.system('mkdir -p '+outputDir)

    inputFiles = { }  

    for masspoint in opt.masspoints.split(','):
        inputFiles[masspoint] = ROOT.TFile(opt.inputDirMaxFit+'/'+yearset+'/'+tag+'/'+masspoint+'/fitDiagnostics'+tag+'.root', 'READ')
                   
    refmasspoint = opt.masspoints.split(',')[0]

    for fittype in opt.fit.split('-'):
        for year in yearset.split('-'):
            for cut in cuts:
                if 'SR' in cut:
       
                    tableName = outputDir+fittype+'_'+cut+'_'+year+'.tex'
                    table = open(tableName , 'w')

                    for variable in variables:
                        nbins = len(variables[variable]['range'][0])-1

                    #table.write('\\begin{center}\n')
                    table.write('\\begin{tabular}{l')
                    for ibin in range(nbins): table.write('c')
                    table.write('}\n')

                    table.write('\\hline\n')
                
                    table.write('\\mtll bin')

                    for variable in variables:
                        for ibin in range(nbins-1):
                            table.write(' & '+str(variables[variable]['range'][0][ibin])+'-'+str(variables[variable]['range'][0][ibin+1]))
                        table.write(' & $\\ge '+str(variables[variable]['range'][0][nbins-1])+'$')

                    table.write(' \\\\\n')
                   
                    inDir = 'shapes_'+fittype+'/'+cut+'_'+year+'/'
                                  
                    signalPoint = [ ]
                    signalYields = { }
                    signalMaximum = { }

                    for iteration in range(4):
                        if (iteration!=2 or opt.unblind) and (iteration!=3 or not opt.nosignal): table.write('\\hline\n')
                        for sample in plot.keys():

                            if iteration==0 and (plot[sample]['isData'] or plot[sample]['isSignal'] or sample=='total_background'): continue
                            if iteration==1 and sample!='total_background': continue
                            if iteration==2 and (not plot[sample]['isData'] or not opt.unblind): continue 
                            if iteration==3 and (not plot[sample]['isSignal'] or opt.nosignal): continue
                            if 'isControlSample' in samples[sample] and samples[sample]['isControlSample']: continue 

                            sampleName = 'data' if plot[sample]['isData'] else sample
                            if plot[sample]['isSignal']:
                                shape = inputFiles[sample].Get(inDir+sample)
                            else:
                                shape = inputFiles[refmasspoint].Get(inDir+sample)

                            if shape:
                                sampleName = plot[sample]['nameLatex'] if 'nameLatex' in plot[sample] else plot[sample]['nameHR']
                                sampleYields, maxYields = _getSampleYields(sample, shape)
                                if iteration!=3:
                                    table.write(sampleName+sampleYields+' \\\\\n')
                                elif maxYields>0.6:
                                    signalPoint.append(sampleName)
                                    signalYields[sampleName] = sampleYields             
                                    signalMaximum[sampleName] = maxYields

                    for s1 in range(len(signalPoint)):
                        for s2 in range(s1+1, len(signalPoint)):
                            if signalMaximum[signalPoint[s2]]>signalMaximum[signalPoint[s1]]:
                                saveSignalName = signalPoint[s1]
                                signalPoint[s1] = signalPoint[s2]
                                signalPoint[s2] = saveSignalName

                    for siter in range(len(signalPoint)):
                        if siter<opt.maxsignallines:
                            table.write(signalPoint[siter]+signalYields[signalPoint[siter]]+' \\\\\n')

                    table.write('\\hline\n')

                    table.write('\\end{tabular}\n')
                    #table.write('\\end{center}\n') 
 
