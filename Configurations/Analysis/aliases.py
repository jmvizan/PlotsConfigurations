##### aliases = {}

import os

includePath = 'gSystem->AddIncludePath("-I%s/src/");' % os.getenv('CMSSW_RELEASE_BASE')
aliasDir = os.getenv('PWD')+'/aliases'

## Kinematic weights

if 'Kinematics:' in opt.tag:

    dataDir = '/'.join([ os.getenv('PWD') , 'Data', opt.campaign, 'Kinematics' ]) 

    weightFileList = os.listdir(dataDir)

    for weightFile in weightFileList:
        if opt.method+':' in weightFile and weightFile.replace(opt.method, 'Kinematics').replace('.root','') in opt.tag:

            for source in kinematicWeightsMap:

                applicationSamples = [ ]

                for sample in samples:
                    if sample in kinematicWeightsMap[source]:
                        applicationSamples.append(sample)        

                if len(applicationSamples)>0:

                    histoName  = source+'-'+weightFile.split(':')[-1].replace('.root','')
                    weightName = histoName.replace('-','')  

                    aliases[weightName] = { 'linesToAdd': [ includePath, '.L '+aliasDir+'/kinematicWeightsReader.cc+' ],
                                            'class': 'KinematicWeightsReader',
                                            'args': ( dataDir+'/'+weightFile, histoName ),
                                            'samples': applicationSamples
                                           }

                    for sample in applicationSamples:
                        samples[sample]['weight'] += '*' + weightName

