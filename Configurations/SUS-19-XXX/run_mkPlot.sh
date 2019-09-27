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
    else 
	TAG=$2
    fi
    if [ $# -lt 3 ]; then
	SIGSET='SM'
    else
	SIGSET=$3
    fi
fi

mkdir -p ./Plots/$YEAR/$TAG

mkPlot.py --pycfg=configuration.py --tag=$YEAR$TAG --sigset=$SIGSET --inputFile=./Shapes/$YEAR/plots_${TAG}_$SIGSET.root --outputDirPlots=./Plots/$YEAR/$TAG --maxLogCratio=1000 

cp ./Plots/index.php ./Plots/$YEAR/
cp ./Plots/index.php ./Plots/$YEAR/$TAG/

if [ $# -lt 4 ]; then
    rm ./Plots/$YEAR/$TAG/c_*
    rm ./Plots/$YEAR/$TAG/log_c_*
    rm ./Plots/$YEAR/$TAG/cdifference*
    rm ./Plots/$YEAR/$TAG/log_cdifference_*
fi
