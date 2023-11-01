## Installation of the code

The code used is documented here:

    https://github.com/scodella/setup/blob/13TeV/SetupAnalysis.sh

To install, try this

    cmsrel CMSSW_10_6_28 # Not really the latest for Run3, but it's standalone ...
    cd CMSSW_10_6_28/src
    cmsenv
    git clone --branch 13TeV https://github.com/scodella/setup LatinosSetup
    ./LatinosSetup/SetupAnalysis.sh BTagPerf

Copy the file LatinoAnalysis/Tools/python/userConfig_TEMPLATE.py to LatinoAnalysis/Tools/python/userConfig.py and edit it to reflect your local paths. This is needed for batch jobs submission.

Copy the file /afs/cern.ch/work/s/scodella/public/BTagging/Run3/FunctionLibrary.h in LatinoAnalysis/MultiDraw/interface/

Compile all from CMSSW_10_6_28/src.

## Production of weights for kinematic reweighting

The scripts to derive the scale factors are in PlotsConfigurations/Configurations/Analysis. 
The first step is the production of the raw histograms (aka shapes) for the kinematic variables:

    ./runAnalysis.py --action=shapes --year=CAMPAIGNNAME --tag=System8Kinematics/PtRelKinematics

Shapes can be merged by

    ./runAnalysis.py --action=mergesingle --year=CAMPAIGNNAME --tag=System8Kinematics/PtRelKinematics

Then weights as a function of the jet pt can be derived:

    ./runAnalysis.py --action=kinematicWeights --year=CAMPAIGNNAME --tag=System8Kinematics/PtRelKinematics --option=mujetpt

Now, we can produce the shapes with the weights applied ...

    ./runAnalysis.py --action=shapes --year=CAMPAIGNNAME --tag=System8Kinematics.mujetpt/PtRelKinematics.mujetpt --sigset=MC
    ./runAnalysis.py --action=mergesingle --year=CAMPAIGNNAME --tag=System8Kinematics.mujetpt/PtRelKinematics.mujetpt --sigset=MC

... and make some validation plot:

    ./runAnalysis.py --action=plotKinematics --year=CAMPAIGNNAME --tag=System8Kinematics.mujetpt/PtRelKinematics.mujetpt

Finally, we can compute weights as a function of the jet eta on top of the one as a function of the jet pt ...

    ./runAnalysis.py --action=kinematicWeights --year=CAMPAIGNNAME --tag=System8Kinematics.mujetpt/PtRelKinematics.mujetpt --option=mujeteta

... and try their effect:

    ./runAnalysis.py --action=shapes --year=CAMPAIGNNAME --tag=System8Kinematics.mujetpt.mujeteta/PtRelKinematics.mujetpt.mujeteta --sigset=MC
    ./runAnalysis.py --action=mergesingle --year=CAMPAIGNNAME --tag=System8Kinematics.mujetpt.mujeteta/PtRelKinematics.mujetpt.mujeteta --sigset=MC
    ./runAnalysis.py --action=plotKinematics --year=CAMPAIGNNAME --tag=System8Kinematics.mujetpt.mujeteta/PtRelKinematics.mujetpt.mujeteta

## Production of templates for PtRel/System8 fits

First step is the production of the shapes for the System8/PtRel fits:

    ./runAnalysis.py --action=makeShapes --year=CAMPAIGNNAME --tag=System8Templates.mujetpt.mujeteta/PtRelTemplates.mujetpt.mujeteta

Shapes can be merged by

    ./runAnalysis.py --action=mergeShapes --year=CAMPAIGNNAME --tag=System8Templates.mujetpt.mujeteta/PtRelTemplates.mujetpt.mujeteta

Finally, the format of the shapes need to be converted to the input format for the System8/PtRel fits (at least till the fit itself is integrated in the framework): 

    ./runAnalysis.py --action=shapesForFit --year=CAMPAIGNNAME --tag=System8Templates.mujetpt.mujeteta/PtRelTemplates.mujetpt.mujeteta # To be complete
