#!/bin/bash
#$ -P l.gaes
#$ -S /bin/bash
#$ -cwd
#$ -t 1-1
#$ -N HiggsCombine
#$ -o jobs/job_$JOB_ID-$TASK_ID.out
#$ -j y

cd /gpfs/csic_users/sluca/Stop/CMSSW_7_4_7/src/

source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scramv1 runtime -sh`

cd $2

./runPointLimit.sh $1 $3


