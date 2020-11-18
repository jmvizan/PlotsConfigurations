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
    if [ $1 == '-1' ]; then
	YEAR='2016-2017-2018'
    elif [ $1 == '0' ]; then
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
    if [ $# -lt 4 ]; then
	FILESET=$SIGSET
        NORM='None'
    elif [ $# -eq 4 ]; then
        if [ $4 == 'Norm' ] || [ $4 == 'CRnorm' ]; then 
	    NORM=$4
	    FILESET='SM'
	else
	    NORM='None'
	    FILESET=$4
	fi
    else
        if [ $4 == 'Norm' ] || [ $4 == 'CRnorm' ]; then 
	    NORM=$4
	    FILESET=$5
	else
	    NORM=$5
	    FILESET=$4
	fi
    fi
fi

mkdir -p ./Plots/$YEAR/$TAG

NUISANCES=nuisances.py
if [[ $YEAR == *'-'* ]]; then
    ./mergeShapes.py --years=$YEAR --tag=$TAG --sigset=$SIGSET --saveNuisances
    NUISANCES=nuisances_${YEAR}_${TAG}_${SIGSET}.py
fi

if [[ $SIGSET == 'SM'* ]] || [[ $SIGSET == 'Backgrounds'* ]]; then
    if [ $NORM == 'Norm' ]; then
	mkPlot.py --pycfg=configuration.py --tag=$YEAR$TAG --sigset=$SIGSET --inputFile=./Shapes/$YEAR/$TAG/plots_${TAG}_$FILESET.root --outputDirPlots=./Plots/$YEAR/$TAG --maxLogCratio=1000 --minLogCratio=0.1 --scaleToPlot=2 --plotNormalizedDistributions=1 --nuisancesFile=None --showIntegralLegend=1
    elif [ $NORM == 'CRnorm' ]; then
	mkPlot.py --pycfg=configuration.py --tag=$YEAR$TAG --sigset=$SIGSET --inputFile=./Shapes/$YEAR/$TAG/plots_${TAG}_$FILESET.root --outputDirPlots=./Plots/$YEAR/$TAG --maxLogCratio=1000 --minLogCratio=0.1 --scaleToPlot=2 --plotNormalizedCRratio=1 --nuisancesFile=$NUISANCES
    else
	mkPlot.py --pycfg=configuration.py --tag=$YEAR$TAG --sigset=$SIGSET --inputFile=./Shapes/$YEAR/$TAG/plots_${TAG}_$FILESET.root --outputDirPlots=./Plots/$YEAR/$TAG --maxLogCratio=1000 --minLogCratio=0.1 --scaleToPlot=2 --showIntegralLegend=1  --nuisancesFile=$NUISANCES  --fileFormats='png,root,C'
    fi
else 
    mkPlot.py --pycfg=configuration.py --tag=$YEAR$TAG --sigset=$SIGSET --inputFile=./Shapes/$YEAR/$TAG/plots_${TAG}_$FILESET.root --outputDirPlots=./Plots/$YEAR/$TAG --maxLogCratio=1000 --minLogCratio=0.1 --scaleToPlot=2 --nuisancesFile=None --showIntegralLegend=1
fi 

if [[ $YEAR == *'-'* ]]; then # To keep clean
    rm nuisances_${YEAR}_${TAG}_${SIGSET}.py
fi

cp ./Plots/index.php ./Plots/$YEAR/
cp ./Plots/index.php ./Plots/$YEAR/$TAG/

if [ $# -lt 5 ]; then
    if [[ $SIGSET == 'SM'* ]]; then  
	rm ./Plots/$YEAR/$TAG/c_*
	rm ./Plots/$YEAR/$TAG/log_c_*
    else
	rm ./Plots/$YEAR/$TAG/cratio_*
	rm ./Plots/$YEAR/$TAG/log_cratio_*
    fi
    rm ./Plots/$YEAR/$TAG/cdifference*
    rm ./Plots/$YEAR/$TAG/log_cdifference*
fi
