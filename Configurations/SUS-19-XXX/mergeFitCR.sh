#!/bin/bash

if [ $# -lt 2 ]; then
    exit
fi

SHAPEDIR=./Shapes

intag=$2

addCR=0
if [[ $intag == *'FitCR'* ]]; then
    addCR=1
fi

sample=''
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

    if [[ $year == '2016'* ]] || [ $year == '2017' ] || [ $year == '2018' ]; then

        mkdir -p $SHAPEDIR/$year/$intag
        filename=$SHAPEDIR/$year/$intag/plots_${intag}

        infile=${filename}_SM.root
        if test -f "$infile"; then
            echo "$infile exists, will use it."
        else
            smtag="${intag/FitCR/}"
            infile=$SHAPEDIR/$year/$smtag/plots_${smtag}_SM.root
        fi
   
        # Check if tag was already merged
        outfile=${filename}_SM-$sample.root
        if test -f "$outfile"; then
            echo "$outfile exists already."
        else

            sigtag=$intag
            if [ $addCR == '1' ]; then
                sigtag="${intag/FitCR/}"
            fi
            sigfile=$SHAPEDIR/$year/$sigtag/plots_${sigtag}_$sample.root
        
            wztag="${intag/FitCR/FitCRWZ}"
            wzfile=$SHAPEDIR/$year/$wztag/plots_${wztag}_SM.root
        
            zztag="${intag/FitCR/FitCRZZ}"
            zzfile=$SHAPEDIR/$year/$zztag/plots_${zztag}_SM.root   

            ttztag="${intag/FitCR/FitCRttZ}"
            ttzfile=$SHAPEDIR/$year/$ttztag/plots_${ttztag}_SM.root
            if [ $addCR == '1' ]; then    
                ../../../LatinoAnalysis//Tools/scripts/haddfast --compress $outfile $infile $sigfile $wzfile $zzfile $ttzfile
            else
                ../../../LatinoAnalysis//Tools/scripts/haddfast --compress $outfile $infile $sigfile 
            fi

        fi

    else
        echo 'Not supported year:' $year
    fi

done





