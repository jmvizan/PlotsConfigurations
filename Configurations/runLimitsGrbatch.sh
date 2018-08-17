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

cd /gpfs/csic_users/sluca/Stop/CMSSW_8_0_26_patch1/src/PlotsConfigurations/Configurations/T2tt

cat $1 | while read line
do
   if [[ -n $line && "$line" != *"#"* ]]
   then
       ./runPointLimit.sh $line $2
   fi
done

