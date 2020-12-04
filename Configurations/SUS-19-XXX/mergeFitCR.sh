#!/bin/bash

if [ $# -lt 2 ]; then
    exit
fi

intag=$2

if [[ $intag != *'FitCR'* ]]; then
    echo 'Wrong input tag' $intag
fi

sample='SM'
if [ $# -gt 2 ]; then
    sample=$3
fi

if [ $1 == '-1' ]; then
    years='2016-2017-2018'
elif [ $1 == '0' ]; then
    years='2016'
elif [ $1 == '1' ]; then
    years='2017'
elif [ $1 == '2' ]; then
    years='2018'
else
    years=$1
fi

IFS=- read -ra yearlist <<< $years
for year in "${yearlist[@]}"; do

    if [ $year == '2016' ] || [ $year == '2017' ] || [ $year == '2018' ]; then

        filename=./Shapes/$year/$intag/plots_${intag}_SM-${sample}

        # Check if tag was already merged
        backupfile=${filename}_backout.root
        if test -f "$backupfile"; then
            echo "$backupfile exists already."
        else

            outfile=${filename}_merge.root

            infile=${filename}.root
        
            wztag="${intag/FitCR/FitCRWZ}"
            wzfile=./Shapes/$year/$wztag/plots_${wztag}_SM.root
        
            zztag="${intag/FitCR/FitCRZZ}"
            zzfile=./Shapes/$year/$zztag/plots_${zztag}_SM.root   

            ttztag="${intag/FitCR/FitCRttZ}"
            ttzfile=./Shapes/$year/$ttztag/plots_${ttztag}_SM.root

            ../../../LatinoAnalysis//Tools/scripts/haddfast --compress $outfile $infile $wzfile $zzfile $ttzfile

            mv $infile  $backupfile
            mv $outfile $infile

        fi

    else
        echo 'Not supported year:' $year
    fi

done






