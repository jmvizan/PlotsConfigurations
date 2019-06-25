#!/bin/bash

if [ $# -lt 2 ]; then
    echo ''
    echo 'Please provide tag value:'; 
    echo '  Ex.: SignalRegions'
    echo ''
    echo 'Please provide signal mass point value:'; 
    echo '  Ex.: T2tt_mS-450_mX-350'
    echo ''
    exit
else
    TAG=$1
    SIGSET='SM-'$2
    if [ $# == 2 ]; then
	FILESET='SM-'$2
    else
	FILESET=$3
    fi
fi

mkDatacards.py --pycfg=configuration.py --tag=$TAG --sigset=$SIGSET --outputDirDatacard=./Datacards/$2 --inputFile=./Shapes/plots_${TAG}_${FILESET}.root 
