#!/usr/bin/env python
import timeit
import optparse
import json
import LatinoAnalysis.Gardener.hwwtools as hwwtools

# functions used in everyday life ...
from LatinoAnalysis.Tools.commonTools import *

expectedScaleWeights  =   9
expectedMinPdfWeights = 100

if __name__ == '__main__':

    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)

    parser.add_option('--sigset' , dest='sigset' , help='Tag used for the sigset file name'  , default='Backgrounds')
    parser.add_option('--year'   , dest='year'   , help='Year to be processed. Default: all' , default='2016')

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
    
    opt.tag = year

    samples = { }

    exec(open(opt.samplesFile).read())

    TheoryNormalizations = { }
             
    for sam_k, sam_v in samples.iteritems():
    
        if not sam_v['isSignal']:

            qcdStatus = 3
            pdfStatus = 3

            chain = ROOT.TChain('Runs')

            for treeName in sam_v['name']:
                chain.Add(treeName)
                     
            genWeight = 0.
            qcdWeights, pdfWeights = [ ], [ ] 

            expectedPdfWeights = expectedMinPdfWeights
	    pdfWeightWarning = False
            lastnLHEPdfSumw_ = -999
            for ev in range(chain.GetEntries()):
                chain.GetEntry(ev)
                if ev>0 and lastnLHEPdfSumw_!=chain.nLHEPdfSumw_ and not pdfWeightWarning:
                    print 'Warning', sam_k, 'trees have different PDF sets'
                    pdfWeightWarning = True
                expectedPdfWeights = max(expectedPdfWeights, chain.nLHEPdfSumw_)
                lastnLHEPdfSumw_ = chain.nLHEPdfSumw_

            for ev in range(chain.GetEntries()):

                chain.GetEntry(ev)

                genWeight += chain.genEventSumw_

                LHECentralSumw = -1.

                if chain.nLHEScaleSumw_==0 or chain.nLHEScaleSumw_==expectedScaleWeights: 

                    if ev==0:
                        for iqcd in range(expectedScaleWeights):
                            qcdWeights.append(0.)

                    if chain.nLHEScaleSumw_==expectedScaleWeights:

                        LHECentralSumw = chain.LHEScaleSumw_[4]

                        for iqcd in range(chain.nLHEScaleSumw_):
                            qcdWeights[iqcd] += chain.LHEScaleSumw_[iqcd]/LHECentralSumw*chain.genEventSumw_
 
                    else: 

                        for iqcd in range(expectedScaleWeights):                                                                                                   qcdWeights[iqcd] += chain.genEventSumw_
 
                        qcdStatus = 1

                else: 
                    qcdStatus = 0
                    break
                
                if chain.nLHEPdfSumw_==0 or chain.nLHEPdfSumw_>=expectedMinPdfWeights:  
                                                
                    if ev==0: 
                        for ipdf in range(expectedPdfWeights):
                            pdfWeights.append(0.)

                    if chain.nLHEPdfSumw_>=expectedMinPdfWeights:
                        
                        for ipdf in range(expectedPdfWeights):
                            if ipdf<chain.nLHEPdfSumw_:
                                pdfWeights[ipdf] += chain.LHEPdfSumw_[ipdf]/LHECentralSumw*chain.genEventSumw_
                            else:
                                pdfWeights[ipdf] += chain.genEventSumw_
                                pdfStatus = 2
                    else:

                        for ipdf in range(expectedPdfWeights):
                            pdfWeights[ipdf] += chain.genEventSumw_

                        pdfStatus = 1

                else:
                    pdfStatus = 0
                    break

            theoryNormalizations[sam_k] = { }

            theoryNormalizations[sam_k]['qcdScaleStatus'] = qcdStatus
            theoryNormalizations[sam_k]['pdfStatus'] = pdfStatus

            if qcdStatus:
                for iqcd in range(len(qcdWeights)):                                                                                                        qcdWeights[iqcd] /= genWeight
                theoryNormalizations[sam_k]['qcdScale'] = qcdWeights   

            if pdfStatus:		
                for ipdf in range(len(pdfWeights)):
                    pdfWeights[ipdf] /= genWeight
                theoryNormalizations[sam_k]['pdf'] = pdfWeights
            
    with open('./theoryNormalizations_'+opt.sigset+'.py', 'w') as file:
        file.write('theoryNormalizations = { }\n\n')
        for sample in theoryNormalizations:
            file.write('theoryNormalizations[\''+sample+'\'] = '+json.dumps(theoryNormalizations[sample])+'\n\n')




