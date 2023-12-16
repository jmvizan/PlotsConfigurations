## Installation of the code

The code used is documented here:

    https://github.com/scodella/setup/blob/13.6TeV/SetupAnalysis.sh

To install, try this

    setenv SCRAM_ARCH el9_amd64_gcc12
    cmsrel CMSSW_13_3_1
    cd CMSSW_13_3_1/src
    cmsenv
    git clone --branch 13.6TeV https://github.com/scodella/setup LatinosSetup
    ./LatinosSetup/SetupAnalysis.sh BTagPerf

Copy the file LatinoAnalysis/Tools/python/userConfig_TEMPLATE.py to LatinoAnalysis/Tools/python/userConfig.py and edit it to reflect your local paths. This is needed for batch jobs submission.

Compile all from CMSSW_13_3_1/src.

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

Finally, we can compute weights as a function of the jet eta on top of the one as a function of the jet pt, but using a finer pt binning (ProdRun2) ...

    ./runAnalysis.py --action=shapes --year=CAMPAIGNNAME --tag=System8KinematicsProdRun2.mujetpt/PtRelKinematicsProdRun2.mujetpt --sigset=MC
    ./runAnalysis.py --action=mergesingle --year=CAMPAIGNNAME --tag=System8KinematicsProdRun2.mujetpt/PtRelKinematicsProdRun2.mujetpt --sigset=MC
    ./runAnalysis.py --action=shapes --year=CAMPAIGNNAME --tag=System8KinematicsProdRun2/PtRelKinematicsProdRun2 --sigset=Data
    ./runAnalysis.py --action=mergesingle --year=CAMPAIGNNAME --tag=System8KinematicsProdRun2/PtRelKinematicsProdRun2 --sigset=Data
    ./runAnalysis.py --action=kinematicWeights --year=CAMPAIGNNAME --tag=System8KinematicsProdRun2.mujetpt/PtRelKinematicsProdRun2.mujetpt --option=mujeteta

... and try their effect:

    ./runAnalysis.py --action=shapes --year=CAMPAIGNNAME --tag=System8KinematicsProdRun2.mujetpt.mujeteta/PtRelKinematicsProdRun2.mujetpt.mujeteta --sigset=MC
    ./runAnalysis.py --action=mergesingle --year=CAMPAIGNNAME --tag=System8KinematicsProdRun2.mujetpt.mujeteta/PtRelKinematicsProdRun2.mujetpt.mujeteta --sigset=MC
    ./runAnalysis.py --action=plotKinematics --year=CAMPAIGNNAME --tag=System8KinematicsProdRun2.mujetpt.mujeteta/PtRelKinematicsProdRun2.mujetpt.mujeteta

## Production of templates for PtRel/System8 fits

First step is the production of the shapes for the System8/PtRel fits:

    ./runAnalysis.py --action=makeShapes --year=CAMPAIGNNAME --tag=System8Templates.mujetpt.mujeteta/PtRelTemplates.mujetpt.mujeteta

Shapes can be merged by

    ./runAnalysis.py --action=mergeShapes --year=CAMPAIGNNAME --tag=System8Templates.mujetpt.mujeteta/PtRelTemplates.mujetpt.mujeteta

If some shapes were missing, they can be recovered by doing:
  
    ./runAnalysis.py --action=resubmitShapes --year=CAMPAIGNNAME --tag=System8Templates.mujetpt.mujeteta/PtRelTemplatesMuPtDown.mujetpt.mujeteta

Finally, the format of the shapes need to be converted to the input format for the System8/PtRel fits: 

    ./runAnalysis.py --action=shapesForFit --year=CAMPAIGNNAME --tag=System8Templates.mujetpt.mujeteta/PtRelTemplates.mujetpt.mujeteta # To be complete

## Fits and scale factors


