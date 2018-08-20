
#!/bin/bash

echo "Creating postfit shapes for " $1
#
if [[ -z $3 || "$3" = *"asimov"* ]]
then
    ./mkPostFitShapes.py --pycfg=configuration.py --inputFileName=mlfit_asimov --workingDir=$1 --signalPoint=$2
fi
#
if [[ -z $3 || "$3" = *"data"* ]]
then
    ./mkPostFitShapes.py --pycfg=configuration.py --inputFileName=mlfit_data --workingDir=$1 --signalPoint=$2
fi
#
cd -




