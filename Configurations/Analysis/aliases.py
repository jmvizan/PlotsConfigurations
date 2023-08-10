##### aliases = {}

import os

includePath = 'gSystem->AddIncludePath("-I%s/src/");' % os.getenv('CMSSW_RELEASE_BASE')
aliasDir = os.getenv('PWD')+'/aliases'

## Pileup

if 'NoPU' not in opt.tag and ('SM' in opt.sigset or 'MC' in opt.sigset):

    dataDir = '/'.join([ os.getenv('PWD') , 'Data', opt.campaign, 'Pileup' ])

    aliases['pileupWeight'] = { 'linesToAdd': [ includePath, '.L '+aliasDir+'/pileupWeightsReader.cc+' ],
                                'class': 'PileupWeightsReader',
                                'args': ( dataDir+'/pileupWeights_'+campaignRunPeriod['period']+'.root' ),
                                'samples': []
                               }

    for sample in samples:
        if not samples[sample]['isDATA']:
            aliases['pileupWeight']['samples'].append(sample)
            samples[sample]['weight'] += '*pileupWeight[1]'  

## Trigger prescales

if 'NoPS' not in opt.tag and ('SM' in opt.sigset or 'Data' in opt.sigset):

    dataDir = '/'.join([ os.getenv('PWD') , 'Data', opt.campaign, 'Prescales' ])

    for trigger in triggerInfos:

        hltPath = trigger if 'Light' not in opt.tag else triggerInfos[trigger]['jetTrigger']
        prescaleWeight = 'prescale_'+hltPath

        if prescaleWeight not in aliases:

            aliases[prescaleWeight] = { 'linesToAdd': [ includePath, '.L '+aliasDir+'/triggerPrescalesReader.cc+' ],
                                        'class': 'PrescalesWeightsReader',
                                        'args': ( dataDir+'/Prescales_'+campaignRunPeriod['period']+'_'+hltPath+'.csv' ),
                                        'samples': []
                                       }

            for sample in samples:
                if samples[sample]['isDATA']:
                    aliases[prescaleWeight]['samples'].append(sample)

## b fragmentation aliases/bFragmentationWeightsReader.cc

if 'bjets' in samples:

    dataDir = '/'.join([ os.getenv('PWD') , 'Data', 'BFragmentationWeights' ]) # This might need to be updated

    aliases['bHadronWeight'] = { 'linesToAdd': [ includePath, '.L '+aliasDir+'/bFragmentationWeightsReader.cc+' ],
                                 'class': 'BFragmentationWeightsReader',
                                 'args': ( dataDir+'/bfragweights_vs_pt.root', 'fragCP5BL', dataDir+'bdecayweights.root' ),
                                 'samples': [ 'bjets' ]
                                }

    if 'NoBFrag' not in opt.tag: samples['bjets']['weight'] += '*bHadronWeight[1]'

## Inclusive track associator

if 'Light' in opt.tag:

  aliases['TrkInc_jetIdx'] = { 'linesToAdd': [ includePath, '.L '+aliasDir+'/inclusiveTrackAssociator.cc+' ],
                               'class': 'InclusiveTrackAssociator',
                               'args': ( 5., 999. ),
                               'samples': samples.keys()
                              }

## Kinematic weights

if ':' in opt.tag:

    dataDir = '/'.join([ os.getenv('PWD') , 'Data', opt.campaign, 'Kinematics' ]) 

    weightFileList = os.listdir(dataDir)

    for source in kinematicWeightsMap:

        applicationSamples = [ ]

        for sample in samples:
            if sample in kinematicWeightsMap[source]:
                applicationSamples.append(sample)

        if len(applicationSamples)>0:

            for weightFile in weightFileList:
                if opt.method+'_'+source+':' in weightFile and weightFile.replace(opt.method+'_'+source+':','').replace('.root','') in opt.tag:

                    weightName = weightFile.split(':')[-1].replace('.root','') # so far we cannot fill shapes for more than one source in a job!!!
                    aliases[weightName] = { 'linesToAdd': [ includePath, '.L '+aliasDir+'/kinematicWeightsReader.cc+' ],
                                            'class': 'KinematicWeightsReader',
                                            'args': ( dataDir+'/'+weightFile, weightName ),
                                            'samples': applicationSamples
                                           }


