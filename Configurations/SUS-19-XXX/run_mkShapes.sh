#!/bin/bash

if [ $# == 0 ]; then
    echo ''
    echo 'Please provide tag value:'; 
    echo '  0. Preselection: shapes for data/MC comparison of various kinematic observables '
    echo '  1. ValidationRegions'
    echo '  2. SignalRegions'
    echo ''
    exit
else
    if [ $1 == '0' ]; then
	TAG='Preselection'
    elif [ $1 == '1' ]; then
	TAG='ValidationRegions'
    elif [ $1 == '2' ]; then
	TAG='SignalRegions'
    else 
	TAG=$1
    fi
    if [ $# == 1 ] || [ $2 == '0' ] || [ $2 == 'shapes' ]; then
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
    if [ $# -lt 3 ]; then
	SIGSET='SM'
	SPLIT=Samples
    else
	SIGSET=$3
	if [ $# -lt 4 ]; then
	    SPLIT=Samples
	else
	    SPLIT=$4
	fi
    fi
fi

if [ $BATCH == True ]; then
    mkShapes.py --pycfg=configuration.py --tag=$TAG --sigset=$SIGSET --treeName=Events --outputDir=./Shapes/$SPLIT --doBatch=True --batchQueue=testmatch --batchSplit=$SPLIT
else 
    mkShapes.py --pycfg=configuration.py --tag=$TAG --sigset=$SIGSET --treeName=Events --outputDir=./Shapes/$SPLIT --batchSplit=$SPLIT --doHadd=True --doNotCleanup 
    mv ./Shapes/$SPLIT/plots_$TAG.root ./Shapes/plots_${TAG}_${SIGSET}.root    
fi

#mkShapes.py --pycfg=configuration.py --tag=$TAG --treeName=Events --outputDir=./Shapes --doBatch=$BATCH --batchQueue=$QUEUE --batchSplit=Samples --doHadd=$DOHADD --doNotCleanup]==$KEEPINPUT
