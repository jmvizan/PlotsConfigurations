import os
import subprocess
import math
import string
from LatinoAnalysis.Tools.commonTools import *

### Generals

opt.CME = 'XXX'
opt.lumi = 999.6999
treePrefix= 'nanoLatino_'

isDatacardOrPlot = hasattr(opt, 'outputDirDatacard') or hasattr(opt, 'postFit') or hasattr(opt, 'skipLNN') or hasattr(opt, 'inputDirMaxFit')

### Directories

skipTreesCheck = False

if not isDatacardOrPlot: 
    if skipTreesCheck:
        print 'Error: it is not allowed to fill shapes and skipping trees check!'
        exit()

SITE=os.uname()[1]
if 'cern' not in SITE and 'ifca' not in SITE and 'cloud' not in SITE: SITE = 'cern'

### Nuisance parameters

### Analysis Parameters

### Complex variables

### Weights and filters

### MC trees

# Common MC keys

for sample in samples:

    samples[sample]['isDATA']    = 0
    samples[sample]['isSignal']  = 0
    samples[sample]['isFastsim'] = 0
    samples[sample]['treeType']  = 'MC'
    samples[sample]['suppressNegative']          = ['all']
    samples[sample]['suppressNegativeNuisances'] = ['all']
    samples[sample]['suppressZeroTreeNuisances'] = ['all']

### Data

### Files per job
 
for sample in samples:
    if 'FilesPerJob' not in samples[sample]:
        ntrees = len(samples[sample]['name']) 
        multFactor = 6 if 'JobsPerSample' not in samples[sample] else int(samples[sample]['JobsPerSample'])
        samples[sample]['FilesPerJob'] = int(math.ceil(float(ntrees)/multFactor))

### Cleaning (a bit analysis dependent, but keep it for the moment)

if opt.sigset.split('-')[0] not in [ 'SM', 'MC', 'Data' ]:

    sampleToRemove = [ ]

    shortset = opt.sigset.split('-')[0]

    for sample in samples:
        if 'Veto' in shortset:
            if sample in shortset:
                sampleToRemove.append(sample)
        elif sample not in shortset: # Be sure this sample's name is not substring of other samples' names
            sampleToRemove.append(sample)

    for sample in sampleToRemove:
        del samples[sample]

### Nasty clean up for eos

if 'cern' in SITE:
    for sample in samples:
        for ifile in range(len(samples[sample]['name'])):
            samples[sample]['name'][ifile] = samples[sample]['name'][ifile].replace('root://eoscms.cern.ch/', '')

