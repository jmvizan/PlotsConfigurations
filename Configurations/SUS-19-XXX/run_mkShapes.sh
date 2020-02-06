#!/bin/bash

if [ $# == 0 ]; then
    echo ''
    echo 'Please provide data taking year:'; 
    echo '  0. 2016 '
    echo '  1. 2017'
    echo '  2. 2018'
    echo ''
    exit
elif [ $# == 1 ]; then
    echo ''
    echo 'Please provide tag value:'; 
    echo '  0. Preselection: shapes for data/MC comparison of various kinematic observables '
    echo '  1. ValidationRegions'
    echo '  2. StopSignalRegions'
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
    if [ $2 == '0' ]; then
	TAG='Preselection'
    elif [ $2 == '1' ]; then
	TAG='ValidationRegions'
    elif [ $2 == '2' ]; then
	TAG='StopSignalRegions'
    else 
	TAG=$2
    fi
    if [ $# == 2 ] || [ $3 == '0' ] || [ $3 == 'shapes' ]; then
	BATCH=True
	QUEUE=testmatch
	DOHADD=False
	KEEPINPUT=False
    else
	BATCH=False
	QUEUE=''
	DOHADD=True
	KEEPINPUT=True
    fi
    if [ $# -lt 4 ]; then
	SIGSET='SM'
	if [ $TAG == 'btagefficiencies' ]; then
	    SIGSET='Backgrounds'
	fi
	SPLIT='Samples'
    else
	SIGSET=$4
	if [ $# -lt 5 ]; then
	    SPLIT='Samples'
	else
	    SPLIT=$5
	fi
    fi
fi

mkdir -p ./Shapes/$YEAR/$SPLIT

if [ $BATCH == True ]; then
    mkShapes.py --pycfg=configuration.py --tag=$YEAR$TAG --sigset=$SIGSET --treeName=Events --outputDir=./Shapes/$YEAR/$SPLIT --doBatch=True --batchQueue=testmatch --batchSplit=$SPLIT
else 
    rm ./Shapes/$YEAR/$SPLIT/*_temp*.root
    mkShapes.py --pycfg=configuration.py --tag=$YEAR$TAG --sigset=$SIGSET --treeName=Events --outputDir=./Shapes/$YEAR/$SPLIT --batchSplit=$SPLIT --doHadd=True --doNotCleanup 
    if [[ "$SIGSET" == "Backgrounds"* ]] && [[ "$SIGSET" != "Backgrounds-"* ]] && [[ "$SIGSET" != "Backgrounds" ]]; then
	ONLYSAMPLE=${SIGSET#Backgrounds}
	mv ./Shapes/$YEAR/$SPLIT/plots_$YEAR$TAG.root ./Shapes/$YEAR/Samples/plots_${TAG}_ALL_${ONLYSAMPLE}.root
    else
	mv ./Shapes/$YEAR/$SPLIT/plots_$YEAR$TAG.root ./Shapes/$YEAR/plots_${TAG}_${SIGSET}.root 
    fi
    rm ./Shapes/$YEAR/$SPLIT/*_temp*.root   
fi

#mkShapes.py --pycfg=configuration.py --tag=$TAG --treeName=Events --outputDir=./Shapes --doBatch=$BATCH --batchQueue=$QUEUE --batchSplit=Samples --doHadd=$DOHADD --doNotCleanup]==$KEEPINPUT
