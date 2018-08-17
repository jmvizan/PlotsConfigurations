#!/bin/bash

export WORKDIRECTORY=$PWD

mkdir -p jobs

cd jobs/

bsub -q cmscaf1nd -o $WORKDIRECTORY/jobs $WORKDIRECTORY/runPointFit.sh $WORKDIRECTORY/$1 $2 

