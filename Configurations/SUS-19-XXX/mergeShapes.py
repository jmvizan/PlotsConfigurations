#!/usr/bin/env python

import optparse
import json
import ROOT
import LatinoAnalysis.Gardener.hwwtools as hwwtools
import os.path

if __name__ == '__main__':

    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)

    parser.add_option('--tag'            , dest='tag'            , help='Tag used for the shape file name'           , default=None)
    parser.add_option('--years'          , dest='years'          , help='Years'                                      , default='all')
    parser.add_option('--sigset'         , dest='sigset'         , help='Signal samples [SM]'                        , default='SM')
    parser.add_option('--outputDir'      , dest='outputDir'      , help='Output directory'                           , default=None)
    parser.add_option('--skipLNN'        , dest='skipLNN'        , help='Skip lnN nuisances'                         , default=False, action='store_true')
    parser.add_option('--saveNuisances'  , dest='saveNuisances'  , help='Save file with merged nuisances'            , default=False, action='store_true')
    parser.add_option('--localNuisFile'  , dest='localNuisFile'  , help='File with local nuisances'                  , default=None)
    parser.add_option('--nuisancesFile'  , dest='nuisancesFile'  , help='File with nuisances configurations'         , default=None)
    parser.add_option('--verbose'        , dest='verbose'        , help='Activate print for debugging'               , default=False, action='store_true')
    # read default parsing options as well
    hwwtools.addOptions(parser)
    hwwtools.loadOptDefaults(parser)
    (opt, args) = parser.parse_args()

    if opt.years=='-1' or opt.years.lower()=='all':
        years = [ '2016', '2017', '2018' ]
    elif opt.years=='0':
        years = [ '2016' ]
    elif opt.years=='1':
        years = [ '2017' ]
    elif opt.years=='2':
        years = [ '2018' ]
    else:
        years = opt.years.split('-')
   
    if len(years)==1:
        print 'Nothing to do with one year (for the moment?)'
        exit()

    localnuisancesFile = opt.localNuisFile if opt.localNuisFile!=None else opt.nuisancesFile.replace('.py', '_'+'-'.join(years)+'_'+opt.tag+'_'+opt.sigset+'.py')

    localtag = opt.tag
    opt.tag = '-'.join(years) + localtag
 
    samples = {}
    if os.path.exists(opt.samplesFile) :
      handle = open(opt.samplesFile,'r')
      exec(handle)
      handle.close()

    variables = {}
    if os.path.exists(opt.variablesFile) :
      handle = open(opt.variablesFile,'r')
      exec(handle)
      handle.close()

    cuts = {}
    if os.path.exists(opt.cutsFile) :
      handle = open(opt.cutsFile,'r')
      exec(handle)
      handle.close()

    allnuisances = {}
    if os.path.exists(localnuisancesFile) :
        nuisances = {}
        handle = open(localnuisancesFile,'r')
        exec(handle)
        handle.close()
        allnuisances = nuisances
    else:
        yerstagOriginal = yearstag.copy()
        for year2merge in years:
           yearstag.clear()
           yearstag[year2merge] = yerstagOriginal[year2merge]
           nuisances = {}
           handle = open(opt.nuisancesFile,'r')
           exec(handle)
           handle.close()
           for nuisance in nuisances:
               if opt.skipLNN and 'type' in nuisances[nuisance] and nuisances[nuisance]['type']=='lnN': continue
               if nuisance!='stat': 
                   nuisanceKey = nuisance+'__'+nuisances[nuisance]['name']
                   if nuisanceKey not in allnuisances:
                       allnuisances[nuisanceKey] = nuisances[nuisance].copy()
                   else:
                       for sample in nuisances[nuisance]['samples']:
                           if sample not in allnuisances[nuisanceKey]['samples']:
                               allnuisances[nuisanceKey]['samples'][sample] = nuisances[nuisance]['samples'][sample]
                   if 'type' in nuisances[nuisance] and nuisances[nuisance]['type']=='lnN':
                       allnuisances[nuisanceKey]['samples_'+year2merge] = nuisances[nuisance]['samples']
               elif 'stat' not in allnuisances:
                   allnuisances['stat'] = nuisances[nuisance]

    outDirName = opt.outputDir if len(opt.outputDir)>9 else './Shapes/'+'-'.join(years)+'/'+localtag
    os.system ('mkdir -p ' + outDirName)

    outFileName = '/plots_' + localtag + '_' + opt.sigset + '.root'
    outFile = ROOT.TFile.Open(outDirName+outFileName, 'recreate') 

    inFiles = [ ]
    for year in years:
        inFiles.append([ ROOT.TFile('./Shapes/'+year+'/'+localtag.replace('BkgSF', '')+outFileName.replace('BkgSF', ''), 'READ') , year ])

    missingSampleList = [ ]
    if 'BkgSF' in opt.tag:
        globalScale = {
            'ZZTo4L' : { '2016HIPM' : [1.291, 0.257] , '2016noHIPM' : [0.820, 0.224], '2017' : [0.973,0.151], '2018' : [0.887, 0.121]},
            'WZ'     : { '2016HIPM' : [0.850, 0.113] , '2016noHIPM' : [0.840, 0.113], '2017' : [1.105,0.088], '2018' : [0.827, 0.063]},
            'EOYZZ4L': { '2016HIPM' : [1.291, 0.257] , '2016noHIPM' : [0.820, 0.224], '2017' : [0.973,0.151], '2018' : [0.887, 0.121]},
            'EOYVZ'  : { '2016HIPM' : [0.850, 0.113] , '2016noHIPM' : [0.840, 0.113], '2017' : [1.105,0.088], '2018' : [0.827, 0.063]},
            'ttZ'    : { '2016HIPM' : [1.179, 0.313] , '2016noHIPM' : [1.118, 0.322], '2017' : [1.553,0.223], '2018' : [1.553, 0.192]}
        }
        

    for cutName in cuts:

        outFile.mkdir(cutName)

        for variableName in variables:
            if 'cuts' not in variables[variableName] or cutName in variables[variableName]['cuts']:

                folderName = cutName + '/' + variableName
                outFile.mkdir(folderName)

                if opt.verbose: print '################################', folderName

                inDirs = [ ] 
                for infile in inFiles:
                    inDirs.append([ infile[0].Get(folderName), infile[1] ])

                globalScale = None
                for sample in samples:
                    
                    if globalScale and (sample in globalScale.keys() or sample+'EOY' in globalScale.keys()): globalScale_i = globalScale[sample] 
                    else:
                        globalScale_i = { }
                        for year in years:
                            globalScale_i[year] = [1., 0.]
                            
                    #print 'These are the global sF', globalScale_i,'for sample', sample
                    for nuisance in allnuisances:
                        if (sample in allnuisances[nuisance]['samples'] or nuisance=='stat') and ('cuts' not in allnuisances[nuisance] or cutName in allnuisances[nuisance]['cuts']):   

                            if nuisance!='stat': 
                                if 'type' not in allnuisances[nuisance]:
                                    print 'Warning: nuisance without type -> ', nuisance
                                    continue
                                if allnuisances[nuisance]['type']!='shape' and allnuisances[nuisance]['type']!='lnN':
                                    if allnuisances[nuisance]['type']!='rateParam':
                                        print 'Warning: unknown nuisance type -> ', allnuisances[nuisance]['type']
                                    continue

                            shapeName = 'histo_' + sample

                            for var in [ 'Up', 'Down' ]:

                                if nuisance=='stat' and var=='Down': continue 
                                 
                                shapeVar = shapeName if nuisance=='stat' else shapeName + '_' + allnuisances[nuisance]['name'] + var
                                  
                                for idir, indir in enumerate(inDirs):

                                    if indir[0].GetListOfKeys().Contains(shapeVar):
                                        tmpHisto = indir[0].Get(shapeVar)
                                        tmpHisto.SetDirectory(0)   
                                        if globalScale_i[indir[1]][0]!=1.: tmpHisto.Scale(globalScale_i[indir[1]][0]) #We could reformulate this line, too

                                    else:

                                        if not indir[0].GetListOfKeys().Contains(shapeName):
                                            if 'EOY' not in sample and indir[1]+'_'+sample not in missingSampleList: 
                                                print 'Warning:', sample, 'not in input shape file for', indir[1], 'year!'
                                                missingSampleList.append(indir[1]+'_'+sample)
                                            for idir2, indir2 in enumerate(inDirs):
                                                if indir2[0].GetListOfKeys().Contains(shapeName):
                                                    tmpHisto = indir2[0].Get(shapeName)
                                                    tmpHisto.SetDirectory(0)
                                                    tmpHisto.Reset()
                                        else:
                                            tmpHisto = indir[0].Get(shapeName)
                                            tmpHisto.SetDirectory(0)
                                            if globalScale_i[indir[1]][0]!=1.: tmpHisto.Scale(globalScale_i[indir[1]][0])

                                        if opt.verbose: print sample, nuisance,  var, tmpHisto.Integral()
                                        if allnuisances[nuisance]['type']=='lnN' or 'waslnN' in allnuisances[nuisance]:
                                            if 'samples_'+indir[1] in allnuisances[nuisance]:
                                                if sample in allnuisances[nuisance]['samples_'+indir[1]]:
                                                    systNorm = float(allnuisances[nuisance]['samples_'+indir[1]][sample])
                                                    if var=='Down': systNorm = 2. - systNorm
                                                    tmpHisto.Scale(systNorm)
                                                    if opt.verbose: print 'samples_'+indir[1], tmpHisto.Integral()
                                            elif indir[1] in nuisance:
                                                print 'Error: samples_'+indir[1]+' not in allnuisances['+nuisance+']'

                                    if idir==0:
                                        sumHisto = tmpHisto.Clone()
                                        sumHisto.SetDirectory(0)
                                        sumHisto.SetTitle(shapeVar)
                                        sumHisto.SetName(shapeVar)
                                    else:
                                        sumHisto.Add(tmpHisto)

                                outFile.cd(folderName)
                                sumHisto.Write()                         

                                # ...    
 
    if not os.path.exists(localnuisancesFile) and opt.saveNuisances:     
        with open(localnuisancesFile , 'w') as file:
            for nuisance in allnuisances:
                if allnuisances[nuisance]['type']=='lnN':
                    allnuisances[nuisance]['type'] = 'shape'
                    allnuisances[nuisance]['waslnN'] = True
                #file.write('nuisances[\''+nuisance+'\'] = '+json.dumps(allnuisances[nuisance])+'\n\n')
                file.write('nuisances[\''+nuisance+'\'] = '+repr(allnuisances[nuisance])+'\n\n')

