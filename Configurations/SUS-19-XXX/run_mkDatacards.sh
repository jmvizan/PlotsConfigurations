#!/bin/bash

if [ $# -lt 3 ]; then
    echo ''
    echo 'Please provide data taking year:'; 
    echo '  0. 2016 '
    echo '  1. 2017'
    echo '  2. 2018'
    echo ''
    echo 'Please provide tag value:'; 
    echo '  Ex.: SignalRegions'
    echo ''
    echo 'Please provide signal mass point value:'; 
    echo '  Ex.: T2tt_mS-450_mX-350'
    echo ''
    exit
else
    if [ $1 == '0' ]; then
	YEAR='2016'
    elif [ $1 == '1' ]; then
	YEAR='2017'
    elif [ $1 == '2' ]; then
	YEAR='2018'	
    else 
	YEAR=$1
    fi
    TAG=$2
    SIGSET='SM-'$3
    if [ $# == 3 ]; then
	FILESET=$SIGSET
    else
	FILESET=$4
    fi
fi

mkdir -p ./Datacards/$YEAR

mkDatacards.py --pycfg=configuration.py --tag=$YEAR$TAG --sigset=$SIGSET --outputDirDatacard=./Datacards/$YEAR/$3 --inputFile=./Shapes/$YEAR/plots_${TAG}_${FILESET}.root 
