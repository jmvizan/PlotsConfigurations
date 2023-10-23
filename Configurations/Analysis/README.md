## Installation of the code

The code used is documented here:

    https://github.com/scodella/setup/blob/13TeV/SetupAnalysis.sh

To install, try this

    cmsrel CMSSW_10_6_28 # Not really the latest for Run3, but it's standalone ...
    cd CMSSW_10_6_28/src
    cmsenv
    git clone --branch 13TeV https://github.com/scodella/setup LatinosSetup
    source LatinosSetup/SetupAnalysis.sh BTagPerf

## Production of weights for kinematic reweighting

First step is the production of the raw histograms (aka shapes) for the kinematic variables:

    ./runAnalysis.py --action=shapes --year=CAMPAIGNNAME --tag=System8Kinematics/PtRelKinematics

Shapes can be merged by

    ./runAnalysis.py --action=mergesingle --year=CAMPAIGNNAME --tag=System8Kinematics/PtRelKinematics

Then wights as a function of the jet pt can be derived:

    ....

## Production of templates for PtRel/System8 fits

First step is the production of the shapes for the System8/PtRel fits:

    ./runAnalysis.py --action=makeShapes --year=CAMPAIGNNAME --tag=System8Templates/PtRelTemplates

Shapes can be merged by

    ./runAnalysis.py --action=mergeShapes --year=CAMPAIGNNAME --tag=System8Templates/PtRelTemplates

Finally, the format of the shapes need to be converted to the input format for the System8/PtRel fits (at least till the fit itself is integrated in the framework): 

    ./runAnalysis.py --action=shapesForFit --year=CAMPAIGNNAME --tag=System8Templates/PtRelTemplates # To be complete

