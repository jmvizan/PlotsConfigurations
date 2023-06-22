#!/usr/bin/env python
import timeit
import optparse
import json
import LatinoAnalysis.Gardener.hwwtools as hwwtools
import glob 

# functions used in everyday life ...
from LatinoAnalysis.Tools.commonTools import *

expectedMinPdfWeights =  33

if __name__ == '__main__':

    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)

    parser.add_option('--sigset'  , dest='sigset'  , help='Tag used for the sigset file name'  , default='Backgrounds')
    parser.add_option('--year'    , dest='year'    , help='Year to be processed. Default: all' , default='2016')
    parser.add_option('--verbose' , dest='verbose' , help='Verbose level. Default: 0'          , default=0)

    # read default parsing options as well
    hwwtools.addOptions(parser)
    hwwtools.loadOptDefaults(parser)
    (opt, args) = parser.parse_args()

    if opt.year=='0':
        year = '2016'
    elif opt.year=='1':
        year = '2017'
    elif opt.year=='2':
        year = '2018'
    else:
        year = opt.year
    
    opt.tag = year+'TheoryNormalizations'

    samples = { }

    exec(open(opt.samplesFile).read())

    theoryNormalizations = { }

    for sam_k, sam_v in samples.iteritems():

        if not sam_v['isFastsim']: # Background samples + reference mass point samples

            expectedScaleWeights = 9

            print 'Deriving theory normalizations for sample', sam_k

            subSamples = {}

            for treeName in sam_v['name']:
                if 'rootd' not in treeName:
                    treeName = treeName.replace('###', '')
                treeName = treeName.replace('root://eoscms.cern.ch/', '')
                subSample = treeName.split('/')[-1].split('__part')[0].replace('.root','')
                subSample = subSample.replace(subSample.split('_')[0]+'_','')
                if subSample not in subSamples: subSamples[subSample] = { 'trees' : [] }
                subSamples[subSample]['trees'].append(treeName)

            for subSample in subSamples:

                if opt.verbose>=1: print ' Deriving theory normalizations for subsample', subSample

                qcdStatus = 3
                pdfStatus = 3

                chain = ROOT.TChain('Runs')
                chevt = ROOT.TChain('Events')
 
                for treeName in subSamples[subSample]['trees']:
                    chain.Add(treeName)
                    chevt.Add(treeName)

                genWeight = 0.
                qcdWeights, pdfWeights = [ ], [ ] 

                underscore = ''
                expectedPdfWeights = expectedMinPdfWeights
    	        pdfWeightWarning = False
                lastnLHEPdfSumw_ = -999

                for ev in range(chain.GetEntries()):

                    chain.GetEntry(ev)

                    if ev==0:
                        chevt.GetEntry(ev)
                        subSamples[subSample]['baseW'] = chevt.baseW

                    if hasattr(chain, 'nLHEPdfSumw_'): underscore = '_'

                    if hasattr(chain, 'nLHEPdfSumw'+underscore):
                        if ev>0 and lastnLHEPdfSumw_!=getattr(chain, 'nLHEPdfSumw'+underscore) and not pdfWeightWarning:
                            print '   Error', sam_k, subSample, 'trees have different PDF sets'
                            pdfWeightWarning = True
                        expectedPdfWeights = max(expectedPdfWeights, getattr(chain, 'nLHEPdfSumw'+underscore))
                        lastnLHEPdfSumw_ = getattr(chain, 'nLHEPdfSumw'+underscore)

                for iqcd in range(expectedScaleWeights): qcdWeights.append(0.)
                for ipdf in range(expectedPdfWeights): pdfWeights.append(0.)

                negativeErrorAlarmGiven = False

                for ev in range(chain.GetEntries()):

                    chain.GetEntry(ev)

                    if not hasattr(chain, 'genEventSumw'+underscore):
                        if opt.verbose>=2:
                            print 'Error:', sam_k, subSample, 'tree does not have gen event weight information'
                        qcdStatus = 0
                        pdfStatus = 0
                        break

                    if not hasattr(chain, 'nLHEScaleSumw'+underscore):
                        if opt.verbose>=2:
                            print 'Error:', sam_k, subSample, 'tree does not have qcd scale information'
	                qcdStatus = 0
                
                    if not hasattr(chain, 'nLHEPdfSumw'+underscore):
                        if opt.verbose>=2:     
                            print 'Error:', sam_k, subSample, 'tree does not have pdf scale information'
                        pdfStatus = 0

                    genWeight += getattr(chain, 'genEventSumw'+underscore)

                    if qcdStatus and (getattr(chain, 'nLHEScaleSumw'+underscore)==0 or getattr(chain, 'nLHEScaleSumw'+underscore)==expectedScaleWeights): 

                        if getattr(chain, 'nLHEScaleSumw'+underscore)==expectedScaleWeights:

                            LHECentralSumw = chain.LHEScaleSumw_[4] if underscore=='_' else chain.LHEScaleSumw[4]
                            if abs(LHECentralSumw-1.)>1.e-04: print 'Warning:', sam_k, 'LHEScaleSumw_[4] different from 1', LHECentralSumw                       
                     
                            for iqcd in range(getattr(chain, 'nLHEScaleSumw'+underscore)):
                                eventWeight = chain.LHEScaleSumw_[iqcd] if underscore=='_' else chain.LHEScaleSumw[iqcd]
                                qcdWeights[iqcd] += eventWeight/LHECentralSumw*getattr(chain, 'genEventSumw'+underscore)
 
                        else: 

                            if opt.verbose>=2:
                                print 'Warning:', sam_k, subSample, 'tree with nLHEScaleSumw', getattr(chain, 'nLHEScaleSumw'+underscore)
                            for iqcd in range(expectedScaleWeights):   
                                qcdWeights[iqcd] += getattr(chain, 'genEventSumw'+underscore)
  
                            qcdStatus = 1

                    else: 
                        qcdStatus = 0

	    	    if pdfStatus and (getattr(chain, 'nLHEPdfSumw'+underscore)==0 or getattr(chain, 'nLHEPdfSumw'+underscore)>=expectedMinPdfWeights):  

                        if getattr(chain, 'nLHEPdfSumw'+underscore)>=expectedMinPdfWeights:
                       
                            for ipdf in range(expectedPdfWeights):
                                if ipdf<getattr(chain, 'nLHEPdfSumw'+underscore):
                                    eventWeight = chain.LHEPdfSumw_[ipdf] if underscore=='_' else chain.LHEPdfSumw[ipdf]
                                    pdfWeights[ipdf] += eventWeight*getattr(chain, 'genEventSumw'+underscore)
                                    if eventWeight<0 and not negativeErrorAlarmGiven: 
                                        print '  Error:', sam_k, subSample, 'tree has negative pdf weights'
                                        negativeErrorAlarmGiven = True
                                        pdfStatus = 2
                                else:
                                    pdfWeights[ipdf] += getattr(chain, 'genEventSumw'+underscore) 
                                    print 'Error: this should never happen!'
                                    if pdfStatus>2: pdfStatus = 2   

                        else:

                            if opt.verbose>=2:
                               print 'Warning:', sam_k, subSample, 'tree with nLHEPdfSumw', getattr(chain, 'nLHEPdfSumw'+underscore)
                            for ipdf in range(expectedPdfWeights):
                                pdfWeights[ipdf] += getattr(chain, 'genEventSumw'+underscore)

                            pdfStatus = 1

                    else:
                        pdfStatus = 0

                subSamples[subSample]['qcdScaleStatus'] = qcdStatus
                subSamples[subSample]['pdfStatus'] = pdfStatus

                if qcdStatus:
                    for iqcd in range(len(qcdWeights)):
                        qcdWeights[iqcd] /= genWeight
                    subSamples[subSample]['qcdScale'] = qcdWeights
                elif opt.verbose>=2:
                    print 'Error: no qcd scale weights for sample', sam_k, subSample

                if pdfStatus:
                    for ipdf in range(len(pdfWeights)):
                        pdfWeights[ipdf] /= genWeight
                    subSamples[subSample]['pdf'] = pdfWeights
                elif opt.verbose>=2:
                    print 'Error: no pdf weights for sample', sam_k, subSample

            if opt.verbose>=1:
                for subSample in subSamples:
                    print subSample, subSamples[subSample]['baseW']
                    print ' qcdScaleStatus', subSamples[subSample]['qcdScaleStatus']
                    if opt.verbose>=2: print ' qcdScale      ', subSamples[subSample]['qcdScale']
                    print ' pdfStatus     ', subSamples[subSample]['pdfStatus']
                    print ' n pdf         ', len(subSamples[subSample]['pdf'])
                    if opt.verbose>=2: print ' pdf           ', subSamples[subSample]['pdf']
          
            for subSample1 in subSamples:
                for subSample2 in subSamples:
                    if subSample1!=subSample2:
                        if (abs((subSamples[subSample1]['baseW']/subSamples[subSample2]['baseW'])-1.)<1.e-04):
                            print '  Warning:', subSample1, 'and', subSample2, 'have close baseW ratio:', subSamples[subSample1]['baseW']/subSamples[subSample2]['baseW']

            theoryNormalizations[sam_k] = { }

            theoryNormalizations[sam_k]['qcdScaleStatus'], theoryNormalizations[sam_k]['pdfStatus'], nPDFs = 0., 0., 0
            for subSample in subSamples:
                theoryNormalizations[sam_k]['qcdScaleStatus'] = max(theoryNormalizations[sam_k]['qcdScaleStatus'], subSamples[subSample]['qcdScaleStatus'])
                theoryNormalizations[sam_k]['pdfStatus'] = max(theoryNormalizations[sam_k]['pdfStatus'], subSamples[subSample]['pdfStatus'])
                nPDFs = max(nPDFs, len(subSamples[subSample]['pdf']))

            if theoryNormalizations[sam_k]['qcdScaleStatus']==3:
                theoryNormalizations[sam_k]['qcdScale'] = []
                for iqcd in range(expectedScaleWeights):                                           
                    qcdScaleNormalization = '(1.'                    
                    for subSample in subSamples:
                        if subSamples[subSample]['qcdScaleStatus']==3:
                            qcdScaleNormalization += '+(abs((baseW/'+str(subSamples[subSample]['baseW'])+')-1.)<1.e-05)*('+str(subSamples[subSample]['qcdScale'][iqcd])+'-1.)'
                    theoryNormalizations[sam_k]['qcdScale'].append(qcdScaleNormalization+')')
            elif opt.verbose>=2:                                                     
                print 'Error: no qcd scale weights for sample', sam_k

            if theoryNormalizations[sam_k]['pdfStatus']==3:
                theoryNormalizations[sam_k]['pdf'] = []		
                for ipdf in range(nPDFs):
                    pdfNormalization = '(1.'
                    for subSample in subSamples:
                        if subSamples[subSample]['pdfStatus']==3 and ipdf<len(subSamples[subSample]['pdf']):
                            pdfNormalization += '+(abs((baseW/'+str(subSamples[subSample]['baseW'])+')-1.)<1.e-05)*('+str(subSamples[subSample]['pdf'][ipdf])+'-1.)'
                    theoryNormalizations[sam_k]['pdf'].append(pdfNormalization+')')
            elif opt.verbose>=2:                           
                print 'Error: no pdf weights for sample', sam_k

            if sam_v['isSignal']:
                del theoryNormalizations[sam_k]['pdfStatus']
                del theoryNormalizations[sam_k]['pdf']

        else: # Signal samples

            expectedScaleWeights = 45
            getTreesFromOriginal = True

            sam_j = sam_k.split('_')[0] + '_' + sam_k.split('_')[1].split('-')[1] + '_' + sam_k.split('_')[2].split('-')[1]

            qcdStatus = 0

            genWeight = 0.
            qcdWeights = [ ]

            for iqcd in range(expectedScaleWeights):
		qcdWeights.append(0.)

            baseTreeName = sam_v['name'][0]

            if 'rootd' not in baseTreeName:
                baseTreeName = baseTreeName.replace('###', '')
            baseTreeName = baseTreeName.replace('root://eoscms.cern.ch/', '')
            if getTreesFromOriginal:
                baseTreeNameList = baseTreeName.replace('//','/').split('/')
                datasetName = baseTreeNameList[-1].replace(baseTreeNameList[-1].split('_')[0]+'_','').split('__part')[0].replace('.root','')
                baseTreeName = baseTreeName.replace(baseTreeNameList[-2],datasetName)
                baseTreeName = baseTreeName.replace(baseTreeNameList[-3],baseTreeNameList[-3].split('_')[0]+'_*')
                baseTreeName = baseTreeName.replace(baseTreeNameList[-1],'*'+datasetName+'*.root')
            else:
                #baseTreeName = baseTreeName.split('susyGen')[0]+'susyGen/' 
                #baseTreeName += sam_v['name'][0].split('/')[-1].replace('.root','').split('_part')[0]+'*.root' 
                baseTreeName = baseTreeName.split('_part')[0].replace('.root','')+'*.root'
            treeList = glob.glob(baseTreeName)

            for treeName in treeList: #sam_v['name']:

		chain = ROOT.TChain('Runs')
                if 'rootd' not in treeName:
                    treeName = treeName.replace('###', '')
                treeName = treeName.replace('root://eoscms.cern.ch/', '')		
                chain.Add(treeName)

                for ev in range(chain.GetEntries()):

                    chain.GetEntry(ev)
                 
                    underscore = '_' if hasattr(chain, 'nLHEScaleSumw_'+sam_j) else ''

                    if hasattr(chain, 'nLHEScaleSumw'+underscore+sam_j):                        
                        if getattr(chain, 'nLHEScaleSumw'+underscore+sam_j)==expectedScaleWeights:

                            LHEScaleSumw_ = getattr(chain, 'LHEScaleSumw'+underscore+sam_j)
  
                            if not isinstance(LHEScaleSumw_, float):

                                genWeight += getattr(chain, 'genEventSumw'+underscore+sam_j)

                                for iqcd in range(expectedScaleWeights):
                                    qcdWeights[iqcd] += LHEScaleSumw_[iqcd]*getattr(chain, 'genEventSumw'+underscore+sam_j)

                                qcdStatus = 3

                            else: print 'Error: sample', sam_j, 'has float LHEScaleSumw_'

            theoryNormalizations[sam_k] = { }

            theoryNormalizations[sam_k]['qcdScaleStatus'] = qcdStatus
                                                                
            if qcdStatus:
                if opt.verbose>=1: print 'Got qcd scale weights for sample', sam_k
                theoryNormalizations[sam_k]['qcdScale'] = []
                for iqcd in range(len(qcdWeights)):  
                    qcdWeights[iqcd] /= genWeight
                    theoryNormalizations[sam_k]['qcdScale'].append(str(qcdWeights[iqcd]))
                if opt.verbose>=2:             
                    print sam_k, genWeight 
            else:
                print 'Error: no qcd scale weights for sample', sam_k 
                  
    with open('./theoryNormalizations/theoryNormalizations'+recoFlag+'_'+opt.year+'_'+opt.sigset+'.py', 'w') as file:
        if opt.sigset=='Backgrounds':
            file.write('theoryNormalizations = { }\n\n')
        for sample in theoryNormalizations:
            file.write('theoryNormalizations[\''+sample+'\'] = '+json.dumps(theoryNormalizations[sample])+'\n\n')




