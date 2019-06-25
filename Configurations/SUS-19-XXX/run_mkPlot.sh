#!/bin/bash

if [ $# == 0 ]; then
    echo ''
    echo 'Please provide tag value:'; 
    echo '  0. Preselection: shapes for data/MC comparison of various kinematic observables '
    echo ''
    exit
else
    if [ $1 == '0' ]; then
	TAG='Preselection'
    else 
	TAG=$1
    fi
    if [ $# <2 ]; then
	SIGSET='SM'
    else
	SIGSET=$2
    fi
fi

mkPlot.py --pycfg=configuration.py --tag=$TAG --inputFile=./Shapes/plots_$TAG_$SIGSET.root --outputDirPlots=./Plots/$TAG --maxLogCratio=1000 

cp ./Plots/index.php ./Plots/$TAG/

if [ $# == 1 ]; then
    rm ./Plots/$TAG/c_*
    rm ./Plots/$TAG/log_c_*
    rm ./Plots/$TAG/cdifference*
    rm ./Plots/$TAG/log_cdifference_*
fi
