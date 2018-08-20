#!/bin/bash

cd /afs/cern.ch/work/s/scodella/Stop/CMSSW_7_4_7/

eval `scramv1 runtime -sh`
source /afs/cern.ch/project/eos/installation/cms/etc/setup.sh

cd $2

./runPointLimit.sh $1 $3

