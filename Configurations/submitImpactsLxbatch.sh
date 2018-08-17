#!/bin/bash

export WORKDIRECTORY=$PWD

mkdir -p jobs

cd jobs/

bsub -q cmscaf1nd -o $WORKDIRECTORY/jobs $WORKDIRECTORY/runPointImpacts.sh $WORKDIRECTORY/$1 

