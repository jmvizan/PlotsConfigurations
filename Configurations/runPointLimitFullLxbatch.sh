#!/bin/bash

echo "Processing " $1 

cd $2

eval `scramv1 runtime -sh`
source /afs/cern.ch/project/eos/installation/cms/etc/setup.sh

./createPointDatacards.sh $1 $3

cd /afs/cern.ch/work/s/scodella/Stop/CMSSW_7_4_7/

eval `scramv1 runtime -sh`
source /afs/cern.ch/project/eos/installation/cms/etc/setup.sh

cd $2

./combinePointDatacards.sh Datacards$3/MassPoint$1

./runPointLimit.sh $1 $3

rm -r Datacards$3/MassPoint$1/SR*
rm -r Datacards$3/MassPoint$1/*.txt
